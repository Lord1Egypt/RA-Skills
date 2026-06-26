# Reddit posts for Awesome OpenClaw Resources

Repo: https://github.com/SebConejo/awesome-openclaw-resources

Post one sub per day in this order.

---

## 1. r/openclaw

**Title:** I compiled 70+ open source tools, tutorials, and resources for OpenClaw into one list

**Body:**

Been digging through the ecosystem for a while and realized there was no single place listing everything worth knowing about. So I put one together.

It covers:

- Open source LLM routers (route requests to cheaper models automatically)
- Observability tools (track tokens, cost, latency per call)
- Hosting and deployment (Docker, K8s, one-click VPS setups)
- Security (guardrails, prompt injection defense, sandboxing)
- Skills and plugins
- Tutorials from beginner to advanced
- Podcasts including the Lex Fridman episode with Peter
- Content creators worth following

CC0 licensed, open to contributions. If your project or something you use is missing, open a PR.

https://github.com/SebConejo/awesome-openclaw-resources

---

## 2. r/LocalLLaMA

**Title:** Awesome list of open source tools for OpenClaw, focused on cost reduction and model routing

**Body:**

Put together a curated list of open source tools for people running OpenClaw. A big chunk of it is about solving the token burn problem.

The LLM routers section lists tools that sit between your agent and the provider and route each request to the cheapest model that can handle it. Some claim 70%+ savings by sending simple tasks to small models and reserving frontier models for what actually needs them.

There is also an observability section with dashboards that break down token usage and cost per call, so you can see where the money goes before trying to fix it.

The rest covers hosting (Docker, K8s, VPS), security, skills, tutorials, podcasts, and content creators.

Open source, CC0 licensed. PRs welcome if something is missing.

https://github.com/SebConejo/awesome-openclaw-resources

---

## 3. r/selfhosted

**Title:** Curated list of self-hosting tools for OpenClaw (Docker, K8s, VPS deployments, security)

**Body:**

If you are self-hosting OpenClaw or thinking about it, I put together an awesome list that has a dedicated hosting section.

What is in there:

- Docker setups (multiple options, including one with Chromium for browser skills)
- A Kubernetes operator with auto-updates, backup/restore, and Prometheus integration
- Hardened VPS deployment with Docker Compose, Caddy TLS, Redis, and automated S3 backups
- Security tools: prompt injection defense, sandboxed execution, config auditing

The list also covers LLM routers (route to cheaper models to cut API costs), observability dashboards, tutorials, and more.

Everything is open source. CC0 licensed. Contributions welcome.

https://github.com/SebConejo/awesome-openclaw-resources

---

## 4. r/ChatGPTCoding

**Title:** 70+ open source tools and resources for OpenClaw, organized by category

**Body:**

Compiled a list of everything useful I could find for OpenClaw. Figured other people building with it might save some time.

Categories: LLM routers (cheaper API calls by routing to the right model), observability (see where your tokens go), hosting (Docker/K8s/VPS), security, skills and plugins, tutorials, podcasts, and content creators.

All open source. If you know something that should be on the list, PRs are open.

https://github.com/SebConejo/awesome-openclaw-resources

---

## 5. r/artificial

**Title:** Curated list of 70+ open source tools and resources for the OpenClaw AI agent ecosystem

**Body:**

OpenClaw has grown fast and the ecosystem around it is getting hard to navigate. I put together an awesome list covering the main categories.

Open source LLM routers, observability dashboards, hosting platforms, security tools, skills and plugins, tutorials, podcasts, and content creators. Everything links to the source.

Open source and CC0 licensed. Contributions welcome via PR.

https://github.com/SebConejo/awesome-openclaw-resources

---

## 6. r/ClaudeAI

**Title:** Awesome list of open source tools for OpenClaw (the autonomous agent running on Claude)

**Body:**

Put together a curated list for people using OpenClaw. Since most setups run on Claude, figured this sub might find it useful.

The list covers LLM routers (route simple tasks to cheaper models, keep Claude for the hard stuff), observability (track token usage and cost), hosting, security, skills, tutorials, podcasts, and content creators.

One thing that might interest this sub specifically: the LLM routers section. A few of those tools let you automatically send simple requests to Haiku or Flash and reserve Opus/Sonnet for reasoning tasks. Cuts the bill without changing how the agent works.

Open source, CC0. PRs welcome.

https://github.com/SebConejo/awesome-openclaw-resources

---

## 7. r/LangChain

**Title:** Curated list of open source infrastructure tools for OpenClaw agents

**Body:**

If you are working with AI agents and curious about the OpenClaw ecosystem, I compiled an awesome list of open source tools.

Relevant to this sub: LLM routing (same concept as LangChain's model fallback but as standalone tools), observability with Langfuse integration, MCP adapters, and a reinforcement learning framework for agent personalization.

Full list covers hosting, security, skills, tutorials, podcasts, and more.

https://github.com/SebConejo/awesome-openclaw-resources

---

## 8. r/devops

**Title:** Open source deployment and infrastructure tools for OpenClaw (K8s operator, Docker, hardened VPS)

**Body:**

If anyone here is deploying OpenClaw in production, I compiled a list of open source infra tools that might save you some research.

Highlights for this sub:

- K8s operator with auto-updates, backup/restore, and Prometheus metrics
- Hardened VPS deployment (Docker Compose, Caddy TLS, Redis, S3 backups)
- Multiple Docker setups (auto-build, daily checks for new releases)
- Security: config auditing, sandboxed execution, prompt injection guardrails
- Observability dashboards with token and cost tracking

The full list also covers LLM routing, skills, tutorials, and more.

https://github.com/SebConejo/awesome-openclaw-resources
