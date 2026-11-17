---
name: workspace-architect
description: Create, analyze, and optimize OpenClaw workspace configuration files (SOUL.md, IDENTITY.md, USER.md, MEMORY.md, TOOLS.md, AGENTS.md, STYLE.md, HEARTBEAT.md) with guided workflows and best practices validation. Analyzes existing files for patterns, clarity, injection order, and content placement. All work is done in a sandbox area without modifying originals.
metadata:
  {
    "openclaw": {
      "emoji": "🏗️",
      "user-invocable": true,
      "homepage": "https://docs.openclaw.ai/tools/skills"
    }
  }
---

# Workspace Architect

## O que faz

Cria, analisa e otimiza arquivos de configuração do workspace OpenClaw com validação de melhores práticas baseadas em pesquisa (Anthropic Context Engineering 2026, JetBrains NeurIPS 2025, OpenClaw docs).

## Uso

### Criar novo agente:
```
Usuário: "Criar novo agente assistente de vendas"
→ Skill faz perguntas estruturadas, cria arquivos em sandbox/
→ Usuário confirma com "apply"
```

### Analisar workspace existente:
```
Usuário: "Analisa se minha workspace está bem configurada"
→ Skill lê arquivos, analisa padrões, clareza, ordem de injeção
→ Apresenta relatório com problemas e recomendações
```

### Otimizar arquivos:
```
Usuário: "Meus arquivos estão muito grandes"
→ Skill analisa clareza, ruído, duplicação, ordem de atenção
→ Sugere redistribuição de conteúdo com justificativa
```

### Quando usar:
- Criar novo agente/workspace do zero
- Estruturar configuração de workspace existente
- Otimizar clareza e redução de ruído
- Corrigir violações de padrões (conteúdo no arquivo errado)
- Verificar se a ordem de injeção está otimizada

### Gatilhos:
- "criar novo agente", "analisar workspace", "otimizar arquivos"
- "verificar se arquivos estão corretos", "workspace configurar"

## Conceitos Chave

### 1. Curva U de Atenção (Pesquisa: Chroma RULER)

LLMs têm uma **curva U de atenção**: prestam mais atenção no **início** e no **fim** do contexto. O meio recebe menos atenção. Isso significa:

- **Início (posições 1-2):** Regras que NUNCA podem ser ignoradas → AGENTS.md, SOUL.md
- **Meio (posições 3-6):** Referências consultivas → TOOLS.md, IDENTITY.md, USER.md, MEMORY.md
- **Fim (posições 7-8):** Formato de saída → HEARTBEAT.md, STYLE.md

**Ao analisar:** Se uma instrução crítica está no meio, sugerir mover para início ou fim. Se uma referência está no início, considerar mover para o meio.

### 2. Dono Único (Single Source of Truth)

Cada tipo de conteúdo deve estar em **apenas um arquivo**:

| Conteúdo | Dono (arquivo) |
|----------|---------------|
| Regras constitucionais | SOUL.md |
| Personalidade/vibe | IDENTITY.md |
| Perfil humano | USER.md |
| Fatos duráveis | MEMORY.md |
| Ferramentas/referências | TOOLS.md |
| Regras operacionais | AGENTS.md |
| Estilo de comunicação | STYLE.md |
| Interaction preferences | STYLE.md |
| Checklist automático | HEARTBEAT.md |

**Ao analisar:** Se o mesmo conteúdo aparece em 2+ arquivos, marcar como duplicação e sugerir dono único.

### 3. Regra vs Referência (Just-in-Time)

- **Regra** (sempre aplica) → deve estar em core file, mantenha curto
- **Referência** (consulta quando precisa) → pode ser referência curta em core file, detalhes em arquivo externo

**Ao analisar:** Se uma seção é código bash completo, tutorial longo, ou documentação detalhada, sugerir mover para `scripts/`, `memory/`, ou `docs/` e manter apenas referência.

### 4. Limite de Truncamento do OpenClaw

- `bootstrapMaxChars`: **12,000 chars por arquivo** (padrão, configurável)
- `bootstrapTotalMaxChars`: **60,000 chars total** (padrão, configurável)
- Acima = conteúdo é **truncado** = comportamento imprevisível

⚠️ Estes são **limites de plataforma** (truncation), NÃO metas de tamanho. Não escreva para atingir um número — escreva para ser claro. Se um arquivo passa de 12.000 chars, o OpenClaw corta; se está abaixo mas é confuso, o tamanho não salva.

### 5. Princípio de Clareza Primeiro

**Princípio fundamental: Resuma o máximo possível sem perder a clareza e o objetivo da instrução.**

Cada palavra deve conquistar seu lugar. Se dá pra dizer em menos palavras sem perder significado, faça-o. Mas NUNCA sacrifique clareza ou completude para atingir um número arbitrário.

