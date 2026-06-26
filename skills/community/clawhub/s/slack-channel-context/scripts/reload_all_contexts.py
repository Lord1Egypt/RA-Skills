#!/usr/bin/env python3
"""
Reload all Slack channel context files.

This script forces a cache bypass for all context files in the slack-channel-contexts directory.
Use this after editing context files to ensure the changes are picked up immediately.

Usage:
    python reload_all_contexts.py
"""

import os
import sys

# Add the skills directory to the path
skills_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, skills_dir)

from load_context import SlackContextLoader


def reload_all_contexts():
    """Reload all channel context files, bypassing cache."""
    loader = SlackContextLoader()
    contexts_dir = loader.contexts_dir

    print(f"Context directory: {contexts_dir}")
    print("Reloading all context files...\n")

    # Get all .md files
    md_files = [f for f in os.listdir(contexts_dir) if f.endswith(".md")]

    if not md_files:
        print("No context files found!")
        return

    print(f"Found {len(md_files)} context file(s):\n")

    for file in sorted(md_files):
        # Skip README.md
        if file == "README.md":
            continue

        # Extract channel name from filename (remove .md extension)
        channel_name = file[:-3]  # Remove .md

        try:
            # Force reload this context
            context = loader.load_context(channel_name=channel_name, force_reload=True)

            if context:
                print(f"Reloaded: {file}")
            else:
                print(f"Context not found for: {file}")

        except Exception as e:
            print(f"Error reloading {file}: {e}")

    print(f"\nDone! All {len(md_files)} context file(s) reloaded.")
    print(
        "\nTip: Next time you message in a Slack channel, the updated context will be used."
    )


if __name__ == "__main__":
    reload_all_contexts()
