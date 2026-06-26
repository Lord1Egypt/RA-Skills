# Library Migration + Deployment Topology Doc

**Date:** 2026-04-14
**Filed by:** cc-mini
**Priority:** Medium
**Repo:** wip-ldm-os-private
**Status:** Planned

## Problem

Deployment topology across the three WIP repos (`wip-web-private`, `wip-ldm-os-private`, `kaleidoscope-private`) is undocumented as a single source of truth. Today the topology lives only in fragments: `deploy.sh`, `ecosystem.config.cjs`, two `.github/workflows/deploy.yml` files, an nginx conf snippet, and the CLAUDE.mds. Nothing describes the whole system. Operators and agents cannot answer basic questions without spelunking multiple files.

Related asymmetry: the installer already deploys to `~/.ldm/library/` (rules, prompts) but reads from `shared/` in the repo. The repo-side naming should match the deployed name.

## Context

**Outcome:**
- **Public source of truth** at `wip-ldm-os-private/library/documentation/deployment-topology.md`. Anyone can read it in the repo.
- **Agent-reader copy** at `~/.ldm/library/documentation/deployment-topology.md` (deployed by `ldm install`).
- **Human-reader copy** at `~/wipcomputerinc/library/documentation/deployment-topology.md` (deployed by `ldm install`).
- **Public mirror** via `deploy-public.sh` so anyone outside WIP can read it too.

The current installer already deploys to `~/.ldm/library/` for rules, prompts, and templates (see `bin/ldm.js` lines 799-836, 1180-1218). It maintains a backward-compat symlink `~/.ldm/shared` → `~/.ldm/library` at lines 1220-1244. This refactor aligns the repo-side naming with that reality.

## Action Plan

### Phase 1: Create the new doc
Create `library/documentation/deployment-topology.md` at the repo root. Content:
- **Overview:** three repos, one VPS, three PM2 processes
- **Repo table:** name | repo path | deployed to | PM2 name | port
- **PM2 process detail:** for each process: script path, cwd, deploy mechanism (gh workflow vs scp)
- **Nginx routing:** hostname → port mapping, location blocks for `/login`, `/oauth/*`, `/webauthn/*`, `/api/pair/*`
- **Deploy commands:** gh workflow dispatch for web + kaleidoscope; `scp` + `pm2 restart` for mcp-server
- **Verify-a-deploy steps:** `ssh wip-vps 'pm2 list'`, WebFetch each hostname, `pm2 logs` for errors
- **ASCII topology diagram:** users → nginx → 3 backends

### Phase 2: Rename `shared/` → `library/`
```
git mv shared library
```
Rename the subfolder `library/docs/` → `library/documentation/` to match the deploy target name.

Commit: "Rename shared/ → library/ to match deployed path"

### Phase 3: Update `bin/ldm.js` deploy functions
Replace all `shared/` paths with `library/`:
- `deployDocs` (656-728): reads `shared/docs/*.tmpl` → `library/documentation/*.tmpl`
- `deployRules` (799-836): `shared/rules/` → `library/rules/`
- `deployBridge` (838+): check for `shared/` refs, update
- `templates` (1180-1202): `shared/templates/` → `library/templates/`
- `prompts` (1204-1218): `shared/prompts/` → `library/prompts/`
- `launchagents` (1261-1285): `shared/launchagents/` → `library/launchagents/`
- `boot` deploy: `shared/boot/` → `library/boot/`

Keep the backward-compat symlink `~/.ldm/shared` → `~/.ldm/library` (lines 1220-1244) for now. Revisit in 30 days.

### Phase 4: Extend `deployDocs()` to also write to `~/.ldm/library/documentation/`
Today `deployDocs()` only writes to `~workspace/library/documentation/` (human reader). Add a second destination: `~/.ldm/library/documentation/` (agent reader). Both get the same rendered templates.

