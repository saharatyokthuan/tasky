from __future__ import annotations

import argparse
import sys

from . import __version__
from .models import Task
from .storage import Store, TaskNotFound


def _format(task: Task) -> str:
    mark = "x" if task.done else " "
    return f"[{mark}] {task.id:>3}  {task.title}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tasky",
        description="A tiny task manager.",
    )
    parser.add_argument("--version", action="version", version=f"tasky {__version__}")
    parser.add_argument(
        "--file",
        metavar="PATH",
        help="use a custom store file instead of the default location",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a new task")
    p_add.add_argument("title", help="task description")

    p_list = sub.add_parser("list", help="list tasks")
    p_list.add_argument("-a", "--all", action="store_true", help="include completed tasks")

    p_done = sub.add_parser("done", help="mark a task as completed")
    p_done.add_argument("id", type=int)

    p_rm = sub.add_parser("rm", help="remove a task")
    p_rm.add_argument("id", type=int)

    sub.add_parser("clear", help="remove all completed tasks")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = Store(args.file)

    try:
        if args.command == "add":
            task = store.add(args.title)
            print(f"added: {_format(task)}")

        elif args.command == "list":
            tasks = store.all(include_done=args.all)
            if not tasks:
                print("no tasks")
                return 0
            for task in tasks:
                print(_format(task))

        elif args.command == "done":
            print(f"done: {_format(store.complete(args.id))}")

        elif args.command == "rm":
            print(f"removed: {_format(store.remove(args.id))}")

        elif args.command == "clear":
            count = store.clear_done()
            print(f"removed {count} completed task(s)")

    except TaskNotFound as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
