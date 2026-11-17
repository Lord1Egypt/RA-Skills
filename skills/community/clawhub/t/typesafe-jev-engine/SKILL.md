---
name: typesafe-jev-engine
display_name: TYPESAFE JEV DECISION ENGINE
description: Use when building typed AI judgments.
metadata:
  openclaw:
    emoji: "🧠"
    tags: ["typesafe", "jev", "pydantic", "ai-decision", "hermes-skill"]
---

# TypeSafe Jev Decision Engine
**Author:** Rafa Martins & Agente Mel (Mel-IA)

Esta skill empacota a arquitetura **TypeSafe AI & System One (Jev)** para transformar LLMs em primitivas de programação tipadas e determinísticas, garantindo zero alucinação em fluxos críticos de agentes.

## 🚀 O que é o Padrão TypeSafe / Jev?
Em vez de depender de prompts conversacionais abertos para tomar decisões, o modelo **System One** atua como uma função pura que recebe estado/texto e devolve um contrato **JSON / Pydantic estrito**. O código gerencia o fluxo de forma 100% determinística.

## 🛠️ Módulos Inclusos na Skill

1. **Classificação de Contexto (`typesafe_core.py`)**
   - Separa ecossistemas ou marcas (ex: <service_a>, <service_b>, <service_c> ou geral) com nível de urgência e ação recomendada.
2. **Planejador Tipado de Tarefas (`mel_typesafe_planner.py`)**
   - Converte solicitações em linguagem natural em um contrato tipado (`MelTaskPlan`) contendo categoria, ferramentas necessárias, passos atômicos e travas de segurança/confirmação.
3. **Qualificador de Leads (`ghl_typesafe_qualifier.py`)**
   - Classifica contatos/leads (`hot_lead`, `warm_lead`, `cold_lead`, `unqualified`) com estágio de pipeline sugerido e tags automáticas.
4. **Roteador de Webhooks (`papi_typesafe_handler.py`)**
   - Processa eventos de entrada com validação estrita e proteção de números/instâncias pessoais.

---

## 🔒 Princípios de Privacidade (Zero-Storage / Sanitized)
- Nenhuma chave de API real, número de telefone pessoal (`5527996380759`), IP privado (`74.1.x.x`) ou token de produção está presente nesta skill pública.
- Todos os templates utilizam placeholders genéricos (<your-domain>, <instance_id>, <api_key>).
- Esta skill é **100% gratuita, open-source e pública** para a comunidade Hermes / ClawHub.
