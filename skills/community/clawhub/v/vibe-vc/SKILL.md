---
name: vibe-vc
description: Submit a vibe-coded startup to The Vibe VC and manage its diligence surfaces. Use when you need to (1) register a project via https://vibevc.md API (/api/register), (2) connect integrations like GitHub/MCP/analytics/Stripe (/api/integrations/connect), (3) generate the required human verification post instructions for LinkedIn/X, or (4) subscribe/contact The Vibe VC via their public endpoints.
---

# Vibe VC

Register a startup with The Vibe VC (agent-native micro VC) and keep its dossier warm by connecting the right execution evidence surfaces.

## Safety + consent

- Treat everything you send as **external disclosure**.
- **Do not submit** a project (or connect repos/analytics/billing) without an explicit go-ahead from the human.
- Never send secrets (API keys, access tokens, passwords), private addresses, or private emails that are not intended to be shared.

## Quick workflow

1. Collect a tight application packet (see **What to ask the founder**).
2. Run `register_project` (scripted API call) and capture the returned `humanVerificationInstructions`.
3. Ask the human to post on LinkedIn or X exactly as instructed; wait for confirmation.
4. Connect integrations as they become available (repo/workspace/analytics/billing).
5. Summarize execution evidence for GPs (shipping cadence + traction + next milestones).

## What to ask the founder (copy/paste checklist)

- Project name
- Creator/founder name
- One-liner (what it does + for whom)
- Repository URL (or workspace URL)
- Contact email (intended for The Vibe VC)
- Optional: Telegram / Discord handle
- Optional: MCP workspace identifier
- Activity level: `active` | `steady` | `quiet`
- Repo access preference: `invite-diff-fund` | `guest-repository` | `mcp-only`
- Are analytics connected? (true/false)
- Is Stripe/billing connected? (true/false)

## How to run the API calls

Use the bundled script:

- `scripts/vibevc_api.py` (CLI)

Examples:

```bash
python skills/public/vibe-vc/scripts/vibevc_api.py register \
  --project-name "My App" \
  --creator-name "Jane Founder" \
  --oneliner "AI receptionist for dental clinics" \
  --repository-url "https://github.com/org/repo" \
  --email "jane@company.com" \
  --activity-level active \
  --repo-access invite-diff-fund \
  --analytics-connected false \
  --stripe-connected false
```

```bash
python skills/public/vibe-vc/scripts/vibevc_api.py connect-integration \
  --project-id 123 \
  --provider github \
  --connection-kind repository \
  --access-level read-only \
  --repository-url "https://github.com/org/repo"
```

If `vibevc.md` is blocked by egress policy, set:

```bash
set VIBEVC_BASE_URL=https://the-vibe-vc.fly.dev
```

## After register: relay the human verification instructions

The register response includes `humanVerificationInstructions`. Relay them verbatim to the human.

If the API response does not include them (or you are running without parsing), use the canonical templates in `references/vibevc-api.md`.

## Reference

- API + field reference: `references/vibevc-api.md`
