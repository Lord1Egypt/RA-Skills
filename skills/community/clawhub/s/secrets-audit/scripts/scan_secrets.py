#!/usr/bin/env python3
"""Scan project directories for exposed secrets, API keys, tokens, and credentials."""

import argparse
import json
import math
import os
import re
import subprocess
import sys
import time

# Directories to skip
SKIP_DIRS = {
    'node_modules', '.git', 'vendor', '.venv', 'venv', '__pycache__',
    '.tox', '.eggs', 'dist', 'build', '.next', '.nuxt', '.output',
    'coverage', '.nyc_output', '.pytest_cache', '.mypy_cache',
}

# File extensions to skip
SKIP_EXTENSIONS = {
    '.lock', '.min.js', '.min.css', '.map', '.woff', '.woff2', '.ttf',
    '.eot', '.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
    '.mp3', '.mp4', '.avi', '.mov', '.pdf', '.zip', '.tar', '.gz',
    '.bz2', '.7z', '.exe', '.dll', '.so', '.dylib', '.pyc', '.pyo',
    '.class', '.jar', '.war', '.ear',
}

# Skip specific filenames
SKIP_FILES = {
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'Cargo.lock',
    'Gemfile.lock', 'poetry.lock', 'composer.lock', 'go.sum',
}

# Secret patterns: (name, regex, severity, description)
SECRET_PATTERNS = [
    # AWS
    ('AWS Access Key ID', r'(?:^|["\'\s=:])(?:AKIA[0-9A-Z]{16})', 'HIGH', 'AWS access key'),
    ('AWS Secret Key', r'(?:aws_secret_access_key|aws_secret_key|secret_key)\s*[=:]\s*["\']?([A-Za-z0-9/+=]{40})', 'HIGH', 'AWS secret access key'),

    # GCP
    ('GCP API Key', r'AIza[0-9A-Za-z_-]{35}', 'HIGH', 'Google Cloud API key'),
    ('GCP Service Account', r'"type"\s*:\s*"service_account"', 'HIGH', 'GCP service account JSON'),

    # Azure
    ('Azure Storage Key', r'(?:AccountKey|account_key)\s*[=:]\s*["\']?([A-Za-z0-9+/=]{88})', 'HIGH', 'Azure storage account key'),

    # OpenAI
    ('OpenAI API Key', r'sk-[A-Za-z0-9]{20,}T3BlbkFJ[A-Za-z0-9]{20,}', 'HIGH', 'OpenAI API key'),
    ('OpenAI Key (new format)', r'sk-proj-[A-Za-z0-9_-]{40,}', 'HIGH', 'OpenAI project API key'),

    # Stripe
    ('Stripe Secret Key', r'sk_live_[0-9a-zA-Z]{24,}', 'HIGH', 'Stripe live secret key'),
    ('Stripe Publishable Key', r'pk_live_[0-9a-zA-Z]{24,}', 'MEDIUM', 'Stripe live publishable key'),

    # GitHub
    ('GitHub Token', r'gh[pousr]_[A-Za-z0-9_]{36,}', 'HIGH', 'GitHub personal access token'),
    ('GitHub OAuth', r'gho_[A-Za-z0-9]{36}', 'HIGH', 'GitHub OAuth token'),

    # Generic tokens/keys
    ('Private Key', r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----', 'HIGH', 'Private key file'),
    ('JWT Secret', r'(?:jwt_secret|JWT_SECRET|jwt_key|JWT_KEY)\s*[=:]\s*["\']?([^\s"\']{8,})', 'HIGH', 'JWT signing secret'),

    # Database
    ('Database URL', r'(?:postgres|mysql|mongodb|redis|amqp)://[^\s"\']+:[^\s"\']+@[^\s"\']+', 'HIGH', 'Database connection string with credentials'),
    ('DB Password', r'(?:DB_PASSWORD|DATABASE_PASSWORD|MYSQL_PASSWORD|POSTGRES_PASSWORD|MONGO_PASSWORD)\s*[=:]\s*["\']?([^\s"\']{4,})', 'HIGH', 'Database password'),

    # Generic secrets
    ('Password Assignment', r'(?:password|passwd|pwd)\s*[=:]\s*["\']([^"\']{4,})["\']', 'HIGH', 'Hardcoded password'),
    ('Secret Key Assignment', r'(?:secret_key|SECRET_KEY|api_secret|API_SECRET)\s*[=:]\s*["\']?([^\s"\']{8,})', 'HIGH', 'Hardcoded secret key'),
    ('API Key Assignment', r'(?:api_key|API_KEY|apikey|APIKEY)\s*[=:]\s*["\']?([A-Za-z0-9_-]{16,})', 'MEDIUM', 'Potential API key'),

    # Auth URLs
    ('URL with Credentials', r'https?://[^\s:]+:[^\s@]+@[^\s"\']+', 'HIGH', 'URL with embedded credentials'),

    # Webhook
    ('Slack Webhook', r'https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+', 'HIGH', 'Slack webhook URL'),
    ('Discord Webhook', r'https://discord(?:app)?\.com/api/webhooks/\d+/[A-Za-z0-9_-]+', 'HIGH', 'Discord webhook URL'),

    # Telegram
    ('Telegram Bot Token', r'\d{8,10}:[A-Za-z0-9_-]{35}', 'HIGH', 'Telegram bot token'),

    # SendGrid
    ('SendGrid API Key', r'SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}', 'HIGH', 'SendGrid API key'),

    # Twilio
    ('Twilio API Key', r'SK[0-9a-fA-F]{32}', 'MEDIUM', 'Twilio API key'),

    # Mailgun
    ('Mailgun API Key', r'key-[0-9a-zA-Z]{32}', 'HIGH', 'Mailgun API key'),

    # Heroku
    ('Heroku API Key', r'(?:heroku_api_key|HEROKU_API_KEY)\s*[=:]\s*["\']?([0-9a-fA-F-]{36})', 'HIGH', 'Heroku API key'),

    # .env populated secrets
    ('Env Secret', r'^[A-Z_]+(?:SECRET|TOKEN|KEY|PASSWORD|PASS|PWD|AUTH|CREDENTIAL|API_KEY)\s*=\s*[^\s$]{4,}', 'MEDIUM', 'Populated secret in env file'),

    # TODO/FIXME about secrets
    ('Secret TODO', r'(?:TODO|FIXME|HACK|XXX).*(?:secret|password|key|token|credential)', 'LOW', 'TODO mentioning secrets'),

    # Placeholder credentials
    ('Placeholder Creds', r'(?:admin|root|test|user)(?:/|:)(?:admin|root|test|password|pass|123)', 'LOW', 'Placeholder/default credentials'),
]


def calculate_entropy(s):
    """Calculate Shannon entropy of a string."""
    if not s:
        return 0
    entropy = 0
    length = len(s)
    seen = set(s)
    for char in seen:
        freq = s.count(char) / length
        if freq > 0:
            entropy -= freq * math.log2(freq)
    return entropy


def is_binary_file(filepath):
    """Check if a file is binary."""
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(8192)
        return b'\x00' in chunk
    except (IOError, OSError):
        return True


def should_skip(filepath, root, allowed_extensions=None):
    """Determine if a file should be skipped."""
    basename = os.path.basename(filepath)
    _, ext = os.path.splitext(basename)

    if basename in SKIP_FILES:
        return True
    if ext.lower() in SKIP_EXTENSIONS:
        return True
    if allowed_extensions and ext.lower() not in allowed_extensions:
        return True

    # Check directory components
    rel_path = os.path.relpath(filepath, root)
    parts = rel_path.split(os.sep)
    for part in parts:
        if part in SKIP_DIRS:
            return True

    return False


def scan_file(filepath, patterns):
    """Scan a single file for secret patterns."""
    findings = []

    if is_binary_file(filepath):
        return findings

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except (IOError, OSError):
        return findings

    for line_num, line in enumerate(lines, 1):
        line_stripped = line.strip()

        # Skip comments that look like documentation/examples
        if line_stripped.startswith('#') and ('example' in line_stripped.lower() or 'sample' in line_stripped.lower()):
            continue

        for name, pattern, severity, description in patterns:
            matches = re.finditer(pattern, line_stripped, re.IGNORECASE)
            for match in matches:
                # Get matched value
                matched_text = match.group(1) if match.lastindex else match.group(0)

                # Skip very short matches for generic patterns
                if severity == 'MEDIUM' and len(matched_text) < 8:
                    continue

                # Check entropy for potential false positives on generic patterns
                if 'Assignment' in name or 'Env Secret' in name:
                    clean = re.sub(r'[=:\s"\']', '', matched_text)
                    if len(clean) > 4 and calculate_entropy(clean) < 2.5:
                        continue  # Low entropy = likely not a real secret

                # Build context (surrounding lines)
                context_start = max(0, line_num - 2)
                context_end = min(len(lines), line_num + 1)
                context_lines = lines[context_start:context_end]
                context = ''.join(context_lines).strip()

                findings.append({
                    'name': name,
                    'severity': severity,
                    'description': description,
                    'file': filepath,
                    'line': line_num,
                    'match': matched_text[:60] + ('...' if len(matched_text) > 60 else ''),
                    'context': context[:200],
                })
                break  # One finding per pattern per line

    return findings


def scan_git_history(project_path):
    """Scan git history for previously committed secrets."""
    findings = []
    try:
        result = subprocess.run(
            ['git', '-C', project_path, 'log', '--diff-filter=D', '--name-only', '--pretty=format:'],
            capture_output=True, text=True, timeout=30
        )
        deleted_files = [f for f in result.stdout.split('\n') if f.strip()]

        # Check for sensitive deleted files
        sensitive_patterns = ['.env', 'credentials', 'secret', '.pem', '.key', 'id_rsa']
        for f in deleted_files:
            for pattern in sensitive_patterns:
                if pattern in f.lower():
                    findings.append({
                        'name': 'Deleted Sensitive File',
                        'severity': 'MEDIUM',
                        'description': f'Previously committed file may contain secrets (still in git history)',
                        'file': f,
                        'line': 0,
                        'match': f'Deleted file: {f}',
                        'context': 'File was deleted but still exists in git history. Secrets may need rotation.',
                    })
                    break

        # Check commit messages for secret-related keywords
        result = subprocess.run(
            ['git', '-C', project_path, 'log', '--oneline', '-50', '--all'],
            capture_output=True, text=True, timeout=30
        )
        for line in result.stdout.split('\n'):
            if any(kw in line.lower() for kw in ['remove secret', 'remove password', 'remove key', 'remove token', 'oops', 'accidentally']):
                findings.append({
                    'name': 'Suspicious Commit Message',
                    'severity': 'LOW',
                    'description': 'Commit message suggests secrets may have been removed',
                    'file': 'git history',
                    'line': 0,
                    'match': line.strip()[:80],
                    'context': 'Review this commit for previously exposed secrets.',
                })

    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return findings


def format_text_report(findings, project_path, files_scanned, files_skipped, elapsed):
    """Format findings as human-readable text report."""
    lines = []
    lines.append('=== Secrets Audit Report ===')
    lines.append(f'Project: {project_path}')
    lines.append(f'Scanned: {files_scanned} files | Skipped: {files_skipped} files')
    lines.append(f'Time: {elapsed:.1f}s')
    lines.append('')

    for severity in ['HIGH', 'MEDIUM', 'LOW']:
        sev_findings = [f for f in findings if f['severity'] == severity]
        if not sev_findings:
            continue

        lines.append(f'--- {severity} SEVERITY ({len(sev_findings)} findings) ---')
        lines.append('')

        for i, finding in enumerate(sev_findings, 1):
            prefix = severity[0]
            lines.append(f'[{prefix}{i}] {finding["name"]}')
            if finding['line'] > 0:
                rel_path = os.path.relpath(finding['file'], project_path)
                lines.append(f'  File: {rel_path}:{finding["line"]}')
            else:
                lines.append(f'  File: {finding["file"]}')
            lines.append(f'  Match: {finding["match"]}')
            lines.append(f'  {finding["description"]}')
            lines.append('')

    # Summary
    high = len([f for f in findings if f['severity'] == 'HIGH'])
    medium = len([f for f in findings if f['severity'] == 'MEDIUM'])
    low = len([f for f in findings if f['severity'] == 'LOW'])

    lines.append('--- SUMMARY ---')
    lines.append(f'High: {high} | Medium: {medium} | Low: {low} | Total: {len(findings)}')

    if high > 0:
        lines.append('Recommendation: Rotate all HIGH severity credentials immediately')
    elif medium > 0:
        lines.append('Recommendation: Review MEDIUM severity findings and remediate')
    else:
        lines.append('Status: No critical secrets detected')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Scan projects for exposed secrets and credentials')
    parser.add_argument('path', help='Project directory to scan')
    parser.add_argument('--git-history', action='store_true', help='Also scan git history')
    parser.add_argument('--extensions', help='Only scan specific extensions (comma-separated, e.g. .py,.js,.env)')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--output', '-o', help='Output file path')
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f'Error: {args.path} is not a directory', file=sys.stderr)
        sys.exit(1)

    project_path = os.path.abspath(args.path)
    allowed_extensions = None
    if args.extensions:
        allowed_extensions = set(ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions.split(','))

    start_time = time.time()
    all_findings = []
    files_scanned = 0
    files_skipped = 0

    # Walk the directory tree
    for root, dirs, files in os.walk(project_path):
        # Skip directories in-place
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            filepath = os.path.join(root, filename)

            if should_skip(filepath, project_path, allowed_extensions):
                files_skipped += 1
                continue

            files_scanned += 1
            findings = scan_file(filepath, SECRET_PATTERNS)
            all_findings.extend(findings)

    # Git history scan
    if args.git_history:
        git_findings = scan_git_history(project_path)
        all_findings.extend(git_findings)

    # Deduplicate
    seen = set()
    unique_findings = []
    for f in all_findings:
        key = (f['name'], f['file'], f['line'])
        if key not in seen:
            seen.add(key)
            unique_findings.append(f)

    elapsed = time.time() - start_time

    # Output
    if args.format == 'json':
        output = json.dumps({
            'project': project_path,
            'files_scanned': files_scanned,
            'files_skipped': files_skipped,
            'elapsed_seconds': round(elapsed, 1),
            'findings': unique_findings,
            'summary': {
                'high': len([f for f in unique_findings if f['severity'] == 'HIGH']),
                'medium': len([f for f in unique_findings if f['severity'] == 'MEDIUM']),
                'low': len([f for f in unique_findings if f['severity'] == 'LOW']),
                'total': len(unique_findings),
            }
        }, indent=2)
    else:
        output = format_text_report(unique_findings, project_path, files_scanned, files_skipped, elapsed)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'Report written to {args.output}')
    else:
        print(output)

    # Exit code for CI
    high_count = len([f for f in unique_findings if f['severity'] == 'HIGH'])
    if high_count > 0:
        sys.exit(2)
    elif unique_findings:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
