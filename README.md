# Mikado Graph

Python tool to draw graphs for Mikado refactoring.

## Install

```bash
virtualenv -p python3 env
source env/bin/activate
pip install watchdog graphviz
```

## Usage

```bash
python mikado-graph/mikado_graph.py mikado-graph/mikado_example.txt --view
```
will draw the graph from the specified input file and display it.

Explore the options using `--help`
```bash
python mikado-graph/mikado_graph.py --help
```

## Graph description symbols

Parent/child dependency is encoded by indentation.

There are three kinds of nodes in the graph
- Comments are prefixed by one of the following symbol: `//`, `#`
- Done tasks (drawn in green) are prefixed by one of the following symbols: `v`, `V`, `x`, `X`
- Pending tasks (drawn in red) are prefixed by any symbol that is not used by the above two choices.
  We recommend using `_` to keep the description file human readable


## Known issues

- `graphviz` will always save a temporary file when asked to render the graph.
