import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from scaffold import scaffold
from package_plugin import checked_file, package_plugin


class HelpersTest(unittest.TestCase):
    def test_scaffold_keeps_existing_and_handles_unicode(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'com.example.demo.sdPlugin'
            scaffold('com.example.demo', 'Test "counter" \u2603', target)
            manifest = json.loads((target / 'manifest.json').read_text())
            self.assertEqual(manifest['Name'], 'Test "counter" \u2603')
            self.assertEqual(manifest['Actions'][1]['Controllers'], ['Knob'])
            before = (target / 'manifest.json').read_bytes()
            with self.assertRaises(FileExistsError):
                scaffold('com.example.demo', 'replacement', target)
            self.assertEqual(before, (target / 'manifest.json').read_bytes())

    def test_paths_reject_escape_and_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'outside.txt').write_text('not a runtime asset')
            for path in ['../outside.txt', '/outside.txt', 'folder\\outside.txt']:
                with self.assertRaises(ValueError):
                    checked_file(root, path)
            (root / 'link').symlink_to(root / 'outside.txt')
            with self.assertRaises(ValueError):
                checked_file(root, 'link')

    def test_package_excludes_private_files_and_keeps_license(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / 'com.example.demo.sdPlugin'
            scaffold('com.example.demo', 'Demo', root)
            ws = root / 'node_modules/ws'
            (ws / 'lib').mkdir(parents=True)
            for filename in ['index.js', 'browser.js', 'wrapper.mjs', 'LICENSE', 'lib/websocket.js']:
                (ws / filename).write_text('fixture')
            (ws / 'package.json').write_text(json.dumps({'version': '8.22.0'}))
            (root / 'package-lock.json').write_text(json.dumps({'packages': {'node_modules/ws': {'version': '8.22.0'}}}))
            (root / 'config.json').write_text('{"token":"private-fixture"}')
            (root / '.env').write_text('TOKEN=private-fixture')
            (root / 'runtime.log').write_text('private-fixture')
            output = Path(temporary) / 'plugin.zip'
            package_plugin(root, output)
            with zipfile.ZipFile(output) as archive:
                names = archive.namelist()
                self.assertTrue(any(name.endswith('/ws/LICENSE') for name in names))
                self.assertFalse(any(name.endswith(('config.json', '.env', 'runtime.log', 'smoke.cjs')) for name in names))
            with self.assertRaises(FileExistsError):
                package_plugin(root, output)
            manifest_path = root / 'manifest.json'
            manifest = json.loads(manifest_path.read_text())
            manifest['Icon'] = 'private.png'
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError):
                package_plugin(root, Path(temporary) / 'bad.zip')


if __name__ == '__main__':
    unittest.main()
