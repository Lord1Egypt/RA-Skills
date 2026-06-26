---
name: service-catalog
description: Auto-discover and catalog all services in a codebase or organization — scan Dockerfiles, docker-compose, Kubernetes manifests, package.json, systemd units, Procfiles. Generate a living service inventory with ownership, dependencies, tech stack, and health status.
---

# Service Catalog

Build and maintain a comprehensive service catalog by scanning infrastructure-as-code, config files, and project metadata. Answers "what services do we run, who owns them, what do they depend on, and are they healthy?"

Use when: "list all our services", "what microservices do we have", "service inventory", "who owns this service", "map our infrastructure", "service dependencies", "platform engineering audit", or setting up an internal developer portal.

## Commands

### 1. `discover` — Auto-Discover Services

Scan the workspace for service definitions across all common patterns.

#### Docker Services
```bash
# Docker Compose services
find . -maxdepth 4 \( -name "docker-compose.yml" -o -name "docker-compose.yaml" -o -name "compose.yml" -o -name "compose.yaml" \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | while read f; do
  echo "=== $f ==="
  # Extract service names
  python3 -c "
import sys
in_services = False
indent = 0
for line in open('$f'):
    stripped = line.rstrip()
    if stripped == 'services:':
        in_services = True
        continue
    if in_services:
        if stripped and not stripped.startswith(' ') and not stripped.startswith('#'):
            break
        if stripped and not stripped.startswith('  ') or (len(stripped) > 0 and stripped[0] != ' ' and stripped != ''):
            break
        if stripped.endswith(':') and stripped.startswith('  ') and not stripped.startswith('    '):
            name = stripped.strip().rstrip(':')
            print(f'  Service: {name}')
" 2>/dev/null || grep -E '^\s{2}\w+:' "$f" | grep -v '^\s{4}' | sed 's/://;s/^\s*/  Service: /'
done

# Dockerfiles (each usually = one service)
find . -maxdepth 4 \( -name "Dockerfile" -o -name "Dockerfile.*" -o -name "*.Dockerfile" \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null | while read f; do
  DIR=$(dirname "$f")
  BASE=$(head -5 "$f" | grep -oP '(?<=FROM )\S+' | head -1)
  echo "Dockerfile: $f (base: ${BASE:-unknown}) — dir: $DIR"
done
```

#### Kubernetes Manifests
```bash
# K8s Deployments, StatefulSets, Services, CronJobs
find . -maxdepth 5 -name "*.yaml" -o -name "*.yml" | \
  xargs grep -l "kind:\s*\(Deployment\|StatefulSet\|Service\|CronJob\|DaemonSet\|Job\)" 2>/dev/null | \
  grep -v node_modules | while read f; do
  echo "=== $f ==="
  grep -E "^\s*(kind|name|namespace|image):" "$f" | head -10
done

# Helm charts
find . -maxdepth 4 -name "Chart.yaml" -not -path '*/node_modules/*' 2>/dev/null | while read f; do
  echo "=== Helm Chart: $f ==="
  grep -E "^(name|version|description|appVersion):" "$f"
done
```

#### Application Configs
```bash
# Node.js services (package.json with a start script)
find . -maxdepth 3 -name "package.json" -not -path '*/node_modules/*' 2>/dev/null | while read f; do
  HAS_START=$(python3 -c "import json; d=json.load(open('$f')); print('yes' if 'start' in d.get('scripts',{}) else 'no')" 2>/dev/null)
  if [ "$HAS_START" = "yes" ]; then
    NAME=$(python3 -c "import json; print(json.load(open('$f')).get('name','unknown'))" 2>/dev/null)
    echo "Node service: $NAME ($f)"
  fi
done

# Python services (with main entry point)
find . -maxdepth 3 -name "pyproject.toml" -not -path '*/vendor/*' 2>/dev/null | while read f; do
  DIR=$(dirname "$f")
  echo "Python project: $f"
  grep -E "^(name|version)" "$f" | head -2
done

# Go services
find . -maxdepth 3 -name "go.mod" 2>/dev/null | while read f; do
  MODULE=$(head -1 "$f" | awk '{print $2}')
  echo "Go module: $MODULE ($f)"
done

# Procfile (Heroku/Dokku)
find . -maxdepth 3 -name "Procfile" 2>/dev/null | while read f; do
  echo "=== Procfile: $f ==="
  cat "$f"
done

# Systemd units
find . -maxdepth 4 -name "*.service" -not -path '*/.git/*' 2>/dev/null | while read f; do
  echo "Systemd unit: $f"
  grep -E "^(Description|ExecStart|After|Requires)=" "$f" 2>/dev/null
done
```

#### CI/CD Pipelines (reveal deployed services)
```bash
# GitHub Actions deploy workflows
find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null | \
  xargs grep -l "deploy" 2>/dev/null | while read f; do
  echo "Deploy workflow: $f"
  grep -E "^\s*(name|runs-on|env):" "$f" | head -5
done

# GitLab CI deploy stages
grep -A5 "deploy" .gitlab-ci.yml 2>/dev/null | head -20
```

### 2. `catalog` — Generate Service Catalog

After discovery, compile into a structured catalog. For each service, extract:

