---
name: shipcheck
description: |
  Pre-ship safety net. Scan an npm package, OpenClaw skill folder, or git repo BEFORE publishing
  to catch personal info leaks (absolute home paths, emails, internal IPs / Tailscale hostnames,
  private project codenames, AWS/GitHub/OpenAI/Anthropic/Slack tokens, JWT, PEM/SSH keys, soft
  Chinese first-person NL leaks in markdown). Best-effort PII/secret checkup — NOT a replacement
  for manual review or a full secret scanner. Use when the user is about to `npm publish` /
  `clawhub publish` / push a public GitHub repo, or asks "is it safe to share this?", "check
  leaks", "扫一下个人信息", "发布前体检", "shipcheck".
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["shipcheck"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "@symbolstar/shipcheck",
              "bins": ["shipcheck"],
              "label": "Install shipcheck CLI (npm)",
            },
          ],
      },
  }
---

# shipcheck — pre-publish PII & secret check

`shipcheck` is a best-effort pre-publish safety net. Run it **before** `npm publish`,
`clawhub publish`, or pushing a repo public to catch the stuff you'll regret shipping:
absolute `/Users/<you>/` paths, internal IPs, Tailscale hostnames, API keys, internal
project codenames, and soft natural-language personal leaks in markdown.

It is **NOT**:

- a replacement for manual review
- a full secret scanner (gitleaks / trufflehog cover more)
- a security audit

It is one more pair of eyes before you hit publish.

## When to use this skill

Trigger this skill when the user is about to publish or push something public:

- `npm publish` / `npm publish --dry-run`
- `clawhub publish ./my-skill ...`
- `git push` to a brand-new public repo
- "check leaks", "is it safe to share?", "扫一下个人信息", "发布前体检"

## Install

```bash
npm i -g @symbolstar/shipcheck
# or one-shot
npx -y @symbolstar/shipcheck
```

## Run

### npm package (default mode)

Scans only files that would actually be published — resolves `package.json.files`,
`.npmignore`, `.gitignore` statically (does **not** invoke `npm pack`).

```bash
cd /path/to/npm-package
shipcheck
```

### Skill folder / generic repo

```bash
shipcheck --scan-mode=dir ./path/to/skill-or-repo
```

### Common flags

```bash
shipcheck --scan-mode=dir|npm     # default: npm
shipcheck --allow <id>            # acknowledge a finding by id
shipcheck --config ./shipcheck.config.json
```

## What it catches

| Category   | Examples                                                                                                     | Severity   |
| ---------- | ------------------------------------------------------------------------------------------------------------ | ---------- |
| `secrets`  | AWS keys, GitHub PAT (`ghp_/gho_/ghu_/ghs_/ghr_`), OpenAI `sk-…`, Anthropic `sk-ant-…`, Google `AIza…`, Slack `xox[bp]-…`, JWT, PEM/SSH private keys (~30 rules) | `critical` |
| `identity` | Emails, China mobile + E.164, `/Users/<name>/` & `/home/<name>/` absolute paths, SSH fingerprint              | `high`     |
| `infra`    | RFC1918 IPs, Tailscale CGNAT `100.64/10`, `*.tail<id>.ts.net`, `*.lan`/`*.local`, private git remotes         | `high`     |
| `business` | User-defined `forbidden_terms` from `shipcheck.config.json` (codenames, internal product names…)             | `medium`   |
| `softNL`   | Chinese first-person personal context in `*.md` (我家 / 我老板 / 我同事 + 关系词)                              | `info`     |
| `binaries` | `*.png/.jpg/.mp4/.zip/.pdf` > 50 KB inside the publish set                                                    | `warn`     |

## Recommended workflow

```bash
# 1. Run it
shipcheck                       # or: shipcheck --scan-mode=dir .

# 2. Triage findings
#    - real leak → fix the file
#    - false positive → add to shipcheck.config.json allow / forbidden_terms

# 3. Re-run until 0 critical / high
shipcheck

# 4. Publish
npm publish    # or: clawhub publish ./skill --slug ...
```

## Exit codes

| Code | Meaning                                                            |
| ---- | ------------------------------------------------------------------ |
| `0`  | No findings, or only allow-listed / `info` / `warn`                |
| `1`  | One or more `critical` / `high` / `medium` findings — do **not** ship |

Use the exit code in CI or `prepublishOnly`:

```json
{
  "scripts": {
    "prepublishOnly": "shipcheck && npm run build && npm test"
  }
}
```

## Configuration (optional)

`shipcheck.config.json` in the project root:

```json
{
  "forbidden_terms": ["AcmeInternalCodename", "ProjectStarfish"],
  "allow": [
    "rule:identity.absolute-home:fixtures/golden/01/setup.md#L12"
  ],
  "scanMode": "npm"
}
```

## Links

- npm: <https://www.npmjs.com/package/@symbolstar/shipcheck>
- source: <https://github.com/SymbolStar/shipcheck> _(public mirror — main dev on local repo)_
- author: SymbolStar
