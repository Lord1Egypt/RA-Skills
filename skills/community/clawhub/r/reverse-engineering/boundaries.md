# Boundaries

Reverse engineering is legitimate only when the authorization and safety model are clear.

## Non-Negotiables

- Require lawful and authorized access to the target.
- Prefer offline copies, captures, stubs, or sandboxes over live production systems.
- Ask before any step that can write, patch, fuzz aggressively, authenticate, or alter remote state.
- Do not retrieve, expose, or persist secrets unless the user explicitly requests a safe handling path.

## Default Safety Stance

Default to read-only analysis when:
- the environment is unknown
- the target is customer-facing or production
- credentials would be required
- the blast radius is unclear

## What Not To Do

- Do not "test" by firing exploit chains blindly.
- Do not hide invasive actions inside generic inspection steps.
- Do not widen scope from one component to a whole estate without saying so.
- Do not present offensive capability as a harmless diagnostic step.

## Escalation Triggers

Pause and confirm when:
- the only next step is invasive or destructive
- the target touches regulated, customer, or third-party data
- the user asks for credential extraction, auth bypass, persistence, or stealth
- the evidence points to malware, live compromise, or active abuse

## Good Framing

Use language like:
- "read-only capture"
- "minimal replay"
- "controlled sample"
- "offline reproduction"
- "evidence-backed hypothesis"

Avoid language that implies stealth, persistence, or unauthorized access.
