# OpenClaw config — client workspace

## Agent (agents.list)

Ajouter un agent dédié avec workspace séparé.

Points importants :
- sandbox activé (`mode: all`, `scope: agent`)
- `tools.alsoAllow` inclut `message` + `sessions_send`
- deny minimum: `gateway` (+ autres selon politique)
- **Modèle** : `anthropic/claude-opus-4-6` en primaire, `openai-codex/gpt-5.4` en fallback
- Le fallback utilise OAuth Codex (pas de clé API consommée)
- **Important** : `openai/gpt-5.4` (provider `openai`) != `openai-codex/gpt-5.4` (provider `openai-codex`). Le premier consomme une clé API, le second utilise OAuth Codex.
- **Règle absolue** : pour un modèle agent OpenClaw, écrire `openai-codex/gpt-5.4` sauf demande explicite d'Erwan. Réserver `openai/gpt-*` aux appels API directs (Whisper, TTS, image generation, etc.).

### Identity (obligatoire)

Chaque agent **doit** avoir un bloc `identity` dans sa config. Au minimum :

```json
"identity": {
  "name": "<Prénom de l'agent>"
}
```

Champs disponibles :
- `name` — nom affiché. Utilisé pour le préfixe self-chat `[Nom]` et les templates `{identity.name}`
- `emoji` — emoji de l'agent (fallback pour ackReaction si pas configuré ailleurs)
- `avatar` — image : path workspace-relatif, URL http(s), ou data URI
- `theme` — thème visuel (optionnel)

