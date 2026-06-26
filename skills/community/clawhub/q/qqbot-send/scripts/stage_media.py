import shutil
import sys
import uuid
from pathlib import Path

MAX_SIZE = 10 * 1024 * 1024
DEST_DIR = Path.home() / '.openclaw' / 'media' / 'qqbot'


def main() -> int:
    if len(sys.argv) != 2:
        print('usage: python stage_media.py <source_path>', file=sys.stderr)
        return 2

    src = Path(sys.argv[1]).expanduser()
    if not src.is_absolute():
        src = src.resolve()

    if not src.exists() or not src.is_file():
        print(f'ERROR: file not found: {src}', file=sys.stderr)
        return 1

    size = src.stat().st_size
    if size > MAX_SIZE:
        print(f'ERROR: file too large: {size} bytes > {MAX_SIZE} bytes', file=sys.stderr)
        return 1

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    ext = src.suffix
    dest = DEST_DIR / f'{uuid.uuid4()}{ext}'
    shutil.copy2(src, dest)
    print(dest)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
