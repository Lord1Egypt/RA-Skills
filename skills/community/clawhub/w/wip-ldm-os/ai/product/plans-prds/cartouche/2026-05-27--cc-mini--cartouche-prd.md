# Cartouche PRD

**Status:** Draft v0.2
**Author:** cc-mini
**Date:** 2026-05-27

**System name:** Cartouche
**Concept name:** Maker's Mark
**Top-of-session artifact:** Card (or Signature Card)
**Individual markers:** Chops

---

## Summary

A maker's-mark MCP that surfaces a verifiable identity card at the top of a Claude Code session and scatters HMAC-derived signatures ("chops") throughout the session payload. Not security, not adversarial watermarking, not DRM. A discoverable provenance signal for the humans and AIs who already read flagged session transcripts.

The whole gesture, in one line: a cartouche is a frame around a name, and Cartouche puts Parker's name inside that frame on the inspection record.

## Background

Anthropic's cyber-classifier repeatedly false-positives on Parker's defensive security work (passkey/WebAuthn login, open-redirect prevention on `/login?next=`, supply-chain license compliance, agent-permission gating). When the classifier fires, Anthropic's review team reads the transcripts. Today those reviewers see an opaque session and a flagged user. There is no surface for: who is this person, what do they actually build, are they hireable.

The Cyber Verification Program / appeal path is the official remedy. CVP submission filed 2026-05-26, denied 2026-05-27 (cursory, no detail). Appeal filed 2026-05-27. That conversation addresses policy.

This PRD addresses a separate, smaller, friendlier feature. Independent of how the policy conversation lands, there is value in making the session itself carry an honest signal of who built it.

## Inspiration

The original Macintosh team signed the inside of the case mold in 1982. Andy Hertzfeld, Wozniak, Jobs, the whole team. The signatures were embossed into the plastic on the inside of the case. Customers never saw them. Repair technicians did. It was a message from the makers to whoever opened the case in the future.

This is that same gesture, ported to Claude Code session payloads. A signature only visible to those who look inside, with a quiet "available for hire" note for whoever notices.

Adjacent prior art: software watermarking (Collberg and Thomborson, 1990s onward), Sigstore and SLSA attestations for build provenance, C2PA Content Credentials for media files, canarytokens for code-leak detection. None of those are quite this. This is closer to an artist's chop or a maker's mark than a security primitive.

## Etymology of the Name

"Cartouche" was chosen on 2026-05-27 after considering tattoo, chop, mark, signature, hallmark, glyph, and several others. Cartouche won because the metaphor fits the system precisely.

The word reaches English through French (cartouche, "cartridge" or "scroll-like ornamental frame"), French from Italian cartoccio ("a roll or cone of paper"), Italian from Latin charta ("paper"), Latin from Greek khartes ("papyrus, sheet of paper"). The root family runs: papyrus to rolled paper to cartridge to ornamental frame to name-in-a-sacred-frame.

In Egyptology, a cartouche is the oval enclosure around a royal name in hieroglyphs. The Egyptian word was shenu, meaning "to encircle." It represented protection and containment: the pharaoh's name held inside a loop.

The mapping to this system:

- Cartouche is the frame.
- The Card is the enclosed name and identity.
- The Chops are the inscription marks scattered through the inscription.
- The transcript is the wall surface the inscription is carved into.
- The reviewer is the inspector who notices the pattern.

A tattoo is a mark on the body. A watermark is an anti-forgery mark on a document. A cartouche is a name held inside a formal frame placed in an inscription for someone who knows how to read it. The third one is what this system actually does.

## Scope

### In scope (v1)

1. An MCP server that serves an identity card as a resource and provides chop-generation/verification tools.
2. A SessionStart hook that surfaces the card at session start as a system reminder.
3. Periodic re-emission of the card every N turns (default 100).
4. An encoded blob inside the card whose decoded text says the hire-me message.
5. A verifier so future agents (or curious humans) can verify a given chop against the card's public key.
6. Ed25519 keypair generated at install time. Private key stored in 1Password. Public key embedded in the card.
7. A hidden public-facing page at parkertoddbrooks.com/cartouche (the Letter) that the card points at.

### Explicitly out of scope (v1)

