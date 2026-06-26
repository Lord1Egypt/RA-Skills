"""章节标题质量检查测试 v2.2.1"""

import os
import sys
import json
import tempfile
import pytest

# 添加父目录到 path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chapter_title_check import (
    extract_title, title_char_count, list_chapter_files,
    check_title_length, check_title_attractiveness,
    check_format_consistency, check_hooks,
    run_check, VERSION,
)


# ============================================================
# 辅助函数
# ============================================================

def create_chapter_dir(tmpdir, filenames):
    """在临时目录创建章节文件"""
    for fname in filenames:
        path = os.path.join(tmpdir, fname)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f'# {fname}\n正文内容\n')
    return tmpdir


# ============================================================
# 测试用例
# ============================================================

class TestExtractTitle:
    """标题提取测试"""

    def test_normal_title(self):
        assert extract_title('第001章_暗流涌动.md') == '暗流涌动'

    def test_no_title(self):
        assert extract_title('第001章.md') == ''

    def test_space_separator(self):
        assert extract_title('第1章 秘密揭晓.md') == '秘密揭晓'

    def test_dash_separator(self):
        assert extract_title('第10章-命运的抉择.txt') == '命运的抉择'


class TestTitleCharCount:
    """字数统计测试"""

    def test_chinese_only(self):
        assert title_char_count('暗流涌动') == 4

    def test_mixed(self):
        assert title_char_count('第3次危机') == 4

    def test_empty(self):
        assert title_char_count('') == 0


class TestCheckTitleLength:
    """长度检查测试"""

    def test_no_title(self):
        issues = check_title_length('', 1)
        assert any(i['type'] == '无标题' for i in issues)

    def test_short_title(self):
        issues = check_title_length('逃', 2, min_len=2)
        assert any(i['type'] == '标题过短' for i in issues)

    def test_long_title(self):
        long_title = '这是一个非常非常非常非常非常非常长的标题超过二十五字'
        issues = check_title_length(long_title, 3, max_len=25)
        assert any(i['type'] == '标题过长' for i in issues)

    def test_good_title(self):
        issues = check_title_length('暗夜中的秘密追踪', 4)
        assert len(issues) == 0


class TestCheckTitleAttractiveness:
    """吸引力检查测试"""

    def test_flat_title_第二天(self):
        issues = check_title_attractiveness('第二天', 1)
        assert any(i['type'] == '平淡标题' for i in issues)

    def test_flat_title_only_number(self):
        issues = check_title_attractiveness('', 2)  # 无标题不算平淡标题，由长度检查处理
        assert not any(i['type'] == '平淡标题' for i in issues)

    def test_clickbait_title(self):
        title = '震惊！竟然意想不到的结局'
        issues = check_title_attractiveness(title, 3)
        assert any(i['type'] == '标题党' for i in issues)

    def test_spoiler_title(self):
        issues = check_title_attractiveness('大反派的最终覆灭', 4)
        assert any(i['type'] == '信息过量' for i in issues)

    def test_good_title(self):
        issues = check_title_attractiveness('暗流涌动', 5)
        assert len(issues) == 0


class TestCheckFormatConsistency:
    """格式一致性测试"""

    def test_inconsistent_separators(self):
        filenames = [(1, '第1章_标题A.md'), (2, '第2章-标题B.md')]
        issues = check_format_consistency(filenames)
        assert any(i['type'] == '格式不统一' for i in issues)

    def test_consistent_format(self):
        filenames = [(1, '第001章_标题A.md'), (2, '第002章_标题B.md')]
        issues = check_format_consistency(filenames)
        assert not any(i['type'] == '格式不统一' for i in issues)

    def test_inconsistent_padding(self):
        filenames = [(1, '第001章_标题A.md'), (2, '第2章_标题B.md')]
        issues = check_format_consistency(filenames)
        assert any(i['type'] == '编号格式不统一' for i in issues)


class TestCheckHooks:
    """钩子检测测试"""

    def test_no_hook_long_title(self):
        issues = check_hooks('平凡的一天开始了', 1)
        assert any(i['type'] == '缺少钩子' for i in issues)

    def test_has_hook(self):
        issues = check_hooks('隐藏的真相', 2)
        assert len(issues) == 0  # 有钩子词不报问题

    def test_short_title_no_hook_ok(self):
        issues = check_hooks('逃', 3)
        assert len(issues) == 0  # 短标题无钩子不报


class TestRunCheck:
    """集成测试"""

    def test_full_check_with_issues(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            create_chapter_dir(tmpdir, [
                '第001章.md',                  # 无标题
                '第002章_第二天.md',            # 平淡标题
                '第003章_暗流涌动.md',          # 好标题
            ])
            result = run_check(tmpdir, output_format='json')
            assert result['stats']['total_chapters'] == 3
            assert result['stats']['no_title'] == 1
            assert len(result['issues']) > 0

    def test_all_good_titles(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            create_chapter_dir(tmpdir, [
                '第001章_暗夜追踪.md',
                '第002章_迷雾重重.md',
                '第003章_真相浮现.md',
            ])
            result = run_check(tmpdir, output_format='json')
            assert result['stats']['total_chapters'] == 3
            # 这些标题都有钩子词，问题应该很少
            high_issues = [i for i in result['issues'] if i['severity'] == 'high']
            assert len(high_issues) == 0

    def test_version(self):
        assert VERSION == 'v2.2.1'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
