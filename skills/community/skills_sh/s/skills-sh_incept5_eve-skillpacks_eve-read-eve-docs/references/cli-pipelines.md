# CLI: Builds, Releases, Pipelines, Workflows

## Use When
- You need to run, inspect, or debug pipeline-driven build/release/deploy flows.
- You need deterministic artifact promotion and release lookup.
- You need workflow automation for reusable multi-step invocation.

## Load Next
- `references/builds-releases.md` for artifact/data model.
- `references/pipelines-workflows.md` for manifest-level pipeline definitions.
- `references/deploy-debug.md` when run failures block deployment.

## Ask If Missing
- Confirm whether behavior is pipeline-driven or direct deploy.
- Confirm target environment, project, and required input payload.
- Confirm whether release tags are required vs `--ref`/`--repo-dir`.

## Builds

Builds are first-class primitives tracking container image construction. See `references/builds-releases.md`.

```bash
eve build list [--project <id>]                         # List build specs
eve build show [--project <id>] [--json]                # Build spec details
eve build create --project <id> --ref <sha>             # Create a build spec
  --manifest-hash <hash>
  [--services <list>] [--repo-dir <path>]
eve build run <build_id>                                # Start a build run
eve build runs <build_id>                               # List runs for a build
eve build logs <build_id> [--run <id>]                  # View build logs
eve build artifacts <build_id>                          # List image artifacts (digests)
eve build diagnose <build_id>                           # Full diagnostic dump
eve build cancel <build_id>                             # Cancel active build
```

Builds happen automatically in pipeline `build` steps. Use `eve build diagnose` to debug failures.

## Releases

```bash
eve release resolve <tag> [--project <id>]              # Resolve release by tag
```

Releases are created automatically by pipeline `release` steps. See `references/builds-releases.md`.

## Pipelines

Pipeline run statuses: `pending`, `running`, `succeeded`, `failed`, `cancelled`, `awaiting_approval`.
Step types: `build`, `release`, `deploy`, `run`, `job`.

For services with managed DB state, include a migration step as a pipeline `job` before `deploy`:

```bash
eve pipeline run deploy-sandbox --env sandbox --ref main
```

Manifest example:

```yaml
pipelines:
  deploy-sandbox:
    steps:
      - name: migrate
        action: { type: job, service: migrate }
      - name: release
        depends_on: [migrate]
        action: { type: release }
      - name: deploy
        depends_on: [release]
        action: { type: deploy, env_name: sandbox }
```

```bash
eve pipeline list [--project <id>]
eve pipeline show <project> <name>
eve pipeline run <name> --ref <sha-or-branch>
  [--env staging] [--inputs '{"k":"v"}']
  [--repo-dir ./my-app]
eve pipeline runs [project] [--status <status>]
eve pipeline show-run <pipeline> <run-id>
eve pipeline approve <run-id>
eve pipeline cancel <run-id>
eve pipeline logs <pipeline> <run-id> --step <name>
```

## Workflows

```bash
eve workflow list [--project <id>]
eve workflow show <project> <name>
eve workflow run [project] <name> --input '{"k":"v"}' --env-override KEY=VALUE   # Start async
eve workflow invoke [project] <name> --input '{"k":"v"}' --env-override KEY=VALUE  # Start and poll
  [--no-wait]                                           # Return immediately
eve workflow retry <root-job-id> --failed                # Retry failed/upstream-failed tail
eve workflow retry <root-job-id> --from <step-name>      # Retry named step + downstream tail
eve workflow logs <job-id> [--attempt <n>] [--after <cursor>]
```
