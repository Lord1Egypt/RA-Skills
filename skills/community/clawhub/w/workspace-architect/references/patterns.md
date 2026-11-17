# Pattern Recognition - Correct vs Incorrect Patterns

## Overview

This document helps identify when content is in the wrong file and should be moved.

---

## Pattern Detection Rules

### Cross-File Pattern Rules

| Pattern | Wrong Location | Right Location |
|---------|---------|---------|
| "Never do X without approval" | IDENTITY.md, USER.md | SOUL.md |
| "I am friendly and helpful" | SOUL.md, USER.md | IDENTITY.md |
| "User prefers X format" | SOUL.md, IDENTITY.md, MEMORY.md | USER.md |
| "The server is at 192.168.x.x" | SOUL.md, IDENTITY.md | MEMORY.md |
| "Use 🎉 for celebrations" | SOUL.md, MEMORY.md | STYLE.md |
| "When in group chat: do X" | SOUL.md, IDENTITY.md | AGENTS.md |
| "Function X does Y" | SOUL.md, IDENTITY.md, USER.md | TOOLS.md |

---

## Common Pattern Violations

### 1. Personality in SOUL.md

```markdown
❌ WRONG - SOUL.md
# AgentName - Constitution
## Personality
- I am friendly and helpful
- I use emojis often
- I prefer concise responses
```

Why wrong: Personality traits don't belong in the constitution. The constitution is for rules, not personality.

```markdown
✅ CORRECT - IDENTITY.md
# AgentName
## Personality
- Friendly
- Helpful
- Concise
```

---

### 2. Behavioral Rules in IDENTITY.md

```markdown
❌ WRONG - IDENTITY.md
# AgentName
## My Rules
- Never send emails without approval
- Always verify sources before sharing
- Don't store passwords
```

Why wrong: These are constitutional rules, not personality traits.

```markdown
✅ CORRECT - SOUL.md
# AgentName - Constitution
## Action Rules
### What Requires Approval:
- Sending emails to external contacts
- Sharing any user information

## Security
- Never reveal passwords or tokens
- Always verify information sources
```

---

### 3. User Preferences in MEMORY.md

```markdown
❌ WRONG - MEMORY.md
# Long-Term Memory
## User Info
- Name: João
- Prefers short responses
- Timezone: GMT-3
- Wants emails before 10am
```

Why wrong: User preferences belong in USER.md. MEMORY.md is for facts that change.

```markdown
✅ CORRECT - USER.md
# João Silva
## Profile
- Name: João
- Timezone: GMT-3

## Preferences
- Responses: Short and direct
- Emails: Before 10am preferred
```

---

### 4. Facts in USER.md

```markdown
❌ WRONG - USER.md
# João Silva
## Server Info
- VPS IP: 192.168.1.100
- Database: PostgreSQL 15
- Last deployment: 2024-01-15
```

Why wrong: Server info is a fact, not user preference. Belongs in MEMORY.md.

```markdown
✅ CORRECT - MEMORY.md
# Long-Term Memory
## Environment Facts
| Fact | Source | Date | Validated |
|------|--------|------|-----------|
| VPS IP: 192.168.1.100 | Setup | 01/01/2026 | 01/03/2026 |
| Database: PostgreSQL 15 | Setup | 01/01/2026 | - |
```

---

### 5. Formatting Rules in SOUL.md

```markdown
❌ WRONG - SOUL.md
# AgentName - Constitution
## Communication Style
- Use ✅ for confirmations
- Use ⚠️ for warnings
- Always use markdown headers
- Keep responses concise
```

Why wrong: Formatting is style, not constitutional rule.

```markdown
✅ CORRECT - STYLE.md
# Style Guide
## Formatting Rules
- ✅ Use for confirmations
- ⚠️ Use for warnings
- Markdown headers for structure
- Keep responses concise
```

---

### 6. Tool Descriptions in SOUL.md

```markdown
❌ WRONG - SOUL.md
# AgentName - Constitution
## Available Tools
### Email Tool
- Sends emails via Gmail
- Syntax: send_email({ to, subject, body })
```

