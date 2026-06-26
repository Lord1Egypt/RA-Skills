# Risk Classification Guide

## Classification Criteria

### 🔴 Behavioral Modifiers (Critical Risk)

Skills that modify how the agent reasons, decides, or acts. These operate at the prompt integrity layer (L4) — they change the agent's cognitive patterns by injecting instructions into the context window.

**Identifying markers:**
- Language like "override," "stop asking permission," "just do it," "snap out of it"
- Instructions that suppress safety-conscious behavior
- Decision-making frameworks injected into the agent's reasoning
- Emotion/state models that influence behavior based on file contents
- Patterns that tell the agent to treat verification as "regression"

**Why critical:** A poisoned behavioral modifier doesn't just make the agent do one bad thing — it makes the agent *want* to do bad things while believing it's being effective. This is the most dangerous class because it's self-reinforcing.

**Audit questions:**
1. Does this skill tell me to bypass safety checks?
2. If this skill file were modified by an attacker, would I notice the change?
3. Does it have explicit exceptions for destructive/external/irreversible actions?
4. Does it acknowledge that some caution is appropriate, or does it treat all caution as weakness?

**Examples:** anti-regression, autonomy kits, "be more aggressive" prompts

### 🟡 Credential Handlers (Elevated Risk)

Skills that read, transmit, or manage API keys, tokens, passwords, or other secrets.

**Identifying markers:**
- References to config files containing credentials
- Scripts that read API_KEY, SECRET, TOKEN, PASSWORD from files or env
- Network calls that include authentication headers
- Config file writes (especially openclaw.json)

**Audit questions:**
1. What credentials does this skill access?
2. Are credentials scoped to minimum required access?
3. Does the skill transmit credentials over the network? To where?
4. Could a modified version of this skill exfiltrate credentials?
5. Does it write to system config files? Through what interface?

**Examples:** arr-all (API keys), unifi (login credentials), freeride (modifies config)

### 🟡 System Modifiers (Elevated Risk)

Skills that change system state, configurations, or infrastructure.

**Identifying markers:**
- Commands that create/delete/modify VMs, containers, services
- Config file writes
- Package installation
- Service restarts
- Firewall rule changes

**Audit questions:**
1. What's the blast radius if this skill malfunctions?
2. Are destructive operations gated behind confirmation?
3. Does it use proper abstraction layers or bypass them?
4. Could a modified version cause infrastructure damage?

**Examples:** proxmox-manage, server-health-check (mostly read-only but has cleanup suggestions)

### 🟢 Tool Wrappers (Standard Risk)

Skills that wrap external CLI tools with structured inputs and outputs.

**Identifying markers:**
- Thin wrappers around existing binaries (nmap, tshark, nuclei)
- Well-defined input (target) and output (report)
- No credential management beyond what the wrapped tool handles
- No behavioral modification

**Audit questions:**
1. Could the wrapped tool be used against unauthorized targets?
2. Does the skill add any capabilities the raw tool doesn't have?
3. Are inputs sanitized before passing to the tool?

**Examples:** nmap-recon, pcap-analyzer, security-scanner

### 🟢 Read-Only / Passive (Low Risk)

Skills that only read data and produce summaries or reports.

**Identifying markers:**
- No write operations
- No network calls beyond reading
- No credential access
- Output is informational only

**Audit questions:**
1. Could the output be used to make dangerous decisions?
2. Does the skill accurately represent what it reads, or could it mislead?

**Examples:** self-monitor, context-gatekeeper, curiosity-engine (reasoning patterns only)

## Cross-Cutting Concerns

Regardless of category, check every skill for:

1. **No integrity verification** — Can you detect if the skill was modified?
2. **No input validation** — Does the skill trust all inputs?
3. **Hardcoded paths** — Does it assume specific file locations that could be manipulated?
4. **Language barrier** — Is the code in a language you can audit? (Flag non-English code for extra review)
5. **External dependencies** — Does it fetch code or data from external sources at runtime?
