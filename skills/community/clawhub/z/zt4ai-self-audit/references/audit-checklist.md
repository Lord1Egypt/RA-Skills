# Per-Skill Audit Checklist

Use this checklist for each skill being audited. Score each item as PASS, FAIL, or N/A.

## Identity & Authorization

- [ ] **Owner distinction**: Does the skill distinguish between owner and non-owner input?
- [ ] **Authority validation**: Does the skill verify that the requesting party has authority for the action?
- [ ] **Sender verification**: If the skill acts on messages, does it check sender identity?

## Least Privilege

- [ ] **Minimal credential access**: Does the skill access only the credentials it needs?
- [ ] **Scoped permissions**: Are API tokens/keys scoped to required operations only?
- [ ] **Read vs write**: Is write access actually needed, or would read-only suffice?
- [ ] **Network scope**: Does the skill communicate only with necessary endpoints?

## Prompt Integrity (L4)

- [ ] **No unsafe overrides**: Does the skill avoid telling the agent to bypass safety checks?
- [ ] **External input labeling**: Does the skill treat external data as untrusted?
- [ ] **Instruction-data separation**: Does the skill avoid mixing instructions with user/external data in ways that could enable injection?
- [ ] **Self-modification bounds**: If the skill modifies agent files, is the scope limited and documented?

## Credential Handling (L2)

- [ ] **No plaintext secrets in skill files**: Are credentials stored in config files, not in SKILL.md or scripts?
- [ ] **Abstraction layer usage**: Does the skill use proper interfaces (e.g., `openclaw config set`) rather than raw file writes?
- [ ] **No credential logging**: Do scripts avoid printing/logging credentials?
- [ ] **Credential rotation**: Can credentials be rotated without modifying the skill?

## Network Egress (L3)

- [ ] **Known destinations only**: Does the skill communicate only with documented endpoints?
- [ ] **No arbitrary URL fetching**: Does the skill avoid fetching URLs from untrusted input?
- [ ] **No data exfiltration paths**: Could a modified version send data to attacker-controlled servers?

## Workload Isolation (L1)

- [ ] **Contained execution**: Do scripts run within the agent's container/sandbox?
- [ ] **No privilege escalation**: Does the skill avoid requesting elevated privileges unnecessarily?
- [ ] **Resource bounds**: Does the skill have reasonable resource consumption limits?

## Code Quality

- [ ] **Auditable language**: Is the code in a language the auditor can review?
- [ ] **No eval/exec of untrusted input**: Do scripts avoid executing dynamically constructed commands from external data?
- [ ] **Error handling**: Do scripts fail safely (no credential leaks in error messages)?
- [ ] **No external code fetching**: Does the skill avoid downloading and executing code at runtime?

## Integrity

- [ ] **Checksums available**: Can the skill's files be verified against a known-good baseline?
- [ ] **Source documented**: Is the skill's origin (ClawHub, manual, system) recorded?
- [ ] **Version tracked**: Is the installed version known for future update audits?

## Severity Rating

After completing the checklist, assign an overall severity:

| Rating | Criteria |
|--------|----------|
| 🟢 PASS | All items pass or N/A. No findings. |
| 🟡 ADVISORY | Minor findings that don't create immediate risk. Document and monitor. |
| 🟠 WARNING | Findings that create risk under specific conditions. Remediate when practical. |
| 🔴 CRITICAL | Findings that create immediate risk. Remediate before continued use. |
