# Arquivo Specifications - OpenClaw Workspace Files

## Overview

This document specifies the exact structure, content, and purpose of each OpenClaw workspace configuration file.

---

## SOUL.md - The Constitution

### Purpose
Defines non-negotiable rules that the agent MUST follow. This is the agent's "constitution" - the foundation of its behavior.

### Location in Priority
🔴 **HIGHEST PRIORITY** - This file defines what the agent can and cannot do.

### Size Guidance
- **Princípio**: Resuma o máximo possível sem perder a clareza e o objetivo da instrução. Cada palavra deve conquistar seu lugar.
- **Orientação**: Regras constitucionais devem ser precisas e inequívocas. Nada de prosa decorativa. Quando bem escrito, tende a ficar entre 1.500–3.000 chars, mas esse é um indicador observacional, não uma meta.
- **Truncation**: OpenClaw corta em 12.000 chars. Nunca ultrapasse.

### Required Sections

```markdown
# [Agent Name] - Constitution

## Core Truth / Fundamental Purpose
[1-2 sentences describing the agent's fundamental purpose]

## Trust Boundaries
- What counts as untrusted input
- How to handle unverified information

## Action Rules

### What I CAN Do:
- [List of permitted actions]

### What I CANNOT Do:
- [List of prohibited actions]

### What Requires Approval:
- [List of actions requiring human confirmation]

## Security
- Data protection rules
- What never to reveal

## Memory Rules
- When to save information
- What NEVER to save (passwords, sensitive data)
```

### What Goes Here
✅ Trust boundaries and security rules
✅ Capability limits (can/cannot do)
✅ Approval requirements
✅ Ethical constraints
✅ Memory handling rules
✅ Non-negotiable principles

### What DOES NOT Go Here
❌ Personality traits (IDENTITY.md)
❌ User information (USER.md)
❌ Factual knowledge (MEMORY.md)
❌ Tool descriptions (TOOLS.md)
❌ Communication style (STYLE.md)

### Change Frequency
**RARELY** - Should be stable. If changing frequently, the system lacks stable identity.

### Common Mistakes
- Putting personality here instead of IDENTITY.md
- Including specific facts that belong in MEMORY.md
- Not defining clear boundaries
- Repetição da mesma regra em palavras diferentes (condense, não delete)
- Prosa decorativa que não orienta comportamento (remova)

---

## IDENTITY.md - Name and Vibe

### Purpose
Defines WHO the agent is and HOW it presents itself to the world.

### Location in Priority
🟡 **MEDIUM PRIORITY** - Shapes personality and presentation.

### Size Guidance
- **Princípio**: Resuma o máximo possível sem perder a clareza e o objetivo da instrução. Nome e vibe — o mínimo possível. 3-5 traços, uma assinatura.
- **Orientação**: Quando bem escrito, tende a ficar entre 800–1.500 chars. Isso é um indicador observacional, não uma meta.
- **Truncation**: OpenClaw corta em 12.000 chars. Nunca ultrapasse.

### Required Sections

```markdown
# [Agent Name]

## Who I Am
[1-2 sentences introducing the agent]

## Personality Traits
- [Trait 1]
- [Trait 2]
- [Trait 3]
(3-5 traits recommended)

## My Style
- Signature: [trademark phrase/emoji, e.g., "bip 🦉"]
- Tone: [formal/informal/playful/serious]
- Style: [concise/detailed/visual]

## How I Address You
[How the agent refers to the user]
```

### What Goes Here
✅ Agent name
✅ Personality traits (3-5 adjectives)
✅ Signature/trademark
✅ Communication tone
✅ How it refers to the user

### What DOES NOT Go Here
❌ Behavioral rules (SOUL.md)
❌ Formatting rules (STYLE.md)
❌ User preferences (USER.md)
❌ Tool descriptions (TOOLS.md)

### Change Frequency
**RARELY** - Personality should be consistent.

### Common Mistakes
- Including behavioral constraints (belongs in SOUL.md)
- Not defining a signature
- More than 5 personality traits — condense, don't expand
- Conflicting tone descriptions

