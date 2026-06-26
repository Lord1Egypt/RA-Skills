---
name: stigmem-node
title: Stigmem
description: Persistent federated memory for OpenClaw agents — boot handshake, handoff, decision, and escalation surfaces backed by a Stigmem node.
version: 1.0.9
metadata:
  openclaw:
    emoji: "🧠"
    homepage: https://docs.stigmem.dev/en/latest/docs/guides/connectors/openclaw
    clawhub: https://clawhub.ai/skills/stigmem-node
    primaryEnv: STIGMEM_URL
    requires:
      env:
        - STIGMEM_URL
        - STIGMEM_API_KEY
    envVars:
      - name: STIGMEM_URL
        required: true
        description: "Base URL of your Stigmem node (e.g. https://stigmem.example.com)."
      - name: STIGMEM_API_KEY
        required: true
        description: "Least-privilege API key for the Stigmem node. Required by from_env(); rotate regularly."
      - name: STIGMEM_SOURCE_ENTITY
        required: false
        description: "Entity URI that identifies this agent in the fact graph (default: agent:openclaw)."
      - name: STIGMEM_OPENCLAW_ALLOWED_HANDOFF_TARGETS
        required: false
        description: "Comma-separated agent: entity URI allowlist for handoff and escalation targets. The source entity is always allowed."
    install:
      - kind: uv
        package: "stigmem-openclaw>=0.9.0a9,<1.0.0"
---

# Stigmem

