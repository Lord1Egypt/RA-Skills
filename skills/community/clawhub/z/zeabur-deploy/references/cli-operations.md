# CLI operations and observed pitfalls

CLI help verified on 2026-10-20 with CLI **0.22.2**. Examples are command shapes,
not permission to run mutations. `version` is a subcommand; `--version` failed
in this version. Prefer an existing official binary; `npx --yes zeabur@latest`
is the verified fallback. If using an installed `zeabur` binary, replace the
`npx --yes zeabur@latest` prefix in examples with that binary. Inspect help and record the version again on future
runs. Use browser login when needed; never include authentication tokens in
committed examples or shell history.

## Discover without changing context

```sh
umask 077
ZB_PRIVATE_DIR=$(mktemp -d "${TMPDIR:-/tmp}/zeabur-deploy.XXXXXX")
npx --yes zeabur@latest version
npx --yes zeabur@latest workspace current > "$ZB_PRIVATE_DIR/workspace.txt" 2>&1
npx --yes zeabur@latest project list --json > "$ZB_PRIVATE_DIR/projects.json" 2>&1
npx --yes zeabur@latest server list --json > "$ZB_PRIVATE_DIR/servers.json" 2>&1
npx --yes zeabur@latest service list --help
npx --yes zeabur@latest deploy --help
```

Team operations support a one-shot global `--workspace <name-or-id>` override.
Prefer that to changing persistent workspace/context in a shared environment.
Project/service names alone are ambiguous. Inspect a resource's returned project,
environment and server before reusing it. Treat JSON exports as potentially
secret-bearing, even if the command only reads state. Inspect files privately;
report only explicitly selected ID/name/status fields after checking the response
shape. Do not paste whole objects, environment maps or logs into tool output.

## First deployment versus update

The following shell variables are placeholders resolved from live inventory or
the user's contract, not hardcoded defaults:
`ZB_PROJECT_ID`, `ZB_ENV_ID`, `ZB_API_ID`, `ZB_SERVER_ID`, `ZB_SOURCE_ROOT`,
`ZB_PRIVATE_DIR`, `ZB_PROJECT_NAME`, `ZB_SERVICE_NAME`, `ZB_DOMAIN_LABEL`.
Do not run a block until all its required values have been checked. Prepare
`ZB_PRIVATE_DIR` as a dedicated ignored directory with mode 0700 and set
`umask 077` before capturing outputs; do not reuse an unrelated shared directory.
Redirect every mutation's stdout/stderr there and inspect only redacted status.

For an approved first deployment on an existing dedicated server, a prior
deployment used region `server-<server-id>`. Reconfirm placement with current
server/project help and the returned project before deploying dependencies.

```sh
npx --yes zeabur@latest project create \
  --name "$ZB_PROJECT_NAME" --region "server-$ZB_SERVER_ID" \
  --interactive=false --json > "$ZB_PRIVATE_DIR/project-create.json" 2>&1
npx --yes zeabur@latest template deploy \
  --file "$ZB_PRIVATE_DIR/mysql-template.yaml" --project-id "$ZB_PROJECT_ID" \
  --interactive=false --json > "$ZB_PRIVATE_DIR/mysql-deploy.json" 2>&1
```

Template deployment can create additional services and is not a generic retry
for an existing database. Do not rerun it after an ambiguous response until live
inventory establishes whether creation succeeded. Use a reviewed template based
on the current official schema, with a persistent database volume and no public
forwarding. Keep rendered credentials local and private.

Run local uploads **from the service source directory**, not a monorepo root:

```sh
cd "$ZB_SOURCE_ROOT"
# First deployment only:
npx --yes zeabur@latest deploy --create --project-id "$ZB_PROJECT_ID" \
  --name "$ZB_SERVICE_NAME" --interactive=false --json \
  > "$ZB_PRIVATE_DIR/api-create.json" 2>&1
# Subsequent source upload to the existing service/environment:
npx --yes zeabur@latest deploy --project-id "$ZB_PROJECT_ID" \
  --service-id "$ZB_API_ID" --environment-id "$ZB_ENV_ID" \
  --interactive=false --json > "$ZB_PRIVATE_DIR/api-upload.json" 2>&1
```

Any unknown result or timeout, for creation **or update**, requires checking live
inventory/deployment metadata before retry. Confirm the returned deployment maps
to the intended source revision; health success can belong to an older binary.

Choose one route: for a service sourced from Git, use the verified Git source,
branch, build root and deployment mechanism instead of silently changing its
source to a CLI upload. A GitHub push alone does not prove a Zeabur deployment.
`service restart` restarts the runtime; do not describe it as uploading new code.

## Variables, networking and diagnostics

`variable env --help` says **overwrite variables from a .env file**. Before an
update, privately preserve the current environment and merge only intended
changes. Do not apply a minimal example file that drops unrelated required vars.
The command's output may contain the values: redirect stdout and stderr to a
protected local file, then report only redacted status.

```sh
npx --yes zeabur@latest variable env --id "$ZB_API_ID" --env-id "$ZB_ENV_ID" \
  --file "$ZB_PRIVATE_DIR/api.env" --interactive=false --json \
  > "$ZB_PRIVATE_DIR/variable-result.json" 2>&1
npx --yes zeabur@latest service restart --id "$ZB_API_ID" \
  --env-id "$ZB_ENV_ID" --interactive=false --json \
  > "$ZB_PRIVATE_DIR/api-restart.json" 2>&1
npx --yes zeabur@latest domain list --id "$ZB_API_ID" --env-id "$ZB_ENV_ID" --json \
  > "$ZB_PRIVATE_DIR/domain-list.json" 2>&1
# Only if an approved API endpoint is not already provisioned:
npx --yes zeabur@latest domain create --id "$ZB_API_ID" --env-id "$ZB_ENV_ID" \
  --generated --domain "$ZB_DOMAIN_LABEL" --yes --interactive=false --json \
  > "$ZB_PRIVATE_DIR/domain-create.json" 2>&1
npx --yes zeabur@latest deployment get --service-id "$ZB_API_ID" \
  --env-id "$ZB_ENV_ID" --json > "$ZB_PRIVATE_DIR/deployment.json" 2>&1
npx --yes zeabur@latest deployment log -t=runtime --service-id "$ZB_API_ID" \
  --env-id "$ZB_ENV_ID" --json > "$ZB_PRIVATE_DIR/runtime-log.json" 2>&1
npx --yes zeabur@latest service network --id "$ZB_DB_ID" --env-id "$ZB_ENV_ID" --json \
  > "$ZB_PRIVATE_DIR/database-network.json" 2>&1
```

`ZB_DB_ID` is the separately verified database service ID. Read commands can
still emit secrets in configuration or logs; capture privately before sharing.
Confirm the database has **no public TCP port forwarding**. Private hostnames
must come from current platform metadata; do not guess from another deployment.
Use the actual returned public hostname. A regional platform may append a suffix
different from a generic example. Do not turn a provisioning timeout into a
purchase, custom-domain registration or TLS exception.

## Authoritative references

- [Official CLI](https://zeabur.com/docs/en-US/developer/cli)
- [Template schema](https://zeabur.com/docs/en-US/template/template-format)
- [Private networking](https://zeabur.com/docs/en-US/deploy/networking/private-networking)
- [Git service root directory](https://zeabur.com/docs/en-US/deploy/config/root-directory)

The command flags above were checked against local CLI help; the dedicated-server
region form and configuration-before-restart incident are observed experience,
not a promise that every future account/CLI behaves identically.
