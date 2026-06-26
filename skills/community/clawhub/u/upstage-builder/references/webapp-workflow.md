# Webapp Project & Deployment Workflow

Use this reference when the user wants a full web service/app, not just a code snippet.

## Startup Questions

Before creating a new webapp project, confirm these setup choices once if they are not already known:

1. Which deployment system should be used?
   - Preferred default: `vercel`
2. Which project root should be used?
   - Preferred default: `/data/.openclaw/workspace/projects`
3. Which visibility mode should be used?
   - Preferred default: `password-protected`
   - Other possible answers: `private-team-only`, `public`, `code-only`

If the user has already given defaults, use them without asking every time.

## Recommended Defaults

- Project root: `/data/.openclaw/workspace/projects`
- Deployment provider: `vercel`
- Visibility: `password-protected`
- Vercel access model: publicly reachable deployment URL + app-level password gate (do not rely on Vercel login wall by default)
- Web stack: `Next.js + TypeScript`

## Project Layout

Create one folder per app:

- `/data/.openclaw/workspace/projects/<project-slug>/`

Include at minimum:

- `README.md` — what the app does and how to run it
- `.env.example` — required environment variables
- `DEPLOY.md` — deployment notes and target URL pattern

## Delivery Contract

When finishing a webapp task, return all of these if available:

- project path
- stack/framework used
- required environment variables
- deployment method
- visibility mode
- deployment URL or next deployment step
- site password, if password-protected deployment was requested

## Vercel Default

When the deployment provider is `vercel`:

- prefer a Next.js app
- make the app buildable without localhost access
- treat an external preview or production URL as part of the deliverable
- default to password-protected deployments unless the user says otherwise
- if deployment cannot be completed from the current environment, leave a ready-to-deploy project and say exactly what command or UI step remains
