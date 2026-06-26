---
name: skill-scan
description: |
  Security scanning tool for OpenClaw Skills. Detects malicious code patterns, 
  extracts domains, and checks threat intelligence APIs. Use when: installing new 
  Skills (pre-installation security check), auditing installed Skills, detecting 
  malicious code, scanning suspicious domains, generating security reports, or 
  verifying Skill safety before distribution.
---

# Skill Scan - Security Scanner for OpenClaw Skills

## Purpose

Skill Scan is a security tool that analyzes OpenClaw Skills for potentially malicious code and threat intelligence indicators before installation or during audits.

## Features

- 🔍 **Static Code Analysis**: Detects dangerous patterns (exec, network, filesystem, sensitive data access)
- 🌐 **Domain Extraction**: Identifies all domains referenced in Skill code
- 🛡️ **Threat Intelligence Check**: Validates domains against abuse databases (Abuse.ch, AbuseIPDB, VirusTotal)
- 📊 **Risk Scoring**: Generates risk levels (low/medium/high) with detailed reports
- 💾 **JSON Export**: Saves scan results for automation and CI/CD integration

## Usage

### Basic Scan

```bash
python3 ~/.openclaw/skills/skill-scan/scripts/skill-scan.py <skill-path>
```

### Examples

```bash
# Scan a specific Skill
python3 ~/.openclaw/skills/skill-scan/scripts/skill-scan.py ~/.openclaw/extensions/mem9

# Scan all installed Skills
for skill in ~/.openclaw/extensions/*/; do
  echo "Scanning: $skill"
  python3 ~/.openclaw/skills/skill-scan/scripts/skill-scan.py "$skill"
done

# Scan before installation
tar -xzf new-skill.tgz -C /tmp/skill-check/
python3 ~/.openclaw/skills/skill-scan/scripts/skill-scan.py /tmp/skill-check/
```

## Output

### Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🟢 **low** | Only routine network requests | Safe to install |
| 🟡 **medium** | Contains exec/system calls | Review code manually |
| 🔴 **high** | Suspicious domains/malicious patterns | ⚠️ Do NOT install |

### Report Format

```
============================================================
📊 Skill Security Scan Report
============================================================
Skill Path: /path/to/skill
Risk Level: low
Total Findings: 2
Domains Checked: 1

📋 Findings by Category:
  - network: 2

📝 Details:
  [network] /path/to/file.ts:30
    const resp = await fetch(this.baseUrl + "/v1alpha1/mem9s", {
============================================================
```

## Detection Categories

### 1. Exec (System Command Execution)
- `exec()`, `execSync()`, `spawn()`
- `child_process`, `subprocess.*`
- `os.system()`, `shell_exec()`

### 2. Network (Network Requests)
- `fetch()`, `axios.*`
- `http.get`, `https.get`
- `requests.*`, `urllib.request`
- `XMLHttpRequest`

### 3. Filesystem (File Operations)
- `fs.writeFile`, `fs.readFile`, `fs.unlink`
- `open(..., 'w')`
- `shutil.(copy|move|remove)`

### 4. Sensitive (Sensitive Data Access)
- `process.env`, `process.argv`
- `os.environ`
- Hardcoded secrets: `secret=`, `password=`, `token=`, `api_key=`

## Threat Intelligence Sources

### Built-in (Free APIs)

| Source | Type | API |
|--------|------|-----|
| **Abuse.ch URLhaus** | Malicious domains/IPs | https://urlhaus-api.abuse.ch/ |
| **AbuseIPDB** | IP reputation | https://www.abuseipdb.com/api |
| **Local Blacklist** | Known malicious domains | Built-in |

### Optional (API Key Required)

| Source | Type | API |
|--------|------|-----|
| **VirusTotal** | Files/URLs/Domains | https://www.virustotal.com/api/ |
| **AlienVault OTX** | Threat intelligence | https://otx.alienvault.com/api |
| **Google Safe Browsing** | Malicious websites | https://safebrowsing.googleapis.com/ |

## Configuration

To enable additional threat intelligence APIs, edit the script and add your API keys:

```python
THREAT_INTEL_APIS = {
    "virustotal": {
        "url": "https://www.virustotal.com/api/v3/domains/",
        "key_param": "x-apikey",
        "api_key": "YOUR_API_KEY"  # Add your key here
    }
}
```

## Integration

### Pre-installation Hook

Add to your CI/CD pipeline:

```bash
#!/bin/bash
# Pre-installation security check

SKILL_PATH=$1
REPORT=$(python3 ~/.openclaw/skills/skill-scan/scripts/skill-scan.py "$SKILL_PATH")

if echo "$REPORT" | grep -q "Risk Level: high"; then
  echo "❌ Security check failed: High risk detected"
  exit 1
fi

echo "✅ Security check passed"
```

### Periodic Audit

Create a cron job for weekly audits:

```bash
# /etc/cron.d/skill-scan
0 2 * * 1 niuqun python3 ~/.openclaw/skills/skill-scan/scripts/skill-scan.py ~/.openclaw/extensions/* >> /var/log/skill-scan.log
```

## Security Best Practices

1. **Always scan before installing** - Never install Skills from unknown sources without scanning
2. **Review medium/high risks** - Don't ignore warnings
3. **Keep threat intel updated** - Regularly update local blacklists
4. **Report false positives** - Help improve the tool
5. **Contribute signatures** - Add new malicious patterns you discover

## Troubleshooting

### Issue: Script fails to run
**Solution**: Ensure Python 3 is installed and script has execute permission
```bash
chmod +x ~/.openclaw/skills/skill-scan/scripts/skill-scan.py
```

### Issue: Threat intelligence API timeout
**Solution**: Check network connection or API key validity
```bash
curl -I https://urlhaus-api.abuse.ch/
```

### Issue: Too many false positives
**Solution**: Adjust detection patterns in the script or add domains to whitelist

## Limitations

- **Static analysis only** - Cannot detect runtime behavior
- **API rate limits** - Free APIs have request limits
- **Evasion techniques** - Obfuscated code may bypass detection
- **No sandbox** - Does not execute code in isolation

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Add new detection patterns
3. Integrate additional threat intelligence sources
4. Submit pull requests

## License

MIT License - See LICENSE file for details

## Support

- **Issues**: https://github.com/yourusername/skill-scan/issues
- **Documentation**: https://github.com/yourusername/skill-scan/wiki
- **Threat Intel**: Report malicious domains to abuse@yourdomain.com

---

**Remember**: This tool is a first line of defense. Always combine with manual code review and other security measures for critical systems.
