---
name: setup-client-workspace
description: "Mise en place d'un workspace agent dédié pour un nouveau client TNCG. Utiliser quand Erwan demande de configurer un nouvel agent client (workspace, fichiers de base, config OpenClaw, WhatsApp linking, sandbox, escalation, monitoring)."
---

# Setup Client Workspace (Orchestrateur)

Ce skill est l'orchestrateur. Il reste court par design.
Les détails opérationnels sont dans `references/`.

## Règle d'exécution

Quand Erwan demande de créer/configurer un agent client :

1. Lire `references/workflow.md` (vue d'ensemble + ordre des étapes)
2. Lire `references/templates.md` pour générer les fichiers workspace
3. Lire `references/openclaw-config.md` pour la config JSON, WhatsApp, bindings, sandbox
4. Lire `references/security-checklist.md` avant validation finale

Ne pas improviser hors de ces procédures sans le signaler explicitement.

## Minimum à collecter avant setup

- Nom du client / entreprise
- Rôle de l'agent (admin, commercial, webmaster, ...)
- Contexte métier (secteur, contraintes)
- Fuseau horaire client + horaires de travail (obligatoire)
- Site/repo GitHub si l'agent modifie un site

## Convention horaire (obligatoire)

Pour toute alerte/rappel client :

- afficher d'abord l'heure **client**,
- puis conversions utiles (UTC / Taiwan / France) seulement si nécessaire.

Format recommandé :
`Rappel: 09:00 Europe/Paris (16:00 Taiwan, 08:00 UTC)`

## Principe d'architecture

- Skill = procédure / playbook
- Plugin = code runtime (nouveaux tools, hooks, commandes)

Pour ce cas d'usage (onboarding client), rester en skill modulaire.