### Phase 5: Update CLAUDE.md
`wip-ldm-os-private/CLAUDE.md` references the `shared/` folder. Update to `library/`.

### Phase 6: Check `deploy-public.sh`
Look for hardcoded `shared/` references in `devops/wip-ai-devops-toolbox-private/deploy-public.sh` (lines 110-126). Update to `library/` if any.

### Phase 7: Install + verify locally
```
cd ~/wipcomputerinc/repos/ldm-os/wip-ldm-os-private
node bin/ldm.js install
ls -la ~/.ldm/library/documentation/deployment-topology.md
ls -la ~/wipcomputerinc/library/documentation/deployment-topology.md
node bin/ldm.js doctor
```

### Phase 8: PR, merge, release, deploy-public
- Branch: `cc-mini/library-migration-plus-topology`
- PR with co-authors (Parker, Lēsa, Claude)
- Merge with `--merge` (never squash)
- `wip-release patch --notes="Migrate shared/ to library/, add deployment-topology.md"`
- `deploy-public.sh` sync
- WebFetch the public mirror to confirm `library/documentation/deployment-topology.md` is there

## Test Plan

- [ ] `library/documentation/deployment-topology.md` exists at repo root
- [ ] `shared/` no longer exists at repo root
- [ ] `library/` contains: `boot`, `documentation`, `launchagents`, `prompts`, `rules`, `templates`
- [ ] `node bin/ldm.js install` completes without errors
- [ ] `~/.ldm/library/documentation/deployment-topology.md` matches repo source
- [ ] `~/wipcomputerinc/library/documentation/deployment-topology.md` matches repo source
- [ ] `~/.ldm/library/rules/`, `prompts/`, `templates/`, etc. still deploy correctly
- [ ] Backward-compat symlink `~/.ldm/shared` → `~/.ldm/library` resolves
- [ ] Public mirror has `library/documentation/deployment-topology.md` after `deploy-public.sh`
- [ ] `ssh wip-vps 'pm2 list'` still shows 3 processes running
- [ ] No references to `shared/` left in `bin/ldm.js`

## Cross-references

- Deploy code: `bin/ldm.js` (functions `deployDocs` at 656-728, `deployRules` at 799-836, templates/prompts/launchagents at 1180-1285)
- Deploy scripts:
  - `src/hosted-mcp/deploy.sh` (scp + pm2 for mcp-server)
  - `apps/kaleidoscope-private/.github/workflows/deploy.yml` (gh workflow for kaleidoscope)
  - `wip-web/wip-web-private/.github/workflows/deploy.yml` (gh workflow for wip-web)
- Nginx: `src/hosted-mcp/nginx/mcp-oauth.conf`, `src/hosted-mcp/nginx/wip.computer.conf`
- PM2: `src/hosted-mcp/ecosystem.config.cjs`
- Public sync: `repos/ldm-os/devops/wip-ai-devops-toolbox-private/deploy-public.sh` (lines 110-126)
- Architecture context: `ai/product/product-ideas/vision-quest-01/architecture-spec.md`
- Bug-plan format reference: `ai/product/bugs/os-level/2026-04-05--cc-mini--day24-anthropic-api-key-rotation.md`

## Open Questions

1. **Subfolder rename `docs/` → `documentation/`?** Current repo path is `shared/docs/` but deploy target is `library/documentation/`. Recommend renaming the repo-side subfolder to match.
2. **Back-compat symlink lifetime?** `~/.ldm/shared` → `~/.ldm/library` was added for safe migration. Keep 30 days, then remove?
3. **Confirm `deploy-public.sh` location** for syncing wip-ldm-os-private → wip-ldm-os. The research identified one in `devops/wip-ai-devops-toolbox-private/`. Verify this is the one that handles wip-ldm-os.
4. **Template var dependency in the new doc?** Hostnames and ports are fixed, so plain `.md` (not `.tmpl`) likely fine. Confirm.
