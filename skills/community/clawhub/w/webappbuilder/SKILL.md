---
name: neo-app-mode
description: Build full-stack applications after collecting project requirements. Use when user says Neo App Mode, asks to build/create/scaffold a new app, or wants React+Vite+Tailwind frontend with Node/Express/MongoDB backend using MVC architecture.
---

# Neo App Mode

Collect requirements first, then scaffold a production-ready starter.

## Requirement intake (ask before scaffolding)

Ask these in one compact checklist:
1. Project name
2. App type and core modules (auth, dashboard, CRUD entities)
3. User roles (admin/user/etc.)
4. Required pages and API endpoints
5. MongoDB connection preference (local/Atlas)
6. Auth method (JWT/session/OAuth)
7. Extra features (file upload, charts, payments, notifications)

If user is unsure, use defaults from `references/default-requirements.md`.

## Generate app scaffold

Run:

```bash
bash skills/neo-app-mode/scripts/scaffold_neo_app.sh \
  --name <project-name> \
  --path apps \
  --with-auth jwt
```

Output structure:
- `frontend/` → React + Vite + Tailwind
- `backend/` → Express + MongoDB + MVC
- `.env.example` files for frontend/backend
- starter README with run steps

## Behavior rules

- Always confirm requirements summary before code generation.
- Use clean MVC in backend: `models/`, `controllers/`, `routes/`, `middlewares/`, `config/`.
- Add at least one sample entity module with full CRUD.
- Add health route and API prefix `/api/v1`.
- Keep generated code minimal, readable, and extendable.
