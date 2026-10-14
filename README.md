# tasky

A tiny task manager CLI, written as a learning project. Pure standard library,
no runtime dependencies.

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
tasky add "buy milk"     # add a task
tasky list               # list pending tasks
tasky list --all         # include completed tasks
tasky done 1             # mark task 1 as completed
tasky rm 1               # remove task 1
tasky clear              # remove all completed tasks
```

Tasks are stored as JSON under `$XDG_DATA_HOME/tasky/tasks.json`
(default: `~/.local/share/tasky/tasks.json`). Override with `--file PATH`:

```bash
tasky --file ./tasks.json list
```

You can also run it without installing:

```bash
python -m tasky add "hello"
```

## Development

```bash
python -m pip install -e ".[dev]"
pytest
```

## Layout

```
src/tasky/
  __init__.py   # version
  __main__.py   # python -m tasky entry point
  models.py     # Task dataclass
  storage.py    # JSON persistence
  cli.py        # argparse CLI
tests/
  test_storage.py
  test_cli.py
```
