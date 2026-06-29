---
name: codex-dev-deploy
description: Guide pas à pas pour coder avec OpenAI Codex CLI, gérer un repo GitHub, et déployer sur un serveur. Nécessite codex CLI, git, et optionnellement des tokens de déploiement.
homepage: https://developers.openai.com/codex/
version: 2.0.0
author: qapten
metadata: {
  "openclaw": {
    "requires": {
      "bins": ["codex", "git", "npm"],
      "anyBins": ["gh", "curl", "ssh", "docker"]
    },
    "primaryEnv": "GH_TOKEN"
  }
}
---

# Codex CLI — Flow Complet : Dev → GitHub → Deploy

## Vue d'ensemble

Cette skill guide un développeur pas à pas pour :
1. Installer et authentifier **OpenAI Codex CLI**
2. Coder avec Codex (tâches simples à complexes)
3. Gérer un repo **GitHub**
4. Déployer sur un serveur (**Coolify**, **Railway**, ou **SSH classique**)

⚠️ Cette skill est **générique** — remplace les placeholders `<...>` par tes propres infos.

---

## Prérequis

### Binaires requis (déclarés en metadata)

- **codex** — le coding agent CLI OpenAI
- **git** — gestion de version
- **npm** — installation de codex

### Binaires optionnels (selon ton workflow)

- **gh** (GitHub CLI) — gestion de repos depuis la CLI
- **curl** — appels API (Coolify, GitHub)
- **ssh** — connexion aux serveurs
- **docker** — déploiement conteneurisé

### Variables d'environnement (recommandées)

- `GH_TOKEN` — Personal Access Token GitHub (optionnel, sinon passer par `gh auth login`)

### Secrets à configurer (non stockés dans le skill)

- `<GH_TOKEN>` — token GitHub avec droits `repo`
- `<COOLIFY_TOKEN>` — token API Coolify (si déployement Coolify)
- Clé SSH privée — accès au serveur de déploiement

---

## Étape 1 — Installer Codex CLI

```bash
npm install -g @openai/codex
```

Vérifier :
```bash
which codex
codex --help
```

---

## Étape 2 — Authentifier avec ChatGPT

### Méthode A : Device Code Flow (recommandé pour serveur/VPS)

```bash
codex login --device-auth
```

Le CLI affiche un code court (type `VQ4Z-XSTZV`). Ouvre **https://auth.openai.com/codex/device** dans ton navigateur, connecte-toi avec ton compte ChatGPT **Pro/Plus**, entre le code.

Vérifier :
```bash
codex login --status
```

### Méthode B : Flow navigateur (en local)

```bash
codex login
```

---

## Étape 3 — Coder avec Codex CLI

Codex n'est pas un LLM à qui tu poses des questions — c'est un **coding agent** qui lit, modifie et teste ton code sur place.

### Tâche simple

```bash
cd /chemin/du/projet
codex exec --json --color never --skip-git-repo-check "Décris ce que tu veux faire ici..."
```

### Avec sandbox désactivé (si le sandbox n'est pas supporté)

⚠️ **Utilise cette option uniquement si tu sais ce que tu fais** — elle désactive l'isolation du sandbox.

```bash
codex exec --json --color never --sandbox danger-full-access --skip-git-repo-check "Ta tâche..."
```

> **Recommandation de sécurité** : n'utilise pas `--sandbox danger-full-access` sur des machines contenant des données sensibles. Privilégie un conteneur isolé pour les tâches à risque.

### Tâche interactive (dans un terminal avec TTY)

```bash
cd /chemin/du/projet
codex "Décris ta tâche"
```

### Flags importants

