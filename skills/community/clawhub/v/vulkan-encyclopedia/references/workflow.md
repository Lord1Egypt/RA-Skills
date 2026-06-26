# Vulkan Encyclopedia Workflow

## Core stance

Use the authoritative Vulkan specification plus local observed project state together.

Default order:
1. check `.Vulkan-Encyclopedia/` cache/notes
2. check official Vulkan docs when needed
3. inspect live code/project state
4. answer or act
5. record durable learnings

## When docs lookup is mandatory

Do a docs lookup before answering or acting when any of these are true:
- the user asks about Vulkan command syntax, structure members, object lifetime, synchronization, or valid-usage behavior
- the task involves instance/device creation, swapchains, queues, command buffers, descriptors, pipelines, render passes or dynamic rendering, memory/resources, or extension/feature enabling
- the task involves VUIDs, validation-layer messages, or spec interpretation
- the task involves a version-sensitive feature or behavior you are not highly confident about
- the task involves live implementation/review guidance and the exact rule boundaries matter

## Cache-first rule

Before fetching docs, check whether the needed material already exists under:
- `.Vulkan-Encyclopedia/docs/docs.vulkan.org/spec/latest/...`
- `.Vulkan-Encyclopedia/notes/components/...`
- `.Vulkan-Encyclopedia/notes/patterns/...`
- `.Vulkan-Encyclopedia/inventory/...`

If the local cache is good enough, use it.
If not, fetch/check the official docs and then cache what you used.

## How to cache docs

Use `scripts/cache_doc.py`.

Typical usage:

```bash
python3 scripts/cache_doc.py   --url 'https://docs.vulkan.org/spec/latest/chapters/synchronization.html'   --root '<workspace>/.Vulkan-Encyclopedia'
```

The script will:
- fetch the page
- convert it into a normalized markdown-ish cache file
- place it under `.Vulkan-Encyclopedia/docs/docs.vulkan.org/spec/latest/...`
- add metadata such as source URL and fetch timestamp

## How to store local knowledge

### Component notes

Use `.Vulkan-Encyclopedia/notes/components/<component-name>.md` for:
- subsystem purpose
- Vulkan object/model role
- sensitive boundaries
- discovered quirks

### Pattern notes

Use `.Vulkan-Encyclopedia/notes/patterns/<topic>.md` for:
- recurring synchronization patterns
- resource-lifetime rules used by the project
- repeated validation/debugging gotchas
- environment- or engine-specific design conventions

### Inventory files

Use `.Vulkan-Encyclopedia/inventory/` for:
- project/access inventory
- architecture/runtime layout
- documentation index

## Distinguish evidence types

When writing notes, label information mentally as one of:
- **Authoritative docs** — from the Vulkan specification/docs
- **Observed local state** — from live code/project inspection
- **Inference/recommendation** — your judgment based on docs + local state

Do not blur these together.

## Recommended answer style

When it helps, mention whether your answer is based on:
- cached official docs
- freshly checked official docs
- live project/code inspection
- best-practice inference

## High-sensitivity areas

Treat these as high-sensitivity even when you have live access:
- synchronization and memory-ordering rules
- resource lifetime and ownership transitions
- extension/feature gating decisions
- layout transitions and queue ownership transfers
- validation/VUID interpretation that could mislead implementation

For these, prefer docs lookup even if you think you remember the rule.
