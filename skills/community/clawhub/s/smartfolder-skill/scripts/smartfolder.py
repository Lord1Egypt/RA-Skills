#!/usr/bin/env python3
"""
SmartFolder - Intelligent File Organization Assistant
Main entry point
"""

import sys
import os

# Ensure Python 3.8+
if sys.version_info < (3, 8):
    print("Error: Python 3.8+ required", file=sys.stderr)
    sys.exit(1)

from pathlib import Path
import argparse
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import hashlib
from collections import defaultdict

__version__ = "1.0.0"

# Default file categories
DEFAULT_CATEGORIES = {
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".raw", ".cr2"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm", ".m4v", ".mpg", ".mpeg"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a", ".opus"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".xml", ".yaml", ".yml", ".sql", ".sh", ".bat"],
    "Executables": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".appimage"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "Data": [".csv", ".tsv", ".db", ".sqlite", ".parquet", ".feather"]
}

class SmartFolder:
    """Main class for file organization operations"""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.operations_log = []
        
    def log_operation(self, operation: str, source: str, target: str = None):
        """Log an operation for potential undo"""
        self.operations_log.append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "source": source,
            "target": target
        })
    
    def get_file_category(self, file_path: Path) -> str:
        """Determine file category based on extension"""
        ext = file_path.suffix.lower()
        for category, extensions in DEFAULT_CATEGORIES.items():
            if ext in extensions:
                return category
        return "Misc"
    
    def format_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} PB"
    
    def organize_by_type(self, source_dir: Path, target_dir: Path = None) -> Dict:
        """Organize files by type into subdirectories"""
        if target_dir is None:
            target_dir = source_dir
            
        source_dir = Path(source_dir).expanduser().resolve()
        target_dir = Path(target_dir).expanduser().resolve()
        
        if not source_dir.exists():
            return {"error": f"Source directory does not exist: {source_dir}"}
        
        # Scan files
        files = [f for f in source_dir.iterdir() if f.is_file() and not f.name.startswith('.')]
        
        if not files:
            return {"message": "No files to organize", "organized": 0}
        
        # Plan operations
        operations = []
        for file_path in files:
            category = self.get_file_category(file_path)
            target_subdir = target_dir / category
            target_path = target_subdir / file_path.name
            
            # Handle name conflicts
            counter = 1
            original_target = target_path
            while target_path.exists() and target_path != file_path:
                stem = original_target.stem
                suffix = original_target.suffix
                target_path = original_target.parent / f"{stem}_{counter}{suffix}"
                counter += 1
            
            operations.append({
                "source": file_path,
                "target": target_path,
                "category": category
            })
        
        if self.dry_run:
            return {
                "dry_run": True,
                "operations": len(operations),
                "plan": operations
            }
        
        # Execute operations
        organized = 0
        for op in operations:
            try:
                op["target"].parent.mkdir(parents=True, exist_ok=True)
                op["source"].rename(op["target"])
                self.log_operation("move", str(op["source"]), str(op["target"]))
                organized += 1
            except Exception as e:
                print(f"Error moving {op['source']}: {e}", file=sys.stderr)
        
        return {
            "organized": organized,
            "categories": len(set(op["category"] for op in operations))
        }
    
    def find_duplicates(self, directory: Path, min_size: int = 1024) -> Dict[str, List[Path]]:
        """Find duplicate files by hash"""
        directory = Path(directory).expanduser().resolve()
        
        if not directory.exists():
            return {"error": f"Directory does not exist: {directory}"}
        
        # Collect all files
        files = []
        for path in directory.rglob("*"):
            if path.is_file() and not path.name.startswith('.') and path.stat().st_size >= min_size:
                files.append(path)
        
        if not files:
            return {"duplicates": {}, "total_files": 0}
        
        # Calculate hashes
        hash_map = defaultdict(list)
        total = len(files)
        
        print(f"Scanning {total} files...")
        
        for i, file_path in enumerate(files, 1):
            if i % 100 == 0:
                print(f"Progress: {i}/{total}")
            
            try:
                file_hash = self._file_hash(file_path)
                hash_map[file_hash].append(file_path)
            except Exception as e:
                print(f"Error hashing {file_path}: {e}", file=sys.stderr)
        
        # Filter duplicates
        duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
        
        return {
            "duplicates": duplicates,
            "total_files": total,
            "duplicate_groups": len(duplicates),
            "duplicate_files": sum(len(paths) - 1 for paths in duplicates.values())
        }
    
    def _file_hash(self, file_path: Path, chunk_size: int = 8192) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def analyze_disk_usage(self, directory: Path, top_n: int = 20, older_than_days: int = None) -> Dict:
        """Analyze disk usage and find large/old files"""
        directory = Path(directory).expanduser().resolve()
        
        if not directory.exists():
            return {"error": f"Directory does not exist: {directory}"}
        
        files = []
        total_size = 0
        cutoff_time = None
        
        if older_than_days:
            from datetime import timedelta
            cutoff_time = datetime.now() - timedelta(days=older_than_days)
        
        # Collect all files
        for path in directory.rglob("*"):
            if path.is_file() and not path.name.startswith('.'):
                try:
                    stat = path.stat()
                    mtime = datetime.fromtimestamp(stat.st_mtime)
                    
                    if cutoff_time and mtime > cutoff_time:
                        continue
                    
                    files.append({
                        "path": path,
                        "size": stat.st_size,
                        "modified": mtime
                    })
                    total_size += stat.st_size
                except Exception:
                    pass
        
        # Sort by size
        files.sort(key=lambda x: x["size"], reverse=True)
        
        # Category breakdown
        categories = defaultdict(int)
        for f in files:
            cat = self.get_file_category(f["path"])
            categories[cat] += f["size"]
        
        return {
            "total_files": len(files),
            "total_size": total_size,
            "total_size_formatted": self.format_size(total_size),
            "top_files": files[:top_n],
            "categories": dict(categories)
        }

