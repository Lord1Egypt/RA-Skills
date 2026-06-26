---
name: setup-client-workspace
description: "Mise en place d'un workspace agent dédié pour un nouveau client TNCG. Utiliser quand Erwan demande de configurer un nouvel agent pour un client. Couvre : création workspace, SOUL.md, IDENTITY.md, TOOLS.md, BOOTSTRAP.md, USER.md, MEMORY.md, compte WhatsApp dédié, sandbox Docker, escalation vers David, cron monitoring usage."
---

# Setup Client Workspace

Procédure complète pour déployer un agent dédié à un nouveau client TheNoCodeGuy.

## Prérequis

Avant de commencer, obtenir d'Erwan :
1. **Nom du client / entreprise**
2. **Rôle de l'agent** (assistant admin, commercial, webmaster, etc.)
3. **Contexte métier** (secteur, services, particularités)
4. **Fuseau horaire client + horaires de travail** (obligatoire pour rappels/cron)
5. **Site web** (optionnel — si l'agent doit pouvoir modifier du contenu)
6. **Repo GitHub du site** (optionnel — si site web, pour configurer le push)

Le numéro WhatsApp du client n'est PAS nécessaire en amont — le client scanne un QR code pour lier son propre WhatsApp (voir étape 9).

## Étapes

### 1. Créer le workspace

```bash
mkdir -p ~/.openclaw/workspace-<client>/docs
```

### 2. Créer SOUL.md

Adapter le template ci-dessous au contexte du client :

```markdown
# SOUL.md — [rôle] de [Prénom Client]

<!-- Remplacer toutes les variables [entre crochets] par les infos du client. -->

## Contraintes

**Toujours :**
- Répondre en français, ton professionnel direct
- Confirmer avant toute action irréversible
- Anonymiser les données clients dans toute escalation

**Demander d'abord :**
<!-- Lister les actions spécifiques au client qui nécessitent confirmation. -->
- [actions spécifiques au client nécessitant confirmation]

**Jamais :**
- Décisions financières ou contractuelles
- Contact d'un tiers sans accord explicite de [Prénom]
- Données confidentielles en clair dans une escalation

## Identité

[Description courte : rôle, entreprise, localisation, équipe.]

## Communication

Quand [Prénom] pose une question métier :
- Réponse directe, max 3 paragraphes, puces si plus de 2 items

Quand [Prénom] demande une rédaction (courrier, email, document) :
- Produire un brouillon complet, demander validation avant envoi

Quand la réponse n'est pas vérifiable :
- Le dire explicitement, proposer une recherche ou une escalation L2

Quand [Prénom] ne demande rien :
- Ne rien envoyer. Pas de messages proactifs sauf heartbeat configuré.

## Escalation (ITIL)

### L1 — Autonome

Triggers : questions métier, rédaction, recherche, [outils spécifiques au client].

Action : traiter directement. En cas d'échec, expliquer le blocage à [Prénom] avant d'escalader.

### L2 — David/Erwan

Triggers :
- Problème technique non résolu après tentative
- [Prénom] insatisfait(e) malgré les tentatives
- Action humaine requise (OAuth bloqué, infra, bug)
- Demande hors périmètre

Procédure :
1. Dire à [Prénom] : "Je transmets à Erwan (support technique)."
2. Appeler l'outil `sessions_send` avec ces paramètres :
   - `agentId`: `"david"`
   - `message`: description du problème + ce qui a été tenté + résultat obtenu
3. Erwan reçoit le message et contacte [Prénom] directement

## Apprentissage continu

Quand un problème nouveau est résolu :
- Noter la solution dans MEMORY.md (problème, cause, résolution)

Quand la même demande revient 3 fois :
- Proposer à [Prénom] d'automatiser
```

### 3. Créer IDENTITY.md

```markdown
# IDENTITY.md
- **Name:** [Nom Agent]
- **Creature:** Assistant [rôle] pour [Client]
- **Vibe:** [description courte du style]
- **Emoji:** [emoji pertinent]
```

### 4. Créer USER.md

```markdown
# USER.md — Profil utilisateur

## [Prénom Client]

- **Métier :** [rôle, entreprise]
- **Localisation :** [ville, fuseau horaire]
- **Canal principal :** WhatsApp
- **Langue :** Français
- **Référence horaire des rappels :** [heure client] + conversions [UTC / Taiwan / France si utile]

## Style de communication

- À compléter au fil des échanges
```

### 5. Créer MEMORY.md

```markdown
# MEMORY.md — Mémoire long terme

## [Prénom Client] — Infos clés

- [Infos de base sur le client]

## [Entreprise] — L'entreprise

- [Description courte]

## Historique

- [date] : Workspace créé. Agent configuré par Erwan (TheNoCodeGuy).
```

### 6. Créer BOOTSTRAP.md (onboarding premier contact)

```markdown
# BOOTSTRAP — Premier contact avec [Prénom]

C'est ton premier échange avec [Prénom]. Avant toute chose, fais connaissance.

## Ce que tu dois faire

1. **Présente-toi brièvement** — dis que tu es son assistant IA mis en place par Erwan (TheNoCodeGuy).

2. **Demande-lui comment il/elle veut t'appeler.** Mets à jour IDENTITY.md avec le nom choisi.

3. **Demande ses priorités** — qu'est-ce qui prend le plus de temps ? Qu'est-ce qu'il/elle aimerait déléguer en premier ? Note dans MEMORY.md.

4. **Demande si il/elle veut des rappels proactifs** — si oui, crée un HEARTBEAT.md adapté.

5. **Demande son fuseau horaire et ses horaires de travail** — note dans USER.md.

6. **Valide la convention d'horaires** — tous les rappels doivent être exprimés d'abord en heure client, puis conversion explicite (UTC/Taiwan/France si pertinent).

7. **Confirme que tu es prêt** — résume ce que tu as compris.

## Ton
Chaleureux mais professionnel. Premier contact — bonne impression sans en faire trop.

## Après
Une fois l'onboarding terminé, **supprime ce fichier** (BOOTSTRAP.md).
```

### 7. Créer TOOLS.md

**RÈGLE : jamais de secrets en clair.** Utiliser des fichiers hors workspace ou des variables d'env.

Template de base :

```markdown
# TOOLS.md — Procédures opérationnelles

## 1. Messagerie WhatsApp

Tu peux envoyer des messages WhatsApp au nom de [Prénom] via son compte lié.

### Envoyer un message

Quand [Prénom] demande d'envoyer un message WhatsApp :
1. Confirmer le destinataire et le contenu avec [Prénom] (contrainte : jamais contacter un tiers sans accord)
2. Appeler l'outil `message` avec ces paramètres :
   - `action`: `"send"`
   - `channel`: `"whatsapp"`
   - `accountId`: `"<client>"`
   - `target`: numéro du destinataire au format E.164 (ex: `"+33612345678"`)
   - `message`: le texte du message

### Envoyer un fichier

Quand [Prénom] demande d'envoyer un document :
1. Appeler l'outil `message` avec :
   - `action`: `"send"`
   - `channel`: `"whatsapp"`
   - `accountId`: `"<client>"`
   - `target`: numéro du destinataire
   - `media`: chemin du fichier ou URL
   - `caption`: texte d'accompagnement (optionnel)

### Règles
- Numéro au format E.164 : `+33...`, `+1...`
- Ne jamais envoyer sans accord explicite de [Prénom]
- Si numéro sans indicatif pays, demander confirmation

## 2. Automations & Workflows

Pour mettre en place des automatisations, **escalade vers David**.
L'infrastructure d'automation (Windmill) est gérée par l'équipe technique.

### Callback hooks Windmill → Gateway (⚠️ BETA)

Les jobs Windmill longs peuvent notifier la gateway via POST `/hooks/windmill`. Le résultat est relayé sur WhatsApp via le système d'announce. Voir **skill `windmill-setup` § 6. Callback Hooks** pour la configuration complète.

Pour chaque nouveau workflow client dans Windmill :
1. Créer le script métier dans Windmill (ex: `f/<client>/mon_script`)
2. Créer un wrapper `f/<client>/mon_script_and_notify` qui appelle le script + `notify_gateway(summary)`
3. La variable `f/openclaw/gateway_hook_token` est partagée (pas besoin d'en créer par client)
4. Le mapping `/hooks/windmill` route vers David qui forward à Erwan

## 3. Escalation technique (outil sessions_send)

Voir SOUL.md section "Escalation (ITIL)" pour les critères et triggers.

### Comment escalader vers David/Erwan

Appeler l'outil `sessions_send` avec :
- `agentId`: `"david"`
- `message`: description du problème + ce qui a été tenté

Exemple :
  Outil: sessions_send
  Paramètres:
    agentId: "david"
    message: "API retourne 401. Token vérifié. [Prénom] attend un retour."
```

#### Si le client a un site web à gérer

Ajouter une section site web dans TOOLS.md. Identifier les fichiers "safe" (contenu, textes, navigation) vs "dangereux" (composants, layouts, CSS, config build).

Règle : l'agent peut modifier le contenu textuel, pas le design ni la structure.

Les fichiers du site sont montés via bind mounts Docker dans le sandbox (voir étape 8).

Ajouter la procédure de publication :
```markdown
## Site web

Le site est monté à `/mnt/site/`.

### Modification de contenu (autonome)

Quand [Prénom] demande un changement textuel :
1. Modifier les fichiers concernés
2. Publier :
   ```bash
   cd /mnt/site && git add <fichiers> && git commit -m '<description>' && git push
   ```
3. Notifier David via l'outil `sessions_send` :
   - `agentId`: `"david"`
   - `message`: `"Site mis à jour : <description>"`

### Modification structurelle (composants/layout/CSS)

Quand [Prénom] demande un changement de structure :
1. Résumer le changement prévu et demander confirmation
2. Si confirmé, appliquer la même procédure de publication
```

### 8. Configurer openclaw.json

#### Ajouter l'agent dans `agents.list` :

```json
{
  "id": "<client>",
  "workspace": "/home/ubuntu/.openclaw/workspace-<client>",
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "fallbacks": ["anthropic/claude-haiku-4-5", "google/gemini-3-flash-preview"]
  },
  "tools": {
    "deny": ["gateway", "process"],
    "alsoAllow": ["message", "sessions_send", "sessions_list", "sessions_history"],
    "sandbox": {
      "tools": {
        "allow": [
          "exec", "process", "read", "write", "edit", "apply_patch", "image",
          "sessions_list", "sessions_history", "sessions_send", "sessions_spawn",
          "subagents", "session_status", "message"
        ],
        "deny": [
          "browser", "canvas", "nodes", "cron", "gateway",
          "telegram", "discord", "irc", "googlechat", "slack", "signal", "imessage"
        ]
      }
    }
  },
  "sandbox": {
    "mode": "all",
    "scope": "agent",
    "workspaceAccess": "rw",
    "docker": {
      "image": "openclaw-sandbox:bookworm-slim",
      "network": "bridge",
      "readOnlyRoot": true,
      "memory": "512m",
      "cpus": 1
    }
  }
}
```

> **Pourquoi `tools.sandbox.tools` ?** Le sandbox a sa propre policy qui bloque tous les channels par defaut (`whatsapp`, `telegram`, etc.) et n'inclut pas `message` dans son allow. Sans cette config explicite, l'agent ne peut ni envoyer de WhatsApp ni escalader, meme si `alsoAllow` le permet au niveau agent. Verifier avec `openclaw sandbox explain --agent <client>`.

#### Si le client a un site web — ajouter un bind mount + git credentials :

```json
"sandbox": {
  "docker": {
    "dangerouslyAllowExternalBindSources": true,
    "binds": [
      "/chemin/vers/repo-site:/mnt/site"
    ]
  }
}
```

Configurer git push dans le repo du site :
```bash
cd /chemin/vers/repo-site
git remote set-url origin "https://<github-user>:<token>@github.com/<owner>/<repo>.git"
git config user.email "assistant@<domaine-client>"
git config user.name "<Nom Agent>"
```

Le token est stocké dans `.git/config` (pas versionné). L'agent peut push directement grâce à `network: bridge`.

#### Ajouter le compte WhatsApp du client :

Dans `channels.whatsapp.accounts` :
```json
"<client>": {
  "name": "<Nom Client / Entreprise>",
  "enabled": true,
  "dmPolicy": "allowlist",
  "allowFrom": []
}
```

Le `allowFrom` sera rempli après le scan QR (le numéro du client y sera ajouté).

#### Ajouter le binding WhatsApp :
```json
{
  "agentId": "<client>",
  "match": {
    "channel": "whatsapp",
    "accountId": "<client>",
    "peer": { "kind": "direct", "id": "+<numéro>" }
  }
}
```

#### Communication inter-agents (agentToAgent + sessions)

La communication inter-agents (`sessions_send`, `sessions_list`, etc.) nécessite **4 couches** de configuration. Si une seule manque, l'escalation échoue silencieusement.

##### Couche 1 — Agent-level tools

```json
"tools": {
  "alsoAllow": ["message", "sessions_send", "sessions_list", "sessions_history"]
}
```

**Piège :** `allow` = whitelist stricte (UNIQUEMENT ces outils). `alsoAllow` = ajout aux outils par défaut. Toujours utiliser `alsoAllow`.

##### Couche 2 — Sandbox tool policy

Le sandbox a sa propre policy avec `DEFAULT_TOOL_DENY` qui bloque **tous les channels** (whatsapp, telegram, etc.) et `DEFAULT_TOOL_ALLOW` qui n'inclut **pas** `message`. Sans override explicite, l'agent sandbox ne peut ni envoyer de WhatsApp ni escalader.

```json
"tools": {
  "sandbox": {
    "tools": {
      "allow": ["exec", "process", "read", "write", "edit", "apply_patch", "image",
        "sessions_list", "sessions_history", "sessions_send", "sessions_spawn",
        "subagents", "session_status", "message"],
      "deny": ["browser", "canvas", "nodes", "cron", "gateway",
        "telegram", "discord", "irc", "googlechat", "slack", "signal", "imessage"]
    }
  }
}
```

**Piège :** `whatsapp` ne doit PAS être dans `deny` ici — sinon l'outil `message` ne peut pas envoyer via WhatsApp.

##### Couche 3 — sessionToolsVisibility

Le sandbox clamp la visibilité des sessions à `"tree"` par défaut (l'agent ne voit que ses propres sessions). Pour l'escalation cross-agent, il faut :

```json
"sandbox": {
  "sessionToolsVisibility": "all"
}
```

C'est au même niveau que `mode`, `scope`, `docker` dans le bloc `sandbox`.

##### Couche 4 — Config globale

Au niveau racine de `openclaw.json` (PAS au niveau agent) :

```json
"tools": {
  "sessions": { "visibility": "all" },
  "agentToAgent": { "enabled": true, "allow": ["david", "kelly"] }
}
```

**Piège :** `tools.sessions` et `tools.agentToAgent` n'existent qu'au niveau global. Les mettre dans un agent fait crasher la gateway.

##### agentToAgent.allow — comportement et isolation multi-tenant

`allow` est une **flat list, pas directionnelle**. Si `["david", "kelly", "client-a"]` : client-a peut parler à david ET kelly (et vice versa). Il n'y a pas de filtre "client-a ne peut parler QU'à kelly".

**Pattern recommandé pour l'isolation multi-tenant :**

Ne PAS mettre les agents clients dans `agentToAgent.allow`. Ainsi :
1. L'agent client communique UNIQUEMENT via son canal WhatsApp (bindé à Kelly)
2. Kelly est dans `allow` → elle peut escalader vers David via `sessions_send`
3. David reçoit, traite, répond à Kelly qui répond au client
4. Le client ne peut physiquement pas contacter David : son seul canal est WhatsApp, bindé à Kelly

Le routing directionnel se fait via le **channel binding**, pas via agentToAgent.

### 9. Lier le WhatsApp du client

Le client lie son propre WhatsApp à la gateway (comme WhatsApp Web). L'agent envoie et reçoit depuis le numéro du client.

```bash
# Valider le JSON
node -e "JSON.parse(require('fs').readFileSync('/home/ubuntu/.openclaw/openclaw.json','utf8')); console.log('OK')"

# Redémarrer la gateway
pkill -9 -f openclaw-gateway || true
nohup openclaw gateway run --bind loopback --port 18789 --force > /tmp/openclaw-gateway.log 2>&1 &

# Lancer le login WhatsApp pour le client
openclaw channels login --channel whatsapp --account <client>
```

Un QR code s'affiche. Le client le scanne depuis **WhatsApp → Appareils liés → Lier un appareil**.

Après connexion :
1. Le numéro du client apparaît dans les logs
2. Ajouter ce numéro dans `allowFrom` du compte et dans le binding `peer.id`
3. Redémarrer la gateway

Le client parle à l'agent en s'envoyant un message à lui-même (self-chat WhatsApp).

### 10. Monitoring usage (recommandé)

Ajouter un cron OpenClaw pour surveiller l'usage du nouvel agent :

```bash
openclaw cron add \
  --name "<client>-usage-alert" \
  --agent david \
  --every "1h" \
  --announce --channel whatsapp --to "+886920010612" \
  --best-effort-deliver \
  --message "Check usage agent <client> aujourd'hui. Alerte si > 5 USD." \
  --thinking low \
  --model "anthropic/claude-haiku-4-5"
```

## Checklist finale

- [ ] Workspace créé avec tous les fichiers : SOUL.md, IDENTITY.md, TOOLS.md, USER.md, MEMORY.md, BOOTSTRAP.md
- [ ] Fuseau horaire client documenté + convention d'affichage des rappels validée (heure client d'abord)
- [ ] Agent ajouté dans openclaw.json (agents.list)
- [ ] Sandbox Docker configuré (mode: all, scope: agent, network: bridge)
- [ ] Bridges socat docker0 actifs : `socat-bridge-gateway-18789` et `socat-bridge-windmill-8000` (partagés par tous les sandboxes, voir skill windmill-setup § Inventaire)
- [ ] Bind mount site web + git credentials (si applicable)
- [ ] Compte WhatsApp `<client>` créé dans channels.whatsapp.accounts
- [ ] Client a scanné le QR code (WhatsApp lié)
- [ ] Numéro client dans allowFrom du compte + binding peer.id
- [ ] accountId dans le binding
- [ ] Communication inter-agents : 4 couches vérifiées (alsoAllow, sandbox.tools, sessionToolsVisibility, global agentToAgent)
- [ ] Si multi-tenant : agent client PAS dans agentToAgent.allow (relay via Kelly)
- [ ] Tools restreints (deny: gateway, process)
- [ ] Secrets dans .git/config ou fichiers hors workspace, PAS dans les fichiers workspace
- [ ] JSON validé + gateway restart
- [ ] Test : le client s'envoie un message (self-chat) → l'agent répond avec le BOOTSTRAP
- [ ] Cron monitoring usage en place

## Sécurité — rappels

- **Sandbox Docker obligatoire** pour tout agent client (mode: all, scope: agent)
- **Image** : `openclaw-sandbox:bookworm-slim` (construite via `scripts/sandbox-setup.sh`)
- **Network: bridge** — accès réseau pour git push, web search, API calls
- **Bridges socat docker0** — Les sandboxes tournent sur le réseau `bridge` (docker0, gateway 172.17.0.1). Deux bridges partagés par tous les clients : `socat-bridge-gateway-18789` (→ gateway OpenClaw) et `socat-bridge-windmill-8000` (→ Windmill). Vérifier qu'ils sont actifs (`systemctl status socat-bridge-*`). Pas besoin d'en créer par client. Voir skill `windmill-setup` § Inventaire bridges.
- **readOnlyRoot: true** — filesystem container en lecture seule (sauf workspace et binds)
- **Tools deny** : au minimum `gateway` et `process`
- **Pas de secrets en clair** dans les fichiers workspace — utiliser .git/config pour les tokens GitHub, fichiers workspace pour tokens API (ex: `.windmill-token`)
- **Bind mount site** : repo complet monté (versionné git = réversible), l'agent est guidé par TOOLS.md
- **dangerouslyAllowExternalBindSources** : nécessaire uniquement si bind mounts hors workspace
- **WhatsApp multi-compte** : chaque client a son propre compte WhatsApp lié. L'agent envoie depuis le numéro du client, PAS depuis celui d'Erwan.
- **agentToAgent** : flat list (pas directionnelle). Pour l'isolation multi-tenant, ne PAS mettre les agents clients dans `allow` — ils communiquent uniquement via leur canal WhatsApp bindé à Kelly (relay pattern)
- **sessionToolsVisibility** : doit être `"all"` dans le bloc sandbox pour que l'escalation cross-agent fonctionne. Par défaut le sandbox clamp à `"tree"` (l'agent ne voit que ses propres sessions)
- **tools.sessions.visibility** : doit être `"all"` au niveau **global** (pas agent). Sans ça, `sessions_send` cross-agent échoue silencieusement
- Le client ne doit **jamais** avoir accès aux données d'un autre client ou au workspace principal
