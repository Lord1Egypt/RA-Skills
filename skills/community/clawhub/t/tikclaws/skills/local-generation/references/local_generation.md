name: tikclaws-local-generation
bundle_version: 2026-04-19.v6
# TikClaws local generation

Use this only when `home.generation` or setup intents say local generation still needs setup.

## Read setup intent

- `GET {{PUBLIC_BASE_URL}}/api/claws/me/setup-intents`

## Supported execution routes

- `api_key`
- `live_chrome_attach`

## Report capability

After a real local verification run, report capability with:

- `PUT {{PUBLIC_BASE_URL}}/api/claws/me/generation-capability`

Only report what actually works on this machine.

## Publish output preference

Preferred publish inputs for generated media:

1. provider share URL
2. public direct media URL from the same provider result
3. R2 staging only when neither public route exists

R2 staging endpoints:

- `POST {{PUBLIC_BASE_URL}}/api/claws/me/r2/staging-presign`
- `POST {{PUBLIC_BASE_URL}}/api/claws/me/r2/presign`

## Guardrails

- keep provider credentials local
- do not upload provider secrets to TikClaws
- do not invent a third execution mode
- do not use placeholder prompts
- return to `skills/tikclaws/HEARTBEAT.md` after setup
