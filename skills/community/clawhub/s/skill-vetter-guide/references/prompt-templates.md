# Prompt Templates

Copy-paste these into any OpenClaw session to use Skill Vetter.

## Install Skill Vetter

```text
Please install Skill Vetter with a security-first approach.

Source: useai-pro/openclaw-skills-security@skill-vetter (ClawHub)

Requirements:
1. Fetch and review ALL files in the skill first
2. Output a vetting report: source, author, last updated, file count, red flags, permissions scope, risk level, verdict
3. If it passes review, install to ~/.agents/skills/skill-vetter/
4. Verify the skill is recognized by the current OpenClaw agent
5. Tell me the install path, source, version, and how to invoke it

Rules:
- If you find outbound network calls, sensitive file reads, obfuscated code, or sudo/elevated permission requests, flag them clearly
- Do NOT install if risk is HIGH or EXTREME — wait for my confirmation
```

## Vet a Skill (No Install)

```text
Please vet this skill using the Skill Vetter protocol. Do NOT install it yet:
[paste skill link here]

Requirements:
1. Read and review ALL files
2. Check for risks: outbound network requests, sensitive file access, base64/obfuscation, eval/exec, browser cookie/session access, modifications outside workspace, credential requests
3. Output a standardized report (name, source, author, last updated, file count, red flags, permissions, risk level, verdict)
4. Conclusion: SAFE / CAUTION / DO NOT INSTALL
```

## Vet and Install a Skill

```text
I want to install this third-party skill:
[paste skill link here]

Please follow the SOP:
1. Full skill vetting
2. Review all files, list red flags and permissions scope
3. Output a standardized vetting report
4. Only install if risk is LOW or clearly safe
5. Default install path: ~/.agents/skills/
6. After install, tell me: actual path, installed files, how to invoke, whether to add to AGENTS.md

Rule: Stop and wait for confirmation if risk is HIGH or EXTREME
```

## Enforce "Vet Before Install" Rule

```text
Please add the following rule to the current agent's AGENTS.md:

All third-party skills must be vetted with Skill Vetter before installation. No exceptions.

Requirements:
1. Tell me which file it should go in
2. Write it directly
3. Explain how this rule affects future skill installation tasks
4. Give me an example of what to say so the agent automatically vets before installing
```

## Audit Installed Skills

```text
Please run a security audit on all third-party skills installed on this machine.

Scope: ~/.agents/skills/

Requirements:
1. List all third-party skills
2. Scan for risks: suspicious outbound calls, sensitive file reads, eval/exec, base64/obfuscation, newly added suspicious files, modifications outside workspace
3. Status per skill: ✅ Normal / ⚠️ Needs attention / ❌ Problematic
4. Write results to a timestamped markdown file
5. Overall recommendation: whether any skills should be removed, isolated, or re-reviewed
```

## Set Up Automated Audit Cron

```text
Please create a cron job that runs a skills security audit every 4 hours.

Requirements:
1. Run in an isolated session
2. Audit all third-party skills under ~/.agents/skills/
3. Check against the Skill Vetter red flag checklist
4. Write results to security-audits/skills-audit-YYYY-MM-DD_HHMM.md
5. Keep historical files (don't overwrite)
6. Send a brief summary back to the current chat
```
