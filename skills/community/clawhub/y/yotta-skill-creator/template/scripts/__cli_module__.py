#!/usr/bin/env python3
"""{{skill_name}}: {{summary}}

零依赖（Python 3.8+ 标准库）。用法:
  python3 scripts/{{cli_module}}.py <子命令> [选项]
"""
import argparse
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

VERSION = "0.1.0"


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="{{skill_name}}",
        description="{{description}}",
    )
    ap.add_argument("--version", action="version", version="%(prog)s " + VERSION)
    sub = ap.add_subparsers(dest="command")

    p_hello = sub.add_parser("hello", help="示例子命令")
    p_hello.add_argument("--name", default="agent", help="称呼")
    p_hello.set_defaults(func=cmd_hello)

    args = ap.parse_args(argv)
    if not getattr(args, "func", None):
        ap.print_help()
        return 0
    return args.func(args)


def cmd_hello(args):
    print("hello, %s! 这是 {{skill_name}} v" % args.name + VERSION)
    return 0


if __name__ == "__main__":
    sys.exit(main())