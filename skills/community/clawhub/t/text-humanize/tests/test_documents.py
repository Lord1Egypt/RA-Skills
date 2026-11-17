"""Static document checks, distinct from unexecuted model behavior cases."""
import ast
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DocumentTests(unittest.TestCase):
    def test_current_local_markdown_links_resolve(self):
        documents = [ROOT / 'SKILL.md', ROOT / 'README.md', ROOT / 'tests' / 'README.md',
                     *sorted((ROOT / 'references').glob('*.md'))]
        for document in documents:
            for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                self.assertTrue((document.parent / target.split('#')[0]).exists(), f'{document}: {target}')

    def test_exactly_four_current_references(self):
        self.assertEqual({p.name for p in (ROOT / 'references').glob('*.md')}, {
            'style-patterns-cn.md', 'style-patterns-en.md', 'rhetoric-cn.md', 'lyrical-appositive.md'})

    def test_no_old_reference_paths_in_active_documents(self):
        for document in [ROOT / 'SKILL.md', ROOT / 'README.md', *sorted((ROOT / 'references').glob('*.md'))]:
            self.assertNotRegex(document.read_text(), r'ai-smells(?:-r)?-(?:cn|en)\.md')

    def test_script_imports_only_standard_library(self):
        tree = ast.parse((ROOT / 'scripts' / 'preflight-check.py').read_text())
        imports = {alias.name for node in ast.walk(tree) if isinstance(node, ast.Import) for alias in node.names}
        self.assertEqual(imports, {'argparse', 'json', 'pathlib', 're', 'sys'})
        self.assertFalse(any(isinstance(n, ast.ImportFrom) for n in ast.walk(tree)))

    def test_behavior_manifest_is_explicitly_not_run(self):
        manifest = json.loads((ROOT / 'tests' / 'behavior-cases.json').read_text())
        self.assertEqual(manifest['status'], 'not_run')
        self.assertEqual(len(manifest['cases']), 12)
        ids = [case['id'] for case in manifest['cases']]
        self.assertEqual(len(ids), len(set(ids)))
        for case in manifest['cases']:
            self.assertTrue(case['prompt'])
            self.assertTrue(case['expected'])

    def test_version_and_history_boundary(self):
        self.assertIn('**Version**: 1.6.0', (ROOT / 'SKILL.md').read_text())
        self.assertIn('旧版目标和写作规则已废弃', (ROOT / 'SKILL.md').read_text())
        changelog = (ROOT / 'CHANGELOG.md').read_text()
        self.assertLess(changelog.index('### v1.6.0'), changelog.index('### v1.4.0'))
        self.assertIn('不作为当前操作规则', changelog)


if __name__ == '__main__':
    unittest.main()
