#!/usr/bin/env python3
"""Integration tests for image upload to UseMemos.

Requires USEMEMOS_URL and USEMEMOS_TOKEN in .env or environment.
Tests call the actual scripts in scripts/ as subprocesses.
"""
import hashlib
import json
import os
import re
import struct
import subprocess
import tempfile
import unittest
import urllib.error
import urllib.request
import zlib


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

def load_env():
    """Load .env file from project root."""
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    os.environ.setdefault(key.strip(), val.strip())


load_env()

BASE_URL = os.environ.get('USEMEMOS_URL', '').rstrip('/')
TOKEN = os.environ.get('USEMEMOS_TOKEN', '')
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'scripts')


# ---------------------------------------------------------------------------
# Helpers: call scripts as subprocesses
# ---------------------------------------------------------------------------

def run_script(script_name, args):
    """Run a script from scripts/ and return (stdout, stderr, returncode)."""
    cmd = ['python3', os.path.join(SCRIPTS_DIR, script_name)] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode


def script_create_memo(content, visibility='PRIVATE'):
    """Call create_memo.py and return the memo ID."""
    stdout, stderr, rc = run_script('create_memo.py', [content, visibility])
    if rc != 0:
        raise RuntimeError(f'create_memo.py failed: {stderr}')
    match = re.search(r'Created memo \[(.+?)\]', stdout)
    if not match:
        raise RuntimeError(f'Could not parse memo ID from: {stdout}')
    return match.group(1)


def script_upload_and_link(memo_id, filepath, filename, filetype):
    """Call upload_and_link_attachment.py and return stdout."""
    stdout, stderr, rc = run_script(
        'upload_and_link_attachment.py',
        [memo_id, filepath, filename, filetype],
    )
    if rc != 0:
        raise RuntimeError(f'upload_and_link_attachment.py failed: {stderr}')
    return stdout


# ---------------------------------------------------------------------------
# Helpers: API calls for verification and cleanup only
# ---------------------------------------------------------------------------

def api_request(path, method='GET', data=None):
    """Make an authenticated API request and return parsed JSON."""
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        f'{BASE_URL}{path}', data=body, headers=headers, method=method,
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_memo(memo_id):
    return api_request(f'/api/v1/memos/{memo_id}')


def delete_memo(memo_id):
    try:
        api_request(f'/api/v1/memos/{memo_id}', method='DELETE')
    except urllib.error.HTTPError:
        pass


