from pathlib import Path
import argparse
import json
import subprocess
import sys
import tempfile
import unittest

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import u1_trellis as runner


class TrellisRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='u1-trellis-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def image(self, name='source.png', alpha=True):
        path = self.root / name
        image = Image.new('RGBA', (12, 18), (100, 60, 30, 0 if alpha else 255))
        for x in range(3, 9):
            for y in range(3, 15):
                image.putpixel((x, y), (100, 60, 30, 255))
        image.save(path)
        return path

    def manifest(self, program='raise SystemExit(7)\n'):
        source = self.root / 'runtime/trellis-v1'
        dino = self.root / 'runtime/torch/hub/dinov2'
        snapshot = self.root / 'runtime/weights'
        for folder in [source / 'scripts', source / 'trellis', dino, snapshot]:
            folder.mkdir(parents=True, exist_ok=True)
        (source / 'scripts/run_real_pipeline.py').write_text(program)
        (dino / 'hubconf.py').write_text('# fixture encoder\n')
        (snapshot / 'pipeline.json').write_text('{}')
        (snapshot / 'weight.safetensors').write_bytes(b'fixture weights')
        checkpoint = self.root / 'runtime/torch/hub/checkpoints/dinov2_vitl14_reg4_pretrain.pth'
        checkpoint.parent.mkdir()
        checkpoint.write_bytes(b'fixture encoder weights')
        paths = runner.source_files(source, dino)
        assets = [snapshot / 'pipeline.json', snapshot / 'weight.safetensors', checkpoint]
        data = {'schema_version': 1, 'source_commit': runner.SOURCE_COMMIT,
                'dino_commit': runner.DINO_COMMIT, 'model_revision': runner.MODEL_REVISION,
                'source': str(source), 'dino_source': str(dino), 'python': sys.executable,
                'snapshot': str(snapshot), 'torch_home': str(self.root / 'runtime/torch'),
                'sources': {str(p): runner.file_record(p) for p in paths},
                'assets': {str(p): runner.file_record(p) for p in assets},
                'environment_pointers': {}}
        manifest = self.root / 'runtime/trellis-engine.json'
        runner.write_json(manifest, data)
        return manifest, data

    def test_output_guard_preserves_existing_folder_and_dangling_link(self):
        source = self.image()
        for name, symlink in [('existing', False), ('link', True)]:
            output = self.root / name
            if symlink:
                output.symlink_to(self.root / 'missing', target_is_directory=True)
            else:
                output.mkdir()
                (output / 'keep').write_text('original')
            with self.assertRaisesRegex(ValueError, 'must not exist'):
                runner.validate_paths([source], output)
        self.assertEqual((self.root / 'existing/keep').read_text(), 'original')
        self.assertFalse((self.root / 'missing').exists())

    def test_identical_files_are_not_treated_as_distinct_views(self):
        source = self.image()
        duplicate = self.root / 'copy.png'
        duplicate.write_bytes(source.read_bytes())
        for sources in [[source, source], [source, duplicate]]:
            with self.assertRaisesRegex(ValueError, 'Duplicate'):
                runner.validate_paths(sources, self.root / 'new')

    def test_offline_environment_uses_local_assets_and_restores_memory_guards(self):
        _, manifest = self.manifest()
        inherited = {'PYTORCH_MPS_HIGH_WATERMARK_RATIO': '0.0', 'PYTORCH_MPS_LOW_WATERMARK_RATIO': '0.0',
                     'PYTHONPATH': '/some/other/source', 'TRELLIS_LATENT_CHECKPOINT': '/old/job.pt'}
        environment = runner.offline_environment(self.root / 'runtime', manifest, inherited)
        for key in inherited:
            self.assertNotIn(key, environment)
        self.assertEqual(environment['HF_HUB_OFFLINE'], '1')
        self.assertEqual(environment['TRANSFORMERS_OFFLINE'], '1')
        self.assertEqual(environment['TRELLIS_LOW_MEMORY'], '1')
        self.assertEqual(environment['TRELLIS_MODEL_PATH'], manifest['snapshot'])
        self.assertEqual(environment['TRELLIS_DINOV2_SOURCE'], manifest['dino_source'])

    def test_source_and_encoder_cache_changes_fail_before_generation(self):
        path, manifest = self.manifest()
        runner.verify_manifest(path)
        extra = Path(manifest['dino_source']) / 'unexpected.py'
        extra.write_text('# changed source')
        with self.assertRaisesRegex(ValueError, 'source file set'):
            runner.verify_manifest(path)
        extra.unlink()
        checkpoint = Path(manifest['torch_home']) / 'hub/checkpoints/dinov2_vitl14_reg4_pretrain.pth'
        checkpoint.unlink()
        with self.assertRaisesRegex(ValueError, 'missing or changed'):
            runner.verify_manifest(path)

    def test_same_size_weight_corruption_is_detected_by_generation_preflight(self):
        path, manifest = self.manifest()
        weight = Path(manifest['snapshot']) / 'weight.safetensors'
        weight.write_bytes(b'x' * weight.stat().st_size)
        runner.verify_manifest(path, verify_assets=False)  # fast doctor explicitly does not verify weight hashes
        with self.assertRaisesRegex(ValueError, 'checksum changed'):
            runner.verify_manifest(path, verify_assets=True)

    def test_provided_alpha_and_original_bytes_are_preserved(self):
        source = self.image()
        original = source.read_bytes()
        output = self.root / 'new'
        output.mkdir()
        prepared, records = runner.prepare_images([source], output, self.root / 'missing-vision')
        self.assertEqual(source.read_bytes(), original)
        self.assertEqual(Path(records[0]['preserved']).read_bytes(), original)
        self.assertEqual(records[0]['preparation'], 'provided_alpha')
        with Image.open(prepared[0]) as image:
            self.assertEqual(image.size, (12, 18))
            self.assertEqual(image.getextrema()[3], (0, 255))

    def test_opaque_input_requires_native_extraction_without_model_fallback(self):
        source = self.image(alpha=False)
        output = self.root / 'new'
        output.mkdir()
        with self.assertRaisesRegex(ValueError, 'Apple Vision'):
            runner.prepare_images([source], output, self.root / 'missing-vision')

    def test_failed_subprocess_is_recorded_as_failed_not_a_candidate(self):
        path, _ = self.manifest()
        source = self.image()
        output = self.root / 'new'
        args = argparse.Namespace(images=[source], output_dir=output, seed=1, steps=25)
        with self.assertRaisesRegex(RuntimeError, 'exit 7'):
            runner.generate(args, {}, self.root / 'runtime', path)
        job = json.loads((output / 'job.json').read_text())
        self.assertEqual(job['status'], 'failed')
        self.assertFalse(job['ready_to_print'])
        self.assertFalse(job['likeness_accepted'])
        self.assertTrue((output / 'inputs/original-01.png').is_file())
        self.assertTrue((output / 'run.log').is_file())

    def test_command_passes_real_distinct_images_to_multi_image_cli(self):
        _, manifest = self.manifest()
        photos = [self.root / 'one.png', self.root / 'two.png', self.root / 'three.png']
        command = runner.generation_command(manifest, photos, self.root / 'new')
        self.assertEqual(command.count('--additional-image'), 2)
        self.assertIn('--require-alpha', command)
        self.assertNotIn('--include-radiance-field', command)
        for photo in photos:
            self.assertIn(str(photo), command)

    def test_child_network_guard_blocks_ip_and_dns_but_allows_unix_ipc(self):
        probe = self.root / 'socket_probe.py'
        probe.write_text('''import json, socket, tempfile
from pathlib import Path
blocked = []
def expect_blocked(name, operation):
    try:
        operation()
    except PermissionError:
        blocked.append(name)
    else:
        raise AssertionError(name + " was not blocked")
for family, address in [(socket.AF_INET, ("127.0.0.1", 9)), (socket.AF_INET6, ("::1", 9))]:
    with socket.socket(family, socket.SOCK_STREAM) as connection:
        expect_blocked(str(family)+"connect", lambda: connection.connect(address))
        expect_blocked(str(family)+"connect_ex", lambda: connection.connect_ex(address))
        expect_blocked(str(family)+"send", lambda: connection.send(b"x"))
        expect_blocked(str(family)+"sendall", lambda: connection.sendall(b"x"))
    with socket.socket(family, socket.SOCK_DGRAM) as connection:
        expect_blocked(str(family)+"sendto", lambda: connection.sendto(b"x", address))
for name, arguments in [("getaddrinfo", ("localhost", 9)), ("gethostbyname", ("localhost",)), ("gethostbyname_ex", ("localhost",)), ("gethostbyaddr", ("127.0.0.1",)), ("getnameinfo", (("127.0.0.1", 9), 0))]:
    expect_blocked(name, lambda: getattr(socket, name)(*arguments))
left, right = socket.socketpair(socket.AF_UNIX)
with left, right:
    left.sendall(b"local")
    assert right.recv(5) == b"local"
print(json.dumps({"blocked_operations": len(blocked), "unix_ipc": "passed"}))
''')
        result = subprocess.run([sys.executable, str(runner.SKILL_ROOT / 'scripts/u1_offline_exec.py'), '--', str(probe)],
                                check=False, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), {'blocked_operations': 15, 'unix_ipc': 'passed'})


if __name__ == '__main__':
    unittest.main()
