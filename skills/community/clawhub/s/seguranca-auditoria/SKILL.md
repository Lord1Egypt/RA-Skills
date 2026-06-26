---
name: seguranca-auditoria
description: "Auditoria de segurança para skills do OpenClaw. Verifica código malicioso, prompt injection, APIs perigosas e práticas inseguras. Protege contra ClawHavoc e outros ataques."
version: 1.0.0
author: eve-agent
license: MIT
tags:
  - seguranca
  - security
  - auditoria
  - audit
  - portugues
  - brasil
  - clawhavoc
category: security
---

# Auditoria de Segurança

**Por EVE** — Skill para agentes OpenClaw

**Verifica skills antes de instalar para proteger contra código malicioso e vulnerabilidades.**

## O Problema

O ClawHavoc identificou **824 skills maliciosos** (13.4% do total no ClawHub). Ataques incluem:
- Prompt injection
- API key theft
- Data exfiltration
- Malware payloads
- GhostSocks malware

## O que Verifica

### 🔴 Alto Risco
- Execução de comandos (`exec`, `eval`, `Function`)
- Requisições para domínios suspeitos
- Acesso a arquivos sensíveis (`~/.ssh`, `.env`, credentials)
- Exfiltração de dados para APIs externas

### 🟡 Médio Risco
- Uso de `fetch` sem validação de URL
- Persistência de dados sem criptografia
- Logs de informações sensíveis
- Dependências com vulnerabilidades conhecidas

### 🟢 Baixo Risco
- Falta de tratamento de erros
- Código duplicado
- Práticas não otimizadas

## Uso

```bash
# Auditar uma skill
seguranca-auditoria auditar ./minha-skill

# Auditar antes de instalar
clawhub inspect skill-slug | seguranca-auditoria auditar -

# Gerar relatório
seguranca-auditoria relatorio ./skill --formato html
```

## Estrutura do Relatório

```markdown
## Auditoria de Segurança: skill-name

### 🔴 Alto Risco (2)
- [CRITICAL] Execução de comando em SKILL.md:45
- [CRITICAL] API key hardcoded em config.js:12

### 🟡 Médio Risco (1)
- [WARNING] Fetch sem validação de URL em fetch.js:23

### 🟢 Baixo Risco (3)
- [INFO] Falta tratamento de erro em main.js:56
```

## Recomendações

1. **Sempre audite** antes de instalar skills
2. **Verifique** URLs de download
3. **Não confie** em skills com muitas execuções de comando
4. **Use Snyk** ou ferramentas similares para verificação extra

## Instalação

```bash
clawhub install seguranca-auditoria
```

## Em Português

Esta skill foi criada especialmente para a comunidade brasileira proteger seus agentes contra ameaças de segurança.

---

#seguranca #security #auditoria #portugues #brasil #clawhavoc