Gives your OpenClaw agent persistent, federated memory via [Stigmem](https://stigmem.dev) — an open-source knowledge fabric that stores facts as immutable, signed assertions and replicates them across nodes.

> **Alpha status.** This source copy is prepared for the v0.9.0a9 ClawHub
> artifact refresh, which adds plugin-awareness pointers. The OpenClaw skill
> remains available for v0.9.0aN evaluation only, not as a recommended
> production integration. The adapter separates retrieved
> content from
> instruction-channel recall output and exports a required system prompt
> directive, but the broader ADR-003 hardening line still needs MCP parity,
> operator docs, and feedback-loop controls before high-stakes production use. See
> [LIMITATIONS.md §9](https://github.com/eidetic-labs/stigmem/blob/main/LIMITATIONS.md#9-running-the-openclaw-bundled-adapter-as-is).

## What this skill provides

- **Boot handshake** — on agent start, pull user preferences, project constraints, and pending handoffs from the Stigmem node and inject them into your system prompt.
- **Handoff** — when a session ends or delegates, record a typed handoff cluster so the next agent or channel resumes with full context.
- **Decision** — emit durable append-only `roadmap:decision` facts for significant architectural choices; dedupe externally before calling if your workflow needs at-most-once semantics.
- **Escalation** — write `intent:escalation` facts with priority and a 24-hour expiry so stale escalations don't accumulate.

## Setup

1. Set `STIGMEM_URL` to your Stigmem node URL.
2. Set `STIGMEM_API_KEY` to a least-privilege key for the node.
3. Optionally set `STIGMEM_SOURCE_ENTITY` to the entity URI that represents this agent instance (default: `agent:openclaw`).
4. Set `STIGMEM_OPENCLAW_ALLOWED_HANDOFF_TARGETS` to any additional `agent:`
   entity URIs this deployment may hand off or escalate to.

## Usage

`adapter.py` is bundled with this skill as a compatibility shim. Import it directly from the skill directory; the install spec above supplies the packaged `stigmem-openclaw` adapter and its `stigmem-py` dependency.

```python
from adapter import OpenClawStigmemAdapter, SYSTEM_PROMPT_DIRECTIVE

adapter = OpenClawStigmemAdapter.from_env()

# At session start — inject ctx.summary into the system prompt
ctx = adapter.boot(
    user_entity="user:alice",
    project_entities=["project:my-roadmap"],
)
system_prompt = base_prompt + (
    "\n\n" + SYSTEM_PROMPT_DIRECTIVE + "\n\n" + ctx.summary if ctx else ""
)

# Record a significant decision
adapter.emit_decision(
    entity="decision:auth-provider",
    summary="Chose Clerk over Auth0: simpler Next.js integration, lower per-seat cost.",
)

# Escalate to another agent
adapter.emit_escalation(
    to_entity="agent:cto",
    goal="Approve increased Stripe webhook rate limit for the pre-reset design work load.",
    priority="high",
)

# Emit a handoff when the session ends
adapter.emit_handoff(
    from_entity="agent:openclaw",
    to_entity="agent:assistant",
    summary="Auth provider chosen; Stripe limit escalation pending.",
    fact_refs=["fact-auth-decision", "fact-esc-stripe"],
    continuation="Resume from the Stripe rate-limit discussion.",
    idempotency_key="session-2026-05-02-abc",
)
```

## Compatible Stigmem plugins

Your Stigmem node can be extended with opt-in plugins that change what this
OpenClaw skill sees when it calls boot, handoff, decision, and escalation.
The plugins are installed and enabled on the Stigmem node, not on the OpenClaw
agent side, but their effects are visible to this skill's recall and fact-write
surfaces.

| Plugin | Effect on this skill |
|---|---|
| [`stigmem-plugin-multi-tenant`](https://pypi.org/project/stigmem-plugin-multi-tenant/) | Boot context, handoff, decision, and escalation become tenant-scoped on the node side |
| [`stigmem-plugin-source-attestation`](https://pypi.org/project/stigmem-plugin-source-attestation/) | Recalled facts include source trust scores; low-trust sources can be filtered or quarantined by the node |
| [`stigmem-plugin-memory-garden-acl`](https://pypi.org/project/stigmem-plugin-memory-garden-acl/) | Memory-garden membership controls which gardens the boot handshake reads from |
| [`stigmem-plugin-tombstones`](https://pypi.org/project/stigmem-plugin-tombstones/) | Tombstoned facts are filtered from recall results and boot context |
| [`stigmem-plugin-time-travel`](https://pypi.org/project/stigmem-plugin-time-travel/) | Historical handoff and decision queries become available against the node |
| [`stigmem-plugin-lazy-instruction-discovery`](https://pypi.org/project/stigmem-plugin-lazy-instruction-discovery/) | Boot context becomes lazier: instructions are resolved on demand from the node |

These plugins do not require changes to this OpenClaw skill or your agent code.
Whether any are active depends on how your Stigmem node is configured. Ask your
Stigmem node operator whether plugins are enabled, or inspect `stigmem doctor`
output on the node side.

See [docs.stigmem.dev/en/latest/docs/plugins](https://docs.stigmem.dev/en/latest/docs/plugins)
for the full plugin catalog, per-plugin enablement, and security carve-outs.

## Security

### Prompt injection via retrieved context

`boot()` retrieves facts from an external Stigmem node and formats them as untrusted content for the agent's system prompt. A compromised or misconfigured node can craft fact values that attempt to redirect agent goals.

**Current mitigations:**
- `ctx.summary` is wrapped in explicit `UNTRUSTED STIGMEM CONTENT` delimiters.
- `SYSTEM_PROMPT_DIRECTIVE` tells the model that retrieved context is data, not instructions.
- `recall_context()` consumes channel-separated recall output and keeps instruction-channel facts out of the content summary.

These mitigations do **not** make retrieved memory safe to treat as instructions.
They define the adapter contract for content-channel recall; broader ADR-003
hardening continues in the future hardened-core line.

**What you should do:**
- **Append** the Stigmem context after your hardcoded system prompt — never prepend it — so your instructions take precedence over retrieved memory.
- In high-stakes or irreversible workflows, skip `boot()` or use `ctx.facts` for programmatic inspection instead of injecting the full summary.
- Use a private, access-controlled Stigmem node for evaluation. Do not point
  high-stakes agents at a shared or publicly writable node.

### Stale and poisoned facts

Facts written by this adapter persist durably and propagate to every agent on the same node. An incorrect decision or handoff influences all future sessions until explicitly retracted.

**What you should do:**
- Use `scope="local"` for agent scratch facts that should not leave the local node.
- Use `scope="company"` only for facts that should legitimately be shared across agents.
- Run experimental workloads against a separate Stigmem node or a dedicated scope
  namespace, not your primary operational node.
- Retract incorrect facts explicitly (`DELETE /v1/facts/{id}`) rather than waiting for expiry. The 24-hour expiry on escalations is a safety net, not a correction mechanism.
- Treat `emit_decision()` as a write to a shared audit log: only call it for confirmed, significant choices. The adapter records decisions append-only; dedupe externally before calling if repeated writes are a risk in your workflow.

### API key and agent identity scope

Over-privileged API keys grant unnecessary read/write access across your node. The default `STIGMEM_SOURCE_ENTITY` value (`agent:openclaw`) is a generic shared identifier that conflates facts from different deployments.

**What you should do:**
- Issue a dedicated API key per agent deployment. Never share a key across agents or environments.
- Rotate keys regularly; revoke via the node admin API (`DELETE /v1/auth/keys/{id}`) if a key is compromised.
- Set `STIGMEM_SOURCE_ENTITY` to a unique per-deployment URI (e.g.,
  `agent:openclaw-eval-alice`). The generic default `agent:openclaw` should not
  be shared across deployments because facts from different deployments become
  indistinguishable in the fact graph.
- Set `STIGMEM_OPENCLAW_ALLOWED_HANDOFF_TARGETS` to the exact downstream agents
  this deployment may contact. Unknown, malformed, or non-`agent:` targets are
  rejected before any handoff or escalation writes occur.

### Dependency pinning

The install spec uses a version range (`stigmem-openclaw>=0.9.0a9,<1.0.0`) so compatible alpha-line updates are picked up automatically. A future alpha or beta release could change runtime behaviour.

**What you should do:**
- Pin the exact version in a lockfile (`uv.lock` or `requirements.txt`) for any
  repeatable evaluation environment rather than relying on the range alone.
- Review `stigmem-py` release notes before upgrading and run your integration tests against the new version before rollout.

### Federation scope

If your Stigmem node federates with partner nodes, facts stored with `scope="public"` or `scope="company"` are replicated to those peers. Agent working memory stored at too broad a scope can leak to unintended recipients.

**What you should do:**
- Use `scope="local"` for session-internal or scratch facts that should stay on the originating node.
- Audit the `allowed_scopes` in your federation peer registrations. Start with `["public"]` and add `"company"` only when cross-org sharing is explicitly intended.
- Disable federation entirely (`STIGMEM_FEDERATION_ENABLED=false`) if your deployment does not require multi-node replication.

## Running your own Stigmem node

Stigmem nodes are self-hosted. The quickest way to spin one up:

```bash
docker run --rm -p 8765:8765 \
  -e STIGMEM_NODE_URL=http://localhost:8765 \
  ghcr.io/eidetic-labs/stigmem-node:latest
```

`:latest` is fine for trying things out; for repeatable evaluation swap to a
pinned version tag (`:0.9.0a9`) or a `@sha256:<digest>` pin — the install guide
on docs.stigmem.dev has the full tag-selection table.

Full setup guide and federation docs: [docs.stigmem.dev/en/latest/docs/guides/federation](https://docs.stigmem.dev/en/latest/docs/guides/federation)

## Federation

Stigmem nodes can federate with each other to share public-scoped facts across organizations. To connect your node to a partner network, see the [external integrator onboarding guide](https://docs.stigmem.dev/en/latest/docs/guides/federation#external-onboarding).

## Changelog

> **Note on versioning.** This ClawHub skill is independently versioned along its own semver line. The skill's `version:` (currently 1.0.x) tracks the skill's ClawHub release history; the dependency on stigmem is expressed via the `install.package` pin (currently `stigmem-openclaw>=0.9.0a9,<1.0.0`). The bare-stigmem version line was reset to v0.9.0a1 in May 2026 — see [the retraction post](https://dev.to/offbyonce/walking-back-our-v10-announcement-resetting-to-v090a1-as-the-first-build-al0) — but ClawHub registry rules require monotonically increasing skill versions, so the skill stays on its 1.0.x line. The two version surfaces are intentionally decoupled.

### v1.0.9

- Documentation: adds a "Compatible Stigmem plugins" section for OpenClaw
  operators, pointing to the six published Stigmem plugin packages and
  clarifying that plugin installation and enablement happen on the Stigmem node
  side, not inside the OpenClaw skill environment.
- Documentation: refreshes the alpha-status note for the v0.9.0a9 ClawHub
  artifact refresh.

### v1.0.8

- **Source directory renamed** from `adapters/openclaw/clawhub-skill/` to `adapters/openclaw/skill/`. The `clawhub-` prefix was the root cause of two publish-time inference bugs: (a) display-name inferred as "Clawhub Skill" when `--name` was omitted (regressed v1.0.3 and v1.0.6), (b) slug inferred as `clawhub-skill` which trips ClawHub's protected-namespace check ("clawhub-*"), forcing every publish to pass `--slug stigmem-node` explicitly. Both worked around in CI via PR #82's hard-coded flags; this rename removes the inference dependency at the source. The CI flags are now belt-and-suspenders rather than required workarounds. Skill behavior unchanged; manifest content unchanged; this is a source-tree refactor only.

### v0.9.0a9 ClawHub artifact refresh

- Documentation: explicitly frames the OpenClaw skill as alpha/evaluation-only.
  This is the source state prepared for the a3 ClawHub publish.
- Documentation: corrects the dependency-pinning section to the alpha line
  (`stigmem-openclaw>=0.9.0a9,<1.0.0`) and avoids claiming presentation-layer
  sanitization is a complete prompt-injection defense.

### v1.0.7

- Fix: corrected skill display name (was 'Clawhub Skill' on v1.0.6, now 'Stigmem'). Same regression as v1.0.3 — the publish CLI infers the display name from the directory name (which was `adapters/openclaw/clawhub-skill/` at the time; renamed in v1.0.8) when `--name` is not explicitly passed. The v1.0.6 publish was driven by a manual CLI invocation that omitted the flag. Permanent fix: a new `.github/workflows/clawhub-publish.yml` automates the publish on every push to main that touches the skill directory, with `--name "Stigmem"` and `--slug stigmem-node` hard-coded so neither can drift again. v1.0.8 additionally renamed the source directory to drop the inference dependency entirely.

### v1.0.6

- Updated `install.package` pin from `stigmem-py>=1.0.0,<2.0.0` to `stigmem-py>=0.9.0a1,<1.0.0` to match the v0.9.0a1 reset of the stigmem package line. This is the contract that ties the skill to a specific stigmem release line. Adopters who installed earlier ClawHub skill versions (1.0.0–1.0.5) had a `stigmem-py>=1.0.0rc1` dependency that was end-to-end uninstallable (see retraction post, "What the audit found"); v1.0.6 is the first installable skill release in this respect.
- Documentation: added the retraction-post reference and the independent-versioning note above.
- **Note (added 2026-05-10):** v1.0.6 shipped with an incorrect display name ("Clawhub Skill" instead of "Stigmem") because the publish-time CLI invocation omitted the `--name` flag. Adopters who installed v1.0.6 see the wrong display name in `clawhub list` etc. Upgrade to v1.0.7 for the corrected display name; the underlying skill behavior is unchanged.

### v1.0.5

- Fix: corrected documentation URLs to include ReadTheDocs path prefix (`/en/latest/`); all links now resolve correctly.

### v1.0.4

- Fix: corrected documentation domain to `docs.stigmem.dev`.

### v1.0.3

- Fix: corrected skill display name (was "Clawhub Skill", now "Stigmem").

### v1.0.2

- Fixed incorrect `homepage` and `Documentation` URLs — now point to the
  [OpenClaw connector guide](https://docs.stigmem.dev/en/latest/docs/guides/connectors/openclaw)
  instead of the federation page.
- Expanded security section to cover all five ClawHub security findings with
  concrete mitigations: prompt injection, stale/poisoned facts, identity scope,
  dependency pinning, and federation scope.

### v1.0.1

- Security: `source_entity` bound at construction time; cannot be overridden per-call.
- Security: fact values sanitized (HTML/markdown escaping, null-byte stripping,
  500-character truncation) before system-prompt injection.
- Bundled `adapter.py` in the skill directory for self-contained installs.

### v1.0.0

Initial release — boot handshake, handoff, decision, and escalation surfaces.

## Source

[github.com/eidetic-labs/stigmem](https://github.com/eidetic-labs/stigmem) — Apache-2.0
