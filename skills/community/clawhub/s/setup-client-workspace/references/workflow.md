# Workflow — Setup client workspace

## 0) Preparation

Collecter : client, role, contexte, fuseau horaire + horaires, site/repo (optionnel).

Obtenir du client ou d'Erwan :
- Numero WhatsApp du client (E.164)
- Cle OpenAI dediee pour cet agent (Whisper / transcription audio)

## 1) Creer le workspace

```bash
mkdir -p ~/.openclaw/workspace-<client>/docs
```

## 2) Generer les fichiers de base

Creer :
- `SOUL.md`
- `IDENTITY.md`
- `USER.md`
- `MEMORY.md`
- `BOOTSTRAP.md`
- `TOOLS.md`

Utiliser `templates.md`.

## 2b) Installer les skills standard

```bash
cd ~/.openclaw/workspace-<client>

# Self-improvement (capture erreurs/corrections/apprentissages)
clawhub install self-improving-agent

# Recherche web Tavily
clawhub install tavily-search

# Escalation vers le superviseur (webhook gateway)
cp -r ~/.openclaw/workspace/skills/escalation skills/escalation

# Creer les fichiers .learnings/ pour le self-improvement
mkdir -p .learnings
```

Creer les fichiers vides :
- `.learnings/LEARNINGS.md`
- `.learnings/ERRORS.md`
- `.learnings/FEATURE_REQUESTS.md`

Si `clawhub` installe au mauvais endroit (detecte un autre workspace), copier manuellement depuis un workspace existant.

**Note escalation :** le skill `escalation` utilise le webhook gateway (`/hooks/agent`) pour réveiller le superviseur même s'il n'a pas de session active. Variables d'env requises dans le sandbox : `HOOKS_TOKEN`, `GATEWAY_HOST`, `GATEWAY_PORT`. Le `DELIVER_TO` par défaut est le Telegram d'Erwan.

## 3) Configurer OpenClaw

Details exacts : `openclaw-config.md`.

### 3a) Agent dans `agents.list`
- Workspace separe
- Modele : `anthropic/claude-opus-4-6` primaire, `openai-codex/gpt-5.4` fallback
- Sandbox avec browser enabled
- Inter-agent comm (tools.alsoAllow, sessionToolsVisibility)
- `identity` : laisser vide au setup initial (l'agent choisit son nom au bootstrap). Une fois le nom choisi, mettre à jour `identity.name` avec le prénom. Cela active le préfixe `[Nom]` en self-chat WhatsApp.

### 3b) Compte WhatsApp
- `dmPolicy: "allowlist"`
- `selfChatMode: true` (si le client utilise son propre numero)
- `allowFrom: ["+<numero-client>"]`
- `allowSendTo: ["*"]`

### 3c) Auth profiles
- Verifier que `anthropic:openclaw` et `openai-codex:default` sont herites
- Ajouter la cle OpenAI dediee `openai:<client>` dans le store agent (pour Whisper)
- NE PAS utiliser la cle globale `OPENAI_API_KEY` — chaque agent a sa propre cle

### 3d) Communication inter-agents
- Ajouter le nouvel agent dans `tools.agentToAgent.allow`
- Verifier `tools.sessions.visibility: "all"`

### 3e) Socat bridge
- Verifier que le reseau Docker du sandbox a un socat vers la gateway (port 18789)
- Le reseau `bridge` est couvert par `socat-bridge-gateway-18789`

### 3f) Build
- Si le code source a ete modifie : `pnpm build` avant restart
- Le gateway tourne depuis `dist/index.js` (build local), pas npm global

## 4) Lier WhatsApp du client

```bash
openclaw channels login --channel whatsapp --account <client>
```

- Le client scanne le QR
- Verifier `allowFrom` + binding

## 5) Restart + verifications

```bash
openclaw gateway restart
```

Checklist :
1. [ ] Message WhatsApp selfChat ou depuis le numero client
2. [ ] Transcription audio (envoyer un vocal)
3. [ ] Communication inter-agents (`sessions_send` vers david)
4. [ ] Browser agent fonctionne dans le sandbox
5. [ ] Convention horaire (heure client d'abord dans les reponses)

## 6) Monitoring

Ajouter un cron leger de monitoring usage (optionnel mais recommande).

## Pieges connus

| Piege | Symptome | Solution |
|---|---|---|
| `openai/gpt-5.4` vs `openai-codex/gpt-5.4` | Mauvais provider, auth incohérente, ou facturation API non prévue sur un agent | Utiliser `openai-codex/` pour les modèles agent OAuth, `openai/` pour les appels API directs |
| `dist/` stale | `Unknown model` ou `missing` dans models list | `pnpm build && openclaw gateway restart` |
| Pas de cle Whisper | Transcription audio echoue | Ajouter `openai:<client>` dans auth-profiles du store agent |
| Session non compactee | Rate limit TPM (contexte trop gros) | `/new` ou `/reset` pour demarrer une session fraiche |
| `selfChatMode` manquant | Read receipts sur ses propres messages, prefix manquant | Ajouter `selfChatMode: true` si numero perso |
| `identity.name` manquant | Pas de préfixe `[Nom]` en self-chat, messages agent indistinguables | Ajouter `identity: { name: "Prénom" }` dans l'agent config |
