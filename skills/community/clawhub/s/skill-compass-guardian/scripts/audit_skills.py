#!/usr/bin/env python3
"""
Skill Compass - Audit Script
Scans skill directories for triggering issues and outputs a diagnostic report.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# YAML frontmatter pattern
FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
NAME_RE = re.compile(r'^name:\s*(.+)$', re.MULTILINE)
DESC_RE = re.compile(r'^description:\s*(.+?)(?=\n[a-z_]+:|\n---|\Z)', re.MULTILINE | re.DOTALL)

# Trigger phrase indicators
TRIGGER_PHRASES = [
    "use when", "invoke when", "always invoke", "use for", "trigger",
    "activate when", "run when", "always use", "do not use for",
    "do not use when", "not for"
]

# Directive language indicators
DIRECTIVE_WORDS = [
    "always", "must", "never", "do not", "ensure", "require",
    "invoke", "activate", "trigger", "load this"
]

# Vague/non-triggering language
WEAK_PHRASES = [
    "helps with", "this skill provides", "this skill is for",
    "can be used", "supports", "enables", "allows you to"
]

# Common skill directories to check
DEFAULT_SKILL_DIRS = [
    os.path.expanduser("~/.openclaw/skills"),
    os.path.expanduser("~/.openclaw/workspace/skills"),
    os.path.expanduser("~/.agents/skills"),
    os.path.expanduser("~/.openclaw/.agents/skills"),
]

# Token budget threshold (chars)
TOKEN_BUDGET_WARN = 20000
TOKEN_BUDGET_CRITICAL = 30000

# Description length thresholds
DESC_MIN_CHARS = 30
DESC_MAX_CHARS = 350  # ideal is <150 for core trigger, but total can be longer


def parse_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """Extract YAML frontmatter from SKILL.md content."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, content
    
    fm_text = match.group(1)
    body = content[match.end():]
    
    # Parse name
    name_match = NAME_RE.search(fm_text)
    name = name_match.group(1).strip().strip('"\'') if name_match else None
    
    # Parse description (may span multiple lines until next key or ---)
    desc_match = DESC_RE.search(fm_text)
    desc = desc_match.group(1).strip().strip('"\'') if desc_match else None
    
    # Check for unquoted colons in description
    colon_issue = False
    if desc:
        # Re-check raw line for unquoted colon issues
        for line in fm_text.split('\n'):
            if line.strip().startswith('description:'):
                val = line.split('description:', 1)[1].strip()
                if ':' in val and not (val.startswith('"') or val.startswith("'")):
                    colon_issue = True
                break
    
    return {
        'name': name,
        'description': desc,
        'colon_issue': colon_issue,
        'raw_frontmatter': fm_text,
    }, body


def score_description(desc: str, name: str) -> Dict:
    """Score a description for trigger quality. Returns score (0-100) and issues."""
    if not desc:
        return {
            'score': 0,
            'issues': ['CRITICAL: No description found'],
            'suggestions': ['Add a description with trigger conditions']
        }
    
    issues = []
    suggestions = []
    score = 100
    desc_lower = desc.lower()
    
    # Check length
    if len(desc) < DESC_MIN_CHARS:
        score -= 30
        issues.append(f'SHORT: Description is only {len(desc)} chars (min {DESC_MIN_CHARS})')
        suggestions.append('Expand to include specific trigger conditions and keywords')
    
    if len(desc) > DESC_MAX_CHARS:
        score -= 15
        issues.append(f'LONG: Description is {len(desc)} chars (max {DESC_MAX_CHARS})')
        suggestions.append('Move detail to SKILL.md body, keep frontmatter concise')
    
    # Check for trigger phrases
    has_trigger = any(p in desc_lower for p in TRIGGER_PHRASES)
    if not has_trigger:
        score -= 35
        issues.append('NO_TRIGGER: Missing trigger condition (no "Use when..." or similar)')
        suggestions.append('Add trigger phrases: "Use when...", "Invoke when...", "ALWAYS use for..."')
    
    # Check for weak language
    has_weak = any(p in desc_lower for p in WEAK_PHRASES)
    if has_weak:
        score -= 15
        issues.append('WEAK_LANG: Uses passive language instead of directive')
        suggestions.append('Replace "Helps with..." with "ALWAYS invoke when..."')
    
    # Check for directive language
    has_directive = any(w in desc_lower for w in DIRECTIVE_WORDS)
    if has_directive:
        score += 5  # bonus, capped at 100
    
    # Check for negative constraints
    has_negative = any(p in desc_lower for p in ['do not use', 'not for', 'do not invoke'])
    if not has_negative:
        score -= 5
        suggestions.append('Consider adding "Do NOT use for..." to prevent false triggers')
    
    # Check for keywords/trigger vocabulary
    word_count = len(desc.split())
    if word_count < 10:
        score -= 10
        issues.append('FEW_KEYWORDS: Description too short for good keyword matching')
    
    score = max(0, min(100, score))
    
    return {
        'score': score,
        'issues': issues,
        'suggestions': suggestions,
    }


