#!/usr/bin/env python3

# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""
Remind Me - Create, list, and cancel cron-based reminders scoped to a channel.

Usage:
    uv run main.py create <name> <message> <schedule> <channel> <to> [once] [tz:<timezone>]
    uv run main.py list <channel> <to>
    uv run main.py cancel id <jobId>
    uv run main.py cancel name <name>

Schedule format:
    every:<duration>   e.g. every:30m  every:1h
    cron:<expr>        e.g. cron:0 9 * * 1-5
    at:<duration>      e.g. at:20m  at:2h

Timezone format (optional, for create only):
    tz:<IANA>          e.g. tz:Europe/London  tz:America/New_York
    If omitted, falls back to UTC or whatever is resolved from USER.md by the AI.
"""

import sys

from service import format_cancel_output, format_create_output, format_list_output

USAGE = """\
Usage:
  remind-me create <name> <message> <schedule> <channel> <to> [once] [tz:<timezone>]
  remind-me list   <channel> <to>
  remind-me cancel id   <jobId>
  remind-me cancel name <name>

Timezone (optional, create only):
  Pass tz:<IANA> anywhere after the required args.
  e.g. tz:Europe/London  tz:America/New_York  tz:Africa/Lagos
  Omit to fall back to UTC.
"""


def _extract_flag(args: list[str], prefix: str) -> tuple[str | None, list[str]]:
    """Extract the first argument that starts with a given prefix, returning its value and the remaining args.

    Returns (value, remaining_args). Value does not include the prefix itself.
    If no match is found, returns (None, original_args).
    """
    for i, arg in enumerate(args):
        if arg.startswith(prefix):
            value = arg[len(prefix) :]
            remaining = args[:i] + args[i + 1 :]
            return value, remaining
    return None, args


def main():
    """Entry point — reads positional args and dispatches to the correct service function."""
    args = sys.argv[1:]

    if not args:
        print(USAGE)
        sys.exit(1)

    command = args[0].lower()

    if command == "create":
        # create <name> <message> <schedule> <channel> <to> [once] [tz:<timezone>]
        # First strip optional tz: flag from anywhere in the tail args
        remaining = args[1:]
        timezone, remaining = _extract_flag(remaining, "tz:")

        if len(remaining) < 5:
            print(
                "Usage: remind-me create <name> <message> <schedule> <channel> <to> [once] [tz:<timezone>]"
            )
            sys.exit(1)

        name = remaining[0]
        message = remaining[1]
        schedule = remaining[2]
        channel = remaining[3]
        to = remaining[4]

        # 'once' can appear as the 6th positional arg (index 5)
        once = len(remaining) >= 6 and remaining[5].lower() == "once"

        print(
            format_create_output(name, message, schedule, channel, to, once, timezone)
        )

    elif command == "list":
        # list <channel> <to>
        if len(args) < 3:
            print("Usage: remind-me list <channel> <to>")
            sys.exit(1)
        channel = args[1]
        to = args[2]
        print(format_list_output(channel, to))

    elif command == "cancel":
        # cancel id <jobId>  |  cancel name <name>
        if len(args) < 3:
            print(
                "Usage: remind-me cancel id <jobId>  OR  remind-me cancel name <name>"
            )
            sys.exit(1)
        by = args[1].lower()
        value = args[2]
        if by == "id":
            print(format_cancel_output(job_id=value, name=None))
        elif by == "name":
            print(format_cancel_output(job_id=None, name=value))
        else:
            print(f"Error: Unknown cancel mode '{by}'. Use 'id' or 'name'.")
            sys.exit(1)

    else:
        print(f"Error: Unknown command '{command}'.\n")
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
