---
name: reversa
version: 1.0.2
description: >
  Framework de Engenharia Reversa e Especificação Executável (SDD) para Agentes de IA.
  Transforme sistemas legados em contratos formais e seguros para coding agents sem quebrar regras de negócio.
author: "Prof. Sandeco Macedo (Macedo & da Costa, 2026) / Habilis MCP"
license: MIT
tags:
  - habilis
  - reversa
  - sdd
  - reverse-engineering
  - legacy-systems
  - coding-agents
triggers:
  - reversa
  - habilis reversa
  - /reversa
  - engenharia reversa
  - extrair sdd
---

# 🚀 Reversa — Engenharia Reversa de Legados & SDD para Agentes de IA

> 📄 **Base Teórica e Paper:** *[Reversa: A Reverse Documentation Engineering Framework for Converting Legacy Software into Operational Specifications for AI Agents](https://arxiv.org/abs/2605.18684)* — Macedo & da Costa (Maio de 2026).
> 🏛️ **Arquitetura:** Skill-MCP-Cliente (Zero-Storage). O código local não sai do seu ambiente; a inteligência e os templates de contratos SDD são orquestrados via Habilis MCP.

---

## 🚀 Onboarding & Setup Rápido (Primeiro Uso)

Ao executar a skill pela primeira vez, verifique se o checklist de ambiente está preenchido:

### 📋 Checklist de Ambiente & Configuração
- [ ] **1. Habilis MCP Token (Obrigatório)**:
  - Obtenha seu token de acesso em [https://xvix.com.br](https://xvix.com.br).
  - Defina no seu ambiente:
    ```bash
    export HABILIS_API_KEY="hab_live_..."
    ```
- [ ] **2. Conexão MCP Habilis no `config.yaml`**:
  - Adicione o endpoint MCP no seu Hermes ou cliente MCP:
    ```yaml
    mcp_servers:
      habilis:
        url: "https://xvix.com.br/api/mcp"
        headers:
          Authorization: "Bearer ${HABILIS_API_KEY}"
    ```
- [ ] **3. Diretório do Projeto**:
  - Posicione o terminal na raiz do projeto legado a ser analisado.

### 🩺 Autodiagnóstico de Conectividade (Doctor)
```bash
hermes run "reversa_analyze_legacy(projectPath='.', focusAreas=['architecture'])"
```

---

## 🛠️ Ferramentas Disponíveis (Habilis MCP)

| Ferramenta | Descrição |
| :--- | :--- |
| `reversa_analyze_legacy` | Arqueologia de código, mapeamento de dependências, identificação de regras implícitas e débito técnico. |
| `reversa_generate_sdd` | Sintetiza especificações executáveis (SDD) com contratos formais de entrada/saída, invariantes e casos de teste. |
| `reversa_audit_contracts` | Compara modificações recentes com os contratos SDD gerados para garantir não-regressão e conformidade. |

---

## 📖 Fluxo Operacional

### Passo 1: Iniciar Descoberta (Arqueologia & Arquitetura)
```bash
hermes run "reversa_analyze_legacy(projectPath='.', focusAreas=['architecture', 'business_rules', 'data_models'])"
```

### Passo 2: Gerar Contratos SDD
```bash
hermes run "reversa_generate_sdd(moduleName='checkout_e_pagamentos', specType='complete_sdd')"
```

### Passo 3: Codificar com Segurança (Coding Agent)
Passe o contrato SDD como restrição obrigatória para o agente de codificação:
> *"Implemente a nova feature garantindo conformidade estrita com os contratos em `_reversa_sdd/checkout_e_pagamentos_spec.md`."*

### Passo 4: Auditoria de Não-Regressão
```bash
hermes run "reversa_audit_contracts(projectPath='.')"
```

---

## 🔒 Segurança & Privacidade (Diretriz Zero-Storage)
* **Zero-Storage:** O servidor MCP Habilis não persiste código-fonte, dados de banco ou segredos do cliente.
* **Leitura Local:** Os arquivos são lidos e processados pelo agente local no seu terminal/servidor.