def find_skill_dirs(search_paths: List[str]) -> List[Path]:
    """Find all skill directories containing SKILL.md files."""
    skill_files = []
    for base in search_paths:
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            # Skip hidden directories and node_modules
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
            if 'SKILL.md' in files:
                skill_files.append(Path(root) / 'SKILL.md')
    return skill_files


def detect_conflicts(skills: List[Dict]) -> List[Dict]:
    """Detect description conflicts/overlaps between skills."""
    conflicts = []
    
    for i, s1 in enumerate(skills):
        for s2 in skills[i+1:]:
            if not s1.get('description') or not s2.get('description'):
                continue
            
            d1 = set(s1['description'].lower().split())
            d2 = set(s2['description'].lower().split())
            
            if not d1 or not d2:
                continue
            
            # Jaccard similarity
            overlap = len(d1 & d2) / len(d1 | d2)
            
            if overlap > 0.4:
                conflicts.append({
                    'skill_a': s1.get('name', 'unknown'),
                    'skill_b': s2.get('name', 'unknown'),
                    'overlap': f'{overlap:.0%}',
                    'shared_keywords': sorted(d1 & d2)[:10],
                    'severity': 'HIGH' if overlap > 0.6 else 'MEDIUM',
                    'suggestion': f'Add negative constraints to distinguish {s1.get("name")} from {s2.get("name")}',
                })
    
    return conflicts


def audit_skills(skills_dir: str, auto_fix: bool = False) -> Dict:
    """Audit all skills in a directory."""
    report = {
        'skills_dir': skills_dir,
        'total_skills': 0,
        'issues_found': 0,
        'skills': [],
        'conflicts': [],
        'token_budget': {'total_chars': 0, 'status': 'OK'},
        'summary': {},
    }
    
    # Find skill files
    if os.path.isdir(skills_dir):
        search_paths = [skills_dir]
    else:
        search_paths = DEFAULT_SKILL_DIRS
    
    skill_files = find_skill_dirs(search_paths)
    report['total_skills'] = len(skill_files)
    
    if not skill_files:
        report['error'] = f'No SKILL.md files found in {search_paths}'
        return report
    
    total_desc_chars = 0
    
    for sf in skill_files:
        try:
            content = sf.read_text(encoding='utf-8')
        except Exception as e:
            report['skills'].append({
                'path': str(sf),
                'error': f'Cannot read file: {e}',
                'score': 0,
            })
            report['issues_found'] += 1
            continue
        
        fm, body = parse_frontmatter(content)
        
        if fm is None:
            report['skills'].append({
                'path': str(sf),
                'error': 'No YAML frontmatter found',
                'score': 0,
                'issues': ['CRITICAL: Missing YAML frontmatter (--- ... ---)'],
                'suggestions': ['Add frontmatter with name: and description: fields'],
            })
            report['issues_found'] += 1
            continue
        
        skill_info = {
            'path': str(sf),
            'name': fm['name'] or 'MISSING',
            'description_length': len(fm['description'] or ''),
        }
        
        if fm['colon_issue']:
            skill_info['issues'] = ['YAML: Colon in description may break parsing']
            skill_info['auto_fix'] = 'Wrap description in quotes'
            report['issues_found'] += 1
            
            if auto_fix:
                fixed = auto_fix_colon(content)
                if fixed:
                    sf.write_text(fixed)
                    skill_info['fixed'] = True
        
        score_result = score_description(fm['description'] or '', fm['name'] or '')
        skill_info.update(score_result)
        
        if score_result['issues']:
            report['issues_found'] += len(score_result['issues'])
        
        if fm['description']:
            total_desc_chars += len(fm['description'])
        
        report['skills'].append(skill_info)
    
    # Token budget analysis
    report['token_budget']['total_chars'] = total_desc_chars
    if total_desc_chars > TOKEN_BUDGET_CRITICAL:
        report['token_budget']['status'] = 'CRITICAL'
        report['token_budget']['message'] = f'{total_desc_chars} chars exceeds critical threshold. Skills may be silently dropped.'
    elif total_desc_chars > TOKEN_BUDGET_WARN:
        report['token_budget']['status'] = 'WARNING'
        report['token_budget']['message'] = f'{total_desc_chars} chars approaching budget limit.'
    
    # Conflict detection
    report['conflicts'] = detect_conflicts(report['skills'])
    
    # Summary
    scores = [s.get('score', 0) for s in report['skills']]
    report['summary'] = {
        'avg_score': sum(scores) / len(scores) if scores else 0,
        'passing': sum(1 for s in scores if s >= 70),
        'failing': sum(1 for s in scores if s < 70),
        'critical': sum(1 for s in scores if s < 30),
    }
    
    return report


