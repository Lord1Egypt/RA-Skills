#!/usr/bin/env python3
"""
Slack Channel Context Loader - Legacy Module

Loads Slack channel context files from slack-channel-contexts/ directory.
Context files are named simply as <CHANNEL_ID>.md or <CHANNEL_NAME>.md.

This module is kept for backward compatibility.
Use scripts/skill.py for new implementations.
"""

import os
from pathlib import Path
from datetime import datetime, timedelta


class SlackContextLoader:
    """Loads Slack channel context files into session."""

    def __init__(self, workspace_dir=None):
        self.workspace = (
            Path(workspace_dir).expanduser()
            if workspace_dir
            else Path.home() / ".openclaw" / "workspace"
        )

        # Check if skill is enabled (default: true)
        enabled_env = os.environ.get("SLACK_CONTEXT_ENABLED", "true").lower()
        self.enabled = enabled_env in ("true", "1", "yes", "on")

        # Check if loading on thread start is enabled (default: true)
        # This allows disabling context loading in threaded messages
        load_on_threads_env = os.environ.get(
            "SLACK_CONTEXT_LOAD_ON_THREADS", "true"
        ).lower()
        self.load_on_threads = load_on_threads_env in ("true", "1", "yes", "on")

        # Context files are stored in a dedicated folder
        # Use SLACK_CONTEXT_CONTEXTS_DIR env var if set, otherwise default
        contexts_dir_env = os.environ.get("SLACK_CONTEXT_CONTEXTS_DIR")
        if contexts_dir_env:
            self.contexts_dir = Path(contexts_dir_env).expanduser()
        else:
            self.contexts_dir = self.workspace / "slack-channel-contexts"

        # Cache duration in seconds (default: 3600 = 1 hour)
        cache_ttl_env = os.environ.get("SLACK_CONTEXT_CACHE_TTL", "3600")
        try:
            self.cache_ttl = int(cache_ttl_env)
        except ValueError:
            self.cache_ttl = 3600  # Default to 1 hour if invalid

        # Whether to load context on thread/session start (default: true)
        load_on_thread_start_env = os.environ.get(
            "SLACK_CONTEXT_LOAD_ON_THREAD_START", "true"
        ).lower()
        self.load_on_thread_start = load_on_thread_start_env in (
            "true",
            "1",
            "yes",
            "on",
        )

        self.cache = {}
        self.cache_times = {}

        # Path to README template (relative to this script)
        skill_dir = Path(__file__).parent.parent
        self.readme_template_path = skill_dir / "README.template.md"

    def load_context(
        self, channel_id=None, channel_name=None, force_reload=False, is_thread=False
    ):
        """
        Load the context file for the given channel.

        Priority order:
        1. <CHANNEL_ID>.md (e.g., C0AK8SDFS4W.md)
        2. <CHANNEL_NAME>.md (e.g., bebops.md)
        3. No default fallback - returns None if no file exists

        Args:
            channel_id: Slack channel ID
            channel_name: Slack channel name
            force_reload: If True, bypass cache and read file fresh
            is_thread: If True, check SLACK_CONTEXT_LOAD_ON_THREADS setting

        Returns:
            Context content if found and skill enabled, None otherwise
        """
        # If skill is disabled, don't load context
        if not self.enabled:
            return None

        # If in a thread and thread loading is disabled, don't load context
        if is_thread and not self.load_on_threads:
            return None

        # Check cache first (unless force_reload)
        cache_key = f"{channel_id}:{channel_name}"
        if not force_reload and cache_key in self.cache_times:
            if (
                datetime.now() - self.cache_times[cache_key]
                < timedelta(seconds=self.cache_ttl)
            ):
                return self.cache[cache_key]

        # Try channel ID first (in contexts folder)
        if channel_id:
            context_file = self.contexts_dir / f"{channel_id}.md"
            if context_file.exists():
                content = self._read_file(context_file)
                self._cache(cache_key, content)
                return content

        # Try channel name (in contexts folder)
        if channel_name:
            # Normalize channel name (remove #, lowercase)
            normalized_name = channel_name.lstrip("#").lower()
            context_file = self.contexts_dir / f"{normalized_name}.md"
            if context_file.exists():
                content = self._read_file(context_file)
                self._cache(cache_key, content)
                return content

        # No default fallback - return None if no file exists
        return None

    def _read_file(self, filepath):
        """Read and return file contents."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return None

    def _cache(self, key, content):
        """Cache context content."""
        if content:
            self.cache[key] = content
            self.cache_times[key] = datetime.now()

    def initialize_readme(self):
        """
        Initialize README.md in contexts directory if it doesn't exist.
        Copies from README.template.md in the skill directory.
        """
        readme_path = self.contexts_dir / "README.md"

        # Only initialize if README doesn't exist
        if readme_path.exists():
            return {"success": True, "message": "README.md already exists"}

        # Create contexts directory if it doesn't exist
        self.contexts_dir.mkdir(parents=True, exist_ok=True)

        # Check if template exists
        if not self.readme_template_path.exists():
            return {
                "success": False,
                "message": f"README template not found at {self.readme_template_path}",
            }

        # Copy template to contexts directory
        try:
            with open(self.readme_template_path, "r", encoding="utf-8") as src:
                template_content = src.read()

            with open(readme_path, "w", encoding="utf-8") as dst:
                dst.write(template_content)

            return {
                "success": True,
                "message": f"Created README.md in {self.contexts_dir}",
            }
        except Exception as e:
            return {"success": False, "message": f"Failed to create README.md: {e}"}

    def get_context_for_slack_message(self, message_metadata):
        """
        Extract channel info from Slack message metadata and load context.

        Expected metadata format:
        {
            "channel_id": "C0AK8SDFS4W",
            "channel": "bebops",
            "thread_id": "12345",  # Optional - if present, this is a thread message
            ...
        }
        """
        # Auto-initialize README on first context load
        self.initialize_readme()

        channel_id = message_metadata.get("channel_id") or message_metadata.get(
            "chat_id"
        )
        channel_name = message_metadata.get("channel") or message_metadata.get(
            "group_subject"
        )

        # Check if this is a thread message (has thread_id)
        is_thread = (
            "thread_id" in message_metadata or "thread_ts" in message_metadata
        )

        return self.load_context(
            channel_id=channel_id,
            channel_name=channel_name,
            is_thread=is_thread,
        )


def load_channel_context(
    channel_id=None,
    channel_name=None,
    workspace_dir=None,
    force_reload=False,
    is_thread=False,
):
    """
    Load Slack channel context for the current session.

    This is the tool function that OpenClaw agents call to load channel context.

    Args:
        channel_id: Slack channel ID (e.g., "C0AK8SDFS4W")
        channel_name: Slack channel name (e.g., "bebops")
        workspace_dir: Optional custom workspace directory
        force_reload: If True, bypass cache and read file fresh (use after editing context files)
        is_thread: If True, check SLACK_CONTEXT_LOAD_ON_THREADS setting

    Returns:
        dict with keys:
            - success: bool
            - context: str (the loaded context content, empty if disabled or not found)
            - channel_id: str
            - channel_name: str
            - message: str (description of what was loaded)
    """
    loader = SlackContextLoader(workspace_dir)

    # If skill is disabled, return success=False
    if not loader.enabled:
        return {
            "success": False,
            "context": "",
            "channel_id": channel_id or "unknown",
            "channel_name": channel_name or "unknown",
            "message": "Slack channel context skill is disabled (SLACK_CONTEXT_ENABLED=false)",
        }

    # Get context using the existing method
    context = loader.get_context_for_slack_message(
        {
            "channel_id": channel_id,
            "channel": channel_name,
            "thread_id": "1" if is_thread else None,  # Mark as thread if needed
        }
    )

    # If force_reload is True, bypass cache by reading file directly
    if force_reload and context is None:
        # Try to reload from file
        if channel_id:
            context_file = loader.contexts_dir / f"{channel_id}.md"
            if context_file.exists():
                context = loader._read_file(context_file)
        if not context and channel_name:
            normalized_name = channel_name.lstrip("#").lower()
            context_file = loader.contexts_dir / f"{normalized_name}.md"
            if context_file.exists():
                context = loader._read_file(context_file)
        # No default fallback

    if context:
        return {
            "success": True,
            "context": context,
            "channel_id": channel_id or "unknown",
            "channel_name": channel_name or "unknown",
            "message": f"Loaded channel context for {channel_name or 'default'} channel",
        }
    else:
        return {
            "success": False,
            "context": "",
            "channel_id": channel_id or "unknown",
            "channel_name": channel_name or "unknown",
            "message": "No context file found for this channel. Context files must be created in slack-channel-contexts/ directory.",
        }


def main():
    """Test the context loader or load context from command line."""
    import sys

    # Check if called from command line with arguments
    if len(sys.argv) > 1:
        # Parse command line arguments
        channel_id = None
        channel_name = None
        workspace_dir = None
        is_thread = False

        i = 1
        while i < len(sys.argv):
            if (
                sys.argv[i] == "--channel_id"
                and i + 1 < len(sys.argv)
            ):
                channel_id = sys.argv[i + 1]
                i += 2
            elif (
                sys.argv[i] == "--channel_name"
                and i + 1 < len(sys.argv)
            ):
                channel_name = sys.argv[i + 1]
                i += 2
            elif (
                sys.argv[i] == "--workspace_dir"
                and i + 1 < len(sys.argv)
            ):
                workspace_dir = sys.argv[i + 1]
                i += 2
            elif (
                sys.argv[i] == "--is_thread"
                and i + 1 < len(sys.argv)
            ):
                is_thread = sys.argv[i + 1].lower() in (
                    "true",
                    "1",
                    "yes",
                    "on",
                )
                i += 2
            else:
                i += 1

        # Load context with provided parameters
        result = load_channel_context(
            channel_id=channel_id,
            channel_name=channel_name,
            workspace_dir=workspace_dir,
            is_thread=is_thread,
        )

        # Output as JSON for Node.js to parse
        import json

        print(json.dumps(result))
        return

    # Test mode (no arguments)
    loader = SlackContextLoader()

    # Test with sample metadata
    test_metadata = {
        "channel_id": "C0AK8SDFS4W",
        "channel": "bebops",
    }

    context = loader.get_context_for_slack_message(test_metadata)

    if context:
        print("Context loaded successfully!")
        print(f"\n--- Context Content ({len(context)} chars) ---\n")
        print(context[:500] + "..." if len(context) > 500 else context)
    else:
        print("No context file found")
        print(f"Workspace: {loader.workspace}")
        print(f"Contexts directory: {loader.contexts_dir}")
        print("\nLooking for:")
        if channel_id:
            print(f"  - {channel_id}.md")
        if channel_name:
            print(f"  - {channel_name.lstrip('#').lower()}.md")
        print(f"\nIn: {loader.contexts_dir}")
        print(
            "\nNote: Context files are named simply as <CHANNEL_ID>.md or <CHANNEL_NAME>.md"
        )


if __name__ == "__main__":
    main()
