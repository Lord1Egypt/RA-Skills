# Vulkan Topic Map

Use this as a quick orientation aid when deciding what docs to look up.

## Core areas

- Instance/device creation and feature enabling
- Queues, command pools, and command buffers
- Swapchains, presentation, and surface behavior
- Buffers, images, memory, and resource lifetime
- Descriptors, descriptor sets, and pipeline layouts
- Render passes, framebuffers, and dynamic rendering
- Pipelines, shaders, and SPIR-V in a Vulkan pipeline context
- Synchronization, barriers, semaphores, and fences
- Validation, VUIDs, limits, formats, and extensions

## Typical lookup prompts

When the task is about...

### Initialization / feature enabling
Look for docs covering:
- instances
- physical devices
- logical devices
- queue families
- features and extensions
- limits and properties

### Presentation / swapchain
Look for docs covering:
- surfaces
- swapchains
- present modes
- image acquisition/presentation synchronization

### Resources / memory
Look for docs covering:
- buffers
- images
- image layouts
- memory requirements
- allocation/binding
- transfer/copy behavior

### Descriptors / pipelines
Look for docs covering:
- descriptor set layouts
- descriptor writes
- pipeline layouts
- graphics/compute pipelines
- push constants

### Synchronization / validation
Look for docs covering:
- synchronization chapter
- pipeline barriers
- semaphores
- fences
- queue ownership transfer
- validation messages / VUID references

## Trigger boundary reminder

Use this skill for Vulkan-specific API/spec/review/troubleshooting work.
Do not trigger it for generic graphics or shader questions unless the Vulkan API layer materially matters.
