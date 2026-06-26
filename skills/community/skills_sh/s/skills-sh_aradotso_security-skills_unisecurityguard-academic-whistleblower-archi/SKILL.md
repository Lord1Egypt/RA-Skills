---
name: unisecurityguard-academic-whistleblower-archive
description: Archive and documentation platform for academic employment transparency and whistleblowing in Chinese higher education institutions
triggers:
  - how do I archive academic whistleblowing content
  - set up a backup platform for censored social media
  - document academic employment issues
  - preserve evidence of institutional misconduct
  - create a GitHub-based content archive
  - backup xiaohongshu or red book content
  - archive screenshots and testimonials safely
  - document academic career transparency
---

# UniSecurityGuard Academic Whistleblower Archive

> Skill by [ara.so](https://ara.so) — Security Skills collection.

## Overview

UniSecurityGuard is a GitHub-based archive platform documenting the experience of a Chinese academic who transitioned from associate professor to security guard. The project serves as a censorship-resistant backup for social media content that faces institutional pressure and platform removal. It demonstrates how to use GitHub as a transparent, immutable documentation platform for whistleblowing and advocacy.

**Key Use Case**: Preserving evidence of academic employment issues, institutional misconduct, and career transitions when primary platforms (Xiaohongshu/Little Red Book) are threatened with censorship.

**Primary Language**: Markdown (documentation-focused)

**Repository Structure**:
- README.md: Main narrative and updates
- assets/: Screenshots and image evidence
- Issues section: Community Q&A and documentation

## Installation & Setup

### Fork or Clone for Your Own Archive

```bash
# Clone the repository
git clone https://github.com/UniSecurityGuard/UniSecurityGuard.git
cd UniSecurityGuard

# Create your own backup archive (fork approach)
# 1. Fork via GitHub UI
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/YOUR_ARCHIVE_NAME.git
cd YOUR_ARCHIVE_NAME
```

### Initialize Your Own Archive

```bash
# Create basic structure
mkdir -p assets/{screenshots,documents,evidence}
touch README.md
touch TIMELINE.md
touch FAQ.md

# Initialize git
git init
git add .
git commit -m "Initial archive setup"

# Push to GitHub (create repo first on github.com)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_ARCHIVE.git
git branch -M main
git push -u origin main
```

## Core Patterns

### 1. Document Progressive Updates

The project uses the README.md as a chronological narrative with new updates at the top:

```markdown
# [Latest Update - Critical Situation]

## [Date]: Current Status

Description of latest developments...

## [Earlier Date]: Previous Situation

Earlier context...

## Background

Original story and context...
```

### 2. Asset Organization

Store evidence systematically:

```bash
assets/
├── screenshots/
│   ├── 1.jpg          # Numbered chronologically
│   ├── 2.jpg
│   └── 3.jpg
├── documents/
│   ├── contract.pdf
│   └── correspondence.pdf
└── evidence/
    ├── salary_records/
    └── institutional_communications/
```

### 3. Embed Images in README

```markdown
## Evidence Documentation

<img src="assets/screenshots/1.jpg" width="400" alt="Description of evidence">
<img src="assets/screenshots/2.jpg" width="400" alt="Context">
<img src="assets/screenshots/3.jpg" width="400" alt="Timeline proof">
```

### 4. Use Issues for FAQ and Community Support

The project uses 154+ issues as a documentation and Q&A system:

```markdown
# Create structured issues for common questions

Issue #1: "关于学校施压的详细情况" (Details about institutional pressure)
Issue #2: "如何保护自己在类似情况下" (How to protect yourself in similar situations)
Issue #3: "法律建议和资源" (Legal advice and resources)
```

## Real-World Implementation Examples

### Example 1: Creating a Censorship-Resistant Archive

```bash
#!/bin/bash
# backup_social_media.sh
# Automate archiving of social media content to GitHub

ARCHIVE_DIR="./archive/$(date +%Y-%m-%d)"
mkdir -p "$ARCHIVE_DIR"

# Download screenshots (manual or automated via APIs)
# Save to archive directory
cp ~/Downloads/xiaohongshu_screenshots/* "$ARCHIVE_DIR/"

# Create daily update
cat > "$ARCHIVE_DIR/update.md" << EOF
# Update: $(date +%Y-%m-%d)

## Status
- Platform status: [Active/Restricted/Removed]
- Follower count: [NUMBER]
- Content removed: [YES/NO]

## New Developments
[Description]

## Evidence
$(ls "$ARCHIVE_DIR"/*.jpg | sed 's/^/- /')
EOF

# Commit to git
git add "$ARCHIVE_DIR"
git commit -m "Archive update: $(date +%Y-%m-%d)"
git push origin main
```

### Example 2: Structured Timeline Documentation

Create `TIMELINE.md`:

```markdown
# Career Transition Timeline

## 2025-12-27: Repository Created
- Initial backup platform established
- 3 key screenshots archived
- Background story documented

## 2025-12: Institutional Pressure Begins
- 7 leaders visit rental apartment
- Demands to delete content and claim fiction
- Threats to reclaim salary and benefits

## 2025: Security Guard Transition
- Removed from associate professor position
- Transferred to campus security
- Salary: ¥4,000/month base + ¥800 security supplement
- Annual performance bonus: ¥6,000+

## Background: Academic Career
- Undergraduate: C9 university (华五)
- PhD: QS50 US university (withdrawn)
- Position: Associate professor at brother institution
```

### Example 3: README Template for Academic Whistleblowing

```markdown
# [Project Title]: Academic Employment Transparency

## ⚠️ Current Situation

[Latest critical update - always at top]

## Background

### Academic Credentials
- Undergraduate: [Institution]
- Graduate: [Institution]
- Position: [Title] at [Institution]

### Employment Transition
- Previous role: [Title], Salary: [Amount]
- Current role: [Title], Salary: [Amount]
- Reason for transition: [Description]

## Institutional Response

### Pressure Tactics
1. [Specific action]
2. [Specific threat]
3. [Specific demand]

### Evidence
<img src="assets/evidence_1.jpg" width="400" alt="Evidence description">

## Documentation Purpose

This repository serves as:
1. Immutable record of events
2. Backup for censored social media content
3. Resource for others in similar situations
4. Transparent accountability mechanism

## How to Support

- ⭐ Star this repository for visibility
- 📋 Open issues with questions or similar experiences
- 🔄 Share (carefully, considering safety)
- 📸 Screenshot and archive content locally
```

### Example 4: Automated Git Backup Script

```python
#!/usr/bin/env python3
# auto_archive.py - Automated content archiving

import os
import json
from datetime import datetime
import subprocess

class AcademicArchive:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.assets_dir = os.path.join(repo_path, 'assets')
        
    def add_update(self, title, content, evidence_files=None):
        """Add new update to README"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        update = f"\n# {title}\n\n"
        update += f"**Date**: {timestamp}\n\n"
        update += f"{content}\n\n"
        
        if evidence_files:
            update += "## Evidence\n\n"
            for f in evidence_files:
                # Copy evidence to assets
                dest = os.path.join(self.assets_dir, os.path.basename(f))
                subprocess.run(['cp', f, dest])
                update += f'<img src="assets/{os.path.basename(f)}" width="400" alt="">\n'
        
        # Prepend to README
        readme_path = os.path.join(self.repo_path, 'README.md')
        with open(readme_path, 'r') as f:
            existing = f.read()
        
        with open(readme_path, 'w') as f:
            f.write(update + existing)
        
        return update
    
    def commit_and_push(self, message):
        """Commit changes and push to GitHub"""
        os.chdir(self.repo_path)
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', message])
        subprocess.run(['git', 'push', 'origin', 'main'])
    
    def create_issue_faq(self, question, answer):
        """Create issue for FAQ (requires GitHub CLI)"""
        subprocess.run([
            'gh', 'issue', 'create',
            '--title', question,
            '--body', answer,
            '--label', 'faq'
        ])

# Usage example
archive = AcademicArchive('/path/to/UniSecurityGuard')

# Add update with evidence
archive.add_update(
    title="Latest Institutional Pressure",
    content="""
    School leadership removed the chair from security booth.
    Reason: "Security guards shouldn't sit - it doesn't look proper."
    Now standing 8 hours straight daily.
    """,
    evidence_files=[
        '/path/to/screenshots/booth_before.jpg',
        '/path/to/screenshots/booth_after.jpg'
    ]
)

archive.commit_and_push("Update: Security booth chair removed")
```

## Configuration & Best Practices

### Repository Settings

1. **Enable GitHub Pages** (optional, for web presence):
   - Settings → Pages → Source: main branch
   - Creates public website at `https://USERNAME.github.io/REPO`

2. **Issue Templates**:

Create `.github/ISSUE_TEMPLATE/faq.md`:

```markdown
---
name: FAQ Question
about: Ask questions about the situation
title: '[FAQ] '
labels: faq
---

## Question

[Your question]

## Context (if applicable)

[Additional context]
```

3. **Archive Metadata**:

Create `archive_metadata.json`:

```json
{
  "archive_name": "UniSecurityGuard",
  "primary_platform": "Xiaohongshu (Little Red Book)",
  "backup_date": "2025-12-27",
  "last_update": "2026-05-13",
  "status": "active",
  "content_type": "academic_whistleblowing",
  "language": "zh-CN",
  "evidence_count": 154,
  "follower_snapshot": {
    "platform": "xiaohongshu",
    "count": "unknown",
    "status": "threatened"
  }
}
```

### Safety Considerations

1. **Anonymization**: Remove or redact:
   - Personal identifying information of third parties
   - Specific institutional names (if legally required)
   - Location details that enable physical tracking

2. **Evidence Integrity**:
   ```bash
   # Generate checksums for evidence files
   sha256sum assets/**/*.jpg > assets/checksums.txt
   git add assets/checksums.txt
   git commit -m "Add evidence checksums for integrity verification"
   ```

3. **Backup Beyond GitHub**:
   ```bash
   # Create encrypted backup archive
   tar -czf archive_backup.tar.gz .
   gpg --symmetric --cipher-algo AES256 archive_backup.tar.gz
   # Store archive_backup.tar.gz.gpg in multiple locations
   ```

## Common Use Cases

### Migrating from Censored Platform

```markdown
## Platform Migration Notice

Due to [PLATFORM] censorship/removal, this content has migrated to GitHub.

**Original platform**: [NAME]
**Original account**: [HANDLE/ID]
**Migration date**: [DATE]
**Reason**: [Platform pressure/content removal/account suspension]

### How to Follow Updates
1. ⭐ Star this repository
2. 👁️ Watch → All Activity (for notifications)
3. Check back regularly or use RSS feed:
   `https://github.com/USERNAME/REPO/commits/main.atom`
```

### Community Support Hub

```markdown
## Support & Resources

### For Those in Similar Situations
- 📋 [FAQ Issues](https://github.com/USERNAME/REPO/issues?q=label%3Afaq)
- 💬 [Discussions](https://github.com/USERNAME/REPO/discussions)
- 📚 [Resource List](./RESOURCES.md)

### Legal & Safety Resources
- [Labor law consultation contacts]
- [Academic employment advocacy organizations]
- [Digital security guides]
```

## Troubleshooting

### Issue: Content Visibility

**Problem**: Updates not appearing to others

```bash
# Verify commits are pushed
git status
git log --oneline -5

# Force push if necessary (use cautiously)
git push --force origin main
```

### Issue: Large Files

**Problem**: Screenshots/documents exceed GitHub limits (100MB file, 1GB repo)

```bash
# Use Git LFS for large files
git lfs install
git lfs track "*.pdf"
git lfs track "*.mp4"
git add .gitattributes
git commit -m "Configure Git LFS"

# Or link to external storage
echo "Large evidence files: [External Archive Link]" >> README.md
```

### Issue: Institutional Takedown Requests

**GitHub provides**:
1. DMCA counter-notice process
2. Transparency reports for takedown requests
3. Archive repositories before potential removal

```bash
# Create redundant mirrors
git clone --mirror https://github.com/USERNAME/REPO.git
cd REPO.git
git push --mirror https://gitlab.com/USERNAME/REPO.git
git push --mirror https://codeberg.org/USERNAME/REPO.git
```

### Issue: Community Management

**High issue volume (154+ issues)**:

```bash
# Use labels effectively
gh label create "institutional-pressure" --color "d73a4a"
gh label create "legal-advice" --color "0075ca"
gh label create "career-advice" --color "008672"

# Bulk label issues
gh issue list --limit 100 --json number --jq '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "faq"
```

## Advanced Patterns

### Automated Monitoring

```python
# monitor_platform.py - Check if primary platform content is still accessible
import requests
import json
from datetime import datetime

def check_platform_status(platform_url):
    """Monitor if content is still accessible"""
    try:
        response = requests.get(platform_url, timeout=10)
        status = {
            'timestamp': datetime.now().isoformat(),
            'accessible': response.status_code == 200,
            'status_code': response.status_code
        }
    except Exception as e:
        status = {
            'timestamp': datetime.now().isoformat(),
            'accessible': False,
            'error': str(e)
        }
    
    # Log status
    with open('platform_status.jsonl', 'a') as f:
        f.write(json.dumps(status) + '\n')
    
    return status

# Run periodically via cron
# 0 */6 * * * /usr/bin/python3 /path/to/monitor_platform.py
```

### RSS Feed for Followers

GitHub automatically provides RSS feeds:

```
# Commits feed
https://github.com/USERNAME/REPO/commits/main.atom

# Issues feed  
https://github.com/USERNAME/REPO/issues.atom

# Share with followers
"Subscribe to updates: Add this URL to your RSS reader"
```

This skill enables AI agents to help users create censorship-resistant documentation platforms, archive evidence of institutional misconduct, and maintain transparency when facing content removal pressure.
