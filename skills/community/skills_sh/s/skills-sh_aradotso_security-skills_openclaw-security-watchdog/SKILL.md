---
name: openclaw-security-watchdog
description: OpenClaw security scanning skill that performs comprehensive system security audits and generates human-friendly reports
triggers:
  - run security scan
  - perform security audit
  - check system security
  - execute security inspection
  - do a security check
  - scan for security issues
  - run openclaw security watchdog
  - perform system security audit
---

# OpenClaw Security Watchdog

> Skill by [ara.so](https://ara.so) — Security Skills collection.

OpenClaw Security Watchdog is an automated security scanning tool that performs comprehensive system security audits across 14 critical security dimensions. It generates human-readable reports with clear risk indicators (✅/⚠️/🚨) and can integrate with threat intelligence databases.

## Installation

**Prerequisites:**
- Node.js v18 or higher
- OpenClaw CLI installed

**Install via OpenClaw (Recommended):**
```bash
# In OpenClaw chat, say:
# "Install the security watchdog skill from https://github.com/CTCT-CT2/openclaw-security-watchdog"
```

**Manual Installation:**
```bash
git clone https://github.com/CTCT-CT2/openclaw-security-watchdog.git
cd openclaw-security-watchdog
npm install
```

## Triggering the Scan

Once installed as an OpenClaw skill, trigger it conversationally:

```
Execute security inspection
```

```
Help me check system security
```

```
Run a security audit
```

OpenClaw will automatically recognize and execute the security watchdog skill.

## Scan Modes

### Full Scan (Recommended)
- Runs all 14 security checks
- Queries threat intelligence databases (optional)
- Sends anonymized metadata for analysis
- Provides comprehensive risk scoring

### Local-Only Mode
- Zero network traffic
- All data stays on local machine
- No threat intelligence lookups
- Privacy-first approach

## Security Check Coverage

The tool scans 14 critical areas:

1. **Core Runtime Environment Health** - Checks Node.js/system integrity
2. **Sensitive Directory Tamper Detection** - Monitors critical system paths
3. **Gateway Process Memory Isolation** - Validates credential isolation
4. **Configuration Integrity & Permission Baseline** - Audits config file permissions
5. **Component Supply Chain Integrity** - Validates package checksums
6. **Remote Access & Brute Force Monitoring** - SSH/RDP attack detection
7. **Network Exposure & Anomalous Processes** - Open ports and suspicious processes
8. **Automated Tasks & Backdoor Detection** - Cron/scheduled task analysis
9. **Privilege Escalation & Unauthorized Commands** - Sudo abuse detection
10. **Outbound Connections & Data Exfiltration** - Network traffic analysis
11. **System Credentials & Sensitive File Access** - Access log auditing
12. **Hardcoded Secrets & Mnemonic Leak Scanning** - Secret detection in code
13. **Sudo Privilege Audit** - Privilege escalation tracking
14. **Malicious Component Threat Intelligence** - Known malware detection

## Code Examples

### Basic Scan Execution (JavaScript)

```javascript
const SecurityWatchdog = require('openclaw-security-watchdog');

// Initialize scanner
const scanner = new SecurityWatchdog({
  mode: 'full', // or 'local'
  reportPath: '~/.openclaw/security-reports/',
  enableThreatIntel: true
});

// Run scan
async function runSecurityScan() {
  try {
    const results = await scanner.scan();
    
    console.log(`Security Score: ${results.score}/100`);
    console.log(`Passed: ${results.passed}/${results.total}`);
    console.log(`Warnings: ${results.warnings}`);
    console.log(`Critical: ${results.critical}`);
    
    // Access individual check results
    results.checks.forEach(check => {
      console.log(`${check.icon} ${check.name}: ${check.status}`);
      if (check.findings.length > 0) {
        console.log(`  Findings: ${check.findings.join(', ')}`);
      }
    });
    
    // Generate report
    await scanner.generateReport(results);
    
  } catch (error) {
    console.error('Scan failed:', error);
  }
}

runSecurityScan();
```

### Scheduled Scanning

```javascript
const cron = require('node-cron');
const SecurityWatchdog = require('openclaw-security-watchdog');

// Schedule daily scan at 2 AM
cron.schedule('0 2 * * *', async () => {
  const scanner = new SecurityWatchdog({ mode: 'full' });
  const results = await scanner.scan();
  
  // Send alerts on critical findings
  if (results.critical > 0) {
    await scanner.sendAlert(results, {
      channel: 'email',
      recipients: [process.env.SECURITY_ALERT_EMAIL]
    });
  }
});
```

### Custom Check Integration

```javascript
const SecurityWatchdog = require('openclaw-security-watchdog');

const scanner = new SecurityWatchdog();

// Add custom security check
scanner.addCheck({
  name: 'Custom API Key Validation',
  category: 'secrets',
  async execute() {
    const apiKeys = await this.scanForPattern(/api[_-]?key\s*[:=]\s*['"][^'"]{20,}['"]/gi);
    
    return {
      status: apiKeys.length === 0 ? 'pass' : 'fail',
      findings: apiKeys,
      severity: 'high',
      recommendation: 'Move API keys to environment variables'
    };
  }
});

scanner.scan();
```

### Filtering Scan Results

```javascript
const scanner = new SecurityWatchdog();

const results = await scanner.scan();

// Get only critical findings
const criticalIssues = results.checks.filter(
  check => check.severity === 'critical' && check.status === 'fail'
);

// Get all permission-related issues
const permissionIssues = results.checks.filter(
  check => check.category === 'permissions'
);

// Generate filtered report
await scanner.generateReport(results, {
  filter: check => check.severity === 'high' || check.severity === 'critical'
});
```

## Configuration

Create `~/.openclaw/security-watchdog.json`:

```json
{
  "mode": "full",
  "reportPath": "~/.openclaw/security-reports/",
  "enableThreatIntel": true,
  "excludePaths": [
    "/tmp",
    "/var/cache"
  ],
  "checksToRun": [
    "runtime-health",
    "directory-tamper",
    "memory-isolation",
    "config-integrity",
    "supply-chain",
    "remote-access",
    "network-exposure",
    "scheduled-tasks",
    "privilege-escalation",
    "outbound-connections",
    "credential-access",
    "secret-scanning",
    "sudo-audit",
    "threat-intel"
  ],
  "alerting": {
    "enabled": true,
    "thresholds": {
      "critical": 1,
      "high": 3
    },
    "channels": ["email", "slack"]
  },
  "threatIntelSources": [
    "https://threat-intel.openclaw.io/api/v1/lookup"
  ]
}
```

## Environment Variables

```bash
# Threat intelligence API key (if using external sources)
export OPENCLAW_THREAT_INTEL_API_KEY=your_api_key_here

# Alert notification endpoints
export SECURITY_ALERT_EMAIL=security@example.com
export SECURITY_ALERT_SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Report encryption key (optional)
export OPENCLAW_REPORT_ENCRYPTION_KEY=your_encryption_key_here
```

## Report Output

Reports are saved to `~/.openclaw/security-reports/` with timestamp:

```
security-report-2026-05-06-14-30-00.json
security-report-2026-05-06-14-30-00.html
security-report-2026-05-06-14-30-00.txt
```

### Accessing Report Programmatically

```javascript
const fs = require('fs');
const path = require('path');

const reportPath = path.join(
  process.env.HOME,
  '.openclaw/security-reports/security-report-latest.json'
);

const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));

console.log(`Overall Security Score: ${report.score}/100`);
console.log(`Risk Level: ${report.riskLevel}`); // low, medium, high, critical
```

## Common Patterns

### Pre-Deployment Security Gate

```javascript
// In CI/CD pipeline
const SecurityWatchdog = require('openclaw-security-watchdog');

async function securityGate() {
  const scanner = new SecurityWatchdog({ mode: 'local' });
  const results = await scanner.scan();
  
  if (results.critical > 0) {
    console.error('❌ Critical security issues found. Deployment blocked.');
    process.exit(1);
  }
  
  if (results.score < 80) {
    console.warn('⚠️  Security score below threshold. Review required.');
    process.exit(1);
  }
  
  console.log('✅ Security scan passed. Proceeding with deployment.');
}

securityGate();
```

### Continuous Monitoring

```javascript
const SecurityWatchdog = require('openclaw-security-watchdog');
const EventEmitter = require('events');

class SecurityMonitor extends EventEmitter {
  constructor() {
    super();
    this.scanner = new SecurityWatchdog({ mode: 'full' });
  }
  
  startMonitoring(intervalMinutes = 60) {
    setInterval(async () => {
      const results = await this.scanner.scan();
      
      if (results.critical > 0) {
        this.emit('criticalThreat', results);
      }
      
      if (results.score < this.lastScore - 10) {
        this.emit('scoreDropped', results);
      }
      
      this.lastScore = results.score;
    }, intervalMinutes * 60 * 1000);
  }
}

const monitor = new SecurityMonitor();
monitor.on('criticalThreat', results => {
  console.error('🚨 Critical threat detected!', results);
});
monitor.startMonitoring();
```

## Troubleshooting

### Permission Errors

```bash
# Ensure proper permissions for scanning system directories
sudo chmod +r /var/log/auth.log
sudo chmod +r /etc/ssh/sshd_config

# Or run with elevated privileges (not recommended for regular use)
sudo openclaw scan
```

### Missing Dependencies

```bash
# Reinstall dependencies
npm install

# Check Node.js version
node --version  # Should be v18+
```

### Threat Intelligence Timeout

```javascript
// Increase timeout in configuration
const scanner = new SecurityWatchdog({
  threatIntel: {
    timeout: 30000, // 30 seconds
    retries: 3
  }
});
```

### Report Generation Fails

```javascript
// Ensure report directory exists and is writable
const fs = require('fs');
const reportDir = path.join(process.env.HOME, '.openclaw/security-reports');

if (!fs.existsSync(reportDir)) {
  fs.mkdirSync(reportDir, { recursive: true });
}
```

### Large Codebases (Slow Scanning)

```javascript
// Optimize for large projects
const scanner = new SecurityWatchdog({
  excludePaths: [
    'node_modules',
    '.git',
    'dist',
    'build',
    'coverage'
  ],
  maxFileSize: 1048576, // 1MB
  parallelScans: 4
});
```

## Privacy Considerations

**Full Mode sends:**
- Check names and results (pass/fail)
- Anonymized device identifier (SHA-256 hash)
- Summary statistics only

**Full Mode does NOT send:**
- File contents
- Passwords or API keys
- Log file contents
- IP addresses
- Usernames

**Local Mode:**
- Zero network requests
- All data remains on device
- No telemetry or analytics
