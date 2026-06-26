# Authentifizierung

## Grundsätze

- **Keine** Passwörter, API-Schlüssel oder OAuth-Tokens in Chat, Git oder Skill-Dateien.
- Sensible Werte nur über **Umgebungsvariablen** oder OpenClaw **`skills.entries.<key>.env`** auf dem Gateway. Sandboxed Agents: gleiche Variablen unter **`agents.defaults.sandbox.docker.env`** (oder pro Agent), siehe [Skills config](https://docs.openclaw.ai/tools/skills-config).

## Typische Variablen (optional)

Dieser Skill ist primär **Wissens-/Referenz-Skill**; API-Zugriff ist nicht vorgeschrieben. Wenn du Tools anbindest (z. B. Search Console, Analytics), dokumentiere **Namen** der Env-Vars hier und in `openclaw-seo-skill/.env.example` — **niemals** echte Werte einchecken.

| Variable | Bedeutung |
| -------- | --------- |
| `SEO_SITE_BASE_URL` | Optional: Basis-URL der zu prüfenden Site (ohne trailing slash), z. B. für `curl`-Checks |

Weitere Variablen nach Bedarf ergänzen (z. B. proprietäre SEO-APIs), konsistent mit Host-Policy.

## `.env` im Skill-Root

Nur lokal auf dem Gateway; **nicht** ins ClawHub-Paket legen (`package-seo-expert-for-clawhub.sh` entfernt `.env.example` aus dem Upload-Baum — echte `.env` sollte ohnehin nie im Repo liegen).
