#!/usr/bin/env python3
"""
RedactKit - AI Privacy Scrubber
Main scanning and redaction engine.

Author: Shadow Rose
License: MIT
"""

import json
import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from redact_patterns import PatternLibrary, CustomPatternManager, RedactionPattern


@dataclass
class RedactionMatch:
    """A single redaction match."""
    pattern_name: str
    original_value: str
    placeholder: str
    start_pos: int
    end_pos: int
    category: str
    sensitivity: str


@dataclass
class RedactionResult:
    """Result of redacting a text."""
    original_text: str
    redacted_text: str
    matches: List[RedactionMatch]
    mapping_id: str  # For restoration


class RedactionEngine:
    """Main redaction engine."""
    
    def __init__(self, sensitivity_level: str = 'medium', 
                 custom_patterns: CustomPatternManager = None,
                 enabled_categories: List[str] = None):
        """
        Initialize redaction engine.
        
        Args:
            sensitivity_level: Minimum sensitivity level ('low', 'medium', 'high')
            custom_patterns: CustomPatternManager for user patterns
            enabled_categories: List of enabled categories (None = all)
        """
        self.sensitivity_level = sensitivity_level
        self.custom_patterns = custom_patterns or CustomPatternManager()
        self.enabled_categories = enabled_categories
        
        # Build pattern list
        self.patterns = self._build_pattern_list()
        
        # Mapping storage for restoration
        self.mappings: Dict[str, List[RedactionMatch]] = {}
    
    def _build_pattern_list(self) -> List[RedactionPattern]:
        """Build list of active patterns based on config."""
        # Get built-in patterns by sensitivity
        patterns = PatternLibrary.get_by_sensitivity(self.sensitivity_level)
        
        # Add custom patterns
        patterns.extend(self.custom_patterns.get_all())
        
        # Filter by category if specified
        if self.enabled_categories:
            patterns = [p for p in patterns if p.category in self.enabled_categories]
        
        return patterns
    
    def redact(self, text: str, mapping_id: str = None) -> RedactionResult:
        """
        Redact sensitive data from text.
        
        Args:
            text: Input text to redact
            mapping_id: Optional ID for restoration mapping
        
        Returns:
            RedactionResult with redacted text and match details
        """
        if mapping_id is None:
            import hashlib
            from datetime import datetime
            mapping_id = hashlib.sha256(
                (text + datetime.utcnow().isoformat()).encode()
            ).hexdigest()[:16]
        
        matches = []
        redacted = text
        offset = 0  # Track position changes from replacements
        
        # Track replacements per pattern for indexing
        pattern_counters = {}
        
        # Find all matches
        for pattern in self.patterns:
            pattern_matches = []
            
            for match in pattern.pattern.finditer(text):
                # Get match value
                if match.groups():
                    # If there are groups, use the first group
                    value = match.group(1)
                    start = match.start(1)
                    end = match.end(1)
                else:
                    value = match.group(0)
                    start = match.start()
                    end = match.end()
                
                pattern_matches.append((start, end, value))
            
            # Sort by position
            pattern_matches.sort(key=lambda x: x[0])
            
            # Apply redactions
            pattern_counter = pattern_counters.get(pattern.name, 0)
            
            for start, end, value in pattern_matches:
                pattern_counter += 1
                
                # Generate placeholder
                placeholder = pattern.placeholder_template.format(index=pattern_counter)
                
                # Record match
                redaction_match = RedactionMatch(
                    pattern_name=pattern.name,
                    original_value=value,
                    placeholder=placeholder,
                    start_pos=start + offset,
                    end_pos=end + offset,
                    category=pattern.category,
                    sensitivity=pattern.sensitivity
                )
                
                matches.append(redaction_match)
            
            pattern_counters[pattern.name] = pattern_counter
        
        # Sort matches by position (reverse order for replacement)
        matches.sort(key=lambda m: m.start_pos, reverse=True)
        
        # Apply replacements (reverse order to maintain positions)
        for match in matches:
            redacted = (
                redacted[:match.start_pos] +
                match.placeholder +
                redacted[match.end_pos:]
            )
        
        # Store mapping
        self.mappings[mapping_id] = matches
        
        return RedactionResult(
            original_text=text,
            redacted_text=redacted,
            matches=matches,
            mapping_id=mapping_id
        )
    
    def save_mapping(self, mapping_id: str, output_path: str):
        """
        Save redaction mapping to file for restoration.
        
        Args:
            mapping_id: Mapping ID to save
            output_path: Output file path
        """
        if mapping_id not in self.mappings:
            raise ValueError(f"Mapping not found: {mapping_id}")
        
        mapping_data = {
            'mapping_id': mapping_id,
            'matches': [asdict(m) for m in self.mappings[mapping_id]]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(mapping_data, f, indent=2)
    
    def redact_file(self, input_path: str, output_path: str,
                   mapping_path: str = None, report_only: bool = False) -> RedactionResult:
        """
        Redact a file.
        
        Args:
            input_path: Input file path
            output_path: Output file path
            mapping_path: Path to save mapping (optional)
            report_only: If True, don't write output, just return result
        
        Returns:
            RedactionResult
        """
        # Read input
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            raise IOError(f"Error reading {input_path}: {e}")
        
        # Redact
        result = self.redact(text)
        
        # Write output if not report-only
        if not report_only:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(result.redacted_text)
            except Exception as e:
                raise IOError(f"Error writing {output_path}: {e}")
        
        # Save mapping if requested
        if mapping_path:
            self.save_mapping(result.mapping_id, mapping_path)
        
        return result
    
    def redact_directory(self, input_dir: str, output_dir: str,
                        mapping_dir: str = None, extensions: List[str] = None,
                        report_only: bool = False) -> Dict[str, RedactionResult]:
        """
        Redact all files in a directory.
        
        Args:
            input_dir: Input directory
            output_dir: Output directory
            mapping_dir: Directory for mapping files (optional)
            extensions: File extensions to process (default: .txt, .md, .py, .json, .csv, .yaml)
            report_only: If True, don't write files, just return results
        
        Returns:
            Dict mapping file paths to RedactionResults
        """
        if extensions is None:
            extensions = ['.txt', '.md', '.py', '.json', '.csv', '.yaml', '.yml']
        
        results = {}
        
        # Create output directories
        if not report_only:
            os.makedirs(output_dir, exist_ok=True)
            if mapping_dir:
                os.makedirs(mapping_dir, exist_ok=True)
        
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
                
                # Create output subdirectory
                if not report_only:
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                
                # Mapping path
                if mapping_dir:
                    mapping_path = os.path.join(mapping_dir, rel_path + '.mapping.json')
                    os.makedirs(os.path.dirname(mapping_path), exist_ok=True)
                else:
                    mapping_path = None
                
                # Redact file
                try:
                    result = self.redact_file(
                        input_path,
                        output_path,
                        mapping_path=mapping_path,
                        report_only=report_only
                    )
                    results[rel_path] = result
                except Exception as e:
                    print(f"Warning: Error processing {rel_path}: {e}")
        
        return results


def main():
    """CLI interface for RedactKit."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description='RedactKit - AI Privacy Scrubber'
    )
    parser.add_argument(
        'input',
        nargs='?',
        help='Input file or directory (stdin if not provided)'
    )
    parser.add_argument(
        '--output',
        help='Output file or directory'
    )
    parser.add_argument(
        '--mapping',
        help='Mapping file or directory for restoration'
    )
    parser.add_argument(
        '--sensitivity',
        default='medium',
        choices=['low', 'medium', 'high'],
        help='Sensitivity level'
    )
    parser.add_argument(
        '--category',
        action='append',
        help='Enable specific category (repeatable)'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Report mode (show what would be redacted, no output)'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Batch mode (process directory)'
    )
    parser.add_argument(
        '--extensions',
        help='File extensions for batch mode (comma-separated, default: .txt,.md,.py,.json,.csv,.yaml)'
    )
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = RedactionEngine(
        sensitivity_level=args.sensitivity,
        enabled_categories=args.category
    )
    
    try:
        if args.batch:
            # Batch mode
            if not args.input or not os.path.isdir(args.input):
                print("Error: --batch requires an input directory", file=sys.stderr)
                sys.exit(1)
            
            if not args.output and not args.report:
                print("Error: --output required for batch mode (unless --report)", file=sys.stderr)
                sys.exit(1)
            
            # Parse extensions
            extensions = None
            if args.extensions:
                extensions = ['.' + ext.lstrip('.') for ext in args.extensions.split(',')]
            
            # Process directory
            results = engine.redact_directory(
                args.input,
                args.output or '/tmp/redact-output',
                mapping_dir=args.mapping,
                extensions=extensions,
                report_only=args.report
            )
            
            # Print summary
            total_matches = sum(len(r.matches) for r in results.values())
            print(f"✅ Processed {len(results)} files")
            print(f"   Found {total_matches} sensitive items")
            
            if args.report:
                print("\n🔍 Report mode - no files written\n")
                for path, result in results.items():
                    if result.matches:
                        print(f"{path}: {len(result.matches)} matches")
        
        else:
            # Single file/stdin mode
            if args.input:
                # File input
                result = engine.redact_file(
                    args.input,
                    args.output or args.input + '.redacted',
                    mapping_path=args.mapping,
                    report_only=args.report
                )
            else:
                # Stdin input
                text = sys.stdin.read()
                result = engine.redact(text)
                
                if not args.report:
                    print(result.redacted_text)
                
                if args.mapping:
                    engine.save_mapping(result.mapping_id, args.mapping)
            
            # Print summary
            print(f"\n✅ Found {len(result.matches)} sensitive items:", file=sys.stderr)
            
            # Group by category
            by_category = {}
            for match in result.matches:
                by_category.setdefault(match.category, []).append(match)
            
            for category, matches in sorted(by_category.items()):
                print(f"   {category}: {len(matches)}", file=sys.stderr)
            
            if args.report:
                print("\n🔍 Report mode - showing matches:\n", file=sys.stderr)
                for match in result.matches[:10]:  # First 10
                    print(f"  [{match.pattern_name}] {match.original_value[:30]} → {match.placeholder}", file=sys.stderr)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
