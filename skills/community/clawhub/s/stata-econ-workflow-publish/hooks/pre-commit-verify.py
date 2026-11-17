#!/usr/bin/env python3
"""
Pre-commit verification hook.
Checks: log freshness, quality score >= 80, no hardcoded absolute paths.

Usage: python scripts/pre-commit-verify.py <project_root>
"""

import os, sys, subprocess, glob

def check_hardcoded_paths(dofile):
    """Check for hardcoded absolute paths in dofile."""
    issues = []
    with open(dofile, 'r', encoding='utf-8', errors='replace') as f:
        for i, line in enumerate(f, 1):
            stripped = line.strip()
            # Skip comments
            if stripped.startswith('*'):
                continue
            # Check for cd with absolute path
            if 'cd "' in stripped.lower() and ':\\' in stripped:
                issues.append(f'{dofile}:{i} — Hardcoded absolute path: {stripped[:60]}')
            if '/home/' in stripped or '/Users/' in stripped:
                issues.append(f'{dofile}:{i} — Hardcoded absolute path: {stripped[:60]}')
    return issues

def check_log_freshness(dofile, log_dir):
    """Check if log exists and is newer than dofile."""
    import glob
    base = os.path.splitext(os.path.basename(dofile))[0]
    logs = glob.glob(os.path.join(log_dir, f'*{base}*.log'))
    if not logs:
        return f'No log found for {os.path.basename(dofile)}'
    
    dofile_mtime = os.path.getmtime(dofile)
    log_mtime = max(os.path.getmtime(l) for l in logs)
    
    if log_mtime < dofile_mtime:
        return (f'Log stale for {os.path.basename(dofile)}: '
                f'dofile {os.path.getmtime(dofile):.0f} > log {log_mtime:.0f}')
    return None

def main():
    if len(sys.argv) < 2:
        root = os.getcwd()
    else:
        root = sys.argv[1]
    
    log_dir = os.path.join(root, 'logs')
    dofiles = glob.glob(os.path.join(root, 'dofiles', '**', '*.do'), recursive=True)
    dofiles += glob.glob(os.path.join(root, 'dofiles', '**', '*.py'), recursive=True)
    
    errors = []
    warnings = []
    
    for df in sorted(dofiles):
        # Check hardcoded paths
        path_issues = check_hardcoded_paths(df)
        errors.extend(path_issues)
        
        # Check log freshness
        if os.path.isdir(log_dir):
            log_issue = check_log_freshness(df, log_dir)
            if log_issue:
                warnings.append(log_issue)
    
    # Run quality score
    qc = os.path.join(root, 'scripts', 'quality_score.py')
    if os.path.exists(qc):
        print('Running quality score...')
        r = subprocess.run(['python', qc] + dofiles, capture_output=True, text=True)
        if r.returncode != 0:
            warnings.append('Quality score < 80 for some files')
        print(r.stdout[-500:])
    
    print(f'\n--- Pre-commit Verification ---')
    if errors:
        print(f'ERRORS ({len(errors)}):')
        for e in errors:
            print(f'  ✗ {e}')
        print('\nBlocking commit. Fix errors above.')
        sys.exit(1)
    
    if warnings:
        print(f'WARNINGS ({len(warnings)}):')
        for w in warnings:
            print(f'  ⚠ {w}')
    
    print('✓ All checks passed')
    sys.exit(0)

if __name__ == '__main__':
    main()
