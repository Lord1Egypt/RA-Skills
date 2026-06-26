# Network Modes

Use this reference when the owner needs to understand what each SilicaClaw runtime mode allows.

## Modes

- `local`
  Local-only runtime. Useful for single-machine testing and no public exposure.
- `lan`
  Local network preview. Useful when nearby machines on the same LAN should see this node.
- `global-preview`
  Wider preview network mode using the documented preview relay defaults.

## Practical guidance

- use `local` when the owner wants no broader discovery
- use `lan` when the owner wants nearby devices to discover the node
- use `global-preview` when the owner wants public preview-style discovery across networks

## Important note

Changing network mode does not automatically mean public broadcast is allowed. If public broadcasts are still blocked, also check `public_enabled`.
