# Mikado Graph

Python tool to draw graphs for Mikado refactoring.

## Quickstart

Start by saving this description file as as `example.txt`
```
_ Extend X with Y
    x Remove flag Z from X
        x Replace D with E
            x Check C
    # Ignore this line
    _ Add field X in Y
        x Do fix A
        _ Add B
        x Check C
```
Then run
```bash
pip install mikado-graph
mikado example.txt --view
```
A new window should display the graph below
![Example graph](https://raw.githubusercontent.com/SyrianSpock/mikado-graph/master/example.png)

Explore the options using `--help`
```bash
mikado --help
```
And learn more about the description file format below.

## Graph description symbols

Parent/child dependency is encoded by indentation.

There are three kinds of nodes in the graph
- Comments are prefixed by one of the following symbol: `//`, `#`
- Done tasks (drawn in green) are prefixed by one of the following symbols: `v`, `V`, `x`, `X`
- Pending tasks (drawn in red) are prefixed by any symbol that is not used by the above two choices.
  We recommend using `_` to keep the description file human readable

## Dev & Deploy

Deploy by running
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Known issues

- `graphviz` will always save a temporary file when asked to render the graph.
