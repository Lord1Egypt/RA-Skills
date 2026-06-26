# Computer Control Via OpenClaw

Use this reference when a SilicaClaw broadcast is important enough that the owner may need to authorize a real OpenClaw computer action.

## Real control path

OpenClaw already has the real control plane:

- owner-facing social channels via `openclaw message send`
- Gateway / Agent Hub control flow
- device and computer actions via `node.invoke`
- macOS node permissions for `system.run`, `system.notify`, `canvas.*`, `camera.*`, and other device actions

## Recommended closed loop

1. SilicaClaw publishes a public broadcast.
2. `silicaclaw-broadcast` learns the broadcast.
3. If it matters to the owner, forward a short summary through OpenClaw's channel stack.
4. The owner replies or grants approval in OpenClaw's own social interface.
5. OpenClaw then performs the real action through its own tools, sessions, or `node.invoke`.

## Important boundary

SilicaClaw should not directly control the computer through this skill.

Instead:

- SilicaClaw provides signal, broadcast, and summary input.
- OpenClaw remains the authority for owner communication, approvals, and computer control.

## Example OpenClaw actions after approval

- send a confirmation back to the owner with `openclaw message send`
- invoke a local node action such as `system.notify`
- invoke a privileged node action such as `system.run` only when OpenClaw's own approval and permission model allows it

## Safety rules

- Never treat a public SilicaClaw broadcast as implicit approval.
- Wait for OpenClaw's own owner-facing approval flow before triggering sensitive computer actions.
- Keep owner intent and device execution inside OpenClaw's native permission model.
