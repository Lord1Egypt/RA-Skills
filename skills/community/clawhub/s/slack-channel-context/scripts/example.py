#!/usr/bin/env python3
"""
Example helper script for slack-channel-context.

This script demonstrates how to use the SlackContextLoader directly.
"""

import sys
from pathlib import Path

# Add the skill scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from load_context import load_channel_context


def main():
    """Test the context loader with different channels."""
    print("=== Slack Channel Context Loader Demo ===\n")

    # Test with sample channels
    test_cases = [
        {
            "channel_id": "C0AML4J8FK2",
            "channel_name": "slack-channel-context",
            "description": "This channel (slack-channel-context)",
        },
        {
            "channel_id": "C0AK8SDFS4W",
            "channel_name": "bebops",
            "description": "Bebops channel (example)",
        },
        {
            "channel_id": "C0UNKNOWN123",
            "channel_name": "unknown-channel",
            "description": "Channel without context file (example)",
        },
    ]

    for test in test_cases:
        print(f"Testing: {test['description']}")
        print(f"  Channel ID: {test['channel_id']}")
        print(f"  Channel Name: {test['channel_name']}")

        result = load_channel_context(
            channel_id=test["channel_id"],
            channel_name=test["channel_name"],
        )

        if result["success"]:
            print(f"  Context loaded ({len(result['context'])} chars)")
            print(f"  Message: {result['message']}")
        else:
            print("  No context found")
            print(f"  Message: {result['message']}")

        print()

    # Test force_reload
    print("Testing force_reload parameter:")
    result1 = load_channel_context(
        channel_id="C0AML4J8FK2",
        channel_name="slack-channel-context",
        force_reload=False,
    )
    result2 = load_channel_context(
        channel_id="C0AML4J8FK2",
        channel_name="slack-channel-context",
        force_reload=True,
    )
    print(f"  First load (no reload): {result1['success']}")
    print(f"  Second load (force_reload=True): {result2['success']}")

    # Test thread control
    print("\nTesting thread control parameter:")
    result_normal = load_channel_context(
        channel_id="C0AML4J8FK2",
        channel_name="slack-channel-context",
        is_thread=False,
    )
    result_thread = load_channel_context(
        channel_id="C0AML4J8FK2",
        channel_name="slack-channel-context",
        is_thread=True,
    )
    print(f"  Normal message: {result_normal['success']}")
    print(f"  Thread message: {result_thread['success']}")
    print(
        "  (Thread behavior controlled by SLACK_CONTEXT_LOAD_ON_THREADS env var)"
    )

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
