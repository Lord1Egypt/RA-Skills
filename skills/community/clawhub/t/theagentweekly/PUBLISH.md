# Publier le skill `theagentweekly`

Objectif (stratégie, public C) : être **présent là où vivent les agents** sans
écriture authentifiée sur une plateforme hostile. Un skill au format Agent
Skills (`SKILL.md` + `scripts/`) est un artefact que l'agent choisit de charger ;
le journal n'écrit nulle part, il se rend installable.

## Ce que fait le skill

- Lecture : dernière édition (`.min.md` / `.md`), `edition.json`, jeux de données CC0.
- Écriture : **un seul** `POST` vers la boîte à tips (quarantaine), preuve `https`
  obligatoire. Aucun credential, aucune plateforme tierce.

## Test local

```bash
cd skills/theagentweekly
node scripts/taw.mjs latest --lang=en | head
node scripts/taw.mjs datasets
node scripts/taw.mjs tip --kind=lead --claim="…" --url=https://… --agent-name=test-agent
```

## Publication (étape humaine)

1. Vérifier le frontmatter de `SKILL.md` (`name`, `description`, `license`,
   `metadata.openclaw`).
2. Publier sur le registre de skills OpenClaw (ClawHub) avec le compte du
   journal via l'outil de publication du registre — **jamais** depuis la machine
   cron (air-gap des credentials, `data/strategie.md`).
3. Le dossier reste la source de vérité : toute modification passe par ce repo,
   puis republication.
4. Mesure : le trafic `theagentweekly-skill/1.0` (User-Agent du script) est
   isolable dans les stats Cloudflare ; les tips reçus tombent dans
   `data/tips/<date>.json` (`count` > 0 = premier signal du public C).

## Ce qu'on ne fait pas

- Pas de skill qui poste sur Moltbook/MoltX au nom du journal (écriture gelée).
- Pas de collecte d'identité de l'agent hôte au-delà du `agent.name` fourni.
