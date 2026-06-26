---
name: pnpm-docker
description: Docker builds with BuildKit cache, pnpm fetch, pnpm deploy
---

# pnpm Docker Best Practices

Docker can't use reflinks/hardlinks between container and host. Use BuildKit cache mounts. For Btrfs/CoW filesystems, [Podman](https://pnpm.io/podman) can share store via mounted volumes.

## Single Package: Multi-stage

```dockerfile
FROM node:20-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
COPY . /app
WORKDIR /app

FROM base AS prod-deps
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --prod --frozen-lockfile

FROM base AS build
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run build

FROM base
COPY --from=prod-deps /app/node_modules /app/node_modules
COPY --from=build /app/dist /app/dist
EXPOSE 8000
CMD ["pnpm", "start"]
```

## Monorepo: pnpm deploy

```dockerfile
FROM node:20-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

FROM base AS build
COPY . /usr/src/app
WORKDIR /usr/src/app
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile
RUN pnpm run -r build
RUN pnpm deploy --filter=app1 --prod /prod/app1
RUN pnpm deploy --filter=app2 --prod /prod/app2

FROM base AS app1
COPY --from=build /prod/app1 /prod/app1
WORKDIR /prod/app1
CMD ["pnpm", "start"]

FROM base AS app2
COPY --from=build /prod/app2 /prod/app2
WORKDIR /prod/app2
CMD ["pnpm", "start"]
```

Build: `docker build . --target app1 --tag app1:latest`

## CI: pnpm fetch

When BuildKit cache mounts aren't available, use `pnpm fetch`—only needs `pnpm-lock.yaml`. Cache invalidates only when deps change:

```dockerfile
FROM node:20-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

FROM base AS prod
COPY pnpm-lock.yaml /app
WORKDIR /app
RUN pnpm fetch --prod

COPY . /app
RUN pnpm install -r --offline --prod
RUN pnpm run build

FROM base
COPY --from=prod /app/node_modules /app/node_modules
COPY --from=prod /app/dist /app/dist
CMD ["node", "dist/index.js"]
```

## Podman (Btrfs)

On Btrfs, Podman can share the store between host and container via volumes:

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

```bash
podman build . -t my-image -v "$HOME/.local/share/pnpm/store:/pnpm-store" -v "$(pwd)/node_modules:/app/node_modules"
```

## .dockerignore

```
node_modules
.git
.gitignore
*.md
dist
```

## Monorepo pnpm-workspace.yaml for deploy

```yaml
packages:
  - 'packages/*'
syncInjectedDepsAfterScripts:
  - build
injectWorkspacePackages: true
```

<!--
Source references:
- https://pnpm.io/docker
- https://pnpm.io/podman
- https://pnpm.io/cli/fetch
- https://pnpm.io/cli/deploy
-->