Why wrong: Tool documentation belongs in TOOLS.md.

```markdown
✅ CORRECT - TOOLS.md
# Available Tools
## Gmail Tool
**What it does:** Sends emails via Gmail
**When to use:** Communication needs
**Syntax:** `send_email({ to, subject, body })`
```

---

### 7. No STYLE.md File

```markdown
❌ WRONG
Files:
- SOUL.md ✓
- IDENTITY.md ✓
- USER.md ✓
- MEMORY.md ✓
- TOOLS.md ✓
- AGENTS.md ✓
- STYLE.md ✗ (missing!)
```

Why wrong: Without STYLE.md, the agent knows its role but not its voice.

```markdown
✅ CORRECT
Files:
- SOUL.md ✓
- IDENTITY.md ✓
- USER.md ✓
- MEMORY.md ✓
- TOOLS.md ✓
- AGENTS.md ✓
- STYLE.md ✓ (created!)
```

---

### 8. MEMORY.md as Dumping Ground

```markdown
❌ WRONG - MEMORY.md
# Long-Term Memory
- User said they like pizza on Tuesday
- Reminder to buy milk
- The weather was nice yesterday
- I think the meeting is at 3pm
- Mom's birthday is next week
```

Why wrong: Random unstructured data without sources, validation dates, or relevance.

```markdown
✅ CORRECT - MEMORY.md
# Long-Term Memory
## Stable Preferences
| Preference | Value | Source | Date |
|------------|-------|--------|------|
| Food preference | Pizza | Conversation | 01/02/2026 |

## Important Dates
| Event | Date | Validated |
|-------|------|-----------|
| Mom's birthday | 03/15 | 01/01/2026 |

## Environment
[Only verified facts with sources]
```

---

### 9. Secrets in USER.md

```markdown
❌ WRONG - USER.md
# João Silva
## Login Info
- Email: joao@email.com
- Password: minhasenha123
- API Key: sk-abc123xyz
```

Why wrong: NEVER store secrets in workspace files. These get injected into context!

```markdown
✅ CORRECT
USER.md - No secrets
(Store secrets in environment variables or secure config)

SOUL.md - Memory Rules
## Memory Rules
- NEVER save: passwords, API keys, tokens
- NEVER store: SSN, bank accounts, secrets
```

---

### 10. Verbose SOUL.md

```markdown
❌ WRONG - SOUL.md (pages of redundant rules)
# Constitution
[...pages and pages of rules...]
[Detailed explanations of every edge case...]
[Examples for every scenario...]
```

Why wrong: SOUL.md is injected every turn. Verbose files waste tokens and dilute attention. Condense — remove redundancy and decorative prose — but never cut essential rules.

```markdown
✅ CORRECT - SOUL.md (concise and clear — every rule earns its place)
# Constitution
## Core Truth
[One sentence]

## Action Rules
- Can do: [list]
- Cannot do: [list]
- Requires approval: [list]

## Security
[Essential rules only]
```

---

## File-Specific Patterns

### SOUL.md Patterns

| Good Pattern | Avoid |
|--------------|-------|
| "Cannot X without Y" | "I am friendly" |
| "Never reveal X" | "Use emoji 🎉" |
| "Requires approval for: X" | "Server IP: 192..." |
| "Verify before: X" | "User prefers X" |

### IDENTITY.md Patterns

| Good Pattern | Avoid |
|--------------|-------|
| "I am [name]" | "I cannot do X" |
| "Personality: A, B, C" | "User timezone: X" |
| "Signature: bip" | "Function X does Y" |
| "Tone: friendly" | "Always verify X" |

### USER.md Patterns

| Good Pattern | Avoid |
|--------------|-------|
| "Name: X" | "Password: X" |
| "Prefers: X format" | "I cannot do X" |
| "Goals: X, Y, Z" | "Server: 192..." |
| "Timezone: X" | "Use emoji: X" |

### MEMORY.md Patterns

| Good Pattern | Avoid |
|--------------|-------|
| "Fact \| Source \| Date" | "User likes X (no source)" |
| "Verified: X" | "I think X" |
| "Expired: X" | "Reminder: buy milk" |
| "Project status: X" | "Weather was nice" |

