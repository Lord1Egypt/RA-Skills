#!/usr/bin/env python3
"""Centralized argument parser wrapper for spex CLI scripts."""

from __future__ import annotations

import argparse


class ArgumentParser(argparse.ArgumentParser):
    """Thin wrapper around argparse.ArgumentParser.

    Usage::

        parser = ArgumentParser(prog="spex todo-helper xml2json")
        parser.add_argument("xml_file")
        parser.add_argument("-a", "--append", action="store_true")
        args = parser.parse()  # defaults to sys.argv[1:]
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("allow_abbrev", False)
        super().__init__(*args, **kwargs)

    def parse(self, argv=None):
        """Parse arguments from a list, defaulting to sys.argv[1:]."""
        return self.parse_args(argv)

    def parse_known(self, argv=None):
        """Parse known arguments, returning (args, remaining)."""
        return self.parse_known_args(argv)
