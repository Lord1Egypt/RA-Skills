# CREATE SOURCE: MySQL (New Syntax)
Connecting Materialize to a MySQL database for Change Data Capture (CDC).
> **Public Preview:** This feature is in public preview.

> **Disambiguation:** This page reflects the new syntax which allows Materialize to handle upstream DDL changes, specifically adding or dropping columns, without downtime. For the deprecated syntax, see the [old reference page](/sql/create-source/mysql/).

Creates a new source from MySQL.  Materialize
supports creating sources from MySQL version 8.0.1&#43;.  Once a new source is created, you can <a href="/sql/create-table/" ><code>CREATE TABLE FROM SOURCE</code></a>
to create the corresponding tables in Materialize and start the data ingestion
process.

## Prerequisites

<p>To create a source from MySQL(8.0.1+), you must first:</p>
<ul>
<li><strong>Configure upstream MySQL instance</strong>
<ul>
<li>Enable <a href="#change-data-capture" >GTID-based binary log(binlog)
replication</a>. You <strong>must</strong> set
<a href="#change-data-capture" ><code>binlog_row_metadata=FULL</code></a> to use the new
<code>CREATE SOURCE</code> syntax.</li>
<li>Create a replication user and password for Materialize to use to
connect.</li>
</ul>
</li>
<li><strong>Configure network security</strong>
<ul>
<li>Ensure Materialize can connect to your MySQL instance.</li>
</ul>
</li>
<li><strong>Create a connection to MySQL in Materialize</strong>
<ul>
<li>The <a href="/sql/create-connection/#mysql" >connection setup</a> depends on the
network security configuration.</li>
</ul>
</li>
</ul>

## Syntax

To create a source from an external MySQL database:

```mzsql
CREATE SOURCE [IF NOT EXISTS] <source_name>
[IN CLUSTER <cluster_name>]
FROM MYSQL CONNECTION <connection_name>
[WITH ( <with_option> [, ...] )]
;

```

