# Stack-specific checks

Read only the relevant section. Confirm APIs and defaults in the installed version; these are traps to investigate, not a mandate to replace working project conventions.

## Python and FastAPI

- Blocking I/O inside `async def` blocks the event loop. Use the project's async client or appropriate offloading; an in-process background task is not durable across restarts.
- Explicit response schemas prevent internal fields from escaping. Test dependency-based authorization at object level and clear test dependency overrides after use.
- Starlette's standard session cookie is signed, not encrypted. Do not place secrets in it. Confirm session settings and the OIDC library's actual state/nonce/PKCE behavior.
- Review Alembic output: a rename may become drop/add, and an autocommit block changes transaction boundaries. Test migration behavior with the target database engine.

## TypeScript and React

- `fetch` can resolve successfully for HTTP error statuses; check the response and bound the request lifetime. Runtime input still needs validation even when TypeScript types compile.
- JavaScript parses ISO date-only strings as UTC, but date-times without an offset as local time. Keep calendar dates distinct from instants; test conversion across the relevant timezone boundary.
- Browser bundles and client-visible environment variables cannot keep secrets. Avoid unsafe HTML insertion and token persistence accessible to injected scripts.
- Preserve the project's accessible components. Test focus and interaction behavior, not just rendered markup. Handle stale async results and component cleanup where requests can overlap.

## .NET

- Use the project's managed `HttpClient` lifecycle; per-request clients can exhaust connections. Account for handler pooling when cookies are involved and propagate cancellation.
- The standard HTTP resilience handler retries all methods by default. Disable unsafe-method retries with `options.Retry.DisableForUnsafeHttpMethods()` or establish safe idempotency for the operation. Stacking retry layers can multiply effects and latency.
- Keep `DbContext` scoped and avoid concurrent operations on one instance. Apply reviewed production migrations through the existing release procedure, not competing application startups. Do not initialize with `EnsureCreated` when the database uses EF migrations; it bypasses that migration history.

## Azure

- Verify which identity is actually selected in deployment. Prefer an explicit workload identity and narrow resource scope where the environment supports it; preserve integrations during credential changes.
- Read what-if/plan output for replacements, deletes and permission expansion. Verify origin application health separately from successful access-control authentication.
- A deployment's name or resource region does not establish where model requests are processed. Confirm the chosen deployment type's current residency behavior. Search fields hidden from results are not access control.

## Data pipelines

- A replayed batch must not append duplicate business records. Use stable keys/partitions, track watermarks and test restart after partial output.
- Distinguish event time from processing time. Test late records, overlapping windows and deduplication; reconcile financial totals with the source.
- Validate freshness and completeness as well as schema. A successful empty job can still be a production failure. Review downstream consumers before schema changes.

## Power Platform

- Non-delegable queries can silently examine only a client-limited subset. Test beyond that limit, or temporarily lower it to expose truncation; use a supported server-side query when needed.
- Preserve environment-specific connection references and data policies. Check connection ownership and what happens if the owner leaves or credentials expire. Do not use a personal connector to evade restrictions.
- Uninstalling a managed solution can delete its custom-table data. Verify dependencies and recovery before removal. Use the existing solution/environment release process rather than editing production directly.

## Sources

- [FastAPI async behavior](https://fastapi.tiangolo.com/async/)
- [Starlette sessions](https://www.starlette.io/middleware/#sessionmiddleware)
- [Alembic autogeneration limits](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [TypeScript type assertions and runtime behavior](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html#type-assertions)
- [React effects](https://react.dev/reference/react/useEffect)
- [ECMAScript date parsing](https://tc39.es/ecma262/multipage/numbers-and-dates.html#sec-date.parse)
- [.NET HTTP resilience defaults](https://learn.microsoft.com/en-us/dotnet/core/resilience/http-resilience)
- [EF Core schema creation](https://learn.microsoft.com/en-us/ef/core/managing-schemas/ensure-created)
- [.NET HttpClient guidelines](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/http/httpclient-guidelines)
- [EF Core DbContext lifetime](https://learn.microsoft.com/en-us/ef/core/dbcontext-configuration/)
- [Azure identity credential chains](https://learn.microsoft.com/en-us/dotnet/azure/sdk/authentication/credential-chains)
- [Azure model deployment types](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types)
- [Spark structured streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)
- [Power Apps delegation](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview)
- [Power Platform solution concepts](https://learn.microsoft.com/en-us/power-platform/alm/solution-concepts-alm)