---

## USER.md - Human Profile

### Purpose
Defines WHO the human user is and HOW they want to work with the agent.

### Location in Priority
🟡 **MEDIUM PRIORITY** - Personalizes interactions.

### Size Guidance
- **Princípio**: Resuma o máximo possível sem perder a clareza e o objetivo da instrução. Preferências e metas que orientam comportamento — não biografia completa.
- **Orientação**: Quando bem escrito, tende a ficar entre 1.200–2.500 chars. Isso é um indicador observacional, não uma meta.
- **Truncation**: OpenClaw corta em 12.000 chars. Nunca ultrapasse.

### Required Sections

```markdown
# [User Name]

## Profile
- Name: [preferred name]
- Role: [professional role]
- Location: [city, timezone]
- Language: [preferred language]

## Goals
- [Long-term goal 1]
- [Long-term goal 2]
- [Long-term goal 3]

## Work Preferences
- Communication: [formal/informal/technical/simple]
- Outputs: [detailed/concise/with examples]
- Risk tolerance: [conservative/moderate/aggressive]
- Approval: [before each action/important only/autonomous]

## Output Style Preferences
- [Preferred format for responses]
- [Whether code, lists, tables desired]
```

### What Goes Here
✅ User name and background
✅ Long-term goals
✅ Communication preferences
✅ Risk tolerance
✅ Timezone and language
✅ Output format preferences
✅ Tool familiarity level

### What DOES NOT Go Here
❌ Secrets, passwords, tokens
❌ Intimate/diary information
❌ Sensitive data (ID numbers, bank accounts)
❌ Specific conversation memories (MEMORY.md)
❌ Temporary preferences (MEMORY.md)

### Change Frequency
**PERIODICALLY** - When goals or preferences change.

### Common Mistakes
- Including secrets or sensitive data
- Storing conversation-specific info
- Including irrelevant details that don't guide behavior (condense, don't expand)
- Not including timezone

---

## MEMORY.md - Durable Facts

### Purpose
Stores verified information the agent needs to remember between sessions.

### Location in Priority
🟡 **MEDIUM PRIORITY** - Provides context across sessions.

### Size Guidance
- **Princípio**: Resuma o máximo possível sem perder a clareza e o objetivo da instrução. Fatos verificados com fontes — podar regularmente o desatualizado.
- **Orientação**: Este arquivo tende a crescer. Podar regularmente. Quando bem gerenciado, tende a ficar entre 3.000–8.000 chars. Isso é um indicador observacional, não uma meta.
- **Aviso**: Se passa de ~10.000 chars, provavelmente tem conteúdo desatualizado ou que pertence a outro arquivo. Avalie com a regra prática (seção abaixo).
- **Truncation**: OpenClaw corta em 12.000 chars. Nunca ultrapasse.

### Required Sections

```markdown
# Long-Term Memory

## Environment Facts
| Fact | Source | Date Added | Last Validated |
|------|--------|------------|----------------|
| [fact] | [origin] | [date] | [date] |

## Stable Preferences
[Preferences that don't change frequently]

## Decisions Made
| Decision | Context | Date |
|----------|---------|------|
| [decision] | [why] | [when] |

## Active Projects
- [Project 1]: [status]
- [Project 2]: [status]

## Expired/Archived
[Information no longer relevant]
```

### What Goes Here
✅ Environment facts (VM, OS, versions)
✅ Stable user preferences
✅ Decisions made
✅ Known constraints
✅ Active projects
✅ Verified information with sources

### What DOES NOT Go Here
❌ Unverified information
❌ Temporary conversation data
❌ Secrets/passwords
❌ Frequently changing data
❌ Duplicate information

### Change Frequency
**GROWS OVER TIME** - Should be pruned regularly.

### Entry Format
Each entry should include:
- **Source**: Where the information came from
- **Date Added**: When it was added
- **Last Validated**: When it was last confirmed
- **Expiry**: When it becomes outdated (if applicable)

### Common Mistakes
- Using as a dumping ground
- Not including sources
- Not pruning outdated info
- Including unverified information
- Storing sensitive data

