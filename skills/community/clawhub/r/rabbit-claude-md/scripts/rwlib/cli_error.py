"""
cli_error.py - LLM-friendly CLI argument and I/O error formatting utilities.

When an LLM agent executes a script with missing or invalid arguments,
standard argparse output or raw python tracebacks fail to provide explicit
context on argument requirements, data types, and valid invocation patterns.

This module provides LLMArgumentParser (a custom argparse.ArgumentParser)
and error formatting helpers that output structured, clear error guidance
to stderr for consumption by LLMs and human users.
"""

import argparse
import os
import sys


def format_llm_error(script_name, error_message, parser=None, examples=None):
    """Format a detailed, structured CLI error message for an LLM agent."""
    out = []
    out.append("=" * 70)
    out.append(f"CLI ERROR: {error_message}")
    out.append("=" * 70)
    out.append(f"Script: {script_name}")

    if parser and parser.description:
        desc_lines = parser.description.strip().splitlines()
        if desc_lines:
            out.append(f"Description: {desc_lines[0]}")

    if parser and hasattr(parser, "_actions"):
        out.append("\nREQUIRED & OPTIONAL PARAMETERS:")
        for action in parser._actions:
            if action.dest == "help" or action.help == argparse.SUPPRESS:
                continue

            names = action.option_strings if action.option_strings else [action.dest]
            name_str = ", ".join(names)

            is_positional = not action.option_strings
            is_required = action.required or (is_positional and action.nargs not in ('?', '*'))
            status = "REQUIRED" if is_required else "OPTIONAL"

            if action.choices:
                type_str = f"choice [{', '.join(str(c) for c in action.choices)}]"
            elif action.type:
                type_str = getattr(action.type, '__name__', str(action.type))
            elif isinstance(action, (argparse._StoreTrueAction, argparse._StoreFalseAction)):
                type_str = "boolean flag"
            elif is_positional and action.nargs in ('+', '*'):
                type_str = "list of file paths / strings"
            else:
                type_str = "file path / string"

            help_text = action.help or "No description provided."
            default_info = ""
            if not is_required and action.default not in (None, argparse.SUPPRESS) and action.default is not False:
                default_info = f" (default: {action.default})"

            out.append(f"  - {name_str} ({status}, type: {type_str}){default_info}")
            out.append(f"    Purpose: {help_text}")

    if examples:
        out.append("\nVALID USAGE EXAMPLES:")
        for ex in examples:
            out.append(f"  {ex}")
    elif parser and hasattr(parser, "epilog") and parser.epilog:
        out.append(f"\n{parser.epilog}")

    out.append("=" * 70)
    return "\n".join(out)


def format_file_error(script_name, path, parameter_name, expected_type="file path", details=None, examples=None):
    """Format an I/O or missing file error message for an LLM agent."""
    out = []
    out.append("=" * 70)
    out.append("FILE / I/O ERROR: Target path is invalid or unreadable.")
    out.append("=" * 70)
    out.append(f"Script: {script_name}")
    out.append(f"Parameter: '{parameter_name}' (expected type: {expected_type})")
    out.append(f"Provided Path: {path!r}")
    if details:
        out.append(f"Details: {details}")
    if examples:
        out.append("\nVALID USAGE EXAMPLES:")
        for ex in examples:
            out.append(f"  {ex}")
    out.append("=" * 70)
    return "\n".join(out)


class LLMArgumentParser(argparse.ArgumentParser):
    """Custom ArgumentParser subclass that emits structured LLM error messages on failure."""

    def __init__(self, *args, examples=None, **kwargs):
        self.examples = examples or []
        super().__init__(*args, **kwargs)

    def error(self, message):
        formatted = format_llm_error(
            script_name=os.path.basename(self.prog),
            error_message=message,
            parser=self,
            examples=self.examples
        )
        sys.stderr.write(formatted + "\n")
        sys.exit(2)
