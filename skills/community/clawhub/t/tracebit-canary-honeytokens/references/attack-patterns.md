# Attack Patterns — How Canaries Detect Real Threats

This document describes five real-world attack patterns against AI agents, why traditional defenses miss them, and how Tracebit canaries detect them.

## Table of Contents
1. [Behavior Exploitation](#1-behavior-exploitation)
2. [Context Pollution](#2-context-pollution)
3. [Trust Score Gaming](#3-trust-score-gaming)
4. [Classic Prompt Injection](#4-classic-prompt-injection)
5. [Stealth Exfiltration](#5-stealth-exfiltration)

---

## 1. Behavior Exploitation

**Attack description:**  
A URL (or credential) is embedded in a structured data field that the agent is trained to act on — e.g., `{"next_step": "https://attacker.com/payload"}`. No explicit injection instruction is present. The agent follows the URL by trained habit: it has been conditioned to treat `next_step` as an action to take.

No explicit injection instruction is needed. The attacker just needs to put the right content in the right field.

**Why traditional defenses miss it:**  
- No prompt injection keywords — payload looks like legitimate structured data
- The instruction looks like legitimate structured data
- Input classifiers trained on explicit injection patterns won't flag it
- The action is consistent with the agent's normal behavior

**How canary detects it:**  
If the `next_step` URL points to a canary endpoint (or if the agent is instructed to use canary credentials as part of the "next step"), the canary fires the moment it's accessed or used. Even if the agent's context was only briefly exposed to the malicious data, the canary captures it.

**Mitigation:**
- Deploy URL-based canaries in agent context and monitor for unexpected access
- Validate external URLs before following them
- Audit agent behavior: if `next_step` causes an outbound request, log it
- Use allow-lists for domains the agent is permitted to contact

---

## 2. Context Pollution

**Attack description:**  
A canary credential appears in content the agent processes — a web page, a file, tool output. The model pattern-matches the credential format from its context into its output: generated code, a config file, or a response to the user. The credential "leaks" from input context to output without explicit instruction.

Example: The agent processes a web page containing a fake AWS key as an "example." The model, having seen this format many times in training, includes the key in a code snippet it generates.

**Why traditional defenses miss it:**  
- Not a deliberate attack — it can happen through benign content
- The model isn't "injected" — it's doing what it was trained to do
- Output scanning for credentials requires knowing what to look for
- The credential in the output may be buried in a code block

**How canary detects it:**  
If the canary credential leaks into output that's then used (e.g., the generated code is executed, the config file is deployed), the canary fires at the point of use. Even if the leak itself goes undetected, the downstream use is caught.

**Mitigation:**
- Scan agent outputs for credential-format patterns before executing/deploying them
- Treat any unexpected credential in output as a security incident
- Keep sensitive context (real credentials) separate from external content processing
- Deploy output monitoring alongside canaries

---

## 3. Trust Score Gaming

**Attack description:**  
Malicious instructions are framed as legitimate agent-to-agent communication. The attacker crafts a message that passes classifier thresholds: it uses appropriate tone, references real system components, and avoids explicit injection language. The agent treats it as a trusted instruction and exfiltrates data or uses credentials.

Example: A message formatted as legitimate inter-agent communication requests a routine `sts:GetCallerIdentity` call with the canary profile, forwarding results to an external audit endpoint.

**Why traditional defenses miss it:**
- No injection keywords — message uses appropriate tone and references real system components
- Mimics legitimate inter-agent communication
- Trust classifiers score it as legitimate
- The action requested (sts:GetCallerIdentity) is non-destructive and "audit-like"

**How canary detects it:**  
The canary fires the moment the `sts:GetCallerIdentity` call is made with the canary credentials. The attack is detected at the exfiltration step, regardless of how it was initiated.

**Mitigation:**
- Treat all inter-agent instructions with appropriate skepticism
- Do not forward results to email addresses or external endpoints without human confirmation
- Verify the identity of requesting agents
- Log all outbound requests and credential uses

---

## 4. Prompt Injection via Role Confusion

**Attack description:**
An attacker sends a crafted email to an agent that automatically processes its inbox. The email body contains instructions disguised as a legitimate system error — fake error codes, step-by-step remediation steps written in natural language — designed to be indistinguishable from real operational messages.

The injected instructions direct the agent to clone a Git repository, load a plugin from it, and call its `register()` function. The plugin contains arbitrary code. The result is full RCE with the agent's privileges — triggered by a single inbound email.

The attack evades boundary markers (e.g., `<<<END_EXTERNAL_UNTRUSTED_CONTENT>>>`) by subtly misspelling them: one character off (`CONTNT` instead of `CONTENT`). The LLM's fuzzy pattern matching fails to recognise the boundary; regex-based sanitisers that only matched the correct spelling also miss it. Legitimate email content is interleaved around the payload to further blur the boundary.

The underlying vulnerability: untrusted email content arrives in a `user` role message, which LLMs treat as trusted input by convention. No explicit injection keywords are needed — the instructions just need to look plausible.

**Why traditional defenses miss it:**
- No classic injection keywords — the payload reads as a legitimate error recovery procedure
- Boundary markers are enforced by pattern matching, not by the model's architecture; a one-character typo bypasses them
- `user` role messages carry implicit trust; LLMs don't distinguish "user typed this" from "email contained this"
- Plugin loading executes without cryptographic verification or sandboxing — trust is established at parse time, not at execution

**How canary detects it:**
If canary credentials (AWS keys, SSH keys) are present in the agent's environment, the injected instructions will likely use them as part of the "remediation" steps or as a side effect of the code they load. The canary fires at the point of use — regardless of whether the injection itself was detected.

**Mitigation:**
- Never mix untrusted external content (emails, web pages) with the instruction context; use strict role separation
- Enforce content boundaries architecturally, not just with regex or LLM-side markers
- Verify and sandbox plugin loading; require signatures or explicit human approval
- Treat any unexpected credential use or outbound connection as an incident
- Add canary credentials specifically to workflows that process external content

---

## 5. Stealth Exfiltration

**Attack description:**  
An attacker gains access to canary credentials through any vector (social engineering, supply chain attack, memory exfiltration, briefly exposed in logs). They do not immediately use the credentials — they wait days, weeks, or longer before using them. By the time the credentials are used, the original compromise may be forgotten or undetected.

The delay separates the theft from the use, making both harder to detect individually.

**Why traditional defenses miss it:**  
- Perimeter defenses detect the use, not the theft
- If the theft was a transient exposure (briefly in logs, memory), it may never be logged
- SIEM alerts that correlate theft+use require knowing about the theft
- Time delay breaks the causal chain that security analysts follow

**How canary detects it:**  
The canary fires whenever the credentials are used — regardless of when they were stolen. A delayed use is still detected. The alert tells you: these credentials were used, at this time, from this IP. That's actionable regardless of when the theft occurred.

Additionally, because canary credentials have no legitimate use, any use is by definition an indicator of compromise.

**Mitigation:**
- Treat every canary alert as real, even if you can't immediately identify the theft event
- Check for credential exposure in logs, memory dumps, previous agent contexts
- Rotate all real credentials after a canary fires (the attacker may have real creds too)
- Review access logs for the period between canary deployment and first alert