| Arquivo | Orientação Qualitativa | Observação |
|---------|----------------------|------------|
| SOUL.md | Regras constitucionais — preciso, não longo | Cada regra deve ser clara e inequívoca; nada de enfeite |
| IDENTITY.md | Nome/vibe — mínimo possível | 3-5 traços, uma assinatura; se consegue dizer em menos palavras, diga |
| USER.md | Perfil humano — ferramentas vão pra TOOLS | Foco no que orienta comportamento; preferências, não biografia |
| MEMORY.md | Decisões & fatos — podar regularmente | Remover desatualizado; manter só o que ainda orienta decisões |
| TOOLS.md | Referências — pode ser maior | Sintaxe e regras de uso; exemplos rápidos, não tutoriais |
| AGENTS.md | Regras operacionais — regras críticas precisam de espaço | Prioridades, segurança, roteamento; não economizar em regras que importam |
| STYLE.md | Estilo de comunicação — exemplos ajudam | Exemplos concretos valem mais que abstrações |
| HEARTBEAT.md | Checklist mínimo — evitar token burn | Só ações automáticas; nada discursivo |

**Sinais de que um arquivo precisa resumir (não cortar):**
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

### 6. Regra Prática de Otimização

Para cada seção de cada arquivo, pergunte:

1. **Isso é regra (sempre aplica) ou referência (consulta quando precisa)?** Regra → mantenha curto. Referência → mova para arquivo externo.
2. **Se eu tirar essa seção, o modelo vai se comportar diferente?** Se não, é ruído.
3. **Isso já está em outro arquivo?** Se sim, mantenha em apenas UM lugar (dono único).
4. **Isso precisa ser lido em TODO turno?** Se só aplica em heartbeat, heartbeat lê. Se só aplica em missões, skill de missão lê.

## Capabilities

### 1. CREATE - Criar Novos Arquivos
Criação guiada através de questionários estruturados. Segue as specs em `references/arquivo-specs.md`.

### 2. ANALYZE - Analisar Arquivos Existentes
Análise profunda identificando:
- Violações de padrão (conteúdo no arquivo errado)
- Duplicação entre arquivos (sem dono único)
- Oportunidades de clarificação e condensação
- Problemas de segurança (secrets expostos)
- **Ordem de injeção e atenção (curva U)**
- **Regra vs referência (just-in-time)**

### 3. OPTIMIZE - Sugerir Melhorias
Compara arquivos contra melhores práticas e sugere:
- Redistribuição de conteúdo (mover para arquivo correto)
- Melhorias de estrutura
- Reduções por condensação (sem perder clareza)
- Seções faltantes
- Ajustes de ordem de atenção
- **Fortalecimento de segurança**

## Workflow

1. **INTENT** - Entender o que o usuário quer (create/analyze/optimize)
2. **READ** - Ler todos os core files
3. **ANALYZE** - Comparar contra specs, patterns, e curva U
4. **DRAFT** - Criar versões otimizadas em sandbox/
5. **VALIDATE** - Verificar contra padrões e clareza
6. **PRESENT** - Mostrar diferenças com justificativa
7. **CONFIRM** - Usuário decide: apply, download, ou revise

## Sandbox

Todas as modificações acontecem em sandbox/. Arquivos originais NUNCA são modificados diretamente.

## Guardrails

- NUNCA modificar arquivos originais diretamente
- SEMPRE trabalhar em sandbox/
- SEMPRE apresentar diferenças antes de aplicar
- EXIGIR confirmação explícita do usuário
- SINALIZAR issues de segurança (secrets, dados sensíveis)
- SUGERIR melhorias, não forçar
- RESUMIR ao máximo sem perder clareza — cada palavra deve conquistar seu lugar
- **Verificar dono único para cada tipo de conteúdo**
- **Verificar se regras críticas estão no início ou fim (curva U)**

## References

See `{baseDir}/references/` for:
- `arquivo-specs.md` - Specs detalhadas de cada arquivo (incluindo ordem de injeção, curva U, e limites com hard limits)
- `patterns.md` - Padrões corretos e incorretos (incluindo orientação qualitativa)
- `questionnaire.md` - Perguntas guiadas para criação

## Output Format

### Analysis Report

```markdown
# Workspace Analysis Report

## Summary
- Files analyzed: X
- Issues found: Y (Z critical, W warning)
- Size: total chars / 60,000 hard limit (N%) — concise or needs condensing
- Injection order: optimized / needs adjustment

## Injection Order & Attention (U-Curve)
Position 1 (AGENTS.md): HIGH attention - [status]
Position 2 (SOUL.md): HIGH attention - [status]
...
Position 8 (STYLE.md): HIGH attention - [status]

## File-by-File Analysis

### SOUL.md (X chars — bem resumido / pode condensar / pode estar incompleto)
- ✅ Good: [what's good]
- ⚠️ Review: [can condense without losing meaning — identify redundancy, decorative prose, or content that belongs elsewhere]
- ❌ Issue: [what's wrong]
- 📍 Position: [injection order and attention level]

### Pattern Violations
1. [Content in wrong file] → Move from X to Y
2. [Duplicated content] → Keep in Y, remove from X
3. [Reference should be rule] → Promote to core file

### Recommendations
1. [Specific recommendation with justification]
2. [Specific recommendation with justification]
```