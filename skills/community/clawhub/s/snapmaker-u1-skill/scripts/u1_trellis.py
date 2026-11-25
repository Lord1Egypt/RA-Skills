#!/usr/bin/env python3
"""Run the reviewed local TRELLIS Mac runtime from one or more real photos.

No downloads or cloud services. `configure` pins an existing installation;
generation remains experimental and never establishes likeness or printability.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

SKILL_ROOT = Path(__file__).resolve().parents[1]
SOURCE_COMMIT = 'f7c175a8620c2c23923d5b6fca3bf7f53604335f'
DINO_COMMIT = '7764ea0f912e53c92e82eb78a2a1631e92725fc8'
MODEL_REVISION = '25e0d31ffbebe4b5a97464dd851910efc3002d96'
SOURCE_EXTENSIONS = {'.py', '.metal', '.h', '.cpp', '.mm'}


def digest(path):
    value = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            value.update(block)
    return value.hexdigest()


def write_json(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')
    temporary.replace(path)


def settings(config_path):
    config = json.loads(Path(config_path).read_text()) if Path(config_path).is_file() else {}
    runtime = Path(config.get('runtime_dir', SKILL_ROOT / '.runtime')).expanduser().resolve()
    return config, runtime, Path(config.get('trellis_manifest', runtime / 'trellis-engine.json')).expanduser().resolve()


def source_files(source, dino):
    roots = [source / 'trellis', source / 'scripts', dino]
    paths = {path for root in roots for path in root.rglob('*')
             if path.is_file() and path.suffix in SOURCE_EXTENSIONS and '.git' not in path.parts}
    return sorted(paths)


def file_record(path):
    return {'bytes': path.stat().st_size, 'sha256': digest(path)}


def configure(runtime, manifest_path, replace=False):
    """Explicitly trust/pin an already reviewed runtime; never install anything."""
    if os.path.lexists(manifest_path) and not replace:
        raise ValueError('Manifest already exists; review changes before explicit --replace-manifest.')
    source = runtime / 'trellis-v1'
    dino = runtime / 'torch/hub/facebookresearch_dinov2_main'
    for checkout, expected in [(source, SOURCE_COMMIT), (dino, DINO_COMMIT)]:
        actual = subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip()
        if actual != expected:
            raise ValueError('Unexpected source revision: ' + str(checkout))
    public = json.loads((source / 'public_weights.json').read_text())
    if public['trellis_revision'] != MODEL_REVISION:
        raise ValueError('Unexpected public model revision.')
    snapshot = Path(public['trellis_snapshot'])
    expected_snapshot = runtime / 'hf/hub/models--microsoft--TRELLIS-image-large/snapshots' / MODEL_REVISION
    if snapshot != expected_snapshot or not snapshot.is_dir():
        raise ValueError('Pinned local TRELLIS snapshot is missing or points elsewhere.')
    checkpoint = runtime / 'torch/hub/checkpoints/dinov2_vitl14_reg4_pretrain.pth'
    if not checkpoint.is_file():
        raise ValueError('Public DINOv2 checkpoint missing; setup must finish before offline configuration.')
    assets = {str(path): file_record(path) for path in sorted(snapshot.rglob('*'))
              if path.is_file() and path.suffix in {'.json', '.safetensors'}}
    for relative, expected in public['verified_trellis_weights'].items():
        if assets.get(str(snapshot / relative)) != expected:
            raise ValueError('Previously verified model asset changed: ' + relative)
    if str(snapshot / 'pipeline.json') not in assets:
        raise ValueError('Local pipeline configuration missing.')
    assets[str(checkpoint)] = file_record(checkpoint)
    python = source / '.venv/bin/python'
    if not python.is_file() or not os.access(python, os.X_OK):
        raise ValueError('Local runtime interpreter missing.')
    files = source_files(source, dino)
    if source / 'scripts/run_real_pipeline.py' not in files or not files:
        raise ValueError('Local generation source missing.')
    environment_files = list((source / '.venv').glob('lib/python*/site-packages/*.pth'))
    environment_files += [source / '.venv/pyvenv.cfg']
    manifest = {'schema_version': 1, 'source': str(source), 'dino_source': str(dino),
                'source_commit': SOURCE_COMMIT, 'dino_commit': DINO_COMMIT,
                'snapshot': str(snapshot), 'model_revision': MODEL_REVISION,
                'python': str(python), 'torch_home': str(runtime / 'torch'),
                'sources': {str(path): file_record(path) for path in files},
                'environment_pointers': {str(path): file_record(path) for path in environment_files if path.is_file()},
                'assets': assets, 'configured_at_unix': time.time(),
                'scope': 'Pins runtime source, cached model files and environment pointers; third-party package contents are not fully pinned.',
                'portrait_quality_accepted': False, 'ready_to_print': False}
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(manifest_path, manifest)
    return manifest


def verify_manifest(path, verify_assets=True):
    if not path.is_file():
        raise ValueError('TRELLIS is not configured. Finish/review the existing local setup, then run configure explicitly.')
    manifest = json.loads(path.read_text())
    if (manifest.get('schema_version'), manifest.get('source_commit'), manifest.get('dino_commit'), manifest.get('model_revision')) != (1, SOURCE_COMMIT, DINO_COMMIT, MODEL_REVISION):
        raise ValueError('Unrecognized TRELLIS manifest/revisions.')
    actual_sources = {str(p) for p in source_files(Path(manifest['source']), Path(manifest['dino_source']))}
    if (actual_sources != set(manifest['sources'])
            or str(Path(manifest['source']) / 'scripts/run_real_pipeline.py') not in actual_sources
            or str(Path(manifest['dino_source']) / 'hubconf.py') not in actual_sources):
        raise ValueError('Runtime source file set changed; review before reconfiguration.')
    snapshot = Path(manifest['snapshot'])
    checkpoint = Path(manifest['torch_home']) / 'hub/checkpoints/dinov2_vitl14_reg4_pretrain.pth'
    actual_assets = {str(p) for p in snapshot.rglob('*') if p.is_file() and p.suffix in {'.json', '.safetensors'}} | {str(checkpoint)}
    if (actual_assets != set(manifest['assets']) or str(snapshot / 'pipeline.json') not in actual_assets
            or not any(p.endswith('.safetensors') for p in actual_assets)):
        raise ValueError('Cached model file set changed; offline generation will not download replacements.')
    if not Path(manifest['python']).is_file() or not os.access(manifest['python'], os.X_OK):
        raise ValueError('Runtime interpreter missing.')
    for group in ['sources', 'environment_pointers', 'assets']:
        for filename, expected in manifest[group].items():
            file = Path(filename)
            if not file.is_file() or file.stat().st_size != expected['bytes']:
                raise ValueError('Pinned local file missing or changed: ' + filename)
            if group != 'assets' or verify_assets or file.suffix not in {'.safetensors', '.pth'}:
                if digest(file) != expected['sha256']:
                    raise ValueError('Pinned local file checksum changed: ' + filename)
    return manifest


def offline_environment(runtime, manifest, inherited=None):
    environment = dict(os.environ if inherited is None else inherited)
    environment.update(HF_HOME=str(runtime / 'hf'), HF_HUB_CACHE=str(runtime / 'hf/hub'),
                       HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1', HF_HUB_DISABLE_IMPLICIT_TOKEN='1',
                       HF_HUB_DISABLE_TELEMETRY='1', DO_NOT_TRACK='1',
                       TORCH_HOME=manifest['torch_home'], TRELLIS_MODEL_PATH=manifest['snapshot'],
                       TRELLIS_DINOV2_SOURCE=manifest['dino_source'], PYTORCH_ENABLE_MPS_FALLBACK='1',
                       TRELLIS_LOW_MEMORY='1', TRELLIS_CONV_CHUNK='32768')
    for key in ['PYTORCH_MPS_HIGH_WATERMARK_RATIO', 'PYTORCH_MPS_LOW_WATERMARK_RATIO',
                'TRELLIS_LATENT_CHECKPOINT', 'PYTHONPATH', 'PYTHONHOME']:
        environment.pop(key, None)
    return environment


def validate_paths(images, output):
    requested = Path(output).expanduser().absolute()
    if os.path.lexists(requested):
        raise ValueError('Output path must not exist, including empty directories and symlinks.')
    output = requested.resolve()
    sources = [Path(image).expanduser().resolve() for image in images]
    if not sources or any(not p.is_file() for p in sources):
        raise ValueError('Every input must be an existing local photo.')
    if any(p == output or output in p.parents or p in output.parents for p in sources):
        raise ValueError('Input/output paths must not overlap.')
    if len(set(sources)) != len(sources) or len({digest(p) for p in sources}) != len(sources):
        raise ValueError('Duplicate photos do not supply additional views.')
    return sources, output


def prepare_images(sources, output, vision):
    from PIL import Image, ImageOps
    folder = output / 'inputs'
    folder.mkdir()
    prepared, records = [], []
    for index, original in enumerate(sources, 1):
        original_hash = digest(original)
        saved = folder / f'original-{index:02d}{original.suffix.lower()}'
        shutil.copy2(original, saved)
        if digest(saved) != original_hash:
            raise ValueError('Input changed during preservation: ' + str(original))
        target = folder / f'input-{index:02d}.png'
        with Image.open(saved) as source:
            if source.width * source.height > 40_000_000:
                raise ValueError('Photo exceeds 40 megapixels; prepare a suitable local reference first.')
            image = ImageOps.exif_transpose(source).convert('RGBA')
        minimum, maximum = image.getextrema()[3]
        method = 'provided_alpha'
        if minimum == 255:
            if not vision.is_file() or not os.access(vision, os.X_OK):
                raise ValueError('Opaque input requires the configured native Apple Vision executable.')
            report = folder / f'vision-{index:02d}.json'
            result = subprocess.run([str(vision), '--input', str(saved), '--output', str(target),
                                     '--report', str(report), '--mode', 'foreground'], capture_output=True, text=True, timeout=120)
            if result.returncode:
                raise ValueError('Native extraction failed: ' + (result.stdout or result.stderr).strip()[:800])
            method = 'Apple Vision foreground'
        else:
            image.save(target)
        with Image.open(target) as checked:
            if checked.mode != 'RGBA' or checked.size != image.size:
                raise ValueError('Extraction did not preserve the oriented full RGBA frame.')
            alpha = checked.getextrema()[3]
        if alpha[0] == 255 or alpha[1] < 205:
            raise ValueError('Background-free nonempty alpha image required: ' + str(original))
        prepared.append(target)
        records.append({'source': str(original), 'sha256': original_hash, 'preserved': str(saved),
                        'prepared': str(target), 'preparation': method, 'full_frame_preserved': True,
                        'mask_review_required': True})
    return prepared, records


def generation_command(manifest, images, output, seed=1, steps=25):
    command = [manifest['python'], '-u', str(SKILL_ROOT / 'scripts/u1_offline_exec.py'), '--',
               str(Path(manifest['source']) / 'scripts/run_real_pipeline.py'),
               str(images[0]), 'model']
    for image in images[1:]:
        command += ['--additional-image', str(image)]
    return command + ['--require-alpha', '--multi-image-mode', 'stochastic', '--sampling-steps', str(steps),
                      '--out-dir', str(output), '--device', 'mps', '--seed', str(seed), '--skip-previews',
                      '--simplify', '0.75', '--texture-size', '1024', '--multiview-resolution', '512',
                      '--multiview-nviews', '40', '--fill-holes-resolution', '512']


def generate(args, config, runtime, manifest_path):
    sources, output = validate_paths(args.images, args.output_dir)
    manifest = verify_manifest(manifest_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()  # reserve once; a concurrent creator must not be overwritten
    started = time.monotonic()
    job = {'status': 'preprocessing', 'engine': 'TRELLIS local MPS', 'input_views': len(sources),
           'network_mode': 'offline', 'external_upload_performed': False,
           'runtime_python_ip_network_guard': True,
           'network_guard_scope': 'Runtime Python socket/DNS APIs; AF_UNIX IPC allowed. Native code and independent subprocess networking are not an OS-wide air gap.',
           'unseen_surfaces': 'inferred', 'likeness_accepted': False, 'ready_to_print': False,
           'geometry_validated': False, 'slicing_verified': False,
           'manifest_sha256': digest(manifest_path)}
    try:
        write_json(output / 'job.json', job)
        images, records = prepare_images(sources, output, Path(config.get('apple_vision_binary', runtime / 'apple/u1_vision')))
        command = generation_command(manifest, images, output, args.seed, args.steps)
        write_json(output / 'command.json', command)
        job.update(status='generating', inputs=records)
        write_json(output / 'job.json', job)
        print('Local progress log: ' + str(output / 'run.log'), flush=True)
        with (output / 'run.log').open('w') as log:
            completed = subprocess.run(command, cwd=manifest['source'], env=offline_environment(runtime, manifest),
                                       stdout=log, stderr=subprocess.STDOUT)
        if completed.returncode or not (output / 'model.glb').is_file():
            raise RuntimeError(f'Local generation failed (exit {completed.returncode}); inspect run.log. Earlier raw/latent outputs are preserved.')
        job.update(status='candidate_pending_visual_review', master=str(output / 'model.glb'),
                   raw_geometry=str(output / 'model_raw.glb'), color_representation='generated UV texture; not calibrated filament colors')
        job.update(master_up_axis='y', raw_geometry_up_axis='z', subject_front_axis='not inferred')
    except Exception as error:
        job.update(status='failed', error=f'{type(error).__name__}: {error}')
        raise
    except KeyboardInterrupt:
        job.update(status='interrupted', error='Interrupted by user; earlier outputs preserved.')
        raise
    finally:
        job['elapsed_seconds'] = round(time.monotonic() - started, 2)
        write_json(output / 'job.json', job)
    return job


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=SKILL_ROOT / 'local-runtime.json')
    commands = parser.add_subparsers(dest='command', required=True)
    setup = commands.add_parser('configure', help='Pin an existing reviewed local installation; no downloads')
    setup.add_argument('--replace-manifest', action='store_true')
    doctor = commands.add_parser('doctor')
    doctor.add_argument('--verify-assets', action='store_true', help='Hash large model weights as well as source/configuration')
    run = commands.add_parser('generate')
    run.add_argument('images', nargs='+', type=Path)
    run.add_argument('--output-dir', required=True, type=Path)
    run.add_argument('--seed', type=int, default=1)
    run.add_argument('--steps', type=int, default=25)
    args = parser.parse_args(argv)
    if args.command == 'generate' and not 1 <= args.steps <= 100:
        parser.error('steps must be between 1 and 100')
    try:
        config, runtime, path = settings(args.config)
        if args.command == 'configure':
            configure(runtime, path, args.replace_manifest)
            result = {'status': 'configured_existing_assets', 'manifest': str(path), 'downloads_performed': False,
                      'likeness_accepted': False, 'ready_to_print': False}
        elif args.command == 'doctor':
            manifest = verify_manifest(path, args.verify_assets)
            result = {'status': 'configured', 'manifest': str(path), 'source': manifest['source'],
                      'source_integrity_verified': True, 'model_weight_checksums_verified': args.verify_assets,
                      'gpu_availability_tested': False, 'network_mode': 'offline', 'ready_to_print': False,
                      'limitations': ['Experimental general-object model; no accepted portrait likeness or commercial-service parity.',
                                      'One-shot process; mesh and Gaussian only; installed dependencies are shared.',
                                      'Prior successful trial reported 30.99 GB peak footprint on this 24 GB Mac.']}
        else:
            result = generate(args, config, runtime, path)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
