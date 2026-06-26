#!/usr/bin/env python3
"""
Tavily Web Search - Test Suite
Tests for Search, Extract, and Usage APIs

Usage:
    python3 test_all.py [--quick]
"""
import subprocess
import sys
import json
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent

def run_script(script: str, args: list, expect_success: bool = True) -> bool:
    """Run a script and check result"""
    cmd = [sys.executable, str(SCRIPTS_DIR / script), *args]
    print(f"\n{'='*60}")
    print(f"Testing: {script} {' '.join(args)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print stderr (logs)
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
    
    # Print stdout
    if result.stdout:
        output = result.stdout[:500] + ("..." if len(result.stdout) > 500 else "")
        print(f"STDOUT:\n{output}")
    
    success = result.returncode == 0
    
    if success == expect_success:
        print(f"✅ PASS")
        return True
    else:
        print(f"❌ FAIL (expected {'success' if expect_success else 'failure'})")
        return False


def test_search():
    """Test Search API"""
    tests = [
        # Basic search
        ("search.py", ["--query", "Python tutorial", "--max-results", "2", "--format", "compact"], True),
        # News search
        ("search.py", ["--query", "AI news", "--topic", "news", "--time-range", "day", "--max-results", "2"], True),
        # Domain filter
        ("search.py", ["--query", "Python", "--include-domains", "python.org", "--max-results", "2"], True),
        # JSON output
        ("search.py", ["--query", "test", "--max-results", "1", "--format", "raw"], True),
    ]
    
    results = []
    for script, args, expect in tests:
        results.append(run_script(script, args, expect))
    
    return results


def test_extract():
    """Test Extract API"""
    tests = [
        # Single URL
        ("extract.py", ["--urls", "https://tavily.com", "--output", "compact"], True),
        # Multiple URLs
        ("extract.py", ["--urls", "https://tavily.com,https://example.com", "--output", "compact"], True),
        # With query
        ("extract.py", ["--urls", "https://tavily.com", "--query", "find features", "--output", "compact"], True),
        # JSON output
        ("extract.py", ["--urls", "https://tavily.com", "--output", "raw"], True),
    ]
    
    results = []
    for script, args, expect in tests:
        results.append(run_script(script, args, expect))
    
    return results


def test_usage():
    """Test Usage API"""
    tests = [
        # Compact output
        ("usage.py", [], True),
        # Markdown output
        ("usage.py", ["--md"], True),
        # JSON output
        ("usage.py", ["--json"], True),
    ]
    
    results = []
    for script, args, expect in tests:
        results.append(run_script(script, args, expect))
    
    return results


def test_disabled_apis():
    """Test that expensive APIs are disabled by default"""
    tests = [
        # Crawl without --enable should fail
        ("crawl.py", ["--url", "https://example.com"], False),
        # Map without --enable should fail
        ("map.py", ["--url", "https://example.com"], False),
        # Research without --enable --confirm should fail
        ("research.py", ["--query", "test"], False),
        # Research with only --enable should fail
        ("research.py", ["--query", "test", "--enable"], False),
    ]
    
    results = []
    for script, args, expect in tests:
        results.append(run_script(script, args, expect))
    
    return results


def main():
    import argparse
    
    ap = argparse.ArgumentParser(description="Tavily Test Suite")
    ap.add_argument("--quick", action="store_true", help="Quick test (search only)")
    args = ap.parse_args()
    
    print("\n" + "="*60)
    print("🧪 TAVILY WEB SEARCH - TEST SUITE")
    print("="*60)
    
    all_results = []
    
    # Test Search
    print("\n📍 Testing Search API...")
    all_results.extend(test_search())
    
    if not args.quick:
        # Test Extract
        print("\n📄 Testing Extract API...")
        all_results.extend(test_extract())
        
        # Test Usage
        print("\n📊 Testing Usage API...")
        all_results.extend(test_usage())
        
        # Test disabled APIs (should fail without --enable)
        print("\n🔒 Testing safety controls (should fail without --enable)...")
        all_results.extend(test_disabled_apis())
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    passed = sum(all_results)
    total = len(all_results)
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
