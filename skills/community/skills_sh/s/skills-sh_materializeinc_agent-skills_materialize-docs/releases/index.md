# Releases

Materialize release notes

> **Note:** Starting with the v26.1.0 release, Materialize releases on a weekly schedule for
> both Cloud and Self-Managed. See [Release schedule](/releases/schedule) for details.

## v26.27.0
*Released to Materialize Cloud: 2026-06-04* <br>
*Released to Materialize Self-Managed: 2026-06-05* <br>

This release includes improvements to the MCP Server for Agents, general
improvements, and bug fixes.

### MCP Server for Agents
We've made several improvements to our MCP Server for Agents, which can be used to give agents in production fresh context from Materialize.

- **`query` tool enabled by default**: The MCP Server for Agents now
  enables the [`query` tool](/integrations/mcp-server/mcp-agent-tools/#query)
  by default, allowing agents to join across data products.
- **Data product routing**: The `read_data_product` tool now
  automatically routes queries to the data product's catalog cluster,
  eliminating the need to specify the cluster manually.
- **Data product hydration status**: The MCP Server for Agents now
  surfaces hydration readiness state for data products, enabling agents
  to check whether a data product is fully hydrated before querying.

For more information, refer to:
- [MCP Server for Agents](/integrations/mcp-server/mcp-agent/)

### Improvements {#v26.27-improvements}

- **Improved `EXPLAIN` output**: Default `EXPLAIN` output now uses
  cleaner formatting for joins and explicitly identifies cross joins.

### Bug Fixes {#v26.27-bug-fixes}

- Fixed the Console in self-managed deployments not displaying the
  balancerd hostname in the connection dialog.
- Fixed incorrect query results from filter pushdown when using
  timestamp or date arithmetic with interval values.
- Fixed incorrect query results from filter pushdown when using `CASE`
  expressions over JSON columns with keys present in only one branch.
- Fixed `LATERAL` subqueries with table functions returning wrong
  results when the input table has an index on a non-leading column.
- Fixed `COPY FROM` CSV decoding silently treating quoted `NULL` markers
  as SQL `NULL` and dropping rows after a quoted end-of-copy marker.
- Fixed a panic when applying a timezone offset to a near-maximum
  timestamp value.
- Fixed a panic when applying a timezone offset to a leap-second
  timestamp value.
- Fixed a panic when a replica targeted by `CREATE MATERIALIZED VIEW ...
  IN CLUSTER ... REPLICA <name>` was concurrently dropped.
- Fixed a panic when specifying a `REFRESH` interval shorter than
  1 millisecond; now returns a clear error instead.
- Fixed SSH tunnel connections to HTTPS schema registries failing with
  TLS handshake errors when the URL omitted the default port.
- Fixed Iceberg sink errors when writing tables with `smallint` columns,
  map-typed columns, or `range`-typed equality delete keys.
- Fixed `SHOW CREATE` incorrectly displaying passwords and `AS OF`
  clauses.

## v26.26.0
*Released to Materialize Cloud: 2026-05-28* <br>
*Released to Materialize Self-Managed: 2026-05-29* <br>

This release includes Single Sign-On (SSO) for Self-Managed, a new Objects page
in the Console, performance improvements, and bug fixes.

### Single Sign-On (SSO) for Self-Managed

> **Public Preview:** This feature is in public preview.

Self-managed deployments can now configure single sign-on via any OIDC-compliant identity provider (Okta, Microsoft Entra ID, Auth0, Keycloak). Users authenticate via their IdP and receive a JWT token that Materialize validates; new users are auto-provisioned as database roles on first login, and existing users with matching emails map automatically to their current accounts. Enabling SSO is backward compatible: password-based auth continues to work for applications and service accounts.

For more information, refer to:
- [Single sign-on (SSO)](https://materialize.com/docs/security/self-managed/sso/)

### Objects page

The Console includes a new Objects page, which provides a unified view of all
sources, materialized views, indexes and sinks. You can track real-time freshness
metrics, hydration status, and cluster assignments. If an object is stale, you can diagnose why.
If lag is inherited from upstream, you can visualize the critical path. And if an object itself
is the cause of lag, you can diagnose the root cause.

### Improvements {#v26.26-improvements}

- **More performant temporal filters**: We've significantly improved the performance of
  temporal filters. While specific results will vary by workload, in our tests we saw CPU utilization drop from 75% to
  4% on workloads dominated by temporal filter evaluation.
- **Faster DDL at scale**: DDL operations (`CREATE TABLE`, `DROP TABLE`,
  etc.) are now up to 65% faster in environments with many objects by
  eliminating a per-table loop that previously ran on every group commit.
- **Faster storage usage collection**: Periodic storage usage collection is
  now up to 17x faster at 10,000 shards, reducing coordinator stalls from
  ~500ms to ~30ms per cycle.
- **`dbt-materialize`: `PARTITION BY` support**: Added a `partition_by`
  config option for materialized views, generating the `PARTITION BY (...)`
  clause in `CREATE MATERIALIZED VIEW`.
- **`dbt-materialize`: Unmanaged cluster support for blue/green
  deployments**: The `deploy_init` macro now supports unmanaged clusters by
  cloning each replica's size and availability zone, enabling blue/green
  deployments for environments not using managed clusters.

### Bug Fixes {#v26.26-bug-fixes}

- Fixed wrong results for `JOIN ... USING (col) AS t` with `RIGHT` or
  `FULL` joins.
- Fixed `round()` producing `-0` for negative fractional values that round
  to zero, causing mismatches in `DISTINCT`, `UNION`, and `GROUP BY`.
- Fixed `list_length_max` returning incorrect results for list-of-lists with
  `NULL` siblings before non-`NULL` sublists.
- Fixed incorrect query results when casting `text` to `"char"` or `bytea`
  in index lookups and equality filters.
- Fixed incorrect query results when casting `text` to `name` or
  `varchar(n)` in contexts that rely on uniqueness, such as `DISTINCT` or
  joins.
- Fixed MySQL sources failing to decode `TIMESTAMP` and `DATETIME` columns
  when using `TEXT COLUMNS`.
- Fixed `COPY FROM ... (FORMAT PARQUET)` producing range values that did not
  compare equal to logically-identical values constructed in SQL.
- Fixed missing audit log entries for `ALTER TABLE ADD COLUMN` and
  `ALTER SOURCE ... SET (TIMESTAMP INTERVAL)`.
- Fixed the Console Data Explorer page intermittently failing to load due to
  a WebSocket connection race condition.

## v26.25.0
*Released to Materialize Cloud: 2026-05-21* <br>
*Released to Materialize Self-Managed: 2026-05-22* <br>

This release includes source versioning for MySQL sources, improvements, and
bug fixes.

### MySQL: Source versioning

> **Public Preview:** This feature is in public preview.

For MySQL sources, we've introduced new syntax for [`CREATE
SOURCE`](/sql/create-source/mysql-v2/) and [`CREATE
TABLE`](/sql/create-table/). This allows you to better handle schema changes
in your source MySQL tables.

> **Note:** - Changing column types is currently unsupported.

For more information, refer to:
- [Guide: Handling upstream MySQL schema changes with zero
  downtime](/ingest-data/mysql/source-versioning/)
- [Syntax: `CREATE SOURCE`](/sql/create-source/mysql-v2/)
- [Syntax: `CREATE TABLE`](/sql/create-table/)

### Improvements {#v26.25-improvements}

- **Source versioning in public preview**: Source versioning helps you handle
  upstream schema changes without downtime in Materialize. With v26.25, source
  versioning has graduated from private preview to public preview, and is now
  available by default across all environments. For more information, refer to
  the source versioning guides:
    - [PostgreSQL](/ingest-data/postgres/source-versioning/)
    - [MySQL](/ingest-data/mysql/source-versioning/)
    - [SQL Server](/ingest-data/sql-server/source-versioning/)

### Bug Fixes {#v26.25-bug-fixes}

- Fixed dependents of replica-targeted materialized views being left in an
  inconsistent state when the target replica is dropped, causing subsequent
  queries against those dependents to fail.
- Fixed `ALTER CLUSTER ... SET (SIZE, WORKLOAD CLASS) WITH (WAIT FOR ...)`
  silently dropping the workload class change during zero-downtime
  reconfiguration.
- Fixed `CREATE TABLE FROM SOURCE` retaining the old source name in the stored
  definition after the source is renamed.
- Fixed `ALTER CONNECTION IF EXISTS` notice reporting the wrong object type.
- Fixed ambiguous column names being silently accepted in sink `KEY` clauses
  instead of returning an error.
- Fixed a panic during query optimization when `EXPECTED GROUP SIZE` is set
  to `0`.
- Fixed real-time recency timeout and dropped-object errors returning generic
  error messages instead of the correct SQL error codes and descriptions.
- Fixed Kafka sources hanging indefinitely when the start offset no longer
  exists due to topic retention or compaction.
- Fixed `EXPLAIN` plans omitting join projections, making some join closures
  appear as identity when they were not.
- Fixed Self-Managed replica scheduling when `availability_zones` is set,
  where `minDomains` could leave additional replicas stuck in a pending state.

## v26.24.3
*Released to Materialize Self-Managed: 2026-05-20* <br>

This patch release fixes a MySQL source ingestion bug.

### Bug Fixes {#v26.24.3-bug-fixes}

- Fixed MySQL sources failing to decode `TIMESTAMP` and `DATETIME` columns
  ingested via `TEXT COLUMNS`. Zero-value timestamps (`0000-00-00 00:00:00`)
  continue to require `TEXT COLUMNS` plus a `CAST` in user queries.

## v26.24.2
*Released to Materialize Self-Managed: 2026-05-18* <br>

This patch release extends the v26.24.0 catalog migration repair to cover
additional edge cases.

### Bug Fixes {#v26.24.2-bug-fixes}

- Extended the v26.24.0 catalog migration repair to also clear residual
  negative multiplicities and normalize Role rows still stored in the
  pre-v81 byte form.

## v26.24.1
*Released to Materialize Cloud: 2026-05-14 on as-needs basis* <br>

This patch release adds configurable Kafka sink message and batch size limits.

### Improvements {#v26.24.1-improvements}
Configurable Kafka sink size limits: The maximum size of individual Kafka sink messages and message batches can now be configured beyond their previous defaults.

## v26.24.0
*Released to Materialize Cloud: 2026-05-14* <br>

This release introduces the built-in MCP server for agents, improvements, and
bug fixes.

### MCP Server for Agents

> **Public Preview:** This feature is in public preview.

Give your agents fresh context using Materialize. Materialize environments now
include a built-in Model Context Protocol (MCP) [server for agents
(`/api/mcp/agent`)](/integrations/mcp-server/mcp-agent/). Once connected, an
agent can discover your data products, understand the underlying data ontology,
and run queries to fetch fresh data.

Agents can discover [materialized views](/sql/create-materialized-view/) or [indexed](/sql/create-index/) views. You can use [comments](/sql/comment-on/) to document the data products, and describe them to agents. Agents authenticate as [roles](/sql/create-role/) in Materialize, so [RBAC privileges](/manage/access-control/) govern which data products are visible. Finally, you can set up a dedicated [cluster](/concepts/clusters/) for your agents, so they're isolated from the rest of your environment.

The MCP server for agents complements the [MCP server for
developers](/integrations/mcp-server/mcp-developer/) released in v26.20.2. The
developer server gives coding agents (like Claude Code) access to Materialize's
observability so you can build on Materialize faster; the agent server gives
production agents fresh, governed context from your data products.

For more information, refer to:
- [Integrations: MCP Server for Agents](/integrations/mcp-server/mcp-agent/)

### Improvements {#v26.24-improvements}

- **`dbt-materialize` connection overrides**: The dbt adapter now supports
  passing custom connection options via the `options` field in `profiles.yml`,
  enabling OIDC authentication and other advanced connection configurations.
- **`COPY FROM` rejects HTTP redirects**: `COPY FROM` now returns a clear error
  if the target URL responds with an HTTP redirect, preventing unexpected data
  sources and potential security issues.
- **[Agent skills](/integrations/coding-agent-skills/) — improved `mcp-developer-analysis` client setup**: The skill now includes a comprehensive playbook for connecting MCP-capable clients (Claude Code, Cursor, VS Code, Zed, Continue, Windsurf, Claude Desktop) to the [MCP server for developers](/integrations/mcp-server/mcp-developer/).

### Bug Fixes {#v26.24-bug-fixes}

- Fixed MySQL sources with RDS IAM authentication failing when the database
  username contains special characters like `&` or `#`.
- Fixed joins incorrectly failing with a type mismatch error when join columns
  differed only in nullability.
- Fixed fast-path `SELECT` queries returning incorrect results when `OFFSET`
  was specified.
- Fixed `string_to_array` returning incorrect results when `null_string` is
  specified and the delimiter is empty.
- Fixed `INSERT INTO ... SELECT` silently ignoring the `OFFSET` clause in the
  source query.
- Fixed `seahash` function catalog metadata reporting the wrong return type
  (`uint4` instead of `uint8`).
- Fixed `mz_egress_ips` storing non-canonical CIDR notation (e.g.,
  `10.0.5.7/24` instead of `10.0.5.0/24`).
- Fixed Console crashing on OIDC-protected routes when the identity provider
  initialization fails, instead of falling through to password-based sign-in.
- Fixed catalog migration bug from v26.18.0 by which a
  `Non-positive multiplicity in DistinctBy` error could occur on queries
  containing `SELECT DISTINCT` over role-derived catalog views (e.g.,
  anything reading from `mz_roles`, `mz_role_members`, or views that
  internally project role columns). The error is resolved automatically by
  upgrading to v26.24.2 or newer.

## v26.23.2
*Released to Materialize Cloud: 2026-05-11* <br>

This patch release includes bug fixes.

### Bug Fixes {#v26.23.2-bug-fixes}

- Fixed a regression in v26.23.0 that caused storage replicas to spend a large
  share of their CPU time walking small data fragments during Parquet decode,
  slowing queries that read from object storage.
- Fixed a regression in v26.23.0 that caused storage replicas to retain extra
  memory when reading from object storage.

## v26.23.0
*Released to Materialize Cloud: 2026-05-07* <br>

This release introduces enhanced Kafka PrivateLink routing options, security
improvements, and bug fixes.

### Features {#v26.23-features}

- **Dynamic Kafka brokers with AWS PrivateLink**: Kafka connections can now
  route dynamically discovered brokers through a PrivateLink tunnel, rather than
  requiring every advertised broker to be enumerated in the `BROKERS (...)`
  clause. Two new options are available:
  - `MATCHING 'pattern' USING AWS PRIVATELINK conn (...)` inside `BROKERS (...)`
    associates a PrivateLink connection with any broker whose advertised
    hostname matches `pattern`, including brokers that only appear in Kafka
    metadata after the connection is established.
  - `BOOTSTRAP BROKER 'addr' USING AWS PRIVATELINK conn (...)` pins the initial
    bootstrap address to an explicit PrivateLink tunnel.

  Together, these resolve availability-zone mismatches that previously affected
  MSK and other Kafka clusters that rely on broker discovery, by ensuring every
  broker, including those learned from metadata, is reached through a
  PrivateLink endpoint in the broker's own AZ. Refer to our documentation on
  [AWS PrivateLink connections](/ingest-data/network-security/privatelink/) and
  the [Kafka `CREATE CONNECTION` PrivateLink syntax](/sql/create-connection/#kafka-privatelink-syntax)
  for more information.

### Improvements {#v26.23-improvements}

- **New `repeat_row_non_negative` SQL function**: The new
  `repeat_row_non_negative` table function generates a specified number of rows
  but errors on negative input rather than silently producing incorrect results,
  making it safer to use in general-purpose queries than the existing
  `repeat_row`.
- **Queries fail gracefully on internal errors**: Certain internal errors that
  previously caused `environmentd` to crash now return a query error instead,
  improving cluster stability.
- **dbt deploy retries on concurrent DDL conflicts**: `dbt deploy` now
  automatically retries the `ALTER SWAP` atomic deployment when it encounters a
  DDL interrupt from concurrent catalog operations, preventing spurious
  deployment failures in busy environments.
- **Clearer temporal filter error messages**: Error messages for unsupported
  temporal predicates now include the actual filter expression, making it easier
  to identify and fix the offending query.
- **`COPY TO S3` Parquet type validation at planning time**: `COPY TO S3` with
  `FORMAT PARQUET` now rejects Parquet-incompatible column types (such as
  `interval`) at query planning time with a clear error, rather than failing at
  execution time with an opaque message.
- **`mcp-developer-analysis`**: A new
  [coding agent skill](/integrations/coding-agent-skills/) that pairs with the
  `/api/mcp/developer` endpoint to provide diagnostic workflows, system catalog
  references, and remediation runbooks for AI-powered troubleshooting.
- **System catalog ontology for the MCP developer server**: The system
  catalog now exposes an ontology that describes how `mz_*` tables relate to
  one another and which tables to consult for common diagnostic questions. The
  [MCP server for developers](/integrations/mcp-server/mcp-developer/) uses
  this ontology to plan catalog queries directly instead of probing the schema,
  reducing the number of round trips needed to answer questions about
  hydration, freshness, and resource usage.
- **~10% faster materialized view hydration**: We've reduced the work performed
  during initial materialized view hydration, observing approximately 10%
  faster hydration times across our benchmarks. This shortens the window
  between creating (or restarting) a materialized view and the point at which
  it begins serving up-to-date results.

### Bug Fixes {#v26.23-bug-fixes}

- Fixed `statement_timeout = 0` (which means "disabled" in PostgreSQL semantics)
  causing every `SELECT` and `EXPLAIN FILTER PUSHDOWN` to fail immediately with a
  spurious `StatementTimeout` error.
- Tightened default validation on headers in Self-Managed deployments.
- Enhanced session-based HTTP authentication.
- Fixed `SHOW CREATE TYPE` emitting the bare type name instead of the
  fully-qualified `database.schema.type` name, unlike every other `SHOW CREATE`
  variant.
- Fixed Self-Managed `orchestratord` `--enable-rbac False` silently inverting
  the value and enabling RBAC instead of disabling it.
- Fixed SQL Server source composite primary key columns being recorded in
  non-deterministic order, causing incorrect constraint definitions and
  non-deterministic behavior across `ALTER SOURCE` and re-purification.
- Fixed PostgreSQL source RLS policy validation producing false positives that
  blocked replication for users whose roles inherit BYPASSRLS through role
  membership.
- Fixed SQL Server source growing memory without bound during table snapshots due
  to a `RowArena` that was never cleared between rows.
- Fixed `SELECT` queries with both `LIMIT` and `OFFSET` processing all remaining
  rows instead of stopping after the limit was reached.
- Fixed SQL Server source opening one upstream connection per Timely worker
  instead of one total, multiplying SQL Server connections and
  `sp_cdc_cleanup_change_table` calls by the worker count.
- Fixed SQL Server source with PrivateLink connections only attempting the first
  resolved IP address instead of trying all available addresses.
- Fixed `regexp_replace` returning an invalid regular expression error instead of
  `NULL` when called with a `NULL` replacement column and a literal pattern that
  fails to compile.
- Fixed `pg_index.indnatts` counting columns of the indexed table instead of the
  index itself, and `pg_class.relnatts` always reporting `0` for index rows,
  improving compatibility with tools that introspect the PostgreSQL catalog.
- Fixed toggling `memory_limiter_interval` from `0s` to a non-zero value at
  runtime potentially triggering an immediate replica kill even when memory usage
  was well below the limit.
- Fixed Self-Managed Kubernetes deployments where setting both
  `cluster_topology_spread_soft = on` and `cluster_topology_spread_min_domains`
  caused all replica pod creation to fail with an admission error.

## v26.22.0
*Released to Materialize Cloud: 2026-04-30* <br>
*Released to Materialize Self-Managed: 2026-05-01* <br>

This release includes various improvements, including faster sink performance
with up to 50% lower memory usage, and bug fixes.

### Improvements {#v26.22-improvements}

#### Sink improvements {#v26.22-improvements-sink}

- **Faster sink performance with up to 50% lower memory usage**: Sink operations
  now process data more efficiently by walking arrangements directly via
  cursors, reducing memory overhead and improving throughput. For large sinks,
  we have seen memory usage reduced by up to 50%.
- **Iceberg sink support for interval and range types**: Iceberg sinks now
  support `interval` and `range` data types, expanding compatibility with
  complex data schemas.

#### MCP security improvements {#v26.22-improvements-mcp-security}

- **Enhanced MCP server security**: MCP server origin validation now uses CORS
  allowlists instead of self-comparison checks, preventing DNS rebinding
  attacks.
- **Stricter MCP search path security**: MCP developer endpoint now sets a tight
  `search_path` to prevent bypass attacks.

#### General improvements {#v26.22-improvements-general}

- Catalog synchronization now uses more efficient consolidation algorithms,
  reducing overhead for environments with many objects.

- Improved query optimization by pushing `COALESCE` operations into `CASE WHEN`
  expressions where beneficial.

### Bug Fixes {#v26.22-bug-fixes}

- Fixed Iceberg upsert sinks dropping delete operations when handling more than
  100,000 distinct keys.
- Fixed `EXPLAIN OPTIMIZED PLAN` failure after renaming materialized views,
  indexes, or continual tasks.
- Fixed Parquet map key handling to properly deduplicate keys and use the final
  value when duplicates exist.
- Fixed subquery handling to properly account for negative diffs in accumulation
  logic.
- Fixed PostgreSQL source compatibility by using only `pg_catalog.server_version_num` for version detection.
- Fixed PostgreSQL `format_type` output to properly quote the `"char"` type (OID
  18).
- Fixed an issue in the Console where the cursor would not appear in the SQL
  editor.
- Fixed incorrect results from `mz_dataflow_global_ids` view when multiple
  objects shared the same dataflow.
- Fixed interval conversion overflow in Arrow utilities when converting
  microseconds to nanoseconds.
- Fixed OpenTelemetry rate limiting filter that was incorrectly suppressing all
  events instead of just rate-limited ones.
- Fixed catalog leak when dropping replacement collections without applying
  them.
- Enhanced security by ensuring sensitive authentication data is properly
  cleared from memory after use.
- Enhanced security by ensuring TLS certificate data is properly zeroized when
  dropped.
- Improved SQL name escaping in catalog operations for better reliability.
- Removed unused `memory_request` field from replica allocation configuration.
- Added regression test for Kafka sink handling of negative accumulations.

## v26.20.2
*Released to Materialize Cloud: 2026-04-16* <br>
*Released to Materialize Self-Managed: 2026-04-17* <br>

This release introduces the built-in Developer MCP server, Console
improvements, and bug fixes.

### MCP Server for Developers

> **Public Preview:** This feature is in public preview.

Materialize environments now include a built-in Model Context Protocol (MCP)
[Developer endpoint
(`/api/mcp/developer`)](/integrations/mcp-server/mcp-developer/). Connecting an
MCP-compatible coding agent (such as Claude Code, Claude Desktop, or Cursor) to
this endpoint lets you ask natural language questions about your environment.

For example, you could ask *why is my materialized view stale?* or *how much memory is my cluster using?*. You'll receive a diagnosis and recommendations on how to fix isssues.

For more information, refer to:
- [Integrations: MCP Server for
  Developers](/integrations/mcp-server/mcp-developer/)

### Improvements {#v26-20-improvements}
- **Better Console schema navigation**: The schema dropdown in the SQL Shell now
  prioritizes schemas from the current database, making it easier to find
  relevant schemas.

### Bug Fixes {#v26-20-bug-fixes}
- Fixed Console RBAC users tab that was displaying incorrectly for cloud users
  due to null `rolcanlogin` values.
- Fixed builtin dependency ordering issue that could cause system catalog
  inconsistencies.

## v26.19.0
*Released to Materialize Cloud: 2026-04-09* <br>
*Released to Materialize Self-Managed: 2026-04-10* <br>

This release introduces append mode for [Iceberg sinks](/sql/create-sink/iceberg/),
and bug fixes.

### Iceberg sink append mode

When an [Iceberg sink](/sql/create-sink/iceberg/) is created in append
mode, all changes are written as data rows — no Iceberg delete files are
produced. This is especially useful if you're sinking data from a materialized
view with temporal filters, and you don't want data to be deleted from your Iceberg table as it ages out.

```mzsql
CREATE SINK events_log_iceberg
  IN CLUSTER analytics_cluster
  FROM user_events
  INTO ICEBERG CATALOG CONNECTION iceberg_catalog_connection (
    NAMESPACE = 'events',
    TABLE = 'user_events_log'
  )
  USING AWS CONNECTION aws_connection
  MODE APPEND
  WITH (COMMIT INTERVAL = '5m');
```

For more information, refer to:
- [Guide: Apache Iceberg sink](/serve-results/sink/iceberg/)
- [Reference: `CREATE SINK ICEBERG`](/sql/create-sink/iceberg/)

### Bug Fixes {#v26.19-bug-fixes}

- Fixed identifier display in system catalog tables `mz_kafka_source_tables`,
  `mz_mysql_source_tables`, and `mz_postgres_source_tables` to show raw values
  without SQL quoting (e.g., `my-kafka-topic` instead of `"my-kafka-topic"`).

## v26.18.0
*Released to Materialize Cloud: 2026-04-02* <br>
*Released to Materialize Self-Managed: 2026-04-03* <br>

This release includes various improvements and bug fixes.

### Improvements {#v26.18-improvements}

- **Improved Console reconnect behavior**. The Console shell now reconnects
  more reliably, with toast notifications that no longer stack.

- **Expanded `COPY FROM` data type support**. [`COPY FROM` parquet
  files](/sql/copy-from/#parquet-formatting) now supports `map` and `interval`
  data types.

- **Improved query performance on wide tables**. Queries on tables with many
  columns now execute faster.

### Bug Fixes {#v26.18-bug-fixes}

- Fixed SSL certificate loading to properly handle all certificates in PEM
  bundles instead of only the first one.
- Fixed materialized view sinks getting stuck when instantiated with output
  shards whose initial frontier is less than the dataflow as-of.
- Fixed panic when dropping computed tables with active `SUBSCRIBE` operations.
- Fixed `EXPLAIN ANALYZE` not working correctly due to quoting issues in
  `mz_mappable_objects`.

## v26.17.1
*Released to Materialize Self-Managed: 2026-03-27* <br>

This release includes a bug fix.

### Bug Fixes {#v26.17.1-bug-fixes}

- Fixed Iceberg sinks failing to write unsigned integer types (UInt8,
  UInt16, UInt32, UInt64) by mapping them to Iceberg-compatible signed
  types.

## v26.17.0
*Released to Materialize Cloud: 2026-03-26* <br>
*Released to Materialize Self-Managed: 2026-03-27* <br>

This release includes performance improvements and bug fixes.

### Improvements {#v26.17-improvements}

- **10% improved transactional DDL performance**: We've eliminated an O(n^2) operation. DDL transactions (such as creating multiple tables from a source in a single transaction) now execute faster.
- **Reduced catalog server load during blue/green deploys**: The dbt-materialize adapter now uses a single batched query instead of
  per-cluster sequential polling. This is especially useful when creating a large number of objects.

### Bug Fixes {#v26.17-bug-fixes}

- Fixed a correctness bug where LEFT JOIN, RIGHT JOIN, and FULL JOIN with an
  empty relation produced incorrect results (empty instead of NULLs) due to
  join identity elision.
- Fixed Kafka sinks incorrectly writing negative Avro timestamps (pre-epoch
  dates) by treating the timestamp microseconds as unsigned instead of signed.
- Fixed Avro fixed-decimal encoding not left-padding unscaled bytes to the
  schema's fixed size, which could cause `UnexpectedEof` errors or data
  corruption in downstream consumers.
- Fixed a race condition in persist where a batch could be selected before
  obtaining a lease, potentially causing unexpected read-time halts.
- Fixed PROXY protocol v2 header parsing failing when headers arrived across
  multiple TCP segments, which could corrupt subsequent HTTP parsing between
  balancerd and environmentd.
- Fixed the Fivetran destination connector logging `app_password` in plaintext
  in connection logs.
- Fixed queries with expensive functions in subqueries (e.g., `UNION ALL`,
  `EXISTS`, scalar subqueries) being incorrectly routed to `mz_catalog_server`
  instead of the user's cluster.
- Fixed webhook secret cache not invalidating when secrets are changed,
  requiring a restart to pick up new secret values.
- Fixed orchestratord image reference parsing treating registry ports (e.g.,
  `gcr.io:443/...`) and digest separators (`@sha256:...`) as image tags,
  producing invalid references for Self-Managed deployments.
- Fixed optimizer feature flags being auto-enabled during item parsing, which
  rendered plan caching ineffective.
- Fixed `mz_catalog_raw` not being consistently readable under strict
  serializable isolation by keeping the catalog shard's frontier up-to-date
  with the oracle read timestamp.
- Fixed a security vulnerability in the `lz4_flex` dependency
  (RUSTSEC-2026-0041).
- Fixed a bad assertion in oneshot source storage worker reconciliation that
  could cause panics.
- Fixed hydration check errors during 0dt upgrades for replica-targeted
  collections, where non-target replicas would report `CollectionMissing`
  errors.
- Fixed SQL Server source `Transaction::drop` not sending ROLLBACK, leaving
  the SQL Server session in an open transaction after drop.
- Fixed a panic in authentication when receiving a proof of unexpected length.
- Fixed an issue causing console session variables to be lost after a reconnect.

## v26.16.0
*Released to Materialize Cloud: 2026-03-19* <br>
*Released to Materialize Self-Managed: 2026-03-20* <br>

This release adds support for copying Parquet files from object storage, performance improvements, and bug fixes.

### `COPY FROM` Parquet files in object storage

`COPY FROM` now supports bulk importing data from Parquet files stored in Amazon
S3 and any S3-compatible object storage service, such as Google Cloud Storage,
Cloudflare R2, or MinIO. You can import Parquet files using an AWS connection or
a presigned URL.

```mzsql
COPY INTO my_table
FROM 's3://my_bucket/my_data.parquet'
(FORMAT PARQUET, AWS CONNECTION = my_aws_conn);
```

For more information, refer to:
- [Syntax: COPY FROM](/sql/copy-from/)
- [Syntax: CREATE CONNECTION (S3-compatible)](/sql/create-connection/#s3-compatible-object-storage)

### Improvements {#v26.16-improvements}

- **Improved [`AS OF`](/sql/subscribe/#as-of) error messages**: Error messages
  for `AS OF` queries now use user-facing terminology (e.g., "Indexed
  input", "Storage inputs") instead of internal names.
- **Streamed [WebSocket](/integrations/websocket-api/) query results**:
  WebSocket query results are now streamed directly instead of buffered,
  reducing memory usage for large result sets.

### Bug Fixes {#v26.16-bug-fixes}

- Fixed an RBAC security bypass that allowed a non-superuser with
  `CREATEROLE` privilege to strip superuser status from any role via
  `ALTER ROLE ... NOSUPERUSER`.
- Fixed indexes on older versions of altered tables or replaced
  materialized views being lost during environment bootstrap, which
  could cause panics.
- Fixed pgwire encoding errors leaving partial messages in the connection
  buffer, which caused clients to see "lost synchronization" errors
  instead of proper error messages.
- Fixed unbounded queue growth in storage since-downgrade processing that
  could lead to out-of-memory conditions in environments with many
  storage collections.
- Fixed a correctness bug when parsing large Avro fixed-size decimals
  from Kafka sources, where values were returned as raw bytes instead of
  decoded decimal numbers.
- Fixed subqueries being incorrectly allowed in the `SET` clause of
  `UPDATE` statements.
- Fixed `COPY FROM S3` requiring manual column specification for tables
  with `NOT NULL` columns by removing a redundant non-null check during
  planning.
- Fixed a correctness issue with `COPY FROM STDIN` when using headers.
- Fixed column name deduplication bug in `COPY TO` / Parquet writer that
  could produce duplicate column names.
- Fixed `RETAIN HISTORY` value being ignored for webhook tables.
- Fixed `DROP OWNED BY` and `REASSIGN OWNED BY` not including network
  policies, which could block `DROP ROLE` for roles that own network
  policies.
- Fixed false positive wallclock lag reporting (showing ~56 years of lag)
  during replica startup for compute introspection indexes.

## v26.15.0
*Released to Materialize Cloud: 2026-03-12* <br>
*Released to Materialize Self-Managed: 2026-03-13* <br>

This release includes various improvements and bug fixes.

### Improvements {#v26.15-improvements}

- **Improved memory efficiency for joins on `varchar` and `text` columns**:
  Previously, joining on these columns required creating a new arrangement,
  effectively doubling memory usage. Materialize can now reuse existing
  arrangements on these columns. We've seen memory improvements by as much as 25%
  in some cases involving `varchar` indexes.
- Added support for setting `cpu_request` independently of `cpu_limit`
  in cluster replica sizes for Self-Managed deployments.
- Renamed the **Org ID** label to **Environment ID** in the Console Shell
  to disambiguate organization IDs from environment IDs, which was
  causing confusion for Self-Managed deployments.

### Bug Fixes {#v26.15-bug-fixes}

- Fixed unmaterializable functions (e.g., `now()`) being allowed in
  `AS OF` queries, which could return incorrect results.
- Fixed Kafka sink creation failing with an authorization error when the
  progress topic already exists, which affected workflows where topics
  are pre-created by a superuser.
- Fixed a panic when running `COPY FROM STDIN` concurrently with table
  drops.
- Fixed unbounded command queue buildup in internal storage writer tasks
  that could lead to out-of-memory conditions when environments have a
  large number of indexes.
- Fixed the Role Filters display in dark mode in the Console.
- Fixed an incorrect join condition in the Console cluster list that
  could cause incorrect cluster information to be displayed.

## v26.14.1
*Released to Materialize Cloud: 2026-03-05* <br>
*Released to Materialize Self-Managed: 2026-03-06* <br>

This release introduces `COPY FROM` support for CSVs in object storage, source versioning for SQL Server sources, and performance improvements to DDL.

### `COPY FROM` CSVs in object storage

`COPY FROM` now supports bulk importing data directly from Amazon S3 and any
S3-compatible object storage service, such as Google Cloud Storage, Cloudflare
R2, or MinIO. You can import CSV files using an AWS connection or a presigned
URL.

```mzsql
COPY INTO my_table
FROM 's3://my_bucket/my_data.csv'
(FORMAT CSV, AWS CONNECTION = my_aws_conn);
```

For more information, refer to:
- [Syntax: COPY FROM](/sql/copy-from/)
- [Syntax: CREATE CONNECTION (S3-compatible)](/sql/create-connection/#s3-compatible-object-storage)

### SQL Server: Source versioning

For SQL Server sources, we've introduced new syntax
for [`CREATE SOURCE`](/sql/create-source/sql-server-v2/) and [`CREATE
TABLE`](/sql/create-table/). This allows you to better handle schema changes
in your source SQL Server tables.

> **Note:** - Changing column types is currently unsupported.

For more information, refer to:
- [Guide: Handling upstream schema changes with zero
  downtime](/ingest-data/sql-server/source-versioning/)
- [Syntax: `CREATE SOURCE`](/sql/create-source/sql-server-v2/)
- [Syntax: `CREATE TABLE`](/sql/create-table/)

### Improvements {#v26.14-improvements}

- **Faster DDL at scale**: We've improved DDL (e.g., `CREATE VIEW`, `CREATE INDEX`, `DROP`) latency by 37-55% for environments with many objects by making the internal catalog state a persistent data structure with structural sharing.
- **Faster Iceberg sink commits**: We've improved Iceberg sink commit performance by disabling the duplicate check for RowDelta actions, which was causing significant commit time overhead.
- **Up to 28x faster `COPY FROM STDIN`**: We've improved `COPY FROM STDIN` performance by parallelizing ingestion and using constant memory.

### Bug Fixes {#v26.14-bug-fixes}

- Fixed the jsonb contains operator (`?`) to correctly return NULL when
  the left operand is NULL, matching PostgreSQL behavior.
- Internal optimization that reduces resource usage of the catalog server; this can
  reduce resource consumption on restart when indexes are added.
- Fixed a panic when using `COPY FROM` with invalid range values (e.g.,
  `[7,3)` where lower bound exceeds upper bound), now returning a
  proper error message.
- Fixed incorrect replication lag display in the Console during
  PostgreSQL source snapshots, where `offset_committed` was incorrectly
  reported as zero until the snapshot completed.
- Fixed a panic when dropping materialized views that had active
  subscribes depending on older GlobalIds.
- Fixed dataflows being incorrectly re-planned after an environmentd
  restart due to missing per-cluster optimizer feature overrides.
- Fixed query formatting for SQL Server and MySQL sources.

## v26.13.0
*Released to Materialize Cloud: 2026-02-26* <br>
*Released to Materialize Self-Managed: 2026-02-27* <br>

This release includes the release of our Iceberg Sink, performance improvements to `SUBSCRIBE`, and bugfixes.

### Iceberg Sink
> **Public Preview:** This feature is in public preview.

Iceberg sinks provide exactly once delivery of updates from Materialize into [Apache
Iceberg](https://iceberg.apache.org/) tables hosted on [Amazon S3
Tables](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-tables.html).
As data changes in Materialize, the corresponding Iceberg tables are
automatically kept up to date. You can sink data from a materialized view, a
source, or a table.

```mzsql
CREATE SINK my_iceberg_sink
  IN CLUSTER sink_cluster
  FROM materialized_view_mv1
  INTO ICEBERG CATALOG CONNECTION iceberg_catalog_connection (
    NAMESPACE = 'my_iceberg_namespace',
    TABLE = 'mv1'
  )
  USING AWS CONNECTION aws_connection
  KEY (row_id)
  MODE UPSERT
  WITH (COMMIT INTERVAL = '60s');
```

For more information, refer to:
- [Guide: How to export results from Materialize to Apache Iceberg Tables](/serve-results/sink/iceberg)
- [Blog: Making Iceberg work for Operational Data](https://materialize.com/blog/making-iceberg-work-for-operational-data/)
- [Syntax: CREATE SINK... INTO ICEBERG ](/sql/create-sink/iceberg)

### Improvements {#v26.13-improvements}
- **Improved `SUBSCRIBE` Performance**: We've optimized `SUBSCRIBE` to skip initial snapshots in more cases. This can speed up `SUBSCRIBE` start times.
- **Improved compatibility with external tools**: We've added `strpos` as a
  synonym for the `position` function, improving compatibility with tools such
  as PowerBI.
- **Improved database concurrency**: We've reduced contention when a single
  collection experiences a high volume of updates.

### Bug Fixes {#v26.13-bug-fixes}
- Fixed a panic when constructing multi-dimensional arrays with null values,
  now treating null elements as zero-dimensional arrays consistent with
  PostgreSQL behavior.
- Fixed a bug where dropping a replacement materialized view (instead of
  applying the replacement) could seal the target materialized view for all
  times after an environmentd restart.
- Fixed a bug where `Int2Vector` to `Array` casting did not correctly handle
  element type conversions, potentially causing incorrect results or errors.
- Fixed the Self-Managed bug in the memory-based calculation of replica size
  credits, which was incorrectly multiplying by the number of workers instead of
  using the correct per-process memory limit.
- Fixed an overflow display issue on the roles page in the console.
- Fixed SSO connection configuration pages in the console, which did not load properly due to missing content security policy entries.

## v26.12.0
*Released to Materialize Cloud: 2026-02-19* <br>
*Released to Materialize Self-Managed: 2026-02-20* <br>

This release introduces our Roles and Users page, performance improvements, and bugfixes.

### Role Management
The new Roles and Users page on the Materialize Console allows organization administrators to create roles, grant privileges, and assign roles to users. You can also track the hierarchy of roles using the graph view.

![Create Role experience](/images/releases/v2612_create_role.png)

![Graph View experience](/images/releases/v2612_graph_view.png)

You can navigate to the Roles and Users page directly from the Materialize console. If you're on Materialize Self-Managed, upgrade to v26.12 first. If you're on Materialize Cloud, you can go directly to https://console.materialize.com/roles to reach the page.

### Improvements {#v26.12-improvements}
- **Updated default resource requirements** (<red>*Materialize Self-Managed only*</red>): We've updated the Materialize Self-Managed Helm charts to ensure correct operation on Kind clusters
- **Improved console query history performance**: We've optimized RBAC queries to use OIDs instead of names, resulting in 2-3x faster page execution.

### Bug Fixes {#v26.12-bug-fixes}
- Fixed a panic when using unsupported types (e.g., float) with range
  expressions, now returning a proper error message instead of an internal error.
- Fixed a panic when using empty `int2vector` values, which could cause internal
  errors during query optimization or execution.
- Fixed internal errors that could occur during query optimization due to type
  checking mismatches in `ColumnKnowledge` and related transforms, adding
  fallback handling to prevent crashes.
- Fixed compatibility with older Amazon Aurora PostgreSQL versions when using
  parallel snapshots, by using `SELECT current_setting()` instead of `SHOW` for
  version retrieval.
- Fixed version comparison in the Materialize Kubernetes operator to correctly
  follow semver precedence rules, no longer rejecting upgrades that differ only in build metadata.

## v26.11.0
*Released to Materialize Cloud: 2026-02-19* <br>
*Released to Materialize Self-Managed: 2026-02-13* <br>

This release includes improvements to Avro Schema references, `EXPLAIN` commands, and bug fixes.

### Improvements {#v26.11-improvements}
- **Avro Schema References**: Sources can now use avro schemas which reference
  other schemas when using Confluent Schema Registry.
- **`EXPLAIN` improvements**: `EXPLAIN` now allows you to inspect the query plan
  for `SUBSCRIBE` statements. It also fully qualifies index names if there are
  identically-named indexes across different schemas.
- **More efficient dbt-adapter**: We've added indexes on `mz_hydration_statuses` and `mz_materialization_lag`.
  This should speed up "deployment ready" queries made by our dbt-adapter.

### Bug Fixes {#v26.11-bug-fixes}
- Fixed a bug where `IS DISTINCT FROM` could fail typechecking in certain cases
  involving different data types, causing query errors.
- Improved the error message when `INSERT INTO ... SELECT` transitively
  references a source.

## v26.10.1
*Released to Materialize Cloud: 2026-02-05* <br>
*Released to Materialize Self-Managed: 2026-02-06* <br>

This release introduces Replacement Materialized Views, performance improvements,
and bugfixes.

### Replacement Materialized Views
> **Public Preview:** This feature is in public preview.

Replacement materialized views allow you to modify the definition of an existing materialized view, while preserving all downstream dependencies. Materialize is able to replace a materialized view in place, by calculating the *diff* between the original and the replacement. Once applied, the *diff* flows downstream to all dependent objects.

For more information, refer to:
- [Guide: Replace Materialized Views](/transform-data/updating-materialized-views/replace-materialized-view)
- [Syntax: CREATE REPLACEMENT MATERIALIZED VIEW](/sql/create-materialized-view)
- [Syntax: ALTER MATERIALIZED VIEW](/sql/alter-materialized-view)

### Improvements {#v26.10-improvements}
- **Improved hydration times for PostgreSQL sources**: PostgreSQL sources now perform parallel snapshots. This should improve initial hydration times, especially for large tables.

### Bug Fixes {#v26.10-bug-fixes}
- Fixed an issue where floating-point values like `-0.0` and `+0.0` could be
  treated as different values in equality comparisons but the same in ordering,
  causing incorrect results in operations like `DISTINCT`.
- Fixed an issue where certain SQL keywords required incorrect quoting in
  expressions.
- Fixed the `ORDER BY` clause in `EXPLAIN ANALYZE MEMORY` to correctly sort by
  memory usage instead of by the text representation.
- Fixed a bug where the optimizer could mishandle nullability inside record
  types.
- Fixed an issue where the `mz_roles` system table could produce invalid
  retractions when certain system variables were changed.
- *Console*: Fixed SQL injection vulnerability in identifier quoting where only
  the first quote character was being escaped.

## v26.9.0
*Released to Materialize Cloud: 2026-01-29* <br>
*Released to Materialize Self-Managed: 2026-01-30* <br>

v26.9 includes significant performance improvements to QPS & query latency.

### Improvements {#v26.9-improvements}
- **Up to 2.5x increased QPS**: <a name="v26.9-qps"></a>We've significantly optimized how `SELECT` statements are processed; they are now processed outside the main thread. In our tests, this change increased QPS by as much as 2.5x.
![Chart of QPS before/after](/images/releases/v2609_qps.png)
- **Significant reduction in query latency**: <a
  name="v26.9-latency-reduction"></a>Moving `SELECT` statements off the main
  thread has significantly reduced latency. p99 has reduced by up to 50% for
some workloads. ![Chart of latency
before/after](/images/releases/v2609_latency.png)
- **Dynamically configure system parameters using a ConfigMap** (<red>*Materialize Self-Managed only*</red>): <a name="v26.9-sm-configmap"></a>You can now use a ConfigMap to dynamically update system parameters at runtime. In many cases, this means you don't need to restart Materialize for new system parameters to take effect. You can also specify system parameters which survive restarts and upgrades. Refer to our [documentation on configuring system parameters](/self-managed-deployments/configuration-system-parameters/#configure-system-parameters-via-configmap).
- Added `ABORT` as a PostgreSQL-compatible alias for the `ROLLBACK` transaction command, to improve compatibility with GraphQL engines like Hasura

### Bug Fixes {#v26.9-bug-fixes}
- Fixed an issue causing new generations to be promoted prematurely when using the `WaitUntilReady` upgrade strategy (<red>*Materialize Self-Managed only*</red>)
- Fixed a race condition in source reclock that could cause panics when the `as_of` timestamp was newer than the cached upper bound.
- Improved error messages when the load balancer cannot connect to the upstream environment server

## v26.8.0
*Released to Materialize Cloud: 2026-01-22* <br>
*Released to Materialize Self-Managed: 2026-01-23* <br>

v26.8 includes a new notice in the Console to help catch common SQL mistakes,
Protobuf compatibility improvements, and performance optimizations for view
creation.

### Improvements {#v26.8-improvements}
- Added a Console notice when users write `= NULL`, `!= NULL`, or `<>
  NULL` in SQL expressions instead of `IS NULL` or `IS NOT NULL`. Comparisons
  using `=`, `!=`, or `<>` with `NULL` always evaluate to `NULL`.
- Protobuf schemas that import well-known types (such as `google.protobuf.Timestamp` or `google.protobuf.Duration`) now work automatically when using a Confluent Schema Registry connection.
- Improved performance of view creation by caching optimized expressions, resulting in approximately 2x faster view creation in some scenarios.

## v26.7.0
*Released to Materialize Self-Managed: 2026-01-16* <br>
*Released to Materialize Cloud: 2026-01-17* <br>

v26.7 improves compatibility with go-jet and includes bug fixes.

### Improvements {#v26.7-improvements}

- **Improved compatibility with go-jet**: We've added the `attndims` column to `pg_attribute`. We've also fixed `pg_type.typelem` to correctly report element types for named list types.
- **Pretty print SQL in the console**: We've made it easier to read the definitions for views and materialized views in the console.

### Bug Fixes {#v26.7-bug-fixes}
- Fixed an issue where type error messages could inadvertently expose constant values from queries.
- The console reconnects more gracefully if the connection to the backend is interrupted

## v26.6.0
*Released to Materialize Cloud: 2026-01-08*<br>
*Released to Materialize Self-Managed: 2026-01-09*<br>

v26.6.0 includes bug fixes for Kafka sinks and Self-Managed deployments.

### Bug Fixes {#v26.6-bug-fixes}
- Fixed an issue where console and balancer deployments could fail to upgrade to the correct version during Self-Managed environment upgrades.
- Fixed an issue where `ALTER SINK ... SET FROM` on Kafka sinks could incorrectly restart in snapshot mode even when the sink had already made progress, causing unnecessary resource consumption and potential out-of-memory errors.

## v26.5.1
*Released to Materialize Self-Managed: 2025-12-23* <br>
*Released to Materialize Cloud: 2026-01-08* <br>

v26.5.1 enhances our SQL Server source, improves performance, and strengthens Materialize Self-Managed reliability.

### Improvements {#v26.5-improvements}
- **VARCHAR(MAX) and NVARCHAR(MAX) support for SQL Server**: The Materialize SQL Server source now supports `varchar(max)` and `nvarchar(max)` data types.
- **Faster authentication for connection poolers**: We've added an index to the `pg_authid` system catalog. This should significantly improve the performance of default authentication queries made by connection poolers like pgbouncer.
- **Faster Kafka sink startup**: We've updated the default Kafka progress topic configuration to reduce the amount of progress data processed when creating new [Kafka sinks](/serve-results/sink/kafka/).
- **dbt strict mode**: We've introduced `strict_mode` to dbt-materialize, our dbt adapter. `strict_mode` enforces production-ready isolation rules and improves cluster health monitoring. It does so by validating source idempotency, schema isolation, cluster isolation and index restrictions.
- **SQL Server Always On HA failover support** (<red>*Materialize Self-Managed only*</red>): Materialize Self-Managed now offers better support for handling failovers, without downtime, in SQL Server Always On sources. [Contact our support team](/support/) to enable this in your environment.
- **Auto-repair accidental changes** (<red>*Materialize Self-Managed only*</red>): Improvements to the controller logic allow Materialize to auto-repair changes such as deleting a StatefulSet. This means that your production setups should be more robust in the face of accidental changes.
- **Track deployment status after upgrades** (<red>*Materialize Self-Managed only*</red>): The Materialize custom resource now displays both active and desired `environmentd` versions. This makes it easier to track deployment status after upgrades.

### Bug fixes {#v26.5-bug-fixes}
- Added additional checks to string functions (`replace`, `translate`, etc.) to help prevent out-of-memory errors from inflationary string operations.
- Fixed an issue which could cause panics during connection drops; this means improved stability when clients disconnect.
- Fixed an issue where disabling console or balancers would fail if they were already running.
- Fixed an issue where balancerd failed to upgrade and remained stuck on its pre-upgrade version.

## v26.4.0

*Released to Materialize Self-Managed: 2025-12-17* <br>
*Released to Materialize Cloud: 2025-12-18*

v26.4.0 introduces several performance improvements and bugfixes.

### Improvements {#v26.4-improvements}
- **Over 2x higher connections per second (CPS)**: We've optimized how Materialize handles inbound connection requests. In our tests, we've observed 2x - 4x improvements to the rate at which new client connections can be established. This is especially beneficial when spinning up new environments, warming up connection pools, or scaling client instances.
- **Up to 3x faster hydration times for large PostgreSQL tables**: We've reduced the overhead incurred by communication between multiple *workers* on a large cluster. We've observed up to 3x throughput improvement when ingesting 1 TB PostgreSQL tables on large clusters.
- **More efficient source ingestion batching**: Sources now batch writes more effectively. This can result in improved freshness and lower resource utilization, especially when a source is doing a large number of writes.
- **CloudSQL HA failover support** (<red>*Materialize Self-Managed only*</red>): Materialize Self-Managed now offers better support for handling failovers in CloudSQL HA sources, without downtime. [Contact our support team](/support/) to enable this in your environment.
- **Manual Promotion** (<red>*Materialize Self-Managed only*</red>): [Rollout strategies](/self-managed-deployments/upgrading/#rollout-strategies) allow you control how Materialize transitions from the current generation to a new generation during an upgrade. We've added a new rollout strategy called `ManuallyPromote` which allows you to choose when to promote the new generation. This means that you can minimize the impact of potential downtime.

### Bug Fixes {#v26.4-bug-fixes}
- Fixed timestamp determination logic to handle empty read holds correctly.
- Fixed lazy creation of temporary schemas to prevent schema-related errors.
- Reduced SCRAM iterations in scalability framework and fixed fallback image configuration.

## v26.3.0

*Released to Materialize Cloud & Materialize Self-Managed: 2025-12-12*<br>

### Improvements {#v26.3-improvements}
- For Self-Managed: added version upgrade window validation, to prevent skipping required intermediate versions during upgrades.
- Improved activity log throttling to apply across all statement executions, not just initial prepared statement execution, providing more consistent logging behavior.

### Bug Fixes {#v26.3-bug-fixes}
- Fixed validation for replica sizes to prevent configurations with zero scale or workers, which previously caused division-by-zero errors and panics.
- Fixed frontend `SELECT` sequencing to gracefully handle collections that are dropped during real-time recent timestamp determination.

## v26.2.0

*Released Cloud: 2025-12-05*<br>
*Released Self-Managed: 2025-12-09*

This release focuses primarily on bug fixes.

### Bug fixes {#v26.2-bug-fixes}
- **Catalog updates**: Fixed a bug where catalog item version updates were incorrectly ignored when the `create_sql` didn't change, which could cause version updates to not be applied properly.

- **Console division by zero**: Fixed a division by zero error in the console, specifically when viewing `mz_console_cluster_utilization_overview`.

- **ALTER SINK improvements**: Fixed `ALTER SINK ... SET FROM` to prevent panics in certain situations.

- **Improved rollout handling**: Fixed an issue where rollouts could leave a pod at their previous configuration.

- **Dependency drop handling**: Fixed panics that could occur when dependencies are dropped during a SELECT or COPY TO. These operations now gracefully return a `ConcurrentDependencyDrop` error.

## v26.1.0
*Released Self-Managed: 2025-11-26*

v26.1.0 introduces `EXPLAIN ANALYZE CLUSTER`, console bugfixes, and improvements for SQL Server support, including the ability to create a SQL Server Source via the Console.

### `EXPLAIN ANALYZE CLUSTER`
The [`EXPLAIN ANALYZE`](/sql/explain-analyze/) statement helps analyze how objects, namely indexes or materialized views, are running. We've introduced a variation of this statement, `EXPLAIN ANALYZE CLUSTER`, which presents a summary of every object running on your current cluster.

You can use this statement to understand the CPU time spent and memory consumed per object on a given cluster. You can also reveal whether an object has skewed operators, where work isn't evenly distributed among workers.

For example, to get a report on memory, you can run `EXPLAIN ANALYZE CLUSTER MEMORY`, and you'll receive an output similar to the table below:
| object                                  | global_id | total_memory | total_records |
| --------------------------------------- | --------- | ------------ | ------------- |
| materialize.public.idx_top_buyers       | u85496    | 2086 bytes   | 25            |
| materialize.public.idx_sales_by_product | u85492    | 1909 kB      | 148607        |
| materialize.public.idx_top_buyers       | u85495    | 1332 kB      | 77133         |

To understand worker skew, you can run `EXPLAIN ANALYZE CLUSTER CPU WITH SKEW`, and you'll receive an output similar the table below:
| object                                  | global_id | worker_id | max_operator_cpu_ratio | worker_elapsed  | avg_elapsed     | total_elapsed   |
| --------------------------------------- | --------- | --------- | ---------------------- | --------------- | --------------- | --------------- |
| materialize.public.idx_sales_by_product | u85492    | 0         | 1.18                   | 00:00:00.094447 | 00:00:00.079829 | 00:00:00.159659 |
| materialize.public.idx_top_buyers       | u85495    | 0         | 1.15                   | 00:00:01.371221 | 00:00:01.363659 | 00:00:02.727319 |
| materialize.public.idx_top_buyers       | u85495    | 1         | 1.03                   | 00:00:01.356098 | 00:00:01.363659 | 00:00:02.727319 |
| materialize.public.idx_top_buyers       | u85496    | 1         | 1.01                   | 00:00:00.021163 | 00:00:00.021048 | 00:00:00.042096 |
| materialize.public.idx_top_buyers       | u85496    | 0         | 0.99                   | 00:00:00.020932 | 00:00:00.021048 | 00:00:00.042096 |
| materialize.public.idx_sales_by_product | u85492    | 1         | 0.82                   | 00:00:00.065211 | 00:00:00.079829 | 00:00:00.159659 |

### Improved SQL Server support

Materialize v26.1.0 includes improved support for SQLServer, including the ability to create a SQLServer Source via the console.

### Upgrade notes for v26.1.0

<ul>
<li>To upgrade to <code>v26.1</code> or future versions, you must first upgrade to <code>v26.0</code></li>
</ul>

## Self-Managed v26.0.0

*Released: 2025-11-18*

### Swap support

Starting in v26.0.0, Self-Managed Materialize enables swap by default. Swap
allows for infrequently accessed data to be moved from memory to disk. Enabling
swap reduces the memory required to operate Materialize and improves cost
efficiency.

To facilitate upgrades from v25.2, Self-Managed Materialize added new labels to
the node selectors for `clusterd` pods:

- To upgrade using Materialize-provided Terraforms, upgrade your Terraform
  version to `v0.6.1`:
  - <a href="https://github.com/MaterializeInc/terraform-aws-materialize?tab=readme-ov-file#v061" >AWS Terraform v0.6.1 Upgrade
Notes</a>.
  - <a href="https://github.com/MaterializeInc/terraform-google-materialize?tab=readme-ov-file#v061" >GCP Terraform v0.6.1 Upgrade
Notes</a>.
  - <a href="https://github.com/MaterializeInc/terraform-azurerm-materialize?tab=readme-ov-file#v061" >Azure Terraform v0.6.1 Upgrade
Notes</a>.

- To upgrade if <red>**not**</red> using a Materialize-provided Terraforms,  you
must prepare your nodes by adding the required labels. For detailed
instructions, see [Prepare for swap and upgrade to
v26.0](/self-managed-deployments/appendix/upgrade-to-swap/).

### SASL/SCRAM-SHA-256 support

Starting in v26.0.0, Self-Managed Materialize supports SASL/SCRAM-SHA-256
authentication for PostgreSQL wire protocol connections. For more information,
see [Authentication](/security/self-managed/authentication/).

When SASL authentication is enabled:

- **PostgreSQL connections** (e.g., `psql`, client libraries, [connection
  poolers](/integrations/connection-pooling/)) use SCRAM-SHA-256 authentication
- **HTTP/Web Console connections** use standard password authentication

This hybrid approach provides maximum security for SQL connections while maintaining
compatibility with web-based tools.

### License Key

Starting in v26.0.0, Self-Managed Materialize requires a license key.

| License key type | Deployment type | Action |
| --- | --- | --- |
| Community | New deployments | <p>To get a license key:</p> <ul> <li>If you have a Cloud account, visit the <a href="https://console.materialize.com/license/" ><strong>License</strong> page in the Materialize Console</a>.</li> <li>If you do not have a Cloud account, visit <a href="https://materialize.com/self-managed/community-license/" >https://materialize.com/self-managed/community-license/</a>.</li> </ul> |
| Community | Existing deployments | Contact <a href="https://materialize.com/docs/support/" >Materialize support</a>. |
| Enterprise | New deployments | Visit <a href="https://materialize.com/self-managed/enterprise-license/" >https://materialize.com/self-managed/enterprise-license/</a> to purchase an Enterprise license. |
| Enterprise | Existing deployments | Contact <a href="https://materialize.com/docs/support/" >Materialize support</a>. |

For new deployments, you configure your license key in the Kubernetes Secret
resource during the installation process. For details, see the [installation
guides](/self-managed-deployments/installation/). For existing deployments, you can configure your
license key via:

```bash
kubectl -n materialize-environment patch secret materialize-backend -p '{"stringData":{"license_key":"<your license key goes here>"}}' --type=merge
```

### PostgreSQL: Source versioning

For PostgreSQL sources, starting in v26.0.0, Materialize introduces new syntax
for [`CREATE SOURCE`](/sql/create-source/postgres-v2/) and [`CREATE
TABLE`](/sql/create-table/) to allow better handle DDL changes to the upstream
PostgreSQL tables.

> **Note:** - This feature is currently supported for PostgreSQL sources, with
> additional source types coming soon.
> - Changing column types is currently unsupported.

For more information, see:
- [Guide: Handling upstream schema changes with zero
  downtime](/ingest-data/postgres/source-versioning/)
- [`CREATE SOURCE`](/sql/create-source/postgres-v2/)
- [`CREATE TABLE`](/sql/create-table/)

### Deprecation

The `inPlaceRollout` setting has been deprecated and will be ignored. Instead,
use the new setting `rolloutStrategy` to specify either:

- `WaitUntilReady` (*Default*)
- `ImmediatelyPromoteCausingDowntime`

For more information, see [`rolloutStrategy`](/self-managed-deployments/upgrading/#rollout-strategies).

### Terraform helpers

Corresponding to the v26.0.0 release, the following versions of the sample
Terraform modules have been released:

| Module | Description |
| --- | --- |
| <a href="https://github.com/MaterializeInc/materialize-terraform-self-managed/tree/main/aws" >Amazon Web Services (AWS)</a> | An example Terraform module for deploying Materialize on AWS. See <a href="/self-managed-deployments/installation/install-on-aws/" >Install on AWS</a> for detailed instructions usage. |
| <a href="https://github.com/MaterializeInc/materialize-terraform-self-managed/tree/main/azure" >Azure</a> | An example Terraform module for deploying Materialize on Azure. See <a href="/self-managed-deployments/installation/install-on-azure/" >Install on Azure</a> for detailed instructions usage. |
| <a href="https://github.com/MaterializeInc/materialize-terraform-self-managed/tree/main/gcp" >Google Cloud Platform (GCP)</a> | An example Terraform module for deploying Materialize on GCP. See <a href="/self-managed-deployments/installation/install-on-gcp/" >Install on GCP</a> for detailed instructions usage. |

 **Materialize on AWS:**

| Terraform version | Notable changes |
| --- | --- |
| <a href="https://github.com/MaterializeInc/terraform-aws-materialize/releases/tag/v0.6.4" >v0.6.4</a> | <ul> <li>Released as part of v26.0.0.</li> <li>Uses <code>terraform-helm-materialize</code> version <code>v0.1.35</code>.</li> </ul>  |

If upgrading from a deployment that was set up using an earlier version of the
Terraform modules, additional considerations may apply when using an updated Terraform modules to your existing deployments.

Click on the Terraform version link to go to the release-specific Upgrade Notes.

**Materialize on Azure:**

| Terraform version | Notable changes |
| --- | --- |
| <a href="https://github.com/MaterializeInc/terraform-azurerm-materialize/releases/tag/v0.6.4" >v0.6.4</a> | <ul> <li>Released as part of v26.0.0.</li> <li>Uses <code>terraform-helm-materialize</code> version <code>v0.1.35</code>.</li> </ul>  |

If upgrading from a deployment that was set up using an earlier version of the
Terraform modules, additional considerations may apply when using an updated
Terraform modules to your existing deployments.

See also Upgrade Notes for release specific notes.

**Materialize on GCP:**

| Terraform version | Notable changes |
| --- | --- |
| <a href="https://github.com/MaterializeInc/terraform-google-materialize/releases/tag/v0.6.4" >v0.6.4</a> | <ul> <li>Released as part of v26.0.0.</li> <li>Uses <code>terraform-helm-materialize</code> version <code>v0.1.35</code>.</li> </ul>  |

If upgrading from a deployment that was set up using an earlier version of the
Terraform modules, additional considerations may apply when using an updated
Terraform modules to your existing deployments.

See also Upgrade Notes for release specific notes.

**terraform-helm-materialize:**

| terraform-helm-materialize | Notes | Release date |
| --- | --- | --- |
| v0.1.35 | <ul> <li>Released as part of v26.0.0.</li> <li>Uses as default Materialize Operator version: <code>v26.0.0</code></li> </ul>  | 2025-11-18 |

#### Upgrade notes for v26.0.0

<ul>
<li>
<p>Upgrading to <code>v26.0.0</code> is a major version upgrade. To upgrade to <code>v26.0</code> from
<code>v25.2.X</code> or <code>v25.1</code>, you must first upgrade to <code>v25.2.16</code> and then upgrade to
<code>v26.0.0</code>.</p>
</li>
<li>
<p>For upgrades, the <code>inPlaceRollout</code> setting has been deprecated and will be
ignored. Instead, use the new setting <code>rolloutStrategy</code> to specify either:</p>
<ul>
<li><code>WaitUntilReady</code> (<em>Default</em>)</li>
<li><code>ImmediatelyPromoteCausingDowntime</code></li>
</ul>
<p>For more information, see
<a href="/self-managed-deployments/upgrading/#rollout-strategies" ><code>rolloutStrategy</code></a>.</p>
</li>
<li>
<p>New requirements were introduced for <a href="/releases/#license-key" >license keys</a>.
To upgrade, you will first need to add a license key to the <code>backendSecret</code>
used in the spec for your Materialize resource.</p>
<p>See <a href="/releases/#license-key" >License key</a> for details on getting your license
key.</p>
</li>
<li>
<p>Swap is now enabled by default. Swap reduces the memory required to
operate Materialize and improves cost efficiency. Upgrading to <code>v26.0</code>
requires some preparation to ensure Kubernetes nodes are labeled
and configured correctly. As such:</p>
<ul>
<li>
<p>If you are using the Materialize-provided Terraforms, upgrade to version
<code>v0.6.1</code> of the Terraform.</p>
</li>
<li>
<p>If you are <red><strong>not</strong></red> using a Materialize-provided Terraform, refer
to <a href="/self-managed-deployments/appendix/upgrade-to-swap/" >Prepare for swap and upgrade to v26.0</a>.</p>
</li>
</ul>
</li>
</ul>

See also [Version specific upgrade
notes](/self-managed-deployments/upgrading/#version-specific-upgrade-notes).

## See also

- [Release Schedule](/releases/schedule/)

---

## Materialize v26.29

---

## Materialize v26.28

---

## Materialize v26.27

---

## Materialize v26.26

---

## Materialize v26.25

---

## Materialize v26.24

---

## Materialize v26.23

---

## Materialize v26.22

---

## Materialize v26.21

---

## Materialize v26.20

---

## Materialize v26.19

---

## Materialize v26.18

---

## Materialize v26.17

---

## Materialize v26.16

---

## Materialize v26.15

---

## Materialize v26.14

---

## Materialize v26.13

---

## Materialize v26.12

---

## Materialize v26.11

---

## Materialize v26.10

---

## Materialize v26.9

---

## Materialize v26.8

---

## Materialize v26.7

---

## Materialize v26.6

---

## Materialize v26.5

---

## Materialize v26.4

---

## Materialize v26.3

---

## Materialize v26.2

---

## Materialize v26.1

---

## Materialize v26.0

---

## Materialize v0.164

---

## Materialize v0.163

---

## Materialize v0.162

---

## Materialize v0.161

---

## Materialize v0.160

---

## Materialize v0.159

---

## Materialize v0.158

---

## Materialize v0.157

---

## Materialize v0.156

---

## Materialize v0.155

---

## Materialize v0.154

---

## Materialize v0.153

---

## Materialize v0.152

---

## Materialize v0.151

---

## Materialize v0.150

---

## Materialize v0.149

---

## Materialize v0.148

---

## Materialize v0.147

---

## Materialize v0.146

---

## Materialize v0.145

---

## Materialize v0.144

---

## Materialize v0.143

---

## Materialize v0.142

---

## Materialize v0.141

---

## Materialize v0.140

---

## Materialize v0.139

---

## Materialize v0.138

---

## Materialize v0.137

---

## Materialize v0.136

---

## Materialize v0.135

---

## Materialize v0.134

---

## Materialize v0.133

---

## Materialize v0.132

---

## Materialize v0.131

---

## Materialize v0.130

---

## Materialize v0.129

---

## Materialize v0.128

---

## Materialize v0.127

---

## Materialize v0.126

---

## Materialize v0.125

---

## Materialize v0.124

---

## Materialize v0.123

---

## Materialize v0.122

---

## Materialize v0.121

---

## Materialize v0.120

---

## Materialize v0.118

---

## Materialize v0.117

---

## Materialize v0.116

---

## Materialize v0.115

---

## Materialize v0.114

---

## Materialize v0.113

---

## Materialize v0.112

---

## Materialize v0.111

---

## Materialize v0.110

## v0.110

---

## Materialize v0.109

---

## Materialize v0.108

## v0.108

#### Sources and sinks

* Allow specifying the message key format and the message value format
  separately in [Kafka sinks](/sql/create-sink/kafka/), using the new `KEY
  FORMAT ... VALUE FORMAT ...` option.

* Support including a header row in `CSV` files exported using [S3 bulk exports](/sql/copy-to/#copy-to-s3).

  ```mzsql
  COPY some_view TO 's3://mz-to-snow/csv/'
  WITH (
      AWS CONNECTION = aws_role_assumption,
      FORMAT = 'csv',
      HEADER = true
    );
  ```

#### SQL

* Add `hydration_time` to the [`mz_internal.mz_compute_hydration_statuses`](/reference/system-catalog/mz_internal/#mz_compute_hydration_statuses)
  system catalog view. This column shows the amount of time it took for a
  dataflow-powered object to hydrate (i.e., be backfilled with any pre-existing
  data).

#### Bug fixes and other improvements

* Disallow creating sinks that directly depend on system catalog objects ([#28122](https://github.com/MaterializeInc/materialize/issues/28122)).

---

## Materialize v0.107

## v0.107

#### Sources and sinks

* Support exporting data to Google Cloud Storage (GCS) using [AWS connections](/sql/create-connection/#aws)
  and the [`COPY TO`](/sql/copy-to/) command. While Materialize does not natively
  support Google Cloud Platform (GCP) connections, GCS is interoperable with
  Amazon S3 (via the [XML API](https://cloud.google.com/storage/docs/interoperability)),
  which allows GCP users to take advantage of [S3 bulk exports](/sql/copy-to/#copy-to-s3)
  also for GCS.

#### SQL

* Add the [`@>` and `<@` operators](/sql/types/list/#list-containment), which
  allow checking if a list contains the elements of another list. Like
  [array containment operators in PostgreSQL](https://www.postgresql.org/docs/current/functions-array.html#FUNCTIONS-ARRAY),
  list containment operators in Materialize **do not** account for duplicates.

  ```mzsql
  SELECT LIST[7,3,1] @> LIST[1,3,3,3,3,7] AS contains;
  ```
  ```nofmt
   contains
  ----------
   t
  ```

* Add `database_name` and `search_path` to the
  [mz_internal.mz_recent_activity_log](/reference/system-catalog/mz_internal/#mz_recent_activity_log)
  system catalog view. These columns show the value of the `database` and
  `search_path` configuration parameters at execution time, respectively.

* Add `connection_id` to the [mz_internal.mz_sessions](/reference/system-catalog/mz_internal/#mz_sessions)
  system catalog table. This column shows the connection ID of the session, which
  is unique for active sessions and corresponds to `pg_backend_pid()`.

#### Bug fixes and other improvements

* Move the `PROGRESS TOPIC REPLICATION FACTOR` option to the `CREATE CONNECTION`
  command for [Kafka connections](/sql/create-connection/#kafka)
  ([#27931](https://github.com/MaterializeInc/materialize/issues/27931)). The progress topic is a property of the connection, not the
  source or sink.

---

## Materialize v0.106

[//]: # "NOTE(morsapaes) v0.106 shipped support for the new `VALUE DECODING
ERRORS` clause behind a feature flag, which allows Kafka upsert sources to
continue ingesting data in the presence of decoding errors."

## v0.106

#### SQL

* Add support for the [`SHOW CREATE CLUSTER`](/sql/show-create-cluster/)
  command, which returns the DDL statement used to create a cluster.

  ```mzsql
  SHOW CREATE CLUSTER c;
  ```
  ```nofmt
      name          |    create_sql
  ------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
   c                | CREATE CLUSTER "c" (DISK = false, INTROSPECTION DEBUGGING = false, INTROSPECTION INTERVAL = INTERVAL '00:00:01', MANAGED = true, REPLICATION FACTOR = 1, SIZE = '100cc', SCHEDULE = MANUAL)
  ```

#### Bug fixes and other improvements

* Add the `mz_catalog_unstable` and [`mz_introspection`](/reference/system-catalog/mz_introspection/)
  system schemas to the system catalog, in support of the ongoing migration of
  unstable and replica introspection relations from the [`mz_internal`](/reference/system-catalog/mz_internal/)
  system schema into dedicated schemas.

* Add `introspection_debugging` and `introspection_interval` to the
  `mz_clusters` system catalog table. These columns are useful for feature
  development.

* Fix a bug in the [MySQL source](https://materialize.com/docs/sql/create-source/mysql/)
  that unecessarily enforced the `replica_preserve_commit_order` configuration
  parameter when connecting to a primary server for replication. This
  configuration parameter is only required when connecting to a MySQL
  read-replica.

---

## Materialize v0.105

---

## Materialize v0.104

---

## Materialize v0.103

---

## Materialize v0.102

---

## Materialize v0.101

## v0.101

#### Sources and sinks

* Allow configuring the initial and the maximum snapshot size for [load generator sources](/sql/create-source/load-generator/)
  via the new `AS OF` and `UP TO` `WITH` options.

#### SQL

* Disallow using the [`mz_now()` function](/sql/functions/now_and_mz_now/) in
  all positions and dependencies of `INSERT`, `UPDATE`, and `DELETE`
  statements.

#### Bug fixes and other improvements

* Extend `pg_catalog` and `information_schema` system catalog coverage for
  compatibility with Metaplane ([#27155](https://github.com/MaterializeInc/materialize/issues/27155)).

* Add details to errors related to insufficient privileges pointing to the
  missing permissions ([#27176](https://github.com/MaterializeInc/materialize/issues/27176)).

* Avoid resetting sink statistics when using the [`ALTER CONNECTION`](/sql/alter-connection/)
  command ([#27236](https://github.com/MaterializeInc/materialize/issues/27236)).

* Modify the output of the [`SHOW CREATE SOURCE`](/sql/show-create-source/)
  command for [load generator sources](/sql/create-source/load-generator/) to
  always include the `FOR ALL TABLES` clause, which is required ([#27250](https://github.com/MaterializeInc/materialize/issues/27250)).

---

## Materialize v0.100

## v0.100

#### SQL

* Add a [`MAP` expression](/sql/types/map/#construction) that allows constructing a `map`
  from a list of key–value pairs or a subquery.

  ```mzsql
  SELECT MAP['a' => 1, 'b' => 2];

       map
  -------------
   {a=>1,b=>2}
  ```

#### Bug fixes and other improvements

* Support the [`COPY TO`](/sql/copy-to/) command in the WebSocket API, so it's
  possible to run it from the SQL Shell.

---

## Materialize v0.99

## v0.99

#### Sources and sinks

* **Private preview.** Support exporting objects and query results to Amazon s3
    using the [`COPY TO`](/sql/copy-to/) command and [`AWS connections`](/sql/create-connection/#aws).
    Both CSV and Parquet are supported as file formats.

  **Syntax**

  ```mzsql
  CREATE CONNECTION s3_conn
   TO AWS (ASSUME ROLE ARN = 'arn:aws:iam::000000000000:role/Materializes3Exporter');

  COPY mv TO 's3://mz-to-s3/'
  WITH (
    AWS CONNECTION = aws_role_assumption,
    FORMAT = 'parquet'
  );
  ```

  It's important to note that this command isn't supported in the SQL Shell yet,
  but will be in the next release ([#27114](https://github.com/MaterializeInc/materialize/issues/27114)).

* Support ingesting datetime columns as text via the `TEXT COLUMNS` option in
  the [MySQL source](/sql/create-source/mysql/) to work around MySQL's _zero_
  value for datetime types (`0000-00-00`, `0000-00-00 00:00:00`), as well as
  other differences in the range of supported values between MySQL and
  PostgreSQL.

#### SQL

* **Private preview.** Support setting a history retention period for sources,
    tables, materialized views, and indexes via the new [`RETAIN HISTORY`](/transform-data/patterns/durable-subscriptions/#history-retention-period)
    option. This is useful to implement [durable subscriptions](/transform-data/patterns/durable-subscriptions/).

  **Syntax**

  ```mzsql
  ALTER MATERIALIZED VIEW winning_bids SET (RETAIN HISTORY FOR '2hr');
  ```

  ```mzsql
  ALTER MATERIALIZED VIEW winning_bids RESET (RETAIN HISTORY);
  ```

* Add [`mz_internal.mz_history_retention_strategies`](https://materialize.com/docs/reference/system-catalog/mz_internal/#mz_history_retention_strategies)
  to the system catalog. This table describes the history retention strategies
  for tables, sources, indexes, and materialized views that are configured with
  a history retention period.

* Add [`mz_internal.mz_materialized_view_refreshes`](https://materialize.com/docs/reference/system-catalog/mz_internal/#mz_materialized_view_refreshes)
  to the system catalog. This table shows the time of the last successfully
  completed refresh and the time of the next scheduled refresh for each
  materialized view with a refresh strategy other than `on-commit`.

#### Bug fixes and other improvements

* Allow `interval` types to be cast to `mz_timestamp` ([#26970](https://github.com/MaterializeInc/materialize/issues/26970)).

* Move the `mz_cluster_replica_sizes` system catalog table from the `mz_internal
  schema` to `mz_catalog`, making the table definition stable. Any queries
  referencing the `mz_internal.mz_cluster_replica_sizes` catalog table must be
  adjusted to use `mz_catalog.mz_cluster_replica_sizes` instead.

---

## Materialize v0.98

## v0.98

#### Sources and sinks

* Support writing metadata to Kafka message headers in [Kafka sinks](/sql/create-sink/kafka/)
  via the new [`HEADERS` option](/sql/create-sink/kafka/#headers).

* Allow dropping subsources in PostgreSQL sources using the [`DROP SOURCE`](/sql/drop-source/)
  command. The `ALTER SOURCE...DROP SUBSOURCE` command has been removed.

* Require the `CASCADE` option to drop PostgreSQL and MySQL sources with active
  subsources. Previously, dropping a PostgreSQL or MySQL source automatically
  dropped all the corresponding subsources.

* Allow changing the ownership of a subsource using the [`ALTER OWNER`](/sql/alter-owner/)
  command. Subsources may now have different owners to the parent source.

#### SQL

* Add [`mz_internal.mz_postgres_source_tables`](/reference/system-catalog/mz_internal/#mz_postgres_source_tables) and [`mz_internal.mz_mysql_source_tables`](/reference/system-catalog/mz_internal/#mz_mysql_source_tables)
to the system catalog. These tables .

---

## Materialize v0.97

## v0.97

#### Sources and sinks

* Optimize memory usage of large transaction processing in the [PostgreSQL](/sql/create-source/postgres/)
  and [MySQL](/sql/create-source/mysql/) sources.

#### SQL

* Add the [`initcap` function](/sql/functions/#initcap), which returns a given
  string with the first character of every word in upper case and all other
  characters in lower case.

  ```mzsql
  SELECT initcap('bye DrivEr');

    initcap
   ---------------------
    Bye Driver
   (1 row)
  ```

* Add [`mz_materialized_view_refresh_strategies`](/reference/system-catalog/mz_internal/#mz_materialized_view_refresh_strategies)
  and [`mz_cluster_schedules`](/reference/system-catalog/mz_internal/#mz_cluster_schedules)
  to the system catalog. These tables were added in support of ongoing feature
  development.

---

## Materialize v0.96

## v0.96

#### SQL

* Support `FORMAT CSV` in the `COPY .. TO STDOUT`
  command.

* Add [`mz_role_parameters`](/reference/system-catalog/mz_catalog/#mz_role_parameters)
  to the system catalog. This table contains a row for each parameter whose default
value has been altered for a given role using [ALTER ROLE ... SET](/sql/alter-role/#syntax).

#### Bug fixes and other improvements

* Fix the behavior of the [`translate`](https://materialize.com/docs/sql/functions/#translate)
  function when used with multibyte chars ([#26585](https://github.com/MaterializeInc/materialize/issues/26585)).

* Avoid panicking in the presence of composite keys in [`SUBSCRIBE`](/sql/subscribe/)
  commands using `ENVELOPE UPSERT` ([#26567](https://github.com/MaterializeInc/materialize/issues/26567)).

* Remove the unstable introspection relations
  `mz_internal.mz_compute_delays_histogram`,
  `mz_internal.mz_compute_delays_histogram_per_worker`, and
  `mz_internal.mz_compute_delays_histogram_raw`.

---

## Materialize v0.95

## v0.95

#### Sources and sinks

* Improve the readability of the output of the [`SHOW CREATE SOURCE`](/sql/show-create-source/)
  command for PostgreSQL and MySQL sources ([#26376](https://github.com/MaterializeInc/materialize/issues/26376)).

#### SQL

* Make the [`max_query_result_size`](/sql/set/#other-configuration-parameters)
  configuration parameter user-configurable. This parameter allows tuning the
  maximum size in bytes for a single query’s result.

* Improve the performance of the [`ALTER SCHEMA...SWAP WITH...`](https://materialize.com/docs/sql/alter-swap/)
  command ([#26361](https://github.com/MaterializeInc/materialize/issues/26361)), which speeds up [blue/green deployments](https://materialize.com/docs/manage/blue-green/).

* Support using the [`min()`](/sql/functions/#min) and [`max()`](/sql/functions/#max)
  functions with `time` values.

#### Bug fixes and other improvements

* Add the [`mz_probe`](/sql/show-clusters/#mz_probe-system-cluster) and
  [`mz_support`](/sql/show-clusters/#mz_support-system-cluster) system clusters
  to support internal monitoring tasks. Users are **not billed** for these
  clusters.

---

## Materialize v0.94

## v0.94

#### Sources and sinks

* Set subsources into an errored state in the [PostgreSQL source](/sql/create-source/postgres/)
  if the corresponding table is dropped from the publication upstream.

* Add a `KEY VALUE` load generator source,
  which produces keyed data that can be passed through to [`ENVELOPE UPSERT`](/sql/create-source/kafka/).
  This is useful for internal testing.

---

## Materialize v0.93

## v0.93

#### Sources and sinks

* Do not error if the `oid` or `typmod` of a column changes when using the `TEXT COLUMNS`
  option to ingest data as text in a [PostgreSQL source](/sql/create-source/postgres/).
  As an example, this allows evolving the structure of `enum` columns by using
  `ALTER TABLE <table> ALTER COLUMN <enum column> TYPE...`, which would
  previously have set the affected subsource into an errored state.

#### Bug fixes and other improvements

* Extend `pg_catalog` coverage with support for the [`obj_description()`](/sql/functions/#obj_description)
  and [`col_description`](https://materialize.com/docs/sql/functions/#col_description) functions.

---

## Materialize v0.92

## v0.92

#### SQL

* Adjust null handling in the [`to_jsonb`](https://materialize.com/docs/sql/functions/#to_jsonb)
  function to match PostgreSQL's behavior. The functin now returns `NULL` when
  its input is `NULL`, rather than returning the JSON `null` value.

* Add `timeline_id` to the `mz_internal.mz_postgres_sources` system catalog
  table. This column registers the PostgreSQL [timeline ID](https://www.postgresql.org/docs/current/continuous-archiving.html#BACKUP-TIMELINES)
  determined on source creation.

#### Bug fixes and other improvements

* Fix a panic when calling the [`to_jsonb`](https://materialize.com/docs/sql/functions/#to_jsonb)
  on a list containing `NULL` array values.

---

## Materialize v0.91

## v0.91

[//]: # "NOTE(morsapaes) v0.91 shipped support for EXPLAIN FILTER PUSHDOWN
behind a feature flag."

#### Sources and sinks

* **Private preview.** Add a new [MySQL source](/sql/create-source/mysql/),
  which allows propagating change data from MySQL (5.7+) databases in real-time
  using [GTID-based binlog replication](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html).

  **Syntax**

  ```mzsql
  CREATE SECRET mysqlpass AS '<MYSQL_PASSWORD>';

  CREATE CONNECTION mysql_connection TO MYSQL (
      HOST 'instance.foo000.us-west-1.rds.amazonaws.com',
      PORT 3306,
      USER 'materialize',
      PASSWORD SECRET mysqlpass
  );

  CREATE SOURCE mz_source
    FROM MYSQL CONNECTION mysql_connection
    FOR ALL TABLES;
  ```

    This source is compatible with MySQL managed services like
    [Amazon RDS for MySQL](/ingest-data/mysql/amazon-rds/),
    [Amazon Aurora MySQL](/ingest-data/mysql/amazon-aurora/),
    [Azure DB for MySQL](/ingest-data/mysql/azure-db/),
    and [Google Cloud SQL for MySQL](/ingest-data/mysql/google-cloud-sql/).

#### SQL

* Emit a notice if the `cluster` specified in the connection string used to
  connect to Materialize does not exist and the specified role does not have a
  default `cluster` set.

  ```bash
  NOTICE:  default cluster "quickstart" does not exist
  HINT:  Set a default cluster for the current role with ALTER ROLE <role> SET cluster TO <cluster>.
  psql (15.5 (Homebrew), server 9.5.0)
  Type "help" for help.

  materialize=>
  ```

#### Bug fixes and other improvements

* Bump the `max_connections` connection limit to `5000`, and enforce it for all
  users (including _superusers_).

* Correctly initialize source statistics in `mz_internal.mz_sources_statistics`
  when subsources are dropped and recreated using the `ALTER SOURCE...{ ADD |
  DROP } SUBSOURCE` command.

---

## Materialize v0.90

## v0.90

#### Sources and sinks

* Bump the maximum number of allowed concurrent connections in [wehbook sources](https://materialize.com/docs/sql/create-source/webhook/)
  from 250 to 500.

#### SQL

* Support using `LIKE`, `NOT LIKE`, `ILIKE`, and `NOT ILIKE` as operators within
  `ANY`, `SOME`, and `ALL` expressions.

* Add `mz_version` to the [`mz_internal.mz_recent_activity_log`](/reference/system-catalog/mz_internal/#mz_recent_activity_log)
  system catalog view. This column stores the version of Materialize that was
  running when the statement was executed.

#### Bug fixes and other improvements

* Fix the implementation of the `to_jsonb` function for `list` and `array`
  types ([#25536](https://github.com/MaterializeInc/materialize/issues/25536)). The return value is now a JSON array, rather than a
  JSON string literal containing the textual representation of the list or
  array.

---

## Materialize v0.89

## v0.89

#### Sources and sinks

* Improve source and sink statistics reporting to no longer reset on restarts,
  and include the following new metrics in [`mz_internal.mz_source_statistics`](https://materialize.com/docs/reference/system-catalog/mz_internal/#mz_source_statistics):

  | Metric                                        | Description                                                             |
  | --------------------------------------------- | ----------------------------------------------------------------------- |
  | `snapshot_records_known`                      | The size of the source's snapshot.                                      |
  | `snapshot_records_staged`                     | The amount of the source's snapshot Materialize has read.               |
  | `snapshot_committed`                          | Whether the initial snapshot for a source has been committed.           |
  | `offset_known`                                | The offset of the most recent data in the source's upstream service that Materialize knows about. |
  | `offset_committed`                            | The offset of the source's upstream service Materialize has fully committed.                      |

  These changes will be available in the Materialize console soon, so you can
  more easily monitor snapshot and ingestion progress for your sources.

#### SQL

* Remove the `mz_activity_log` system catalog view. These view was superseeded
by [`mz_recent_activity_log`](/reference/system-catalog/mz_internal/#mz_recent_activity_log),
which contains a log of the SQL statements that have been issued to
Materialize in the past 3 days.

* Add [`mz_internal.mz_compute_operator_hydration_statuses`](/reference/system-catalog/mz_internal/#mz_compute_operator_hydration_statuses)
to the system catalog. This table describes the dataflow operator hydration
status of compute objects (indexes or materialized views).

#### Bug fixes and other improvements

* Temporarily disallow `ALTER CONNECTION` commands on sources using the `UPSERT`
  envelope ([#25418](https://github.com/MaterializeInc/materialize/issues/25418)).

---

## Materialize v0.88

## v0.88

#### SQL

* Allow `LIMIT` expressions to contain parameters.

	```mzsql
	  PREPARE foo AS SELECT generate_series(1, 10) LIMIT $1;
	  EXECUTE foo (7::bigint);

	  generate_series
	  -----------------
	                 1
	                 2
	                 3
	                 4
	                 5
	                 6
	                 7
	```

#### Bug fixes and other improvements

* Fix a bug that potentially prevented timestamp with timezone data from being
  correctly parsed when ingested through PostgreSQL sources ([#25216](https://github.com/MaterializeInc/materialize/issues/25216)).

* Fix float parsing of certain zero values, such as `0.` and `.0` ([#25141](https://github.com/MaterializeInc/materialize/issues/25141)).

* Fix multiple bugs related to interval rounding ([#25202](https://github.com/MaterializeInc/materialize/issues/25202)).

---

## Materialize v0.87

## v0.87

#### Sources and sinks

* Add support for handling batched events formatted as `NDJSON` in the
  [webhook source](https://materialize.com/docs/sql/create-source/webhook/).

  ```mzsql
  CREATE SOURCE webhook_json IN CLUSTER quickstart FROM WEBHOOK
  BODY FORMAT JSON;

  -- Send multiple events delimited by newlines to the webhook source.
  HTTP POST to 'webhook_json'
    { 'event_type': 'foo' }
    { 'event_type': 'bar' }

  SELECT COUNT(*) FROM webhook_json;
  2
  ```

* Allow specifying a default AWS PrivateLink connection when creating a [Kafka connection over PrivateLink](https://materialize.com/docs/sql/create-connection/#aws-privatelink)
  using the `AWS PRIVATELINK` top-level option. The default connection will be
  used to connect to all brokers, and is exclusive with the `BROKER` and
  `BROKERS` options.

  ```mzsql
  CREATE CONNECTION privatelink_svc TO AWS PRIVATELINK (
      SERVICE NAME 'com.amazonaws.vpce.us-east-1.vpce-svc-0e123abc123198abc',
      AVAILABILITY ZONES ('use1-az1')
  );

  CREATE CONNECTION kafka_connection TO KAFKA (
      AWS PRIVATELINK (PORT 30292)
      SECURITY PROTOCOL = 'SASL_PLAINTEXT',
      SASL MECHANISMS = 'SCRAM-SHA-256',
      SASL USERNAME = 'foo',
      SASL PASSWORD = SECRET red_panda_password
  );
  ```

* Add `topic` to the [`mz_internal.mz_kafka_sources`](https://materialize.com/docs/reference/system-catalog/mz_catalog/#mz_kafka_sources)
  system catalog table. This column contains the name of the Kafka topic the
  source is reading from.

#### SQL

* Support user-configured data retention for tables via the `RETAIN HISTORY`
  syntax.

#### Bug fixes and other improvements

* Add a `node_ids` [output modifier](https://materialize.com/docs/sql/explain-plan/#output-modifiers)
for `EXPLAIN PHYSICAL PLAN` statements, to show the unique ID of each subplan in
the plan ([#24944](https://github.com/MaterializeInc/materialize/issues/24944)).

---

## Materialize v0.86

## v0.86

#### Sources and sinks

* Add support for [handling batched events](https://materialize.com/docs/sql/create-source/webhook/#handling-batch-events)
  in the webhook source via the new `JSON ARRAY` format.

  ```mzsql
  CREATE SOURCE webhook_source_json_batch IN CLUSTER my_cluster FROM WEBHOOK
  BODY FORMAT JSON ARRAY
  INCLUDE HEADERS;
  ```

  ```
  POST webhook_source_json_batch
  [
    { "event_type": "a" },
    { "event_type": "b" },
    { "event_type": "c" }
  ]
  ```

  ```mzsql
  SELECT COUNT(body) FROM webhook_source_json_batch;
  ----
  3
  ```

* Decrease memory utilization for [unpacking Kafka headers](https://materialize.com/docs/sql/create-source/kafka/#headers).
  Use the new `mapbuild` function to turn all headers exposed via `INCLUDE
  HEADERS` into a `map`, which makes it easier to extract header values.

   ```mzsql
   SELECT
       id,
       seller,
       item,
       convert_from(mapbuild(headers)->'client_id', 'utf-8') AS client_id,
       mapbuild(headers)->'encryption_key' AS encryption_key,
   FROM kafka_metadata;

    id | seller |        item        | client_id |    encryption_key
   ----+--------+--------------------+-----------+----------------------
     2 |   1592 | Custom Art         |        23 | \x796f75207769736821
     3 |   1411 | City Bar Crawl     |        42 | \x796f75207769736821
   ```

#### SQL

* Add support for new SQL functions:

  | Function                                        | Description                                                                                                 |
  | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
  | [`mapbuild`](/sql/functions/#map_build) | Builds a map from a list of records whose fields are two elements, the first of which is `text`.     |
  | [`map_agg`](/sql/functions/#map_agg)    | Aggregate keys and values (including nulls) as a map. |

#### Bug fixes and other improvements

* Mitigate queue saturation is Kafka sinks ([#24871](https://github.com/MaterializeInc/materialize/issues/24871)).

* Fix a correctness issue with subqueries that referred to ungrouped columns
  when columns of the same name existed in an outer scope ([#24354](https://github.com/MaterializeInc/materialize/issues/24354)).

* Fix casts from interval to time for large negative intervals ([#24795](https://github.com/MaterializeInc/materialize/issues/24795)).

* Prevent `INSERT`s with table references in `VALUES` in transactions ([#24697](https://github.com/MaterializeInc/materialize/issues/24697)).

---

## Materialize v0.85

## v0.85

#### SQL

* Add [`mz_internal.mz_recent_activity_log`](/reference/system-catalog/mz_internal/#mz_recent_activity_log)
  to the system catalog. This view contains a log of the SQL statements that have
  been issued to Materialize in the past 3 days, along with various metadata
  about them. Querying this view is typically much faster than querying
  `mz_internal.mz_activity_log`.

#### Bug fixes and other improvements

* Fix a bug where [`DISCARD ALL`](/sql/discard/) did not consider system or role
  defaults ([#24601](https://github.com/MaterializeInc/materialize/issues/24601)).

* Fix a bug causing the `mz_monitor` and `mz_monitor_redacted` system roles to
  not show up in the `mz_roles` system catalog table ([#24617](https://github.com/MaterializeInc/materialize/issues/24617)).

---

## Materialize v0.84

## v0.84

#### Sources and sinks

* **Breaking change.** Deprecate the `SIZE` option for sources and sinks, which
    transparently created a (linked) cluster to maintain the object. Use the
    `IN CLUSTER` clause to create a source or sink in a specific a cluster. If
    you omit the clause altogether, the object will be created in the active
    cluster for the session.

  **New syntax**

  ```mzsql
  --Create the object in a specific cluster
  CREATE SOURCE json_source
  IN CLUSTER some_cluster
  FROM KAFKA CONNECTION kafka_connection (TOPIC 'ch_anges')
  FORMAT JSON;

  --Create the object in the active cluster
  CREATE SOURCE json_source
  FROM KAFKA CONNECTION kafka_connection (TOPIC 'ch_anges')
  FORMAT JSON;
  ```

  **Deprecated syntax**

  ```mzsql
  --Create the object in a dedicated (linked) cluster
  CREATE SOURCE json_source
  FROM KAFKA CONNECTION kafka_connection (TOPIC 'ch_anges')
  FORMAT JSON
  WITH (SIZE = '3xsmall');
  ```

* Make timeouts (`transaction.timeout.ms`) configurable for
  [Kafka sinks](https://materialize.com/docs/sql/create-sink/). Default: 60000ms.

#### Bug fixes and other improvements

* Fix query results that rely on static views with temporal filters ([#24408](https://github.com/MaterializeInc/materialize/issues/24408)).

---

## Materialize v0.83

## v0.83

#### Sources and sinks

* Improve status reporting for [PostgreSQL sources](/sql/create-source/postgres/)
  by ensuring definite errors (e.g. dropping a publication upstream) are exposed.

#### Bug fixes and other improvements

* Prevent users from creating indexes on system catalog objects. If you're using
  these objects in a context that requires indexing, we recommend creating a
  view over the catalog objects, and indexing that view instead.

  ```mzsql
  CREATE VIEW mz_objects_indexed AS
  SELECT  o.id AS object_id,
          s.name AS schema_name
  FROM mz_objects o
  LEFT JOIN mz_schemas s ON o.schema_id = s.id;

  CREATE INDEX cara_tmp_i on mz_objects_indexed (object_id);
  ```

* Fix a bug that allowed users to configure clusters containing storage objects
  (i.e., sources, sinks) with more than one replica. This is an unsupported
  state, since such clusters can, at most, have `REPLICATION FACTOR = 1`.

---

## Materialize v0.82

## v0.82.0

[//]: # "NOTE(morsapaes) v0.82 shipped support for REFRESH options in
materialized views and statement lifecycle logging behind a feature flag."

#### Bug fixes and other improvements

* Rename the [pre-installed cluster](/sql/show-clusters/#pre-installed-clusters)
  from `default` to `quickstart` for **new** Materialize regions. In existing
  regions where the pre-installed cluster has not been renamed or dropped, this
  cluster retains the `default` name.

---

## Materialize v0.81

## v0.81.0

[//]: # "NOTE(morsapaes) v0.81 shipped a stub implementation of the MySQL source
behind a feature flag."

#### SQL

* Allow _superusers_ to modify the default value for certain [configuration parameters](/sql/set/#other-configuration-parameters)
  globally (i.e. for all users) using the[`ALTER SYSTEM...SET`](/sql/alter-system-set/)
  command.

* Support user-configured data retention for materialized views and sources
  (excluding multi-output sources, i.e. PostgreSQL sources) via the new `RETAIN
  HISTORY` syntax. Support in multi-output sources will be added in a future
  release.

* Add [`mz_hydration_statuses`](/reference/system-catalog/mz_internal/#mz_hydration_statuses)
  to the system catalog. This view describes the per-replica hydration status of
  each object powered by a dataflow.

#### Bug fixes and other improvements

* Rename `mz_compute_hydration_status` to [`mz_compute_hydration_statuses`](/reference/system-catalog/mz_internal/#mz_compute_hydration_statuses),
  for consistency with other objects in the system catalog.

* Fix a bug in which Avro-formatted Kafka sources could fail to decode records
  if the reader schema contained a field with a logical type of
  `timestamp-millis`, `timestamp-micros`, or `date` with a default value
  ([#24094](https://github.com/MaterializeInc/materialize/issues/24094)).

---

## Materialize v0.80

## v0.80.0

[//]: # "NOTE(morsapaes) v0.80 shipped support for expressions in the LIMIT
clause and AWS connections behind a feature flag."

#### Sources and sinks

* **Breaking change.** Disallow specifying more starting offsets than the number
    of partitions for [Kafka sources](/sql/create-source/kafka/#setting-start-offsets).

* Allow configuring the group ID (`GROUP ID PREFIX`) for [Kafka sources](/sql/create-source/kafka/),
  and the group ID and transactional ID (`TRANSACTIONAL ID PREFIX`, `PROGRESS GROUP ID PREFIX`)
  for [Kafka sinks](/sql/create-sink/kafka/#syntax)).

#### SQL

* Add `statement_kind` to `mz_internal.mz_activity_log`.
This column provides the type of the logged statement, e.g. `select` for a
`SELECT` query, or `NULL` if the statement was empty.

* Add [mz_internal.mz_notices](/reference/system-catalog/mz_internal/#mz_notices) to
  the system catalog. This view contains a list of currently active notices
  emitted by the system, and requires `superuser` privileges for querying.

#### Bug fixes and other improvements

* Allow bare references to tables, views, and sources whose name matches the
  name of a type.

---

## Materialize v0.79

## v0.79.0

#### Sources and sinks

* For [PostgreSQL sources](https://materialize.com/docs/sql/create-source/postgres/),
  prevent the creation of new sources when the upstream database does not have a
  sufficient number of replication slots available.

* Fix a bug where subsources where created in the active schema, rather than the
  schema of the source, when using the `FOR SCHEMAS` option in
  [PostgreSQL sources](https://materialize.com/docs/sql/create-source/postgres/).

* Add [`mz_aws_privatelink_connection_status_history`](/reference/system-catalog/mz_internal/#mz_aws_privatelink_connection_status_history)
  to the system catalog. This table contains a row describing the historical
  status for each [AWS PrivateLink connection](/sql/create-connection/#aws-privatelink)
  in the system.

#### SQL

* Add [`mz_compute_hydration_status`](/reference/system-catalog/mz_internal/#mz_compute_hydration_statuses)
  to the system catalog. This table describes the per-replica hydration status of
  indexes, materialized views, or subscriptions, which is useful to track when
  objects are "caught up" in the context of [blue/green deployments](/manage/blue-green).

* Add `create_sql` to object-specific tables in `mz_catalog`(_e.g._ `mz_sources`).
  This column provides the DDL used to create the object.

* Allow calling functions from the `mz_internal` schema, which are considered
  safe but unstable (_e.g._ `is_rbac_enabled`).

#### Bug fixes and other improvements

* Improve type coercion in `WITH MUTUALLY RECURSIVE` common table expressions. For
  example, you can now return `NUMERIC` values of arbitrary scales (_e.g._ `NUMERIC
  (38,2)` for columns defined as `NUMERIC`.

* Automatically enable compaction when creating the progress topic for a Kafka
  sink. **Warning:** Versions of Redpanda before v22.3 do not support using
  compaction for Materialize's progress topics. You need to manually create the
  connection's progress topic with compaction disabled to use sinks with these
  versions of Redpanda.

---

## Materialize v0.78

## v0.78.0

#### Sources and sinks

* **Breaking change.** Use `SSL` as the default security protocol in Kafka
    connections when no `SSL...` or `SASL...` options are specified.
    Previously, `PLAINTEXT` was used as the default.

* Add support for the `PLAINTEXT` and `SASL_PLAINTEXT` security protocols for
  Kafka connections.

* Allow Kafka connections to enable the `SSL` security protocol without enabling
  TLS client authentication (i.e., using TLS only for encryption).

* Add the [`INCLUDE HEADER` option](/sql/create-source/kafka/#headers) to Kafka
sources, which allows extracting individual headers from Kafka messages and
expose them as columns of the source.

  ```mzsql
  CREATE SOURCE kafka_metadata
    FROM KAFKA CONNECTION kafka_connection (TOPIC 'data')
    FORMAT AVRO USING CONFLUENT SCHEMA REGISTRY CONNECTION csr_connection
    INCLUDE HEADER 'c_id' AS client_id, HEADER 'key' AS encryption_key BYTES,
    ENVELOPE NONE
  ```

  ```mzsql
  SELECT
      id,
      seller,
      item,
      client_id::numeric,
      encryption_key
  FROM kafka_metadata;

  id | seller |        item        | client_id |    encryption_key
  ----+--------+--------------------+-----------+----------------------
    2 |   1592 | Custom Art         |        23 | \x796f75207769736821
    3 |   1411 | City Bar Crawl     |        42 | \x796f75207769736821
```

#### SQL

* Add [`mz_timezone_names`](/reference/system-catalog/mz_catalog/#mz_timezone_names)
and [`mz_timezone_abbreviations`](/reference/system-catalog/mz_catalog/#mz_timezone_abbreviations)
to the system catalog. These views contains a row for each supported timezone
and each supported timezone abbreviation, respectively.

---

## Materialize v0.77

## v0.77.0

#### Sources and sinks

* Support the `now()` function in the `CHECK` expression of [webhook sources](/sql/create-source/webhook/).
  This allows rejecting requests when a timestamp included in the headers is too
  far behind Materialize's clock, which is often recommended by webhook providers to
  help revent replay attacks.

  **Example**

  ```mzsql
  CREATE SOURCE webhook_with_time_based_rejection
  IN CLUSTER webhook_cluster
  FROM WEBHOOK
	  BODY FORMAT TEXT
	  CHECK (
	    WITH (HEADERS)
	    (headers->'timestamp'::text)::timestamp + INTERVAL '30s' >= now()
	  );
  ```

#### SQL

* Support using timezone abbreviations in contexts where timezone input is accepted.

  **Example**

  ```mzsql
  SELECT timezone_offset('America/New_York', '2023-11-05T06:00:00+00')
  ----
  (EST,-05:00:00,00:00:00)
  ```

* Add [`mz_internal.mz_materialization_lag`](/reference/system-catalog/mz_internal/#mz_materialization_lag)
  to the system catalog. This view describes the difference between the input
  frontiers and the output frontier for each materialized view, index, and sink
  in the system. For hydrated dataflows, this lag roughly corresponds to the time
  it takes for updates at the inputs to be reflected in the output.

#### Bug fixes and other improvements

* **Breaking change.** Fix timezone offset parsing ([#22896](https://github.com/MaterializeInc/materialize/issues/22896)) and remove
    support for the `time` type ([#22960](https://github.com/MaterializeInc/materialize/issues/22960)) in the `timezone` function
    and the `AT TIME ZONE` operator. These changes follow the PostgreSQL
    specification.

* Extend `pg_catalog` system catalog coverage to include the
  [`pg_timezone_abbrevs`](https://www.postgresql.org/docs/current/view-pg-timezone-abbrevs.html) and [`pg_timezone_names`](https://www.postgresql.org/docs/current/view-pg-timezone-names.html) views.
  This is useful to support custom timezone abbreviation logic while timezone
  support doesn't land in Materialize.

* Improve the output format of [`EXPLAIN...PLAN AS TEXT`](/sql/explain-plan/) when the `humanized_exprs`
  [output modifier](/sql/explain-plan/#output-modifiers) to avoid ambiguities when
  multiple columns have the same name.

---

## Materialize v0.76

## v0.76.0

#### Sources and sinks

* Allow specifying a default SSH connection when creating a [Kafka connection over SSH](https://materialize.com/docs/sql/create-connection/#ssh-tunnel-t1)
  using the `SSH TUNNEL` top-level option. The default connection will be used
  to connect to any new or unlisted brokers.

  ```mzsql
  CREATE CONNECTION kafka_connection TO KAFKA (
      BROKER 'broker1:9092',
      SSH TUNNEL ssh_connection
  );
  ```

* Support previewing the Avro schema that will be generated for an
  Avro-formatted [Kafka sink](/sql/create-sink/kafka/) ahead of sink creation
  using the [`EXPLAIN { KEY | VALUE } SCHEMA`](/sql/explain-schema/) syntax.

#### Bug fixes and other improvements

* Improve [connection validation](/sql/create-connection/#connection-validation)
  for Confluent Schema Registry connections. Materialize will now attempt to
  connect to the identified service, rather than only building the client during
  validation.

---

## Materialize v0.75

## v0.75.0

#### SQL

* Support [`ALTER [ CLUSTER | SCHEMA ] SWAP`](/sql/alter-swap/), which allows
  atomically renaming clusters and schemas. This is useful in the context of
  [Blue/Green deployments](/manage/blue-green/).

* Change the semantics and schema of the [`mz_internal.mz_frontiers`](https://materialize.com/docs/reference/system-catalog/mz_internal/#mz_frontiers)
  system catalog table, and add the [`mz_internal.mz_cluster_replica_frontiers`](https://materialize.com/docs/reference/system-catalog/mz_internal/#mz_cluster_replica_frontiers)
  system catalog table. These objects are mostly useful to support existing and
  upcoming features in Materialize.

#### Bug fixes and other improvements

* Remove the requirement of `USAGE` privileges on types for `SELECT` and
  `EXPLAIN` statements.

---

## Materialize v0.74

## v0.74.0

[//]: # "NOTE(morsapaes) v0.74 shipped the ALTER SCHEMA...RENAME command behind
a feature flag. This work makes progress towards supporting blue/green
deployments."

#### SQL

* Bring back support for [window aggregations](/sql/functions/#window-functions), or
  aggregate functions (e.g., `sum`, `avg`) that use an `OVER` clause.

  ```mzsql
  CREATE TABLE sales(time int, amount int);

  INSERT INTO sales VALUES (1,3), (2,6), (3,1), (4,5), (5,5), (6,6);

  SELECT time, amount, SUM(amount) OVER (ORDER BY time) AS cumulative_amount
  FROM sales
  ORDER BY time;

   time | amount | cumulative_amount
  ------+--------+-------------------
      1 |      3 |                 3
      2 |      6 |                 9
      3 |      1 |                10
      4 |      5 |                15
      5 |      5 |                20
      6 |      6 |                26
  ```

  For an overview of window function support, check the [updated documentation](/transform-data/patterns/window-functions/).

* Add support for new `SHOW` commands related to [role-based access control](/security/cloud/access-control/#role-based-access-control-rbac) (RBAC):

  | Command                                                    | Description                                          |
  | ---------------------------------------------------------- | ---------------------------------------------------- |
  | [`SHOW PRIVILEGES`](/sql/show-privileges/)                 | Lists the privileges granted on all objects.         |
  | [`SHOW ROLE MEMBERSHIP`](/sql/show-role-membership/)       | Lists the members of each role.                      |
  | [`SHOW DEFAULT PRIVILEGES`](/sql/show-default-privileges/) | Lists any default privileges granted on any objects. |

#### Bug fixes and other improvements

* Improve error message for possibly mistyped column names, suggesting similarly
  named columns if the one specified cannot be found.

  ```mzsql
  CREATE SOURCE case_sensitive_names
  FROM POSTGRES CONNECTION pg (
    PUBLICATION 'mz_source',
    TEXT COLUMNS [pk_table."F2"]
  )
  FOR TABLES (
    "enum_table"
  );
  contains: invalid TEXT COLUMNS option value: column "pk_table.F2" does not exist
  hint: The similarly named column "pk_table.f2" does exist.
  ```

* Fix a bug where `ASSERT NOT NULL` options on materialized views were not
  persisted across restarts of the environment.

---

## Materialize v0.73

## v0.73.0

[//]: # "NOTE(morsapaes) v0.73 shipped the ASSERT NOT NULL option for sinks
behind a feature flag."

#### Sources and sinks

* **Private preview.** Allow propagating comments in materialized views to the
    Avro schema of [Kafka sinks](/sql/create-sink/kafka/), as well as manually
    specifying comments using the new `[KEY|VALUE] DOC ON
    [TYPE|COLUMN] <identifier>` [connection option](/sql/create-sink/kafka/#syntax).

    **Example:**

	```mzsql
	CREATE TABLE t (c1 int, c2 text);
	COMMENT ON TABLE t IS 'materialize comment on t';
	COMMENT ON COLUMN t.c2 IS 'materialize comment on t.c2';

	CREATE SINK avro_sink
	  IN CLUSTER my_io_cluster
	  FROM t
	  INTO KAFKA CONNECTION kafka_connection (TOPIC 'test_avro_topic')
	  KEY (c1)
	  FORMAT AVRO USING CONFLUENT SCHEMA REGISTRY CONNECTION csr_connection
	  (
	    DOC ON TYPE t = 'top-level comment for avro record in both key and value schemas',
	    KEY DOC ON COLUMN t.c1 = 'comment on column only in key schema',
	    VALUE DOC ON COLUMN t.c1 = 'comment on column only in value schema'
	  )
	  ENVELOPE UPSERT;
	```

	**Key schema:**
	```json
	{
	  "type": "record",
	  "name": "row",
	  "doc": "this is a materialized view",
	  "fields" : [
	    {"name": "a", "type": "string", "doc": "this is column a"},
	    {"name": "b", "type": "string"}
	  ]
	}{
	  "type": "record",
	  "name": "row",
	  "doc": "top-level comment for avro record in both key and value schemas",
	  "fields": [
	    {
	      "name": "c1",
	      "type": [
	        "null",
	        "int"
	      ],
	      "doc": "comment on column only in key schema"
	    }
	  ]
	}
	```

	**Value schema:**

	```json
	{
	  "type": "record",
	  "name": "envelope",
	  "doc": "top-level comment for avro record in both key and value schemas",
	  "fields": [
	    {
	      "name": "c1",
	      "type": [
	        "null",
	        "int"
	      ],
	      "doc": "comment on column only in value schema"
	    },
	    {
	      "name": "c2",
	      "type": [
	        "null",
	        "string"
	      ],
	      "doc": "materialize comment on t.c2"
	    }
	  ]
	}
	```

#### Bug fixes and other improvements

* Allow the value of the `SASL MECHANISM` option for [Kafka connections](/sql/create-connection/#kafka)
to be specified in any case style. Previously, Materialize only accepted
uppercase case style (as required by `librdkafka`).

---

## Materialize v0.72

## v0.72.0

#### Bug fixes and other improvements

* Refactor [`mz_internal.mz_dataflow_arrangement_sizes`](/reference/system-catalog/mz_introspection/#mz_dataflow_arrangement_sizes)
to include **all active dataflows**, not just the ones referenced from the
system catalog. This makes debugging issues like high memory usage caused by
arrangements more intuitive for users.

---

## Materialize v0.71

## v0.71.0

[//]: # "NOTE(morsapaes) v0.71 shipped setting configuration parameters for roles
behind a feature flag."

#### Sources and sinks

* Support using the new `NULL DEFAULTS` option in Avro-formatted [Kafka sinks](/sql/create-sink/).
When specified, this option will generate an Avro schema where every nullable
field has a default of `NULL`.

#### SQL

* Add the [`EXPLAIN CREATE { MATERIALIZED VIEW | INDEX }`](/sql/explain-plan/#explained-object)
syntax options, which allow exploring what plan Materialize would create if one
were to re-create the object with the current catalog state.

---

## Materialize v0.70

## v0.70.0

#### Sources and sinks

* Automatically check if there are tables not currently configured to use `REPLICA IDENTITY FULL` in a publication used with a [PostgreSQL source](/sql/create-source/postgres/).

* Support constraining the precision of the fractional seconds in timestamps. This allows users to construct Avro-formatted sinks that use the `timestamp-millis` logical type instead of the `timestamp-micros` logical type.

#### Bug fixes and other improvements

* Limit the amount of data that can be copied using `COPY FROM` to 1 GiB. Please [contact us](https://materialize.com/contact/) if you need this limit increased in your Materialize region.

* Restrict transactions to execute on a single cluster, in order to improve use case isolation. The first query in a transaction now determines the time domain of the entire transaction ([#21854](https://github.com/MaterializeInc/materialize/issues/21854)).

---

## Materialize v0.69

## v0.69.0

#### Sources and sinks

[//]: # "NOTE(morsapaes) This feature was released in v0.59 behind a feature
flag. The flag was raised in v0.69 — so mentioning it here."

* Support validating the parameters provided in a `CREATE CONNECTION` statement
  against the target external system. For most connection types,
  Materialize **automatically validates** connections on creation.

  For connection types that require additional setup steps after creation
  (AWS PrivateLink, SSH tunnel), you can **manually validate** connections
  using the new [`VALIDATE CONNECTION`](https://materialize.com/docs/sql/validate-connection/)
  syntax:

   ```mzsql
   VALIDATE CONNECTION ssh_connection;
   ```

#### SQL

* Add support for new SQL functions:

  | Function                                                           | Description                                                 |
  | ------------------------------------------------------------------ | ----------------------------------------------------------- |
  | [`mz_is_superuser`](/sql/functions/#access-privilege-inquiry-functions) |  Reports whether the current role is a _superuser_ with administration privileges in Materialize. |
  | [`regexp_replace`](/sql/functions/#string-functions) | Replaces the first occurrence of the specified regular expression in a string with the specified replacement string.    |
  | [`regexp_split_to_array`](/sql/functions/#string-functions)      | Splits a string by the specified regular expression into an array. |
  | [`regexp_split_to_table`](/sql/functions/#table-functions)       | Splits a string by the specified regular expression.               |

<br>

* Add the `IN CLUSTER` option to the `SHOW { SOURCES | SINKS }` commands to
  restrict the objects listed to a specific cluster.

  ```mzsql
  SHOW SOURCES;
  ```
  ```nofmt
              name    | type     | size  | cluster
  --------------------+----------+-------+---------
   my_kafka_source    | kafka    |       | c1
   my_postgres_source | postgres |       | c2
  ```

  ```mzsql
  SHOW SOURCES IN CLUSTER c2;
  ```
  ```nofmt
  name       | type  | size     | cluster
  -----------+-------+----------+--------
  my_postgres_source | postgres | c2
  ```

* Make the syntax for [`GROUP SIZE` query hints](/transform-data/optimization/#query-hints)
  more intuitive by deprecating the `EXPECTED GROUP SIZE` hint and introducing
  three new hints: `AGGREGATE INPUT GROUP SIZE`, `DISTINCT ON INPUT GROUP SIZE`
  and `LIMIT INPUT GROUP SIZE`; which more clearly map to the target operation
  to optimize.

  The old `EXPECTED GROUP SIZE` hint is still supported for backwards
  compatibility, but its use is discouraged.

* Add `savings` to the [`mz_internal.mz_expected_group_size_advice`](/reference/system-catalog/mz_introspection/#mz_expected_group_size_advice)
  system catalog table. This column provides a conservative estimate of the memory
  savings that can be expected by using [`GROUP SIZE` query hints](/transform-data/optimization/#query-hints).

#### Bug fixes and other improvements

* Support SQL parameters in `SUBSCRIBE` and `DECLARE` statements.

---

## Materialize v0.68

## v0.68.0

[//]: # "NOTE(morsapaes) v0.68 includes a first version of the COMMENT ON syntax
released behind a feature flag."

#### SQL

* Enable Role-based access control (RBAC) for all new environments. Check the
  [updated documentation](/security/access-control/) for guidance on setting up
  RBAC in your Materialize organization.

* Extend the [`EXPLAIN PLAN`](/sql/explain-plan/) syntax to allow explaining
  plans used for index maintenance.

#### Bug fixes and other improvements

* Extend `pg_catalog` and `information_schema` system catalog coverage for
  compatibility with Power BI.

---

## Materialize v0.67

## v0.67.0

#### Sources and sinks

[//]: # "NOTE(morsapaes) This feature was released in v0.53 behind a feature
flag. The flag was raised in v0.67 for ENVELOPE UPSERT -— so mentioning it
here."

* Support upserts in the output of `SUBSCRIBE` via the new [`ENVELOPE UPSERT` clause](/sql/subscribe/#envelope-upsert).
  This clause allows you to specify a `KEY` that Materialize uses to interpret the
  rows as a series of inserts, updates and deletes within each distinct
  timestamp. The output rows will have the following structure:

  ```mzsql
   SUBSCRIBE mview ENVELOPE UPSERT (KEY (key));

   mz_timestamp | mz_state | key  | value
   -------------|----------|------|--------
   100          | upsert   | 1    | 2
   100          | upsert   | 2    | 4
  ```

#### SQL

* Add [`mz_internal.mz_compute_dependencies`](/reference/system-catalog/mz_internal/#mz_compute_dependencies)
  to the system catalog. This table describes the dependency structure between
  each compute object (index, materialized view, or subscription) and the
  sources of its data.

* Improve the output of [`EXPLAIN { OPTIMIZED | PHYSICAL } PLAN FOR MATERIALIZED VIEW`](/sql/explain-plan/)
  to return the plan generated at object creation time, rather than the plan that
  would be generated if the object was created with the current catalog state.

* Add support for [`TABLE`](/sql/table) expressions, which retrieve all rows
  from the named SQL table.

#### Bug fixes and other improvements

* Extend `pg_catalog` and `information_schema` system catalog coverage for
  compatibility with Power BI.

* Increase in precision for the `AVG`, `VAR_*`, and `STDDEV*` functions.

---

## Materialize v0.66

## v0.66.0

This release focuses on stabilization work and performance improvements. It does
not introduce any new user-facing features. 👷

#### Bug fixes and other improvements

* Fix a bug that prevented [`ALTER SOURCE...`](/sql/alter-source/) from
  completing in PostgreSQL sources when existing tables were listed in a
  publication in a different order than that observed when Materialize first
  processed them.

---

## Materialize v0.65

## v0.65.0

#### SQL

* **Breaking change.** Limit the length of object identifiers to 255 bytes.

* Include the name and size of cluster replicas in the output of
  [`SHOW CLUSTERS`](/sql/show-clusters/) as a new column named `replicas`.

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Add the [`SHOW ROLES`](/sql/show-roles/) command, which lists the roles
    available in the system.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

* Add [`mz_internal.mz_object_fully_qualified_names`](/reference/system-catalog/mz_internal/#mz_object_fully_qualified_names)
  and [`mz_internal.mz_object_lifetimes`](/reference/system-catalog/mz_internal/#mz_object_lifetimes)
  to the system catalog. These views enrich [`mz_objects`](/reference/system-catalog/mz_catalog/#mz_objects)
  with namespace and lifetime event information, respectively.

* Add [`mz_internal.mz_expected_group_size_advice`](/reference/system-catalog/mz_introspection/#mz_expected_group_size_advice)
  to the system catalog. This view provides advice on opportunities to set the
  `EXPECTED GROUP SIZE` [query hint](https://materialize.com/docs/sql/select/#query-hints).

#### Bug fixes and other improvements

* **Breaking change.** Disallow executing functions from the `mz_internal`
    schema ([#20998](https://github.com/MaterializeInc/materialize/issues/20998)). This change should have no user impact, but
    please [let us know](https://materialize.com/s/chat) if you run into any
    issues.

---

## Materialize v0.64

## v0.64.0

#### SQL

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Require specifying a target role in the `ALTER DEFAULT PRIVILEGES` command.
    Previously, the target role was optional and defaulted to the current role,
    which is seldom what users intend to achieve with this command.

  * Add the `has_role` function as an alias to `pg_has_role`. This function
    reports if a specified `user` has `USAGE` or `MEMBER` privileges for a
    specified `role`.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

#### Bug fixes and other improvements

* Fix a bug that let users specify the `DETAILS` option when creating a
  [PostgreSQL source](/sql/create-source/postgres/) ([#20944](https://github.com/MaterializeInc/materialize/issues/20944)).

* Extend support for single DDL statements in explicit transactions to the
  `ALTER` and `DROP` commands. This improves the integration experience with
  external tools like [Deepnote](https://deepnote.com/) and [Hex](https://hex.tech/).

---

## Materialize v0.63

## v0.63.0

#### SQL

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Require `USAGE` privileges on the schemas of all connections, secrets, and types used in a query.

  * Add system catalog views that present privileges and role memberships using
    human-readable names instead of identifiers. Each view has two variants:
    one that presents all privileges or roles, and another that only presents
    privileges and roles that contain the current role.

    **Privileges**

    * [`mz_internal.mz_show_all_privileges`](/reference/system-catalog/mz_internal/#mz_show_all_privileges)
    * [`mz_internal.mz_show_[my_]cluster_privileges`](/reference/system-catalog/mz_internal/#mz_show_cluster_privileges)
    * [`mz_internal.mz_show_[my_]database_privileges`](/reference/system-catalog/mz_internal/#mz_show_database_privileges)
    * [`mz_internal.mz_show_[my_]default_privileges`](/reference/system-catalog/mz_internal/#mz_show_default_privileges)
    * [`mz_internal.mz_show_[my_]object_privileges`](/reference/system-catalog/mz_internal/#mz_show_object_privileges)
    * [`mz_internal.mz_show_[my_]schema_privileges`](/reference/system-catalog/mz_internal/#mz_show_schema_privileges)
    * [`mz_internal.mz_show_[my_]system_privileges`](/reference/system-catalog/mz_internal/#mz_show_system_privileges)

    **Roles**

    * [`mz_internal.mz_show_[my_]role_members`](/reference/system-catalog/mz_internal/#mz_show_role_members)

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

#### Bug fixes and other improvements

* Add the `max_query_result_size` [configuration parameter](https://materialize.com/docs/sql/show/#other-configuration-parameters),
which allows limiting the size in bytes of a single query’s result.

* Support most single DDL statements in explicit transactions. This improves the
  integration experience with external tools like [Deepnote](https://deepnote.com/)
  and [Hex](https://hex.tech/).

---

## Materialize v0.62

## v0.62.0

#### Sources and sinks

* Support adding individual subsources in the [PostgreSQL source](/sql/create-source/postgres/)
  using the new `ALTER SOURCE...ADD SUBSOURCE` syntax.

#### SQL

* Add the [`try_parse_monotonic_iso8601_timestamp`](/sql/functions/pushdown/)
  function, which should be used in temporal filters involving `string` timestamps
  (e.g. extracted from `jsonb` columns) to benefit from [filter pushdown optimization](/transform-data/patterns/temporal-filters/#temporal-filter-pushdown).

  For a given JSON-formatted source, the following query cannot
  benefit from filter pushdown:

  ```mzsql
  SELECT *
  FROM foo
  WHERE (data ->> 'timestamp')::timestamp > mz_now();
  ```

  But can be optimized as:

  ```mzsql
  SELECT *
  FROM foo
  WHERE try_parse_monotonic_iso8601_timestamp(data ->> 'timestamp') > mz_now();
  ```

  It's important to note that temporal filter pushdown is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Add the `pg_has_role` function, which reports if a specified `user` has
    `USAGE` or `MEMBER` privileges for a specified `role`.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

#### Bug fixes and other improvements

* Extend `information_schema` system catalog coverage with RBAC-specific views:

  * [`applicable_roles`](https://www.postgresql.org/docs/15/infoschema-applicable-roles.html)
  * [`enabled_roles`](https://www.postgresql.org/docs/15/infoschema-enabled-roles.html)
  * [`role_table_grants`](https://www.postgresql.org/docs/15/infoschema-role-table-grants.html)
  * [`table_privileges`](https://www.postgresql.org/docs/15/infoschema-table-privileges.html)

---

## Materialize v0.61

## v0.61.0

[//]: # "NOTE(morsapaes) v0.61 includes a first version of webhook sources
released behind a feature flag."

#### SQL

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Include `GRANT`, `REVOKE`, `ALTER DEFAULT PRIVILEGES`, and `ALTER OWNER`
    events in the [`mz_audit_events`](/reference/system-catalog/mz_catalog/#mz_audit_events)
    system catalog table.

  * Require connection and secret `USAGE` privileges to execute [`CREATE SINK`](/sql/create-sink/)
    commands.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

#### Bug fixes and other improvements

* Do not require a valid active cluster to run specific types of queries, like
  `SELECT n` health checks ([#20420](https://github.com/MaterializeInc/materialize/issues/20420)). This fixes a known issue in the
  `dbt-materialize` adapter, where specific commands that run such queries as
  part of their execution (e.g. `dbt debug`) would fail in the absence of the
  pre-installed `default` cluster.

* Extend `pg_catalog` and `information_schema` system catalog coverage for
  compatibility with external tools like DBeaver and PopSQL ([#20429](https://github.com/MaterializeInc/materialize/issues/20429))
  ([#20314](https://github.com/MaterializeInc/materialize/issues/20314)) ([#20427](https://github.com/MaterializeInc/materialize/issues/20427)).

* Avoid panicking in the presence of concurrent DDL and `UPDATE`, `DELETE`, or
  `INSERT INTO` statements ([#20420](https://github.com/MaterializeInc/materialize/issues/20420)).

---

## Materialize v0.60

## v0.60.0

#### Sources and sinks

* **Private preview.** Support filter pushdown, which can substantially improve
    latency for queries using temporal filters. For an overview of this new
    optimization mechanism, check the [updated documentation](/transform-data/patterns/temporal-filters/#temporal-filter-pushdown).

[//]: # "NOTE(morsapaes) This feature was released in v0.53 behind a feature
flag. The flag was raised in v0.60 -— so mentioning it here."

* Support `FORMAT JSON` for [Kafka sources](/sql/create-source/kafka/).
  This format option automatically decodes messages as `jsonb`, which is a
  quality-of-life improvement over JSON handling using `FORMAT BYTES`.

  **New syntax**

  ```mzsql
  CREATE SOURCE json_source
  FROM KAFKA CONNECTION kafka_connection (TOPIC 'ch_anges')
  FORMAT JSON
  WITH (SIZE = '3xsmall');

  CREATE VIEW extract_json_source AS
  SELECT
    (data->>'field1')::boolean AS field_1,
    (data->>'field2')::int AS field_2,
    (data->>'field3')::float AS field_3
  -- Automatic conversion to jsonb
  FROM json_source;
  ```

  **Old syntax**

  ```mzsql
  CREATE SOURCE json_source
  FROM KAFKA CONNECTION kafka_connection (TOPIC 'ch_anges')
  FORMAT BYTES
  WITH (SIZE = '3xsmall');

  CREATE VIEW extract_json_source AS
  SELECT
    (data->>'field1')::boolean AS field_1,
    (data->>'field2')::int AS field_2,
    (data->>'field3')::float AS field_3
  -- Manual conversion to jsonb
  FROM (SELECT CONVERT_FROM(data, 'utf8')::jsonb AS data FROM json_source);
  ```

#### SQL

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Restrict granting and revoking [system privileges](/security/access-control/manage-roles/)
    to _superuser_ users with admin privileges.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

#### Bug fixes and other improvements

* Fix timestamp generation for transactions with multiple statements that could
  lead to crashes ([#20267](https://github.com/MaterializeInc/materialize/issues/20267)).

---

## Materialize v0.59

## v0.59.0

#### Sources and sinks

* Support dropping individual subsources in the [PostgreSQL source](/sql/create-source/postgres/)
using the new `ALTER SOURCE...DROP SUBSOURCE` syntax. Adding subsources will be
supported in the next release.

#### SQL

* Support parsing multi-dimensional arrays, including multi-dimensional empty arrays.

  ```mzsql
  materialize=> SELECT '{{1}, {2}}'::int[];
     arr
  -----------
   {{1},{2}}
  (1 row)
  ```

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * **Breaking change.** Replace role attributes with system privileges, which
      are inheritable and applied system-wide. This change improves the
      usability of RBAC by consolidating the semantics controlling role
      privileges, making it less cumbersome for admin users to grant(or revoke)
      privileges to manipulate top level objects to multiple users.

  * **Breaking change.** Remove the `create_role`, `create_db`, and
      `create_cluster` from the `mz_roles` system catalog table.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

#### Bug fixes and other improvements

* Make error messages using object names more consistent. In particular, error
  messages now consistently use the fully qualified object name
  (`database_name.schema_name.item_name`).

* **Breaking change.** Disallow `SHOW` commands in the creation of views and
    materialized views ([#20257](https://github.com/MaterializeInc/materialize/issues/20257)). This change should have no user
    impact, but please [let us know](https://materialize.com/s/chat) if you run
    into any issues.

---

## Materialize v0.58

## v0.58.0

#### SQL

* Add support for new SQL functions:

  | Function                                        | Description                                                                                                 |
  | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
  | [`datediff`](/sql/functions/datediff/)  | Returns the difference between two date, time or timestamp expressions based on the specified date or time part.     |
  | [`pg_cancel_backend`](/sql/functions/#pg_cancel_backend)    | Cancels an in-progress query on the specified connection ID. Returns whether the connection ID existed. |

* Accept [scalar functions](/sql/functions/#scalar-functions) in the `FROM` clause of a query.

* Add support for the PostgreSQL `IS DISTINCT FROM` operator. This operator
  behaves like `<>`, except that it treats `NULL` like a normal value that
  compares equal to itself and not equal to all other values.

* Allow specifying a comma-separated list of schemas in the `DROP SCHEMA`.

* Add [`mz_internal.mz_object_transitive_dependencies`](/reference/system-catalog/mz_internal/#mz_object_transitive_dependencies)
  to the system catalog. This table describes the transitive dependency structure between all database objects in the system.

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Allow specifying multiple role names in the [`GRANT ROLE`](/sql/grant-role)
    and [`REVOKE ROLE`](/sql/revoke-role) commands.

  * Add the [`ALTER DEFAULT PRIVILEGES`](/sql/alter-default-privileges/) command,
    which allows users to configure the default privileges for newly created
    objects.

  * Add the `has_system_privilege` function to query role's system privileges,
    which reports if a specified user has a system privilege.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

---

## Materialize v0.57

## v0.57.0

#### SQL

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Allow specifying multiple database objects in the [`GRANT PRIVILEGE`](/sql/grant-privilege)
    and [`REVOKE PRIVILEGE`](/sql/revoke-privilege) commands.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

* Add `RESET schema` as an alias to `RESET search_path`. From this release, the
  following sequence of commands provide the same functionality:

  ```mzsql
  materialize=> SET schema = finance;
  SET
  materialize=> SHOW schema;
   schema
  ---------
   finance
  (1 row)

  materialize=> RESET schema;
  RESET
  materialize=> SHOW schema;
   schema
  --------
   public
  (1 row)
  ```

  ```mzsql
   materialize=> SET search_path = finance, public;
   SET
   materialize=> SELECT current_schema;
    current_schema
   ----------------
    finance
   (1 row)

   materialize=> RESET schema;
   RESET
   materialize=> SELECT current_schema;
    current_schema
   ----------------
    public
   (1 row)
  ```

* Add support for new SQL functions:

  | Function                                        | Description                                                                                                 |
  | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
  | [`array_position`](/sql/functions/#array-functions)  | Returns the subscript of the first occurrence of the second argument in the array. `NULL` if not found.     |
  | [`parse_ident`](/sql/functions/#string-functions)    | Splits a qualified identifier into an array of identifiers, removing any quoting of individual identifiers. |

#### Bug fixes and other improvements

* **Breaking change.** Change the `type` associated with progress subsources in
    the `mz_sources` system catalog table from `subsource` to `progress`. This
    change should have no user impact, but please [let us know](https://materialize.com/s/chat)
    if you run into any issues.

* **Breaking change.** Add `oid` and re-order the columns of the `mz_secrets`
    system catalog table. This change should have no user impact, but please
    [let us know](https://materialize.com/s/chat) if you run into any issues.

* Avoid panicking in the absence of the default `materialize` database ([#19874](https://github.com/MaterializeInc/materialize/issues/19874)).

---

## Materialize v0.56

## v0.56.0

#### Sources and sinks

* Add a `MARKETING` [load generator source](/sql/create-source/load-generator/#marketing),
  which provides synthetic data to simulate Machine Learning scenarios.

#### SQL

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Add the `has_table_privilege` access control function, which allows a role
    to query if it has privileges on a specific relation:

    ```mzsql
    SELECT has_table_privilege('marta','auction_house','select');

	 has_table_privilege
	---------------------
	 t
	(1 row)
    ```

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

---

## Materialize v0.55

## v0.55.0

#### SQL

* Add `SET schema` and `SHOW schema` as aliases to `SET search_path` and `SELECT
  current_schema`, respectively. From this release, the following sequence of
  commands provide the same functionality:

  ```mzsql
  materialize=> SET schema = finance;
  SET
  materialize=> SHOW schema;
   schema
  ---------
   finance
  (1 row)
  ```

  ```mzsql
   materialize=> SET search_path = finance, public;
   SET
   materialize=> SELECT current_schema;
    current_schema
   ----------------
    finance
   (1 row)
  ```

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Add support for the [`REASSIGN OWNED`](/sql/reassign-owned/) command, which
    allows reassigning the ownership of objects owned by one or more roles to a
    different role.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

---

## Materialize v0.54

## v0.54.0

#### SQL

* Add [`mz_internal.mz_cluster_replica_history`](/reference/system-catalog/mz_internal/#mz_cluster_replica_history)
  to the system catalog. This view contains information about the timespan of
  each replica, including the times at which it was created and dropped (if
  applicable).

* Add `envelope_state_bytes` and `envelope_state_count` to the
  [`mz_internal.mz_source_statistics`](/reference/system-catalog/mz_internal/#mz_source_statistics)
  system catalog table. These columns provide an approximation of the state
  size maintained for upsert sources (i.e. sources using `ENVELOPE
  UPSERT` or `ENVELOPE DEBEZIUM`). In the future, this will allow users to
  relate upsert state size to disk utilization.

* Improve and extend the base implementation of **Role-based
  access control** (RBAC):

  * Consider privileges on database objects when executing statements. If RBAC
    is enabled, Materialize will check the privileges for a role before
    executing any statements.

  * Improve the `GRANT` and `REVOKE` privilege commands to support multiple
    roles, as well as the `ALL` keyword to indicate that all privileges should
    be granted or revoked.

    ```mzsql
    GRANT SELECT ON mv TO joe, mike;

    GRANT ALL ON CLUSTER dev TO joe;
    ```

  * Add support for the [`DROP OWNED`](/sql/drop-owned/) command, which drops
    all the objects that are owned by one of the specified roles from a
    Materialize region. Any privileges granted to the given roles on objects
    will also be revoked.

  It's important to note that role-based access control (RBAC) is **disabled by
  default**. You must [contact us](https://materialize.com/contact/) to enable
  this feature in your Materialize region.

---

## Materialize v0.53

## v0.53.0

#### SQL

* Add support for table aliases in [joins](https://materialize.com/docs/transform-data/join/)
  that specify the `USING` clause. As an example, the column `c` used as the
  join condition in the statement below will be referenceable as `lhs.c`,
  `rhs.c`, and `joint.c`.

  ```mzsql
  SELECT *
  FROM lhs
  JOIN rhs USING (c) AS joint;
  ```

* Require the `CREATECLUSTER` attribute when creating sources or sinks using the
  `SIZE` parameter, which results in the creation of a linked cluster (see
  [Materialize v0.39](../v0.39)). This is part of the work to enable **Role-based
  access control** (RBAC) ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

#### Bug fixes and other improvements

* Fix a bug that prevented the PostgreSQL source from replicating tables with
  identifiers that contained quotes (e.g. `"""table"""`) or needed to be
  quoted (e.g. `"select"`).

* This release restores compatibility with `dbt-materialize` <= v1.4.0, which
  broke in the previous release due to the changes in introspection routing
  (see [Materialize v0.52](../v0.52)).

---

## Materialize v0.52

## v0.52.0

#### Sources and sinks

* Allow reading from all non-errored subsources in the [PostgreSQL source](/sql/create-source/postgres/),
  when a source error occurs. Prior to this release, if Materialize encountered
  an error during replication for _any_ table, it'd block reads from _all_
  replicated tables associated with the source.

#### SQL

[//]: # "NOTE(morsapaes) This feature was released in v0.49, but is only
considered production-ready after the changes shipping in v0.52 -— so
mentioning it here."

* Automatically run introspection queries in the [`mz_introspection` cluster](/sql/show-clusters/#mz_catalog_server-system-cluster),
  which has several indexes installed to speed up queries using system catalog
  objects (like `SHOW` commands). This behavior can be disabled via the new
  `auto_route_introspection_queries` [configuration parameter](/sql/set/#other-configuration-parameters).

* Add `reason` to the `mz_internal.mz_cluster_replica_statuses` system catalog
  table. If a cluster replica is in a `not-ready` state, this column provides
  details on the cause (if available). With this release, the only possible non-null
  value for `reason` is `oom-killed`, which indicates that a cluster replica was killed because it ran
  out of memory (OOM).

* Add `credits_per_hour` to the `mz_internal.mz_cluster_replica_sizes` system
  catalog table, and rate limit [free trial accounts](/free-trial-faqs/) to 4
  credits per hour.

  To see your current credit consumption rate, measured in credits per hour, run
  the following query:

  ```mzsql
  SELECT sum(s.credits_per_hour) AS credit_consumption_rate
    FROM mz_cluster_replicas r
    JOIN mz_internal.mz_cluster_replica_sizes s ON r.size = s.size;
  ```

* Add default privileges to databases objects. Each object-specific system table
  now has a `privileges` column that specifies the privileges belonging to the
  object. This is part of the work to enable **Role-based access control**
  (RBAC) ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

  It's important to note that privileges cannot currently be modified, and are
  not considered when executing statements. This functionality will be added in
  a future release.

* Add the [`GRANT PRIVILEGE`](/sql/grant-privilege) and [`REVOKE PRIVILEGE`](/sql/revoke-privilege)
  commands, which allow granting/revoking privileges on a database object. To
  ensure compatibility with PostgreSQL, sources, views and materialized views
  must specify `TABLE` as the object type, or omit it altogether.

  This is part of the work to enable **Role-based access control** (RBAC) in a
  future release ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

#### Bug fixes and other improvements

* **Breaking change.** Change the type of `id` in the `mz_schemas` and
    `mz_databases` system catalog tables from integer to string, for
    consistency with the rest of the catalog. This change should have no user
    impact, but please [let us know](https://materialize.com/s/chat) if you
    run into any issues.

* Fix a bug where the `before` field was still required in the schema of change
  events for Kafka sources using [`ENVELOPE DEBEZIUM`](https://materialize.com/docs/sql/create-source/kafka/#debezium-envelope)
  ([#18844](https://github.com/MaterializeInc/materialize/issues/18844)).

#### Known issues

* This release inadvertently broke compatibility with `dbt-materialize` <= v1.4.0. Please
  upgrade to `dbt-materialize` v1.4.1, which contains a workaround.

  The upcoming v0.53 release of Materialize will restore compatibility with
  `dbt-materialize` <= v1.4.0.

---

## Materialize v0.51

## v0.51.0

#### Sources and sinks

* Add support for replicating tables from specific schemas in the
  [PostgreSQL source](/sql/create-source/postgres/), using the new `FOR SCHEMAS(...)`
  option:

  ```mzsql
  CREATE SOURCE mz_source
    FROM POSTGRES CONNECTION pg_connection (PUBLICATION 'mz_source')
    FOR SCHEMAS (public, finance)
    WITH (SIZE = '3xsmall');
  ```

  With this option, only tables that are part of the publication _and_
  namespaced with the specified schema(s) will be replicated.

#### SQL

* Add `disk_bytes` to the `mz_internal.mz_cluster_replica_{metrics, sizes}`
  system catalog tables. This column is currently `NULL`.

* Add the `translate` [string function](/sql/functions/#string-functions), which
  replaces a set of characters in a string with another set of characters
  (one by one, regardless of the order of those characters):

  ```mzsql
  SELECT translate('12345', '134', 'ax');

	 translate
	-----------
	 a2x5
  ```

* Add new configuration parameters:

  | Configuration parameter      | Scope    | Description                                                                             |
  | ---------------------------- | -------- | --------------------------------------------------------------------------------------- |
  | `enable_session_rbac_checks` | Session  | **Read-only.** Boolean flag indicating whether RBAC is enabled for the current session. |
  | `enable_rbac_checks`         | System   | Boolean flag indicating whether to apply RBAC checks before executing statements. Setting this parameter requires _superuser_ privileges. |

  This is part of the work to enable **Role-based access control** (RBAC) in a
  future release ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

#### Bug fixes and other improvements

* Improve the reliability of SSH tunnel connections in the presence of short
  idle TCP connection timeouts.

---

## Materialize v0.50

## v0.50.0

#### SQL

* Add [`mz_internal.mz_dataflow_arrangement_sizes`](/reference/system-catalog/mz_introspection/#mz_dataflow_arrangement_sizes)
  to the system catalog. This view describes how many records and batches are
  contained in operators under each dataflow, which is useful to approximate how
  much memory a dataflow is using.

#### Bug fixes and other improvements

* Improve the usability of subscriptions when using the [`WITH (PROGRESS)`](/sql/subscribe/#progress)
  option. Progress information is now guaranteed to include a progress message
  as the **first** update, indicating the `AS OF` time of the subscription.
  This helps distinguish between an empty snapshot and an "in-flight" snapshot.

* Improve the reliability of SSH tunnel connections when used with large cluster
  sizes, and add more verbose logging to make it easier to debug SSH connection
  errors during source and sink creation.

* Mitigate connection interruptions and ingestion hiccups for all connection
  types. If you observe ingestion lag in your sources or sinks, please [get in touch](https://materialize.com/s/chat)!

---

## Materialize v0.49

## v0.49.0

#### SQL

* Change the type of the following system catalog replica ID columns from integer to string:

    * [`mz_catalog.mz_cluster_replicas.id`](/reference/system-catalog/mz_catalog/#mz_cluster_replicas)
    * [`mz_internal.mz_cluster_replica_statuses.replica_id`](/reference/system-catalog/mz_internal/#mz_cluster_replica_statuses)
    * `mz_internal.mz_cluster_replica_heartbeats.replica_id`
    * [`mz_internal.mz_cluster_replica_metrics.replica_id`](/reference/system-catalog/mz_internal/#mz_cluster_replica_metrics)
    * `mz_internal.mz_cluster_replica_frontiers.replica_id`

    This is part of the work to introduce system replicas, which Materialize
    will use for verification and testing purposes and which will not affect
    user billing or system limits ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)). Note that, since
    `mz_catalog` is part of Materialize’s stable interface, the change to
    `mz_catalog.mz_cluster_replicas.id` is a **breaking change**.
    If this change causes you friction, please [let us know](https://materialize.com/s/chat).

* Add the [`ALTER OWNER`](/sql/alter-owner/) command, which updates the owner
  of an object. This is part of the work to enable **Role-based access
  control** (RBAC)([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

* Add permission checks based on object ownership. To `DROP` or `ALTER` an
  object, the executing role must now be an owner of that object or a
  superuser. This is part of the work to enable **Role-based access control**
  (RBAC)([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

* Apply `PRIMARY KEY`, `UNIQUE`, and `NOT NULL` constraints to tables ingested
  from PostgreSQL sources.

* Rename [replica introspection views](https://materialize.com/docs/reference/system-catalog/mz_introspection)
  for consistency, and use the `_per_worker` name suffix for per-worker introspection views.

* Automatically restart failed SSH tunnels to improve the reliability of
  SSH-tunneled Kafka sources.

#### Bug fixes and other improvements

- Fix a correctness bug in Top K processing for monotonic, append-only sources.

- Fix a bug that prevented superusers from altering an object owner if they weren't a member of the new owner's role.

- Fix a bug that would cause PostgreSQL sources to error when columns are added to upstream tables. Note that dropping columns from upstream tables that Materialize ingests still results in error.

---

## Materialize v0.48

## v0.48.0

#### SQL

* Introduce **object owners**, who can manage privileges for other roles on
  each object in the system by adding or revoking grants. In this release,
  object owners have limited functionality and are assigned as follows:

  * All objects that exist at the time of a new Materialize deployment
    (including all system objects) are owned by the `mz_system` role.
  * All objects that predate the release are owned by the new `default_owner`
    role.
  * Any new object is owned by the user who created it.

  This is part of the work to enable **Role-based access control** (RBAC) in a
  future release ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

* Support specifying multiple roles in the [`GRANT ROLE`](/sql/grant-role) and
  [`REVOKE ROLE`](/sql/revoke-role) commands.

  ```mzsql
  -- Grant role
  GRANT data_scientist TO joe, mike;

  -- Revoke role
  REVOKE data_scientist FROM joe, mike;
  ```

  This is part of the work to enable **Role-based access control** (RBAC) in a
  future release ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

* Add [`mz_internal.mz_sessions`](/reference/system-catalog/mz_internal/#mz_sessions)
  to the system catalog. This table describes all active sessions in the
  system.

#### Bug fixes and other improvements

* Fix a bug where subsources were created in the `public` schema instead of
  being correctly created in the same schema as the source ([#17868](https://github.com/MaterializeInc/materialize/issues/17868)).
  This resulted in confusing name resolution for users of the PostgreSQL and
  load generator sources.

[//]: # "NOTE(morsapaes) The `details` column was introduced in v0.47, but we
missed the release note then and it now fits a little cosier with the change
shipping in v0.48 -— so mentioning it here."

* Improve the error messages reported in `mz_internal.mz_{source|sink}_status_history`
  and `mz_internal.mz_{source|sink}_statuses` with more helpful pointers to
  troubleshoot Kafka sources and sinks ([#17805](https://github.com/MaterializeInc/materialize/issues/17805)). From this release, the
  `error` column reports the full error message, and other helpful suggestions
  are added under `details`.

* Stop silently ignoring `NULL` keys in sources using `ENVELOPE UPSERT` ([#6350](https://github.com/MaterializeInc/materialize/issues/6350)). The new behavior is to throw an error when trying to query the
  source. To recover an errored source, you must produce a record with a `NULL`
  value and a `NULL` key to the topic, to force a retraction. As an example,
  you can use [`kcat`](https://docs.confluent.io/platform/current/clients/kafkacat-usage.html) to
  produce an empty message:

  ```bash
  echo ":" | kcat -b $BROKER -t $TOPIC -Z -K: \
    -X security.protocol=SASL_SSL \
    -X sasl.mechanisms=SCRAM-SHA-256 \
    -X sasl.username=$KAFKA_USERNAME \
    -X sasl.password=$KAFKA_PASSWORD
  ```

* Fix a bug that prevented the correct parsing of connection settings specified
  using the [`-c` option](https://www.postgresql.org/docs/current/app-psql.html)
  ([#18239](https://github.com/MaterializeInc/materialize/issues/18239)).

* Respect session settings even in the case where the first statement executed
  errors ([#18317](https://github.com/MaterializeInc/materialize/issues/18317)). Previously, such errors led to these settings being
  ignored.

---

## Materialize v0.47

## v0.47.0

#### SQL

* Add the [`GRANT ROLE`](/sql/grant-role) and [`REVOKE ROLE`](/sql/revoke-role)
  commands, which allow granting/revoking membership of one role to/from another
  role. This is part of the work to enable **Role-based access control** (RBAC)
  in a future release ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

* Allow rejecting user queries based on role attributes. This privilege is
  exclusive to _superusers_. This is part of the work to enable **Role-based
  access control** (RBAC) in a future release ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

* Add [`mz_internal.mz_dataflow_operator_parents`](/reference/system-catalog/mz_introspection/#mz_dataflow_operator_parents)
  to the system catalog. This view describes how operators are nested into
  scopes, by relating operators to their parent operators, which is useful for
  internal system observability.

* Add `dataflow_id` to the [`mz_compute_exports`](/reference/system-catalog/mz_introspection/#mz_compute_exports)
  introspection source. This introspection source describes the dataflows
  created by indexes, materialized views, and subscriptions in the system.

---

## Materialize v0.46

## v0.46.0

#### SQL

* Add [`mz_internal.mz_subscriptions`](/reference/system-catalog/mz_internal/#mz_subscriptions)
  to the system catalog. This table describes all active `SUBSCRIBE` operations
  in the system.

* Add support for new SQL functions:

  | Function                                        | Description                                                             |
  | ----------------------------------------------- | ----------------------------------------------------------------------- |
  | [`uuid_generate_v5`](/sql/functions/#uuid-functions) | Generates a UUID in the given namespace using the specified input name. |

* Add the `is_superuser` configuration parameter, which reports whether the
  current session is a _superuser_ with admin privileges. This is part of the
  work to enable **Role-based access control** (RBAC) in a future release ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

* Add the [`ALTER ROLE`](/sql/alter-role) command, as well as role attributes to
  the [`CREATE ROLE`](/sql/create-role/) command. This is part of the work to
  enable **Role-based access control** (RBAC)([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

  It's important to note that no role attributes or privileges will be
  considered when executing `CREATE ROLE` statements. These attributes will be
  saved and considered in a future release.

#### Bug fixes and other improvements

* Fix a bug that would cause the `mz_sources` and `mz_sinks` system tables to
  report the wrong size for a source after an `ALTER {SOURCE|SINK} ... SET
  (SIZE = ...)` command.

## Patch releases

### v0.46.1

* Stabilizate resource utilization in the [`mz_introspection`](/sql/show-clusters/#mz_catalog_server-system-cluster)
  system cluster.

---

## Materialize v0.45

## v0.45.0

#### Sources and sinks

* Expose source progress metadata as a subsource that can be used to
  monitor **ingestion progress**. The name of the progress subsource can be
  specified using the `EXPOSE PROGRESS AS` clause in `CREATE SOURCE`;
  otherwise, it will be named `<src_name>_progress` by default.

  **Example**

  ```mzsql
  -- Given a "purchases" Kafka source, a "purchases_progress"
  -- subsource is automatically created
  SELECT partition, "offset"
  FROM (
	    SELECT upper(partition)::uint8 AS partition, "offset"
	    FROM purchases_progress
  )
  WHERE partition IS NOT NULL;

   partition |  offset
  -----------+----------
   0         | 13645902
   1         | 13659722
   2         | 13656787
  ```

  For Kafka sources, the progress subsource returns the next possible offset to
  consume from the identified partitions, and for PostgreSQL sources it returns
  the last Log Sequence Number (LSN) consumed from the upstream replication
  stream.

#### SQL

* Improve the behavior of the `search_path` configuration parameter to match that of
  [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html#DDL-SCHEMAS-PATH).
  You can now specify multiple schemas and Materialize will correctly resolve
  unqualified names by following the search path, as well as create objects in
  the first schema named (i.e. the _current schema_).

* Support `options` settings on connection startup. As an example, you can
now specify the cluster to connect to in the `psql` connection string:

  ```mzsql
  psql "postgres://user%40domain.com@host:6875/materialize?options=--cluster%3Dfoo"
  ```

* Add support for the `\du` meta-command, which lists all roles/users of the database.

* Add support for new SQL functions:

  | Function                                        | Description                                                             |
  | ----------------------------------------------- | ----------------------------------------------------------------------- |
  | [`ceiling`](/sql/functions/#numbers-functions)       | Works as an alias of the `ceil` function.                               |

<br>

* Remove the `CREATE USER` command, as well as the `LOGIN` and `SUPERUSER`
  attributes from the [`CREATE ROLE`](/sql/create-role/) command. This is part
  of the work to enable **Role-based access control** (RBAC) in a future release
  ([#11579](https://github.com/MaterializeInc/materialize/issues/11579)).

#### Bug fixes and other improvements

* Improve the error message for naming collisions, specifying the catalog item
  type.

  **Example**

  ```mzsql
  CREATE VIEW foo AS SELECT 'bar';

  ERROR:  view "materialize.public.foo" already exists
  ```

* Fix a bug that would sporadically prevent clusters from coming online ([#17774](https://github.com/MaterializeInc/materialize/issues/17774)).

* Improve `SUBSCRIBE` error handling. Prior to this release, subscriptions
  ignored errors in their input, which could lead to correctness issues.

* Return an error rather than crashing if source data contains invalid
  retractions, which might happen in the presence of e.g. incomplete or invalid
  data ([#17709](https://github.com/MaterializeInc/materialize/issues/17709)).

* Fix a bug that could cause Materialize to crash when expressions in `CREATE
  TABLE ... DEFAULT` clauses or `INSERT ... RETURNING` clauses contained nested
  parentheses ([#17723](https://github.com/MaterializeInc/materialize/issues/17723)).

* Avoid panicking when attempting to parse a range from strings containing
  multibyte characters ([#17803](https://github.com/MaterializeInc/materialize/issues/17803)).

---

## Materialize v0.44

## v0.44.0

* Remove the `cpu_percent_normalized` column from the
  `mz_internal.mz_cluster_replica_utilization` system catalog view. CPU
  utilization metrics will be restored in a future release.

* Add the `timing` option to `EXPLAIN`. Using this option annotates the output
  with the time spent in optimization (including decorrelation), which is
  useful to detect performance regressions in internal benchmarking.

* Add a `MAX CARDINALITY` parameter to the `COUNTER` load generator source. If
  specified, the counter load generator will begin retracting the oldest
  emitted value for each new value it emits, once it has crossed the max
  cardinality threshold. This is useful for internal load testing.

---

## Materialize v0.43

## v0.43.0

* Limit the size of SQL statements to **1MB**. Statements that exceed this limit
  will be rejected.

* Add the `bool_and` and `bool_or` [aggregate functions](/sql/functions/#aggregate-functions),
  which compute whether a column contains all true values or at least one
  true value, respectively.

* Improve the output of `EXPLAIN [MATERIALIZED] VIEW $view_name` and `EXPLAIN
  PHYSICAL PLAN FOR [MATERIALIZED] VIEW $view_name` to print the name of the
  view. The output will now look similar to:

  ```mzsql
  EXPLAIN VIEW v;

      Optimized Plan
  ----------------------------------
   materialize.public.v:           +
     Filter (#0 = 1) AND (#3 = 3)  +
       Get materialize.public.data +
  ```

* Disallow `NATURAL JOIN` and `*` expressions in views that directly reference
  system objects. Instead, project the required columns and convert all
  `NATURAL JOIN`s to `USING` joins.

* Fix a bug where active [subscriptions](/sql/subscribe/) were not terminated when
  their underlying relations were dropped ([#17476](https://github.com/MaterializeInc/materialize/issues/17476)).

---

## Materialize v0.42

## v0.42.0

This release focuses on stabilization work and performance improvements. It does
not introduce any new user-facing features or bug fixes. 👷

---

## Materialize v0.41

## v0.41.0

* Add [`mz_internal.mz_sink_statistics`](/reference/system-catalog/mz_internal/#mz_sink_statistics)
  to the system catalog. This table contains statistics for each
  process of each sink in the system, like the number of messages
  and bytes committed to the external system.

* Add [`mz_internal.mz_postgres_sources`](/reference/system-catalog/mz_internal/#mz_postgres_sources)
  to the system catalog. This table exposes the randomly-generated
  name of the replication slot created in the upstream PostgreSQL
  database that Materialize will create for each source.

    ```mzsql
    SELECT * FROM mz_internal.mz_postgres_sources;

       id   |             replication_slot
    --------+----------------------------------------------
     u8     | materialize_7f8a72d0bf2a4b6e9ebc4e61ba769b71
    ```

* Allow placing sources and sinks in existing clusters using the `IN CLUSTER`
  clause in [`CREATE SOURCE`](/sql/create-source) and [`CREATE SINK`](/sql/create-sink)
  statements, as an alternative to provisioning dedicated
  resources via the `SIZE` parameter.

  **New syntax**

  ```mzsql
  CREATE SOURCE kafka_connection
    IN CLUSTER quickstart
    FROM KAFKA CONNECTION qck_kafka_connection (TOPIC 'test_topic')
    FORMAT AVRO USING CONFLUENT SCHEMA REGISTRY CONNECTION csr_connection
    ENVELOPE DEBEZIUM;
  ```

  It's important to note that clusters containing sources and sinks can have at
  most one replica, and may contain any number of indexes and materialized
  views *or* any number of sources and sinks, but not both types of objects.
  These restrictions will be removed in a future release.

* Support using [`SUBSCRIBE`](/sql/subscribe) with queries over introspection
  sources for [troubleshooting](/ops/troubleshooting/).

---

## Materialize v0.40

## v0.40.0

* Allow configuring an `AVAILABILITY ZONE` option for each broker when creating
  a Kafka connection using [AWS PrivateLink](/sql/create-connection/#kafka-network-security):

  ```mzsql
  CREATE CONNECTION privatelink_svc TO AWS PRIVATELINK (
      SERVICE NAME 'com.amazonaws.vpce.us-east-1.vpce-svc-0e123abc123198abc',
      AVAILABILITY ZONES ('use1-az1', 'use1-az4')
  );

  CREATE CONNECTION kafka_connection TO KAFKA (
      BROKERS (
          'broker1:9092' USING AWS PRIVATELINK privatelink_svc (AVAILABILITY ZONE 'use1-az1'),
          'broker2:9092' USING AWS PRIVATELINK privatelink_svc (
            AVAILABILITY ZONE 'use1-az4',
            PORT 9093
          )
      )
  );
  ```

  Specifying the correct availability zone for each broker allows Materialize to
  be more efficient with its network connections. Without the `AVAILABILITY
  ZONE` option, when Materialize initiates a connection to a Kafka broker, it
  must attempt to connect to each availability zone in sequence to determine
  which availability zone the broker is running in. With the `AVAILABILITY
  ZONE` option, Materialize can connect immediately to the correct availability
  zone.

---

## Materialize v0.39

## v0.39.0

* Add `mz_internal.mz_source_statistics` to the system catalog. This table
  contains statistics for each process of each source in the system, like the
  number of messages and bytes received from the upstream external system.

* Add `mz_internal.mz_object_dependencies` to the system catalog. This table
  describes the dependency structure between all objects in Materialize. As an
  example, you can now get an overview of the relationship between user-defined
  objects using:

  ```mzsql
  SELECT
    object_id,
	o.name,
	o.type,
	referenced_object_id,
	ro.name,
	ro.type
  FROM mz_internal.mz_object_dependencies
  JOIN mz_objects o ON object_id = o.id
  JOIN mz_objects ro ON referenced_object_id = ro.id
  WHERE o.id LIKE 'u%' AND ro.id NOT LIKE 's%'
  ORDER BY o.name DESC, ro.name ASC;
  ```

  It's important to note that these tables are part of an unstable interface of
  Materialize (`mz_internal`), which means that their values may change at any
  time, and you should not rely on them for tasks like capacity planning for
  the time being.

* Add an `mz_version` system configuration parameter, which reports the
  Materialize version information. The value of this parameter is the same as
  the value returned by the existing `mz_version()` function, but the parameter
  form can be more convenient for downstream applications.

  ```mzsql
  SHOW mz_version;
  ```

  ```nofmt
         mz_version
   ---------------------
   v0.39.2 (e6af8921b)
  ```

* Automatically create a linked cluster associated with each source and sink.
  The mappings between sources/sinks and their respective linked cluster are
  exposed in the `mz_internal.mz_cluster_links` system catalog table.

  The concept of a linked cluster is not user-facing, and is intentionally
  undocumented. Linked clusters are meant to preserve the soon-to-be legacy
  interface for sizing sources and sinks, where a `SIZE` parameter is specified
  on the source/sink rather than the cluster replica.

* Add the `IDLE ARRANGEMENT MERGE EFFORT` advanced option to `CREATE CLUSTER
  REPLICA`, which enables configuring the amount of effort a replica exerts on
  compacting arrangements during idle periods.

* **Private preview.** Support [bearer token authentication](/integrations/websocket-api/#endpoint)
  in the WebSocket API endpoint, which supports interactive SQL queries over WebSockets.

---

## Materialize v0.38

## v0.38.0

* Add `cpu_percent_normalized` to the `mz_internal.mz_{source,sink,cluster_replica}_utilization`
  system catalog views. This column provides an approximation of CPU utilization
  as a % of the total of compute workers.

* Add `mz_internal.mz_cluster_replica_frontiers`
  to the system catalog. This table describes the frontiers of each
  dataflow in the system.

* **Private preview.** Support the [`AS OF`](/sql/subscribe/#as-of) and [`UP TO`](/sql/subscribe/#up-to)
  clauses in `SUBSCRIBE`. These clauses allow specifying a timestamp at
  which `SUBSCRIBE` should begin returning results (`AS OF`), or cease
  running (`UP TO`).

  As is, all user-defined sources and tables have a retention window of one
  second, so `AS OF` is of limited use beyond subscribing to queries over
  specific system catalog objects (including `mz_cluster_replicas`,
  `mz_sources`, `mz_sinks`, `mz_internal.mz_cluster_replica_metrics`, and
  `mz_internal.mz_cluster_replica_sizes`).

---

## Materialize v0.37

## v0.37.0

* Add support for connecting to Confluent Schema Registry using an
  [SSH tunnel](/sql/create-connection/#ssh-tunnel) connection to an SSH bastion
  server.

* Add [`mz_internal.mz_cluster_replica_utilization`](/reference/system-catalog/mz_internal/#mz_cluster_replica_utilization)
  to the system catalog. This view allows you to monitor the resource utilization for
  all extant cluster replicas as a % of the total resource allocation:

  ```mzsql
  SELECT * FROM mz_internal.mz_cluster_replica_utilization;
  ```

  ```nofmt
    replica_id | process_id |     cpu_percent      |    memory_percent
   ------------+------------+----------------------+----------------------
    1          | 0          |            9.6629961 |   0.6772994995117188
    2          | 0          |  0.10735560000000001 |   0.3876686096191406
    3          | 0          |           46.8730398 |      0.7110595703125
  ```

  It's important to note that these tables are part of an unstable interface of
  Materialize (`mz_internal`), which means that their values may change at any
  time, and you should not rely on them for tasks like capacity planning for the
  time being.

* Add `mz_internal.mz_storage_host_metrics` and
  `mz_internal.mz_storage_host_sizes` to the system catalog. These objects
  respectively expose the last known CPU and RAM utilization statistics for all
  processes of all extant storage hosts, and a mapping of logical sizes
  (e.g. `xlarge`) to the number of processes, as well as CPU and memory
  allocations for each process.

  The concept of a storage host is not user-facing, and is intentionally
  undocumented. It refers to the physical resource allocation on which
  Materialize can schedule multiple sources and sinks behind the scenes.

* Rename system catalog objects to adhere to the naming conventions defined in
  the Materialize [SQL style guide](https://github.com/chaas/materialize/blob/main/doc/developer/style.md).
  The affected objects are:

  | Schema        | Old name           | New name           |
  | ------------- | ------------------ | --------------------- |
  | `mz_internal` | `mz_source_status` | `mz_source_statuses` |
  | `mz_internal` | `mz_sink_status`   | `mz_sink_statuses`   |

* Support `JSON` as an output format of [`EXPLAIN TIMESTAMP`](https://materialize.com/docs/sql/explain-timestamp/).

* Fix a bug where the `to_timestamp` function would truncate the fractional part
  of negative timestamps (i.e. prior to the Unix epoch: January 1st, 1970 at
  00:00:00 UTC) ([#16610](https://github.com/MaterializeInc/materialize/issues/16610)), and return an error instead of `NULL` when the
  timestamp is out of range. The new behavior matches PostgreSQL.

* **Private preview.** Add a [WebSocket API endpoint](/integrations/websocket-api/)
	which supports interactive SQL queries over WebSockets.

* Change the JSON serialization for rows emitted by the [HTTP API endpoint](/integrations/http-api/)
  to exactly match the JSON serialization used by `FORMAT JSON` Kafka sinks.
  Previously, the HTTP SQL endpoint serialized datums using slightly different
  rules.

---

## Materialize v0.36

## v0.36.0

* Add `mz_internal.mz_sink_status` and `mz_internal.mz_sink_status_history`
  to the system catalog. These objects respectively expose the current and
  historical state for each sink in the system, including potential error
  messages and additional metadata helpful for debugging.

* Add `mz_internal.mz_cluster_replica_sizes`
  to the system catalog. This table provides a mapping of logical sizes
  (e.g. `xlarge`) to the number of processes, as well as CPU and memory
  allocations for each process. To monitor the resource utilization for
  all extant cluster replicas as a % of the total allocation, you can now
  use:

  ```mzsql
  SELECT
    r.id AS replica_id,
    m.process_id,
    m.cpu_nano_cores / s.cpu_nano_cores * 100 AS cpu_percent,
    m.memory_bytes / s.memory_bytes * 100 AS memory_percent
  FROM mz_cluster_replicas AS r
  JOIN mz_internal.mz_cluster_replica_sizes AS s ON r.size = s.size
  JOIN mz_internal.mz_cluster_replica_metrics AS m ON m.replica_id = r.id;
  ```

  It's important to note that these tables are part of an unstable interface of
  Materialize (`mz_internal`), which means that their values may change at any
  time, and you should not rely on them for tasks like capacity planning for the
  time being.

* Add `mz_catalog.mz_aws_privatelink_connections` to the system catalog. This
  table contains a row for each [AWS PrivateLink connection](/sql/create-connection/#aws-privatelink)
  in the system, and allows you to retrieve the AWS principal that
  Materialize will use to connect to the VPC endpoint.

* Return an error rather than crashing if the value of the `AVRO KEY FULLNAME`
  or `AVRO VALUE FULLNAME` option in an Avro-formatted Kafka sink is not a
  valid Avro name ([#16433](https://github.com/MaterializeInc/materialize/issues/16433)).

* Return the current timestamp of the `EpochMillis` timeline when the `mz_now
  ()` function is used outside the context of a specific timeline, such as
  `SELECT mz_now();`. The old behavior was to return [`u64::MAX`](https://doc.rust-lang.org/std/primitive.u64.html#associatedconstant.MAX).

## Patch releases

### v0.36.2

* Fix incorrect decoding of negative timestamps (i.e. prior to the Unix epoch:
  January 1st, 1970 at 00:00:00 UTC) in Avro records ([#16609](https://github.com/MaterializeInc/materialize/issues/16609)).

---

## Materialize v0.33

## v0.33.0

* Add support for connecting to Kafka brokers using an [SSH tunnel connection](/sql/create-connection/#ssh-tunnel)
to an SSH bastion server.

  ```mzsql
  CREATE CONNECTION kafka_connection TO KAFKA (
    BROKERS (
      'broker1:9092' USING SSH TUNNEL ssh_connection,
      'broker2:9092' USING SSH TUNNEL ssh_connection
      )
  );
  ```

* Add [`mz_internal.mz_source_status`](/reference/system-catalog/mz_internal/#mz_source_statuses) and
  [`mz_internal.mz_source_status_history`](/reference/system-catalog/mz_internal/#mz_source_status_history)
  to the system catalog. These objects respectively expose the current
  and historical state for each source in the system, including potential
  error messages and additional metadata helpful for debugging.

* Add [`mz_internal.mz_cluster_replica_metrics`](https://materialize.com/docs/reference/system-catalog/mz_internal/#mz_cluster_replica_metrics) to the system
  catalog. This table records the last known CPU and RAM utilization statistics
  for all processes of all extant cluster replicas.

---

## Materialize v0.32

## v0.32.0

* Add support for replicating tables that contain unsupported types in the
  [PostgreSQL source](/sql/create-source/postgres/), using the new `TEXT
  COLUMNS` option:

  ```mzsql
  CREATE SOURCE mz_source
	FROM POSTGRES CONNECTION pg_connection (
	  PUBLICATION 'mz_source',
	  TEXT COLUMNS (tbl.col_of_unsupported_type)
	) FOR ALL TABLES
  WITH (SIZE = '3xsmall');
  ```

  Any columns specified via this option will be treated as `text` in
  Materialize regardless of the original PostgreSQL type. Examples of
  unsupported types that can now be ingested are `enum`,
  arbitrary precision `numeric`, `money`, and `citext`.

* Improve error message for unexpected or mismatched type catalog errors,
  specifying the catalog item type:

  ```mzsql
  DROP VIEW mz_table;

  ERROR:  "materialize.public.mz_table" is a table not a view
  ```

* Fix a bug in the [`#>>` `jsonb` operator](/sql/types/jsonb/#operators) that
  caused an error when specifying an array index that does not exist, instead
  of returning `NULL` ([#15978](https://github.com/MaterializeInc/materialize/issues/15978)).

* Fix a bug where relations in `pg_catalog` and `information_schema` would
  contain information about all databases, rather than just the current
  database ([#15841](https://github.com/MaterializeInc/materialize/issues/15841)).

* **Private preview.** Add support for
  [AWS PrivateLink connections](/sql/create-connection/#aws-privatelink),
  which establish links to
  [AWS PrivateLink](https://aws.amazon.com/privatelink/) services.

## Patch releases

### v0.32.4

* Stabilize the performance of ad hoc `SELECT` statements against unindexed
  objects in large clusters ([#16090](https://github.com/MaterializeInc/materialize/issues/16090)).

* Fix a bug that caused query performance on unindexed objects to slowly degrade
  over time ([#16127](https://github.com/MaterializeInc/materialize/issues/16127)).

* Fix a bug in predicate pushdown that could result in incorrect query plans ([#16147](https://github.com/MaterializeInc/materialize/issues/16147)).

---

## Materialize v0.31

## v0.31.0

* **Breaking change.** Fix a bug that caused `NULLIF` to be incorrectly
    converted to `COALESCE` ([#15943](https://github.com/MaterializeInc/materialize/issues/15943)). Existing views and materialized
    views using `NULLIF` must be manually dropped and recreated.

* Include the replica status in the output of [`SHOW CLUSTER REPLICAS`](/sql/show-cluster-replicas/)
  as a new column named `ready`, which indicates if a cluster replica is
  online (`t`) or not (`f`).

* Improve the output of [`EXPLAIN PLAN`](/sql/explain-plan/) to make the printing of index
  lookups consistent regardless of whether the explained query uses the fast
  path or not. For both cases, the output will look similar to:

  ```nofmt
  ReadExistingIndex materialize.public.t1 lookup values [("l2"); ("l3")]
  ```

* Fix a bug where subsources were counted towards resource limits for existing
  sources ([#15958](https://github.com/MaterializeInc/materialize/issues/15958)). This resulted in an error for users of the PostgreSQL
  source if the number of replicated tables exceeded the default value for
  `max_sources` (25).

---

## Materialize v0.30

## v0.30.0

* Fix a bug that could cause updates in [sinks](/sql/create-sink) to appear as
  two separate records, instead of consolidated into a single update record ([#15748](https://github.com/MaterializeInc/materialize/issues/15748)). Previously, updates for multiple keys that occurred at the same
  timestamp would either emit a deletion tombstone followed by a record with the
  new value (`ENVELOPE UPSERT`), or a `{"before": "OLDVALUE", "after": null}`
  record followed by a `{"before": null, "after": "NEWVALUE"}` record (`ENVELOPE
  DEBEZIUM`).

* Improve error message for unsupported types in the
  [PostgreSQL source](/sql/create-source/postgres/), specifying the table and
  column containing an unsupported type:

  ```mzsql
  CREATE SOURCE pg_source
	FROM POSTGRES CONNECTION pg_connection (PUBLICATION 'mz_source')
	FOR ALL TABLES
	WITH (SIZE = '3xsmall');

	ERROR:  column "person.current_mood" uses unrecognized type
	DETAIL:  type with OID 211538 is unknown
	HINT:  You may be using an unsupported type in Materialize, such as an enum. Try excluding the table from the publication.
  ```

  Fine-grained control for casting unsupported types into valid
  [Materialize types](/sql/types/) is a work in progress ([#15716](https://github.com/MaterializeInc/materialize/issues/15716)).

* When using both signed and unsigned integers as inputs to a function, cast the
  inputs to a larger lossless type rather than [`double`](/sql/types/float). For
  example, when determining equality between [`integer`](/sql/types/integer)
  (32-bit signed integer) and [`uint4`](/sql/types/uint) (32-bit unsigned
  integer), both values are now cast to [`bigint`](/sql/types/integer)
  (64-bit signed integer). Previously both values would be cast to
  [`double`](/sql/types/double) (64-bit floating point number).

* Improve the performance of DDL statements, especially when many DDL statements
  are run within the same 24 hour period.

* Add an `xlarge` size for sources and sinks.

---

## Materialize v0.29

## v0.29.0

* Fix a bug where implicit type casts prevented indexes from being used ([#15476](https://github.com/MaterializeInc/materialize/issues/15476)).

* Improve Materialize's ability to use indexes when comparing column expressions
  to literal values, particularly in cases where e.g. `col_a` was of type
  `VARCHAR`:

  ```mzsql
  SELECT * FROM table_foo WHERE col_a = 'hello';
  ```

* Fix a bug that prevented using pre-existing topics with multiple partitions in
  Kafka sinks ([#15609](https://github.com/MaterializeInc/materialize/issues/15609)). Previously, the sink would use the default
  Kafka cluster configuration also for pre-existing
  topics, instead of the user-configured number of partitions.

* Improve ordering for joins that have filters applied to their inputs. This
  leads to an order of magnitude performance improvement in cases with highly
  selective filters ([#15120](https://github.com/MaterializeInc/materialize/issues/15120)).

* Treat some errors as transient instead of fatal in the [PostgreSQL source](/sql/create-source/postgres/).
  Errors that would previously set the source into an error state will now retry
  ([#15200](https://github.com/MaterializeInc/materialize/issues/15200)).

* Allow users to create indexes on system objects to optimize the performance of
  [troubleshooting](/ops/troubleshooting/) queries.

* Include indexes created on system objects when running the [`SHOW INDEXES`](/sql/show-indexes)
  command if the `IN CLUSTER` clause is specified.

* Add a `TPCH` [load generator source](/sql/create-source/load-generator/#tpch),
  which implements the TPC-H benchmark specification.

---

## Materialize v0.28

## v0.28.0

* Use [static IPs](/ops/network-security/static-ips/) when initiating connections from sources
  and sinks. You can use these IPs in your firewall configuration to authorize
  connections from your Materialize region.

* Improve the syntax for [`CREATE CONNECTION`](/sql/create-connection). The
  `FROM` keyword was replaced with `TO`, and the option list must now be
  enclosed in parenthesis.

  **New syntax**

  ```mzsql
  CREATE CONNECTION kafka_connection TO KAFKA (
    BROKER 'unique-jellyfish-0000.us-east-1.aws.confluent.cloud.io:9092',
    SASL MECHANISMS = 'SCRAM-SHA-256',
    SASL USERNAME = 'foo',
    SASL PASSWORD = SECRET kafka_password
  );
  ```

  **Old syntax**

  ```mzsql
  CREATE CONNECTION kafka_connection FOR KAFKA
    BROKER 'unique-jellyfish-0000.us-east-1.aws.confluent.cloud:9092',
    SASL MECHANISMS = 'SCRAM-SHA-256',
    SASL USERNAME = 'foo',
    SASL PASSWORD = SECRET kafka_password;
  ```

  The old syntax is still supported for backwards compatibility, but its use is
  discouraged.

* Improve the usability of the `EXPLAIN` command. For an overview of the new
  `EXPLAIN` syntax, check the [updated documentation](/sql/explain-plan/).

* Include all indexes when running the [`SHOW INDEXES`](/sql/show-indexes)
  command, regardless of the number of columns. Previously, `SHOW INDEXES`
  would omit any indexes with 0 columns.

* Include all indexes when a schema is specified using `SHOW INDEXES ON`.
  Previously, the command would not correctly display existing indexes in
  non-active schemas.

* Add a default index for all `SHOW` commands in the
  [`mz_introspection`](/sql/show-clusters/#mz_catalog_server-system-cluster)
  cluster. For the best performance when executing `SHOW` commands, switch to
  the `mz_introspection` cluster using:

  ```mzsql
  SET CLUSTER = mz_introspection;
  ```

* Correctly use the `char` type for `pg_type.typcategory`. Previously,
  `typcategory` used the `text` type, which caused errors in language drivers
  that expect the documented `char` type, like sqlx.

* Add the [`mz_introspection` system
  cluster](/sql/show-clusters/#mz_catalog_server-system-cluster) to support
  efficiently serving common introspection queries.

* Add the [`mz_system` system
  cluster](/sql/show-clusters/#mz_system-system-cluster) to support various
  internal system tasks.

* **Breaking change.** Change the type of a materialized view in the
  `mz_objects` relation from `materialized view` to `materialized-view`, for
  consistency with how multi-word types are represented elsewhere in the
  catalog.

---

## Materialize v0.27

v0.27.0 is the first cloud-native release of Materialize. It contains
substantial breaking changes from [v0.26 LTS].

## v0.27.0

* Add [clusters](/sql/create-cluster) and [cluster replicas](/sql/create-cluster-replica/),
  which together allocate isolated, highly available, and horizontally scalable
  compute resources that incrementally maintain a "cluster" of indexes.

* Add [materialized views](/sql/create-materialized-view), which are views that
  are persisted in durable storage and incrementally updated as new data
  arrives.

  A materialized view is created in a
  [cluster](/concepts/clusters/) that
  is tasked with keeping its results up-to-date, but **can be referenced in any
  cluster**.

  The result of a materialized view is not maintained in memory, unless you
  create an [index](/sql/create-index) on it. However, intermediate state
  necessary for efficient incremental updates of the materialized view may be
  maintained in memory.

* Add [connections](/sql/create-connection/), which describe how to connect to
  and authenticate with external systems. Once created, a connection is reusable
  across multiple [`CREATE SOURCE`](/sql/create-source) and
  [`CREATE SINK`](/sql/create-sink) statements.

* Add [secrets](/sql/create-secret), which securely store sensitive credentials
  (like passwords and SSL keys) for reference in connections.

* Durably record data ingested from [sources](/sql/create-source).

  Once a source has acknowledged data upstream (e.g., via committing a Kafka
  offset or advancing a PostgreSQL replication slot), it will never re-read that
  data. As a result, PostgreSQL sources no longer have a "single
  materialization" limitation. All sources are directly queryable via
  [`SELECT`](/sql/select).

* Allow provisioning the size of a source or sink.

  Each source and sink now runs with an isolated set of compute resources. You
  can adjust the size of the resource allocation with the
  [`SIZE`](/sql/create-source/#sizing-a-source) parameter.

* Add [load generator sources](/sql/create-source/load-generator), which
  produce synthetic data for use in demos and performance tests.

* Add an [HTTP API](/integrations/http-api) which supports executing SQL queries
  over HTTP.

* **Breaking change.** Require all [indexes](/sql/create-index) to be associated
  with a cluster.

* **Breaking change.** Require the use of [connections](/sql/create-connection/)
  with Kafka sources, PostgreSQL sources, and Kafka sinks.

* **Breaking change.** Rename `TAIL` to [`SUBSCRIBE`](/sql/subscribe).

* **Breaking change.** Change the meaning of `CREATE MATERIALIZED VIEW`.

  `CREATE MATERIALIZED VIEW` now creates a new type of object called a
  [materialized view](/sql/create-materialized-view), rather than providing a
  shorthand for creating a view with a default index.

  To emulate the old behavior, explicitly create a default index after creating
  a view:

  ```mzsql
  CREATE VIEW <name> ...;
  CREATE DEFAULT INDEX ON <name>;
  ```

* **Breaking change.** Remove the `MATERIALIZED` option from `CREATE SOURCE`.

  `CREATE MATERIALIZED SOURCE` is no longer shorthand for creating a source with
  a default index. Instead, you must explicitly create a default index after
  creating a source:

  ```mzsql
  CREATE SOURCE <name> ...;
  CREATE DEFAULT INDEX ON <name>;
  ```

* **Breaking change.** Remove support for the following source types:

  * PubNub
  * Kinesis
  * S3

* **Breaking change.** Remove the `reuse_topic` option from
  [Kafka sinks](/sql/create-sink).

  The exactly-once semantics enabled by `reuse_topic` are now on by default.

* **Breaking change.** Remove the `consistency_topic` option from
  [Kafka sinks](/sql/create-sink).

* **Breaking change.** Do not default to the [Debezium
  envelope](/sql/create-sink/kafka/#debezium-envelope) in `CREATE SINK`. You
  must explicitly specify the envelope to use.

* **Breaking change.** Remove the `CREATE VIEWS` statement, which was used to
  separate the data in a PostgreSQL source into a single relation per upstream
  table.

  The PostgreSQL source now automatically creates a relation in Materialize
  for each upstream table.

* **Breaking change.** Overhaul the system catalog.

  The relations in the [`mz_catalog`](/reference/system-catalog/mz_catalog) schema
  have been adjusted substantially to support the above changes. Many column
  and relation names were adjusted for consistency. The resulting relations
  are now part of Materialize's stable interface.

  Relations which were not ready for stabilization were moved to a new
  [`mz_internal`](/reference/system-catalog/mz_internal) schema.

* **Breaking change.** Rename `mz_logical_timestamp()` to [`mz_now`](/sql/functions/now_and_mz_now/).

## Upgrade guide

Following are several examples of how to adapt source and view definitions
from Materialize v0.26 LTS for Materialize v0.27:

### Authenticated Kafka source

Change from:

```mzsql
CREATE SOURCE kafka_sasl
  FROM KAFKA BROKER 'broker.tld:9092' TOPIC 'top-secret' WITH (
      security_protocol = 'SASL_SSL',
      sasl_mechanisms = 'PLAIN',
      sasl_username = '<BROKER_USERNAME>',
      sasl_password = '<BROKER_PASSWORD>'
  )
  FORMAT AVRO USING CONFLUENT SCHEMA REGISTRY 'https://schema-registry.tld' WITH (
      username = '<SCHEMA_REGISTRY_USERNAME>',
      password = '<SCHEMA_REGISTRY_PASSWORD>'
  );
```

to:

```mzsql
CREATE SECRET kafka_password AS '<BROKER_PASSWORD>';
CREATE SECRET csr_password AS '<SCHEMA_REGISTRY_PASSWORD>';

CREATE CONNECTION kafka FOR KAFKA
    BROKER 'broker.tld:9092',
    SASL MECHANISMS 'PLAIN',
    SASL USERNAME 'materialize',
    SASL PASSWORD SECRET kafka_password;

CREATE CONNECTION csr
  FOR CONFLUENT SCHEMA REGISTRY
    USERNAME = '<SCHEMA_REGISTRY_USERNAME>',
    PASSWORD = SECRET csr_password;

CREATE SOURCE kafka_top_secret
  FROM KAFKA CONNECTION kafka TOPIC ('top-secret')
  FORMAT AVRO USING CONFLUENT SCHEMA REGISTRY CONNECTION csr
  WITH (SIZE = '3xsmall');
```

### Materialized view

Change from:

```mzsql
CREATE MATERIALIZED VIEW v AS SELECT ...
```

to:

```mzsql
CREATE VIEW v AS SELECT ...
CREATE DEFAULT INDEX ON v
```

### Materialized source

Change from:

```mzsql
CREATE MATERIALIZED SOURCE src ...
```

to:

```mzsql
CREATE SOURCE src ...
```

If you are performing point lookups on `src` directly, consider building an
index on `src` directly:

```
CREATE INDEX on src (lookup_col1, lookup_col2)
```

### `TAIL`

Change from:

```mzsql
COPY (TAIL t) TO STDOUT
```

to:

```mzsql
COPY (SUBSCRIBE t) TO STDOUT
```

[v0.26 LTS]: https://materialize.com/docs/lts/release-notes/#v0.26.4

---

## Release Schedule

Starting with the v26.1.0 release, Materialize releases on a weekly schedule for
both Cloud and Self-Managed.

## Cloud upgrade schedule

In general, Materialize Cloud uses the following weekly schedule to upgrade all
regions to the latest release, the listed times may vary based on operational needs:

Region        | Day of week | Time
--------------|-------------|-----------------------------
aws/eu-west-1 | Wednesday   | 2100-2300 [Europe/Dublin]
aws/us-east-1 | Thursday    | 0500-0700 [America/New_York]
aws/us-west-2 | Thursday    | 0500-0700 [America/New_York]

During an upgrade, clients may experience brief connection interruptions, but
the service otherwise remains fully available. Upgrade windows were chosen to be
outside of business hours in the most representative time zone for the region.

> **Note:** - Materialize may occasionally deploy unscheduled releases to fix urgent bugs.
> - Actual cutover time may fall outside of the upgrade window.
> - Releases may skip some weeks.
> - Upgrade windows follow any daylight saving time or summer time rules
> for their indicated time zone.

[America/New_York]: https://time.is/New_York
[Europe/Dublin]: https://time.is/Dublin

## Self-Managed release schedule

In general, Materialize releases new Self-Managed versions on Friday.

> **Note:** - Materialize may occasionally have unscheduled releases to fix urgent bugs.
> - Releases may skip some weeks.