def download_attachment(att_id, filename):
    """Download attachment file bytes from the file-serving endpoint."""
    url = f'{BASE_URL}/file/attachments/{att_id}/{filename}'
    req = urllib.request.Request(
        url, headers={'Authorization': f'Bearer {TOKEN}'},
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read(), resp.headers.get('Content-Type')


# ---------------------------------------------------------------------------
# Helpers: generate test images
# ---------------------------------------------------------------------------

def make_test_png(width=8, height=8, color=(255, 0, 0)):
    """Generate a minimal valid PNG file in memory."""
    import binascii

    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack('>I', binascii.crc32(c) & 0xFFFFFFFF)
        return struct.pack('>I', len(data)) + c + crc

    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    raw_data = b''
    for _ in range(height):
        raw_data += b'\x00'
        for _ in range(width):
            raw_data += bytes(color)
    compressed = zlib.compress(raw_data)
    return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')


def make_test_jpg(width=8, height=8, color=(255, 0, 0)):
    """Generate a valid JPEG via sips (macOS)."""
    png_data = make_test_png(width, height, color)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as pf:
        pf.write(png_data)
        png_path = pf.name
    jpg_path = png_path.replace('.png', '.jpg')
    try:
        subprocess.run(
            ['sips', '-s', 'format', 'jpeg', png_path, '--out', jpg_path],
            capture_output=True, check=True,
        )
        with open(jpg_path, 'rb') as f:
            return f.read()
    finally:
        for p in (png_path, jpg_path):
            try:
                os.unlink(p)
            except OSError:
                pass


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestImageUpload(unittest.TestCase):
    """Integration tests: create memos and upload images via scripts/."""

    created_memos = []

    @classmethod
    def setUpClass(cls):
        if not BASE_URL or not TOKEN:
            raise unittest.SkipTest('USEMEMOS_URL and USEMEMOS_TOKEN must be set')
        try:
            api_request('/api/v1/memos?pageSize=1')
        except Exception as e:
            raise unittest.SkipTest(f'Memos API not reachable: {e}')

    @classmethod
    def tearDownClass(cls):
        for memo_id in cls.created_memos:
            try:
                delete_memo(memo_id)
                print(f'  [CLEANUP] Deleted memo {memo_id}')
            except Exception as e:
                print(f'  [CLEANUP] Failed to delete memo {memo_id}: {e}')
        cls.created_memos.clear()

    def _track_memo(self, memo_id):
        self.created_memos.append(memo_id)
        return memo_id

    def _write_temp(self, data, suffix):
        f = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        f.write(data)
        f.close()
        return f.name

    # ------------------------------------------------------------------
    # Test 1: memo + 1 PNG
    # ------------------------------------------------------------------
    def test_01_memo_with_one_png(self):
        png_data = make_test_png(8, 8, (255, 0, 0))
        path = self._write_temp(png_data, '.png')
        try:
            memo_id = self._track_memo(
                script_create_memo('Test: 1 PNG attachment #integration_test'))

            script_upload_and_link(memo_id, path, 'red.png', 'image/png')

            memo = get_memo(memo_id)
            self.assertEqual(len(memo['attachments']), 1)
            att = memo['attachments'][0]
            self.assertEqual(att['filename'], 'red.png')
            self.assertEqual(att['type'], 'image/png')

            att_id = att['name'].split('/')[-1]
            dl_bytes, ct = download_attachment(att_id, 'red.png')
            self.assertEqual(ct, 'image/png')
            self.assertEqual(
                hashlib.md5(png_data).hexdigest(),
                hashlib.md5(dl_bytes).hexdigest(),
                'PNG must be stored binary-identical',
            )
        finally:
            os.unlink(path)

    # ------------------------------------------------------------------
    # Test 2: memo + 2 PNGs
    # ------------------------------------------------------------------
    def test_02_memo_with_two_pngs(self):
        png1 = make_test_png(8, 8, (255, 0, 0))
        png2 = make_test_png(8, 8, (0, 255, 0))
        path1 = self._write_temp(png1, '.png')
        path2 = self._write_temp(png2, '.png')
        try:
            memo_id = self._track_memo(
                script_create_memo('Test: 2 PNG attachments #integration_test'))

            script_upload_and_link(memo_id, path1, 'red.png', 'image/png')
            script_upload_and_link(memo_id, path2, 'green.png', 'image/png')

            memo = get_memo(memo_id)
            self.assertEqual(len(memo['attachments']), 2,
                             'Both PNGs must remain linked')
            filenames = {a['filename'] for a in memo['attachments']}
            self.assertEqual(filenames, {'red.png', 'green.png'})

            for att in memo['attachments']:
                att_id = att['name'].split('/')[-1]
                dl_bytes, ct = download_attachment(att_id, att['filename'])
                self.assertEqual(ct, 'image/png')
                expected = png1 if att['filename'] == 'red.png' else png2
                self.assertEqual(
                    hashlib.md5(expected).hexdigest(),
                    hashlib.md5(dl_bytes).hexdigest(),
                    f'{att["filename"]} must be stored binary-identical',
                )
        finally:
            os.unlink(path1)
            os.unlink(path2)

    # ------------------------------------------------------------------
    # Test 3: memo + 1 JPG
    # ------------------------------------------------------------------
    def test_03_memo_with_one_jpg(self):
        jpg_data = make_test_jpg(8, 8, (0, 128, 255))
        path = self._write_temp(jpg_data, '.jpg')
        try:
            memo_id = self._track_memo(
                script_create_memo('Test: 1 JPG attachment #integration_test'))

            script_upload_and_link(memo_id, path, 'photo.jpg', 'image/jpeg')

            memo = get_memo(memo_id)
            self.assertEqual(len(memo['attachments']), 1)
            att = memo['attachments'][0]
            self.assertEqual(att['filename'], 'photo.jpg')
            self.assertEqual(att['type'], 'image/jpeg')

            att_id = att['name'].split('/')[-1]
            dl_bytes, ct = download_attachment(att_id, 'photo.jpg')
            self.assertEqual(ct, 'image/jpeg')
            self.assertTrue(dl_bytes[:2] == b'\xff\xd8',
                            'Downloaded file must be valid JPEG (SOI marker)')
            self.assertGreater(len(dl_bytes), 0)

            if hashlib.md5(jpg_data).hexdigest() != hashlib.md5(dl_bytes).hexdigest():
                print(f'\n  [INFO] JPEG re-encoded by server: '
                      f'{len(jpg_data)}b -> {len(dl_bytes)}b')
        finally:
            os.unlink(path)

    # ------------------------------------------------------------------
    # Test 4: memo + 3 JPGs
    # ------------------------------------------------------------------
    def test_04_memo_with_three_jpgs(self):
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        jpgs = {}
        for idx, color in enumerate(colors, 1):
            fname = f'photo_{idx}.jpg'
            jpgs[fname] = make_test_jpg(8, 8, color)

        paths = {}
        for fname, data in jpgs.items():
            paths[fname] = self._write_temp(data, '.jpg')

        try:
            memo_id = self._track_memo(
                script_create_memo('Test: 3 JPG attachments #integration_test'))

            for fname, path in paths.items():
                script_upload_and_link(memo_id, path, fname, 'image/jpeg')

            memo = get_memo(memo_id)
            self.assertEqual(len(memo['attachments']), 3,
                             'All 3 JPGs must remain linked after sequential uploads')
            filenames = {a['filename'] for a in memo['attachments']}
            self.assertEqual(filenames, {'photo_1.jpg', 'photo_2.jpg', 'photo_3.jpg'})

            for att in memo['attachments']:
                att_id = att['name'].split('/')[-1]
                dl_bytes, ct = download_attachment(att_id, att['filename'])
                self.assertEqual(ct, 'image/jpeg')
                self.assertTrue(dl_bytes[:2] == b'\xff\xd8',
                                f'{att["filename"]} must be valid JPEG')
                self.assertGreater(len(dl_bytes), 0,
                                   f'{att["filename"]} must have content')
        finally:
            for path in paths.values():
                os.unlink(path)


if __name__ == '__main__':
    unittest.main(verbosity=2)
