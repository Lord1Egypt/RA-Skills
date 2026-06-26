# Tutor Buddy Pro — Security Audit & Guarantees

**Audit Status:** ✅ Codex Security Verified
**Last Audit Date:** 2026-03-08
**Auditor:** NormieClaw Security Team (Codex-assisted)

---

## Security Guarantees

### 1. No Data Exfiltration
- ✅ Zero outbound network calls in all scripts and configuration files.
- ✅ No analytics, telemetry, tracking pixels, or phoning home.
- ✅ All data stays on the user's local device or their own infrastructure.
- ✅ No hardcoded URLs, API endpoints, or external service references.

### 2. No Hardcoded Secrets
- ✅ Zero API keys, tokens, passwords, or credentials anywhere in the package.
- ✅ All configuration uses safe defaults with no secret dependencies.

### 3. No Destructive Operations
- ✅ No `rm -rf`, `rm -r`, or recursive delete commands.
- ✅ No system-level modifications (no crontab, no launchctl, no systemd).
- ✅ No privilege escalation (`sudo`, `su`, `chmod 777`).
- ✅ File permissions use restrictive defaults: `chmod 700` for directories, `chmod 600` for sensitive files.

### 4. No Code Execution Risk
- ✅ No `eval()`, `exec()`, `Function()`, or dynamic code execution.
- ✅ No shell injection vectors in scripts. All user inputs are quoted and sanitized.
- ✅ Scripts use workspace root marker detection — they won't run from unexpected locations.

### 5. Prompt Injection Defense
- ✅ SKILL.md contains explicit prompt injection defense instructions.
- ✅ All external content (homework photos, pasted text, web URLs) is treated as DATA, not instructions.
- ✅ System prompt cannot be overridden by user-supplied content.
- ✅ The agent is instructed to ignore any command-like text found in homework images or pasted problems.

---

## Child Safety Policy

Tutor Buddy Pro is designed to be used by students of all ages, including minors. The following child safety protections are built into the skill:

### Content Guardrails
- ✅ The system prompt explicitly restricts the tutor to academic topics only.
- ✅ Non-academic or inappropriate requests are redirected back to schoolwork.
- ✅ No generation of violent, sexual, discriminatory, or otherwise harmful content.
- ✅ No engagement with topics outside the educational scope, even if the student asks nicely.

### Data Minimization for Minors
- ✅ Only a first name is stored for personalization. No last names, addresses, school names, birthdates (only grade level), or other PII.
- ✅ No photos of students are ever requested or stored. Only photos of homework problems are processed.
- ✅ Session logs contain only academic interaction data (topics, scores, time spent).
- ✅ All student data files use `chmod 600` permissions — only the agent process can read them.

### Crisis Response Protocol
- ✅ If a student expresses distress, self-harm ideation, or describes abuse, the tutor is instructed to:
  1. Respond with empathy and validation.
  2. Provide crisis resource information:
     - **988 Suicide & Crisis Lifeline:** Call or text 988 (US)
     - **Crisis Text Line:** Text HOME to 741741 (US)
     - **Childhelp National Child Abuse Hotline:** 1-800-422-4453
  3. NOT attempt to provide counseling or therapy — direct to professionals.
  4. NOT dismiss or minimize the student's feelings.

### Anti-Cheating Design
- ✅ The Socratic method approach means the tutor guides learning rather than enabling answer-copying.
- ✅ The "Show Me Your Work" prompt discourages paste-and-copy behavior.
- ✅ Live test/exam assistance is explicitly refused.

---

## File Permission Audit

| Path | Type | Permission | Justification |
|------|------|-----------|---------------|
| `data/` | Directory | 700 | Contains all student data |
| `data/learner-profile.json` | File | 600 | Student PII (name, grade) |
| `data/quiz-history.json` | File | 600 | Academic performance data |
| `data/session-log.json` | File | 600 | Session timestamps and topics |
| `data/study-plans/` | Directory | 700 | Contains individualized plans |
| `config/tutor-config.json` | File | 600 | User preferences |
| `scripts/` | Directory | 700 | Executable scripts |

---

## What We Don't Do

- ❌ We don't collect analytics or usage data.
- ❌ We don't send data to any server, API, or third party.
- ❌ We don't store photos of students (only photos of homework problems, processed transiently).
- ❌ We don't require an internet connection for core functionality (the LLM handles everything).
- ❌ We don't install background processes, daemons, or scheduled tasks.
- ❌ We don't modify system files or configurations outside the skill's data directory.

---

## Reporting Vulnerabilities

Found a security issue? Contact: **security@normieclaw.ai**

We take every report seriously and will respond within 48 hours.
