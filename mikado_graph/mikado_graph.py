import argparse
from collections import defaultdict, namedtuple
import time
import os

from graphviz import Digraph
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


Edge = namedtuple('Edge', ['src', 'dst', 'done'])
Node = namedtuple('Node', ['name', 'done', 'goal'])
DONE_SYMBOLS = ['x', 'X', 'v', 'V']
COMMENT_SYMBOLS = ['#', '//']

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate mikado graph from description.')

    parser.add_argument('file', type=str, help='Mikado description file')
    parser.add_argument('-o', '--output', type=str, help='Mikado graph output file base name (no extension)')
    parser.add_argument('-f', '--format', type=str, default='pdf', help='Mikado graph output format (default: pdf)')
    parser.add_argument('-v', '--view', action='store_true', help='View generated Mikado graph')
    parser.add_argument('-w', '--watch', action='store_true',
                        help='Watch Mikado description file for changes and regenerate graph')

    return parser.parse_args()

def cleanup_test_to_comply_with_dot(line):
    return line \
        .replace(':', 'ː') \
        .replace('(', '\\(') \
        .replace(')', '\\)') \

def parse_mikado_description(description_file):
    with open(description_file, 'r') as file:
        text = file.read()
        lines = text.split('\n')

        lines = list(filter(lambda line: all(symbol not in line.lstrip() for symbol in COMMENT_SYMBOLS), lines))
        lines = list(map(cleanup_test_to_comply_with_dot, lines))
        lines = list(map(lambda line: line.replace('\t', ' ' * 4), lines))
        tasks = list((line.lstrip(), _depth_level(line)) for line in lines if len(line) > 0)

        nodes = list(Node(name=_task_strip(task), done=_task_done(task), goal=depth==0) for task, depth in set(tasks))
        edges = list(Edge(src=_task_strip(src), dst=_task_strip(dst), done=_task_done(src) and _task_done(dst))
                         for src, dst in set(_mikado_pairs(tasks, list(), list())))

        return nodes, edges

def _task_done(task):
    return any(task.startswith(symbol) for symbol in DONE_SYMBOLS)

def _task_strip(task):
    return ' '.join(task.split(' ')[1:]).lstrip()

def _depth_level(line):
    return int(_count_indentation(line) / 4)

def _count_indentation(line, count=0):
    if line.startswith(' '): return _count_indentation(line[1:], count + 1)
    else:                    return count

def _mikado_pairs(tasks, mikado_pairs, parents):
    if len(tasks) == 0: return mikado_pairs

    child, depth = tasks[0]

    if len(parents):
        mikado_pairs.append((parents[-(len(parents) - depth + 1)], child))

    if len(parents) != depth:
        return _mikado_pairs(tasks=tasks[1:], mikado_pairs=mikado_pairs, parents=[*parents[:depth], child])
    else:
        return _mikado_pairs(tasks=tasks[1:], mikado_pairs=mikado_pairs, parents=[*parents, child])

def draw_mikado_graph(nodes, edges, format):
    graph = Digraph(strict=True, format=format)
    graph.attr(rankdir='BT')
    for node in nodes: _append_node(graph, node)
    for edge in edges: _append_edge(graph, edge)
    return graph

def _append_node(graph, node):
    color = 'darkgreen' if node.done else 'firebrick'
    graph.node(node.name, color=color, fontcolor=color, peripheries='2' if node.goal else '1')

def _append_edge(graph, edge):
    color = 'darkgreen' if edge.done else 'firebrick'
    graph.edge(edge.src, edge.dst, color=color)

def render_graph(mikado_description, view, output_file, format):
    graph = draw_mikado_graph(*parse_mikado_description(mikado_description), format=format)

    output_dir = os.path.dirname(output_file or '')
    output_gv = os.path.join(output_dir, os.path.basename(output_file or 'graph') + '.gv')
    graph.render(filename=output_gv, view=view, cleanup=True)

    if output_file:
        graph.save(output_file)

def main():
    args = parse_arguments()

    render_graph(args.file, args.view, args.output, args.format)

    if args.watch:
        class MikadoGraphWatcher(FileSystemEventHandler):
            def on_modified(self, event):
                if event == FileModifiedEvent(os.path.join('.', args.file)):
                    render_graph(args.file, args.view, args.output, args.format)

        event_handler = MikadoGraphWatcher()
        observer = Observer()
        observer.schedule(event_handler, path=os.path.dirname(args.file) or '.', recursive=False)
        observer.start()

        try:
            while True: time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()

if __name__ == '__main__':
    main()
