# CREATE SOURCE: SQL Server
Connecting Materialize to a SQL Server database for Change Data Capture (CDC).

> **Disambiguation:** This page reflects the new syntax which allows Materialize to handle upstream DDL changes, specifically adding or dropping columns, without downtime. For the deprecated syntax, see the [old reference page](/sql/create-source/sql-server/).

Creates a new source from SQL Server.  Materialize
supports creating sources from SQL Server version 2016&#43;.  Once a new source is created, you can <a href="/sql/create-table/" ><code>CREATE TABLE FROM SOURCE</code></a>
to create the corresponding tables in Materialize and start the data ingestion
process.

## Prerequisites

To create a source from SQL Server (2016+), you must first:

- Configure your SQL Server.
  - Enable [Change Data
Capture](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/enable-and-disable-change-data-capture-sql-server)
and [`SNAPSHOT` transaction
isolation](https://learn.microsoft.com/en-us/dotnet/framework/data/adonet/sql/snapshot-isolation-in-sql-server)
for the database that you would like to replicate.
- [Create a connection to SQL
  Server](#prerequisite-creating-a-connection-to-sql-server) in Materialize.
  - The connection setup depends on your network security configuration.

## Syntax

```mzsql
CREATE SOURCE [IF NOT EXISTS] <src_name>
[IN CLUSTER <cluster_name>]
FROM SQL SERVER CONNECTION <connection_name>
[WITH ( <with_option> [, ...] )]

```

| Syntax element | Description |
| --- | --- |
| `<src_name>` | The name for the source.  |
| **IF NOT EXISTS** | Optional. If specified, do not throw an error if a source with the same name already exists. Instead, issue a notice and skip the source creation.  |
| **IN CLUSTER** `<cluster_name>` | Optional. The [cluster](/sql/create-cluster) to maintain this source.  |
| **CONNECTION** `<connection_name>` | The name of the SQL Server connection to use in the source. For details on creating connections, check the [`CREATE CONNECTION`](/sql/create-connection/#sql-server) documentation page.  |
| **WITH** (`<with_option>` [, ...]) | Optional. The following `<with_option>`s are supported:  \| Option \| Description \| \|--------\|-------------\| \| `TIMESTAMP INTERVAL [=] <interval>` \| The interval at which timestamps are assigned to data read from this source. Accepts positive [interval](/sql/types/interval/) values (e.g. `'500ms'`, `'1s'`). The value must be between the system parameters `min_timestamp_interval` and `max_timestamp_interval`. Default: the value of the `default_timestamp_interval` system parameter (`1s`). The interval can also be changed after creation with [`ALTER SOURCE`](/sql/alter-source/). \|  |

## Ingesting data

After a source is created, you can create tables from the source
upstream SQL Server database that have [Change Data Capture enabled](https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server).
You can create multiple tables that reference the same table in the source.

See [`CREATE TABLE FROM SOURCE`](/sql/create-table/) for details.

#### Handling table schema changes

The use of the `CREATE SOURCE` with the new [`CREATE TABLE FROM
SOURCE`](/sql/create-table/) allows for the handling of certain upstream DDL
changes without downtime.

See [Guide: Handle upstream schema changes with zero downtime](/ingest-data/sql-server/source-versioning/) for details.

#### Supported types

With the new syntax, after a SQL Server source is created, you [`CREATE TABLE
FROM SOURCE`](/sql/create-table/) to create a corresponding table in
Matererialize and start ingesting data.

<p>Materialize natively supports the following SQL Server types:</p>
<ul style="column-count: 3">
<li><code>tinyint</code></li>
<li><code>smallint</code></li>
<li><code>int</code></li>
<li><code>bigint</code></li>
<li><code>real</code></li>
<li><code>double precision</code></li>
<li><code>float</code></li>
<li><code>bit</code></li>
<li><code>decimal</code></li>
<li><code>numeric</code></li>
<li><code>money</code></li>
<li><code>smallmoney</code></li>
<li><code>char</code></li>
<li><code>nchar</code></li>
<li><code>varchar</code></li>
<li><code>varchar(max)</code></li>
<li><code>nvarchar</code></li>
<li><code>nvarchar(max)</code></li>
<li><code>sysname</code></li>
<li><code>binary</code></li>
<li><code>varbinary</code></li>
<li><code>json</code></li>
<li><code>date</code></li>
<li><code>time</code></li>
<li><code>smalldatetime</code></li>
<li><code>datetime</code></li>
<li><code>datetime2</code></li>
<li><code>datetimeoffset</code></li>
<li><code>uniqueidentifier</code></li>
</ul>

For more information, including strategies for handling unsupported types,
see [`CREATE TABLE FROM SOURCE`](/sql/create-table/).

### Monitoring source progress

[//]: # "TODO(morsapaes) Replace this section with guidance using the new
progress metrics in mz_source_statistics + console monitoring, when available
(also for PostgreSQL)."

By default, SQL Server sources expose progress metadata as a subsource that you
can use to monitor source **ingestion progress**. The name of the progress
subsource can be specified when creating a source using the `EXPOSE PROGRESS
AS` clause; otherwise, it will be named `<src_name>_progress`.

The following metadata is available for each source as a progress subsource:

Field     | Type                          | Details
----------|-------------------------------|--------------
`lsn`     | [`bytea`](/sql/types/bytea/)  | The upper-bound [Log Sequence Number](https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-log-architecture-and-management-guide) replicated thus far into Materialize.

And can be queried using:

```mzsql
SELECT lsn
FROM <src_name>_progress;
```

The reported `lsn` should increase as Materialize consumes **new** CDC events
from the upstream SQL Server database. For more details on monitoring source
ingestion progress and debugging related issues, see [Troubleshooting](/ops/troubleshooting/).

## Example

> **Important:** Before creating a SQL Server source, you must enable Change Data Capture and
> `SNAPSHOT` transaction isolation in the upstream database.

### Creating a source {#create-source-example}

#### Prerequisite: Creating a connection to SQL Server

First, you must create a connection to your SQL Server database. A connection describes how to connect and authenticate to an external system you
want Materialize to read data from.

Once created, a connection is **reusable** across multiple `CREATE SOURCE`
statements. For more details on creating connections, check the
[`CREATE CONNECTION`](/sql/create-connection/#sql-server) documentation page.

```mzsql
CREATE SECRET sqlserver_pass AS '<SQL_SERVER_PASSWORD>';

CREATE CONNECTION sqlserver_connection TO SQL SERVER (
    HOST 'instance.foo000.us-west-1.rds.amazonaws.com',
    PORT 1433,
    USER 'materialize',
    PASSWORD SECRET sqlserver_pass,
    DATABASE '<DATABASE_NAME>'
);
```

If your SQL Server instance is not exposed to the public internet, you can
[tunnel the connection](/sql/create-connection/#network-security-connections)
through and SSH bastion host.

**SSH tunnel:**
```mzsql
CREATE CONNECTION ssh_connection TO SSH TUNNEL (
    HOST 'bastion-host',
    PORT 22,
    USER 'materialize',
    DATABASE '<DATABASE_NAME>'
);
```

```mzsql
CREATE CONNECTION sqlserver_connection TO SQL SERVER (
    HOST 'instance.foo000.us-west-1.rds.amazonaws.com',
    SSH TUNNEL ssh_connection,
    DATABASE '<DATABASE_NAME>'
);
```

For step-by-step instructions on creating SSH tunnel connections and configuring
an SSH bastion server to accept connections from Materialize, check
[this guide](/ops/network-security/ssh-tunnel/).

#### Creating the source in Materialize

You **must** enable Change Data Capture, see [Enable Change Data Capture SQL Server Instructions](/ingest-data/sql-server/self-hosted/#a-configure-sql-server).

Once CDC is enabled for all of the tables you wish to create subsources for, you can create a `SOURCE` in
Materialize to begin replicating data!

_Create source from the connection we just created_

```mzsql
CREATE SOURCE mz_source
    FROM SQL SERVER CONNECTION sqlserver_connection;
```

After a source is created, you can create a table from the source, referencing specific table(s).

_Creates a table in Materialize from the upstream table dbo.items_
```mzsql
CREATE TABLE items FROM SOURCE mz_source(REFERENCE dbo.items);
```

## Related pages

- [`CREATE SECRET`](/sql/create-secret)
- [`CREATE CONNECTION`](/sql/create-connection)
- [`CREATE SOURCE`](../)
