"""
pytest-test-master 单元测试
TDD: 先写测试，再开发核心逻辑
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pytest_master import (
    ALL_TOPICS, FIXTURES_CONTENT, MOCK_CONTENT,
    PARAMETRIZE_CONTENT, COVERAGE_CONTENT, DATA_CONTENT,
    get_topic_keys, output_content, list_all_topics
)


class TestAllTopics:
    """验证所有主题库非空"""

    def test_all_topics_keys(self):
        assert "fixtures" in ALL_TOPICS
        assert "mock" in ALL_TOPICS
        assert "parametrize" in ALL_TOPICS
        assert "coverage" in ALL_TOPICS
        assert "data" in ALL_TOPICS

    def test_fixtures_has_8_topics(self):
        assert len(FIXTURES_CONTENT) == 8
        assert "scope" in FIXTURES_CONTENT
        assert "yield" in FIXTURES_CONTENT
        assert "params" in FIXTURES_CONTENT
        assert "autouse" in FIXTURES_CONTENT
        assert "request" in FIXTURES_CONTENT
        assert "teardown" in FIXTURES_CONTENT
        assert "session" in FIXTURES_CONTENT
        assert "inject" in FIXTURES_CONTENT

    def test_mock_has_7_topics(self):
        assert len(MOCK_CONTENT) == 7
        assert "patch" in MOCK_CONTENT
        assert "mock_obj" in MOCK_CONTENT
        assert "assert_calls" in MOCK_CONTENT
        assert "freeze" in MOCK_CONTENT
        assert "spy" in MOCK_CONTENT
        assert "scope_mock" in MOCK_CONTENT
        assert "common" in MOCK_CONTENT

    def test_parametrize_has_6_topics(self):
        assert len(PARAMETRIZE_CONTENT) == 6
        assert "basic" in PARAMETRIZE_CONTENT
        assert "ids" in PARAMETRIZE_CONTENT
        assert "indirect" in PARAMETRIZE_CONTENT
        assert "combine" in PARAMETRIZE_CONTENT
        assert "generate" in PARAMETRIZE_CONTENT
        assert "product" in PARAMETRIZE_CONTENT

    def test_coverage_has_6_topics(self):
        assert len(COVERAGE_CONTENT) == 6
        assert "report" in COVERAGE_CONTENT
        assert "html" in COVERAGE_CONTENT
        assert "xml" in COVERAGE_CONTENT
        assert "threshold" in COVERAGE_CONTENT
        assert "exclude" in COVERAGE_CONTENT
        assert "debug" in COVERAGE_CONTENT

    def test_data_has_5_topics(self):
        assert len(DATA_CONTENT) == 5
        assert "faker" in DATA_CONTENT
        assert "factory" in DATA_CONTENT
        assert "fixture_data" in DATA_CONTENT
        assert "seed" in DATA_CONTENT
        assert "strategy" in DATA_CONTENT


class TestTopicStructure:
    """验证每个主题都有必需字段"""

    REQUIRED_FIELDS = ["title", "概念", "何时用", "示例", "避坑"]

    def test_fixtures_topic_structure(self):
        for key, info in FIXTURES_CONTENT.items():
            for field in self.REQUIRED_FIELDS:
                assert field in info, f"{key} missing {field}"
            assert len(info["示例"]) > 50, f"{key} 示例太短"

    def test_mock_topic_structure(self):
        for key, info in MOCK_CONTENT.items():
            for field in self.REQUIRED_FIELDS:
                assert field in info, f"{key} missing {field}"
            assert len(info["示例"]) > 50, f"{key} 示例太短"

    def test_parametrize_topic_structure(self):
        for key, info in PARAMETRIZE_CONTENT.items():
            for field in self.REQUIRED_FIELDS:
                assert field in info, f"{key} missing {field}"
            assert len(info["示例"]) > 50, f"{key} 示例太短"

    def test_coverage_topic_structure(self):
        for key, info in COVERAGE_CONTENT.items():
            for field in self.REQUIRED_FIELDS:
                assert field in info, f"{key} missing {field}"
            assert len(info["示例"]) > 50, f"{key} 示例太短"

    def test_data_topic_structure(self):
        for key, info in DATA_CONTENT.items():
            for field in self.REQUIRED_FIELDS:
                assert field in info, f"{key} missing {field}"
            assert len(info["示例"]) > 50, f"{key} 示例太短"


class TestGetTopicKeys:
    """测试 get_topic_keys 函数"""

    def test_fixtures_keys(self):
        keys = get_topic_keys("fixtures")
        assert "scope" in keys
        assert "yield" in keys
        assert len(keys) == 8

    def test_mock_keys(self):
        keys = get_topic_keys("mock")
        assert "patch" in keys
        assert len(keys) == 7

    def test_parametrize_keys(self):
        keys = get_topic_keys("parametrize")
        assert "basic" in keys
        assert len(keys) == 6

    def test_coverage_keys(self):
        keys = get_topic_keys("coverage")
        assert "report" in keys
        assert len(keys) == 6

    def test_data_keys(self):
        keys = get_topic_keys("data")
        assert "faker" in keys
        assert len(keys) == 5

    def test_unknown_subcommand(self):
        keys = get_topic_keys("unknown")
        assert keys == []


class TestOutputContent:
    """测试 output_content 函数"""

    def test_list_fixtures_topics(self):
        result = output_content("fixtures", None)
        assert "fixtures" in result.lower()
        assert "scope" in result
        assert "yield" in result
        assert "可用主题" in result

    def test_output_specific_topic(self):
        result = output_content("fixtures", "scope")
        assert "scope" in result
        assert "fixture" in result.lower()
        assert "概念" in result
        assert "示例" in result

    def test_output_mock_topic(self):
        result = output_content("mock", "patch")
        assert "patch" in result
        assert "unittest.mock" in result or "@patch" in result
        assert "示例" in result

    def test_output_parametrize_topic(self):
        result = output_content("parametrize", "basic")
        # Title for 'basic' is "@pytest.mark.parametrize 基础用法"
        assert "parametrize" in result or "@pytest.mark.parametrize" in result
        assert "示例" in result

    def test_output_coverage_topic(self):
        result = output_content("coverage", "report")
        assert "report" in result
        assert "示例" in result

    def test_output_data_topic(self):
        result = output_content("data", "faker")
        assert "faker" in result
        assert "示例" in result

    def test_unknown_subcommand_output(self):
        result = output_content("unknown", "topic")
        assert "未知子命令" in result

    def test_unknown_topic_output(self):
        result = output_content("fixtures", "nonexistent")
        assert "未知主题" in result
        assert "scope" in result  # 应列出可用主题


class TestListAllTopics:
    """测试 list_all_topics 函数"""

    def test_lists_all_5_subcommands(self):
        result = list_all_topics()
        assert "FIXTURES" in result
        assert "MOCK" in result
        assert "PARAMETRIZE" in result
        assert "COVERAGE" in result
        assert "DATA" in result

    def test_includes_topic_titles(self):
        result = list_all_topics()
        assert "scope" in result
        assert "patch" in result
        assert "basic" in result
        assert "report" in result
        assert "faker" in result


class TestContentQuality:
    """测试内容质量"""

    def test_code_examples_contain_pytest(self):
        """验证代码示例包含 pytest 相关内容"""
        for key, info in FIXTURES_CONTENT.items():
            assert "@pytest.fixture" in info["示例"], f"{key} missing @pytest.fixture"

    def test_mock_examples_contain_mock(self):
        """验证 mock 示例包含 mock 相关代码"""
        for key, info in MOCK_CONTENT.items():
            has_mock = "Mock" in info["示例"] or "mock" in info["示例"]
            has_freeze = "freeze" in info["示例"]
            has_patch = "patch" in info["示例"]
            assert has_mock or has_freeze or has_patch, f"{key} missing mock/patch/freeze code"

    def test_parametrize_examples_contain_parametrize(self):
        for key, info in PARAMETRIZE_CONTENT.items():
            assert "parametrize" in info["示例"] or "parametrize" in info["概念"], f"{key} missing parametrize"

    def test_coverage_examples_contain_coverage(self):
        for key, info in COVERAGE_CONTENT.items():
            assert "cov" in info["示例"].lower() or "coverage" in info["概念"].lower(), f"{key} missing coverage"

    def test_data_examples_contain_faker_or_factory(self):
        for key, info in DATA_CONTENT.items():
            example = info["示例"].lower()
            assert "faker" in example or "factory" in example or "fixture" in example, f"{key} missing data gen pattern"


class TestEdgeCases:
    """边界情况测试"""

    def test_empty_topic_key(self):
        result = output_content("fixtures", "")
        assert "可用主题" in result

    def test_none_topic(self):
        result = output_content("mock", None)
        assert "可用主题" in result


class TestCLIParsing:
    """CLI 参数解析测试"""

    def test_cli_import(self):
        """验证 CLI 可以被 import"""
        import cli
        assert hasattr(cli, "main")

    def test_cli_main_runs(self):
        """验证 CLI main 函数可以运行（不报错）"""
        import cli
        import io
        import contextlib
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            try:
                cli.main()
            except SystemExit:
                pass

    def test_cli_list_flag(self):
        """验证 --list 参数"""
        import cli
        import io
        import contextlib
        old_argv = sys.argv
        sys.argv = ["cli", "--list"]
        try:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    cli.main()
                except SystemExit:
                    pass
            output = f.getvalue()
            assert "FIXTURES" in output
            assert "MOCK" in output
        finally:
            sys.argv = old_argv

    def test_cli_subcommand_topic(self):
        """验证 subcommand + topic 参数"""
        import cli
        import io
        import contextlib
        old_argv = sys.argv
        sys.argv = ["cli", "fixtures", "scope"]
        try:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                try:
                    cli.main()
                except SystemExit:
                    pass
            output = f.getvalue()
            assert "scope" in output
            assert "示例" in output
        finally:
            sys.argv = old_argv


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
