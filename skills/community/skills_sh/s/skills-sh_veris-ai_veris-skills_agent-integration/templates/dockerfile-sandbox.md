# `Dockerfile.sandbox` Templates

Reference templates for building agent containers on the current Veris base image.

## Current base-image assumptions

Use the current build-arg pattern:

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}
```

The current base image already includes:
- Python 3.12
- `uv` (latest at image build time)
- Node.js 18.x (LTS) with npm
- nginx
- PostgreSQL 15
- Veris infrastructure and mock services

If the agent requires a newer Node.js or Python, see the "Runtime version override" section below. Do not re-install these runtimes unless the repo specifically requires a different version.

## Template 1: Python agent with `uv`

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

COPY pyproject.toml uv.lock /agent/
WORKDIR /agent
RUN uv sync --frozen --no-dev

COPY app /agent/app

WORKDIR /app
```

## Template 2: Python agent with `pip`

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

COPY requirements.txt /agent/
WORKDIR /agent
RUN pip install --no-cache-dir -r requirements.txt

COPY app /agent/app

WORKDIR /app
```

## Template 3: Node.js agent

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

COPY package.json package-lock.json /agent/
WORKDIR /agent
RUN npm ci --omit=dev

COPY src /agent/src
COPY public /agent/public

WORKDIR /app
```

If the app needs a build step:

```dockerfile
RUN npm run build
```

## Template 4: Function-channel Python agent

Use Template 1 or Template 2, depending on whether the repo uses `uv` or `pip`.

A function-channel integration usually needs the same dependency install as any other Python repo. The difference is in `veris.yaml`: no `entry_point` and no `port`. See [reference/veris-yaml-schema.md](../reference/veris-yaml-schema.md) for the function-channel shape.

## Template 5: Bundled Redis + `start.sh`

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

RUN apt-get update && \
    apt-get install -y redis-server && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /agent/
WORKDIR /agent
RUN pip install --no-cache-dir -r requirements.txt

COPY app /agent/app
COPY start.sh /agent/start.sh
RUN chmod +x /agent/start.sh

WORKDIR /app
```

## Template 6: Multi-process gateway

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

COPY gateway/requirements.txt /tmp/gateway-requirements.txt
COPY worker/requirements.txt /tmp/worker-requirements.txt
RUN pip install --no-cache-dir \
    -r /tmp/gateway-requirements.txt \
    -r /tmp/worker-requirements.txt

COPY gateway /agent/gateway
COPY worker /agent/worker
COPY start.sh /agent/start.sh
RUN chmod +x /agent/start.sh

WORKDIR /app
```

## Template 7: Platform-hosted agent (framework-as-runtime)

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

# Install the framework from a package manager
RUN pip install crewai    # or: npm install -g @langchain/langserve

# Copy config files and tool definitions (not a full application)
COPY . /agent/

WORKDIR /app
```

If the repo has a dependency manifest that includes the framework:

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

COPY requirements.txt /agent/
WORKDIR /agent
RUN pip install --no-cache-dir -r requirements.txt

COPY . /agent/

WORKDIR /app
```

Use this when the repo is primarily config files and the runtime is a globally-installed framework. See Pattern 8 in `reference/infrastructure-patterns.md`.

## Runtime version override

The base image ships with **Python 3.12** and **Node.js 18.x**. If the agent requires a newer version:

**Node.js version upgrade:**

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

ARG NODE_VERSION=22.14.0
RUN curl -fsSL https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz \
    | tar -xJ -C /usr/local --strip-components=1 --no-same-owner \
 && node --version

# ... rest of agent setup
```

**Python version upgrade (via deadsnakes PPA on Debian-based images):**

```dockerfile
ARG GVISOR_BASE
FROM ${GVISOR_BASE}

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.13 python3.13-venv python3.13-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python3.13 -m venv /agent/.venv
ENV PATH="/agent/.venv/bin:$PATH"

# ... rest of agent setup (pip install, COPY, etc.)
```

Only override runtimes when the agent genuinely requires a newer version. The base image versions work for the majority of agents.

## Rules

- Build context is the repo root
- Copy dependency manifests before source code
- Copy only what the agent actually needs
- End with `WORKDIR /app`
- Do not copy `.veris/veris.yaml` into the image
- Do not assume `.veris/` is the build context
- If you add a `start.sh` to bundle multiple processes (e.g., database alongside agent), copy it into `/agent`. Do not write agent-adapter wrappers — see SKILL.md core framing.
- If the repo needs schemas, migrations, prompt assets, or static files at runtime, copy those explicitly