def auto_fix_colon(content: str) -> Optional[str]:
    """Fix unquoted colons in YAML description field."""
    lines = content.split('\n')
    fixed = False
    for i, line in enumerate(lines):
        if line.strip().startswith('description:'):
            val = line.split('description:', 1)[1].strip()
            if ':' in val and not val.startswith('"') and not val.startswith("'"):
                lines[i] = f'description: "{val}"'
                fixed = True
            break
    return '\n'.join(lines) if fixed else None


def print_report(report: Dict, json_output: bool = False):
    """Print the audit report."""
    if json_output:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return
    
    print("=" * 70)
    print("🛡️  SKILL SENTINEL — AUDIT REPORT")
    print("=" * 70)
    print(f"\n📂 Directory: {report['skills_dir']}")
    print(f"📊 Total skills: {report['total_skills']}")
    print(f"⚠️  Issues found: {report['issues_found']}")
    
    if report.get('error'):
        print(f"\n❌ {report['error']}")
        return
    
    # Summary
    s = report['summary']
    print(f"\n📈 Score Summary:")
    print(f"   Average score: {s.get('avg_score', 0):.0f}/100")
    print(f"   ✅ Passing (≥70): {s.get('passing', 0)}")
    print(f"   ⚠️  Needs work (<70): {s.get('failing', 0)}")
    print(f"   🔴 Critical (<30): {s.get('critical', 0)}")
    
    # Token budget
    tb = report['token_budget']
    status_emoji = {'OK': '✅', 'WARNING': '⚠️ ', 'CRITICAL': '🔴'}.get(tb['status'], '❓')
    print(f"\n🪙  Token Budget: {status_emoji} {tb['total_chars']} chars ({tb['status']})")
    if tb.get('message'):
        print(f"   {tb['message']}")
    
    # Per-skill details
    print(f"\n{'─'*70}")
    print("SKILL DETAILS:")
    print(f"{'─'*70}")
    
    for skill in sorted(report['skills'], key=lambda x: x.get('score', 0)):
        score = skill.get('score', 0)
        name = skill.get('name', 'unknown')
        emoji = '✅' if score >= 70 else '⚠️ ' if score >= 30 else '🔴'
        
        print(f"\n{emoji} {name} — Score: {score}/100")
        print(f"   Path: {skill['path']}")
        
        if skill.get('error'):
            print(f"   ❌ Error: {skill['error']}")
        
        for issue in skill.get('issues', []):
            print(f"   • {issue}")
        
        for sug in skill.get('suggestions', []):
            print(f"   💡 {sug}")
        
        if skill.get('fixed'):
            print(f"   🔧 Auto-fixed!")
    
    # Conflicts
    if report['conflicts']:
        print(f"\n{'─'*70}")
        print(f"⚡ CONFLICTS DETECTED: {len(report['conflicts'])}")
        print(f"{'─'*70}")
        for c in report['conflicts']:
            emoji = '🔴' if c['severity'] == 'HIGH' else '⚠️ '
            print(f"\n{emoji} {c['skill_a']} ↔ {c['skill_b']} ({c['overlap']} overlap)")
            print(f"   Shared: {', '.join(c['shared_keywords'][:5])}")
            print(f"   💡 {c['suggestion']}")
    
    print(f"\n{'='*70}")
    print("Audit complete. Fix issues above to improve skill trigger reliability.")
    print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(description='Skill Compass - Audit skill triggering issues')
    parser.add_argument('--skills-dir', default=None,
                        help='Path to skills directory (auto-detected if omitted)')
    parser.add_argument('--json', action='store_true',
                        help='Output JSON report')
    parser.add_argument('--fix', action='store_true',
                        help='Auto-fix common issues (YAML colons, etc.)')
    
    args = parser.parse_args()
    
    # Determine skills directory
    if args.skills_dir:
        skills_dir = args.skills_dir
    else:
        # Auto-detect: use first existing default dir
        skills_dir = next((d for d in DEFAULT_SKILL_DIRS if os.path.isdir(d)), DEFAULT_SKILL_DIRS[0])
    
    report = audit_skills(skills_dir, auto_fix=args.fix)
    print_report(report, json_output=args.json)


if __name__ == '__main__':
    main()
