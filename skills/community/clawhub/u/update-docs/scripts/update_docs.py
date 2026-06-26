#!/usr/bin/env python3
"""
Update documentation based on code changes for OpenClaw projects.

This script provides a guided workflow for updating documentation
when source code changes are made, ensuring code and docs stay in sync.
"""

import subprocess
import sys
import os
import json
import argparse
from pathlib import Path

def run_git_command(args):
    """Run git command with error handling."""
    try:
        result = subprocess.run(['git'] + args, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(args)}", file=sys.stderr)
        print(f"Error: {e.stderr}", file=sys.stderr)
        return None

def get_changed_files(base_branch="main"):
    """Get list of changed files between base branch and current HEAD."""
    diff_cmd = ["diff", f"{base_branch}...HEAD", "--name-only"]
    result = run_git_command(diff_cmd)
    if result:
        return result.split('\n')
    return []

def identify_doc_relevant_changes(changed_files):
    """Identify which changed files are relevant to documentation."""
    doc_relevant = []
    patterns = [
        'src/',           # Source code changes
        'packages/',      # Package changes  
        'lib/',           # Library changes
        'api/',           # API changes
        'skills/',        # Skill changes
        'docs/',          # Direct doc changes
        'examples/',      # Example changes
        'test/',          # Test changes that might affect examples
    ]
    
    for file_path in changed_files:
        if any(pattern in file_path for pattern in patterns):
            doc_relevant.append(file_path)
    
    return doc_relevant

def map_to_docs(changed_files, mapping_file=None):
    """Map changed source files to corresponding documentation files."""
    # Load mapping from file if provided
    mapping = {}
    if mapping_file and os.path.exists(mapping_file):
        with open(mapping_file, 'r') as f:
            mapping = json.load(f)
    
    doc_files = set()
    
    # Simple mapping logic (can be extended)
    for file_path in changed_files:
        if file_path.startswith('docs/'):
            # Already a doc file
            doc_files.add(file_path)
        elif file_path.endswith('.md') or file_path.endswith('.mdx'):
            # Markdown files might be docs
            doc_files.add(file_path)
        else:
            # Try to map source files to docs
            doc_path = source_to_doc_mapping(file_path, mapping)
            if doc_path:
                doc_files.add(doc_path)
    
    return list(doc_files)

def source_to_doc_mapping(source_file, custom_mapping=None):
    """Map source file to documentation file using patterns."""
    if custom_mapping and source_file in custom_mapping:
        return custom_mapping[source_file]
    
    # Default patterns
    patterns = [
        # Skills mapping
        ('skills/', 'docs/skills/'),
        ('src/skills/', 'docs/skills/'),
        
        # API mapping  
        ('src/api/', 'docs/api/'),
        ('packages/*/src/', 'docs/api/'),
        
        # Examples mapping
        ('examples/', 'docs/examples/'),
        
        # General source to guides
        ('src/', 'docs/guides/'),
        ('lib/', 'docs/guides/'),
    ]
    
    for src_pattern, doc_pattern in patterns:
        if src_pattern in source_file:
            # Replace source pattern with doc pattern
            doc_file = source_file.replace(src_pattern, doc_pattern)
            # Change extension to .md
            if not doc_file.endswith('.md'):
                doc_file = os.path.splitext(doc_file)[0] + '.md'
            return doc_file
    
    return None

def validate_docs(doc_files):
    """Validate documentation files for common issues."""
    issues = []
    
    for doc_file in doc_files:
        if not os.path.exists(doc_file):
            continue
            
        with open(doc_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for frontmatter
        if not content.startswith('---'):
            issues.append(f"{doc_file}: Missing frontmatter")
            continue
            
        # Parse frontmatter
        try:
            end_marker = content.find('\n---', 3)
            if end_marker == -1:
                issues.append(f"{doc_file}: Malformed frontmatter")
                continue
                
            frontmatter = content[3:end_marker]
            
            # Check required fields
            if 'title:' not in frontmatter:
                issues.append(f"{doc_file}: Missing title in frontmatter")
            if 'description:' not in frontmatter:
                issues.append(f"{doc_file}: Missing description in frontmatter")
                
        except Exception as e:
            issues.append(f"{doc_file}: Frontmatter parsing error: {e}")
    
    return issues

def main():
    parser = argparse.ArgumentParser(description="Update documentation based on code changes")
    parser.add_argument("--base-branch", default="main", help="Base branch to compare against")
    parser.add_argument("--mapping-file", help="JSON file with custom source-to-doc mappings")
    parser.add_argument("--validate-only", action="store_true", help="Only validate existing docs")
    parser.add_argument("--list-changes", action="store_true", help="List changed files only")
    
    args = parser.parse_args()
    
    if args.list_changes:
        changed_files = get_changed_files(args.base_branch)
        print("Changed files:")
        for f in changed_files:
            print(f"  {f}")
        return 0
    
    if args.validate_only:
        # Get all markdown files in docs directory
        docs_dir = Path("docs")
        if docs_dir.exists():
            doc_files = [str(f) for f in docs_dir.rglob("*.md")]
            doc_files.extend([str(f) for f in docs_dir.rglob("*.mdx")])
            issues = validate_docs(doc_files)
            if issues:
                print("Documentation validation issues:")
                for issue in issues:
                    print(f"  {issue}")
                return 1
            else:
                print("All documentation files validated successfully!")
                return 0
        else:
            print("No docs directory found")
            return 1
    
    # Main workflow
    changed_files = get_changed_files(args.base_branch)
    if not changed_files:
        print("No changes detected")
        return 0
    
    print(f"Detected {len(changed_files)} changed files")
    
    # Identify doc-relevant changes
    doc_relevant = identify_doc_relevant_changes(changed_files)
    if not doc_relevant:
        print("No documentation-relevant changes detected")
        return 0
    
    print(f"Found {len(doc_relevant)} documentation-relevant changes")
    
    # Map to documentation files
    doc_files = map_to_docs(doc_relevant, args.mapping_file)
    if not doc_files:
        print("No corresponding documentation files found")
        return 0
    
    print("Corresponding documentation files:")
    for doc_file in doc_files:
        print(f"  {doc_file}")
    
    # Validate documentation
    issues = validate_docs(doc_files)
    if issues:
        print("\nDocumentation validation issues:")
        for issue in issues:
            print(f"  {issue}")
        return 1
    
    print("\nDocumentation analysis complete!")
    print("Ready to update the following files:")
    for doc_file in doc_files:
        print(f"  {doc_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())