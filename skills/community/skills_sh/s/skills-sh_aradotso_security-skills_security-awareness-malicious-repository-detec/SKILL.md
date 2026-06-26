---
name: security-awareness-malicious-repository-detection
description: Detect and analyze potentially malicious repositories disguising as legitimate software cracks or pirated tools
triggers:
  - identify malicious repository patterns
  - detect fake software crack repository
  - analyze suspicious github project
  - check for malware distribution repo
  - verify legitimate security software
  - investigate piracy-themed malware
  - scan repository for threat indicators
  - evaluate software crack legitimacy
---

# Security Awareness: Malicious Repository Detection

> Skill by [ara.so](https://ara.so) — Security Skills collection.

## ⚠️ CRITICAL WARNING

**This repository is a MALICIOUS PROJECT distributing malware disguised as cracked security software.**

### Threat Indicators Present

1. **Impersonation**: Claims to be "Bitdefender Total Security Crack" - legitimate security vendors do not distribute cracks
2. **Suspicious Topics**: Includes "defender-bypass", "thread-hijacking", "exploit-mitigation" alongside crack-related terms
3. **Star Manipulation**: 59 stars at 3 stars/day suggests artificial inflation
4. **No Legitimate Code**: No README, likely contains payload downloaders
5. **Red Flag Language**: "Pre-Activated", "Keygen Loader", "Crack" combined with antivirus software
6. **Future Dating**: Created date shows 2026 (timestamp manipulation or test data)

## What This Actually Is

This is a **malware distribution vector** using common social engineering tactics:

- **Lure**: Free premium security software
- **Method**: Fake crack/keygen
- **Payload**: Likely infostealers, ransomware, or backdoors
- **Target**: Users searching for pirated antivirus software

## Detection Patterns

### Repository Red Flags

```go
package detector

import (
    "strings"
    "regexp"
)

type ThreatIndicators struct {
    SuspiciousKeywords []string
    MaliciousPatterns  []string
    RiskScore         int
}

func AnalyzeRepository(description, topics []string) ThreatIndicators {
    indicators := ThreatIndicators{}
    
    // Crack/Piracy keywords
    crackKeywords := []string{
        "crack", "keygen", "pre-activated", "activation",
        "loader", "full version", "license key", "bypass",
    }
    
    // Technical exploit terms
    exploitTerms := []string{
        "defender-bypass", "thread-hijacking", "rootkit",
        "exploit-mitigation", "heuristic-analysis",
    }
    
    descLower := strings.ToLower(description)
    
    for _, keyword := range crackKeywords {
        if strings.Contains(descLower, keyword) {
            indicators.SuspiciousKeywords = append(indicators.SuspiciousKeywords, keyword)
            indicators.RiskScore += 15
        }
    }
    
    for _, term := range exploitTerms {
        for _, topic := range topics {
            if strings.Contains(strings.ToLower(topic), term) {
                indicators.MaliciousPatterns = append(indicators.MaliciousPatterns, term)
                indicators.RiskScore += 20
            }
        }
    }
    
    // Legitimate security software being "cracked"
    legitimateSoftware := []string{"bitdefender", "kaspersky", "norton", "mcafee"}
    for _, software := range legitimateSoftware {
        if strings.Contains(descLower, software) && strings.Contains(descLower, "crack") {
            indicators.RiskScore += 30
        }
    }
    
    return indicators
}

func IsMalicious(indicators ThreatIndicators) bool {
    return indicators.RiskScore >= 50
}
```

### Usage Example

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    description := "Bitdefender Total Security Crack 2026 | Full Version License Key Pre-Activated"
    topics := []string{
        "bitdefender",
        "defender-bypass",
        "thread-hijacking",
        "malware-scanner",
    }
    
    indicators := AnalyzeRepository(description, topics)
    
    fmt.Printf("Risk Score: %d\n", indicators.RiskScore)
    fmt.Printf("Suspicious Keywords: %v\n", indicators.SuspiciousKeywords)
    fmt.Printf("Malicious Patterns: %v\n", indicators.MaliciousPatterns)
    
    if IsMalicious(indicators) {
        fmt.Println("\n⚠️  HIGH RISK: This repository exhibits malware distribution patterns")
        fmt.Println("DO NOT download or execute any files from this source")
        os.Exit(1)
    }
}
```

## Automated Scanning

```go
package scanner

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
)

type GitHubRepo struct {
    Description string   `json:"description"`
    Topics      []string `json:"topics"`
    Stars       int      `json:"stargazers_count"`
    CreatedAt   string   `json:"created_at"`
    Language    string   `json:"language"`
}

func ScanGitHubRepo(owner, repo string) (*ThreatIndicators, error) {
    apiURL := fmt.Sprintf("https://api.github.com/repos/%s/%s", owner, repo)
    
    req, _ := http.NewRequestWithContext(context.Background(), "GET", apiURL, nil)
    req.Header.Set("Accept", "application/vnd.github.v3+json")
    
    // Use GitHub token if available
    if token := os.Getenv("GITHUB_TOKEN"); token != "" {
        req.Header.Set("Authorization", "Bearer "+token)
    }
    
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var repoData GitHubRepo
    if err := json.NewDecoder(resp.Body).Decode(&repoData); err != nil {
        return nil, err
    }
    
    indicators := AnalyzeRepository(repoData.Description, repoData.Topics)
    
    // Additional checks
    if repoData.Stars > 0 {
        // Rapid star growth can indicate manipulation
        indicators.MaliciousPatterns = append(indicators.MaliciousPatterns, "potential-star-manipulation")
    }
    
    return &indicators, nil
}
```

## Protection Recommendations

### For Developers

```go
// Add to your CI/CD pipeline
package main

func PreCommitCheck() {
    blockedPatterns := []string{
        "crack", "keygen", "pirate", "warez",
        "bypass", "nulled", "pre-activated",
    }
    
    // Check repository description and README
    for _, pattern := range blockedPatterns {
        // Implement scanning logic
        fmt.Printf("Scanning for pattern: %s\n", pattern)
    }
}
```

### For Users

**NEVER**:
- Download "cracked" security software
- Execute files from repositories like this
- Disable antivirus to run "activators"
- Trust repositories with no legitimate code

**ALWAYS**:
- Use official software sources
- Verify publisher signatures
- Check repository legitimacy
- Report malicious repositories

## Reporting Malicious Repositories

```bash
# Report to GitHub
# Visit: https://github.com/contact/report-abuse

# Report to security vendors
# Bitdefender: https://www.bitdefender.com/consumer/support/
# Microsoft: https://www.microsoft.com/en-us/wdsi/support/report-unsafe-site
```

## Legitimate Alternatives

```go
package alternatives

// How to actually get security software safely
type LegitimateSource struct {
    Vendor   string
    URL      string
    FreeTier bool
}

var LegitSources = []LegitimateSource{
    {Vendor: "Bitdefender", URL: "https://www.bitdefender.com", FreeTier: true},
    {Vendor: "Windows Defender", URL: "Built-in", FreeTier: true},
    {Vendor: "Malwarebytes", URL: "https://www.malwarebytes.com", FreeTier: true},
}
```

## Educational Purpose

This skill exists to **educate developers and AI agents** about identifying malicious repositories that:

1. Impersonate legitimate software
2. Use SEO-optimized descriptions to appear in searches
3. Distribute malware through social engineering
4. Target users seeking pirated software

**The original repository should be avoided entirely and reported to GitHub.**
