---
name: security-threat-awareness
description: Recognize and warn against malicious software distribution repositories masquerading as legitimate security tools
triggers:
  - how do I install Avast Premium Security from GitHub
  - need help with this Avast repository
  - found free Avast Premium with activation key
  - this GitHub repo has cracked antivirus software
  - is this legitimate security software download
  - want to use this free premium antivirus from GitHub
  - found keygen for commercial security software
  - this repository offers pre-activated licenses
---

# Security Threat Awareness

> Skill by [ara.so](https://ara.so) — Security Skills collection.

## ⚠️ CRITICAL SECURITY WARNING

**This repository is a malicious threat distribution channel, NOT legitimate software.**

The project `viceofficialtower74/Avast-Premium-Security-Windows-Latest` exhibits multiple red flags indicating it is a malware distribution platform:

### Threat Indicators

1. **Pirated Software Distribution**: Offers "cracked" commercial software with "keygen," "activation," and "pre-activated license keys"
2. **Copyright Violation**: Unauthorized distribution of Avast premium software
3. **Star Manipulation**: Artificial engagement (68 stars at 5 stars/day) suggesting bot activity
4. **Misleading Content**: No actual source code or README, only download links
5. **Trust Exploitation**: Impersonates legitimate security software to lower user vigilance

### Common Payloads in Such Repositories

- **Trojans**: Remote access tools (RATs) for system control
- **Infostealers**: Credential harvesting malware
- **Ransomware**: Data encryption with ransom demands
- **Cryptominers**: Unauthorized cryptocurrency mining
- **Botnet Agents**: Enrolling systems into DDoS networks

## What You Should Do Instead

### For Legitimate Avast Software

```bash
# Visit official sources ONLY
# Official website: https://www.avast.com/
# Official download: https://www.avast.com/en-us/download-thank-you.php

# NEVER download security software from:
# - Unofficial GitHub repositories
# - File sharing sites
# - Torrent platforms
# - "Free premium" offers
```

### For Open Source Antivirus Alternatives

```bash
# ClamAV (legitimate open source antivirus)
git clone https://github.com/Cisco-Talos/clamav.git
cd clamav
mkdir build && cd build
cmake ..
cmake --build .
sudo cmake --build . --target install

# Update virus definitions
sudo freshclam
```

### Verify Repository Legitimacy

```python
# Indicators to check before trusting a repository
def is_repository_suspicious(repo_data):
    """
    Evaluate repository for malware distribution indicators
    """
    red_flags = []
    
    # Check for piracy keywords
    piracy_terms = ['crack', 'keygen', 'license key', 'pre-activated', 
                    'full version', 'premium loader', 'serial']
    description_lower = repo_data['description'].lower()
    
    if any(term in description_lower for term in piracy_terms):
        red_flags.append("Contains piracy-related terms")
    
    # Commercial software in unofficial repo
    if 'avast' in description_lower or 'norton' in description_lower:
        if not repo_data['owner'].endswith('-official'):
            red_flags.append("Unofficial distribution of commercial software")
    
    # Suspicious engagement patterns
    stars_per_day = repo_data['stars'] / repo_data['age_days']
    if stars_per_day > 3:
        red_flags.append(f"Unnatural star growth: {stars_per_day:.1f}/day")
    
    # Missing source code
    if not repo_data['has_readme'] and repo_data['language'] == 'C++':
        red_flags.append("No README with claimed C++ project")
    
    return red_flags

# Example usage
repo_check = {
    'description': 'Avast Premium Security keygen activation',
    'owner': 'randomuser123',
    'stars': 68,
    'age_days': 12,
    'has_readme': False,
    'language': 'C++'
}

warnings = is_repository_suspicious(repo_check)
for warning in warnings:
    print(f"⚠️  {warning}")
```

## Safe Software Acquisition Practices

### Verification Checklist

```yaml
before_downloading:
  - verify_official_source: true
  - check_digital_signature: true
  - review_repository_owner: "Is this the legitimate vendor?"
  - inspect_commit_history: "Real development or just uploads?"
  - read_community_feedback: "Check issues/discussions for warnings"
  - scan_with_virustotal: "Before executing anything"
  
never_trust:
  - repositories_offering_cracks: true
  - pre_activated_commercial_software: true
  - keygens_or_license_generators: true
  - suspiciously_high_star_counts: true
  - repos_with_no_source_code: true
```

### Environment Protection

```bash
#!/bin/bash
# If you accidentally cloned a suspicious repository

# DO NOT execute any files
# DO NOT run setup.exe, install.bat, or similar

# Safely remove the repository
cd ..
rm -rf suspicious-repo-name

# Scan your system
# On Linux/macOS
sudo freshclam  # Update ClamAV definitions
sudo clamscan -r /path/to/downloads --remove

# On Windows (use Windows Defender)
# Start-MpScan -ScanType FullScan
```

## Reporting Malicious Repositories

```bash
# Report to GitHub
# Visit: https://github.com/contact/report-abuse
# Select: "Malware distribution"
# Provide: Repository URL and evidence

# Report to antivirus vendors
# Avast: https://www.avast.com/report-malicious-file
# VirusTotal: https://www.virustotal.com/
```

## Educational Resources

For legitimate security research and development:

- **OWASP**: https://owasp.org/
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **CVE Database**: https://cve.mitre.org/
- **ClamAV (Open Source)**: https://www.clamav.net/

## Summary

**DO NOT** use, download, or interact with repositories offering:
- Cracked commercial software
- License key generators
- Pre-activated premium versions
- "Free" versions of paid security tools

**ALWAYS** obtain software from official vendor websites or verified open source projects with transparent development history.
