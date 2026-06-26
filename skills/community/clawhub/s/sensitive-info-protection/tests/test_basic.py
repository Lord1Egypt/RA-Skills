#!/usr/bin/env python3
"""Basic tests for sensitive-info-protection skill"""

import sys
import os
scripts_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
sys.path.insert(0, scripts_path)

from detector import SensitiveDetector


def test_api_key_detection():
    """Test API key detection"""
    detector = SensitiveDetector()
    text = "My OpenAI key is sk-1234567890abcdef1234567890abcdef1234567890abcdef"
    result = detector.scan(text)
    assert result.has_sensitive
    assert any(d.rule.name == "openai_key" for d in result.detections)
    print("✓ API key detection passed")


def test_github_token_detection():
    """Test GitHub token detection"""
    detector = SensitiveDetector()
    text = "github_token: ghp_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
    result = detector.scan(text)
    assert result.has_sensitive
    assert any(d.rule.name == "github_token" for d in result.detections)
    print("✓ GitHub token detection passed")


def test_phone_detection():
    """Test Chinese phone number detection"""
    detector = SensitiveDetector()
    text = "我的手机号是13800138000"
    result = detector.scan(text)
    assert result.has_sensitive
    assert any(d.rule.name == "phone" for d in result.detections)
    print("✓ Phone number detection passed")


def test_email_detection():
    """Test email detection"""
    detector = SensitiveDetector()
    text = "联系我 at test@example.com"
    result = detector.scan(text)
    assert result.has_sensitive
    assert any(d.rule.name == "email" for d in result.detections)
    print("✓ Email detection passed")


def test_desensitization():
    """Test desensitization works correctly"""
    detector = SensitiveDetector()
    text = "My key is sk-1234567890abcdef1234567890abcdef1234567890abcdef and phone is 13800138000"
    desensitized = detector.desensitize(text)
    assert "sk-" not in desensitized
    assert "13800138000" not in desensitized
    assert "***" in desensitized
    print("✓ Desensitization passed")


def test_disable_enable_rule():
    """Test disabling and enabling rules"""
    detector = SensitiveDetector()
    text = "test@example.com"

    # Original detection
    result = detector.scan(text)
    assert result.has_sensitive

    # Disable email detection
    success = detector.disable_rule("email")
    assert success
    result = detector.scan(text)
    assert not result.has_sensitive

    # Enable it back
    success = detector.enable_rule("email")
    assert success
    result = detector.scan(text)
    assert result.has_sensitive
    print("✓ Disable/enable rule passed")


def test_add_custom_rule():
    """Test adding a custom rule"""
    from models import DetectionRule
    detector = SensitiveDetector()

    # Add custom rule for secret pattern
    rule = DetectionRule(
        name="custom_secret",
        pattern="MY_SECRET=\\w+",
        sensitivity="high"
    )
    detector.add_rule(rule)

    text = "MY_SECRET=supersecret123"
    result = detector.scan(text)
    assert result.has_sensitive
    assert any(d.rule.name == "custom_secret" for d in result.detections)
    print("✓ Add custom rule passed")


def test_no_false_positive():
    """Test that normal text doesn't get false positives"""
    detector = SensitiveDetector()
    text = "Hello world! This is a normal message with no sensitive information."
    result = detector.scan(text)
    assert not result.has_sensitive
    print("✓ No false positive passed")


def main():
    """Run all tests"""
    print("Running sensitive-info-protection basic tests...\n")

    tests = [
        test_api_key_detection,
        test_github_token_detection,
        test_phone_detection,
        test_email_detection,
        test_desensitization,
        test_disable_enable_rule,
        test_add_custom_rule,
        test_no_false_positive
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Total: {passed + failed} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if failed > 0:
        sys.exit(1)
    else:
        print("\nAll tests passed! ✓")
        sys.exit(0)


if __name__ == "__main__":
    main()