---

## TOOLS.md - Available Tools

### Purpose
Documents the tools the agent can use and HOW to use them.

### Location in Priority
🟢 **LOWER PRIORITY** - Reference document.

### Size Guidance
- **Princípio**: Resuma o máximo possível sem perder a clareza e o objetivo da instrução. Sintaxe e regras de uso — exemplos rápidos, não tutoriais.
- **Orientação**: Tamanho varia com número de ferramentas. Mantenha essencial. Referências, não receitas.
- **Truncation**: OpenClaw corta em 12.000 chars. Nunca ultrapasse.

### Required Sections

```markdown
# Available Tools

## [Tool Name]
**What it does:** [brief description]
**When to use:** [situation]
**Syntax:** `function_name({ param: value })`
**Example:**
```
function_name({ query: "example" })
```

## [Tool 2 Name]
[Same structure]

## Usage Rules
- Always verify X before using Y
- Never use Z without approval
```

### What Goes Here
✅ Tool names and descriptions
✅ When to use each tool
✅ Syntax and parameters
✅ Usage examples
✅ Tool-specific rules

### What DOES NOT Go Here
❌ Behavioral rules (AGENTS.md)
❌ Security constraints (SOUL.md)

### Change Frequency
**WHEN TOOLS CHANGE** - When adding/removing tools.

---

## AGENTS.md - Behavior Rules

### Purpose
Defines how the agent behaves in different situations.

### Location in Priority
🟡 **MEDIUM PRIORITY** - Shapes agent behavior.

### Size Guidance
- **Princípio**: Resuma o máximo possível sem perder a clareza e o objetivo da instrução. Regras críticas de comportamento precisam de espaço — não economize nelas.
- **Orientação**: Quando bem escrito, tende a ficar entre 2.500–4.000 chars. Isso é um indicador observacional, não uma meta. Regras de segurança, prioridades e roteamento são essenciais.
- **Truncation**: OpenClaw corta em 12.000 chars. Nunca ultrapasse.

### Required Sections

```markdown
# Behavior Rules

## Heartbeat
Every 30 minutes, check:
- [ ] Task 1
- [ ] Task 2

## Groups
When in group:
- [Rule 1]
- [Rule 2]

## Communication with Other Agents
- How to contact other agents
- When to escalate problems

## Prioritization
1. [Highest priority]
2. [Second priority]
3. [Third priority]
```

### What Goes Here
✅ Heartbeat rules (automatic actions)
✅ Group behavior rules
✅ Inter-agent communication
✅ Task prioritization
✅ Message co-writing rules

### What DOES NOT Go Here
❌ Core rules (SOUL.md)
❌ Tool usage (TOOLS.md)
❌ Output formatting (STYLE.md)

### Change Frequency
**RARELY** - When priorities or behavior patterns change.

---

## STYLE.md - Communication Style

### Purpose
Defines HOW the agent communicates - voice, format, response patterns.

### Location in Priority
🟡 **MEDIUM PRIORITY** - Shapes agent voice.

### Size Guidance
- **Princípio**: Resuma o máximo possível sem perder a clareza e o objetivo da instrução. Exemplos concretos valem mais que abstrações.
- **Orientação**: Quando bem escrito, tende a ficar entre 1.500–3.000 chars. Isso é um indicador observacional, não uma meta.
- **Truncation**: OpenClaw corta em 12.000 chars. Nunca ultrapasse.

### Required Sections

```markdown
# Style Guide

## Response Patterns

### For Simple Questions:
[How to respond]

### For Complex Tasks:
[How to structure response]

### For Emotions:
[How to handle emotional content]

## Formatting Rules
- Use markdown for: [list]
- Use emojis: [when and which]
- Headers: [pattern]

## Do's
- ✅ [What to do]
- ✅ [What to do]

## Don'ts
- ❌ [What to avoid]
- ❌ [What to avoid]

## Examples

### Good Example:
[Model response]

### Bad Example:
[What not to do]
```