- **Name**: Service identifier
- **Type**: API, worker, cron job, database, cache, queue, frontend, gateway
- **Tech stack**: Language, framework, runtime
- **Port**: Exposed port(s)
- **Dependencies**: Other services it connects to (from env vars, config, imports)
- **Owner**: From CODEOWNERS, package.json author, git blame
- **Repository**: Git remote URL
- **Health endpoint**: /health, /healthz, /ready, /status
- **Documentation**: README, wiki links

```bash
# Detect service dependencies from env vars and config
rg -n "(DATABASE_URL|REDIS_URL|RABBITMQ_URL|KAFKA_BROKERS|MONGO_URI|API_URL|SERVICE_URL)" \
  -g '!node_modules' -g '!vendor' -g '!dist' --type-not binary 2>/dev/null

# Detect inter-service communication
rg -n "(fetch|axios|http\.get|requests\.get|grpc|amqp|redis)" \
  -g '!node_modules' -g '!vendor' -g '!dist' -g '!*.test.*' -g '!*.spec.*' --type-not binary 2>/dev/null | \
  grep -oP 'https?://[a-zA-Z0-9._/-]+' | sort -u

# Check for CODEOWNERS
cat CODEOWNERS .github/CODEOWNERS docs/CODEOWNERS 2>/dev/null

# Check for health endpoints
rg -n "(\/health|\/healthz|\/ready|\/status|\/ping)" \
  -g '!node_modules' -g '!vendor' --type-not binary 2>/dev/null | head -20
```

Output a catalog document:

```markdown
# Service Catalog
Generated: [date] | Services: N | Owners: N teams

## Services

### api-gateway
- **Type:** API Gateway
- **Stack:** Node.js 20, Express
- **Port:** 3000
- **Owner:** @platform-team
- **Dependencies:** auth-service, user-service, redis
- **Health:** GET /health
- **Repo:** github.com/org/api-gateway
- **Docs:** docs/api-gateway.md

### user-service
...
```

### 3. `deps` — Dependency Graph

Map service-to-service dependencies:

```
api-gateway → auth-service → postgres
api-gateway → user-service → postgres, redis
api-gateway → notification-service → redis, smtp
worker → queue (rabbitmq) → notification-service
frontend → api-gateway
```

Detect:
- **Circular dependencies**: A → B → C → A
- **Single points of failure**: Service depended on by >3 others with no redundancy
- **Missing health checks**: Services without /health endpoints
- **Orphaned services**: Defined in config but not referenced by any other service

### 4. `health` — Check Service Health

For services with known health endpoints or docker containers:

```bash
# Check local docker containers
docker ps --format "{{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null

# Check systemd services
systemctl list-units --type=service --state=running 2>/dev/null | grep -v systemd

# Ping health endpoints
for endpoint in $(rg -o "https?://localhost:[0-9]+/(health|healthz|ready|status)" -g '*.{yml,yaml,json,env}' 2>/dev/null | sort -u); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 3 "$endpoint" 2>/dev/null)
  echo "$endpoint → $STATUS"
done
```

### 5. `owners` — Ownership Report

Map services to teams/individuals:

```bash
# From CODEOWNERS
cat CODEOWNERS .github/CODEOWNERS 2>/dev/null | grep -v '^#' | grep -v '^$'

# From package.json author/maintainers
find . -maxdepth 3 -name "package.json" -not -path '*/node_modules/*' 2>/dev/null | while read f; do
  python3 -c "
import json
d = json.load(open('$f'))
name = d.get('name', 'unknown')
author = d.get('author', 'unassigned')
if isinstance(author, dict): author = author.get('name', 'unassigned')
print(f'{name}: {author}')
" 2>/dev/null
done

# From git blame (most active contributor per directory)
find . -maxdepth 2 -type d -not -path '*/.git*' -not -path '*/node_modules*' | while read d; do
  TOP=$(git log --since="90 days ago" --format="%an" -- "$d" 2>/dev/null | sort | uniq -c | sort -rn | head -1)
  if [ -n "$TOP" ]; then
    echo "$d: $TOP"
  fi
done 2>/dev/null
```

Report unowned services as risks.

### 6. `drift` — Detect Catalog Drift

Compare the generated catalog against a previously saved one (`.service-catalog.json`):

- New services added (not in catalog)
- Services removed (in catalog but no longer found)
- Configuration changes (ports, dependencies, tech stack)
- Ownership changes

Run in CI to catch undocumented infrastructure changes.

## Output Formats

- **text** (default): Human-readable report with sections per service
- **json**: Machine-readable `{services: [{name, type, stack, port, deps, owner, health, repo}], graph: {edges: []}}`
- **markdown**: Wiki-ready document with tables and dependency diagram (Mermaid)
- **mermaid**: Pure Mermaid diagram of service dependencies

## Notes

- Works on monorepos and multi-repo setups (scan from repo root or organization root)
- Does not require running services — discovers from config files and code
- For live service health, services must be reachable from the scan environment
- Ownership detection is heuristic (CODEOWNERS > package.json > git blame) — review and correct
- Save catalog as `.service-catalog.json` to enable drift detection
- Works alongside internal developer portal tools (Backstage, Port, Cortex) as a lightweight alternative or seed data source
