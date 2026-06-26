#!/usr/bin/env python3
"""
Sentinel Manifest — Workspace snapshot generator
Part of Sentinel — AI Agent State Guardian

Author: Shadow Rose
License: MIT
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Import config
try:
    import sentinel_config as config
except ImportError:
    print("ERROR: sentinel_config.py not found. Copy config_example.py to sentinel_config.py and configure it.")
    sys.exit(1)


class ManifestGenerator:
    """Generate workspace manifests for comparison and verification."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.workspace = Path(config_obj.WORKSPACE_ROOT).resolve()
        self.exclude_patterns = getattr(config_obj, 'EXCLUDE_PATTERNS', [
            '.git', '__pycache__', '*.pyc', '*.swp', '.DS_Store'
        ])
    
    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from manifest."""
        path_str = str(path)
        
        for pattern in self.exclude_patterns:
            if pattern.startswith('*'):
                # Suffix match
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern.endswith('*'):
                # Prefix match
                if path.name.startswith(pattern[:-1]):
                    return True
            else:
                # Exact match
                if pattern in path.parts or path.name == pattern:
                    return True
        
        return False
    
    def hash_file(self, filepath: Path) -> Optional[str]:
        """Compute SHA-256 hash of a file."""
        try:
            sha256 = hashlib.sha256()
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception:
            return None
    
    def scan_file(self, filepath: Path) -> Dict:
        """Scan a single file and return its metadata."""
        try:
            stat = filepath.stat()
            
            return {
                'path': str(filepath.relative_to(self.workspace)),
                'size': stat.st_size,
                'mtime': stat.st_mtime,
                'mtime_iso': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'hash': self.hash_file(filepath) if stat.st_size < 100 * 1024 * 1024 else None,  # Skip hash for files >100MB
                'permissions': oct(stat.st_mode)[-3:],
            }
        except Exception as e:
            return {
                'path': str(filepath.relative_to(self.workspace)),
                'error': str(e)
            }
    
    def generate_manifest(self, include_hashes: bool = True) -> Dict:
        """Generate full workspace manifest."""
        manifest = {
            'generated': datetime.now().isoformat(),
            'workspace': str(self.workspace),
            'files': [],
            'directories': [],
            'summary': {
                'total_files': 0,
                'total_directories': 0,
                'total_size': 0,
                'errors': 0
            }
        }
        
        print(f"Scanning workspace: {self.workspace}")
        
        try:
            for root, dirs, files in os.walk(self.workspace):
                root_path = Path(root)
                
                # Filter excluded directories
                dirs[:] = [d for d in dirs if not self.should_exclude(root_path / d)]
                
                # Record directory
                if root_path != self.workspace:
                    rel_path = root_path.relative_to(self.workspace)
                    if not self.should_exclude(root_path):
                        manifest['directories'].append(str(rel_path))
                        manifest['summary']['total_directories'] += 1
                
                # Scan files
                for filename in files:
                    filepath = root_path / filename
                    
                    if self.should_exclude(filepath):
                        continue
                    
                    file_data = self.scan_file(filepath)
                    
                    if not include_hashes and 'hash' in file_data:
                        del file_data['hash']
                    
                    manifest['files'].append(file_data)
                    manifest['summary']['total_files'] += 1
                    
                    if 'error' in file_data:
                        manifest['summary']['errors'] += 1
                    else:
                        manifest['summary']['total_size'] += file_data.get('size', 0)
                    
                    # Progress indicator
                    if manifest['summary']['total_files'] % 100 == 0:
                        print(f"  Scanned {manifest['summary']['total_files']} files...", end='\r')
        
        except Exception as e:
            print(f"\nError during scan: {e}")
        
        print(f"\nScan complete: {manifest['summary']['total_files']} files, "
              f"{manifest['summary']['total_directories']} directories, "
              f"{manifest['summary']['total_size']:,} bytes")
        
        return manifest
    
    def save_manifest(self, manifest: Dict, output_file: Path):
        """Save manifest to file."""
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'w') as f:
                json.dump(manifest, f, indent=2)
            
            print(f"✓ Manifest saved: {output_file}")
            return True
        except Exception as e:
            print(f"✗ Failed to save manifest: {e}")
            return False
    
    def compare_manifests(self, old_manifest: Dict, new_manifest: Dict) -> Dict:
        """Compare two manifests and return differences."""
        # Build file lookup tables
        old_files = {f['path']: f for f in old_manifest.get('files', [])}
        new_files = {f['path']: f for f in new_manifest.get('files', [])}
        
        old_dirs = set(old_manifest.get('directories', []))
        new_dirs = set(new_manifest.get('directories', []))
        
        differences = {
            'added_files': [],
            'deleted_files': [],
            'modified_files': [],
            'added_dirs': list(new_dirs - old_dirs),
            'deleted_dirs': list(old_dirs - new_dirs),
            'summary': {}
        }
        
        # Find added and modified files
        for path, new_data in new_files.items():
            if path not in old_files:
                differences['added_files'].append(path)
            else:
                old_data = old_files[path]
                
                # Check for modifications
                if 'hash' in old_data and 'hash' in new_data:
                    if old_data['hash'] != new_data['hash']:
                        differences['modified_files'].append({
                            'path': path,
                            'old_size': old_data.get('size'),
                            'new_size': new_data.get('size'),
                            'old_mtime': old_data.get('mtime_iso'),
                            'new_mtime': new_data.get('mtime_iso')
                        })
                elif old_data.get('size') != new_data.get('size') or old_data.get('mtime') != new_data.get('mtime'):
                    differences['modified_files'].append({
                        'path': path,
                        'old_size': old_data.get('size'),
                        'new_size': new_data.get('size'),
                        'old_mtime': old_data.get('mtime_iso'),
                        'new_mtime': new_data.get('mtime_iso')
                    })
        
        # Find deleted files
        for path in old_files:
            if path not in new_files:
                differences['deleted_files'].append(path)
        
        # Summary
        differences['summary'] = {
            'added_files': len(differences['added_files']),
            'deleted_files': len(differences['deleted_files']),
            'modified_files': len(differences['modified_files']),
            'added_dirs': len(differences['added_dirs']),
            'deleted_dirs': len(differences['deleted_dirs'])
        }
        
        return differences
    
    def print_diff_summary(self, diff: Dict):
        """Print human-readable diff summary."""
        summary = diff['summary']
        
        print("\n=== Manifest Comparison ===\n")
        print(f"Added files:    {summary['added_files']}")
        print(f"Deleted files:  {summary['deleted_files']}")
        print(f"Modified files: {summary['modified_files']}")
        print(f"Added dirs:     {summary['added_dirs']}")
        print(f"Deleted dirs:   {summary['deleted_dirs']}")
        
        if summary['added_files'] > 0:
            print("\nAdded files:")
            for path in diff['added_files'][:10]:
                print(f"  + {path}")
            if summary['added_files'] > 10:
                print(f"  ... and {summary['added_files'] - 10} more")
        
        if summary['deleted_files'] > 0:
            print("\nDeleted files:")
            for path in diff['deleted_files'][:10]:
                print(f"  - {path}")
            if summary['deleted_files'] > 10:
                print(f"  ... and {summary['deleted_files'] - 10} more")
        
        if summary['modified_files'] > 0:
            print("\nModified files:")
            for item in diff['modified_files'][:10]:
                print(f"  M {item['path']}")
                if item.get('old_size') != item.get('new_size'):
                    print(f"    Size: {item.get('old_size')} → {item.get('new_size')}")
            if summary['modified_files'] > 10:
                print(f"  ... and {summary['modified_files'] - 10} more")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sentinel Manifest — Workspace snapshot generator")
    parser.add_argument('--output', type=str, help='Output manifest file path')
    parser.add_argument('--no-hashes', action='store_true', help='Skip file hash computation (faster)')
    parser.add_argument('--compare', type=str, help='Compare with existing manifest')
    parser.add_argument('--diff-output', type=str, help='Save diff to file')
    
    args = parser.parse_args()
    
    generator = ManifestGenerator(config)
    
    # Generate current manifest
    include_hashes = not args.no_hashes
    manifest = generator.generate_manifest(include_hashes=include_hashes)
    
    # Save manifest if output specified
    if args.output:
        generator.save_manifest(manifest, Path(args.output))
    
    # Compare with existing manifest if requested
    if args.compare:
        try:
            with open(args.compare, 'r') as f:
                old_manifest = json.load(f)
            
            diff = generator.compare_manifests(old_manifest, manifest)
            generator.print_diff_summary(diff)
            
            if args.diff_output:
                with open(args.diff_output, 'w') as f:
                    json.dump(diff, f, indent=2)
                print(f"\n✓ Diff saved: {args.diff_output}")
        
        except Exception as e:
            print(f"✗ Failed to compare manifests: {e}")


if __name__ == '__main__':
    main()
