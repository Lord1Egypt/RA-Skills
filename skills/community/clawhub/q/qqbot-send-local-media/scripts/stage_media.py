import shutil
import sys
import uuid
from pathlib import Path

MAX_SIZE = 100 * 1024 * 1024
DEST_DIR = Path.home() / '.openclaw' / 'media' / 'qqbot'


def ensure_file_not_occupied(path: Path) -> None:
    try:
        with path.open('rb'):
            pass
    except PermissionError as e:
        raise RuntimeError(f'ERROR: file is occupied or permission denied: {path}') from e
    except OSError as e:
        raise RuntimeError(f'ERROR: failed to open file: {path}: {e}') from e


def cleanup_staged_file(path: Path) -> None:
    staged = path.expanduser()
    if not staged.is_absolute():
        staged = staged.resolve()

    dest_dir = DEST_DIR.resolve()
    staged = staged.resolve()

    try:
        staged.relative_to(dest_dir)
    except ValueError:
        raise RuntimeError(f'ERROR: refusing to delete file outside staged directory: {staged}')

    if not staged.exists() or not staged.is_file():
        raise RuntimeError(f'ERROR: staged file not found: {staged}')

    staged.unlink()


def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == '--cleanup':
        try:
            cleanup_staged_file(Path(sys.argv[2]))
        except RuntimeError as e:
            print(e, file=sys.stderr)
            return 1
        return 0

    if len(sys.argv) != 2:
        print('usage: python stage_media.py <source_path>', file=sys.stderr)
        print('usage: python stage_media.py --cleanup <staged_path>', file=sys.stderr)
        return 2

    src = Path(sys.argv[1]).expanduser()
    if not src.is_absolute():
        src = src.resolve()

    if not src.exists() or not src.is_file():
        print(f'ERROR: file not found: {src}', file=sys.stderr)
        return 1

    try:
        ensure_file_not_occupied(src)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1

    size = src.stat().st_size
    if size > MAX_SIZE:
        print(f'ERROR: file too large: {size} bytes > {MAX_SIZE} bytes', file=sys.stderr)
        return 1

    DEST_DIR.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    dest = DEST_DIR / f'{uuid.uuid4()}{ext}'
    shutil.copy2(src, dest)
    print(dest)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())