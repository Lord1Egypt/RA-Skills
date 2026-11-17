---
name: ci-tools-pipeline
description: Build and maintain GitLab CI/CD pipelines with the CI Tools Components Catalog at ci-tools.xrow.de. Use when creating or fixing .gitlab-ci.yml files, choosing CI Tools components, validating component inputs, or designing continuous delivery pipelines for applications, Helm charts, containers, packages, documentation, infrastructure, and GitOps.
metadata: { "openclaw": { "requires": { "bins": ["glab", "curl", "jq"] }, "primaryEnv": "GITLAB_TOKEN" } }
---
# CI Tools Pipeline Skill

Use this skill to build proper GitLab CI/CD pipelines from the CI Tools Components Catalog.
Prefer catalog components over custom jobs when a component exists for the job type.

## Quick Start

1. Read the project `AGENTS.md` first, then inspect the repository layout, current `.gitlab-ci.yml`, and existing pipeline failures.
2. Open the live catalog before choosing components:
   - Catalog: `https://ci-tools.xrow.de/`
   - Components index: `https://ci-tools.xrow.de/Components/`
   - Source: `https://gitlab.com/xrow-public/ci-tools`
3. Select the smallest component set that covers the project:
   - Baseline: `common`, `workflow`, `semantic-release`
   - Hygiene: `label`, `pre-commit`, `spellcheck`, `trivy`
   - Languages and test runners: `bash-unit-tests`, `lint-javascript`, `lint-json`, `lint-yaml`, `lint-markdown`, `lint-ansible`, `lint-helm`, `lint-tofu`
   - Build and package: `container`, `buildah`, `helm`, `helm-docs`, `package`, `package-skill`, `oras-push`
   - Docs and sites: `docusaurus`, `publish-sitemap`, `publish-wiki`
   - Delivery: `deploy-helm`, `deploy-argocd`, `gitops`, `app-of-apps`
   - Project flow: `workflow-trunkbased`, `workflow-gitflow`
4. Validate locally before pushing:
   - `glab ci lint .gitlab-ci.yml`
   - Lint any included template files when supported by the project.
   - Run the narrowest local test for scripts or generated configuration.

## Pipeline Design

- Keep root pipelines component-driven. Add handwritten jobs only when no component exists or a project-specific integration is unavoidable.
- Use `$CI_SERVER_FQDN/xrow-public/ci-tools/<component>@main` for component includes when package registry or fully-qualified host behavior matters; otherwise match the existing project style.
- Put component `inputs` next to the include and keep names stable across related jobs.
- Prefer continuous delivery defaults. Do not create automatic production deployment unless the project already does that or the issue explicitly asks for it.
- Keep validation jobs independent of deployment jobs so a project can fail fast before writing to registries, clusters, or external systems.
- Use `needs` and `dependencies` only when a real artifact or ordering relationship exists.
- Never use `allow_failure: true`, `when: manual`, `rules: when: never`, or skipped tests to hide a broken required pipeline. Use them only when the job is genuinely optional, documented, or intentionally gated.

## Component Selection Heuristics

### Repository Bootstrap

Use these components for most repositories:

```yaml
include:
  - component: $CI_SERVER_HOST/xrow-public/ci-tools/common@main
  - component: $CI_SERVER_HOST/xrow-public/ci-tools/label@main
  - component: $CI_SERVER_HOST/xrow-public/ci-tools/pre-commit@main
  - component: $CI_SERVER_HOST/xrow-public/ci-tools/trivy@main
  - component: $CI_SERVER_HOST/xrow-public/ci-tools/workflow@main
  - component: $CI_SERVER_HOST/xrow-public/ci-tools/semantic-release@main
```

Use `label` early when the project needs standard `priority::*`, `size::*`, `type::*`, and `workflow::*` labels for automation.

### Containers

Use `container` for normal application images and `buildah` when the project needs direct image build control.
Set `name` and `path` explicitly when the repository has multiple build roots.

```yaml
include:
  - component: $CI_SERVER_HOST/xrow-public/ci-tools/container@main
    inputs:
      name: app
      path: container/app
```

### Helm Charts

Use `helm` for chart build/test/publish flows and add `helm-docs` when chart documentation must be generated.
Set `test-enabled: false` only when there is no safe cluster-backed test path.

```yaml
include:
  - component: $CI_SERVER_HOST/xrow-public/ci-tools/helm@main
    inputs:
      name: chart
      path: chart
```

### Review Testing

Keep review environments close to production while making destructive checks explicit and temporary.
For Helm review tests, validate install, upgrade, readiness, ingress, cleanup, and storage behavior through chart values instead of ad hoc shell overrides.
Document any review-only threshold or fixture in the MR so reviewers can see why it differs from production defaults.

### Documentation

Use `docusaurus` for docs sites and pair it with `publish-sitemap` when the project publishes public pages.
Pass `name` and `path` explicitly.

### Infrastructure and GitOps

Use `lint-ansible`, `ansible-collection`, `ansible-ee`, `ansible-runner`, `lint-tofu`, `tofu-module`, `gitops`, `deploy-argocd`, and `app-of-apps` according to the repository type.
Keep plan, build, and deploy stages separate unless the catalog component documents a tighter flow.

## Validation Workflow

1. Fetch the live component page and verify the input names before editing:

   ```bash
   curl -fsSL https://ci-tools.xrow.de/Components/<component> | sed -n '1,220p'
   ```

2. Lint the pipeline:

   ```bash
   glab ci lint .gitlab-ci.yml
   ```

3. For merge requests, push with CI skipped first, then start an MR pipeline through GitLab Agent rules:

   ```bash
   git push origin <branch> -o ci.skip
   glab ci run --mr
   ```

4. If CI fails, inspect the failed job trace and fix the underlying problem. If the failure comes from the catalog or main branch, open or link the dependency and mark the MR blocked rather than weakening the pipeline.

## Review Checklist

- The pipeline uses CI Tools components where available.
- Component inputs match the live catalog documentation.
- Protected branch behavior is respected.
- Required checks are not hidden behind skips or `allow_failure`.
- Registry, cluster, and deploy writes are gated by existing project rules.
- The MR description lists the plan, acceptance criteria, and validation commands.
