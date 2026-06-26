# Security Analyst Plugins

Framework and infrastructure-specific security checks that are automatically loaded when the target project uses a matching technology.

## How Plugins Work

1. After the recon agent maps the codebase, the orchestrator scans this directory for `*.md` files (excluding this README)
2. Each plugin's `detect` frontmatter is checked against the recon step files and project files
3. Matching plugins have their agent-specific sections extracted and appended to the relevant agent prompts via the `{PLUGIN_CHECKS}` placeholder
4. Agents receive only the plugin sections relevant to their focus area

## Plugin File Format

Each plugin is a single markdown file with YAML frontmatter and sections keyed by agent name.

### Frontmatter Schema

```yaml
---
name: "Human-readable plugin name"
detect:
  files: ["list", "of", "filenames"]         # Match if ANY file exists in the project root
  dependencies: ["package-a", "package-b"]    # Match if ANY dependency appears in step-13-dependencies.md
  keywords: ["Framework", "Platform"]         # Match if ANY keyword appears in step-01-metadata.md
---
```

A plugin matches if **any single** detection criterion hits across any of the three lists. This means a project using Firebase will match even if only `firebase.json` exists.

### Detection Fields

| Field | What It Checks | Example |
|-------|---------------|---------|
| `detect.files` | File existence via Glob in project root | `["firebase.json", ".firebaserc", "firestore.rules"]` |
| `detect.dependencies` | Package names in `step-13-dependencies.md` | `["firebase-admin", "firebase-functions"]` |
| `detect.keywords` | Strings in `step-01-metadata.md` (Framework, Infrastructure, Runtime fields) | `["Firebase", "Cloud Functions"]` |

### Agent Sections

After the frontmatter, add `## {agent-name}` sections for each agent you want to extend. The section name **must** match the agent prompt filename without the `.md` extension.

Available agent section names:

| Section Name | Agent | What to Add |
|-------------|-------|------------|
| `recon-agent` | Reconnaissance | Additional discovery steps (file patterns, config locations) |
| `attack-surface-http` | HTTP Entry Points | Framework-specific endpoint patterns, middleware quirks |
| `attack-surface-authz` | Authorization Rules | Framework-specific access control analysis |
| `attack-surface-frontend` | Frontend & Client-Side | Framework-specific XSS patterns, client-side security |
| `attack-surface-llm` | LLM/AI Security | Framework-specific AI integration patterns |
| `attack-surface-integrations` | External Integrations | Framework-specific API client patterns |
| `git-history-injections` | Injection Variants | Framework-specific injection patterns to hunt |
| `git-history-auth-bypass` | Auth Bypass Variants | Framework-specific auth bypass patterns |
| `git-history-ssrf` | SSRF Variants | Framework-specific SSRF patterns |
| `git-history-data-exposure` | Data Exposure Variants | Framework-specific data leak patterns |
| `logic-race-conditions` | Race Conditions | Framework-specific concurrency patterns |
| `logic-authz-escalation` | Privilege Escalation | Framework-specific privilege escalation vectors |
| `logic-pipeline-exploit` | Pipeline Exploitation | Framework-specific pipeline logic flaws |
| `logic-dos` | Denial of Service | Framework-specific resource limits and amplification |
| `data-flow-tracer` | Data Flow Tracing | Framework-specific data flow patterns |
| `dependency-audit` | Dependency Audit | Framework-specific dependency concerns |
| `config-infrastructure` | Infrastructure Config | Framework-specific configuration security |

Only include sections where you have framework-specific checks to add. Omitted sections are silently skipped.

## Creating a New Plugin

1. Create a new `.md` file in this directory (e.g., `spring-boot.md`)
2. Add frontmatter with `name`, and at least one `detect` criterion
3. Add `## {agent-name}` sections with framework-specific checks
4. Each section should contain actionable security checks in the same style as the base agent prompts:
   - Offensive framing ("Can an attacker...")
   - Specific code patterns to search for
   - Concrete exploit scenarios
   - Framework-specific gotchas and defaults
5. Keep checks focused on what's **unique** to the framework — don't repeat generic checks already in the base agent prompts

## Plugin Overlap and Conflicts

When multiple plugins inject sections for the same agent (e.g., both Next.js and React inject `## attack-surface-frontend`), the orchestrator concatenates all matching sections. Agents should:

- Treat multiple plugin sections as **complementary** checks — run all of them
- If checks conflict, prefer the **more specific** plugin (e.g., Next.js over React for Next.js projects)
- Report the plugin source in findings so the orchestrator can trace which plugin triggered the check

## Available Plugins

| Plugin | Framework/Platform | Sections |
|--------|-------------------|----------|
| `firebase.md` | Firebase / Firestore / Cloud Functions | HTTP, AuthZ, Frontend, Config, Dependency Audit, Race Conditions, DoS |
| `react.md` | React / React Native | Frontend |
| `nextjs.md` | Next.js | HTTP, Frontend, Config |
| `nodejs-express.md` | Node.js + Express | HTTP, Config |
| `python-fastapi.md` | Python + FastAPI | HTTP, Config |
| `python-django.md` | Python + Django | HTTP, AuthZ, Config |
| `secrets-encryption-storage.md` | Database Secrets Encryption | Recon, AuthZ, Config, Data Flow, Race Conditions, Data Exposure History, Dependency Audit |
| `solidjs.md` | SolidJS / SolidStart | Frontend, HTTP, Config, Dependency Audit |
| `owasp-infra-top10.md` | OWASP Top 10 Infrastructure Security Risks | Recon, HTTP, AuthZ, Config, Data Flow, DoS, Race Conditions, Data Exposure History, Dependency Audit |
| `spring-boot.md` | Spring Boot (Java) | Recon, HTTP, AuthZ, Config, Dependency Audit |
| `ruby-rails.md` | Ruby on Rails | Recon, HTTP, AuthZ, Config, Dependency Audit |
| `vuejs-nuxtjs.md` | Vue.js / Nuxt.js | Frontend, HTTP, Config, Dependency Audit |
| `angular.md` | Angular | Frontend, Config, Dependency Audit |
| `go-gin.md` | Go (Gin / Echo / Fiber) | HTTP, AuthZ, Config, DoS, Dependency Audit |
| `graphql.md` | GraphQL (Apollo, Yoga, etc.) | Recon, HTTP, AuthZ, Config, Data Flow, DoS |
| `docker-kubernetes.md` | Docker / Kubernetes | Recon, Config, Dependency Audit |
| `aws-gcp-azure.md` | AWS / GCP / Azure Cloud | Recon, HTTP, Config, Data Flow, Dependency Audit |
