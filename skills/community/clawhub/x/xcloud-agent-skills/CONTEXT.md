# xCloud Agent Skills

Shared language for this repo: a Claude Code plugin that exposes the xCloud
Public API to Claude as a set of skills. Glossary only — architecture decisions
live in `docs/adr/`.

## Language

### Skill structure

**Domain skill**:
A skill owning one *capability* area of the API. There are exactly five:
`xcloud:servers`, `xcloud:sites`, `xcloud:wordpress`, `xcloud:ssl`,
`xcloud:account`.
_Avoid_: module, package, sub-skill.

**Shared layer**:
The plugin-level `scripts/xcloud.sh` and `reference/` files that every domain
skill references via `${CLAUDE_PLUGIN_ROOT}`. Exists once; never duplicated.
_Avoid_: common, core, base.

**Capability**:
What a user is trying to *do* (renew a cert, scan vulnerabilities) — the axis
skills are organized by. Distinct from **resource**, the API's own organizing
axis (the URL root, `/servers/*` or `/sites/*`). Skills cut across resources.

**Owner**:
The single domain skill responsible for a given sub-resource, decided by
capability. Each skill's description names its owned area and disclaims the rest.

### xCloud domain terms

**Server**:
A managed host (`{uuid}`) that runs sites. Owns databases, PHP versions, cron,
firewall, sudo users.
_Avoid_: box, machine, instance, node.

**Site**:
A hosted application (`{uuid}`) on a server. May be WordPress or other.
_Avoid_: website, app, domain (a site *has* domains).

**Blueprint**:
A predefined WordPress configuration (themes, plugins, post-deploy scripts) used
when creating a site.
_Avoid_: template, preset, recipe.

**Sudo user**:
An OS-level privileged account on a server, distinct from the API token user.
_Avoid_: admin, root user.

**Vulnerability**:
A security finding against a site (typically WordPress plugin/theme CVEs),
surfaced by a scan. Owned by `xcloud:wordpress`.
_Avoid_: CVE, issue, threat.

### Environments

**Live**:
`https://app.xcloud.host` — the default base URL, used at release.
_Avoid_: prod, production host.

**Local**:
`http://xcloud.test` — selected only by setting `XCLOUD_API_BASE_URL`, never
hardcoded in a skill body.
_Avoid_: dev, staging, test server.
