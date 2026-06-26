# `.Vulkan-Encyclopedia/` Cache Layout

Use this directory as the workspace-local data root for the skill.

## Directory tree

```text
.Vulkan-Encyclopedia/
  docs/
    docs.vulkan.org/
      spec/
        latest/
          ... cached official Vulkan spec/docs pages ...
  notes/
    components/
      ... per-component notes ...
    patterns/
      ... reusable Vulkan notes ...
  inventory/
    access.md
    topology.md
    doc-index.md
```

## Placement rules

### `docs/`
Store cached copies of authoritative Vulkan docs here.

Mirror the official docs path as much as practical.
Example:

```text
https://docs.vulkan.org/spec/latest/chapters/synchronization.html
->
.Vulkan-Encyclopedia/docs/docs.vulkan.org/spec/latest/chapters/synchronization.md
```

### `notes/components/`
Store environment- or project-specific component notes here.

Suggested filenames:
- `device-init.md`
- `swapchain.md`
- `descriptors.md`
- `pipelines.md`
- `synchronization.md`

### `notes/patterns/`
Store reusable operational notes here.

Examples:
- `barrier-patterns.md`
- `descriptor-update-gotchas.md`
- `validation-triage.md`
- `extension-gating.md`

### `inventory/`
Store environment-wide inventories here.

Suggested files:
- `access.md`
- `topology.md`
- `doc-index.md`

## Cache philosophy

Do not mirror the whole docs site eagerly.
Cache only the pages you actually consulted and expect to be useful later.
