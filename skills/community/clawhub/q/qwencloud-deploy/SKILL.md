---
name: qwencloud-deploy
version: "2.2"
description: >-
  One-click deploy, publish, and update a local project or Git repository to Alibaba Cloud
  International (alibabacloud.com), producing an accessible online service with a public IP.
  Supports full-stack ROS orchestration, automatic cloud-resource provisioning, pre-deployment
  price confirmation, service health checks, deployment-state recording, hot updates, and
  optional domain + HTTPS setup.
  Use when: the user asks to deploy a project to the cloud, put an app online, publish a
  website, generate an access URL, deploy a Git repo, or update an online version and has NOT
  named a specific cloud platform; or the user mentions "Alibaba Cloud", "alibabacloud.com",
  or the international site.
  Do not use when: the user explicitly targets Aliyun China (aliyun.com), AWS, GCP, Azure, or
  another specific cloud platform.
trigger: >-
  Use when the user asks to deploy a project to the cloud, put an app online, publish a website,
  generate an access URL, deploy a Git repo, or update an online version — and has NOT specified
  a particular cloud platform. Also use when the user mentions "Alibaba Cloud", "alibabacloud.com",
  or the international site.
skip: >-
  Do NOT use when the user explicitly targets Aliyun China (aliyun.com), AWS, GCP, Azure,
  or another specific cloud platform.
prerequisites:
  - aliyun CLI 3.x configured with international-site credentials in OAuth mode
input: >-
  A local project directory, Git URL, or an existing deployment state file (.qwencloud-deploy).
  Optional: user preferences for instance type, region, database.
output: >-
  A running cloud service with public IP (or domain + HTTPS), deployment state file
  (.qwencloud-deploy), and success card with access URL, cost summary, and next-step guidance.
---

# Qwen Cloud Deploy

## Quick Path

1. **Route the task** — Match to one of 4 modes: Full-Stack Deploy · Hot Update · Delete · HTTPS Setup.
2. **Deploy (default)** — Execute steps 1→14 strictly in order, no skipping/reordering; gates and
   skippable steps are in `reference/rules/rule_interaction.md` "Execution order".
3. **Confirm cost before creating anything** — Show hourly price in USD, get user confirmation.
4. **Record state** — On success write `.qwencloud-deploy`.

## Scope

| In Scope | Out of Scope |
|----------|--------------|
| Local project / Git → Alibaba Cloud International | China site → use `qianwenai-deploy` |
| Full-stack ROS, hot update, cleanup | AWS/GCP/Azure/other clouds |
| ECS + optional RDS + OSS + public IP | K8s/Serverless/container orchestration |
| OAuth/AK auth (no credential collection) | — |
| Deploy the user's provided code/project | Reviewing or editing the user's code logic, vouching for code correctness |

## About the user's code

This skill builds and deploys the user's provided code/project. It does not review or modify the
business logic and does not guarantee the code itself is correct.

Bugs, security issues, and any consequences caused by the code once deployed are the user's own; if
the code needs changing, the user decides and makes the change themselves.

## Assumptions

- `aliyun` CLI 3.x installed; when no valid credential, follow `reference/deploy/01_env_check.md`.
- Default region `ap-southeast-1` (Singapore).

---

## Task Routing

| Signal | Mode |
|--------|------|
| `.qwencloud-deploy` exists + user says "update" | **Hot Update** |
| `.qwencloud-deploy` exists + "delete"/"cleanup" | **Delete** |
| "bind domain"/"HTTPS"/"SSL" (deployment exists) | **HTTPS Setup** |
| Git URL or local project (no existing deployment) | **Full-Stack Deploy** |

On trigger, display welcome message first (see `reference/rules/rule_interaction.md`).

---

## Full-Stack Deploy (Steps 1–14)

### Phase 1 · Preparation

| Step | Action | Reference |
|------|--------|-----------|
| 1 | Environment check | `reference/deploy/01_env_check.md` |
| 2 | Git clone (if Git URL) | `reference/deploy/02_git_clone.md` |
| 3 | Project analysis | `reference/deploy/03_analyze_project.md` |

### Phase 2 · Resource Planning

| Step | Action | Reference |
|------|--------|-----------|
| 4 | Existing deployment scan | `reference/deploy/04_check_existing.md` |
| 5 | Database identification | `reference/deploy/05_database.md` |
| 6 | ECS instance type selection | `reference/deploy/06_instance_type.md` |
| 7 | Generate ROS template | `reference/deploy/07_generate_template.md` |
| 8 | Stock check | `reference/deploy/08_check_stock.md` |
| 9 | Template validation + cost estimate | `reference/deploy/09_estimate_cost.md` |

### Phase 3 · Execution

| Step | Action | Reference |
|------|--------|-----------|
| 10 | Upload artifacts + regenerate template | `reference/deploy/10_upload_artifacts.md` |
| 11 | Create stack | `reference/deploy/11_create_stack.md` |
| 12 | Wait for terminal state + health check | `reference/deploy/12_wait_stack.md` |
| 13 | Record state | `reference/deploy/13_record_state.md` |
| 14 | Append application dossier | `reference/deploy/14_app_timeline.md` |

---

## Hot Update

**Trigger**: `.qwencloud-deploy` exists + user wants to update code. IP unchanged.

| Step | Action | Reference |
|------|--------|-----------|
| U1 | Build + upload new artifacts | `reference/deploy/10_upload_artifacts.md` |
| U2 | Deliver update (Cloud Assistant) | `reference/hotfix/update_app.md` |
| U3 | Health check + update state | `reference/hotfix/update_app.md` |
| U4 | Append application dossier (`event=hotfix`) | `reference/deploy/14_app_timeline.md` |

Update script template: `reference/hotfix/update_recipe.md`.

---

## Delete / Cleanup

**Trigger**: User says "delete", "cleanup", "release resources".

> ⚠️ Irreversible — confirm twice. With RDS: warn about data loss.

> 🚫 Never manually delete individual resources — only use `delete_stack.sh`.

See `reference/cleanup/delete_stack.md`.

---

## HTTPS Setup (Optional)

**Trigger**: User says "bind domain" / "HTTPS" / "SSL" after deployment exists.

See `reference/https/https_setup.md`.

---

## Key Constraints

| Constraint | Rule |
|------------|------|
| Currency | Always USD |
| Auth | OAuth (recommended) or AK/SK; never collect credentials via chat |
| Template upload | Must use `--TemplateURL` (WAF blocks TemplateBody) |
| Stack name retry | Reuse — never regenerate |
| Resource deletion | Always via `delete_stack.sh` |
| Region default | `ap-southeast-1` |
| Commands to user | Never show underlying commands |

---

## File Layout

```
scripts/
  generate_template.py  upload_artifacts.py
  create_stack.sh       record_state.py
  delete_stack.sh       update_app.sh
  wait_and_probe.py     setup_domain.sh
  append_timeline.py
reference/
  deploy/
    01_env_check.md ~ 14_app_timeline.md
  hotfix/
    update_app.md       update_recipe.md
  cleanup/
    delete_stack.md
  https/
    https_setup.md
  rules/
    rule_interaction.md  rule_error_handling.md  ram_policies.md
templates/
  ros_single[_rds].yaml
  userdata/{systemd,docker,nginx_proxy,nginx_static,nginx_static_proxy}.sh
```