| Syntax element | Description |
| --- | --- |
| **IF NOT EXISTS** | *Optional.* If specified, do not throw an error if a source with the same name already exists. Instead, issue a notice and skip the source creation.  |
| `<source_name>` | The name of the source to create. Names for sources must follow the [naming guidelines](/sql/identifiers/#naming-restrictions).  |
| **IN CLUSTER** `<cluster_name>` | *Optional.* The [cluster](/sql/create-cluster) to maintain this source. Otherwise, the source will be created in the active cluster.  {{< tip >}} If possible, use a cluster dedicated just for sources. See also [Operational guidelines](/manage/operational-guidelines/#sources). {{< /tip >}}  |
| `<connection_name>` | The name of the MySQL connection to use for the source. For details on creating connections, see [`CREATE CONNECTION`](/sql/create-connection/#mysql).  A connection is **reusable** across multiple `CREATE SOURCE` statements.  To start ingesting data, create a [`CREATE TABLE FROM SOURCE`](/sql/create-table/) statement for each upstream table to replicate.  |
| **WITH** (`<with_option>` [, ...]) | *Optional.* The following `<with_option>`s are supported:  \| Option \| Description \| \|--------\|-------------\| \| `TIMESTAMP INTERVAL [=] <interval>` \| The interval at which timestamps are assigned to data read from this source. Accepts positive [interval](/sql/types/interval/) values (e.g. `'500ms'`, `'1s'`). The value must be between the system parameters `min_timestamp_interval` and `max_timestamp_interval`. Default: the value of the `default_timestamp_interval` system parameter (`1s`). The interval can also be changed after creation with [`ALTER SOURCE`](/sql/alter-source/). \|  |

## Ingesting data

After a source is created, you can create tables from the source referencing
upstream MySQL tables that have [GTID-based binlog replication
enabled](#change-data-capture) (Note: `binlog_row_metadata=FULL` is required to
use the new syntax). You can create multiple tables that reference the same
upstream table. See [`CREATE TABLE FROM SOURCE`](/sql/create-table/) for
details.

### Handling table schema changes

The use of `CREATE SOURCE` with the new [`CREATE TABLE FROM
SOURCE`](/sql/create-table/) allows for the handling of certain upstream DDL
changes, specifically adding or dropping columns in the upstream tables, without
downtime.

See [Guide: Handle upstream schema
changes](/ingest-data/mysql/source-versioning/) for details.

### Supported types

With the new syntax, after a MySQL source is created, you [`CREATE TABLE FROM
SOURCE`](/sql/create-table/) to create a corresponding table in Materialize and
start ingesting data.

<p>Materialize natively supports the following MySQL types:</p>
<ul style="column-count: 3">
<li><code>bigint</code></li>
<li><code>binary</code></li>
<li><code>bit</code></li>
<li><code>blob</code></li>
<li><code>boolean</code></li>
<li><code>char</code></li>
<li><code>date</code></li>
<li><code>datetime</code></li>
<li><code>decimal</code></li>
<li><code>double</code></li>
<li><code>float</code></li>
<li><code>int</code></li>
<li><code>json</code></li>
<li><code>longblob</code></li>
<li><code>longtext</code></li>
<li><code>mediumblob</code></li>
<li><code>mediumint</code></li>
<li><code>mediumtext</code></li>
<li><code>numeric</code></li>
<li><code>real</code></li>
<li><code>smallint</code></li>
<li><code>text</code></li>
<li><code>time</code></li>
<li><code>timestamp</code></li>
<li><code>tinyblob</code></li>
<li><code>tinyint</code></li>
<li><code>tinytext</code></li>
<li><code>varbinary</code></li>
<li><code>varchar</code></li>
</ul>

<p>When replicating tables that contain the <strong>unsupported <a href="/sql/types/" >data
types</a></strong>, you can:</p>
<ul>
<li>
<p>Use <a href="/sql/create-source/mysql/#handling-unsupported-types" ><code>TEXT COLUMNS</code>
option</a> for the
following unsupported  MySQL types:</p>
<ul>
<li><code>enum</code></li>
<li><code>year</code></li>
</ul>
<p>The specified columns will be treated as <code>text</code> and will not offer the
expected MySQL type features.</p>
</li>
<li>
<p>Use the <a href="/sql/create-source/mysql/#excluding-columns" ><code>EXCLUDE COLUMNS</code></a>
option to exclude any columns that contain unsupported data types.</p>
</li>
</ul>

For more information, including strategies for handling unsupported types,
see [`CREATE TABLE FROM SOURCE`](/sql/create-table/).

### Upstream table truncation restrictions

<p>Avoid truncating upstream tables that are being replicated into Materialize.
If a replicated upstream table is truncated, the corresponding
subsource in Materialize becomes inaccessible and will not
produce any data until it is recreated.</p>
<p>Instead of truncating, use an unqualified <code>DELETE</code> to remove all rows from
the upstream table:</p>
<div class="highlight"><pre tabindex="0" class="chroma"><code class="language-mzsql" data-lang="mzsql"><span class="line"><span class="cl"><span class="k">DELETE</span> <span class="k">FROM</span> <span class="n">t</span><span class="p">;</span>
</span></span></code></pre></div>

For additional considerations, see also [`CREATE TABLE`](/sql/create-table/).

### Change data capture

> **Note:** For step-by-step instructions on enabling GTID-based binlog replication for your
> MySQL service, see the integration guides:
> - [Amazon Aurora for MySQL](/ingest-data/mysql/amazon-aurora/)
> - [Amazon RDS for MySQL](/ingest-data/mysql/amazon-rds/)
> - [Azure DB for MySQL](/ingest-data/mysql/azure-db/)
> - [Google Cloud SQL for MySQL](/ingest-data/mysql/google-cloud-sql/)
> - [Self-hosted MySQL](/ingest-data/mysql/self-hosted/)

The source uses MySQL's binlog replication protocol to **continually ingest
changes** resulting from `INSERT`, `UPDATE` and `DELETE` operations in the
upstream database. This process is known as _change data capture_.

The replication method used is based on [global transaction identifiers
(GTIDs)](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids.html), and
guarantees **transactional consistency** — any operation inside a MySQL
transaction is assigned the same timestamp in Materialize, which means that the
source will never show partial results based on partially replicated
transactions.

Before creating a source in Materialize, you **must** configure the upstream
MySQL database for GTID-based binlog replication:

<table>
<thead>
<tr>

<th>MySQL Configuration</th>

<th>Value</th>

<th>Notes</th>

</tr>
</thead>
<tbody>

<tr>

<td>
<code>log_bin</code>
</td>

<td>
<code>ON</code>
</td>

<td>

</td>

</tr>

<tr>

<td>
<code>binlog_row_image</code>
</td>

<td>
<code>FULL</code>
</td>

<td>

</td>

</tr>

<tr>

<td>
<code>binlog_row_metadata</code>
</td>

<td>
<code>FULL</code>
</td>

<td>
<ul>
<li><strong>Required</strong> to use <a href="/sql/create-source/mysql-v2/" ><code>CREATE SOURCE</code> (New
syntax)</a>.</li>
<li>Highly recommended for use with the <a href="/sql/create-source/mysql/" ><code>CREATE SOURCE</code> (Legacy
syntax)</a>.</li>
</ul>

</td>

</tr>

<tr>

<td>
<code>binlog_format</code>
</td>

<td>
<code>ROW</code>
</td>

<td>
<a href="https://dev.mysql.com/doc/refman/8.0/en/replication-options-binary-log.html#sysvar_binlog_format" >Deprecated as of MySQL 8.0.34</a>. Newer versions of MySQL default to row-based logging.
</td>

</tr>

<tr>

<td>
<code>gtid_mode</code>
</td>

<td>
<code>ON</code>
</td>

<td>

</td>

</tr>

<tr>

<td>
<code>enforce_gtid_consistency</code>
</td>

<td>
<code>ON</code>
</td>

<td>

</td>

</tr>

<tr>

<td>
<code>replica_preserve_commit_order</code>
</td>

<td>
<code>ON</code>
</td>

<td>
Only required when connecting Materialize to a read-replica.
</td>

</tr>

</tbody>
</table>

> **Tip:** For `binlog_row_metadata`, using `SET GLOBAL binlog_row_metadata = FULL;` does
> not persist across MySQL server restarts. To make
> the setting durable, use `SET PERSIST` (MySQL 8.0.11+) or set
> `binlog_row_metadata=FULL` in the server's configuration file. On managed
> services, set the variable through the service's parameter configuration
> instead.

If you're running MySQL using a managed service, additional configuration
changes might be required. To enable GTID-based binlog replication for your
MySQL service, see the integration guides.

#### Binlog retention

> **Warning:** If Materialize tries to resume replication and finds GTID gaps due to missing
> binlog files, the source enters an errored state and you have to drop and
> recreate it.

By default, MySQL retains binlog files for **30 days** (i.e., 2592000 seconds)
before automatically removing them. This is configurable via the
[`binlog_expire_logs_seconds`](https://dev.mysql.com/doc/mysql-replication-excerpt/8.0/en/replication-options-binary-log.html#sysvar_binlog_expire_logs_seconds)
system variable. We recommend using the default value for this configuration in
order to not compromise Materialize's ability to resume replication in case of
failures or restarts.

In some MySQL managed services, binlog expiration can be overridden by a
service-specific configuration parameter. It's important that you double-check
if such a configuration exists, and ensure it's set to the maximum interval
available.

As an example, [Amazon RDS for MySQL](/ingest-data/mysql/amazon-rds/) has its
own configuration parameter for binlog retention ([`binlog retention hours`](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/mysql-stored-proc-configuring.html#mysql_rds_set_configuration-usage-notes.binlog-retention-hours))
that overrides `binlog_expire_logs_seconds` and is set to `NULL` by default.

### Monitoring source progress

By default, MySQL sources expose progress metadata as a subsource that you can
use to monitor source **ingestion progress**. The name of the progress subsource
can be specified when creating a source using the `EXPOSE PROGRESS AS` clause;
otherwise, it will be named `<src_name>_progress`.

The following metadata is available for each source as a progress subsource:

| Field             | Type                                   | Details                                                                                          |
| ----------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------ |
| `source_id_lower` | [`uuid`](/sql/types/uuid/)             | The lower-bound GTID `source_id` of the GTIDs covered by this range.                             |
| `source_id_upper` | [`uuid`](/sql/types/uuid/)             | The upper-bound GTID `source_id` of the GTIDs covered by this range.                             |
| `transaction_id`  | [`uint8`](/sql/types/uint/#uint8-info) | The `transaction_id` of the next GTID possible from the GTID `source_id`s covered by this range. |

And can be queried using:

```mzsql
SELECT transaction_id
FROM <src_name>_progress;
```

Progress metadata is represented as a [GTID set](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids-concepts.html)
of future possible GTIDs, which is similar to the
[`gtid_executed`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-gtids.html#sysvar_gtid_executed)
system variable on a MySQL replica. The reported `transaction_id` should
increase as Materialize consumes **new** binlog records from the upstream MySQL
database. For more information, see [Troubleshooting](/ops/troubleshooting/).

## Example

> **Important:** Before creating a MySQL source, you must enable [GTID-based binary log (binlog)
> replication](#change-data-capture), including setting
> [`binlog_row_metadata=FULL`](#change-data-capture) to use the new syntax.

### Prerequisites

<p>To create a source from MySQL(8.0.1+), you must first:</p>
<ul>
<li><strong>Configure upstream MySQL instance</strong>
<ul>
<li>Enable <a href="#change-data-capture" >GTID-based binary log(binlog)
replication</a>. You <strong>must</strong> set
<a href="#change-data-capture" ><code>binlog_row_metadata=FULL</code></a> to use the new
<code>CREATE SOURCE</code> syntax.</li>
<li>Create a replication user and password for Materialize to use to
connect.</li>
</ul>
</li>
<li><strong>Configure network security</strong>
<ul>
<li>Ensure Materialize can connect to your MySQL instance.</li>
</ul>
</li>
<li><strong>Create a connection to MySQL in Materialize</strong>
<ul>
<li>The <a href="/sql/create-connection/#mysql" >connection setup</a> depends on the
network security configuration.</li>
</ul>
</li>
</ul>

For details, see the [MySQL integration
guides](/ingest-data/mysql/#integration-guides).

### Create a source

Once you have configured the upstream MySQL, network security, and created
the [connection to MySQL](/sql/create-connection/#mysql), you can create
the source. In this example, assume the connection you created is named
`mysql_connection`.
```mzsql
CREATE SOURCE mysql_source
FROM MYSQL CONNECTION mysql_connection;

```

After a source is created, you can [create a table from the
source](/sql/create-table/), referencing specific upstream table(s). Use a
[DDL transaction block](/sql/begin/#ddl-only-transactions) to create
multiple tables from the same source.
```mzsql
BEGIN;
CREATE TABLE items
FROM SOURCE mysql_source (REFERENCE mydb.items);

CREATE TABLE orders
FROM SOURCE mysql_source (REFERENCE mydb.orders);
COMMIT;

```

## Related pages

- [`CREATE TABLE`](/sql/create-table/)
- [`CREATE SECRET`](/sql/create-secret)
- [`CREATE CONNECTION`](/sql/create-connection)
- [`CREATE SOURCE`](../)
- [MySQL integration guides](/ingest-data/mysql/#integration-guides)
