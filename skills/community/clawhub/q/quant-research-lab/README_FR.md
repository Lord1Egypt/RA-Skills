<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">中文</a> |
  <a href="README_JA.md">日本語</a> |
  <a href="README_FR.md">Français</a> |
  <a href="README_RU.md">Русский</a>
</p>

<p align="center">
  <h1 align="center">Quant Research Lab</h1>
  <p align="center">
    <strong>Laboratoire de Recherche Quantitative</strong>
  </p>
  <p align="center">
    Cadre R&D de Stratégies Quantitatives Multi-Agents
  </p>
  <p align="center">
    15 Agents LLM Spécialisés, Modélisés d'après les Plus Grandes Firms Quant
  </p>
</p>

<p align="center">
  <a href="https://github.com/anthropics/claude-code" target="_blank"><img alt="Claude Code" src="https://img.shields.io/badge/Claude_Code-Compatible-D97706?logo=anthropic&logoColor=white"/></a>
  <a href="https://hermes.nousresearch.com" target="_blank"><img alt="Hermes Agent" src="https://img.shields.io/badge/Hermes_Agent-Skill-7C3AED?logo=data:image/svg+xml;base64,..." /></a>
  <img alt="Roles" src="https://img.shields.io/badge/Roles-15-blue" />
  <img alt="Pipeline Tracks" src="https://img.shields.io/badge/Pipeline_Tracks-8-green" />
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" /></a>
</p>

---

> **Quant Research Lab** est une compétence d'agents IA qui apporte un flux de travail de recherche en stratégies quantitatives de niveau institutionnel aux agents de programmation alimentés par LLM. Il déploie 15 agents spécialisés — chacun modélisé selon l'expertise d'une grande firme quantitative (Goldman Sachs, Renaissance Technologies, Two Sigma, Citadel, Jane Street, et d'autres) — pour concevoir, backtester, gérer les risques et valider de manière collaborative des stratégies de trading quantitatives.

> ⚠️ **Avertissement** : Ce cadre est conçu uniquement à des fins de **recherche et d'éducation**. Il ne constitue pas un conseil financier, d'investissement ou de trading. Les performances de trading dépendent de nombreux facteurs, notamment le choix du modèle, la qualité des données et les conditions de marché. Effectuez toujours votre propre diligence raisonnable.

---

## Table des matières

