"""
Fuzzing 测试 — ACL 防护层
──────────────────────────
随机注入脏数据，验证 ACL 能否正确拦截。

ACL 必须能够：
1. 拦截 None 值
2. 拦截空列表
3. 拦截非预期类型
4. 拦截缺失字段
"""
import pytest
import random
import string
from layers.acl import (
    validate_not_none,
    validate_list_nonempty,
    validate_dict_has_keys,
    validate_urls,
    validate_string_nonempty,
    StageValidator,
    ACLViolationError,
    search_to_crawl_validator,
)


class TestValidateNotNone:
    def test_none_rejected(self):
        result = validate_not_none(None, "test_field")
        assert not result.passed
        assert "None" in result.errors[0]

    def test_value_accepted(self):
        result = validate_not_none({"key": "value"}, "test_field")
        assert result.passed
        assert result.transformed_data == {"key": "value"}

    def test_empty_string_accepted(self):
        """空字符串不是 None，应通过"""
        result = validate_not_none("", "test_field")
        assert result.passed

    def test_zero_accepted(self):
        """0 不是 None，应通过"""
        result = validate_not_none(0, "test_field")
        assert result.passed

    def test_false_accepted(self):
        """False 不是 None，应通过"""
        result = validate_not_none(False, "test_field")
        assert result.passed


class TestValidateListNonempty:
    def test_empty_list_rejected(self):
        result = validate_list_nonempty([], "results")
        assert not result.passed
        assert "empty" in result.errors[0]

    def test_non_list_rejected(self):
        result = validate_list_nonempty("not_a_list", "results")
        assert not result.passed
        assert "not a list" in result.errors[0]

    def test_none_rejected(self):
        result = validate_list_nonempty(None, "results")
        assert not result.passed

    def test_valid_list_accepted(self):
        result = validate_list_nonempty([1, 2, 3], "results")
        assert result.passed


class TestValidateDictHasKeys:
    def test_missing_keys_rejected(self):
        result = validate_dict_has_keys(
            {"a": 1}, ["a", "b", "c"], "test_dict"
        )
        assert not result.passed
        assert "missing" in result.errors[0]

    def test_all_keys_present_accepted(self):
        result = validate_dict_has_keys(
            {"a": 1, "b": 2}, ["a", "b"], "test_dict"
        )
        assert result.passed

    def test_non_dict_rejected(self):
        result = validate_dict_has_keys("not_a_dict", ["key"], "test_dict")
        assert not result.passed


class TestValidateUrls:
    def test_invalid_url_rejected(self):
        result = validate_urls(["not_a_url"], "urls")
        assert not result.passed

    def test_none_in_list_rejected(self):
        result = validate_urls(["https://example.com", None], "urls")
        assert not result.passed

    def test_valid_urls_accepted(self):
        result = validate_urls(
            ["https://example.com", "http://test.org/path"], "urls"
        )
        assert result.passed

    def test_empty_list_accepted_with_warning(self):
        result = validate_urls([], "urls")
        assert result.passed
        assert result.has_warnings


class TestStageValidator:
    def test_all_checks_pass(self):
        validator = StageValidator([
            lambda d: validate_not_none(d, "data"),
            lambda d: validate_list_nonempty(d, "data"),
        ])
        result = validator.validate([1, 2, 3])
        assert result == [1, 2, 3]

    def test_first_check_fails(self):
        validator = StageValidator([
            lambda d: validate_not_none(d, "data"),
            lambda d: validate_list_nonempty(d, "data"),
        ])
        with pytest.raises(ACLViolationError):
            validator.validate(None)

    def test_second_check_fails(self):
        validator = StageValidator([
            lambda d: validate_not_none(d, "data"),
            lambda d: validate_list_nonempty(d, "data"),
        ])
        with pytest.raises(ACLViolationError):
            validator.validate([])


class TestSearchToCrawlValidator:
    """搜索→爬取 ACL 校验"""

    def test_valid_data_passes(self):
        data = {
            "deduplicated_results": [
                {"url": "https://example.com", "title": "Test", "rank": 1}
            ],
            "total_deduped": 1,
            "status": "complete",
        }
        result = search_to_crawl_validator.validate(data)
        assert result["total_deduped"] == 1

    def test_missing_deduplicated_results(self):
        data = {"total_deduped": 0, "status": "failed"}
        with pytest.raises(ACLViolationError):
            search_to_crawl_validator.validate(data)

    def test_empty_deduplicated_results(self):
        data = {
            "deduplicated_results": [],
            "total_deduped": 0,
            "status": "failed",
        }
        with pytest.raises(ACLViolationError):
            search_to_crawl_validator.validate(data)

    def test_none_data(self):
        with pytest.raises(ACLViolationError):
            search_to_crawl_validator.validate(None)


class TestFuzzACL:
    """Fuzzing: 随机脏数据注入"""

    def _generate_random_string(self, length: int = 50) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation + "中文测试"
        return "".join(random.choice(chars) for _ in range(length))

    def _generate_random_value(self) -> any:
        """生成随机脏数据"""
        generators = [
            lambda: None,
            lambda: "",
            lambda: [],
            lambda: {},
            lambda: 0,
            lambda: -1,
            lambda: 999999999999,
            lambda: self._generate_random_string(),
            lambda: [None, None, None],
            lambda: {"": ""},
            lambda: True,
            lambda: False,
            lambda: 3.14159,
        ]
        return random.choice(generators)()

    def test_fuzz_validate_not_none(self, num_iterations: int = 100):
        """Fuzzing validate_not_none"""
        for _ in range(num_iterations):
            value = self._generate_random_value()
            result = validate_not_none(value, "fuzz_field")
            # 唯一硬性要求：None 必须被拒绝
            if value is None:
                assert not result.passed, f"None should be rejected, got passed"
            else:
                assert result.passed, f"Non-None should be accepted, got: {result.errors}"

    def test_fuzz_validate_list_nonempty(self, num_iterations: int = 100):
        """Fuzzing validate_list_nonempty"""
        for _ in range(num_iterations):
            value = self._generate_random_value()
            result = validate_list_nonempty(value, "fuzz_list")
            # 非 list 或空 list 应被拒绝
            if not isinstance(value, list) or len(value) == 0:
                assert not result.passed
            else:
                assert result.passed

    def test_fuzz_stage_validator_no_crash(self, num_iterations: int = 100):
        """Fuzzing StageValidator — 不应崩溃"""
        validator = StageValidator([
            lambda d: validate_not_none(d, "data"),
        ])
        for _ in range(num_iterations):
            value = self._generate_random_value()
            try:
                validator.validate(value)
            except ACLViolationError:
                pass  # 预期行为
            except Exception as e:
                pytest.fail(f"StageValidator crashed on {type(value).__name__}: {e}")
