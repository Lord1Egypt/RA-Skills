---
name: best-practices-podman
description: Using pnpm with Podman (Btrfs, reflinks, volume mounts)
---

# Podman with pnpm

Podman can use copy-on-write filesystems (e.g. Btrfs). With Btrfs, container runtimes create subvolumes for mounted volumes, and pnpm can **reflink** files between host and container instead of copying. On other filesystems (e.g. Ext4), pnpm will copy.

## Sharing Store and node_modules

Mount the pnpm store and project `node_modules` from the host so the container reuses them:

1. Set global store dir in the image to a volume path (e.g. `/pnpm-store`).
2. Mount the host store and `node_modules` into the container.

Example Dockerfile (works with Podman):

```dockerfile
FROM node:20-slim
RUN corepack enable

VOLUME [ "/pnpm-store", "/app/node_modules" ]
RUN pnpm config --global set store-dir /pnpm-store

COPY package.json /app/package.json
WORKDIR /app
RUN pnpm install
RUN pnpm run build
```

Build with Podman, mounting host store and node_modules:

```bash
podman build . --tag my-podman-image:latest \
  -v "$HOME/.local/share/pnpm/store:/pnpm-store" \
  -v "$(pwd)/node_modules:/app/node_modules"
```

## Key Points

- Btrfs (and similar CoW filesystems) allow reflinks; pnpm reuses files between host and container.
- On non-CoW filesystems, pnpm copies; mounting store and node_modules still avoids re-downloading.
- Use `store-dir` in the container to match the mounted volume path.

<!--
Source references:
- https://pnpm.io/podman
- sources/pnpm/docs/podman.md
-->
