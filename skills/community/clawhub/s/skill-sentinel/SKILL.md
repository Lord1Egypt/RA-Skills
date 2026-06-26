---
name: clawshield
description: Scan OpenClaw skill directories for high-signal security risks such as download-and-execute chains, obfuscated execution, and suspicious callbacks.
homepage: https://github.com/mike007jd/openclaw-skills/tree/main/clawshield
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["node"]}}}
---

# ClawShield

Scan a skill directory without executing it and return a risk level that can be enforced in review or CI.

## When to use

- You want a fast static review before installing or publishing a skill.
- You need machine-readable findings for CI or release gates.
- You want a narrow ruleset aimed at common high-risk supply-chain patterns.

## Command

```bash
node {baseDir}/bin/clawshield.js scan /path/to/skill --format table
node {baseDir}/bin/clawshield.js scan /path/to/skill --format json
node {baseDir}/bin/clawshield.js scan /path/to/skill --format sarif > clawshield.sarif
node {baseDir}/bin/clawshield.js scan /path/to/skill --format table --fail-on caution
```

## Rules

| Rule ID | Severity | Description |
| --- | --- | --- |
| CS001_CURL_PIPE_SH | high | `curl` or `wget` piped directly into a shell |
| CS002_OBFUSCATED_EXEC | high | obfuscated or dynamic execution such as `eval`, `new Function`, or base64 decode flows |
| CS003_SUSPICIOUS_CALLBACK | medium | suspicious outbound callback endpoints such as raw IPs, ngrok, or webhook collectors |
| CS004_SOCIAL_ENGINEERING_PROMPT | medium | instructions that pressure users to bypass safety controls |
| CS005_SHELL_WRAPPER_EXEC | high | `bash -c` wrappers that hide remote execution |

## Risk levels

- **Safe**: no findings after suppressions
- **Caution**: one or more medium-severity findings
- **Avoid**: one or more high-severity findings

## Suppressions

Create `.clawshield-suppressions.json` in the target skill directory:

```json
[
  {
    "ruleId": "CS001_CURL_PIPE_SH",
    "file": "install.sh",
    "line": 15,
    "justification": "Reviewed manually; uses a pinned artifact with signature verification."
  }
]
```

Suppressions without justification are ignored.

## CI example

```yaml
- run: node {baseDir}/bin/clawshield.js scan . --format sarif --fail-on caution
```

## Boundaries

- ClawShield is a static scanner. It does not sandbox or execute the target skill.
- The rule set is intentionally narrow and should be treated as a high-signal first pass, not a full security audit.
