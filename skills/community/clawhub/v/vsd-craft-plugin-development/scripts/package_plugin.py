#!/usr/bin/env python3
"""Package only the counter scaffold's reviewed files, not arbitrary plugin trees."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile


def checked_file(root, relative):
    relative = PurePosixPath(relative)
    if relative.is_absolute() or '..' in relative.parts or '\\' in str(relative):
        raise ValueError(f'Invalid relative path: {relative}')
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'Symlink is not allowed: {relative}')
    if not current.is_file():
        raise ValueError(f'Missing file: {relative}')
    return current


def package_files(root):
    root = Path(root).resolve(strict=True)
    manifest = json.loads(checked_file(root, 'manifest.json').read_text(encoding='utf-8'))
    package = json.loads(checked_file(root, 'package.json').read_text(encoding='utf-8'))
    if root.name != manifest.get('UUID', '') + '.sdPlugin':
        raise ValueError('Folder name and manifest UUID do not match')
    if manifest.get('CodePath') != 'plugin.js' or manifest.get('CodePathWin') != 'plugin.js':
        raise ValueError('This packager only supports the supplied counter scaffold')
    if set(package.get('dependencies', {})) != {'ws'}:
        raise ValueError('Review the packager allowlist before adding dependencies')
    if any(package.get(key) for key in ['devDependencies', 'optionalDependencies', 'peerDependencies']):
        raise ValueError('Extra dependency sections require a reviewed packaging plan')
    files = {
        'manifest.json', 'package.json', 'package-lock.json', 'plugin.js',
        'ui/index.html', 'ui/inspector.js',
        'images/plugin.png', 'images/category.png', 'images/action.png', 'images/key.png',
        'node_modules/ws/package.json', 'node_modules/ws/LICENSE',
        'node_modules/ws/index.js', 'node_modules/ws/browser.js', 'node_modules/ws/wrapper.mjs',
    }
    library = root / 'node_modules' / 'ws' / 'lib'
    if library.is_symlink():
        raise ValueError('Symlink is not allowed: ws/lib')
    files.update(p.relative_to(root).as_posix() for p in library.glob('*.js'))
    references = [manifest['Icon'], manifest['CategoryIcon']]
    for action in manifest['Actions']:
        references.extend([action['Icon'], action['PropertyInspectorPath']])
        references.extend(state['Image'] for state in action['States'])
    for relative in references:
        if relative not in files:
            raise ValueError(f'Manifest resource outside scaffold allowlist: {relative}')
    for relative in files:
        checked_file(root, relative)
    if not list(library.glob('*.js')):
        raise ValueError('ws runtime library is missing')
    lock = json.loads((root / 'package-lock.json').read_text(encoding='utf-8'))
    ws_package = json.loads((root / 'node_modules/ws/package.json').read_text(encoding='utf-8'))
    locked = lock.get('packages', {}).get('node_modules/ws', {}).get('version')
    if not locked or locked != ws_package.get('version'):
        raise ValueError('Installed ws version does not match package-lock.json')
    return root, sorted(files)


def package_plugin(root, output):
    root, files = package_files(root)
    output = Path(output).absolute()
    if output.exists() or output.is_symlink():
        raise FileExistsError(f'Refusing to overwrite {output}')
    if output.suffix.lower() != '.zip':
        raise ValueError('Output must be a .zip archive')
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in files:
            archive.write(checked_file(root, relative), (PurePosixPath(root.name) / relative).as_posix())
    return {'archive': str(output), 'files': files, 'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plugin')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        result = package_plugin(args.plugin, args.output)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f'Packaging failed: {error}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
