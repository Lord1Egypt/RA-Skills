#!/usr/bin/env python3
"""
API Configuration Checker for Skills-Coach
Validates API availability and prompts user for configuration if needed
"""

import os
import sys
from pathlib import Path


def check_anthropic_api() -> tuple[bool, str]:
    """
    Check if Anthropic API is available and configured.

    Returns:
        (is_available, message) tuple
    """
    try:
        import anthropic
    except ImportError:
        return False, "Anthropic SDK not installed. Install with: pip install anthropic"

    # Check for API key or auth token
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    auth_token = os.environ.get("ANTHROPIC_AUTH_TOKEN")
    base_url = os.environ.get("ANTHROPIC_BASE_URL")

    if not api_key and not auth_token:
        return False, "ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN environment variable not set"

    # Try to create client
    try:
        if auth_token:
            # Use auth token with custom base URL
            client = anthropic.Anthropic(
                api_key=auth_token,
                base_url=base_url if base_url else None
            )
            return True, f"Anthropic API configured successfully (using AUTH_TOKEN{' with custom base URL' if base_url else ''})"
        else:
            # Use standard API key
            client = anthropic.Anthropic(api_key=api_key)
            return True, "Anthropic API configured successfully"
    except Exception as e:
        return False, f"Failed to initialize Anthropic client: {e}"


def prompt_user_for_api_key() -> str:
    """
    Prompt user to provide API key.

    Returns:
        API key string or empty string if user cancels
    """
    print("\n" + "="*60)
    print("API Configuration Required")
    print("="*60)
    print("\nSkills-Coach requires access to Claude API for optimization.")
    print("\nOptions:")
    print("1. Provide your Anthropic API key")
    print("2. Skip optimization (will fail)")
    print("\nTo get an API key, visit: https://console.anthropic.com/")

    choice = input("\nEnter choice (1 or 2): ").strip()

    if choice == "1":
        api_key = input("\nEnter your Anthropic API key: ").strip()
        if api_key:
            # Validate the key format (should start with sk-)
            if api_key.startswith("sk-"):
                return api_key
            else:
                print("⚠️  Warning: API key should start with 'sk-'")
                confirm = input("Use this key anyway? (y/n): ").strip().lower()
                if confirm == 'y':
                    return api_key

    return ""


def ensure_api_available() -> bool:
    """
    Ensure API is available, prompting user if needed.

    Returns:
        True if API is available, False otherwise
    """
    is_available, message = check_anthropic_api()

    if is_available:
        print(f"✓ {message}")
        return True

    print(f"⚠️  {message}")

    # Prompt user for API key
    api_key = prompt_user_for_api_key()

    if not api_key:
        print("\n✗ API configuration skipped. Optimization will fail.")
        return False

    # Set the API key in environment
    os.environ["ANTHROPIC_API_KEY"] = api_key

    # Verify it works
    is_available, message = check_anthropic_api()

    if is_available:
        print(f"\n✓ {message}")
        print("\nNote: To avoid this prompt in the future, set ANTHROPIC_API_KEY in your environment:")
        print(f"  export ANTHROPIC_API_KEY='{api_key}'")
        return True
    else:
        print(f"\n✗ {message}")
        return False


if __name__ == "__main__":
    success = ensure_api_available()
    sys.exit(0 if success else 1)
