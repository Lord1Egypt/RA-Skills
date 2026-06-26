#!/usr/bin/env python3
"""
RedactKit - Restoration Tool
Restore original values from mapping files.

Author: Shadow Rose
License: MIT
"""

import json
import os
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class RestorationMapping:
    """Mapping for restoring redacted values."""
    placeholder: str
    original_value: str
    pattern_name: str


class RestorationEngine:
    """Engine for restoring redacted text."""
    
    def __init__(self):
        """Initialize restoration engine."""
        self.mappings: Dict[str, List[RestorationMapping]] = {}
    
    def load_mapping(self, mapping_path: str) -> str:
        """
        Load a mapping file.
        
        Args:
            mapping_path: Path to mapping JSON file
        
        Returns:
            Mapping ID
        """
        try:
            with open(mapping_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise IOError(f"Error loading mapping file: {e}")
        
        mapping_id = data.get('mapping_id')
        if not mapping_id:
            raise ValueError("Invalid mapping file: missing mapping_id")
        
        # Build restoration mappings
        mappings = []
        for match in data.get('matches', []):
            mappings.append(RestorationMapping(
                placeholder=match['placeholder'],
                original_value=match['original_value'],
                pattern_name=match['pattern_name']
            ))
        
        self.mappings[mapping_id] = mappings
        
        return mapping_id
    
    def restore(self, redacted_text: str, mapping_id: str) -> str:
        """
        Restore original values in redacted text.
        
        Args:
            redacted_text: Redacted text with placeholders
            mapping_id: Mapping ID to use for restoration
        
        Returns:
            Restored text
        """
        if mapping_id not in self.mappings:
            raise ValueError(f"Mapping not loaded: {mapping_id}")
        
        restored = redacted_text
        
        # Replace each placeholder with original value
        for mapping in self.mappings[mapping_id]:
            restored = restored.replace(mapping.placeholder, mapping.original_value)
        
        return restored
    
    def restore_file(self, input_path: str, mapping_path: str, output_path: str):
        """
        Restore a redacted file.
        
        Args:
            input_path: Path to redacted file
            mapping_path: Path to mapping file
            output_path: Path for restored output
        """
        # Load mapping
        mapping_id = self.load_mapping(mapping_path)
        
        # Read redacted file
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                redacted_text = f.read()
        except Exception as e:
            raise IOError(f"Error reading redacted file: {e}")
        
        # Restore
        restored = self.restore(redacted_text, mapping_id)
        
        # Write output
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(restored)
        except Exception as e:
            raise IOError(f"Error writing restored file: {e}")
    
    def restore_directory(self, input_dir: str, mapping_dir: str, output_dir: str,
                         extensions: List[str] = None) -> Dict[str, bool]:
        """
        Restore all files in a directory.
        
        Args:
            input_dir: Directory with redacted files
            mapping_dir: Directory with mapping files
            output_dir: Output directory for restored files
            extensions: File extensions to process
        
        Returns:
            Dict mapping file paths to success status
        """
        if extensions is None:
            extensions = ['.txt', '.md', '.py', '.json', '.csv', '.yaml', '.yml']
        
        results = {}
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Process files
        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                # Check extension
                if not any(filename.endswith(ext) for ext in extensions):
                    continue
                
                input_path = os.path.join(root, filename)
                
                # Compute relative path
                rel_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, rel_path)
                
                # Mapping path
                mapping_path = os.path.join(mapping_dir, rel_path + '.mapping.json')
                
                if not os.path.exists(mapping_path):
                    print(f"Warning: No mapping found for {rel_path}")
                    results[rel_path] = False
                    continue
                
                # Create output subdirectory
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Restore file
                try:
                    self.restore_file(input_path, mapping_path, output_path)
                    results[rel_path] = True
                except Exception as e:
                    print(f"Warning: Error restoring {rel_path}: {e}")
                    results[rel_path] = False
        
        return results
    
    def verify_restoration(self, original_text: str, redacted_text: str,
                          restored_text: str) -> bool:
        """
        Verify that restoration matches original.
        
        Args:
            original_text: Original unredacted text
            redacted_text: Redacted text
            restored_text: Restored text
        
        Returns:
            True if restored matches original
        """
        return original_text == restored_text


def main():
    """CLI interface for restoration."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description='RedactKit Restore - Restore redacted data'
    )
    parser.add_argument(
        'input',
        help='Input redacted file or directory'
    )
    parser.add_argument(
        'mapping',
        help='Mapping file or directory'
    )
    parser.add_argument(
        '--output',
        help='Output file or directory'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Batch mode (restore directory)'
    )
    parser.add_argument(
        '--extensions',
        help='File extensions for batch mode (comma-separated)'
    )
    parser.add_argument(
        '--verify',
        help='Verify against original file (single file mode only)'
    )
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = RestorationEngine()
    
    try:
        if args.batch:
            # Batch mode
            if not os.path.isdir(args.input):
                print("Error: --batch requires an input directory", file=sys.stderr)
                sys.exit(1)
            
            if not os.path.isdir(args.mapping):
                print("Error: --batch requires a mapping directory", file=sys.stderr)
                sys.exit(1)
            
            if not args.output:
                print("Error: --output required for batch mode", file=sys.stderr)
                sys.exit(1)
            
            # Parse extensions
            extensions = None
            if args.extensions:
                extensions = ['.' + ext.lstrip('.') for ext in args.extensions.split(',')]
            
            # Restore directory
            results = engine.restore_directory(
                args.input,
                args.mapping,
                args.output,
                extensions=extensions
            )
            
            # Print summary
            success_count = sum(1 for v in results.values() if v)
            print(f"✅ Restored {success_count}/{len(results)} files")
            
            failed = [k for k, v in results.items() if not v]
            if failed:
                print(f"\n❌ Failed to restore {len(failed)} files:")
                for path in failed:
                    print(f"   {path}")
        
        else:
            # Single file mode
            if not args.output:
                print("Error: --output required", file=sys.stderr)
                sys.exit(1)
            
            # Restore file
            engine.restore_file(args.input, args.mapping, args.output)
            
            print(f"✅ Restored: {args.output}")
            
            # Verify if requested
            if args.verify:
                with open(args.verify, 'r', encoding='utf-8') as f:
                    original = f.read()
                
                with open(args.input, 'r', encoding='utf-8') as f:
                    redacted = f.read()
                
                with open(args.output, 'r', encoding='utf-8') as f:
                    restored = f.read()
                
                if engine.verify_restoration(original, redacted, restored):
                    print("✅ Verification passed: restored matches original")
                else:
                    print("❌ Verification failed: restored does NOT match original", file=sys.stderr)
                    sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