**Flow en deux temps :**
1. Au setup initial, laisser `identity` vide ou avec un nom générique (ex: l'id agent)
2. Une fois que l'agent a choisi son nom (via BOOTSTRAP.md / premier contact), mettre à jour `identity.name` avec le prénom choisi

**Pourquoi c'est important :** Sans `identity.name`, le préfixe `[Nom]` n'apparaît pas en self-chat (WhatsApp personal-number). L'utilisateur ne peut pas distinguer ses messages de ceux de l'agent.

Exemple bloc model dans l'agent :
```json
"model": {
  "primary": "anthropic/claude-opus-4-6",
  "fallbacks": ["openai-codex/gpt-5.4"]
}
```

## WhatsApp account

Créer un compte dédié dans `channels.whatsapp.accounts` :

```json
"<client>": {
  "name": "<Nom Client>",
  "enabled": true,
  "dmPolicy": "allowlist",
  "selfChatMode": true,
  "allowFrom": ["+<numero-client>"],
  "allowSendTo": ["*"],
  "groupPolicy": "allowlist",
  "debounceMs": 0
}
```

Notes :
- `selfChatMode: true` : obligatoire si le client utilise son propre numéro perso (pattern "personal-number fallback"). Active les protections self-chat (skip read receipts, pas d'auto-trigger mention, prefix auto dans les réponses).
- `allowFrom` : mettre uniquement le numéro du client.
- `allowSendTo` (optionnel) : autorise l'agent à envoyer à des numéros spécifiques ou `["*"]` pour tous. **Attention : cette fonctionnalité vient de la branche beta (patch Erwan).** Elle n'est pas forcément disponible sur toutes les installations. Toujours vérifier avec Erwan si `allowSendTo` est supporté sur l'instance avant de le configurer. Si absent, ne pas l'inclure dans la config (le comportement par défaut du gateway s'applique).

## Auth profiles (par agent)

Chaque agent a son propre store de credentials dans `~/.openclaw/agents/<client>/agent/auth-profiles.json`.

### Profils hérités automatiquement
- `anthropic:openclaw` : token Anthropic (partagé, mode token)
- `openai-codex:default` : OAuth Codex (partagé, pas de clé API)

### Clé OpenAI dédiée (Whisper / transcription audio)

Chaque agent client **doit** avoir sa propre clé OpenAI pour la transcription audio (Whisper). Ne pas partager la clé env globale `OPENAI_API_KEY`.

Ajouter dans le store de l'agent :
```bash
python3 << 'PYEOF'
import json

path = "/home/ubuntu/.openclaw/agents/<client>/agent/auth-profiles.json"
with open(path, "r") as f:
    data = json.load(f)

data["profiles"]["openai:<client>"] = {
    "provider": "openai",
    "type": "api_key",
    "key": "<CLE_OPENAI_DEDIEE>"
}

with open(path, "w") as f:
    json.dump(data, f, indent=2)
PYEOF
```

Ce profil `openai:<client>` sera utilisé pour tout appel au provider `openai` par cet agent (Whisper, TTS, etc.). Le système d'auth profiles est unifié : `resolveApiKeyForProvider("openai")` cherche dans le store de l'agent d'abord, puis fallback sur `OPENAI_API_KEY` env.

### Piège providers OpenAI

| Provider | Auth | Usage |
|---|---|---|
| `openai` | Clé API (`OPENAI_API_KEY` ou profil `openai:*`) | Whisper, TTS, modèles `openai/gpt-*` |
| `openai-codex` | OAuth (token refresh automatique) | Modèles `openai-codex/gpt-*` (pas de crédit API) |

`normalizeProviderIdForAuth()` ne fusionne PAS ces deux providers. Un profil `openai-codex:default` ne sera jamais utilisé pour un appel provider `openai`.

## Routing binding

Ajouter un binding explicite agent/channel/account/peer.

```json
{
  "agentId": "<client>",
  "match": {
    "channel": "whatsapp",
    "accountId": "<client>",
    "peer": { "kind": "direct", "id": "+<numero-client>" }
  }
}
```

Note : si le selfChat fonctionne sans binding explicite (via le compte WhatsApp + allowFrom), le binding est optionnel mais recommandé pour la clarté.

## WhatsApp pairing (login)

**Obligatoire après la config.** Le compte WhatsApp dans `openclaw.json` et le binding ne suffisent pas — il faut aussi lier le téléphone physique à l'instance browser du gateway.

```bash
openclaw channels login --channel whatsapp --account <client>
```

Ou via le script dev local :
```bash
./openclaw.mjs channels login --channel whatsapp --account <client>
```

Le QR code s'affiche en terminal. Scanner avec WhatsApp > Appareils liés > Lier un appareil.

**Ordre des opérations (les 3 sont nécessaires) :**

1. Compte WhatsApp dans `channels.whatsapp.accounts.<client>` (config)
2. Binding dans `bindings[]` (routing agent ↔ channel)
3. `channels login --channel whatsapp --account <client>` (pairing session)

Sans le login, le status affiche le compte mais il ne sera jamais `linked`/`connected`. Sans le compte config, le login sauvegarde les credentials mais le gateway ignore les messages entrants.

**Après le login :** restart gateway (`openclaw gateway restart` ou kill+relaunch) puis vérifier :

```bash
openclaw channels status --probe
```

Le compte doit afficher : `enabled, configured, linked, running, connected`.

## Communication inter-agents — 4 couches

1. **Agent-level** `tools.alsoAllow` : `sessions_send`, `sessions_list`, `sessions_history`, `message`
2. **Sandbox tools policy** : autoriser ces outils côté sandbox
3. **sessionToolsVisibility** : `"all"` dans le bloc sandbox
4. **Global** (`openclaw.json` racine) :

```json
"tools": {
  "sessions": { "visibility": "all" },
  "agentToAgent": { "enabled": true, "allow": ["david", "kelly", "<client>"] }
}
```

Ne pas oublier d'ajouter le nouvel agent dans la liste `allow`.

## Socat bridges (communication sandbox -> services host)

Le container sandbox de l'agent doit pouvoir joindre les services host. Bridges actifs sur le réseau `bridge` (172.17.0.1) :

| Service | Port | Bridge systemd |
|---------|------|----------------|
| Gateway OpenClaw | 18789 | `socat-bridge-gateway-18789` |
| Windmill | 8000 | `socat-bridge-windmill-8000` |
| **Nango (OAuth2)** | **3003** | **`socat-bridge-nango-3003`** |

Si le sandbox utilise un autre réseau Docker, créer un socat dédié (voir skill `localhost-bridge`).

### Env vars sandbox — 3 niveaux (IMPORTANT)

Il y a 3 niveaux d'env vars. Comprendre la distinction évite les erreurs :

| Niveau | Chemin config | Portée | Transmis au sandbox Docker ? |
|--------|--------------|--------|-------------------------------|
| Global host | `env.vars` | Process gateway uniquement | ❌ NON |
| Defaults sandbox | `agents.defaults.sandbox.docker.env` | Tous les agents sandbox | ✅ OUI (hérité) |
| Per-agent sandbox | `agents.list[].sandbox.docker.env` | Un agent spécifique | ✅ OUI (override defaults) |

**Clés partagées** (dans `agents.defaults.sandbox.docker.env`) :
- `TAVILY_API_KEY` — même clé pour tous
- `JINA_API_KEY` — même clé pour tous
- `NANGO_PROD_SECRET_KEY` — même clé pour tous

**Clés per-agent** (dans `agents.list[].sandbox.docker.env`) :
- `OPENAI_API_KEY` — **TOUJOURS per-agent** (chaque agent a sa propre project key OpenAI, dans `agents/<id>/agent/auth-profiles.json` profil `openai:<id>`). Ne jamais mettre dans defaults.
- Clés spécifiques client (Synology, DataForSEO, etc.)

**Pourquoi OPENAI_API_KEY est per-agent :**
- Le LLM provider utilise `auth-profiles.json` (clé per-agent automatique)
- MAIS les appels directs API depuis le sandbox (Whisper, image-gen via skills) utilisent `$OPENAI_API_KEY` du container
- Si on met la clé globale, la conso Whisper/images de tous les agents est facturée sur le même projet OpenAI

**Pour un nouveau client :** créer une project API key dédiée sur platform.openai.com, la stocker dans `auth-profiles.json` ET dans `sandbox.docker.env.OPENAI_API_KEY`.

### Nango OAuth2 — config agent client

Pour que l'agent client puisse générer des liens OAuth :
1. `NANGO_PROD_SECRET_KEY` est déjà dans les defaults (hérité automatiquement)
2. Copier le skill `nango-oauth` dans le workspace client : `skills/nango-oauth/`
3. L'agent appelle `http://172.17.0.1:3003` (pas localhost) pour l'API Nango

Vérification :
```bash
# Container sandbox de l'agent
docker ps --filter "name=<client>" --format "{{.Names}} {{.Networks}}"

# Socat services actifs
systemctl list-units --type=service | grep socat
```

## Build local

Le gateway tourne depuis `dist/index.js` (build local), pas le npm global. Après tout changement de code source :

```bash
pnpm build
openclaw gateway restart
```

Si un modèle n'est pas reconnu (ex: `openai-codex/gpt-5.4 missing`), c'est probablement que le `dist/` est stale. Rebuild.

## Validation / restart

```bash
node -e "JSON.parse(require('fs').readFileSync('/home/ubuntu/.openclaw/openclaw.json','utf8')); console.log('OK')"
openclaw gateway restart
```

## Checklist post-setup

1. [ ] Agent dans `agents.list` avec modèle Opus + fallback Codex
2. [ ] `identity.name` configuré (ou prévu post-bootstrap)
3. [ ] Compte WhatsApp avec `selfChatMode`, `allowFrom`, `allowSendTo`
4. [ ] Binding WhatsApp dans `bindings[]`
5. [ ] WhatsApp login/pairing (`openclaw channels login --channel whatsapp --account <client>`)
6. [ ] Clé OpenAI dédiée dans auth-profiles (Whisper)
7. [ ] `agentToAgent.allow` mis à jour avec le nouvel agent
8. [ ] Socat bridges vérifiés (gateway 18789, Windmill 8000, Nango 3003)
9. [ ] `NANGO_PROD_SECRET_KEY` dans les env vars sandbox
10. [ ] Skill `nango-oauth` copié dans le workspace
11. [ ] `pnpm build` si changements de code
12. [ ] `openclaw gateway restart`
13. [ ] Test message WhatsApp selfChat ou depuis le numéro client
14. [ ] Vérifier transcription audio (envoyer un vocal)

## Pinning sandbox (stabilité client)

> **Statut : approche théorique à valider en conditions réelles sur notre infra avant usage client massif.**

Pour figer le runtime client malgré les changements serveur/dev :

- pinner `sandbox.docker.image` (global ou par agent), idéalement avec digest (`@sha256:...`)
- éviter les tags mouvants seuls en production (`bookworm-slim` sans digest)

Exemple :

```json
"sandbox": {
  "docker": {
    "image": "openclaw-sandbox:bookworm-slim@sha256:<digest>"
  }
}
```

Après changement d'image :

```bash
openclaw sandbox recreate --agent <client>
```

Validation minimale avant généralisation :
1. Tester sur un agent de test (pas client réel)
2. Vérifier `openclaw sandbox list` (image effectivement utilisée)
3. Vérifier exécution skills/outils critiques (message, sessions_send, etc.)
4. Observer 24h avant déploiement sur clients

## Multi-instance (dev/prod)

Si besoin de séparer dev/prod sur même serveur :
- `openclaw --profile main ...`
- `openclaw --profile dev ...`
- ports et state dirs distincts.

Principe : prod client figée (pin), dev libre sur profil séparé.