| Flag | Pourquoi |
|---|---|
| `--skip-git-repo-check` | Permet de coder hors repo git "trusté" (VPS, Docker) |
| `--sandbox danger-full-access` | ⚠️ Désactive le sandbox — voir avertissement ci-dessus |
| `--json` | Sortie structurée en JSON (utile pour l'analyse automatisée) |
| `--color never` | Pas de codes ANSI (utile dans les logs non-TTY) |

### Exemples de tâches Codex

- "Crée un serveur Express.js avec un endpoint GET /api/health"
- "Ajoute une connexion PostgreSQL basée sur les variables d'environnement"
- "Fix le bug : la fonction parseJSON crash quand l'entrée est vide"
- "Ajoute des tests Jest pour le module auth"

---

## Étape 4 — Repo GitHub

### Authentifier GitHub

Via `gh` CLI :
```bash
gh auth login
```

Ou via token :
```bash
gh auth login --with-token <<< "$GH_TOKEN"
```

### Créer un nouveau repo

```bash
gh repo create ton-username/nom-repo --private --source=. --remote=upstream --push
```

### Git workflow

```bash
# Après que Codex a fait ses modifications
git add -A
git commit -m "Message descriptif du changement"
git push origin <branche>
```

### Conventions de messages

- `feat: ...` → nouvelle fonctionnalité
- `fix: ...` → correction de bug
- `docs: ...` → documentation
- `refactor: ...` → refactoring sans changement fonctionnel

---

## Étape 5 — Déploiement

### Option A : Coolify (auto-hébergé PaaS)

1. **Pré-requis** : Coolify installé (https://coolify.io)
2. Configurer l'app dans Coolify (repo GitHub, branche, variables d'environnement)

3. **Déployer** :
   ```bash
   # Via API Coolify
   curl -X POST "https://<COOLIFY_URL>/api/v1/deploy" \
     -H "Authorization: Bearer <COOLIFY_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{"uuid":"<APP_UUID>","force":true}'
   ```

### Option B : Railway

1. Connecter le repo GitHub dans Railway dashboard
2. Déploiement automatique sur push via GitHub
3. Variables d'environnement dans Railway settings

### Option C : SSH classique / VPS

```bash
# Push le code
git push origin main

# SSH sur le serveur
ssh root@<SERVER_IP>

# Pull et restart
cd /opt/mon-app
git pull origin main
npm install
pm2 restart mon-app
# ou docker compose pull && docker compose up -d --build
```

### Option D : Docker / Cloud Run / autre

- Push l'image Docker sur registry
- Deploy via la CLI du provider (gcloud, aws, etc.)

---

## Checklist de déploiement

Avant de déployer sur **prod** :
- [ ] Le code a été testé en staging
- [ ] Les variables d'environnement sont configurées
- [ ] Les migrations DB sont prêtes (si applicable)
- [ ] Un rollback plan est défini
- [ ] Validation d'un humain (pas de déploiement prod automatique sans go)

---

## Architecture type d'un projet

```
mon-projet/
├── .env.example          # Template des vars d'env (JAMAIS de vraies valeurs dans git)
├── .gitignore
├── package.json
├── server.js             # Point d'entrée
├── src/                  # Code source
├── tests/                # Tests
├── deploy/               # Scripts de déploiement
└── README.md             # Documentation
```

---

## ⚠️ Sécurité et bonnes pratiques

1. **JAMAIS commiter** de tokens, clés API, mots de passe ou `.env` réels
2. Utiliser `.env.example` pour documenter les vars nécessaires
3. Les secrets vont dans les variables d'environnement du serveur (Coolify, Railway, etc.)
4. Token GitHub avec le minimum de permissions nécessaires
5. SSH keys : permissions `600` pour la clé privée, `644` pour la publique
6. `--sandbox danger-full-access` : ne l'utiliser qu'en environnement isolé (container/VM dédiée)
7. **Ne jamais** exécuter Codex avec `--sandbox danger-full-access` sur une machine contenant des credentials de production

---

## Ressources

- Codex CLI docs : https://developers.openai.com/codex/
- Coolify docs : https://coolify.io/docs
- Railway docs : https://docs.railway.app
- Cloudflare DNS API : https://developers.cloudflare.com/api/