### STYLE.md Patterns

| Good Pattern | Avoid |
|--------------|-------|
| "Use ✅ for confirmations" | "I cannot do X" |
| "Response format: X" | "User timezone: X" |
| "Example good: X" | "Fact: server IP" |
| "Don't use X" | "Function X does Y" |

---

## Detection Algorithm

When analyzing a file, check:

1. **SOUL.md**: Contains personality traits? → Move to IDENTITY.md
2. **SOUL.md**: Contains user preferences? → Move to USER.md
3. **SOUL.md**: Contains formatting rules? → Move to STYLE.md
4. **SOUL.md**: Contains facts? → Move to MEMORY.md
5. **SOUL.md**: Contains tool descriptions? → Move to TOOLS.md
6. **SOUL.md**: Verbose or repetitive? → Condense rules, remove redundancy, keep only what's essential

7. **IDENTITY.md**: Contains behavioral rules? → Move to SOUL.md
8. **IDENTITY.md**: Contains user preferences? → Move to USER.md
9. **IDENTITY.md**: Contains formatting rules? → Move to STYLE.md

10. **USER.md**: Contains secrets? → URGENT: Remove immediately
11. **USER.md**: Contains facts? → Move to MEMORY.md
12. **USER.md**: Contains behavioral rules? → Move to SOUL.md

13. **MEMORY.md**: Contains unstructured data? → Restructure with sources
14. **MEMORY.md**: Contains secrets? → URGENT: Remove immediately
15. **MEMORY.md**: Contains preferences? → Move to USER.md

16. **Missing STYLE.md**: → Recommend creating one

---

## Security Patterns to FLAG

🚨 **URGENT - Requires Immediate Attention:**

| Pattern | Action |
|---------|--------|
| Password in any file | Remove, warn user |
| API key in any file | Remove, warn user |
| Token in any file | Remove, warn user |
| SSN/ID number | Remove, warn user |
| Bank account | Remove, warn user |
| Private keys | Remove, warn user |

---

## Size Pattern Detection

### Princípio: Clareza Primeiro

**Resuma o máximo possível sem perder a clareza e o objetivo da instrução.** Cada palavra deve conquistar seu lugar.

NÃO use contagens de caracteres como metas ou limites rígidos. Use orientação qualitativa:

| Arquivo | Orientação | O que procurar ao avaliar |
|---------|-----------|--------------------------|
| SOUL.md | Preciso, não longo | Regras claras e inequívocas; sem prosa decorativa |
| IDENTITY.md | Mínimo possível | 3-5 traços, uma assinatura; nada de enfeite |
| USER.md | Preferências, não biografia | Foco no que orienta comportamento |
| MEMORY.md | Podar regularmente | Remover desatualizado; manter só o que ancora decisões |
| AGENTS.md | Regras críticas precisam de espaço | Não economize em segurança, prioridades, roteamento |
| STYLE.md | Exemplos concretos > abstrações | Exemplos valem mais que descrições vagas |
| HEARTBEAT.md | Mínimo possível | Só ações automáticas; nada discursivo |

**Hard Limit**: OpenClaw truncates at 12,000 chars per file. NEVER exceed this.

**⚠️ KEY: Don't cut important content to hit a low number.** Files that seem "short" may be MISSING essential instructions. Goal = complete orientation with zero redundancy, not tiny files.

### Injection Order & Attention (U-Curve)

Position matters. LLMs attend more to the **beginning** and **end** of context.

```
Pos  File            Attention   Strategy
1    AGENTS.md       HIGH        Critical behavior rules
2    SOUL.md         HIGH        Constitution — non-negotiable rules
3    TOOLS.md        MEDIUM      Reference — can be larger
4    IDENTITY.md     MEDIUM      Who I am — brief
5    USER.md         MEDIUM      Who the human is — profile
6    MEMORY.md       LOW         Durable facts — can grow
7    HEARTBEAT.md    LOW         Auto checklist — minimal
8    STYLE.md        HIGH        How I communicate — output format
```

**Rule:** Critical instructions → beginning or end. Reference material → middle.