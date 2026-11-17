"""Actual automated tests of the stdlib script; no model calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'preflight-check.py'
spec = importlib.util.spec_from_file_location('preflight', SCRIPT)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class PreflightTests(unittest.TestCase):
    def run_cli(self, text, *args, json_output=True):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'draft.md'
            path.write_text(text, encoding='utf-8')
            result = subprocess.run([sys.executable, str(SCRIPT), str(path), *args,
                                     *(['--json'] if json_output else [])], capture_output=True, text=True)
            self.assertEqual(path.read_text(encoding='utf-8'), text, 'script must not mutate its input')
        return result, json.loads(result.stdout) if json_output else result.stdout

    def value(self, data, name):
        return next(row['value'] for row in data['rows'] if row['name'] == name)

    def test_short_dashes_and_normal_headings_are_allowed(self):
        result, data = self.run_cli('# 01 核验\n\n这个结果——还需要复核。', '--tier', 'short', '--strict')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['fail'], 0)
        self.assertEqual(self.value(data, '短文本破折号(允许使用)'), 1)
        self.assertEqual(self.value(data, '编号式小标题(可选体例)'), 1)

    def test_default_format_advice_does_not_fail(self):
        result, data = self.run_cli('这段中文， 有额外空格。另一个结果--尚未确认。')
        self.assertEqual(result.returncode, 0)
        self.assertGreater(data['warn'], 0)
        self.assertTrue(all(row['level'] != 'FAIL' for row in data['rows']))

    def test_check_without_strict_is_advisory(self):
        result, data = self.run_cli('这段中文， 有空格。', '--check', 'spacing')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['fail'], 0)

    def test_strict_only_selected_constraint_fails(self):
        result, data = self.run_cli('这段中文， 有空格。', '--strict', '--check', 'spacing')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data['fail'], 1)
        failing = [r for r in data['rows'] if r['mark'] == 'FAIL']
        self.assertTrue(all(r['check'] == 'spacing' for r in failing))

    def test_unselected_spacing_does_not_fail(self):
        result, data = self.run_cli('这段中文， 有空格。', '--strict', '--check', 'dashes')
        self.assertEqual(result.returncode, 0)
        self.assertGreater(data['warn'], 0)

    def test_repeated_checks_and_duplicate_check(self):
        result, data = self.run_cli('这段中文， 有空格。这是另一个--结果。', '--strict',
                                    '--check', 'spacing', '--check', 'dashes', '--check', 'spacing')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data['fail'], 2)
        self.assertEqual(data['checks'], ['dashes', 'spacing'])

    def test_numbered_heading_is_only_an_explicit_constraint(self):
        result, data = self.run_cli('# 01 Heading\n\nEnglish text.', '--strict', '--check', 'numbered-headings')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(data['fail'], 1)

    def test_markdown_heading_space_is_not_punctuation_space(self):
        result, data = self.run_cli('## “引言标题”\n\n这是正文。', '--lang', 'zh', '--strict', '--check', 'spacing')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(self.value(data, '标点周边空格'), 0)

    def test_baseline_never_infers_transcription_from_counts(self):
        for text in ('他说"好"。', '他说“好”，又说"再见"。'):
            note = preflight.baseline_note(text)
            self.assertIn('不能判断', note)
            self.assertIn('不要自动替换', note)
        self.assertIsNone(preflight.baseline_note('他说“好”。'))

    def test_mixed_english_quotes_apostrophe_and_dashes_are_protected(self):
        result, data = self.run_cli('中文正文需要保留英文引文和术语。He said "don\'t... -- stop".\n\n这是中文说明。',
                                    '--lang', 'zh', '--strict', '--check', 'quotes', '--check', 'punctuation', '--check', 'dashes')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['fail'], 0)
        self.assertEqual(self.value(data, '半角双引号 "(含行内引语)'), 2)

    def test_chinese_inline_quotations_are_protected(self):
        result, data = self.run_cli('作者原文是“保留, 这句--原话”。另有"不要, 改动--引文"。\n\n正文内容。',
                                    '--lang', 'zh', '--strict', '--check', 'quotes', '--check', 'punctuation', '--check', 'dashes')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['fail'], 0)

    def test_protected_inline_spans_do_not_create_phantom_spacing_warnings(self):
        for text in ('作者说：“保留,原话--不要改”，随后离开。',
                     '记录：[详情](https://example.com/path)。',
                     '这是记录：https://example.com/path。',
                     '这是代码：``中文, --``，保持原样。'):
            with self.subTest(text=text):
                result, data = self.run_cli(text, '--lang', 'zh', '--strict', '--check', 'spacing')
                self.assertEqual(result.returncode, 0)
                self.assertEqual(data['fail'], 0)

    def test_unpaired_ascii_quote_can_be_an_explicit_constraint(self):
        result, data = self.run_cli('这是中文正文末尾的引号"', '--strict', '--check', 'quotes')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.value(data, '未保护的半角双引号 "'), 1)

    def test_english_apostrophe_is_not_consumed_as_a_chinese_quote(self):
        result, data = self.run_cli("这是说明don't还有isn't需要保留原样。", '--lang', 'zh', '--strict', '--check', 'quotes')
        self.assertEqual(result.returncode, 0)

    def test_tilde_fence_and_longer_backtick_fence(self):
        for fence in ('~~~', '~~~~', '```', '````', '`````'):
            with self.subTest(fence=fence):
                text = f'正文说明。\n\n{fence}python\n中文, "raw" -- ...\n{fence}\n\n结束。'
                result, data = self.run_cli(text, '--lang', 'zh', '--strict', '--check', 'punctuation', '--check', 'quotes', '--check', 'dashes')
                self.assertEqual(result.returncode, 0)
                self.assertEqual(data['cjk'], 6)

    def test_shorter_or_different_fence_does_not_close_code(self):
        text = '````\n```\n~~~\n中文, -- ...\n````\n正文。'
        self.assertNotIn('中文', preflight.strip_code(text))
        self.assertIn('正文', preflight.strip_code(text))

    def test_unterminated_fence_stays_protected(self):
        result, data = self.run_cli('正文。\n\n~~~\n中文, -- ...', '--lang', 'zh', '--strict', '--check', 'punctuation')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['cjk'], 2)

    def test_inline_code_multiple_backticks(self):
        text = '正文 ``中文, `nested` -- ...`` 说明。'
        result, data = self.run_cli(text, '--lang', 'zh', '--strict', '--check', 'punctuation', '--check', 'dashes')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['cjk'], 4)

    def test_inline_code_can_span_soft_line_wraps(self):
        result, data = self.run_cli('正文 `中文,\n-- ...` 说明。', '--lang', 'zh', '--strict', '--check', 'punctuation')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['cjk'], 4)

    def test_indented_code_is_excluded(self):
        result, data = self.run_cli('正文。\n\n    中文, -- ...\n', '--lang', 'zh', '--strict', '--check', 'punctuation')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['cjk'], 2)

    def test_blockquote_and_lazy_continuation_are_protected(self):
        text = '> 引文, -- ...\n懒续行, -- ...\n\n这是正文。'
        result, data = self.run_cli(text, '--lang', 'zh', '--strict', '--check', 'punctuation', '--check', 'dashes')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['cjk'], 4)
        self.assertEqual(self.value(data, '段落总数'), 1)

    def test_urls_link_destinations_and_citation_definitions(self):
        text = '这是[记录](https://example.com/a_(b)?q="x" "title")。\n\nhttps://example.com/--/...\n\n[^1]: 引文, -- ...\n\n结束。'
        result, data = self.run_cli(text, '--lang', 'zh', '--strict', '--check', 'punctuation', '--check', 'quotes', '--check', 'dashes')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(data['cjk'], 6)

    def test_soft_line_wraps_do_not_change_paragraph_or_rhetoric_stats(self):
        original = '黄昏，大地温柔的信使。晚风，远方沉默的叹息。\n\n这是另一段。'
        wrapped = '黄昏，大地温柔\n的信使。晚风，远方沉默\n的叹息。\n\n这是另一段。'
        _, first = self.run_cli(original, '--tier', 'literary')
        _, second = self.run_cli(wrapped, '--tier', 'literary')
        self.assertEqual(first['rows'], second['rows'])
        self.assertEqual(self.value(first, '段落总数'), 2)
        self.assertEqual(self.value(first, '同位语单段峰值(粗计)'), 2)

    def test_paragraphs_exclude_headings_lists_tables_and_separators(self):
        text = '# 标题\n\n段落一。\n软换行。\n\n1. 列表\n继续列表\n\n- 列表二\n\n| 栏 | 值 |\n|---|---|\n\n---\n\n段落二。'
        self.assertEqual(preflight.body_paragraphs(text), ['段落一。软换行。', '段落二。'])

    def test_setext_heading_not_a_body_paragraph(self):
        self.assertEqual(preflight.body_paragraphs('标题\n====\n\n正文。'), ['正文。'])

    def test_language_boundary_strictly_greater_than_half(self):
        for text, expected in (('中文ab', False), ('中文文ab', True), ('中ab', False), ('123。', False)):
            with self.subTest(text=text):
                _, data = self.run_cli(text)
                self.assertEqual(data['zh_mode'], expected)

    def test_language_ratio_excludes_code_urls_and_quotations(self):
        _, data = self.run_cli('中文。\n\n```\nabcdef\n```\n\n> abcdef\n\nhttps://abc.example\n\n"abcdef"')
        self.assertTrue(data['zh_mode'])
        self.assertEqual(data['cjk_ratio'], 1.0)

    def test_explicit_language_override_does_not_lie_about_ratio(self):
        result, data = self.run_cli('中文, abcdef', '--lang', 'en', '--strict', '--check', 'punctuation')
        self.assertEqual(result.returncode, 0)
        self.assertIn('显式指定 en', data['lang_note'])
        result, data = self.run_cli('中文, abcdef', '--lang', 'zh', '--strict', '--check', 'punctuation')
        self.assertEqual(result.returncode, 1)
        self.assertTrue(data['zh_mode'])
        self.assertLess(data['cjk_ratio'], 0.5)

    def test_high_word_frequency_rhetoric_and_long_paragraph_never_fail_strict(self):
        text = ('咱们其实大概，温柔的信使，沉默的回响。' * 30)
        result, data = self.run_cli(text, '--tier', 'literary', '--para-max', '10', '--strict', '--check', 'spacing')
        self.assertEqual(result.returncode, 0)
        self.assertGreater(data['warn'], 0)
        for row in data['rows']:
            if row['scope'] in ('SS-CN8', 'R类', '节奏'):
                self.assertEqual(row['level'], 'INFO')
                self.assertIsNone(row['limit'])

    def test_short_tier_has_no_ss_cn8(self):
        _, data = self.run_cli('这段中文很短。', '--tier', 'short')
        self.assertFalse(any(r['scope'] == 'SS-CN8' for r in data['rows']))

    def test_lyrical_flag_adds_rhetoric_to_short_tier(self):
        _, data = self.run_cli('黄昏，大地温柔的信使。', '--tier', 'short', '--lyrical')
        self.assertTrue(any(r['scope'] == 'R类' for r in data['rows']))

    def test_cut_ignores_tail_and_uses_first_literal_marker(self):
        result, data = self.run_cli('正文。\n\n## 本轮改动\n这里， 有空格。\n## 本轮改动\n更多。',
                                    '--cut', '## 本轮改动', '--strict', '--check', 'spacing')
        self.assertEqual(result.returncode, 0)
        self.assertTrue(data['cut_found'])
        self.assertEqual(data['cjk'], 2)

    def test_missing_cut_is_visible(self):
        _, data = self.run_cli('正文。', '--cut', '不存在')
        self.assertFalse(data['cut_found'])
        self.assertTrue(any('未找到' in note for note in data['notes']))

    def test_before_after_fixture_has_real_format_result_and_keeps_facts(self):
        outputs = []
        for name in ('original.md', 'revised.md'):
            raw = (ROOT / 'tests' / 'fixtures' / name).read_text()
            result, data = self.run_cli(raw, '--lang', 'zh', '--strict', '--check', 'spacing')
            outputs.append((result.returncode, data['fail']))
            for preserved in ('使用 AI 辅助初稿', '2026-10-16', '12 次', 'https://example.com/log?q=12', '> 原始记录：“核验完成。”'):
                self.assertIn(preserved, raw)
        self.assertEqual(outputs, [(1, 1), (0, 0)])

    def test_text_and_json_exit_codes_agree(self):
        for text, expected in (('正文， 有空格。', 1), ('正文，没有空格。', 0)):
            first, _ = self.run_cli(text, '--strict', '--check', 'spacing')
            second, output = self.run_cli(text, '--strict', '--check', 'spacing', json_output=False)
            self.assertEqual(first.returncode, expected)
            self.assertEqual(second.returncode, expected)
            self.assertIn(f'格式约束失败 {expected} 项', output)

    def test_json_schema_and_empty_input(self):
        result, data = self.run_cli('')
        self.assertEqual(result.returncode, 0)
        self.assertTrue({'file', 'tier', 'cjk', 'cjk_ratio', 'zh_mode', 'rows', 'fail', 'warn'} <= data.keys())
        self.assertEqual(self.value(data, '段落总数'), 0)
        self.assertEqual(self.value(data, '最长段落(字)'), 0)

    def test_missing_file_reports_json_error_and_exit_two(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '/nonexistent/text-humanize.md', '--json'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('error', json.loads(result.stdout))
        self.assertNotIn('Traceback', result.stderr)

    def test_bad_arguments_exit_two(self):
        for args in (('--para-max', '0'), ('--para-max', '-1'), ('--check', 'typos'), ('--tier', 'unknown')):
            result = subprocess.run([sys.executable, str(SCRIPT), 'unused', *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)


if __name__ == '__main__':
    unittest.main()
