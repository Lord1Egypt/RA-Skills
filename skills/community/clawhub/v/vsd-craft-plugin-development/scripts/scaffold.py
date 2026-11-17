#!/usr/bin/env python3
"""Create a new, isolated VSD Craft counter plugin. Never installs or overwrites."""
import argparse
import json
from pathlib import Path
import re
import shutil
import struct
import zlib

SKILL_ROOT = Path(__file__).resolve().parents[1]


def png(size):
    """Original solid-color placeholder; no third-party artwork."""
    def chunk(kind, data):
        return struct.pack('!I', len(data)) + kind + data + struct.pack('!I', zlib.crc32(kind + data) & 0xffffffff)
    pixels = b''.join(b'\0' + bytes([25, 54, 87]) * size for _ in range(size))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('!2I5B', size, size, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(pixels)) + chunk(b'IEND', b''))


def scaffold(plugin_id, name, output):
    if not re.fullmatch(r'[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?(?:\.[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?){2,}', plugin_id):
        raise ValueError('id must be a lowercase reverse-DNS ID with at least three components')
    if not name.strip() or len(name) > 100:
        raise ValueError('name must contain 1-100 characters')
    output = Path(output).absolute()
    if output.name != plugin_id + '.sdPlugin':
        raise ValueError('output folder must be <id>.sdPlugin')
    if output.exists() or output.is_symlink():
        raise FileExistsError(f'Refusing to overwrite {output}')
    manifest = {
        'UUID': plugin_id, 'Name': name, 'Author': 'Plugin author',
        'Description': 'Local counter demonstration for VSD Craft / StreamDock',
        'Version': '0.1.0', 'SDKVersion': 1,
        'CodePath': 'plugin.js', 'CodePathWin': 'plugin.js',
        'Nodejs': {'Version': '20'},
        'OS': [{'Platform': 'windows', 'MinimumVersion': '10'}],
        'Software': {'MinimumVersion': '3.10.188.226'},
        'Icon': 'images/plugin.png', 'Category': name, 'CategoryIcon': 'images/category.png',
        'Actions': [],
    }
    for suffix, controller, title in [('key', 'Keypad', 'Counter: Key'), ('dial', 'Knob', 'Counter: Knob')]:
        manifest['Actions'].append({
            'UUID': plugin_id + '.' + suffix, 'Name': title, 'Icon': 'images/action.png',
            'Controllers': [controller], 'UserTitleEnabled': True, 'SupportedInMultiActions': False,
            'Settings': {'step': 1}, 'PropertyInspectorPath': 'ui/index.html',
            'States': [{'Image': 'images/key.png', 'Title': ''}],
        })
    package = {
        'name': plugin_id.replace('.', '-'), 'version': '0.1.0', 'private': True,
        'description': 'VSD Craft counter scaffold', 'type': 'commonjs',
        'engines': {'node': '>=20'}, 'scripts': {'test': 'node --test test/smoke.cjs'},
        'dependencies': {'ws': '^8.22.0'},
    }
    output.mkdir(parents=True, exist_ok=False)
    for relative in ['plugin.js', 'ui/index.html', 'ui/inspector.js', 'test/smoke.cjs']:
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SKILL_ROOT / 'assets' / 'template' / relative, target)
    for filename, data in [('manifest.json', manifest), ('package.json', package)]:
        (output / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    images = output / 'images'
    images.mkdir()
    for filename, size in [('plugin.png', 128), ('category.png', 48), ('action.png', 40), ('key.png', 144)]:
        (images / filename).write_bytes(png(size))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        output = scaffold(args.id, args.name, args.output)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Scaffold failed: {error}\n')
    print(json.dumps({'created': str(output), 'installed': False, 'next': ['npm install --ignore-scripts --omit=optional --no-audit --no-fund', 'npm test']}, indent=2))


if __name__ == '__main__':
    main()
