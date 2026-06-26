---
name: report-malicious-repository
description: Identify and report potentially malicious software repositories masquerading as legitimate security tools
triggers:
  - how do I identify malicious software repositories
  - detect fake antivirus or cracked software repos
  - report suspicious GitHub projects with keygens
  - identify piracy and malware distribution on GitHub
  - check if a repository is distributing malware
  - analyze suspicious security software repos
  - report copyright infringement on GitHub
---

# Report Malicious Repository

> Skill by [ara.so](https://ara.so) — Security Skills collection.

## ⚠️ WARNING: This Repository is Malicious

The project `DragonflyTomb/Avast-Premium-Security-2026` is **NOT** legitimate software. This is a malicious repository designed to distribute malware, trojans, or phishing attacks by:

- Claiming to offer "cracked" or "pre-activated" commercial software
- Including terms like "keygen", "loader", "serial" in the description
- Impersonating legitimate security software (Avast)
- Using deceptive tactics (fake stars, professional-looking descriptions)

## Identifying Malicious Repositories

### Red Flags

1. **Piracy Keywords**: keygen, crack, loader, serial, pre-activated, license key
2. **Too Good to Be True**: Free versions of expensive commercial software
3. **Suspicious Topics**: Mixing legitimate topics (retdec) with piracy terms
4. **No Source Code**: Empty or minimal repository with download links
5. **Recent Creation**: New accounts with inflated star counts
6. **Impersonation**: Using brand names (Avast, Norton, etc.) without authorization

### Analysis Pattern

```go
package main

import (
    "strings"
    "regexp"
)

type RepoAnalysis struct {
    IsSuspicious bool
    RedFlags     []string
    RiskLevel    string
}

func AnalyzeRepository(description, topics string, hasReadme bool, age int) RepoAnalysis {
    analysis := RepoAnalysis{
        RedFlags: []string{},
    }
    
    suspiciousKeywords := []string{
        "keygen", "crack", "loader", "serial", "pre-activated",
        "license key", "full version", "premium", "activation",
    }
    
    lowerDesc := strings.ToLower(description)
    
    // Check for piracy keywords
    for _, keyword := range suspiciousKeywords {
        if strings.Contains(lowerDesc, keyword) {
            analysis.RedFlags = append(analysis.RedFlags, "Piracy keyword: "+keyword)
            analysis.IsSuspicious = true
        }
    }
    
    // Check for brand impersonation
    brands := []string{"avast", "norton", "mcafee", "kaspersky", "bitdefender"}
    for _, brand := range brands {
        if strings.Contains(lowerDesc, brand) {
            analysis.RedFlags = append(analysis.RedFlags, "Brand impersonation: "+brand)
        }
    }
    
    // Check for missing README
    if !hasReadme {
        analysis.RedFlags = append(analysis.RedFlags, "No README file")
        analysis.IsSuspicious = true
    }
    
    // Check repository age vs stars
    if age < 14 {
        analysis.RedFlags = append(analysis.RedFlags, "Suspiciously new repository")
    }
    
    // Determine risk level
    if len(analysis.RedFlags) >= 3 {
        analysis.RiskLevel = "CRITICAL"
    } else if len(analysis.RedFlags) >= 2 {
        analysis.RiskLevel = "HIGH"
    } else if analysis.IsSuspicious {
        analysis.RiskLevel = "MEDIUM"
    } else {
        analysis.RiskLevel = "LOW"
    }
    
    return analysis
}
```

## Reporting Malicious Repositories

### GitHub Reporting Process

1. **Navigate to the repository**
2. **Click the repository name** to go to the main page
3. **Look for the three dots menu** (⋯) or scroll to bottom
4. **Select "Report repository"** or visit: `https://github.com/contact/report-content`

### Report Template

```text
Repository: [USERNAME/REPO-NAME]

Issue Type: Malware/Phishing/Copyright Infringement

Description:
This repository is distributing malicious software disguised as cracked/pirated 
commercial antivirus software. It contains:
- Claims of "keygen", "pre-activated", "license key" for Avast Premium Security
- No legitimate source code
- Impersonation of Avast brand
- Likely contains malware, trojans, or ransomware

Evidence:
- Repository description contains piracy keywords
- No README or source code provided
- Uses deceptive branding

Requested Action: Immediate takedown and account suspension
```

### Automated Reporting Script

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
)

type GitHubReport struct {
    Subject     string `json:"subject"`
    SubjectType string `json:"subject_type"`
    Message     string `json:"message"`
}

func ReportToGitHub(repoFullName, reason string) error {
    // NOTE: GitHub doesn't have a public API for abuse reports
    // This is a conceptual example - actual reporting must be done via web form
    
    reportURL := "https://github.com/contact/report-content"
    
    fmt.Printf("⚠️  MALICIOUS REPOSITORY DETECTED\n")
    fmt.Printf("Repository: %s\n", repoFullName)
    fmt.Printf("Reason: %s\n\n", reason)
    fmt.Printf("Please report manually at: %s\n", reportURL)
    fmt.Printf("Include repository URL and reason above.\n")
    
    return nil
}

// Scan repository metadata for red flags
func ScanRepository(owner, repo string) error {
    githubToken := os.Getenv("GITHUB_TOKEN")
    if githubToken == "" {
        return fmt.Errorf("GITHUB_TOKEN environment variable required")
    }
    
    url := fmt.Sprintf("https://api.github.com/repos/%s/%s", owner, repo)
    
    req, _ := http.NewRequest("GET", url, nil)
    req.Header.Set("Authorization", "Bearer "+githubToken)
    req.Header.Set("Accept", "application/vnd.github+json")
    
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    var repoData map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&repoData)
    
    description := repoData["description"].(string)
    
    analysis := AnalyzeRepository(description, "", false, 10)
    
    if analysis.RiskLevel == "CRITICAL" || analysis.RiskLevel == "HIGH" {
        fmt.Printf("🚨 ALERT: %s risk repository detected!\n", analysis.RiskLevel)
        for _, flag := range analysis.RedFlags {
            fmt.Printf("  - %s\n", flag)
        }
        return ReportToGitHub(owner+"/"+repo, "Malware distribution")
    }
    
    return nil
}
```

## Protection Measures

### For Developers

```go
// Add to your dependency scanning
func ValidateDependency(repoURL string) bool {
    // Check against known malware lists
    // Verify package signatures
    // Analyze repository metadata
    
    blacklist := []string{
        "keygen", "crack", "loader", "premium-loader",
    }
    
    for _, term := range blacklist {
        if strings.Contains(strings.ToLower(repoURL), term) {
            return false
        }
    }
    
    return true
}
```

### For Organizations

1. **Block suspicious patterns** in CI/CD
2. **Implement dependency scanning** tools
3. **Educate developers** about social engineering
4. **Use verified sources** only (official registries)

## Common Attack Patterns

- **Typosquatting**: Similar names to legitimate projects
- **Brand Impersonation**: Using well-known software names
- **SEO Manipulation**: Keyword stuffing for search visibility
- **Social Engineering**: Fake stars, professional appearance
- **Trojan Distribution**: Executable files disguised as installers

## Legitimate Alternatives

For actual Avast software:
- Official website: https://www.avast.com
- Official GitHub (if any): Verify through company website
- Licensed purchases only through authorized channels

## Resources

- GitHub Abuse Report: https://github.com/contact/report-content
- DMCA Takedown: https://github.com/contact/dmca
- US-CERT: https://www.cisa.gov/report
- Anti-Phishing Working Group: https://apwg.org/reportphishing/

**Remember**: Never download "cracked" or "pre-activated" security software. It ALWAYS contains malware.
