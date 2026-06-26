---
name: releaseguard
description: Scan, harden, sign, and verify release artifacts with ReleaseGuard — the artifact policy engine for dist/ and release/ outputs.
homepage: https://github.com/Helixar-AI/ReleaseGuard
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["releaseguard"],"env":[]}}}
---

# ReleaseGuard Skill

ReleaseGuard is an artifact policy engine. Use it to scan build outputs for secrets, misconfigurations, and supply-chain risks; harden and fix them; generate SBOMs; sign artifacts; and verify release integrity.

## Install ReleaseGuard

**Preferred — Homebrew (macOS / Linux, no remote script execution):**

```bash
brew install Helixar-AI/tap/releaseguard
```

**Alternative — manual download from GitHub Releases (review before running):**

```bash
# 1. Review the install script before executing:
curl -sSfL https://raw.githubusercontent.com/Helixar-AI/ReleaseGuard/main/scripts/install.sh | less

# 2. If satisfied, run it:
curl -sSfL https://raw.githubusercontent.com/Helixar-AI/ReleaseGuard/main/scripts/install.sh | sh
```

**Alternative — direct binary download (no shell script):**

```bash
# Replace VERSION, OS, and ARCH as appropriate (linux/darwin, amd64/arm64)
curl -sSfL https://github.com/Helixar-AI/ReleaseGuard/releases/latest/download/releaseguard-VERSION-OS-ARCH.tar.gz \
  | tar -xz releaseguard
sudo mv releaseguard /usr/local/bin/releaseguard
```

> **Note:** The install script is MIT-licensed and open-source at
> https://github.com/Helixar-AI/ReleaseGuard/blob/main/scripts/install.sh
> Review it before executing in sensitive environments.

---

## External Services

Some commands interact with external services. This is documented per-command below. No data is sent externally unless you explicitly invoke the relevant flag or mode:

| Feature | External Service | Triggered by |
|---|---|---|
| CVE enrichment | OSV.dev (read-only, no auth) | `sbom --enrich-cve` or `vex` |
| Keyless signing | Sigstore / Fulcio (requires OIDC token) | `sign --mode keyless` |
| Cloud obfuscation | ReleaseGuard Cloud API | `obfuscate --level medium/aggressive` |
| SLSA Provenance L3 | ReleaseGuard Cloud API | Cloud plan only |

**Credentials:** Keyless signing requires an OIDC token (available in GitHub Actions, GitLab CI, etc.). Local signing requires a private key file you supply with `--key`. Cloud features require `RELEASEGUARD_CLOUD_TOKEN`. No credentials are used by default for `check`, `fix`, `sbom`, `pack`, `report`, or `verify`.

---

## Commands

### Check / Scan — `releaseguard check <path>`

Scan an artifact path and evaluate the release policy. **No external network calls.**

**Trigger phrases:** "scan", "check", "audit", "analyze release", "inspect dist", "any secrets", "find vulnerabilities"

```bash
releaseguard check <path>
releaseguard check <path> --format json
releaseguard check <path> --format sarif --out results.sarif
releaseguard check <path> --format markdown --out report.md
```

- Default format: `cli` (human-readable)
- Other formats: `json`, `sarif`, `markdown`, `html`
- Exit code 0 = PASS, non-zero = FAIL

---

### Fix — `releaseguard fix <path>`

Apply safe, deterministic hardening transforms. **No external network calls.**

**Trigger phrases:** "fix", "harden", "apply fixes", "remediate", "auto-fix release"

```bash
releaseguard fix <path>
releaseguard fix <path> --dry-run   # preview without applying
```

---

### SBOM — `releaseguard sbom <path>`

Generate a Software Bill of Materials.

**Trigger phrases:** "sbom", "software bill of materials", "dependencies", "generate bom"

```bash
releaseguard sbom <path>                     # no network calls
releaseguard sbom <path> --format spdx
releaseguard sbom <path> --enrich-cve        # fetches CVE data from OSV.dev (read-only)
```

