import json
from pathlib import Path
import tempfile
import unittest

from inspect_data import inspect


class InventoryTest(unittest.TestCase):
    def test_inventory_is_read_only_and_does_not_read_profiles_or_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = root / 'plugins/com.example.demo.sdPlugin'
            plugin.mkdir(parents=True)
            manifest = plugin / 'manifest.json'
            manifest.write_text(json.dumps({
                'UUID': 'com.example.demo', 'Version': '1.0', 'SDKVersion': 1,
                'Nodejs': {'Version': '20'}, 'Actions': [{'UUID': 'com.example.demo.key'}],
                'privateSetting': 'must-not-appear',
            }), encoding='utf-8-sig')
            profile = root / 'profiles/private-scene.sdProfile'
            profile.mkdir(parents=True)
            (profile / 'manifest.json').write_text('must-not-appear', encoding='utf-8')
            (root / 'StreamDockConfig.ini').write_text('must-not-appear', encoding='utf-8')
            bad = root / 'plugins/com.example.broken.sdPlugin'
            bad.mkdir()
            (bad / 'manifest.json').write_text('{malformed', encoding='utf-8')
            (root / 'plugins/com.example.link.sdPlugin').symlink_to(plugin, target_is_directory=True)
            before = manifest.read_bytes()
            result = inspect(root)
            self.assertFalse(result['activeHostConfirmed'])
            self.assertEqual(result['rootProfileCount'], 1)
            self.assertTrue(result['selectionConfigExists'])
            self.assertEqual(len(result['plugins']), 1)
            self.assertEqual(result['plugins'][0]['actionCount'], 1)
            self.assertEqual(len(result['warnings']), 2)
            self.assertNotIn('must-not-appear', json.dumps(result))
            self.assertNotIn('private-scene', json.dumps(result))
            self.assertEqual(manifest.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
