# M11 - Vendor Advisories, Patches & Patch Diff

**Purpose:** Find authoritative vendor advisories, affected/fixed versions, patch commits, and
workarounds. Use patch diffs to understand root cause and build detection, without weaponizing.

**Triggers:** vendor advisory, security advisory, security bulletin, patch, patch diff, MSRC,
PSIRT, release notes, changelog, CVE bulletin, fixed version, workaround, security update,
"is it patched", "affected versions", CNCERT, 腾讯安全, 阿里云安全, 绿盟, 深信服, 启明星辰.

**Process contract:** Always run the Universal Search Loop (Section 1) and the Process Compliance
Gate (Section 0.5). This module supplies sources and queries only.

---

## Primary sources

### Major vendor advisory portals
| Vendor | Portal |
|---|---|
| Microsoft | `msrc.microsoft.com/update-guide`, Security Update Guide |
| Cisco | `sec.cloudapps.cisco.com/security/center/publicationListing.x` |
| Fortinet | `fortiguard.com/psirt` |
| Ivanti | `forums.ivanti.com` / security advisories |
| VMware / Broadcom | Broadcom security advisories |
| Atlassian | `confluence.atlassian.com/security-advisories` |
| Oracle | Critical Patch Updates |
| Adobe | `helpx.adobe.com/security.html` |
| Google Chrome | `chromereleases.googleblog.com` |
| Android | `source.android.com/docs/security/bulletin` |
| Apple | `support.apple.com/en-us/100100` (security releases) |
| AWS | Security Bulletins |
| GitHub | `github.com/advisories` |
| Kubernetes | `kubernetes.io/blog` / security releases |
| Docker | Security advisories |
| OpenSSL | `openssl.org/news/vulnerabilities.html` |
| Linux kernel | `kernel.org` CVE page / stable releases |
| Jenkins / GitLab / WordPress | Respective security pages |

### Chinese CERT and vendor portals
- **CNCERT/CC** (`cert.org.cn`) - China national incident advisories and malware/event reports.
- **Tencent Security Response Center** (`security.tencent.com`) and **Alibaba Cloud Security**
  (`security.alibaba.com`) - Chinese cloud/vendor advisories and SRC notices.
- **NSFOCUS** (`nsfocus.com.cn`), **Sangfor** (`sangfor.com.cn`), **Venustech**
  (`venustech.com.cn`) - Chinese vendor advisories and threat research.
- Chinese advisories may use local vulnerability IDs (CNVD/CNNVD) rather than CVE; map them to the
  CVE and vendor record before relying on affected/fixed versions.

### Distribution and package sources
- Debian Security Tracker (`security-tracker.debian.org`).
- Ubuntu CVE tracker (`ubuntu.com/security/cves`).
- Red Hat Security Advisories (`access.redhat.com/security/security-updates`).
- SUSE, Alpine, Amazon Linux advisories.
- OSV, GitHub Advisories, Snyk, Trivy DB, Grype DB.

### Patch and diff
- Vendor commit links in advisories.
- GitHub compare/commit views, release tags, security branches.
- Backport commits in distro repositories.
- Release notes and changelogs (search "security", "CVE", "fix").

---

## Query recipes

```text
# Vendor advisory
site:msrc.microsoft.com "CVE-2024"
site:sec.cloudapps.cisco.com "advisory" "CVE"
site:fortiguard.com/psirt "CVE"
site:github.com/advisories "package"
site:openssl.org "vulnerabilities" "CVE"
site:kubernetes.io "security release"
site:cert.org.cn "CVE-2024-3400"
site:security.tencent.com "CVE-2024-3400"
site:security.alibaba.com "CVE-2024-3400"
site:nsfocus.com.cn "CVE-2024-3400"

# Patch and fixed version
"CVE-2024-3400" "fixed in"
"CVE-2024-3400" "patch"
"CVE-2024-3400" commit
site:github.com "CVE-2024-3400" "fix"
"security update" "release notes" "CVE"
"changelog" "security fix" "version"

# Distribution trackers
site:security-tracker.debian.org "CVE-2024-3400"
site:ubuntu.com/security "CVE-2024-3400"
site:access.redhat.com "CVE-2024-3400"

# Workarounds
"CVE-2024-3400" workaround
"CVE-2024-3400" mitigation
"CVE-2024-3400" "no patch"
```

---

## Workflow

1. **Identify the exact product and version.** Build, edition, module, and deployment model matter.
2. **Find the authoritative advisory.** Prefer the vendor PSIRT over aggregators.
3. **Extract affected/fixed versions.** Note backports and EOL products.
4. **Find the patch commit or diff.** Identify the vulnerable function and the fix.
5. **Assess exploitability.** Compare with M3: KEV, EPSS, public PoC, prerequisites.
6. **Check workarounds.** Config changes, feature disabling, WAF rules, network restrictions.
7. **Map detection.** What telemetry would show exploitation or vulnerable configuration?
8. **Recommend action.** Patch, mitigate, monitor, or accept with rationale.
9. **Verify.** Confirm the fixed version in a lab; check that the patch actually blocks the PoC.

---

## What to extract

| Field | Example |
|---|---|
| Advisory ID | Vendor-SA-2024-001 |
| CVE | CVE-2024-XXXX |
| Severity | Critical (CVSS 9.8) |
| Affected | 1.0.0 - 1.2.3 |
| Fixed | 1.2.4 |
| Patch | commit hash / diff summary |
| Workaround | disable feature X |
| Detection | log pattern, request signature |
| Confidence | A (vendor + patch + lab) |

---

## Pitfalls

- **Silent fixes.** Some vendors patch without a CVE; compare versions and changelogs.
- **Backports.** A distro may patch an older version without bumping upstream.
- **Version mapping.** Vendor version strings differ from package versions.
- **EOL products.** No patch will come; mitigation is the only option.
- **Severity inflation.** Vendor CVSS may not reflect your configuration.
- **Incomplete advisories.** Details may be withheld until disclosure.
- **Patch diff reverse-engineering** can enable exploitation; keep it defensive and authorized.

---

## Ethics

- Use patches and diffs to defend, detect, and verify - not to weaponize.
- Do not publish exploit details before the coordinated disclosure date.
- Respect vendor terms and embargoes.
- Verify fixes in a lab; do not test on production without change control.

---

## Output contract

```
module:        M11 Vendor Advisories
objective:     determine patch/mitigation status for <product/CVE>
authorization: public advisory / owned systems
sources_used:  vendor PSIRT, distro tracker, patch commit, release notes, mapped to the claim it supports
sources_read:  URLs opened but excluded, with reason (off-scope, stale, duplicate, low confidence, inaccessible, discovery only)
findings:      affected/fixed versions, patch, workaround, detection
pivots:        M3 PoC, M8 reproduction, M6 secure code
caveats:       backports, EOL, incomplete advisory, confidence
```
