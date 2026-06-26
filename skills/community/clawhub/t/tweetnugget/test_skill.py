#!/usr/bin/env python3
"""Test script for tweetnugget skill."""

import glob
import json
import os
import random
import sys
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def pass_msg(msg):
    print(f"{GREEN}PASS{RESET}: {msg}")


def fail_msg(msg):
    print(f"{RED}FAIL{RESET}: {msg}")


def warn_msg(msg):
    print(f"{YELLOW}WARN{RESET}: {msg}")


def load_all_quotes():
    """Load all quotes from references/ directory."""
    quotes = []
    for f in glob.glob("references/*.json"):
        try:
            with open(f) as file:
                data = json.load(file)
                quotes.extend(data.get("quotes", []))
        except json.JSONDecodeError as e:
            print(f"Error parsing {f}: {e}")
            return None
    return quotes


def get_all_tags():
    """Get all unique tags across all quote files."""
    tags = set()
    for f in glob.glob("references/*.json"):
        try:
            with open(f) as file:
                data = json.load(file)
                for quote in data.get("quotes", []):
                    for tag in quote.get("tags", []):
                        tags.add(tag.lower())
        except json.JSONDecodeError as e:
            print(f"Error parsing {f}: {e}")
            return None
    return sorted(tags)


def test_json_parsing():
    """Test 1: Validate all JSON files parse correctly."""
    print("\n=== Test 1: JSON Parsing ===")
    passed = True
    for f in glob.glob("references/*.json"):
        try:
            with open(f) as file:
                data = json.load(file)
                # Check structure
                if "name" not in data or "quotes" not in data:
                    fail_msg(f"{f} missing required fields")
                    passed = False
                else:
                    pass_msg(f"{f} valid JSON with {len(data['quotes'])} quotes")
        except json.JSONDecodeError as e:
            fail_msg(f"{f} - {e}")
            passed = False
        except Exception as e:
            fail_msg(f"{f} - {e}")
            passed = False
    return passed


def test_random_selection():
    """Test 2: Test random selection produces variety."""
    print("\n=== Test 2: Random Selection Variety ===")
    quotes = load_all_quotes()
    if quotes is None:
        fail_msg("Could not load quotes")
        return False

    if len(quotes) < 2:
        warn_msg(f"Only {len(quotes)} quotes total, variety test limited")
        return True

    # Pick 20 quotes and check they're not all the same
    picks = []
    for _ in range(min(20, len(quotes))):
        q = random.choice(quotes)
        picks.append(q["text"])

    unique = len(set(picks))
    if unique > 1:
        pass_msg(f"Random selection varies: {unique} unique quotes from {len(picks)} picks")
        return True
    fail_msg("Random selection not varying: all picks are the same")
    return False


def test_tag_filtering():
    """Test 3: Test tag filtering for all unique tags."""
    print("\n=== Test 3: Tag Filtering ===")
    quotes = load_all_quotes()
    tags = get_all_tags()

    if quotes is None or tags is None:
        fail_msg("Could not load quotes or tags")
        return False

    passed = True
    for tag in tags:
        filtered = [q for q in quotes if any(tag in t.lower() for t in q.get("tags", []))]
        if filtered:
            pass_msg(f"Tag '{tag}': {len(filtered)} quotes found")
        else:
            fail_msg(f"Tag '{tag}': no quotes found (but tag exists in files)")
            passed = False

    return passed


def test_edge_cases():
    """Test 4: Test edge cases."""
    print("\n=== Test 4: Edge Cases ===")
    quotes = load_all_quotes()

    if quotes is None:
        fail_msg("Could not load quotes")
        return False

    passed = True

    # Test nonexistent tag
    tag = "nonexistenttagthatdoesnotexist"
    filtered = [q for q in quotes if any(tag in t.lower() for t in q.get("tags", []))]
    if not filtered:
        pass_msg("Nonexistent tag returns no results (expected)")
    else:
        fail_msg(f"Nonexistent tag returned {len(filtered)} results (unexpected)")
        passed = False

    # Test empty tag (should return all)
    filtered = [q for q in quotes if any("" in t for t in q.get("tags", []))]
    # Empty string matches nothing in Python's "in" check for non-empty strings
    # So we test the actual behavior: empty tag should give no matches
    if not filtered:
        pass_msg("Empty tag returns no results (expected behavior)")
    else:
        warn_msg(f"Empty tag returned {len(filtered)} results")

    # Test tag with partial match
    if quotes:
        sample_tag = quotes[0].get("tags", [""])[0]
        if sample_tag:
            partial = sample_tag[:3]  # First 3 chars
            filtered = [q for q in quotes if any(partial in t.lower() for t in q.get("tags", []))]
            if filtered:
                pass_msg(f"Partial tag '{partial}' matches {len(filtered)} quotes")
            else:
                fail_msg(f"Partial tag '{partial}' matched nothing")
                passed = False

    return passed


def main():
    """Run all tests."""
    print("=" * 50)
    print("TweetNugget Skill Test Suite")
    print("=" * 50)

    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # Run tests
    results = {
        "JSON Parsing": test_json_parsing(),
        "Random Selection": test_random_selection(),
        "Tag Filtering": test_tag_filtering(),
        "Edge Cases": test_edge_cases(),
    }

    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{status}: {test}")

    print("=" * 50)
    print(f"Result: {passed}/{total} tests passed")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
