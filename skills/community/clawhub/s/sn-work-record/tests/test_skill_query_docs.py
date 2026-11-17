"""Local skill routing, safety and context-budget regression checks (no network)."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SkillDocumentationTests(unittest.TestCase):
    def test_main_is_small_and_has_batch_entry(self):
        main = (ROOT / 'SKILL.md').read_text()
        self.assertLessEqual(len(main), 3500)
        self.assertIn('query_time_ranges.py', main)
        self.assertIn('--range', main)
        self.assertIn('不逐天', main)

    def test_direct_reference_links_exist(self):
        docs = [ROOT / 'SKILL.md'] + [ROOT / 'references' / name for name in (
            'query-workflow.md', 'write-workflow.md', 'authentication-runtime.md',
            'reimbursement-query.md', 'script-catalog.md')]
        for doc in docs:
            for link in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
                if '://' not in link and not link.startswith('#'):
                    with self.subTest(doc=doc.name, link=link):
                        self.assertTrue((doc.parent / link.split('#')[0]).exists())

    def test_main_keeps_nonnegotiable_boundaries(self):
        main = (ROOT / 'SKILL.md').read_text()
        for text in ('不授权写入', '不暴露凭据', '时长无 8h 默认', '须专门授权',
                     '不盲重发', '预览不是提交成功', '节假日禁止新增',
                     '草稿', '部分失败', '不夸大'):
            self.assertIn(text, main)

    def test_write_protections_remain_routed_and_preserved(self):
        main = (ROOT / 'SKILL.md').read_text()
        write = (ROOT / 'references/write-workflow.md').read_text()
        for filename in ('write-workflow.md', 'submission-idempotency.md',
                         'amendment-workflow.md', 'personal-settings.md'):
            self.assertIn(filename, main)
        for text in ('submitted-confirmed', 'observed-after-uncertain',
                     '同参数真实提交', '缺少字段', '节假日', '撤回', '中断'):
            self.assertIn(text, write)

    def test_query_and_reimbursement_policy_preserved(self):
        query = (ROOT / 'references/query-workflow.md').read_text()
        fee = (ROOT / 'references/reimbursement-query.md').read_text()
        for text in ('query_time_ranges.py', '按记录 ID', '十进制', '不宣称整月'):
            self.assertIn(text.replace('按记录 ID', '记录 ID'), query)
        for text in ('审批通过不等于', '自然时间', '两行', '金额 + 状态', '--with-progress'):
            self.assertIn(text, fee)

if __name__ == '__main__':
    unittest.main()
