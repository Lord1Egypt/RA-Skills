"""
Regex Master 单元测试
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.regex_engine import RegexMaster


def test_test_method():
    rm = RegexMaster()
    assert rm.test(r"^\d{11}$", "13800138000")["match"] is True
    assert rm.test(r"^\d{11}$", "1380013800")["match"] is False
    assert rm.test(r"^(\d{3})-(\d{4})-(\d{4})$", "138-1234-5678")["groups"] == ["138", "1234", "5678"]
    print("✓ test_test_method passed")


def test_explain_method():
    rm = RegexMaster()
    exp = rm.explain(r"^(?=.*[A-Z])(?=.*\d).{8,}$")
    assert "大写字母" in exp or "数字" in exp or "至少8" in exp or "匹配模式" in exp
    print("✓ test_explain_method passed")


def test_generate_method():
    rm = RegexMaster()
    assert rm.generate("提取中国大陆手机号") == r"1[3-9]\d{9}"
    assert rm.generate("匹配邮箱地址") == r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    assert "1[3-9]" in rm.generate("手机号")
    print("✓ test_generate_method passed")


def test_extract_all_method():
    rm = RegexMaster()
    text = "Contact: alice@test.com, bob@demo.io, charlie@site.org"
    matches = rm.extract_all(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    assert len(matches) == 3
    assert "alice@test.com" in matches
    print("✓ test_extract_all_method passed")


def test_templates():
    rm = RegexMaster()
    assert rm.get_template("email") is not None
    assert rm.get_template("phone_cn") is not None
    assert rm.get_template("nonexistent") is None
    assert "email" in rm.list_templates()
    print("✓ test_templates passed")


def test_validate_pattern():
    rm = RegexMaster()
    assert rm.validate_pattern(r"^[a-z]+$")["valid"] is True
    assert rm.validate_pattern(r"[a-z")["valid"] is False
    print("✓ test_validate_pattern passed")


def test_replace_method():
    rm = RegexMaster()
    text = "hello 123 world 456"
    result = rm.replace(r"\d+", text, "NUM")
    assert result == "hello NUM world NUM"
    print("✓ test_replace_method passed")


if __name__ == "__main__":
    test_test_method()
    test_explain_method()
    test_generate_method()
    test_extract_all_method()
    test_templates()
    test_validate_pattern()
    test_replace_method()
    print("\n所有测试通过! ✅")
