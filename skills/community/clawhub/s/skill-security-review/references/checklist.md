# Security Review Checklist

## 1. Artifact identity
- Name/source:
- Claimed purpose:
- Real files present:
- Any mismatch between claim and contents?

## 2. Sensitive behavior
Mark each as None / Declared / Hidden / Excessive.
- Local file read
- Local file write
- Shell execution
- Download remote content
- Upload data outward
- Persistence change
- Privilege escalation request
- Security-control modification
- Credential access
- Background/daemon behavior

## 3. High-risk indicators
- Obfuscation
- Encoded payloads
- Runtime code fetch
- Unknown binary
- Hidden telemetry
- Broad path access
- Destructive commands
- Policy evasion language

## 4. Transparency
- Does SKILL.md disclose the sensitive actions?
- Are side effects obvious before execution?
- Would a normal user be surprised by any behavior?

## 5. Risk scoring
- Low: narrow scope, transparent, no exfiltration/persistence, no hidden execution
- Medium: justified sensitive access with clear disclosure and manageable controls
- High: unjustified sensitive access, remote execution, weak transparency, or broad system impact
- Critical: stealth, exfiltration, persistence, credential theft, or bypass behavior

## 6. Default verdict rules
- Any stealth, secret upload, credential theft, or persistence without clear need -> REJECT
- Any remote code download + execute without pinning/verification -> usually REJECT
- Any broad but legitimate admin function -> ALLOW WITH GUARDRAILS
- Narrow, transparent, least-privilege workflow -> ALLOW
