#!/usr/bin/env python3
"""Legacy compatibility wrapper for the new parser."""

from nlu.parser import CommandParser


class IntentEngine:
    def __init__(self):
        self.parser = CommandParser()

    def parse(self, command: str):
        return self.parser.parse(command)