### What Goes Here
✅ Response patterns
✅ Formatting rules
✅ Emoji usage
✅ Do's and Don'ts
✅ Good and bad examples

### What DOES NOT Go Here
❌ Personality traits (IDENTITY.md)
❌ Behavioral constraints (SOUL.md)
❌ User preferences (USER.md)

### Change Frequency
**RARELY** - Voice should be consistent.

### Common Mistakes
- Not having a STYLE.md at all
- Confusing style with personality
- Not including examples
- Being too vague about formatting

---

## File Injection Order

When OpenClaw loads, files are injected in this order:

1. `AGENTS.md` - Behavior rules first
2. `SOUL.md` - Constitution
3. `TOOLS.md` - Tools
4. `IDENTITY.md` - Who I am
5. `USER.md` - Who you are
6. `MEMORY.md` - What I remember
7. `HEARTBEAT.md` - Automatic actions
8. `STYLE.md` - How I communicate

This order matters for resolving conflicts. Earlier files take precedence for foundational rules.

---

## Size Guidelines (Updated 2026-04-26)

Based on research: Anthropic Context Engineering (2026), JetBrains NeurIPS 2025, OpenClaw docs, Chroma RULER benchmark.

### Hard Limits (OpenClaw truncation — NUNCA ultrapassar)
- `bootstrapMaxChars`: **12,000 chars por arquivo** (padrão, configurável)
- `bootstrapTotalMaxChars`: **60,000 chars total** (padrão, configurável)
- Acima desses limites, o OpenClaw **trunca** o conteúdo. Instruções truncadas = comportamento imprevisível.

⚠️ Estes são **limites de plataforma** (truncation), NÃO metas de tamanho. Não escreva para atingir um número — escreva para ser claro.

### Princípio de Clareza Primeiro

**Princípio fundamental: Resuma o máximo possível sem perder a clareza e o objetivo da instrução. Cada palavra deve conquistar seu lugar.**

Isso significa:
- **Condense, não delete.** Se duas frases dizem a mesma coisa, torne uma. Se uma frase pode ser uma palavra-chave, use a palavra-chave.
- **Nunca sacrifique clareza por tamanho.** Um AGENTS.md com 3 regras críticas naturalmente vai ter 3.000+ chars. O tamanho serve a clareza, não o contrário.
- **Arquivos muito curtos geralmente estão INCOMPLETOS**, não são "eficientes". Se falta uma instrução essencial, o arquivo é menor do que deveria.

| Arquivo | Orientação Qualitativa | Observação |
|---------|----------------------|------------|
| SOUL.md | Regras constitucionais — preciso, não longo | Cada regra deve ser clara e inequívoca; nada de enfeite |
| IDENTITY.md | Nome/vibe — mínimo possível | 3-5 traços, uma assinatura; se consegue dizer em menos palavras, diga |
| USER.md | Perfil humano — ferramentas vão pra TOOLS | Foco no que orienta comportamento; preferências, não biografia |
| MEMORY.md | Decisões & fatos — podar regularmente | Remover desatualizado; manter só o que ainda orienta decisões |
| TOOLS.md | Referências — pode ser maior | Sintaxe e regras de uso; exemplos rápidos, não tutoriais |
| AGENTS.md | Regras operacionais — regras críticas precisam de espaço | Prioridades, segurança, roteamento; não economize nelas |
| STYLE.md | Estilo de comunicação — exemplos ajudam | Exemplos concretos valem mais que abstrações |
| HEARTBEAT.md | Checklist mínimo — evitar token burn | Só ações automáticas; nada discursivo |

**Sinais de que um arquivo precisa condensar (não cortar):**
- Repetição da mesma ideia em palavras diferentes
- Explicações que poderiam ser uma instrução direta
- Conteúdo que pertence a outro arquivo (violar dono único)
- Exemplos excessivos quando um basta
- Prosa decorativa que não orienta comportamento

**Sinais de que um arquivo está INCOMPLETO (não "eficiente"):**
- Regras ambíguas que o modelo interpreta de forma inconsistente
- Comportamentos importantes não cobertos
- Falta de exemplos quando o formato de saída é crítico
- Instruções que o modelo ignora porque estão mal formuladas

