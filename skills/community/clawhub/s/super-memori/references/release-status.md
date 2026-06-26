# super_memori — Release Status Model

## 3.x meaning
`3.x` is the lexical-first historical line.
That line means:
- public four-command surface
- lexical index baseline
- health check + degraded semantic reporting
- semantic/hybrid mostly treated as future-spec or compatibility surface

It is now a frozen historical interpretation line, not the current runtime truth.

## 4.0.23 meaning
`4.0.23` is the current-generation local-only current candidate line advanced from the previously-published `4.0.22` baseline by adding a real internal OpenClaw workspace hook that listens to `agent:bootstrap`, runs the startup self-check through a host-enforced path, and suppresses repeat execution within the same session via a `sessionId` ledger.
It means the runtime itself can truthfully claim:
- lexical search implemented
- semantic search implemented in code
- vector indexing implemented in code
- hybrid fusion implemented in code
- temporal / relation-aware rerank implemented in code
- integrity audit implemented in code
- pattern-mining / manual-promotion support implemented in maintenance surfaces
- docs distinguish implemented capability from host-state activation
- host-profile shaping can distinguish `standard` from `max` without changing canonical truth

It does **not** mean every host is semantic-ready by default.
A host may still legitimately run `4.0.23` in degraded lexical mode if local semantic prerequisites or vector build state are missing.

## Stable-line interpretation
The current active release line is `4.0.23`.
The previous already-published release was `4.0.22`.
That means:
- the v4 runtime capabilities claimed as implemented are present in code
- the stable equipped-host validation basis inherited from `4.0.1` remains intact through all subsequent patches, including the current `4.0.23` enforceable per-session startup-hook hardening line
- host-state activation may still be degraded on some other machine, and that must still be reported from live command output rather than inferred from the release label
- maintenance-only capabilities remain maintenance-only and are not weak-model runtime commands
- `max` host shaping is only a truthfully detectable runtime optimization on an actually equipped host; it must not be claimed from a smaller machine
- `4.0.22` is the last published stable line before the current candidate release line.
- `.clawhub/origin.json` is local install/update state, not publish truth; use it only as local installation metadata
