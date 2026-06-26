#!/usr/bin/env python3
"""
Test script for skill-rank functionality.
"""

import subprocess
import sys

def run_command(cmd):
    """Run a command and return output."""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def test_help():
    """Test --help command."""
    print("Testing --help...")
    code, out, err = run_command("python3 scripts/skill-rank.py --help")
    assert code == 0, f"Help failed with code {code}"
    assert "Skill Rank" in out, "Help output missing expected text"
    print("  ✓ Help command works")

def test_list():
    """Test --list command."""
    print("Testing --list...")
    code, out, err = run_command("python3 scripts/skill-rank.py --list --top 5")
    assert code == 0, f"List failed with code {code}"
    assert "Top 5 Skills" in out, "List output missing expected text"
    print("  ✓ List command works")

def test_search():
    """Test --search command."""
    print("Testing --search...")
    code, out, err = run_command("python3 scripts/skill-rank.py --search tts")
    assert code == 0, f"Search failed with code {code}"
    assert "xfyun-tts" in out, "Search didn't find expected skill"
    print("  ✓ Search command works")

def test_info():
    """Test --info command."""
    print("Testing --info...")
    code, out, err = run_command("python3 scripts/skill-rank.py --info skill-rank")
    assert code == 0, f"Info failed with code {code}"
    assert "Skill: skill-rank" in out, "Info output missing expected text"
    assert "Quality Dimensions:" in out, "Info missing quality dimensions"
    print("  ✓ Info command works")

def test_config():
    """Test --config command."""
    print("Testing --config...")
    code, out, err = run_command("python3 scripts/skill-rank.py --config")
    assert code == 0, f"Config failed with code {code}"
    assert "ranking weights" in out.lower(), "Config missing weights info"
    print("  ✓ Config command works")

def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("Skill Rank Test Suite")
    print("="*50 + "\n")
    
    tests = [
        test_help,
        test_list,
        test_search,
        test_info,
        test_config
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__}: Unexpected error: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*50 + "\n")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