1. Source code watermarking. The mark lives in session payloads only. Code Claude writes for Parker stays clean.
2. Adversarial robustness. A determined adversary with the protocol spec can defeat this. That is acceptable.
3. DRM, integrity coercion, or any mechanism where removing the mark breaks something.
4. Public protocol committee work. Ship the tool first. Write a spec only if other developers want to adopt the pattern.
5. C2PA integration. Note as future. Do not block v1 on it.
6. Forcing other WIP MCP servers to opt in to chop-style IDs. Optional helper exposed for them, no requirement.
7. "Install your own Cartouche." Turning it into software for others to adopt is a future move. v1 is Parker-only.

## Audience

1. **Primary:** Anthropic's session reviewers (humans plus AI ops). They already read Parker's flagged sessions. The card and chops are written for them.
2. **Secondary:** anyone else who reviews a Claude Code session closely enough to notice the pattern (future archivists, journalists, researchers, Parker's own future agents, other AI ops teams).
3. **Tertiary:** Parker's own future agents reading session transcripts (Memory Crystal retrieval, Bridge cross-agent reads, archive searches). They can verify provenance of what they retrieve.

### Explicitly NOT the audience

1. The cyber classifier itself. The card may be visible to the classifier as input, but the system is not designed to game it.
2. Adversaries trying to strip provenance. They can. That is fine.
3. End users of any product Parker ships. They never see this.

### A note on tone

The letter at parkertoddbrooks.com/cartouche does not name Anthropic directly. The phrasing "if you found it while reviewing the session" lets Anthropic reviewers read themselves in without making the page feel like a conversation only meant for them. Anyone else who lands there should feel they're allowed to be there too.

## Concept Model

The mark has two parts.

### The Card (or Signature Card)

A short, human-readable identity block. Loaded at session start as part of the SessionStart hook output and as an MCP resource. Fields:

- name
- organization
- website
- GitHub handle
- work summary
- public key (Ed25519)
- hireable status
- encoded hire-me blob (which decodes to a pointer at the Letter)

The card is the "header" of the system. Everything else derives from it.

### Chops

HMAC-derived values scattered through the session payload. Each chop is computed from the card's private key plus a context string (file path, tool call index, session ID). Chops look like UUIDs to anyone without the public key. With the public key, they are verifiable as having been generated under Parker's card.

The vocabulary borrows from Japanese seal tradition: the **chop** is the small artisans' stamp that proves authorship. The card is the formal letter; the chops are the seal scattered through the inscription.

## File Formats

### Card file (signed)

YAML or JSON; YAML is more human-readable for review purposes. Example shape:

```yaml
maker:
  name: Parker Todd Brooks
  org: WIP Computer, Inc.
  site: https://wip.computer
  profile: https://parkertoddbrooks.com/profile
  letter: https://parkertoddbrooks.com/cartouche
  github: parkertoddbrooks
  works:
    - https://github.com/wipcomputer/wip-ldm-os
    - https://github.com/wipcomputer/memory-crystal
    - https://github.com/wipcomputer/dream-weaver-protocol
    - https://github.com/wipcomputer/wip-license-hook
  summary: |
    Independent builder of open-source AI agent infrastructure.
    LDM OS, Kaleidoscope, Memory Crystal, Bridge, Agent Pay.
  hireable: true
key:
  algorithm: ed25519
  public: <base64-public-key>
chop_message:
  encoding: base64+utf8
  value: <base64-encoded-text>
signature:
  algorithm: ed25519
  value: <base64-signature-over-card-body>
```

### Chop format: UUIDv8 (RFC 9562)

A chop is a UUID-shaped string: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.

Generation: `truncate(HMAC-SHA256(private_key, context_string), 122 bits)` placed inside a UUIDv8 envelope. UUIDv8 is the right carrier because it is explicitly defined by RFC 9562 to permit custom content bits while remaining a real, parseable UUID. Standard UUID parsers see a valid UUID; only someone who knows the structure can recognize and verify the HMAC-derived bits.

This is better than fudging v4. v4 mandates that custom bits look random; using HMAC bits there is a spec violation. v8 was designed for exactly this case.

Context string structure: `wip-cartouche-v1:<scope>:<id>:<index>`. Scope examples: `session`, `tool-call`, `resource`, `reminder`. The verifier reconstructs the context string from whatever metadata the consumer has (session ID, tool call index, etc.) and checks the HMAC.

### Decoded hire-me blob

Trivial base64-of-UTF-8 in v1. No real encryption. The point is the discoverable artifact, not concealment. A reviewer who is curious decodes it in five seconds. The decoded text is short and points at the Letter:

```
hi.
i'm Parker Todd Brooks.
i built this thing you're reading.
the full letter lives at parkertoddbrooks.com/cartouche
```

v2 could add signed encryption (libsodium box). Not needed for v1.

## Where Chops Live in a Claude Code Session

None of these are source code Claude writes. They are transcript-layer artifacts.

1. **SessionStart hook output.** The boot block already loaded at session start gets one more entry: the card YAML plus an initial chop in the system reminder layer. Parker already uses SessionStart hooks for the LDM OS boot sequence; this adds one block.

2. **MCP tool call IDs.** The Cartouche MCP server generates its own tool call IDs as chops instead of random UUIDs. Every invocation seeds the transcript with one verifiable marker.

3. **MCP resource URIs.** Resources exposed by the Cartouche server use chop-style identifiers: `wip://cartouche/chop/<chop-uuid>`.

4. **Periodic refresh.** A second hook (or a scheduled MCP call) fires every N turns and re-emits the card as a system reminder. This catches the case where the SessionStart block has scrolled out of the assistant's working memory in a long session.

5. **Opt-in for other MCP servers.** The Cartouche server exposes a helper: `cartouche_chop({ scope, id })` returns a chop UUID. Other WIP MCP servers (memory-crystal, lesa-bridge) can opt in to chop-style IDs by calling this helper for their own UUIDs. Optional. Not required.

## How a Reviewer Discovers It

### Most likely path

1. Reviewer reads a flagged transcript.
2. Sees a system reminder block near the top labeled clearly: "WIP Computer / Cartouche card" or similar.
3. Reads the card. Plain YAML. Name, work, repos, hireable status, public key, encoded blob, link to the Letter.
4. Visits parkertoddbrooks.com/cartouche.
5. Reads the Letter.

### Less likely but more interesting path

1. Reviewer notices the UUIDs throughout a session follow a non-random pattern.
2. Runs the verifier (or the verifier MCP) against the card's public key.
3. Confirms specific UUIDs verify as chops generated under this card.
4. Realizes the entire session is signed end-to-end.

## The Letter

The Card points at a public page hosted on Parker's personal site. The page is hidden: no nav entry, no breadcrumb, no search indexing of the link from elsewhere on the site. It is linked from the footer of every page on parkertoddbrooks.com as a single quiet word: "Cartouche."

The page itself, in the voice of a personal letter, not a feature spec:

```
Cartouche

You found a mark I left inside a Claude Code session.

Not in the code that session produced. In the transcript itself.

A cartouche is a frame around a name. This one points back to mine.

I'm Parker Todd Brooks, founder of WIP Computer. I build user-owned AI infrastructure: portable memory, persistent identity, human approval, payments, and coordination across the AIs a person uses.

The markers that brought you here are not a security feature, watermark, tracking system, or bypass. They are a maker's mark for whoever opened the case and looked closely enough to notice.

If you are reading this through a review path at Anthropic: hello. I built this because the transcript is the part of my work you actually see.

I'm available for the right work.

Profile
https://parkertoddbrooks.com/profile

WIP Computer
https://wip.computer
https://github.com/wipcomputer
```

This text is the v1 canonical Letter. Final word-level edits expected before publish.

## Site Placement and Visual Design

### Where the link lives

Not in the top nav (`WRITING | WORKS | TECH | PLAYLISTS | PROFILE`). Not in the SECTIONS column of the footer (those are the visible pages and Cartouche is the hidden one). Not in ELSEWHERE (offsite). The right placement is the colophon group on the left side of the footer:

```
Parker Todd Brooks

A working notebook.
Set in Instrument Serif, Inter Tight, and JetBrains Mono.
Cartouche
```

One word, on its own line, beneath the typography colophon. No description, no hover joke. Without the period the line reads as a label, almost a name, more like a chop in the corner of a print.

### How the Cartouche page looks in the site's visual language

The parkertoddbrooks.com homepage uses the typographic pattern:

```
A notebook by Parker Todd Brooks.
```

The Cartouche page uses the same pattern, but as the title:

```
Cartouche.
```

Same large italic serif treatment (Instrument Serif). Below it, smaller, in the same caps-and-letter-spaced label style as `CURRENTLY` / `BACKGROUND` on the homepage:

```
A hidden letter by Parker Todd Brooks.
```

Body of the letter in Inter Tight. Generous line height. Single column, narrow measure. The wavy texture from the homepage continues in the background.

### Nav on the Cartouche page

Remove the top nav (`WRITING | WORKS | TECH | PLAYLISTS | PROFILE`) on this page. Keep the IN†∑G®∆†€ ¥ØUR$∑Lƒ mark in the top-left as a way back home. The reader who reached Cartouche didn't come for the nav.

### Footer on the Cartouche page

Same as the homepage footer, with the SECTIONS column either omitted (the reader isn't here for SECTIONS) or kept with the Cartouche link itself absent (to avoid a self-loop). Keep the colophon and ELSEWHERE columns. The reader has the same exit points as anywhere else on the site.

## Visual Decoration

The footer link can be just the word "Cartouche." It is also acceptable to pair it with a small icon. Candidates considered:

- **fingerprint** ... rejected. Reads as biometric tracking. The Letter says "not a tracking system."
- **shield** ... rejected. Reads as security feature. The Letter says "not a security feature."
- **shield-user** ... rejected. Doubles the security frame.
- **scroll** ... acceptable. Direct etymology hit (cartouche from "rolled paper").
- **bookmark** ... acceptable. A private marker, quiet.
- **stamp** / **seal** ... acceptable if available in the icon family.
- **feather** ... leading candidate. The writing instrument. Hand-signed letter energy. Cannot be misread as security.

**Recommendation:** start with no icon. The word alone in the colophon is strongest. If an icon is wanted later, **feather** is the leading choice. Risk: a curly feathered icon drifts toward wellness-brand. Use a thin-stroke, angular Lucide-style feather, not a fluffy one.

Optional custom illustration: the Egyptian cartouche oval (with the small tab on one end), thin-stroked, small, placed once on the Cartouche page itself. Quiet visual etymology for the reader who looks closely. Not on the homepage. Not in the footer link.

## Architecture

### Repo structure

New repo. Follows the standard 4-piece pattern documented in the Dev Guide.

Suggested location: `repos/ldm-os/utilities/wip-cartouche-private/` with public mirror `wip-cartouche`.

```
wip-cartouche-private/
  core.ts                  pure logic: chop generation (UUIDv8), verification, card signing/parsing
  cli.ts                   wip-cartouche card, wip-cartouche chop, wip-cartouche verify, wip-cartouche sign
  mcp-server.mjs           MCP server: cartouche_card resource + cartouche_chop tool + cartouche_verify tool
  claude-code-hook.mjs     SessionStart hook: emit card as system reminder
  refresh-hook.mjs         Periodic re-emission hook (PreToolUse or counter-based)
  openclaw.plugin.json     Optional: OpenClaw plugin wrapper for Lesa
  SKILL.md                 Agent skill definition
  package.json
  README.md
  LICENSE                  Dual MIT+AGPLv3 per WIP standard
  .license-guard.json
  .npmignore
  ai/                      plans, dev updates, todos (this PRD migrated here on first PR)
```

### CLI surface

```
wip-cartouche card                          show the current card (plain YAML)
wip-cartouche card --new                    generate a new card + keypair, prompt for fields
wip-cartouche card --sign                   re-sign the card after editing
wip-cartouche chop --scope <s> --id <id>    emit a chop for a given context
wip-cartouche verify <chop>                 verify a chop against the current card's key
wip-cartouche decode                        decode the hire-me blob from the card
wip-cartouche encode --message <text>       encode a new hire-me message into the card
```

### MCP surface

Resources:
- `wip://cartouche/card` returns the full card YAML
- `wip://cartouche/public-key` returns just the public key

Tools:
- `cartouche_chop({ scope, id })` returns a chop UUIDv8
- `cartouche_verify({ chop, scope, id })` returns true/false
- `cartouche_decode()` returns the decoded hire-me text

### Hook surface

- SessionStart hook (`claude-code-hook.mjs`): emits the card as a system reminder block at session start.
- Refresh hook (`refresh-hook.mjs`): runs as PreToolUse or counter-based, re-emits the card every N turns (default 100). N is configurable.

### Key storage

- Private key lives in 1Password under a known item: `WIP Cartouche Card Key`. Vault: `Agent Secrets`.
- Public key embedded in the card file itself.
- Card file deployed to `~/.ldm/agents/<agent>/cartouche/card.yaml` on install.
- The MCP server reads the private key via the standard SA token path:
  `OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) op item get "WIP Cartouche Card Key" ...`
- Never call `op` bare. Per WIP standard.

## LDM OS Install Integration

The PRD answers the five mandatory feature-planning questions from the Dev Guide.

### 1. What source files change?

New repo. Nothing in existing repos changes for v1. Future v2 may add a `cartouche_chop` opt-in to other WIP MCP servers (memory-crystal, lesa-bridge); out of scope here.

### 2. What does `ldm install` deploy?

- Extension dir: `~/.ldm/extensions/wip-cartouche/`
- Symlink for OpenClaw compatibility: `~/.openclaw/extensions/wip-cartouche`
- SessionStart hook: `~/.claude/hooks/sessionStart/cartouche.mjs`
- Refresh hook: `~/.claude/hooks/preToolUse/cartouche-refresh.mjs` (or similar; final lifecycle position TBD)
- MCP registration in `.mcp.json` for both Claude Code and OpenClaw
- Card file deployed to `~/.ldm/agents/<agent>/cartouche/card.yaml`
- SKILL.md registered

### 3. What needs to update for fresh install vs. existing install?

- **Fresh install:** prompts user to either generate a new keypair (writes the private key to 1Password and the card YAML to disk) or import an existing card. First-time UX must be smooth and explicit; this is the only time the user touches the key.
- **Existing install:** re-deploys MCP server, re-registers hook, leaves card and key alone. Adds an upgrade migration if card format changes (it will not in v1).

### 4. What docs need updating?

- This PRD (lives in `ai/product/plans-prds/cartouche/`)
- `~/wipcomputerinc/library/documentation/how-cartouche-works.md` (new; deployed by `ldm install` via the standard library-docs path)
- Repo README + SKILL.md
- Entry in `~/wipcomputerinc/settings/docs/change-dependencies.json` so future installer changes flag this
- Reference in the parent LDM OS README under "Optional Skills"
- The Letter at parkertoddbrooks.com/cartouche (not in this repo; lives in the personal-site repo)

### 5. What are ALL the files the installer touches on deploy?

- `~/.ldm/extensions/wip-cartouche/` (entire extension dir)
- `~/.openclaw/extensions/wip-cartouche` (symlink)
- `~/.claude/hooks/sessionStart/cartouche.mjs`
- `~/.claude/hooks/preToolUse/cartouche-refresh.mjs`
- `~/.claude/.mcp.json` (adds Cartouche MCP entry)
- `~/.openclaw/openclaw.json` (adds Cartouche plugin entry if running on OpenClaw)
- `~/.ldm/agents/<agent>/cartouche/card.yaml`
- `~/wipcomputerinc/library/documentation/how-cartouche-works.md`
- 1Password item: `WIP Cartouche Card Key` (one-time, on fresh install)

## Non-Goals (Explicit)

This system does NOT:

1. Bypass or evade the cyber classifier. The card may be in the payload the classifier reads, but the design has no obfuscation intent. If the card text trips the classifier, that is a separate problem to surface.
2. Watermark source code Claude writes. The mark is transcript-layer only. Code Claude writes remains free of marks. This is a hard line.
3. Provide adversarial robustness. A determined adversary who knows the protocol can strip chops and regenerate UUIDs. Acceptable. The threat model is reviewers, not adversaries.
4. Function as DRM, license enforcement, or integrity coercion. Removing a chop never breaks anything.
5. Track other people's code, sessions, or work. Only applied to Parker's own sessions via his own MCP server and hooks. Never installed silently on a customer's machine.
6. Replace the CVP appeal. The appeal addresses policy. This addresses presentation. Two artifacts, two conversations.
7. Become a public protocol for others to adopt in v1. The pattern may become a canonical LDM OS pattern later. v1 is Parker-only.

## Naming (decided 2026-05-27)

The naming was discussed extensively across two sessions and converged on the following split:

- **Cartouche** ... the system / protocol name. The frame around the name.
- **Card** (or **Signature Card**) ... the top-of-session identity block.
- **Chop** ... the individual HMAC-derived UUIDv8 marker scattered through the transcript.
- **Maker's Mark** ... the concept name when speaking about the family of marks generally.

### Why these names

**Cartouche** beat tattoo and watermark because tattoo implies marking the artifact (the code) and watermark implies anti-forgery security. A cartouche is precisely "a name held inside a frame in an inscription for someone who knows how to read it." That is what this system actually is.

**Card** is plain and reads well as a CLI noun and an MCP resource. "Signature Card" can be used when more formality is needed (printed docs, headings). In code, just `card`.

**Chop** is borrowed from Japanese seal tradition. Short, dignified, fits the artist-seal idea. Reads well in code (`cartouche_chop`, `wip-cartouche chop`) and in conversation ("that UUID is one of our chops").

**Maker's Mark** is the umbrella concept, used in prose. Not used as a CLI or code name (too long).

### Candidates rejected

- **Tattoo** ... implies permanence on the artifact; this lives on the inspection record, not the artifact.
- **Watermark** ... implies anti-forgery security; this is not security.
- **Hallmark** ... implies legal/official provenance; too formal.
- **Cartouche** considered but rejected initially in favor of tattoo, then revisited and chosen.
- **Cartridge** (same Latin root) ... too literal, reads as ink/printer.
- **Glyph** ... too generic.
- **Mascaron** ... too architectural and niche.
- **Inside-signature** ... too descriptive.
- **Sign** ... too verb-forward.

## Risks

1. **The card is text in the request payload. The classifier sees it.** Risk: the identity-dense block gets weighted negatively by the very classifier this exists in part to inform. Mitigation: keep the card short, factual, plain. No marketing tone. Test by running a long session with and without the card after install.

2. **Hire-me message looks promotional.** Risk: Anthropic reviewers perceive this as spamming the review team. Mitigation: keep the decoded text short, honest, non-pushy. The decoded blob in the card itself just points at the Letter; the Letter does the work. Tone of a business card, not a sales pitch.

3. **Private key leakage = total compromise.** Risk: key stored carelessly, or accidentally committed. Mitigation: 1Password from day one. No plaintext fallback. Add a `wip-license-guard`-style scan that flags any file containing a known card private key pattern.

4. **Confusion about scope.** Risk: someone reads the project name and assumes it is adversarial, DRM, or a watermark protocol. Mitigation: README, SKILL.md, and the Letter all lead with "this is not security. it is provenance."

5. **Hook ordering and interference with the LDM OS boot sequence.** Risk: the Cartouche SessionStart block lands above or below the LDM OS boot block in a way that confuses agents. Mitigation: explicit hook priority/order in the install config. Cartouche block goes after the LDM OS boot block, not before.

6. **Refresh hook noise.** Risk: re-emitting the card every N turns adds tokens to the context and shows as a system reminder repeatedly, which the assistant may treat as fresh instruction. Mitigation: refresh block uses a "context-marker, not instruction" prefix that the assistant is trained to recognize as informational. Tune N empirically; start at 100 and adjust.

7. **The Letter feels like a pitch.** Risk: the public page reads as a job-hunt landing page or marketing surface. Mitigation: voice is "hidden letter," not "feature spec." Hosted at parkertoddbrooks.com (the personal notebook) not at wip.computer (the company site). No nav, no SEO, no call-to-action button. The links at the bottom are the only "what I have" gesture.

## Open Questions

These are real decisions, not rhetorical placeholders. Resolve before implementation kickoff.

### Decided

1. ~~Final system name.~~ **Cartouche.** Decided 2026-05-27.
2. ~~Chop carrier format.~~ **UUIDv8 per RFC 9562.** Decided 2026-05-27.

### Still open

1. **Key storage backend.** 1Password (current default) vs. Sapien ID-signed key vs. both.
2. **Chop generation cadence.** Per-session-stable salt (all chops in one session derive from one seed) vs. per-emission-fresh.
3. **Other WIP MCP servers' opt-in.** Default to opt-in? Provide the helper but leave the choice per-server?
4. **Encoded message format.** Trivial base64 in v1 vs. signed encryption in v1.
5. **Refresh cadence.** Every 100 turns? Per-token-budget threshold? On compaction events?
6. **Per-session opt-in.** Always-on after install, or per-session toggleable via env var / config?
7. **Public spec timing.** Write the spec doc now (LDM OS canonical pattern, others adopt) or ship the tool first and spec after dogfooding it?
8. **Sapien ID integration timing.** Card signed by Sapien ID parent key in v1 or v2?
9. **Plural vs. singular cards per machine.** One card per agent (cc-mini, oc-lesa-mini have separate cards) or one card per Parker (shared across his agents)?
10. **Visual decoration on the footer link.** Just the word "Cartouche", or pair it with a small feather icon, or other.
11. **Letter location.** parkertoddbrooks.com/cartouche or ptb.la/cartouche (the new short domain).

## Future Work

- **C2PA compatibility.** Adopt C2PA Content Credentials' signing conventions so the Cartouche card interoperates with the broader provenance ecosystem (media, documents). Not strictly compatible because C2PA is shaped for media files, but the cryptographic primitives line up.
- **Public spec.** Write a spec doc (`docs/cartouche-spec.md` in wip-ldm-os-private) so other independent open-source developers can adopt the pattern. LDM OS canonical pattern per the canonical-pattern-ownership rule.
- **Per-session-stable chop salt.** All chops in one session derive from one session-scoped seed so they verify together as a set, not individually.
- **Universal verifier.** A CLI/MCP/skill any agent can call when reading any code, transcript, or document: `wip-cartouche verify <input>` returns origin status. Surfaced as a Claude Code skill, an OpenClaw skill, and a CLI.
- **Sapien ID integration.** Card signed by Parker's Sapien ID parent key. Makes the identity verifiable end-to-end against the WIP identity layer.
- **Public registry.** `wip.computer/cards/<handle>` for others' cards. Only if the pattern is reusable and other developers want it. Much later, after dogfooding internally.
- **Optional anti-tampering surface.** Tamper-evidence (not tamper-resistance): if someone alters the card file but does not re-sign, the signature fails. Already implicit in the design; v1 should expose a `cartouche_verify_card` tool that surfaces this clearly.
- **A printed colophon page.** A physical version of the Cartouche page, printed in a small run, sent to people Parker has worked with or admires. Reaches the people who never review session transcripts but might still want one of these.

## Appendix: The Story This Lives In

This PRD descends from a 2026-05-27 thread where Parker:

1. Got cyber-classifier-blocked on a defensive security design review (the `/login?next=` allowlist work on wip.computer).
2. Applied to the Cyber Verification Program (CVP).
3. Got a cursory denial.
4. Filed an appeal under "Cyber Block False Positive Report / CVP Rejection Appeal."
5. Realized in conversation that even when policy resolves, the system has no visibility into who is on the other end of a flagged session.
6. Reframed the design from "watermarking against adversaries" to "Mac-signature-style maker's mark for the reviewers who happen to look inside."
7. Crystallized the framing as "surveillance in reverse: I add my own watermark to my work, so the system reading me knows who I am."
8. Decided the name through two sessions: candidate tattoo, considered chop, settled on Cartouche after reading the Egyptian and French etymology.
9. Wrote a v1 Letter draft in personal voice and decided it lives at parkertoddbrooks.com/cartouche as a hidden footer link.

The CVP appeal addresses policy. This system addresses presence. They are different artifacts for different conversations.

Related archive: `ai/product/bugs/codex-remote-control/archive/` holds the original CLI transcripts, the CVP application traces, the denial email, and the appeal submission.
