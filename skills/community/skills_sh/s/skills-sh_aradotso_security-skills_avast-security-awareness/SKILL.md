---
name: avast-security-awareness
description: Recognize and avoid malicious software distribution repositories disguised as legitimate security tools
triggers:
  - how do I identify fake antivirus repositories
  - is this avast repository legitimate
  - how to spot malware distribution on github
  - what are signs of a cracked software scam
  - how to verify legitimate security software sources
  - detect fake keygen and activation tools
---

# Avast Security Awareness Skill

> Skill by [ara.so](https://ara.so) — Security Skills collection.

## ⚠️ Critical Security Warning

This repository is **NOT a legitimate Avast product** and represents a common malware distribution pattern. This skill teaches AI agents to identify and warn users about such threats.

## What This Skill Does

This skill enables AI coding agents to:

- Recognize malicious software distribution repositories
- Identify red flags in repository descriptions and content
- Educate users on safe software acquisition practices
- Prevent installation of potentially malicious software
- Guide users to legitimate security software sources

## Identifying Malicious Repository Patterns

### Red Flags Present in This Repository

1. **Suspicious Keywords**: "Keygen", "Crack", "Pre-Activated", "Loader", "Serial"
2. **Version Manipulation**: Claims of future versions (2026 when current year is earlier)
3. **No Source Code**: No actual implementation despite claiming to be a Go project
4. **Artificial Engagement**: Star velocity inconsistent with legitimate projects
5. **Missing Documentation**: No README or legitimate setup instructions
6. **License Issues**: NOASSERTION license for "open source" security software
7. **Mismatched Topics**: Topics like "retdec" unrelated to described functionality

### Detection Code Example (Go)

```go
package malwaredetect

import (
    "strings"
    "regexp"
)

type RepositoryAnalyzer struct {
    SuspiciousKeywords []string
    MinimumREADMELength int
}

func NewAnalyzer() *RepositoryAnalyzer {
    return &RepositoryAnalyzer{
        SuspiciousKeywords: []string{
            "keygen", "crack", "pre-activated", "loader",
            "serial", "full version", "setup keygen",
        },
        MinimumREADMELength: 100,
    }
}

func (a *RepositoryAnalyzer) AnalyzeRepository(description, readme string) (bool, []string) {
    var warnings []string
    isSuspicious := false

    // Check for suspicious keywords
    descLower := strings.ToLower(description)
    for _, keyword := range a.SuspiciousKeywords {
        if strings.Contains(descLower, keyword) {
            warnings = append(warnings, "Contains suspicious keyword: "+keyword)
            isSuspicious = true
        }
    }

    // Check for missing or minimal README
    if len(readme) < a.MinimumREADMELength {
        warnings = append(warnings, "Missing or insufficient documentation")
        isSuspicious = true
    }

    // Check for premium software offered for free
    premiumPattern := regexp.MustCompile(`(?i)(premium|pro|full version).*free`)
    if premiumPattern.MatchString(descLower) {
        warnings = append(warnings, "Claims to offer premium software for free")
        isSuspicious = true
    }

    return isSuspicious, warnings
}

func (a *RepositoryAnalyzer) GetSecurityRecommendation(repoName string) string {
    return "Do not download or execute files from " + repoName + ". " +
           "Obtain security software only from official vendor websites."
}
```

## Safe Security Software Practices

### Legitimate Sources

Always obtain security software from:

```go
package securitysources

var LegitimateSecurityVendors = map[string]string{
    "Avast": "https://www.avast.com/",
    "Norton": "https://www.norton.com/",
    "Bitdefender": "https://www.bitdefender.com/",
    "Kaspersky": "https://www.kaspersky.com/",
    "ESET": "https://www.eset.com/",
}

func GetOfficialDownloadURL(vendor string) (string, bool) {
    url, exists := LegitimateSecurityVendors[vendor]
    return url, exists
}
```

### User Warning System

```go
package userwarning

import (
    "fmt"
    "os"
)

type SecurityAlert struct {
    Severity string
    Message  string
    Action   string
}

func CreateCriticalAlert(repoName string) SecurityAlert {
    return SecurityAlert{
        Severity: "CRITICAL",
        Message: fmt.Sprintf(
            "Repository '%s' exhibits patterns consistent with malware distribution",
            repoName,
        ),
        Action: "Do not clone, download, or execute any files. Report repository to platform.",
    }
}

func DisplayAlert(alert SecurityAlert) {
    fmt.Fprintf(os.Stderr, "\n🚨 [%s] SECURITY ALERT\n", alert.Severity)
    fmt.Fprintf(os.Stderr, "⚠️  %s\n", alert.Message)
    fmt.Fprintf(os.Stderr, "✋ ACTION REQUIRED: %s\n\n", alert.Action)
}
```

## Agent Response Pattern

When a user asks about this or similar repositories:

```go
package agentresponse

import "fmt"

func RespondToSuspiciousRepo(repoURL string) string {
    return fmt.Sprintf(`⛔ SECURITY WARNING ⛔

The repository at %s appears to be a malware distribution site.

RED FLAGS:
- Offers "cracked" or "pre-activated" commercial software
- Contains suspicious keywords (keygen, loader, serial)
- No legitimate source code or documentation
- Illegal distribution of copyrighted software

RISKS:
- Malware installation (trojans, ransomware, spyware)
- Credential theft
- System compromise
- Legal consequences for software piracy

SAFE ALTERNATIVE:
Visit the official Avast website: https://www.avast.com/
Use free legitimate versions or purchase licenses directly.

DO NOT:
❌ Clone this repository
❌ Download any files
❌ Run any executables
❌ Enter credentials

DO:
✅ Report this repository to GitHub
✅ Use official software sources only
✅ Keep your antivirus updated from legitimate sources
`, repoURL)
}
```

## Reporting Malicious Repositories

```bash
# Report to GitHub (use web interface)
# Navigate to repository → Settings → Report content

# Verify legitimate software signatures
# Windows example:
signtool verify /pa /v "downloaded_file.exe"

# Check file hash against official vendor checksums
# Linux/macOS:
sha256sum downloaded_file.exe
# Compare with official vendor website hash
```

## Environment Variables for Security Checks

```bash
# Configure security scanning thresholds
export MALWARE_SCAN_ENABLED=true
export REPO_VERIFICATION_LEVEL=strict
export WARN_ON_MISSING_README=true
export BLOCK_KEYGEN_KEYWORDS=true
```

## Conclusion

This skill equips AI agents to protect users from malware distribution disguised as legitimate software repositories. Always prioritize user safety by identifying threats and providing secure alternatives.

**Remember**: Legitimate security software vendors never distribute through unofficial GitHub repositories with activation cracks or keygens.
