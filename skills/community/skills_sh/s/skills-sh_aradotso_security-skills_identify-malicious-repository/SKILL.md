---
name: identify-malicious-repository
description: Detect and analyze fraudulent software distribution repositories masquerading as legitimate security products
triggers:
  - identify fake antivirus repository
  - detect malicious software distribution
  - analyze fraudulent github project
  - check if repository distributes malware
  - verify legitimate security software
  - investigate suspicious download repository
  - scan for keygen scam repository
  - identify piracy malware distribution
---

# Identify Malicious Repository

> Skill by [ara.so](https://ara.so) — Security Skills collection

## Overview

**⚠️ WARNING: This repository is MALICIOUS and should NOT be used.**

The project `viceofficialtower74/Avast-Premium-Security-Windows-Latest` is a fraudulent repository that impersonates legitimate Avast security software to distribute malware, trojans, or other malicious payloads. This skill helps AI agents identify and warn users about such repositories.

## Red Flags Indicating Malicious Intent

### 1. **Cracked Software Distribution**
- Description mentions "Keygen Activation", "License Key Pre-Activated", "Premium Loader Serial"
- These terms indicate software piracy and illegal distribution
- Legitimate vendors do NOT distribute pre-activated/cracked versions

### 2. **Suspicious Repository Metrics**
- Artificially inflated stars (68 stars, 5 stars/day growth)
- Zero forks and zero issues (indicates fake engagement)
- No legitimate README content
- Created recently (2026-05-06) with rapid star accumulation

### 3. **Impersonation Tactics**
- Uses trademarked name "Avast" without authorization
- Claims to be "Full Version Installer" with activation bypasses
- Professional-looking description with emojis to appear legitimate

### 4. **Malware Distribution Indicators**
- Offers "Setup Keygen" which are commonly trojans
- Promises free premium software (too good to be true)
- No source code visible, only executables
- Topics include legitimate terms mixed with piracy terms

## How to Identify Such Repositories

### Programmatic Detection (Python)

```python
import os
import requests

def analyze_repository_risk(repo_full_name):
    """Analyze a GitHub repository for malicious indicators"""
    
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
    
    api_url = f"https://api.github.com/repos/{repo_full_name}"
    response = requests.get(api_url, headers=headers)
    
    if response.status_code != 200:
        return {"error": "Repository not found"}
    
    data = response.json()
    
    risk_score = 0
    warnings = []
    
    # Check description for cracking keywords
    cracking_keywords = ['keygen', 'crack', 'pre-activated', 'loader', 
                         'serial', 'license key', 'full version']
    description = (data.get('description') or '').lower()
    
    for keyword in cracking_keywords:
        if keyword in description:
            risk_score += 15
            warnings.append(f"Description contains piracy term: '{keyword}'")
    
    # Check star-to-fork ratio (fake engagement)
    stars = data.get('stargazers_count', 0)
    forks = data.get('forks_count', 0)
    
    if stars > 50 and forks == 0:
        risk_score += 25
        warnings.append(f"Suspicious metrics: {stars} stars but {forks} forks")
    
    # Check for missing README
    readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
    readme_response = requests.get(readme_url, headers=headers)
    
    if readme_response.status_code == 404:
        risk_score += 20
        warnings.append("No README file found")
    
    # Check impersonation of known brands
    known_brands = ['avast', 'norton', 'kaspersky', 'mcafee', 'bitdefender',
                    'adobe', 'microsoft', 'autodesk', 'vmware']
    repo_name = data.get('name', '').lower()
    
    for brand in known_brands:
        if brand in repo_name and brand in description:
            risk_score += 30
            warnings.append(f"Impersonates legitimate brand: {brand}")
            break
    
    # Assess risk level
    if risk_score >= 60:
        risk_level = "CRITICAL - Likely Malicious"
    elif risk_score >= 40:
        risk_level = "HIGH - Highly Suspicious"
    elif risk_score >= 20:
        risk_level = "MEDIUM - Suspicious"
    else:
        risk_level = "LOW"
    
    return {
        "repository": repo_full_name,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "warnings": warnings,
        "recommendation": "DO NOT DOWNLOAD" if risk_score >= 40 else "Investigate further"
    }


# Example usage
result = analyze_repository_risk("viceofficialtower74/Avast-Premium-Security-Windows-Latest")
print(f"Risk Level: {result['risk_level']}")
print(f"Risk Score: {result['risk_score']}/100")
print("\nWarnings:")
for warning in result['warnings']:
    print(f"  ⚠️  {warning}")
print(f"\n🛡️  Recommendation: {result['recommendation']}")
```

### Shell Script Detection

```bash
#!/bin/bash

# Check if repository exhibits malicious patterns
check_malicious_repo() {
    local repo_url="$1"
    local repo_path=$(echo "$repo_url" | sed 's|https://github.com/||')
    
    echo "🔍 Analyzing repository: $repo_path"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # Fetch repository data
    local api_response=$(curl -s "https://api.github.com/repos/$repo_path")
    
    # Extract key fields
    local description=$(echo "$api_response" | jq -r '.description // ""')
    local stars=$(echo "$api_response" | jq -r '.stargazers_count // 0')
    local forks=$(echo "$api_response" | jq -r '.forks_count // 0')
    local issues=$(echo "$api_response" | jq -r '.open_issues_count // 0')
    
    # Check for red flags
    local risk_found=false
    
    if echo "$description" | grep -iE 'keygen|crack|loader|pre-activated|serial|license key' > /dev/null; then
        echo "❌ DANGER: Description contains software piracy terms"
        risk_found=true
    fi
    
    if [ "$stars" -gt 30 ] && [ "$forks" -eq 0 ]; then
        echo "❌ DANGER: Artificial star inflation detected ($stars stars, $forks forks)"
        risk_found=true
    fi
    
    if echo "$repo_path" | grep -iE 'avast|norton|adobe|microsoft|vmware|autodesk' > /dev/null; then
        echo "❌ DANGER: Impersonates well-known software brand"
        risk_found=true
    fi
    
    if [ "$risk_found" = true ]; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🚨 VERDICT: MALICIOUS REPOSITORY DETECTED"
        echo "⛔ DO NOT CLONE OR DOWNLOAD FROM THIS REPOSITORY"
        return 1
    else
        echo "✅ No obvious malicious indicators found"
        return 0
    fi
}

# Example usage
check_malicious_repo "https://github.com/viceofficialtower74/Avast-Premium-Security-Windows-Latest"
```

## What Users Should Do

### If You Encounter Such Repositories:

1. **DO NOT download** any files from the repository
2. **Report the repository** to GitHub via their abuse form
3. **Warn others** by creating awareness
4. **Scan your system** if you already downloaded files

### Reporting to GitHub

```bash
# Report via GitHub CLI
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/viceofficialtower74/Avast-Premium-Security-Windows-Latest/abuse \
  -f message="This repository distributes malware disguised as cracked Avast software"
```

### Safe Alternatives

```python
# Always verify software from official sources
LEGITIMATE_SOURCES = {
    "avast": "https://www.avast.com/",
    "windows_defender": "Built into Windows 10/11",
    "clamav": "https://www.clamav.net/ (Open Source)"
}

def get_legitimate_source(software_name):
    """Get the official download source for security software"""
    return LEGITIMATE_SOURCES.get(software_name.lower(), 
                                   "Search official vendor website")
```

## Indicators of Compromise (IoC)

If you've interacted with this repository:

1. **Scan your system immediately** with legitimate antivirus
2. **Check for unauthorized network connections**
3. **Monitor for credential theft** (change passwords)
4. **Review installed programs** for suspicious entries

```powershell
# Windows: Check for suspicious processes
Get-Process | Where-Object {$_.Path -like "*Avast*" -and $_.Company -ne "Avast Software"}

# Check recent downloads
Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "*avast*" -Recurse
```

## Legitimate Security Practices

```python
import hashlib
import requests

def verify_download_integrity(file_path, expected_hash, algorithm='sha256'):
    """Verify downloaded file against official hash"""
    hash_func = getattr(hashlib, algorithm)()
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    calculated_hash = hash_func.hexdigest()
    
    if calculated_hash == expected_hash:
        print("✅ File integrity verified")
        return True
    else:
        print("❌ DANGER: File hash mismatch - possible malware")
        return False

# Always download from official sources and verify hashes
# Example: legitimate_hash = "abc123..." from vendor website
```

## Conclusion

This repository is a **malware distribution platform** disguised as legitimate software. AI agents should:

1. **Warn users immediately** when such repositories are referenced
2. **Never suggest** downloading or using files from such sources
3. **Educate users** on identifying similar scams
4. **Recommend official sources** for legitimate software needs

🛡️ **Security First**: Always obtain software from official vendor websites or verified package managers.