- Default format: `cyclonedx`
- `--enrich-cve` makes read-only requests to OSV.dev; no credentials required

---

### Obfuscate — `releaseguard obfuscate <path>`

Apply obfuscation to release artifacts.

**Trigger phrases:** "obfuscate", "strip symbols", "protect binary"

```bash
releaseguard obfuscate <path> --level light   # OSS — no network calls
releaseguard obfuscate <path> --level medium  # requires RELEASEGUARD_CLOUD_TOKEN
releaseguard obfuscate <path> --dry-run
```

Levels:
- `none` / `light` — local, no external calls (OSS)
- `medium` / `aggressive` — calls ReleaseGuard Cloud API; requires `RELEASEGUARD_CLOUD_TOKEN`

---

### Harden — `releaseguard harden <path>`

Full hardening pipeline: fix + obfuscate + DRM injection.

**Trigger phrases:** "full harden", "harden release", "full hardening pipeline"

```bash
releaseguard harden <path> --obfuscation light    # no network calls
releaseguard harden <path> --obfuscation medium   # requires RELEASEGUARD_CLOUD_TOKEN
releaseguard harden <path> --dry-run
```

---

### Pack — `releaseguard pack <path>`

Package an artifact into a canonical archive. **No external network calls.**

**Trigger phrases:** "pack", "package artifact", "create archive"

```bash
releaseguard pack <path> --out release.tar.gz
releaseguard pack <path> --out release.zip --format zip
```

---

### Sign — `releaseguard sign <artifact>`

Sign an artifact and its evidence bundle.

**Trigger phrases:** "sign", "cosign", "keyless sign", "sign artifact"

```bash
# Keyless (Sigstore/Fulcio) — requires OIDC token; use in CI environments
releaseguard sign <artifact> --mode keyless

# Local signing — no external calls; requires private key file
releaseguard sign <artifact> --mode local --key signing.key
```

- `keyless` mode contacts Sigstore's Fulcio CA and Rekor transparency log
- `local` mode is fully offline; key stays on disk

---

### Attest — `releaseguard attest <artifact>`

Emit in-toto and SLSA provenance attestations.

**Trigger phrases:** "attest", "provenance", "slsa", "in-toto"

```bash
releaseguard attest <artifact>
```

---

### Verify — `releaseguard verify <artifact>`

Verify artifact signatures and policy compliance. **No credentials required for verification.**

**Trigger phrases:** "verify", "check signature", "validate artifact"

```bash
releaseguard verify <artifact>
```

---

### Report — `releaseguard report <path>`

Export a scan report. **No external network calls.**

**Trigger phrases:** "report", "export report", "compliance report"

```bash
releaseguard report <path> --format sarif --out results.sarif
releaseguard report <path> --format html --out report.html
```

---

### VEX — `releaseguard vex <path>`

Enrich SBOM with VEX vulnerability data. **Makes read-only requests to OSV.dev.**

**Trigger phrases:** "vex", "vulnerability data", "enrich sbom"

```bash
releaseguard vex <path> --sbom .releaseguard/sbom.cdx.json --out vex.json
```

---

## Typical Workflows

### Quick scan (no network, no credentials)
```bash
releaseguard check ./dist
```

### Full pipeline (CI with keyless signing)
```bash
releaseguard check ./dist
releaseguard fix ./dist
releaseguard sbom ./dist
releaseguard pack ./dist --out release.tar.gz
releaseguard sign release.tar.gz --mode keyless   # OIDC token required
releaseguard attest release.tar.gz
releaseguard verify release.tar.gz
```

### Offline pipeline (no network, local key)
```bash
releaseguard check ./dist
releaseguard fix ./dist
releaseguard sbom ./dist
releaseguard pack ./dist --out release.tar.gz
releaseguard sign release.tar.gz --mode local --key signing.key
```

---

## Configuration

```bash
releaseguard init   # creates .releaseguard.yml
```

```yaml
# .releaseguard.yml
version: 2
scanning:
  exclude_paths:
    - test/fixtures
policy:
  fail_on: [critical, high]
```
