import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/download.sh'


class DownloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.record = self.root / 'args.json'
        fake = self.bin / 'yt-dlp'
        import sys
        fake.write_text(f'#!{sys.executable}\n'
                        'import json, os, sys\n'
                        'with open(os.environ["ARG_RECORD"], "w") as f:\n'
                        '    json.dump(sys.argv[1:], f)\n'
                        'sys.exit(int(os.environ.get("FAKE_EXIT", "0")))\n')
        fake.chmod(0o755)
        self.env = {'HOME': str(self.root), 'PATH': f'{self.bin}:/usr/bin:/bin',
                    'ARG_RECORD': str(self.record), 'LC_ALL': 'C'}

    def run_script(self, *args):
        return subprocess.run(['/bin/bash', str(SCRIPT), *args], cwd=self.root,
                              env=self.env, capture_output=True, text=True, timeout=5)

    def args(self):
        return json.loads(self.record.read_text())

    def test_default(self):
        result = self.run_script('https://example.com/video?v=1&x=2')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.args(), ['--ignore-config', '--no-playlist', '--playlist-end', '1', '-P',
                                      str(self.root / 'Downloads/yt-dlp'), '--',
                                      'https://example.com/video?v=1&x=2'])
        self.assertNotIn('?v=1', result.stdout)

    def test_injection_is_literal(self):
        marker = self.root / 'injected'
        payload = f'$(touch${{IFS}}{marker})'
        url = f'https://example.com/{payload}'
        path = str(self.root / f'folder " {payload}')
        fmt = f'best";{payload};"'
        result = self.run_script('--path', path, '--format', fmt, url)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists())
        self.assertIn(path, self.args())
        self.assertIn(fmt, self.args())
        self.assertEqual(self.args()[-1], url)

    def test_invalid_input_has_no_side_effects(self):
        cases = [[], ['--path'], ['--quality'], ['--format'], ['--path', ''],
                 ['--unknown'], ['file:///etc/passwd'], ['https://'],
                 ['https://example.com/a\nb'], ['--exec=command'],
                 ['https://a', 'https://b'], ['--quality', '0', 'https://a'],
                 ['--quality', '720;id', 'https://a'],
                 ['--quality', '720', '--format', 'best', 'https://a']]
        for case in cases:
            with self.subTest(case=case):
                self.assertNotEqual(self.run_script(*case).returncode, 0)
                self.assertFalse(self.record.exists())
                self.assertFalse((self.root / 'Downloads').exists())

    def test_list_does_not_create_directory(self):
        result = self.run_script('--list', '--', 'https://example.com')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.args(), ['--ignore-config', '--no-playlist', '--playlist-end', '1', '-F',
                                      '--', 'https://example.com'])
        self.assertFalse((self.root / 'Downloads').exists())

    def test_options(self):
        ffmpeg = self.bin / 'ffmpeg'
        ffmpeg.write_text('#!/bin/sh\nexit 0\n')
        ffmpeg.chmod(0o755)
        result = self.run_script('--audio', '--subs', '--quality', '720',
                                 '--playlist', '--path', '~/media', 'https://example.com')
        self.assertEqual(result.returncode, 0, result.stderr)
        args = self.args()
        self.assertIn('--yes-playlist', args)
        self.assertNotIn('--no-playlist', args)
        self.assertIn('bestvideo[height<=720]+bestaudio/best[height<=720]', args)
        self.assertIn(str(self.root / 'media'), args)
        self.assertIn('--write-subs', args)
        self.assertIn('mp3', args)

    def test_failure_does_not_report_success(self):
        self.env['FAKE_EXIT'] = '7'
        result = self.run_script('https://example.com')
        self.assertEqual(result.returncode, 7)
        self.assertNotIn('Download complete', result.stdout)

    def test_help(self):
        self.assertEqual(self.run_script('--help').returncode, 0)
        self.assertFalse(self.record.exists())


if __name__ == '__main__':
    unittest.main()
