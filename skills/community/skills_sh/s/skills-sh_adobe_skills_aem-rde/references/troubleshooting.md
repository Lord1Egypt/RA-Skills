# Troubleshooting reference

Map of error → likely cause → fix, plus exit-code semantics.

## Exit codes

The plugin sets these via the oclif error system:

| Code | Meaning | What to do |
|------|---------|-----------|
| 1 | Generic / uncaught | Look at stderr; usually wraps a deeper error. |
| 2 | Configuration | Org / program / env not set, IMS context missing. Run `aio aem rde setup --show`. |
| 3 | Validation | Bad flag / argument. Re-read the relevant `--help`. |
| 4 | Deployment | Install/delete failed server-side. Check `history <id>`. |
| 5 | Internal (retryable) | Transient — retry once or twice before digging deeper. |
| 40 | Deployment-not-fully-performed | Sometimes acceptable mid-pipeline (some steps OK, later step deferred). Inspect history. |

In CI, distinguish 5 (retry) from 4 (don't retry the same artifact, fix the build).

## Configuration errors

### "Missing org/program/environment"

Symptom: `MISSING_ORG_ID`, `MISSING_PROGRAM_ID`, `MISSING_ENVIRONMENT_ID`.
Cause: `cloudmanager_*` config keys not set, or you're in a directory whose `.aio` is empty.
Fix: `aio aem rde setup` (or set the keys with `aio config:set -l`).

### "No IMS context found. Please run `aio login` first."

Cause: token expired or never created.
Fix: `aio login` (browser flow) or, in CI, configure a service-account context.

### "The last RDE command ran more than 24h ago, do you want to continue running the command on cm-pXXXX-eYYYY?"

This is an interactive guard, not an error. It prevents accidental deploys against a stale config. Answer yes if the env is correct; otherwise rerun `setup`.

## Snapshot-specific errors

| Error code | HTTP | Meaning | Fix |
|------------|------|---------|-----|
| `NON_EAP` | 451 | Snapshot EAP not enabled for this customer | Contact account team / Adobe TAM. |
| `DIFFERENT_ENV_TYPE` | 400 | Target is not an RDE | Re-run `setup`, pick an actual RDE. |
| `PROGRAM_OR_ENVIRONMENT_NOT_FOUND` | 404 | Program/env IDs are wrong | `setup --show`, verify with Cloud Manager UI. |
| `SNAPSHOT_NOT_FOUND` | 404 | Snapshot name doesn't exist | `aio aem rde snapshot` to list names. Watch for typos / case. |
| `SNAPSHOT_DELETED` | 404 | Snapshot is in deleted state | `undelete` first, or pick a different snapshot. |
| `ALREADY_EXISTS` | 409 | Name collision | Pick a different name; snapshot names must be unique within env. |
| `INVALID_STATE` | 503 / 406 | Env busy or snapshot is mid-operation | Wait, check `status`. |
| `SNAPSHOT_LIMIT` | 507 | Quota reached | Delete an old snapshot first. |
| `SNAPSHOT_CREATION_FAILED` | (progress = -2) | Backend failed during create | Check logs around the time; re-run create. |
| `SNAPSHOT_CREATION_STUCK` | (no progress 15m) | Backend stalled | If stuck >1h, contact support; otherwise let it finish on its own and check `snapshot` listing later. |
| `SNAPSHOT_RESTORE_FAILED` | (progress = -2) | Backend failed during restore | Check `history`; consider `reset --force`. |
| `SNAPSHOT_WRONG_STATE` | 403 | Tried `delete --force` on a not-yet-removed snapshot | First soft-delete (`snapshot delete <name>`), then `--force` once it's in `removed`. |
| `DEPLOYMENT_IN_PROGRESS` | 503 | Another deploy is running | Wait, check `aio aem rde status` and `history`. |

## Install / delete errors

### `INVALID_GUESS_TYPE`

The plugin couldn't narrow `--type` to a single option. Usually a remote zip URL or an unusual file. Fix: pass `--type` explicitly. See `deployment-types.md` for the guess table.

### `MISSING_CONTENT_PATH`

For `content-file` / `content-xml`, no `--path` flag and the source isn't under `…/jcr_root/…`. Fix: pass `--path /path/in/jcr`.

### `UNSUPPORTED_PROTOCOL`

The location URL has a protocol other than `http`, `https`, or `file`. Fix: use one of the supported schemes.

### `DELETE_NOT_FOUND`

`aio aem rde delete <id>` matched nothing. The error message includes the type and target it searched. Fix: confirm BSN / PID via `aio aem rde status` or `aio aem rde inspect osgi-bundles` / `osgi-configurations`. BSN is case-sensitive.

### `INTERNAL_INSTALL_ERROR`

Generic wrapper around an upload/deploy failure. Use `aio aem rde history` to find the update id, then `history <id>` to see per-instance progress and which step failed.

### Content-package install reports success but JCR content never appears

Symptom: `aio aem rde install <ui.content.zip>` (or any container/all package) returns `deploy completed for content-package …`, `aio aem rde history` shows the update as completed with `No logs available`, but the targeted JCR paths (e.g. `/content/<site>`, `/conf/<site>`, `/apps/<site>`) all return 404 on author. OSGi bundles in the same deploy *do* land — only content-package extraction is a silent no-op.

Cause: a regression in the AEM RDE base image — `com.adobe.granite.rde.provider.runtime` is not in the platform's `LoginAdminAllowList`, so `RDEProviderRepositoryAccess.handleContentPackages` aborts when it tries to open an admin session. The HTTP install API still returns success because the file uploaded fine; the failure happens in the async post-upload importer. Tracked as **SKYOPS-140701** (broken since CQ/quickstart PR #42307 — the property names in `src/main/features/docker/base/rde-runtime.json` were left as the legacy `whitelist.*` after the PID rename to `LoginAdminAllowList.fragment`).

Confirm via `aio aem rde logs -e ""`:

```
*ERROR* com.adobe.granite.repository.impl.SlingRepositoryImpl Bundle
com.adobe.granite.rde.provider.runtime is NOT allow listed to use
SlingRepository.loginAdministrative
javax.jcr.LoginException
  at RDEProviderRepositoryAccess.handleContentPackages
```

Workaround until the platform fix ships — deploy this OSGi config once per affected RDE:

`org.apache.sling.jcr.base.internal.LoginAdminWhitelist.fragment~rdeprovider.cfg.json`
```json
{
  "whitelist.name": "rde-provider-runtime",
  "whitelist.bundles": ["com.adobe.granite.rde.provider.runtime"]
}
```

```
aio aem rde install --type osgi-config \
  org.apache.sling.jcr.base.internal.LoginAdminWhitelist.fragment~rdeprovider.cfg.json
```

Notes:
- Filename is the factory PID — the `.fragment` (with a leading dot) form is what the platform actually consults. The `LoginAdminWhitelistFragment` (camelCase, no dot) form is registered but inert; don't use it.
- After this lands, redeploy any content-packages that "succeeded" earlier — those previous deploys really were no-ops, the JCR is still empty.
- Once SKYOPS-140701 is fixed in the base image and your RDE is re-provisioned (`aio aem rde reset` or naturally over time), this fragment becomes redundant. It's safe to leave in place — it's additive to the platform allow-list.
- Symptoms similar but not the same: a content-package whose filter targets restricted paths (e.g. `/libs`) gets entries skipped — that's expected, not the SKYOPS-140701 bug. Distinguish by the `LoginException` in the logs.

## Bundle-specific gotchas

A bundle that uploaded fine but isn't doing anything is usually one of:

1. **Resolved but not Active** — missing capabilities. `aio aem rde inspect osgi-bundles <bsn>` and read the wires/missing imports. Likely cause: a transitive dep wasn't included.
2. **Active but components Unsatisfied** — DS reference can't bind. `aio aem rde inspect osgi-components` looks for `unsatisfiedReferences` entries.
3. **Active, components Satisfied, but Configuration is wrong** — `aio aem rde inspect osgi-configurations` to see what Configuration Admin actually has.

## Logs command issues

### "405 — too many active log configurations"

AEM caps concurrent log configs per env. The plugin offers to remove an existing one. Accept, then retry. To pick one without removing it, use `--choose`.

### Log output stops mid-tail

The server-side log config got removed (someone else's `logs` command, or env restart). The plugin prints "Log configuration not found any longer …" and exits. Just rerun.

### Colors not rendering

Either you piped the output (in which case pass `--no-color` for clean text) or your terminal doesn't support 256-color escape codes. The default colors are: TRACE gray, DEBUG cyan, INFO green, WARN yellow, ERROR red.

## Reset / restart issues

### Reset hangs

`reset` takes 10-20 minutes. Don't kill it. Use `aio aem rde status --wait` in a separate shell to watch progress.

### Reset fails

Try `reset --force` to bypass the cached base repository. If that also fails, the env may need support intervention — file a ticket with the program and env IDs.

### Restart doesn't bring the bundle back

If the bundle was the one causing the env to be unhealthy, the restart preserves it. Try `delete <bsn>` first, then `restart`, then redeploy.

## "Did I get logged out?" checklist

If commands suddenly throw auth errors:

```bash
aio config:list ims                         # show contexts
aio context:current 2>/dev/null || echo "no current ctx"
aio auth:login                              # re-auth
aio aem rde setup --show                    # confirm
```

For service-account / JWT contexts in CI, re-run the credential setup that initially populated `ims.contexts.<name>`.

## When you don't know which command will help

Run these in order — each is fast and cheap:

```bash
aio aem rde setup --show       # are we even pointed at the right RDE?
aio aem rde status             # is the env Ready and what's deployed?
aio aem rde history            # what just happened?
```

Then:

- For "what's wrong inside AEM": `inspect osgi-bundles`, `inspect osgi-components`, `inspect osgi-configurations`.
- For runtime symptoms: `logs` with `-e "" -w ""`.
- For "I made it worse": `snapshot restore <name>` if you took one beforehand, else `reset --keep-mutable-content`.
