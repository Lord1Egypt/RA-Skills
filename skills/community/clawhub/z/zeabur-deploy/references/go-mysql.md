# Go + MySQL + GORM deployment

Use this reference only for this stack. Keep application environment names,
health response schema and authentication fixtures project-specific.

## Build and runtime contract

- Confirm the directory containing `go.mod`, the executable package, the Go
  version and target architecture. For a multi-module tree, choose the actual
  application root and include required workspace modules in the build context.
- Use the project's existing Dockerfile when it works. A static, CGO-disabled
  binary can use a non-root scratch runtime with CA certificates. CGO or dynamic
  libraries require a compatible runtime instead of blindly copying this shape.
- Listen on `0.0.0.0:$PORT` in the deployed mode. Loopback is for local-only use.
  Validate required DSN/configuration at startup; fail closed without printing
  their values. Catch listener failures and shut down HTTP/SQL pools gracefully.
- Separate liveness from readiness. Readiness must test real database connectivity
  with a bounded timeout and avoid exposing connection errors/credentials.
- Exclude `.local`, `.env*`, signing files and build output in `.dockerignore`.
  Inspect what the selected upload/build context contains before sending it.

## Database and secrets

Use a reviewed MySQL image/version and a persistent volume at the image's data
path (the earlier MySQL 8.4 deployment used `/var/lib/mysql`). Keep MySQL private
and verify port forwarding is disabled, rather than inferring privacy from the
presence of an internal hostname. Use a separate database and application user;
keep root credentials out of the API container. Select capacity/region from the
current deployment contract; do not hardcode the previous project's server.

For a new isolated database, generate credentials into a private ignored location
using a secure random source. For an existing database, preserve its credentials;
changing container initialization variables does not rotate an initialized MySQL
user. Do not rotate credentials, reset volumes or reinitialize data as a repair.

A GORM MySQL DSN typically needs `parseTime=true` and a deliberate character set
and connection/read/write timeouts. Use the actual private service address and
credentials. Never paste a credentialed DSN into a committed example or report.
Use the codebase's tested DSN builder/escaping strategy for chosen credentials.

Inspect startup migration behavior before deployment. Assess locks, destructive
changes and old-binary compatibility; require the applicable approval/backup
before irreversible schema changes. Reuse the project's test-database guard.
A test suite that drops/recreates tables belongs only on the isolated local
schema, never against the deployed database.

## Meaningful verification

Before deployment, run relevant tests, build/vet and the container check supported
by this project. After deployment, verify normal TLS, liveness, database-backed
readiness, unauthorized access rejection and the principal app workflow.

Authentication fixtures are a project decision. Do not copy a previous project's fixed phone
and code into another project. If an internal beta uses a shared fixed identity,
label it clearly, keep it in environment configuration, document data sharing and
retain the production guard. A successful fixture login is not proof of real SMS.

Reverse proxies affect rate limiting: do not trust arbitrary `X-Forwarded-For`
without a verified proxy trust model. A conservative limiter using the immediate
peer may group all users into one bucket. Record that limitation and assess it
for the expected load; do not silently remove throttling to make smoke tests pass.

A smoke script should clean up its own disposable fixtures and revoke its test
session; review its failure/cleanup paths before running it. Do not assume a
`finally` block guarantees server-side cleanup without checking what it does.

## Recover using evidence

| Observed symptom | Next check |
| --- | --- |
| Missing DSN / immediate exit | Required env names, correct service/environment, actual applied vars; restart after the intended configuration is applied |
| HTTP connects but readiness fails | MySQL process/readiness, private DNS/port, database/user permissions, migration errors; inspect privately |
| New MySQL password env does not authenticate | Existing volume initialization state; preserve it and inspect the actual user, do not delete the volume |
| Provisioning domain presents platform certificate | Domain status and certificate provisioning with backoff; keep TLS validation enabled |
| Health passes but client fails | Actual built client base URL, auth mode, API shape, proxy limits and app workflow |

Finish with source revision/deployment ID and schema-compatible rollback target.
Never equate redeploying an older image with restoring an older database schema.

[Official Go deployment guidance](https://zeabur.com/docs/en-US/guides/go)