- [Vue d'ensemble du cadre](#vue-densemble-du-cadre)
- [Les 15 rôles](#les-15-rôles)
- [Architecture du pipeline](#architecture-du-pipeline)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Portes de qualité](#portes-de-qualité)
- [Gestion de l'état](#gestion-de-letat)
- [Structure du projet](#structure-du-projet)
- [Contribuer](#contribuer)
- [Licence](#licence)

---

## Vue d'ensemble du cadre

Quant Research Lab reproduit le fonctionnement des véritables firmes de trading quantitatif : la recherche de stratégies complexes est décomposée en rôles spécialisés, chacun apportant une expertise métier depuis une perspective institutionnelle différente. Le cadre orchestre ces rôles à travers deux modes :

- **Mode Boîte à outils** — Invoquez n'importe quel rôle individuellement pour une analyse ciblée
- **Mode Pipeline** — Exécutez des pistes préconfigurées (séquences de rôles) pour une recherche de stratégies bout en bout

```
┌─────────────────────────────────────────────────────────────┐
│                    Quant Research Lab                        │
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Strategy  │→ │ Backtest │→ │   Risk   │→ │  Alpha   │   │
│  │ Architect │  │  Engine  │  │ Manager  │  │Researcher│   │
│  │ (GS)      │  │ (RenTech)│  │ (Two σ)  │  │ (Citadel)│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │             │              │         │
│       ▼              ▼             ▼              ▼         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Execution │  │  Factor  │  │ Stat Arb │  │  Macro   │   │
│  │ Algo     │  │  Model   │  │(D.E.Shaw)│  │(Bridge-  │   │
│  │ (Virtu)  │  │  (AQR)   │  │          │  │ water)   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │             │              │         │
│       ▼              ▼             ▼              ▼         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Data Pipe │  │    ML    │  │Portfolio │  │ Trading  │   │
│  │ (Bloomberg)│ │Researcher│  │Optimizer │  │ System   │   │
│  │          │  │(Point72) │  │(Man Grp) │  │(Millenn.)│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │Factor Backtest│  │  Compliance  │                        │
│  │(Dimensional)  │  │    (GS)      │                        │
│  └──────────────┘  └──────────────┘                        │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Quality Gate System                     │   │
│  │  Required Fields │ Numerical Sanity │ Dual Signatures│   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Les 15 rôles

Chaque agent est soutenu par un modèle de prompt détaillé qui définit la personnalité, l'expertise et une spécification de tâche multidimensionnelle structurée. Aucun rôle n'est un « assistant » générique — chaque agent réfléchit et produit des résultats dans le style de l'institution associée.

| ID | Rôle | Institution | Dépend de | Complexité | Phase |
|:---|:-----|:------------|:----------|:-----------|:------|
| 01 | **Architecte de Stratégie** | Goldman Sachs | — | Élevée | 1 |
| 02 | **Moteur de Backtest** | Renaissance Technologies | 01 | Normale | 1 |
| 03 | **Gestionnaire de Risques** | Two Sigma | 01 | Normale | 1 |
| 04 | **Chercheur Alpha** | Citadel | — | Élevée | 1 |
| 05 | **Teneur de Marché** | Jane Street | 01 | Normale | 3 |
| 06 | **Constructeur de Modèles Facteurs** | AQR | 02 | Normale | 2 |
| 07 | **Arbitrage Statistique** | D.E. Shaw | 01 | Normale | 2 |
| 08 | **Stratégie Macro** | Bridgewater Associates | 01 | Normale | 3 |
| 09 | **Pipeline de Données** | Bloomberg | — | Normale | 2 |
| 10 | **Algorithme d'Exécution** | Virtu Financial | 01 | Normale | 1 |
| 11 | **Chercheur ML** | Point72 | 01 | Élevée | 3 |
| 12 | **Optimiseur de Portefeuille** | Man Group | 01,02,03,06 | Normale | 2 |
| 13 | **Système de Trading** | Millennium Management | 10,12 | Normale | 2 |
| 14 | **Backtester de Facteurs** | Dimensional Fund Advisors | 01 | Normale | 3 |
| 15 | **Cadre de Conformité** | Goldman Sachs | 13 | Normale | 3 |

### Points forts des rôles

**Architecte de Stratégie (01)** — Couvre 9 dimensions de la conception de stratégies : thèse, sélection de titres, génération de signaux, règles d'entrée/sortie, dimensionnement des positions, paramètres de risque et spécifications d'implémentation. Chaque décision est appuyée par des formules mathématiques et du pseudocode.

**Moteur de Backtest (02)** — Cadre de validation à 10 dimensions incluant la qualité des données, l'architecture du moteur, la modélisation des coûts de transaction (Almgren-Chriss), la rigueur statistique (Ratio de Sharpe Déflaté, Taux de Faux Positifs) et les tests walk-forward.

**Gestionnaire de Risques (03)** — Évaluation des risques multicouche : risque de marché (VaR/CVaR), risque de liquidité, risque de contrepartie, risque extrême (EVT), avec des scénarios de stress testing issus de crises historiques.

**Chercheur Alpha (04)** — Pipeline de découverte de signaux alpha avec analyse IC/ICIR, modélisation de la décroissance des signaux et orthogonalisation multifactorielle.

**Constructeur de Modèles Facteurs (06)** — Construction complète de modèle factoriel de style Barra : facteurs alpha, facteurs de risque, estimation de la covariance factorielle et attribution basée sur les facteurs.

**Chercheur ML (11)** — Pipeline ML bout en bout : ingénierie des caractéristiques, sélection de modèles (XGBoost/LSTM/Transformer), optimisation des hyperparamètres et spécifications de déploiement en production.

---

## Architecture du pipeline

Les rôles forment un **Graphe Acyclique Dirigé (DAG)**, et non une chaîne linéaire. Différents scénarios de recherche utilisent différentes pistes :

| Piste | Phrase de déclenchement | Séquence de rôles | Temps estimé | Cas d'utilisation |
|:------|:------------------------|:-------------------|:-------------|:-----------------|
| **Core** (défaut) | "启动流水线" / "pipeline" | 01→02→03→04→10 | ~15min | Standard : Conception→Backtest→Risque→Alpha→Exécution |
| **Factor** | "因子流水线" | 01→02→06→14→12 | ~20min | Recherche factorielle : Construction→Backtest→Validation→Optimisation |
| **Execution** | "执行流水线" | 01→10→13→15 | ~18min | Déploiement système : Algo→Système de Trading→Conformité |
| **Macro** | "宏观流水线" | 01→08→03→12 | ~18min | Stratégie macro + risques + allocation de portefeuille |
| **Stat Arb** | "套利流水线" | 01→07→02→10 | ~18min | Trading par paires / stratégies de cointégration |
| **ML** | "ML流水线" | 01→11→02→03 | ~18min | Développement de stratégies pilotées par ML |
| **Market Making** | "做市流水线" | 01→05→10→13 | ~18min | Conception de système de teneur de marché |
| **Full** | "全量流水线" | 01→...→15 | ~40min | Complet bout en bout (à utiliser avec prudence) |

### Fonctionnalités du pipeline

- **Reprise à partir d'un point d'arrêt** — Mettez en pause à n'importe quel rôle, reprenez plus tard là où vous vous êtes arrêté
- **Ré-exécution** — Relancez à partir de n'importe quel rôle, en écrasant les résultats en aval
- **Pistes personnalisées** — Définissez vos propres séquences de rôles (par ex. « lancer 01→04→11 »)
- **Mode strict** — Arrêt sur les avertissements des portes de qualité au lieu de continuer automatiquement
- **Suivi de progression** — Affichage de la progression en temps réel avec le statut des portes de qualité par rôle

---

## Installation

### Option 1 : Installation en une ligne (Recommandé)

```bash
npx skills add https://github.com/yili1992/quant-research-lab --skill quant-research-lab
```

### Option 2 : Collez ceci dans Claude Code

> Installez la compétence `quant-research-lab`. Suivez ces étapes :
>
> 1. Assurez-vous que le répertoire `.claude/skills/` existe dans le projet courant (créez-le si nécessaire)
> 2. Exécutez `git clone https://github.com/yili1992/quant-research-lab.git .claude/skills/quant-research-lab`
> 3. Vérifiez : `ls .claude/skills/quant-research-lab/` doit afficher `SKILL.md`, `roles/`, `pipelines/`
> 4. Confirmez l'installation. Lorsque je décrirai des besoins en recherche quantitative, cette compétence s'activera automatiquement.

Collez le texte ci-dessus dans Claude Code — il gérera l'installation complète.

### Option 3 : Ligne de commande manuelle

```bash
git clone https://github.com/yili1992/quant-research-lab.git ~/.hermes/skills/quant-research-lab
```

### Option 4 : En tant que référence autonome

Les modèles de rôles dans `roles/` peuvent être utilisés indépendamment comme prompts système de haute qualité pour n'importe quel LLM — aucun cadre requis. Chaque fichier `.md` est autonome avec sa personnalité, sa spécification de tâche et ses exigences de format de sortie.

### Déclencheurs

Une fois installée, la compétence s'active automatiquement lorsque vous décrivez des besoins en recherche quantitative :

- "Lance un backtest de cette stratégie" — Déclenche le moteur de backtest
- "Lance le pipeline quantitatif" — Affiche le menu de sélection des pistes
- "run a quant pipeline" — Déclencheurs en anglais
- "Utilise le rôle Goldman Sachs" — Mode boîte à outils

---

## Utilisation

### Déclencheurs en langage naturel

La compétence s'active automatiquement lorsque vous décrivez des besoins de recherche quantitative :

```
"帮我设计一个费率套利策略"           → Déclenche l'Architecte de Stratégie (01) (Aide-moi à concevoir une stratégie d'arbitrage de frais)
"做一下这个策略的回测"               → Déclenche le Moteur de Backtest (02) (Fais le backtest de cette stratégie)
"启动量化流水线"                     → Affiche le menu de sélection des pistes (Lancer le pipeline quantitatif)
"因子流水线"                         → Démarre la piste Factor (Pipeline factoriel)
"从角色 03 恢复"                     → Reprend le pipeline depuis le Gestionnaire de Risques (Reprendre depuis le rôle 03)
"用高盛角色" / "做回测" / "风控分析"  → Mode boîte à outils pour des rôles spécifiques (Utiliser le rôle GS / Faire un backtest / Analyse des risques)
"流水线进度" / "status"              → Affiche la progression actuelle du pipeline (Progression du pipeline)
"重置流水线" / "reset"               → Réinitialise l'état du pipeline (Réinitialiser le pipeline)
```

### Mode Boîte à outils

Utilisez des rôles individuels pour une analyse ciblée sans exécuter un pipeline complet :

1. Prononcez le nom du rôle ou décrivez la tâche
2. La compétence identifie le rôle approprié, charge son modèle et dépêche un sous-agent
3. Les résultats sont enregistrés dans `state/research-context.md` avec les annotations des portes de qualité
4. Les rôles en aval qui dépendent de celui-ci sont suggérés comme étapes suivantes

### Mode Pipeline

Exécutez des pistes de recherche bout en bout :

1. Sélectionnez une piste (ou laissez la compétence en suggérer une selon votre objectif)
2. Vérifiez le plan d'exécution : séquence de rôles, temps estimé, graphe de dépendances
3. Confirmez pour démarrer — les rôles s'exécutent séquentiellement avec passage automatique du contexte
4. Surveillez la progression avec une sortie de style `[1/5] 01 Strategy Architect ✅ [QAGATE: PASS]`
5. Mettez en pause à tout moment avec « 暂停 », reprenez plus tard avec « 从角色 NN 恢复 »

---

## Portes de qualité

Chaque sortie de rôle passe par des contrôles de qualité automatisés avant d'être acceptée dans le pipeline :

| Contrôle | Portée | Ce qu'il détecte | En cas d'échec |
|:---------|:-------|:-----------------|:---------------|
| **Champs requis** | Tous les rôles | Bloc `[QAGATE]` manquant, conclusion principale vide, champs aval manquants | `[输出不完整]` |
| **Cohérence numérique** | Rôles Backtest/Risque/Facteurs | Sharpe > 50, MaxDD > -99%, ou autres valeurs invraisemblables | `[数值极端异常]` |
| **Signatures doubles** | Rôles numériques | `method_signature` ou `data_signature` manquant | `[缺少签名]` |

Le bloc QAGATE intégré dans la sortie de chaque rôle sert de rapport de qualité structuré :

```
[QAGATE]
core_conclusion: Strategy achieves Sharpe 1.8 with 12% max drawdown
key_params: lookback=20, threshold=2.0σ, rebalance=weekly
downstream_fields: signal_formula, entry_rules, risk_params
method_signature: momentum_zscore_v1
data_signature: binance_btcusdt_perp_2023_2025
[/QAGATE]
```

---

## Gestion de l'état

L'état du pipeline est persisté dans `state/research-context.md` — un seul fichier markdown avec un frontmatter YAML :

```yaml
---
pipeline_id: btc-arb-20260504
pipeline_track: "核心流水线"
status: in-progress
current_role_id: "03"
completed_roles: ["01", "02"]
next_recovery: "04"
created_at: 2026-05-04T02:16:00Z
project: btc-arb
---
```

La sortie complète de chaque rôle est ajoutée entre les marqueurs `<!-- ROLE_OUTPUT_START:{ID} -->` et `<!-- ROLE_OUTPUT_END:{ID} -->`, permettant :

- **Reprise** — Fermez votre session, revenez plus tard, reprenez là où vous en étiez
- **Ré-exécution sélective** — Écrasez les résultats d'un rôle spécifique et relancez-le
- **Contexte inter-rôles** — Les rôles en aval reçoivent automatiquement les paramètres et conclusions des rôles en amont
- **Piste d'audit** — Historique complet de la sortie de chaque rôle avec les résultats des portes de qualité

---

## Structure du projet

```
quant-research-lab/
├── SKILL.md                          # Skill definition & orchestration logic
├── README.md                         # This file
├── LICENSE                           # MIT License
├── roles/                            # Role prompt templates
│   ├── 01-gs-strategy-architect.md   # Goldman Sachs Strategy Architect
│   ├── 02-rentec-backtest-engine.md  # Renaissance Technologies Backtest Engine
│   ├── 03-twosigma-risk-manager.md   # Two Sigma Risk Manager
│   ├── 04-citadel-alpha-researcher.md# Citadel Alpha Researcher
│   ├── 05-js-market-maker.md         # Jane Street Market Maker
│   ├── 06-aqr-factor-builder.md      # AQR Factor Model Builder
│   ├── 07-deshaw-stat-arb.md         # D.E. Shaw Statistical Arbitrage
│   ├── 08-bridgewater-macro.md       # Bridgewater Macro Strategy
│   ├── 09-bbg-data-pipeline.md       # Bloomberg Data Pipeline
│   ├── 10-virtu-execution.md         # Virtu Execution Algorithm
│   ├── 11-point72-ml-researcher.md   # Point72 ML Researcher
│   ├── 12-man-portfolio-optimizer.md # Man Group Portfolio Optimizer
│   ├── 13-millennium-trading-system.md # Millennium Trading System
│   ├── 14-dimensional-factor-backtest.md # Dimensional Factor Backtest
│   └── 15-gs-compliance.md           # Goldman Sachs Compliance Framework
├── state/                            # Pipeline state (auto-generated)
│   └── research-context.md
└── docs/                             # Design documents & specs
    └── superpowers/
```

---

## Fonctionnement en coulisses

1. **Activation de la compétence** — Correspondance en langage naturel ou déclencheur explicite `/quant-research-lab`
2. **Collecte du contexte** — Lecture du registre des rôles, vérification de l'état existant du pipeline, collecte des entrées utilisateur (marché, capital, focus)
3. **Chargement du modèle** — Lecture du fichier `.md` du rôle cible pour obtenir le modèle de prompt complet
4. **Substitution des placeholders** — Remplacement de `{user_market}`, `{user_capital}`, `{user_focus}`, `{upstream_params}`, `{upstream_summary}` par les valeurs collectées
5. **Déploiement du sous-agent** — Lancement d'un sous-agent dédié (Opus pour les rôles haute complexité, Sonnet pour les rôles normaux) avec le prompt complété
6. **Évaluation de la porte de qualité** — Analyse du bloc QAGATE, exécution de 3 contrôles automatisés
7. **Persistance de l'état** — Ajout de la sortie au fichier d'état avec marqueurs, mise à jour du frontmatter
8. **Suggestion de l'étape suivante** — Balayage du graphe de dépendances et suggestion du prochain rôle logique

---

## Contribuer

Les contributions sont les bienvenues ! Voici comment vous pouvez aider :

### Ajouter un nouveau rôle

1. Créez `roles/NN-your-role.md` en suivant la structure du modèle existant :
   - Section **Personnalité** : parcours institutionnel, domaines d'expertise, philosophie de travail
   - Section **Description de la tâche** : dimensions numérotées avec exigences quantitatives concrètes
   - Section **Format de sortie** : markdown structuré avec tableaux, formules et pseudocode
   - Section **QAGATE** : champs requis et critères de qualité
2. Ajoutez le rôle au tableau registre dans `SKILL.md`
3. Définissez les relations `depends_on` et assignez une `Phase` (1/2/3)

### Ajouter une nouvelle piste de pipeline

1. Définissez la séquence de rôles basée sur le DAG de dépendances
2. Ajoutez-la au tableau des pistes dans `SKILL.md`
3. Ajoutez des mots-clés de déclenchement pour la correspondance en langage naturel

### Améliorer les rôles existants

Chaque modèle de rôle est conçu pour produire des résultats de niveau institutionnel. Les améliorations sont bienvenues dans :
- Des spécifications mathématiques plus précises
- Une gestion supplémentaire des cas limites
- Une meilleure méthodologie statistique
- La modélisation des contraintes du monde réel

---

## Licence

Licence MIT — voir [LICENSE](LICENSE) pour les détails.

---

