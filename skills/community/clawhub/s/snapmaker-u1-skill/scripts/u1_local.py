#!/usr/bin/env python3
"""Account-free TripoSR setup, machine check, segmentation and real 3D inference.

Only `setup` uses the network, to download public code and model weights.
`generate` forces Hugging Face offline and runs the supplied image locally.
This experimental general-object model is NOT a portrait-likeness guarantee.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

SOURCE_URL = 'https://github.com/VAST-AI-Research/TripoSR.git'
SOURCE_COMMIT = '107cefdc244c39106fa830359024f6a2f1c78871'
SKILL_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_POINTER = SKILL_ROOT / 'local-runtime.json'
DEFAULT_RUNTIME = (Path(json.loads(RUNTIME_POINTER.read_text())['runtime_dir'])
                   if RUNTIME_POINTER.is_file() else SKILL_ROOT / '.runtime')
PATCH_FROM = 'from torchmcubes import marching_cubes'
PATCH_TO = 'from u1_mcubes import marching_cubes'


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def atomic_json(path, data):
    path = Path(path)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(data, indent=2) + '\n')
    temp.replace(path)


def paths(runtime):
    runtime = Path(runtime).expanduser().resolve()
    return runtime, runtime / 'TripoSR', runtime / 'engine.json'


def configure_environment(runtime, offline):
    # Project-local caches prevent unrelated application/config changes.
    os.environ['HF_HOME'] = str(runtime / 'hf')
    os.environ['HF_HUB_CACHE'] = str(runtime / 'hf' / 'hub')
    os.environ['TRANSFORMERS_CACHE'] = str(runtime / 'hf' / 'transformers')
    os.environ['U2NET_HOME'] = str(runtime / 'segmentation')
    os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'
    os.environ['DO_NOT_TRACK'] = '1'
    os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
    if offline:
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['TRANSFORMERS_OFFLINE'] = '1'
    else:
        os.environ.pop('HF_HUB_OFFLINE', None)
        os.environ.pop('TRANSFORMERS_OFFLINE', None)


def doctor(runtime):
    runtime, source, manifest = paths(runtime)
    disk_path = runtime
    while not disk_path.exists():
        disk_path = disk_path.parent
    disk = shutil.disk_usage(disk_path)
    result = {
        'platform': platform.system(), 'architecture': platform.machine(),
        'python': sys.version.split()[0], 'free_disk_gib': round(disk.free / 2**30, 2),
        'runtime': str(runtime), 'engine_manifest_present': manifest.is_file(),
        'dependencies': {name: importlib.util.find_spec(name) is not None for name in
                         ['torch', 'transformers', 'rembg', 'onnxruntime', 'skimage', 'trimesh', 'PIL']},
        'native_apple_helpers': {name: (runtime/'apple'/name).is_file() for name in ['u1_vision','u1_apple_plan']},
        'network_image_upload': False,
        'limitations': ['TripoSR is a general-object, single-view baseline, not commercial-model parity.',
                        'Hidden geometry is inferred; human likeness needs visual acceptance.',
                        'Vertex RGB is not calibrated U1 Full Spectrum toolpaths.'],
    }
    if result['dependencies']['torch']:
        import torch
        result['devices'] = {'cpu': True, 'mps': torch.backends.mps.is_available(), 'cuda': torch.cuda.is_available()}
    print(json.dumps(result, indent=2))
    return 0


def setup(runtime):
    runtime, source, manifest_path = paths(runtime)
    runtime.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(runtime).free < 4 * 2**30:
        raise ValueError('Setup needs at least 4 GiB free for weights and working space; free space or choose another runtime directory.')
    configure_environment(runtime, offline=False)
    import truststore
    truststore.inject_into_ssl()
    from huggingface_hub import HfApi, hf_hub_download
    if not source.exists():
        subprocess.run(['git', 'init', str(source)], check=True, stdout=subprocess.DEVNULL)
        subprocess.run(['git', '-C', str(source), 'remote', 'add', 'origin', SOURCE_URL], check=True)
        subprocess.run(['git', '-C', str(source), 'fetch', '--depth', '1', 'origin', SOURCE_COMMIT], check=True)
        subprocess.run(['git', '-C', str(source), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
    current = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    if current != SOURCE_COMMIT:
        raise ValueError('Runtime checkout differs from the reviewed revision; choose a fresh runtime directory.')
    iso = source / 'tsr/models/isosurface.py'
    pristine = subprocess.check_output(['git', '-C', str(source), 'show', 'HEAD:tsr/models/isosurface.py'], text=True)
    expected = pristine.replace(PATCH_FROM, PATCH_TO)
    if pristine == expected or iso.read_text() not in [pristine, expected]:
        raise ValueError('Unexpected isosurface source; refusing to overwrite changes.')
    iso.write_text(expected)
    old = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    api = HfApi(token=False)
    model_rev = old.get('model_revision') or api.model_info('stabilityai/TripoSR').sha
    dino_rev = old.get('dino_revision') or api.model_info('facebook/dino-vitb16').sha
    downloaded = {}
    for filename in ['config.yaml', 'model.ckpt']:
        print('Downloading public model asset:', filename, flush=True)
        downloaded[filename] = hf_hub_download('stabilityai/TripoSR', filename, revision=model_rev, token=False)
    dino = hf_hub_download('facebook/dino-vitb16', 'config.json', revision=dino_rev, token=False)
    # Cache the unversioned DINO ref too: the pinned upstream tokenizer requests main.
    # Store a local config path in the model config instead to keep inference offline.
    from omegaconf import OmegaConf
    local_weights = runtime / 'weights'
    local_weights.mkdir(exist_ok=True)
    for name in ['model.ckpt']:
        target = local_weights / name
        if not target.exists():
            target.symlink_to(Path(downloaded[name]).resolve())
    cfg = OmegaConf.load(downloaded['config.yaml'])
    # Upstream tokenizer calls hf_hub_download. A narrow local-only patch uses its
    # existing config path, not network downloads during image processing.
    tokenizer = source / 'tsr/models/tokenizers/image.py'
    raw = subprocess.check_output(['git', '-C', str(source), 'show', 'HEAD:tsr/models/tokenizers/image.py'], text=True)
    old_call = '''hf_hub_download(
                    repo_id=self.cfg.pretrained_model_name_or_path,
                    filename="config.json",
                )'''
    new_call = 'self.cfg.pretrained_model_name_or_path'
    patched = raw.replace(old_call, new_call)
    if patched == raw or tokenizer.read_text() not in [raw, patched]:
        raise ValueError('Unexpected tokenizer source; refusing to overwrite changes.')
    tokenizer.write_text(patched)
    cfg.image_tokenizer.pretrained_model_name_or_path = str(Path(dino).resolve())
    OmegaConf.save(cfg, local_weights / 'config.yaml')
    import rembg
    import onnxruntime as ort
    ort.disable_telemetry_events()
    print('Downloading public human segmentation weights if missing...', flush=True)
    rembg.new_session('u2net_human_seg', providers=['CPUExecutionProvider'])
    segmentation = runtime / 'segmentation' / 'u2net_human_seg.onnx'
    if not segmentation.is_file():
        raise ValueError('Segmentation weights were not downloaded to the local runtime.')
    manifest = {
        'engine': 'TripoSR', 'source_url': SOURCE_URL, 'source_commit': SOURCE_COMMIT,
        'source_license': 'MIT (see TripoSR/LICENSE)',
        'model_repository': 'stabilityai/TripoSR', 'model_revision': model_rev,
        'dino_revision': dino_rev, 'dino_config_path': str(Path(dino).resolve()),
        'dino_config_sha256': sha256(dino), 'weights': str(local_weights),
        'checkpoint_sha256': sha256(local_weights / 'model.ckpt'),
        'config_sha256': sha256(local_weights / 'config.yaml'),
        'source_patches': {str(p.relative_to(source)): sha256(p) for p in [iso, tokenizer]},
        'segmentation_sha256': sha256(segmentation),
        'patches': ['CPU scikit-image marching cubes adapter', 'local pinned DINO config instead of runtime network lookup'],
        'private_image_upload': False, 'setup_complete': True,
    }
    atomic_json(manifest_path, manifest)
    print('Local engine setup complete:', manifest_path, flush=True)
    return 0


def verify_runtime(runtime, require_segmentation_model=True):
    runtime, source, manifest_path = paths(runtime)
    if not manifest_path.is_file():
        raise ValueError('Engine is not set up. Install requirements-local.txt and run u1_local.py setup first.')
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('source_commit') != SOURCE_COMMIT or not manifest.get('setup_complete'):
        raise ValueError('Engine manifest is incomplete or from another revision.')
    for rel, digest in manifest['source_patches'].items():
        if sha256(source / rel) != digest:
            raise ValueError(f'Runtime source changed after setup: {rel}')
    weights = Path(manifest['weights'])
    if not weights.is_dir() or not (weights/'model.ckpt').is_file():
        raise ValueError('Model files missing; rerun setup.')
    if sha256(weights / 'model.ckpt') != manifest['checkpoint_sha256']:
        raise ValueError('Model checkpoint changed after setup.')
    if sha256(weights / 'config.yaml') != manifest['config_sha256']:
        raise ValueError('Model config changed after setup.')
    dino_config = Path(manifest.get('dino_config_path', ''))
    if not dino_config.is_file() or sha256(dino_config) != manifest.get('dino_config_sha256'):
        raise ValueError('Pinned DINO config missing or changed; run setup explicitly.')
    segmentation = runtime / 'segmentation' / 'u2net_human_seg.onnx'
    if require_segmentation_model and (not segmentation.is_file() or sha256(segmentation) != manifest['segmentation_sha256']):
        raise ValueError('Segmentation weights missing or changed; run setup explicitly. Offline generation will not download replacements.')
    return source, manifest


def select_segmentation_backend(requested, native_binary):
    if requested == 'auto':
        return 'vision' if sys.platform == 'darwin' and Path(native_binary).is_file() else 'human'
    if requested not in ['vision', 'human', 'alpha']:
        raise ValueError('Unknown segmentation backend')
    return requested


def prepare_image(image_path, output, foreground_ratio, segmentation, native_binary=None):
    import numpy as np
    from PIL import Image, ImageOps
    original = ImageOps.exif_transpose(Image.open(image_path)).convert('RGBA')
    if original.width * original.height > 40_000_000:
        raise ValueError('Image exceeds the 40 megapixel limit; resize it before reconstruction.')
    native_binary = Path(native_binary) if native_binary else DEFAULT_RUNTIME / 'apple' / 'u1_vision'
    segmentation = select_segmentation_backend(segmentation, native_binary)
    actual_backend = 'provided_alpha'
    native_report = None
    if original.getextrema()[3][0] == 255:
        if segmentation == 'alpha':
            raise ValueError('--segmentation alpha requires an RGBA image with a supplied transparent background.')
        actual_backend = segmentation
        if segmentation == 'vision':
            if not native_binary.is_file():
                raise ValueError('Apple Vision helper is not built; compile scripts/u1_vision.swift first.')
            native_output = output / 'vision_subject.png'
            native_json = output / 'vision_report.json'
            completed = subprocess.run([str(native_binary), '--input', str(Path(image_path).resolve()),
                                        '--output', str(native_output.resolve()), '--report', str(native_json.resolve())],
                                       capture_output=True, text=True, timeout=120, check=False)
            if completed.returncode != 0:
                raise ValueError('Apple Vision extraction failed: ' + (completed.stdout or completed.stderr).strip()[:800])
            native_report = json.loads(native_json.read_text())
            cutout = Image.open(native_output).convert('RGBA')
        else:
            import rembg
            import onnxruntime as ort
            ort.disable_telemetry_events()
            session = rembg.new_session('u2net_human_seg', providers=['CPUExecutionProvider'])
            cutout = rembg.remove(original, session=session)
    else:
        cutout = original
    cutout.save(output/'subject_rgba.png')
    alpha = np.asarray(cutout.getchannel('A'))
    foreground = alpha > 127
    if not foreground.any():
        raise ValueError('Segmentation found no subject; inspect the photo or provide an alpha-masked PNG.')
    yy, xx = np.where(foreground)
    crop = cutout.crop((int(xx.min()), int(yy.min()), int(xx.max())+1, int(yy.max())+1))
    side = int(np.ceil(max(crop.size) / foreground_ratio))
    square = Image.new('RGBA', (side, side), (128,128,128,0))
    square.alpha_composite(crop, ((side-crop.width)//2, (side-crop.height)//2))
    rgb = Image.new('RGBA',square.size,(128,128,128,255))
    rgb.alpha_composite(square)
    rgb = rgb.convert('RGB').resize((512,512),Image.Resampling.LANCZOS)
    rgb.save(output/'model_input.png')
    return rgb, {'input_size': list(original.size), 'foreground_fraction': float(foreground.mean()),
                 'mask_review_required': True, 'background_method': actual_backend,
                 'native_vision_report': native_report,
                 'input_sha256': sha256(image_path)}


def generate(args):
    runtime, source, manifest_path = paths(args.runtime_dir)
    configure_environment(runtime, offline=True)
    native_binary = runtime / 'apple' / 'u1_vision'
    backend = select_segmentation_backend(args.segmentation, native_binary)
    source, manifest = verify_runtime(runtime, require_segmentation_model=backend == 'human')
    sys.path.insert(0,str(source))
    import torch
    from tsr.system import TSR
    output = Path(args.output_dir).expanduser().resolve()
    output.mkdir(parents=True,exist_ok=True)
    if any(output.iterdir()):
        raise ValueError('Output directory must be empty. Choose a new directory to preserve the source and earlier candidates.')
    if not Path(args.image).is_file():
        raise ValueError('Input image does not exist.')
    device = args.device
    if device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else ('mps' if torch.backends.mps.is_available() else 'cpu')
    if device == 'mps' and not torch.backends.mps.is_available():
        raise ValueError('MPS is unavailable; select --device cpu explicitly.')
    if device == 'cuda' and not torch.cuda.is_available():
        raise ValueError('CUDA is unavailable; select --device cpu or mps.')
    torch.set_num_threads(args.cpu_threads)
    started = time.monotonic()
    job = {'status':'running','engine':'TripoSR','source_commit':SOURCE_COMMIT,
           'model_revision':manifest['model_revision'],'device':device,
           'network_mode':'offline','private_image_uploaded':False,
           'input_views':1,'unseen_surfaces':'inferred','portrait_likeness':'not_validated',
           'print_readiness':'not_sliced','resolution':args.resolution,
           'color_representation':'generated vertex RGB, not UV texture or calibrated filament colors'}
    atomic_json(output/'job.json',job)
    try:
        print('Segmenting subject locally...',flush=True)
        image, info = prepare_image(args.image,output,args.foreground_ratio,backend,native_binary=native_binary)
        job['image_preparation']=info
        atomic_json(output/'job.json',job)
        print(f'Loading pinned TripoSR weights on {device}...',flush=True)
        model = TSR.from_pretrained(manifest['weights'],config_name='config.yaml',weight_name='model.ckpt')
        model.eval().to(device)
        model.renderer.set_chunk_size(args.chunk_size)
        print('Running trained 3D inference (not a traced relief)...',flush=True)
        with torch.inference_mode():
            scene_codes = model([image],device=device)
            print('Extracting a 3D isosurface and vertex colors...',flush=True)
            mesh = model.extract_mesh(scene_codes,has_vertex_color=True,resolution=args.resolution)[0]
        if not len(mesh.faces):
            raise ValueError('The reconstruction produced no triangles.')
        # Correct orientation only; no smoothing or likeness-changing repair.
        corrected = False
        if mesh.is_watertight and mesh.volume < 0:
            mesh.invert();corrected=True
        mesh.export(output/'master.glb')
        mesh.export(output/'master.ply')
        mesh.export(output/'geometry_normalized.stl')
        job.update(status='candidate_generated',elapsed_seconds=round(time.monotonic()-started,2),
                   vertices=len(mesh.vertices),faces=len(mesh.faces),
                   winding_inverted=corrected,watertight=bool(mesh.is_watertight),
                   model_units='normalized; run u1_prepare.py with target height before slicing',
                   visual_review_required=True,
                   next_steps=['Inspect subject mask and actual 360-degree mesh views.',
                               'Reject poor facial geometry even if watertight.',
                               'Scale and prepare accepted mesh, convert target colors, calibrate Full Spectrum and slice.'])
        atomic_json(output/'job.json',job)
        print(json.dumps(job,indent=2),flush=True)
        return 0
    except Exception as exc:
        job.update(status='failed',error=f'{type(exc).__name__}: {exc}',elapsed_seconds=round(time.monotonic()-started,2))
        atomic_json(output/'job.json',job)
        raise


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime-dir',type=Path,default=DEFAULT_RUNTIME)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('doctor');sub.add_parser('setup')
    gen=sub.add_parser('generate')
    gen.add_argument('image',type=Path);gen.add_argument('--output-dir',required=True)
    gen.add_argument('--device',choices=['auto','cpu','mps','cuda'],default='auto')
    gen.add_argument('--resolution',type=int,choices=[64,96,128,192,256],default=192)
    gen.add_argument('--chunk-size',type=int,default=32768)
    gen.add_argument('--cpu-threads',type=int,default=6)
    gen.add_argument('--foreground-ratio',type=float,default=.85)
    gen.add_argument('--segmentation',choices=['auto','vision','human','alpha'],default='auto')
    args=parser.parse_args()
    if args.command=='generate' and (not .2<=args.foreground_ratio<=.95 or args.chunk_size<1 or args.cpu_threads<1):
        parser.error('foreground ratio must be 0.2–0.95; chunk size and threads must be positive')
    try:
        return doctor(args.runtime_dir) if args.command=='doctor' else setup(args.runtime_dir) if args.command=='setup' else generate(args)
    except (ValueError,ImportError,OSError,RuntimeError,subprocess.CalledProcessError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr);return 2

if __name__=='__main__':
    raise SystemExit(main())