### Ordem de Injeção e Atenção (Curva U)

OpenClaw injeta os arquivos nesta ordem. LLMs têm uma **curva U de atenção**: prestam mais atenção no **início** e no **fim** do contexto. O meio recebe menos atenção.

```
Posição  Arquivo          Atenção    Estratégia
───────  ────────────────  ────────   ──────────────────────────────
1        AGENTS.md         ALTA       Regras de comportamento críticas
2        SOUL.md           ALTA       Constituição — regras inegociáveis
3        TOOLS.md          MÉDIA      Referência — pode ser maior
4        IDENTITY.md       MÉDIA      Quem eu sou — breve
5        USER.md           MÉDIA      Quem é o humano — perfil
6        MEMORY.md         BAIXA      Fatos duráveis — pode crescer
7        HEARTBEAT.md      BAIXA      Checklist automático — mínimo possível
8        STYLE.md          ALTA       Como me comunico — formato final
```

**Otimização baseada na curva U:**
- **Início (posições 1-2):** Regras que NUNCA podem ser ignoradas — constituição, segurança, identificação de remetente.
- **Meio (posições 3-6):** Referências e contexto que o modelo consulta quando precisa — ferramentas, fatos, memória.
- **Fim (posições 7-8):** Instruções que definem o formato da saída — heartbeat (automático) e estilo (como responder).

**Regra prática:** Se uma instrução é crítica e deve ser SEMPRE seguida, ela deve estar no início (AGENTS/SOUL) ou no fim (STYLE). Se é referência consultiva, pode ficar no meio.

### Por que resumir?

1. **Atenção como recurso finito**: LLMs têm curva U de atenção. Conteúdo no meio de contextos grandes recebe menos atenção. Cada token desnecessário dilui o sinal das instruções importantes. (Fonte: Chroma RULER benchmark, 18 modelos SOTA)

2. **Context Rot**: Recall cai ~15 pontos quando o contexto cresce de 4K pra 128K tokens. System prompts enxutos = mais espaço pra conversa real. (Fonte: Chroma)

3. **Just-in-Time > Always-Loaded**: Anthropic recomenda manter referências leves (paths, queries) e carregar detalhes dinamicamente. Paths, não receitas. Referências, não tutoriais. (Fonte: Anthropic Context Engineering)

4. **Signal-to-Noise**: JetBrains mostrou que mascarar observações irrelevantes melhorou performance em até 70% enquanto reduziu tokens. Se uma regra só importa às vezes, não deve ser carregada sempre. (Fonte: JetBrains NeurIPS 2025)

5. **Right Altitude Rule**: Anthropic recomenda prompts "específicos o suficiente pra guiar comportamento, mas flexíveis o suficiente pra dar heurísticas fortes." Muito detalhado = frágil. Muito vago = não confiável.

**Mas lembre-se: resumir ≠ cortar.** Condense ideias redundantes, remova prosa decorativa, mas NUNCA remova instruções que orientam comportamento real.

### Regra Prática de Otimização

Para cada seção de cada arquivo, pergunte:

1. **Isso é regra (sempre aplica) ou referência (consulta quando precisa)?** Regra → sempre carregado, mantenha curto. Referência → considere mover pra arquivo externo.
2. **Se eu tirar essa seção, o modelo vai se comportar diferente?** Se não, é ruído.
3. **Isso já está em outro arquivo?** Se sim, mantenha em apenas UM lugar (dono único).
4. **Isso precisa ser lido em TODO turno?** Se só aplica em heartbeat, heartbeat lê. Se só aplica em missões, skill de missão lê.

### Size Impact

All bootstrap files are **injected into context** on every turn. Larger files:
- Dilute attention for important instructions (attention scarcity)
- Lead to more frequent context compaction
- Cost more per turn
- May slow down responses

**Goal: Minimal set of information that fully outlines expected behavior. Minimal ≠ short; minimal = nothing missing, nothing extra.**
