---
name: developer-marketing-jobs-board
description: Daily-updated job board for DevRel, developer marketing, technical writing, and community roles at devtool companies
triggers:
  - find developer relations jobs
  - search for devrel positions
  - look up developer advocate openings
  - show me technical writing jobs
  - find developer marketing roles
  - search for community manager positions
  - check the latest devrel job listings
  - find jobs in developer experience
---

# Developer Marketing Jobs Board

> Skill by [ara.so](https://ara.so) — Marketing Skills collection.

This project is a curated, daily-updated job board featuring Developer Advocate, DevRel, technical writing, developer marketing, community, and documentation roles at devtool companies. Jobs are pulled directly from company ATS feeds every night via GitHub Actions, eliminating aggregator noise and reposts.

## What It Does

- **Automated Job Aggregation**: Pulls jobs nightly from company career pages using their ATS feeds
- **Categorized Listings**: Organizes jobs into DevRel, Technical Writing, Community, and Documentation categories
- **No Signup Required**: All job listings are publicly accessible via GitHub
- **Direct Application Links**: Each listing links directly to the company's application page
- **Company Coverage**: Tracks roles from major devtool companies like MongoDB, Stripe, Discord, Elastic, GitLab, and more

## Installation & Access

This is a web-based resource hosted on GitHub. No installation required.

### Viewing Job Listings

```bash
# Clone the repository to browse locally
git clone https://github.com/Infrasity-Labs/developer-marketing-jobs.git
cd developer-marketing-jobs

# Open the README.md to view current listings
cat README.md
```

### Direct Access

Visit the GitHub repository directly: `https://github.com/Infrasity-Labs/developer-marketing-jobs`

## Project Structure

```
developer-marketing-jobs/
├── README.md              # Main job listings (updated daily)
├── .github/
│   ├── workflows/         # GitHub Actions for automation
│   └── assets/            # Images and branding
└── scripts/               # Job aggregation scripts (if present)
```

## Key Features

### Job Categories

The board tracks four main categories:

1. **Developer Advocate / DevRel**: Developer advocacy, evangelism, and relations roles
2. **Technical Writing**: Documentation, content, and technical communication
3. **Community**: Community management and engagement
4. **Documentation**: Docs engineering and information architecture

### Job Listing Format

Each job entry includes:
- **Role Title**: Position name
- **Company**: Hiring organization
- **Location**: Office location or remote status
- **Apply Link**: Direct link to application

Example from README:

```markdown
| Role | Company | Location | Apply |
|------|---------|----------|-------|
| Senior Developer Advocate | MongoDB | Austin; United States | [→](https://www.mongodb.com/careers/job/?gh_jid=7571308) |
```

## Using This Resource

### For Job Seekers

**Filter by Location**:
```bash
# Search for remote positions
grep -i "remote" README.md | grep "Developer Advocate"

# Find jobs in specific cities
grep -i "san francisco" README.md
```

**Filter by Company**:
```bash
# Find all jobs at a specific company
grep -i "mongodb" README.md

# Count openings per company
grep -oP '\| \K[^|]+(?= \|)' README.md | sort | uniq -c | sort -rn
```

**Export to CSV**:
```bash
# Extract job data (requires sed/awk)
cat README.md | grep "^|" | grep -v "Role" | grep -v "^|---" > jobs.txt
```

### For Automating Job Searches

**Check for New Jobs Daily**:
```bash
#!/bin/bash
# save as check_new_jobs.sh

REPO_URL="https://raw.githubusercontent.com/Infrasity-Labs/developer-marketing-jobs/main/README.md"
KEYWORD="Senior Developer Advocate"

curl -s "$REPO_URL" | grep -i "$KEYWORD" > matching_jobs.txt

if [ -s matching_jobs.txt ]; then
  echo "Found matching jobs:"
  cat matching_jobs.txt
else
  echo "No new jobs matching criteria"
fi
```

**Monitor with GitHub Actions** (in your own repo):
```yaml
# .github/workflows/job-monitor.yml
name: Monitor DevRel Jobs

on:
  schedule:
    - cron: '0 9 * * *'  # Daily at 9 AM
  workflow_dispatch:

jobs:
  check-jobs:
    runs-on: ubuntu-latest
    steps:
      - name: Fetch latest jobs
        run: |
          curl -s https://raw.githubusercontent.com/Infrasity-Labs/developer-marketing-jobs/main/README.md \
            | grep -A 100 "Developer Advocate" \
            | grep "Remote" > new_jobs.txt
          
      - name: Notify if jobs found
        if: success()
        run: |
          if [ -s new_jobs.txt ]; then
            echo "New remote DevRel jobs found!"
            cat new_jobs.txt
          fi
```

### For Integrations

**Parse Job Data in Python**:
```python
import requests
import re
from typing import List, Dict

def fetch_devrel_jobs() -> List[Dict[str, str]]:
    """Fetch and parse DevRel jobs from the board."""
    url = "https://raw.githubusercontent.com/Infrasity-Labs/developer-marketing-jobs/main/README.md"
    response = requests.get(url)
    content = response.text
    
    jobs = []
    in_devrel_section = False
    
    for line in content.split('\n'):
        if '## 🎤 Developer Advocate' in line:
            in_devrel_section = True
            continue
        
        if in_devrel_section and line.startswith('## '):
            break
            
        if in_devrel_section and line.startswith('|') and 'Role' not in line and '---' not in line:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) == 4:
                jobs.append({
                    'role': parts[0],
                    'company': parts[1],
                    'location': parts[2],
                    'apply_url': re.search(r'\((.*?)\)', parts[3]).group(1) if '(' in parts[3] else ''
                })
    
    return jobs

# Usage
jobs = fetch_devrel_jobs()
for job in jobs:
    if 'remote' in job['location'].lower():
        print(f"{job['role']} at {job['company']} - {job['apply_url']}")
```

**Node.js Parser**:
```javascript
const axios = require('axios');

async function fetchDevRelJobs() {
  const url = 'https://raw.githubusercontent.com/Infrasity-Labs/developer-marketing-jobs/main/README.md';
  const { data } = await axios.get(url);
  
  const jobs = [];
  const lines = data.split('\n');
  let inDevRelSection = false;
  
  for (const line of lines) {
    if (line.includes('## 🎤 Developer Advocate')) {
      inDevRelSection = true;
      continue;
    }
    
    if (inDevRelSection && line.startsWith('## ')) {
      break;
    }
    
    if (inDevRelSection && line.startsWith('|') && !line.includes('Role') && !line.includes('---')) {
      const parts = line.split('|').slice(1, -1).map(p => p.trim());
      if (parts.length === 4) {
        const urlMatch = parts[3].match(/\((.*?)\)/);
        jobs.push({
          role: parts[0],
          company: parts[1],
          location: parts[2],
          applyUrl: urlMatch ? urlMatch[1] : ''
        });
      }
    }
  }
  
  return jobs;
}

// Usage
fetchDevRelJobs().then(jobs => {
  const remoteJobs = jobs.filter(j => j.location.toLowerCase().includes('remote'));
  console.log(`Found ${remoteJobs.length} remote positions`);
});
```

## Common Patterns

### Weekly Job Digest

Create a weekly summary of new jobs:

```bash
#!/bin/bash
# weekly_digest.sh

REPO="Infrasity-Labs/developer-marketing-jobs"
WEEK_AGO=$(date -d '7 days ago' +%s)

# Get commits from last week
git log --since="7 days ago" --pretty=format:"%H" | while read commit; do
  git show $commit:README.md | grep "^|" | grep -v "Role"
done | sort -u > weekly_jobs.txt

echo "New jobs this week:"
cat weekly_jobs.txt
```

### Filter by Seniority

```bash
# Find senior-level roles
grep -i "senior\|staff\|principal\|lead" README.md | grep "Developer Advocate"

# Find entry-level or mid-level roles
grep -iv "senior\|staff\|principal\|lead\|director" README.md | grep "Developer Advocate"
```

### Geographic Filtering

```bash
# US-based remote jobs
grep -i "united states\|remote" README.md | grep "Developer Advocate"

# European jobs
grep -iE "london|berlin|paris|amsterdam|remote - europe" README.md

# APAC region
grep -iE "singapore|tokyo|sydney|apac" README.md
```

## Submitting New Job Listings

If you're hiring for a DevRel or related role:

1. Open an issue in the repository
2. Use the job submission template
3. Include: Job title, company, location, ATS feed URL
4. Maintainers will add the company's feed to the automation

Example issue format:
```markdown
**Company**: YourCompany
**Job Title**: Senior Developer Advocate
**Location**: San Francisco / Remote
**ATS Feed URL**: https://jobs.lever.co/yourcompany/feed
**Direct Job URL**: https://jobs.lever.co/yourcompany/job-id
```

## Data Freshness

- **Update Frequency**: Daily (via GitHub Actions)
- **Update Time**: Runs nightly (timezone varies)
- **Badge Status**: Check the "Updated Daily" badge in README
- **Last Updated**: View the commit history for exact timestamp

```bash
# Check last update time
git log -1 --format="%ai" README.md
```

## Integration Examples

### Slack Bot Notification

```python
import os
import requests

def notify_slack_new_jobs(jobs: List[Dict], webhook_url: str):
    """Send new job listings to Slack channel."""
    
    if not jobs:
        return
    
    blocks = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "🎯 New DevRel Jobs"}
        }
    ]
    
    for job in jobs[:10]:  # Limit to 10
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{job['role']}* at {job['company']}\n📍 {job['location']}"
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "Apply"},
                "url": job['apply_url']
            }
        })
    
    payload = {"blocks": blocks}
    requests.post(webhook_url, json=payload)

# Usage with environment variable
webhook = os.environ.get('SLACK_WEBHOOK_URL')
new_jobs = fetch_devrel_jobs()
notify_slack_new_jobs(new_jobs, webhook)
```

### RSS Feed Generator

```python
from feedgen.feed import FeedGenerator
from datetime import datetime

def generate_jobs_rss(jobs: List[Dict]) -> str:
    """Generate RSS feed from jobs."""
    
    fg = FeedGenerator()
    fg.id('https://github.com/Infrasity-Labs/developer-marketing-jobs')
    fg.title('Developer Marketing Jobs')
    fg.link(href='https://github.com/Infrasity-Labs/developer-marketing-jobs', rel='alternate')
    fg.description('Daily DevRel and Developer Marketing Job Listings')
    
    for job in jobs:
        fe = fg.add_entry()
        fe.id(job['apply_url'])
        fe.title(f"{job['role']} at {job['company']}")
        fe.description(f"Location: {job['location']}")
        fe.link(href=job['apply_url'])
        fe.published(datetime.now())
    
    return fg.rss_str(pretty=True)
```

## Troubleshooting

### Jobs Not Showing Up

**Problem**: Recently posted job not in the list
- **Solution**: Wait 24 hours for next automated update, or check if company's ATS feed is included

**Problem**: Company not tracked
- **Solution**: Submit an issue requesting the company be added to the tracking list

### Parsing Issues

**Problem**: Job table format changed
- **Solution**: Update your parsing regex to match the current table format:
  ```python
  # Updated regex pattern
  pattern = r'\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*\[→\]\((.+?)\)'
  ```

### Data Quality

**Problem**: Duplicate listings
- **Solution**: The automation deduplicates by URL; check your local cache

**Problem**: Stale listings
- **Solution**: Jobs are pulled from live ATS feeds; if a job appears stale, it may still be open

## Advanced Usage

### Build a Custom Job Dashboard

```html
<!DOCTYPE html>
<html>
<head>
  <title>My DevRel Job Tracker</title>
  <script>
    async function loadJobs() {
      const response = await fetch('https://raw.githubusercontent.com/Infrasity-Labs/developer-marketing-jobs/main/README.md');
      const text = await response.text();
      
      const jobs = parseMarkdownTable(text);
      displayJobs(jobs.filter(j => j.location.includes('Remote')));
    }
    
    function parseMarkdownTable(markdown) {
      // Parsing logic here
      return jobs;
    }
    
    function displayJobs(jobs) {
      const container = document.getElementById('jobs');
      jobs.forEach(job => {
        const div = document.createElement('div');
        div.innerHTML = `<h3>${job.role}</h3><p>${job.company} - ${job.location}</p>`;
        container.appendChild(div);
      });
    }
    
    loadJobs();
  </script>
</head>
<body>
  <h1>Remote DevRel Jobs</h1>
  <div id="jobs"></div>
</body>
</html>
```

## Related Resources

- **Project Repository**: https://github.com/Infrasity-Labs/developer-marketing-jobs
- **Maintained By**: [Infrasity](https://infrasity.com)
- **License**: MIT
- **Update Mechanism**: GitHub Actions (automated)

This job board is ideal for DevRel professionals, developer marketers, technical writers, and community managers looking for opportunities at devtool companies. The daily automation ensures fresh listings without manual curation overhead.
