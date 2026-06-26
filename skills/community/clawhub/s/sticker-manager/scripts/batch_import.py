#!/usr/bin/env python3
"""Batch import stickers from local directories."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List

from common import get_lang, get_target_dir, SUPPORTED_EXTS, build_vision_plan

DEFAULT_MIN_SIZE = 5 * 1024  # 5KB minimum
DEFAULT_MAX_SIZE = 10 * 1024 * 1024  # 10MB maximum

MESSAGES_IMPORT: Dict[str, Dict[str, str]] = {
    "import_title": {"zh": "📦 批量导入表情包:", "en": "📦 Batch importing stickers:"},
    "import_scanning": {"zh": "  扫描目录: {path}", "en": "  Scanning: {path}"},
    "import_found": {"zh": "  发现 {count} 个图片文件", "en": "  Found {count} image files"},
    "import_copying": {"zh": "  复制中...", "en": "  Copying..."},
    "import_copied": {"zh": "  ✓ {name} ({size_kb}KB)", "en": "  ✓ {name} ({size_kb}KB)"},
    "import_skipped_small": {"zh": "  ✗ 跳过 (太小): {name} ({size}B)", "en": "  ✗ Skipped (too small): {name} ({size}B)"},
    "import_skipped_large": {"zh": "  ✗ 跳过 (太大): {name} ({size_mb}MB)", "en": "  ✗ Skipped (too large): {name} ({size_mb}MB)"},
    "import_skipped_exists": {"zh": "  ✗ 跳过 (已存在): {name}", "en": "  ✗ Skipped (exists): {name}"},
    "import_deduped": {"zh": "  ✗ 跳过 (重复): {name}", "en": "  ✗ Skipped (duplicate): {name}"},
    "import_summary": {"zh": "\n📊 导入完成: {imported} 个导入, {skipped} 个跳过, {duplicates} 个重复", "en": "\n📊 Import complete: {imported} imported, {skipped} skipped, {duplicates} duplicates"},
    "import_no_files": {"zh": "未找到可导入的图片文件", "en": "No image files found to import"},
    "import_no_dirs": {"zh": "未指定有效的源目录", "en": "No valid source directories specified"},
    "import_output": {"zh": "📝 导入报告已保存到: {path}", "en": "📝 Import report saved to: {path}"},
}


def t_import(key: str, lang: str, **kwargs) -> str:
    entry = MESSAGES_IMPORT.get(key, {})
    template = entry.get(lang) or entry.get('en') or key
    return template.format(**kwargs)


def is_image_file(path: Path) -> bool:
    """Check if file has a supported image extension."""
    return path.suffix.lower() in SUPPORTED_EXTS


def compute_file_hash(path: Path) -> str:
    """Compute MD5 hash of file content."""
    return hashlib.md5(path.read_bytes()).hexdigest()


def scan_source_directory(directory: str, recursive: bool = True) -> List[Path]:
    """Scan a directory for image files."""
    results = []
    base = Path(directory).expanduser()
    if not base.exists() or not base.is_dir():
        return results
    
    if recursive:
        pattern = '**/*'
    else:
        pattern = '*'
    
    for f in base.glob(pattern):
        if f.is_file() and is_image_file(f):
            results.append(f)
    return results


def import_stickers(
    source_dirs: List[str],
    target_dir: str,
    recursive: bool = True,
    min_size: int = DEFAULT_MIN_SIZE,
    max_size: int = DEFAULT_MAX_SIZE,
    dedupe: bool = True,
    copy: bool = True,
    lang: str = 'en',
) -> Dict:
    """Import stickers from source directories to target directory."""
    
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Compute hashes of existing files for deduplication
    existing_hashes: Dict[str, str] = {}
    if dedupe:
        for f in target_path.glob('*'):
            if f.is_file() and is_image_file(f):
                existing_hashes[compute_file_hash(f)] = str(f)
    
    imported = []
    skipped = []
    duplicates = []
    imported_hashes = set(existing_hashes.keys())
    
    for source_dir in source_dirs:
        print(t_import('import_scanning', lang, path=source_dir))
        files = scan_source_directory(source_dir, recursive=recursive)
        print(t_import('import_found', lang, count=len(files)))
        
        for src_file in files:
            name = src_file.name
            size = src_file.stat().st_size
            
            # Check size constraints
            if size < min_size:
                skipped.append({'path': str(src_file), 'reason': 'too_small', 'size': size})
                print(t_import('import_skipped_small', lang, name=name, size=size))
                continue
            
            if size > max_size:
                size_mb = size / (1024 * 1024)
                skipped.append({'path': str(src_file), 'reason': 'too_large', 'size': size})
                print(t_import('import_skipped_large', lang, name=name, size_mb=f'{size_mb:.1f}'))
                continue
            
            # Check deduplication
            if dedupe:
                file_hash = compute_file_hash(src_file)
                if file_hash in imported_hashes:
                    duplicate = {'path': str(src_file), 'reason': 'duplicate', 'hash': file_hash}
                    skipped.append(duplicate)
                    duplicates.append(duplicate)
                    print(t_import('import_deduped', lang, name=name))
                    continue
                imported_hashes.add(file_hash)
            
            # Check if already exists
            target_file = target_path / name
            if target_file.exists():
                skipped.append({'path': str(src_file), 'reason': 'exists', 'target': str(target_file)})
                print(t_import('import_skipped_exists', lang, name=name))
                continue
            
            # Copy or link file
            size_kb = size // 1024
            if copy:
                shutil.copy2(src_file, target_file)
            else:
                target_file.symlink_to(src_file)
            
            imported.append({
                'source': str(src_file),
                'target': str(target_file),
                'name': name,
                'size': size,
            })
            print(t_import('import_copied', lang, name=name, size_kb=size_kb))
    
    return {
        'imported': imported,
        'skipped': skipped,
        'duplicates': duplicates,
        'summary': {
            'imported_count': len(imported),
            'skipped_count': len(skipped),
            'total_found': len(imported) + len(skipped),
        }
    }


def build_auto_tag_plan(imported: List[Dict], lang: str) -> Dict:
    """Build a plan for auto-tagging imported stickers."""
    return {
        'task': 'Auto-tag imported stickers with semantic metadata',
        'language': lang,
        'items': [
            {
                'name': item['name'],
                'path': item['target'],
                'vision_plan': build_vision_plan(
                    item['target'],
                    'Analyze this sticker image. Extract: emotions (list), scenes (list), keywords (list), and a brief description.',
                    lang
                ),
            }
            for item in imported
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Batch import stickers from local directories.')
    parser.add_argument('sources', nargs='*', help='Source directories to import from')
    parser.add_argument('--sources-file', help='File containing source directories (one per line)')
    parser.add_argument('--target-dir', default=None, help='Target sticker library directory')
    parser.add_argument('--recursive', '-r', action='store_true', default=True, help='Scan directories recursively (default: True)')
    parser.add_argument('--no-recursive', action='store_false', dest='recursive', help='Do not scan directories recursively')
    parser.add_argument('--min-size', type=int, default=DEFAULT_MIN_SIZE, help='Minimum file size in bytes')
    parser.add_argument('--max-size', type=int, default=DEFAULT_MAX_SIZE, help='Maximum file size in bytes')
    parser.add_argument('--no-dedupe', action='store_false', dest='dedupe', help='Skip deduplication')
    parser.add_argument('--symlink', action='store_true', help='Create symlinks instead of copying')
    parser.add_argument('--lang')
    parser.add_argument('--output', '-o', help='Output JSON file for import report')
    parser.add_argument('--auto-tag', action='store_true', help='Generate auto-tag plan for imported stickers')
    args = parser.parse_args()

    lang = get_lang(args.lang)
    target_dir = args.target_dir or get_target_dir()
    
    # Collect source directories
    source_dirs = []
    for src in args.sources:
        expanded = os.path.expanduser(src)
        if os.path.isdir(expanded):
            source_dirs.append(expanded)
    
    if args.sources_file:
        for line in Path(args.sources_file).read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                expanded = os.path.expanduser(line)
                if os.path.isdir(expanded):
                    source_dirs.append(expanded)
    
    if not source_dirs:
        print(t_import('import_no_dirs', lang))
        return 1
    
    print(t_import('import_title', lang))
    
    result = import_stickers(
        source_dirs=source_dirs,
        target_dir=target_dir,
        recursive=args.recursive,
        min_size=args.min_size,
        max_size=args.max_size,
        dedupe=args.dedupe,
        copy=not args.symlink,
        lang=lang,
    )
    
    summary = result['summary']
    print(t_import('import_summary', lang, 
        imported=summary['imported_count'],
        skipped=summary['skipped_count'],
        duplicates=len(result['duplicates'])))
    
    # Add auto-tag plan if requested
    if args.auto_tag and result['imported']:
        result['auto_tag_plan'] = build_auto_tag_plan(result['imported'], lang)
        print('\n__AUTO_TAG_PLAN__:' + json.dumps(result['auto_tag_plan'], ensure_ascii=False))
    
    # Output report
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(t_import('import_output', lang, path=args.output))
    
    return 0 if summary['imported_count'] > 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