def main():
    parser = argparse.ArgumentParser(
        description="SmartFolder - Intelligent File Organization Assistant",
        prog="smartfolder"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without executing")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Organize command
    org_parser = subparsers.add_parser("organize", help="Organize files in a directory")
    org_parser.add_argument("path", help="Directory to organize")
    org_parser.add_argument("--by-type", action="store_true", default=True, help="Organize by file type")
    org_parser.add_argument("--target-dir", help="Target directory (default: same as source)")
    
    # Duplicates command
    dup_parser = subparsers.add_parser("duplicates", help="Find duplicate files")
    dup_parser.add_argument("path", help="Directory to scan")
    dup_parser.add_argument("--min-size", type=int, default=1024, help="Minimum file size in bytes")
    
    # Analyze command
    ana_parser = subparsers.add_parser("analyze", help="Analyze disk usage")
    ana_parser.add_argument("path", help="Directory to analyze")
    ana_parser.add_argument("--top", type=int, default=20, help="Show top N largest files")
    ana_parser.add_argument("--older-than", type=int, help="Find files older than N days")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    sf = SmartFolder(dry_run=args.dry_run)
    
    if args.command == "organize":
        result = sf.organize_by_type(Path(args.path), Path(args.target_dir) if args.target_dir else None)
        
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        if result.get("dry_run"):
            print("[DRY RUN] No files will be moved")
            print(f"\nPlanned operations: {result['operations']}")
            for op in result["plan"]:
                print(f"  {op['source'].name} -> {op['category']}/{op['target'].name}")
        else:
            print(f"Organized {result['organized']} files into {result['categories']} categories")
    
    elif args.command == "duplicates":
        result = sf.find_duplicates(Path(args.path), args.min_size)
        
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        print(f"\n[SCAN RESULTS]")
        print(f"  Total files scanned: {result['total_files']}")
        print(f"  Duplicate groups found: {result['duplicate_groups']}")
        print(f"  Duplicate files: {result['duplicate_files']}")
        
        if result["duplicates"]:
            print("\n[DUPLICATE FILES]:")
            for hash_val, paths in result["duplicates"].items():
                print(f"\n  Group (hash: {hash_val[:16]}...):")
                for p in paths:
                    size = p.stat().st_size
                    print(f"    - {p} ({sf.format_size(size)})")
    
    elif args.command == "analyze":
        result = sf.analyze_disk_usage(Path(args.path), args.top, args.older_than)
        
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        print(f"\n[DISK USAGE ANALYSIS]: {args.path}")
        print(f"\n  Total files: {result['total_files']}")
        print(f"  Total size: {result['total_size_formatted']}")
        
        if result["categories"]:
            print(f"\n[BY CATEGORY]:")
            for cat, size in sorted(result["categories"].items(), key=lambda x: x[1], reverse=True):
                print(f"  {cat}: {sf.format_size(size)}")
        
        if result["top_files"]:
            print(f"\n[TOP {args.top} LARGEST FILES]:")
            for i, f in enumerate(result["top_files"], 1):
                print(f"  {i}. {f['path']} ({sf.format_size(f['size'])})")

if __name__ == "__main__":
    main()
