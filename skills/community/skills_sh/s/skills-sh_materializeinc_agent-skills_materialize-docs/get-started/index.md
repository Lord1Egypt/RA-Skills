# What is Materialize?

Learn more about Materialize

Materialize is the live data layer for apps and AI agents. To keep results
up-to-date as new data arrives, Materialize incrementally updates results as it
ingests data rather than recalculating results from scratch.

## Materialize offerings

Materialize is available as:

| Offering | Description | Get Started 🚀  |
|----------|-------------|-----------------|
| **Materialize Cloud** | Materialize Cloud is a fully-managed service for Materialize. | Sign up for a [free trial account](https://materialize.com/register/?utm_campaign=General&utm_source=documentation) on Materialize Cloud and try out the [Quickstart](/get-started/quickstart/). |
| **Materialize Self-Managed** | Deploy and operate Materialize in your Kubernetes environment. Whereas Materialize Cloud gives you a fully managed service, Materialize Self-Managed allows you to deploy Materialize in your own infrastructure.<br><br><p>Self-managed Materialize is available as a paid Enterprise Edition and a free
Community Edition:</p>
<table>
  <thead>
      <tr>
          <th>Feature</th>
          <th>Enterprise Edition</th>
          <th>Community Edition</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><strong>Maximum Usage Limits (Memory)</strong></td>
          <td>None</td>
          <td>24 GiB</td>
      </tr>
      <tr>
          <td><strong>Maximum Usage Limits (Disk)</strong></td>
          <td>None</td>
          <td>48 GiB</td>
      </tr>
      <tr>
          <td><strong><a href="/support/" >Support</a></strong></td>
          <td><a href="https://materialize.com/self-managed/enterprise-license/" >Per terms of your license</a></td>
          <td><a href="/support/" >Community slack or messenger app</a></td>
      </tr>
      <tr>
          <td><strong>License</strong></td>
          <td><a href="https://materialize.com/self-managed/enterprise-license/" >Enterprise License - Contact Us</a></td>
          <td><a href="/license/" >BSL/Privacy Policy</a></td>
      </tr>
  </tbody>
</table> | [Install self-managed](/get-started/install/) and try out the [Quickstart](/get-started/quickstart/). |
| **Materialize Emulator** | Materialize Emulator is an all-in-one Docker image that provides the fastest way to get hands-on experience with Materialize for local development. | [Download and run Materialize Emulator](/get-started/install-materialize-emulator/) and try out the [Quickstart](/get-started/quickstart/). |

## Key features

Materialize combines the accessibility of SQL databases with a streaming engine
that is horizontally scalable, highly available, and strongly consistent.

### Incremental updates

In traditional databases, materialized views help you avoid re-running heavy
queries, typically by caching queries to serve results faster. But you have
to make a compromise between the freshness of the results, the cost of
refreshing the view, and the complexity of the SQL statements you can use.

In Materialize, you don't have to make such compromises. Materialize supports
incrementally updated view results that are **always fresh** (even when using
complex SQL statements, like multi-way joins with aggregations) for *both*:

- [Indexed views](/concepts/views/#indexes-on-views) and

- [Materialized views](/concepts/views/#materialized-views).

How?
Its engine is built on [Timely](https://github.com/TimelyDataflow/timely-dataflow#timely-dataflow)
and [Differential Dataflow](https://github.com/timelydataflow/differential-dataflow#differential-dataflow)
— data processing frameworks backed by many years of research and optimized for
this exact purpose.

### Standard SQL support

Like most databases, you interact with Materialize using **SQL**. You can build
complex analytical
workloads using **[any type of join](/sql/select/join/)** (including
non-windowed joins and joins on arbitrary conditions) as well as leverage new
SQL patterns enabled by streaming like [**Change Data Capture
(CDC)**](/ingest-data/), [**temporal
filters**](/sql/patterns/temporal-filters/), and
[**subscriptions**](/sql/subscribe/).

<p>Materialize follows the SQL standard (SQL-92) implementation and aims for
compatibility with the PostgreSQL dialect. It <strong>does not</strong> aim for
compatibility with a specific version of PostgreSQL. This means that
Materialize might support syntax from any released PostgreSQL version, but does
not provide full coverage of the PostgreSQL dialect. The implementation and
performance of specific features (like <a href="/transform-data/idiomatic-materialize-sql/appendix/window-function-to-materialize" >window functions</a>)
might also differ, because Materialize uses an entirely different database
engine based on <a href="/get-started/#incremental-updates" >Timely and Differential Dataflow</a>.</p>
<p>If you need specific syntax or features that are not currently supported in
Materialize, please submit a <a href="/support/#share-your-feedback" >feature request</a>.</p>

### Real-time data ingestion

Materialize provides **native connectors** that allow ingesting data from various external systems:

<div class="multilinkbox">
<div class="linkbox ">
  <div class="title">
    Databases (CDC)
  </div>
  <ul>
<li><a href="/ingest-data/postgres/" >PostgreSQL</a></li>
<li><a href="/ingest-data/mysql/" >MySQL</a></li>
<li><a href="/ingest-data/sql-server/" >SQL Server</a></li>
<li><a href="/ingest-data/cdc-cockroachdb/" >CockroachDB</a></li>
<li><a href="/ingest-data/mongodb/" >MongoDB</a></li>
</ul>

</div>

<div class="linkbox ">
  <div class="title">
    Message Brokers
  </div>
  <ul>
<li><a href="/ingest-data/kafka/" >Kafka</a></li>
<li><a href="/sql/create-source/kafka" >Redpanda</a></li>
</ul>

</div>

<div class="linkbox ">
  <div class="title">
    Webhooks
  </div>
  <ul>
<li><a href="/ingest-data/webhooks/amazon-eventbridge/" >Amazon EventBridge</a></li>
<li><a href="/ingest-data/webhooks/segment/" >Segment</a></li>
<li><a href="/sql/create-source/webhook" >Other webhooks</a></li>
</ul>

</div>

</div>

For more information, see [Ingest Data](/ingest-data/) and
[Integrations](/integrations/).

### PostgreSQL wire-compatibility

Every database needs a protocol to standardize communication with the outside
world. Materialize uses the [PostgreSQL wire protocol](https://datastation.multiprocess.io/blog/2022-02-08-the-world-of-postgresql-wire-compatibility.html),
which allows it to integrate out-of-the-box with many SQL clients and other
tools in the data ecosystem that support PostgreSQL — like [dbt](/integrations/dbt/).

Don't see the a tool that you’d like to use with Materialize listed under
[Tools and integrations](/integrations/)? Let us know by submitting a
[feature request](https://github.com/MaterializeInc/materialize/discussions/new?category=feature-requests&labels=A-integration)!

### Strong consistency guarantees

By default, Materialize provides the highest level of transaction isolation:
[**strict serializability**](https://jepsen.io/consistency/models/strict-serializable).
This means that it presents as if it were a single process, despite spanning a
large number of threads, processes, and machines. Strict serializability avoids
common pitfalls like eventual consistency and dual writes, which affect the
correctness of your results. You can [adjust the transaction isolation level](/overview/isolation-level/)
depending on your consistency and performance requirements.

## Learn more

- [Key concepts](/concepts/)
- [Get started with Materialize](/get-started/quickstart)

---

## Arrangements

The mechanisms that maintain materialized views for Materialize dataflows are
called **arrangements**. Understanding arrangements better can help you make
decisions that will reduce memory usage while maintaining performance.

## Materialized views

Before we talk about the arrangements that maintain materialized views, let's
review what materialized views are, how they work in traditional databases, and
how they work in Materialize.

A view is simply a query saved under a name for convenience; the query is
executed each time the view is referenced, without any savings in performance
or speed. But some databases also support something more powerful: materialized
views, which save the *results* of the query for quicker access.

Traditional databases typically only have limited support for materialized views
in two ways: first, the updates to the views generally occur at set intervals,
so views are not updated in real time, and second, only a limited subset of SQL
syntax is supported. In cases where a traditional database *does* support
refreshes for each data update, it tends to be very slow. These limitations
stem from limited support for incremental updates; most databases are not
designed to maintain long-running incremental queries, but instead are
optimized for queries that are executed once and then wound down. This means
that when the data changes, the materialized view must be recomputed from
scratch in all but a few simple cases.

Our mission at Materialize is to manage materialized views better than this.
Materialize supports incrementally updating a much broader set of views than is
common in traditional databases (e.g. views over multi-way joins with complex
aggregations), and can do incremental updates in the presence of arbitrary
inserts, updates, and deletes in the input streams while maintaining
correctness.

## Dataflows

Materialize can make incremental updates efficiently because it's built on an
incremental data-parallel compute engine, [Differential Dataflow](https://timelydataflow.github.io/differential-dataflow/introduction.html),
which in turn is built on a distributed processing framework called
[Timely Dataflow](https://timelydataflow.github.io/timely-dataflow/).

When you create a materialized view and issue a query, Materialize creates
a **dataflow**. A dataflow consists of instructions on how to respond to data
input and to changes to that data. Once executed, the dataflow computes the
result of the SQL query, polls the source for updates, and then incrementally
updates the query results when new data arrives.

### Collections

Materialize dataflows act on **collections** of data, [multisets](https://en.wikipedia.org/wiki/Multiset)
that store each event in an update
stream as a triple of `(data, time, diff)`.

Term | Definition
-----|-----------
**data**  |  The record update.
**time**  |  The logical timestamp of the update.
**diff**  |  The change in the number of copies of the record (typically `-1` for deletion, `1` for addition).

## Arrangements

A collection provides a data stream of updates as they happen. To provide fast
access to the changes to individual records, the collection can be represented
in an alternate form, indexed on `data` to present the sequence of changes
(`time, diff`) the collection has undergone. This indexed representation is
called an **arrangement**.

Materialize builds and maintains indexes on both the input and output
collections as well as for many intermediate collections created when
processing a query. Because queries can overlap, Materialize might need to
build the exact same indexes for multiple queries. Instead of performing
redundant work, Materialize builds the index once and maintains it in memory,
sharing the required resources across all queries that use the indexed data.
The index is then effectively a sunk cost, and the cost of each query is
determined only by the new work it introduces.

You can find a more detailed analysis of the arrangements built for different
types of queries in our blog post on [Joins in Materialize](https://materialize.com/joins-in-materialize).

### Arrangement size

The size of an arrangement, or amount of memory it requires, is roughly
proportional to its number of distinct `(data, time)` pairs, which can be small
even if the number of records is large. As an illustration, consider a
histogram of taxi rides grouped by the number of riders and the fare amount.
The number of distinct `(rider, fare)` pairs will be much smaller than the
number of total rides that take place.

The amount of memory that the arrangement requires is then further reduced by
background compaction of historical data.

## Analyzing arrangements

Materialize provides various tools that allow you to analyze arrangements,
although they are post-hoc tools best used for debugging, rather than planning
tools to be used before creating indexes or views. See [Diagnosing Using SQL](/ops/troubleshooting/)
and [`EXPLAIN PLAN`](/sql/explain-plan/) for more details.

## Reducing memory usage

### Creating indexes manually

When creating an arrangement for a join where the key is not clear, Materialize
attempts to choose a key that will ensure that data is well distributed. If
there is a primary key, that will be used; if there are source fields not
required by the query, they are not included. Often Materialize can pull
primary key info from a Confluent schema.

If Materialize cannot detect a primary key, the default key is the full set of
columns, in order to ensure good data distribution. Creating an unmaterialized
view and then specifying a custom index makes the key smaller.

For more information on when and how to create indexes, see
[Optimization](../../ops/optimization/).
For more in-depth details on joins, see [Joins in Materialize](https://materialize.com/joins-in-materialize/).

### Type casting

Currently, Materialize handles implicit casts inserted in join constraints in a very memory-intensive way.
Until this issue
is resolved, you can reduce memory usage by building an index on the view with
the type changed for any queries that include implicit casts, for example,
when you combine 32-bit and 64-bit numbers.

## Related pages

* [Optimization](../../ops/optimization/)
* [Joins in Materialize](https://materialize.com/joins-in-materialize/)
* [Diagnosing Using SQL](/ops/troubleshooting/)
* [Deployment](/ops/optimization/)
* [Differential Dataflow](https://timelydataflow.github.io/differential-dataflow/)

---

## Download and run Materialize Emulator

The Materialize Emulator is an all-in-one Docker image available on Docker Hub
for testing and evaluation purposes. The Materialize Emulator is not
representative of Materialize's performance and full feature set.

> **Important:** The Materialize Emulator is <redb> not suitable for production workloads.</redb>.

### Materialize Emulator

Materialize Emulator is the easiest way to get started with Materialize, but is
not suitable for full feature set evaluations or production workloads.

| Materialize Emulator              | Details    |
|-----------------------------------|------------|
| **What is it**                    | A single Docker container version of Materialize. |
| **Best For**                       | Prototyping and CI jobs. |
| **Known Limitations**     | Not indicative of true Materialize performance. <br>Services are bundled in a single container. <br>No fault tolerance. <br>No data persistence. <br>No support for version upgrades. |
| **Evaluation Experience**          | Download from Docker Hub. |
| **Support**                        | [Materialize Community Slack channel](https://materialize.com/s/chat).|
| **License/legal arrangement**      | [BSL/Materialize's privacy policy](#license-and-privacy-policy) |

### Prerequisites

- Docker. If [Docker](https://www.docker.com/) is not installed, refer to its
[official documentation](https://docs.docker.com/get-docker/) to install.

### Run Materialize Emulator

> **Note:** - Use of the Docker image is subject to Materialize's [BSL License](https://github.com/MaterializeInc/materialize/blob/main/LICENSE).
> - By downloading the Docker image, you are agreeing to Materialize's [privacy policy](https://materialize.com/privacy-policy/).

1. In a terminal, issue the following command to run a Docker container from the
   Materialize Emulator image. The command downloads the image, if one has not
   been already downloaded.

   ```sh
   docker run -d -p 127.0.0.1:6874:6874 -p 127.0.0.1:6875:6875 -p 127.0.0.1:6876:6876 -p 127.0.0.1:6877:6877 materialize/materialized:v26.28.0
   ```

   When running locally:

   - The Docker container binds exclusively to localhost for security reasons.
   - The [Materialize Console](/console/) is available on port `6874`.
   - The SQL interface is available on port `6875`.
   - Logs are available via `docker logs <container-id>`.
   - A default user `materialize` is created.
   - A default database `materialize` is created.

1. <a name="materialize-emulator-connect-client"></a>

   Open the Materialize Console in your browser at [http://localhost:6874](http://localhost:6874).

   To streamline development and troubleshooting, we recommend configuring our
   [MCP
   Server](https://materialize.com/docs/integrations/mcp-server/mcp-developer/).

   You can also connect to the Materialize Emulator using your
   preferred SQL client, using the following connection field values:

   | Field    | Value         |
   |----------|---------------|
   | Server   | `localhost`   |
   | Database | `materialize` |
   | Port     | `6875`        |
   | Username | `materialize` |

   For example, if using [`psql`](/integrations/sql-clients/#psql):

   ```sh
   psql postgres://materialize@localhost:6875/materialize
   ```

1. Once connected, you can get started with the
   [Quickstart](/get-started/quickstart).

### Next steps

- To start ingesting your own data from an external system like Kafka, MySQL or
  PostgreSQL, check the documentation for [sources](/sql/create-source/).

- Join the [Materialize Community on Slack](https://materialize.com/s/chat).

- To fully evaluate Materialize Cloud, sign up for a [free trial Materialize
  Cloud
  account](https://materialize.com/register/?utm_campaign=General&utm_source=documentation).
  The full experience of Materialize is also available as a self-managed
  offering. See [Self-managed Materialize](/self-managed-deployments/).

### Technical Support

For questions, discussions, or general technical support, join the [Materialize
Community on Slack](https://materialize.com/s/chat).

#### `mz-debug`

Materialize provides a [`mz-debug`]command-line debug tool called  that helps collect diagnostic information from your emulator environment. This tool can gather:
- Docker logs and resource information
- Snapshots of system catalog tables from your Materialize instance

To debug your emulator instance, you can use the following command:

```console
mz-debug emulator --docker-container-id <your-container-id>
```

This debug information can be particularly helpful when troubleshooting issues or when working with the Materialize support team.

For more detailed information about the debug tool, see the [`mz-debug` documentation](/integrations/mz-debug/).

### License and privacy policy

- Use of the Docker image is subject to Materialize's [BSL
  License](https://github.com/MaterializeInc/materialize/blob/main/LICENSE).

- By downloading the Docker image, you are agreeing to Materialize's
  [privacy policy](https://materialize.com/privacy-policy/).

#### Materialize Self-Managed Community Edition or the Materialize Emulator Privacy FAQ

When you use the Materialize Self-Managed Community Edition or the Materialize Emulator, we may collect the following information from the machine that runs the Materialize Self-Managed Community Edition or the Materialize Emulator software:

- The IP address of the machine running Materialize.

- If available, the cloud provider and region of the machine running
  Materialize.

- Usage data about your use of the product such as the types or quantity of
  commands you run, the number of clusters or indexes you are running, and
  similar feature usage information.

The collection of this data is subject to the [Materialize Privacy Policy](https://materialize.com/privacy-policy/).

Please note that if you visit our website or otherwise engage with us outside of
downloading the Materialize Self-Managed Community Edition or the Materialize
Emulator, we may collect additional information about you as further described
in our [Privacy Policy](https://materialize.com/privacy-policy/).

<style>
red { color: #d33902 }
redb { color: #d33902; font-weight: 500; }
</style>

---

## Install Self-Managed Materialize

<p>You can install Self-Managed Materialize on a Kubernetes cluster running
locally or on a cloud provider. Self-Managed Materialize requires:</p>
<ul>
<li>A Kubernetes (v1.31+) cluster.</li>
<li>PostgreSQL as a metadata database.</li>
<li>Blob storage.</li>
<li>A license key.</li>
</ul>
<h2 id="license-key">License key</h2>
<p>Starting in v26.0, Materialize requires a license key.</p>

| License key type | Deployment type | Action |
| --- | --- | --- |
| Community | New deployments | <p>To get a license key:</p> <ul> <li>If you have a Cloud account, visit the <a href="https://console.materialize.com/license/" ><strong>License</strong> page in the Materialize Console</a>.</li> <li>If you do not have a Cloud account, visit <a href="https://materialize.com/self-managed/community-license/" >https://materialize.com/self-managed/community-license/</a>.</li> </ul> |
| Community | Existing deployments | Contact <a href="https://materialize.com/docs/support/" >Materialize support</a>. |
| Enterprise | New deployments | Visit <a href="https://materialize.com/self-managed/enterprise-license/" >https://materialize.com/self-managed/enterprise-license/</a> to purchase an Enterprise license. |
| Enterprise | Existing deployments | Contact <a href="https://materialize.com/docs/support/" >Materialize support</a>. |

<h2 id="installation-guides">Installation guides</h2>
<p>The following installation guides are available to help you get started:</p>

<h3 id="install-using-helm-commands">Install using Helm Commands</h3>
<table>
  <thead>
      <tr>
          <th>Guide</th>
          <th>Description</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><a href="/self-managed-deployments/installation/install-on-local-kind/" >Install locally on Kind</a></td>
          <td>Uses standard Helm commands to deploy Materialize to a Kind cluster in Docker.</td>
      </tr>
  </tbody>
</table>

<h3 id="install-using-terraform-modules">Install using Terraform Modules</h3>
> **Note:** We recommend pinning your module sources to specific tags to avoid unexpected breaking
> changes in future versions.
> We recommend updating your module source tags when updating Materialize versions,
> taking care to follow any instructions in the release notes.

<table>
  <thead>
      <tr>
          <th>Guide</th>
          <th>Description</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><a href="/self-managed-deployments/installation/install-on-aws/" >Install on AWS</a></td>
          <td>Uses Terraform module to deploy Materialize to AWS Elastic Kubernetes Service (EKS).</td>
      </tr>
      <tr>
          <td><a href="/self-managed-deployments/installation/install-on-azure/" >Install on Azure</a></td>
          <td>Uses Terraform module to deploy Materialize to Azure Kubernetes Service (AKS).</td>
      </tr>
      <tr>
          <td><a href="/self-managed-deployments/installation/install-on-gcp/" >Install on GCP</a></td>
          <td>Uses Terraform module to deploy Materialize to Google Kubernetes Engine (GKE).</td>
      </tr>
  </tbody>
</table>

<h3 id="install-using-legacy-terraform-modules">Install using Legacy Terraform Modules</h3>
> **Note:** We recommend pinning your module sources to specific tags to avoid unexpected breaking
> changes in future versions.
> We recommend updating your module source tags when updating Materialize versions,
> taking care to follow any instructions in the release notes.

<table>
  <thead>
      <tr>
          <th>Guide</th>
          <th>Description</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td><a href="/self-managed-deployments/installation/legacy/install-on-aws-legacy/" >Install on AWS (Legacy Terraform)</a></td>
          <td>Uses legacy Terraform module to deploy Materialize to AWS Elastic Kubernetes Service (EKS).</td>
      </tr>
      <tr>
          <td><a href="/self-managed-deployments/installation/legacy/install-on-azure-legacy/" >Install on Azure (Legacy Terraform)</a></td>
          <td>Uses legacy Terraform module to deploy Materialize to Azure Kubernetes Service (AKS).</td>
      </tr>
      <tr>
          <td><a href="/self-managed-deployments/installation/legacy/install-on-gcp-legacy/" >Install on GCP (Legacy Terraform)</a></td>
          <td>Uses legacy Terraform module to deploy Materialize to Google Kubernetes Engine (GKE).</td>
      </tr>
  </tbody>
</table>

---

## Quickstart

<style>
    red { color: #d33902; }
    redb { color: #d33902; font-weight: 500; }
</style>

Materialize provides always-fresh results while also providing [strong
consistency guarantees](/reference/isolation-level/). In Materialize, both
[indexes](/concepts/indexes/ "Indexes represents query results stored in memory
within a cluster") and [materialized views](/concepts/views/#materialized-views)
**incrementally update** results when Materialize ingests new data; i.e., work
is performed on writes. Because work is performed on writes, reads from these
objects return up-to-date results while being computationally **free**.

In this quickstart, you will continuously ingest a sample auction data set to
build an operational use case around finding auction winners and auction
flippers. Specifically, you will:

- Create and query various [views](/concepts/views/) on sample auction data. The
  data is continually generated at 1 second intervals to mimic a data-intensive
  workload.

- Create an [index](/concepts/indexes "Indexes represents query results stored
  in memory within a cluster") to compute and store view results in memory. As
  new auction data arrives, the index **incrementally updates** view
  results instead of recalculating the results from scratch, making fresh
  results immediately available for reads.

- Create and query views to verify that Materialize always serves
  **consistent results**.

![Image of Quickstart in the Materialize Console](/images/quickstart-console.png "Quickstart in the Materialize Console")

## Prerequisite

To get started with Materialize Cloud, you will need a Materialize account. If
you do not have an account, you can [sign up for a free
trial](https://materialize.com/register/?utm_campaign=General&utm_source=documentation).

Alternatively:

- You can [download the Materialize
Emulator](/get-started/install-materialize-emulator/). However, the Materialize
Emulator does not provide the full experience of using Materialize.

- You can run against your [Self-managed
  Materialize](/self-managed-deployments/).

## Step 0. Open the SQL Shell

- If you have a Materialize account, navigate to the [Materialize
  Console](/console/) and sign in. By default, you should
  be in the SQL Shell. If you're already signed in, you can access the SQL Shell in the left-hand menu.

- If you are using the Materialize Emulator, open the Materialize Console in
  your browser at [http://localhost:6874](http://localhost:6874).

- If you are running against your own [Self-managed
  Materialize], open your deployment's Materialize Console.

## Step 1. Create a schema

By default, you are using the `quickstart` cluster, working in the
`materialize.public` [namespace](/sql/namespaces/), where:

- A [cluster](/concepts/clusters/) is an isolated pool of compute resources
  (CPU, memory, and scratch disk space) for running your workloads),

- `materialize` is the database name, and

- `public` is the schema name.

Create a separate schema for this quickstart. For a schema name to be valid:

- The first character must be either: an ASCII letter (`a-z` and `A-Z`), an
  underscore (`_`), or a non-ASCII character.

- The remaining characters can be: an ASCII letter (`a-z` and `A-Z`), ASCII
  numbers (`0-9`), an underscore (`_`), dollar signs (`$`), or a non-ASCII character.

Alternatively, by double-quoting the name, you can bypass the aforementioned
constraints with the following exception: schema names, whether double-quoted or
not, cannot contain the dot (`.`).

See also [Naming restrictions](/sql/identifiers/#naming-restrictions).

1. Enter a schema name in the text field and click the `Create` button.

1. Switch to the new schema. From the top of the SQL Shell, select your schema
   from the namespace dropdown.

## Step 2. Create the source

[Sources](/concepts/sources/) are external systems from which Materialize reads
in data. This tutorial uses Materialize's [sample `Auction` load
generator](/sql/create-source/load-generator/#auction) to create the source.

1. Create the [source](/concepts/sources "External systems from which
   Materialize reads data.") using the [`CREATE SOURCE`](/sql/create-source/)
   command.

   For the [sample `Auction` load
   generator](/sql/create-source/load-generator/#auction), the quickstart uses
   [`CREATE SOURCE`](/sql/create-source/) with the `FROM LOAD GENERATOR` clause
   that works specifically with Materialize's sample data generators. The
   tutorial specifies that the generator should emit new data every 1s.

    ```mzsql
    CREATE SOURCE auction_house
    FROM LOAD GENERATOR AUCTION
    (TICK INTERVAL '1s', AS OF 100000)
    FOR ALL TABLES;
    ```

    `CREATE SOURCE` can create **multiple** tables (referred to as `subsources`
    in Materialize) when ingesting data from multiple upstream tables. For each
    upstream table that is selected for ingestion, Materialize creates a
    subsource.

1. Use the [`SHOW SOURCES`](/sql/show-sources/) command to see the results of
   the previous step.

    ```mzsql
    SHOW SOURCES;
    ```

    The output should resemble the following:

    ```nofmt
    | name                   | type           | cluster    | comment |
    | ---------------------- | -------------- | ---------- | ------- |
    | accounts               | subsource      | quickstart |         |
    | auction_house          | load-generator | quickstart |         |
    | auction_house_progress | progress       | null       |         |
    | auctions               | subsource      | quickstart |         |
    | bids                   | subsource      | quickstart |         |
    | organizations          | subsource      | quickstart |         |
    | users                  | subsource      | quickstart |         |
    ```

    A [`subsource`](/sql/show-subsources) is how Materialize refers to a table
    that has the following properties:

    - A subsource can only be written by the source; in this case, the
      load-generator.

    - Users can read from subsources.

1. Use the [`SELECT`](/sql/select) statement to query `auctions` and `bids`.

    * View a sample row in `auctions`:

      ```mzsql
      SELECT * FROM auctions LIMIT 1;
      ```

      The output should return a single row (your results may differ):

      ```nofmt
       id    | seller | item               | end_time
      -------+--------+--------------------+---------------------------
       29550 | 2468   | Best Pizza in Town | 2024-07-25 18:24:25.805+00
      ```

    * View a sample row in `bids`:

      ```mzsql
      SELECT * FROM bids LIMIT 1;
      ```

      The output should return a single row (your results may differ):

      ```nofmt
       id     | buyer | auction_id | amount | bid_time
      --------+-------+------------+--------+---------------------------
       295641 | 737   | 29564      | 72     | 2024-07-25 18:25:42.911+00
      ```

    * To view the relationship between `auctions` and `bids`, you can join by
      the auction id:

      ```mzsql
      SELECT a.*, b.*
      FROM auctions AS a
      JOIN bids AS b
        ON a.id = b.auction_id
      LIMIT 3;
      ```

      The output should return (at most) 3 rows (your results may
      differ):

      ```nofmt
      | id    | seller | item               | end_time                   | id     | buyer | auction_id | amount | bid_time                   |
      | ----- | ------ | ------------------ | -------------------------- | ------ | ----- | ---------- | ------ | -------------------------- |
      | 15575 | 158    | Signed Memorabilia | 2024-07-25 20:30:25.085+00 | 155751 | 215   | 15575      | 27     | 2024-07-25 20:30:16.085+00 |
      | 15575 | 158    | Signed Memorabilia | 2024-07-25 20:30:25.085+00 | 155750 | 871   | 15575      | 63     | 2024-07-25 20:30:15.085+00 |
      | 15575 | 158    | Signed Memorabilia | 2024-07-25 20:30:25.085+00 | 155752 | 2608  | 15575      | 16     | 2024-07-25 20:30:17.085+00 |
      ```

      Subsequent steps in this quickstart uses a query to find winning bids for
      auctions to show how Materialize uses views and indexes to provide
      immediately available up-to-date results for various queries.

## Step 3. Create a view to find winning bids

A [view](/concepts/views/) is a saved name for the underlying `SELECT`
statement, providing an alias/shorthand when referencing the query. The
underlying query is not executed during the view creation; instead, the
underlying query is executed when the view is referenced.

Assume you want to find the winning bids for auctions that have ended. The
winning bid for an auction is the highest bid entered for an auction before the
auction ended. As new auction and bid data appears, the query must be rerun to
get up-to-date results.

1. Using the [`CREATE VIEW`](/sql/create-view/) command, create a
   [**view**](/concepts/views/ "Saved name/alias for a query") to find the
   winning (highest) bids.

   ```mzsql
   CREATE VIEW winning_bids AS
   SELECT DISTINCT ON (a.id) b.*, a.item, a.seller
   FROM auctions AS a
    JOIN bids AS b
      ON a.id = b.auction_id
   WHERE b.bid_time < a.end_time
     AND mz_now() >= a.end_time
   ORDER BY a.id,
     b.amount DESC,
     b.bid_time,
     b.buyer;
   ```

   Materialize provides an idiomatic way to perform [Top-K queries](/transform-data/idiomatic-materialize-sql/top-k/)
   using the [`DISTINCT ON`](/transform-data/idiomatic-materialize-sql/top-k/#for-k--1-1)
   clause. This clause is used to group by account `id` and return the first
   element within that group according to the specified ordering.

1. [`SELECT`](/sql/select/) from the view to execute the underlying query.
   For example:

   ```mzsql
   SELECT * FROM winning_bids
   ORDER BY bid_time DESC
   LIMIT 10;
   ```

   ```mzsql
   SELECT * FROM winning_bids
   WHERE item = 'Best Pizza in Town'
   ORDER BY bid_time DESC
   LIMIT 10;
   ```

   Since new data is continually being ingested, you must rerun the query to get
   the up-to-date results. Each time you query the view, you are re-running the
   underlying statement, which becomes less performant as the amount of data
   grows.

   In Materialize, to make the queries more performant even as data
   continues to grow, you can create [**indexes**](/concepts/indexes/) on views.
   Indexes provide always fresh view results in memory within a cluster by
   performing incremental updates as new data arrives. Queries can then read
   from the in-memory, already up-to-date results instead of re-running the
   underlying statement, making queries **computationally free and more
   performant**.

   In the next step, you will create an index on `winning_bids`.

## Step 4. Create an index to provide up-to-date results

Indexes in Materialize represents query results stored in memory within a
cluster. In Materialize, you can create [indexes](/concepts/indexes/) on views
to provide always fresh, up-to-date view results in memory within a cluster.
Queries can then read from the in-memory, already up-to-date results instead of
re-running the underlying statement.

To provide the up-to-date results, indexes **perform incremental updates** as
inputs change instead of recalculating the results from scratch. Additionally,
indexes can also help [optimize operations](/transform-data/optimization/) like
point lookups and joins.

1. Use the [`CREATE INDEX`](/sql/create-index/) command to create the following
   index on the `winning_bids` view.

    ```mzsql
    CREATE INDEX wins_by_item ON winning_bids (item);
    ```

   During the index creation, the underlying `winning_bids` query is executed,
   and the view results are stored in memory within the cluster. As new data
   arrives, the index **incrementally updates** the view results in memory.
   Because incremental work is performed on writes, reads from indexes return
   up-to-date results and are computationally **free**.

   This index can **also** help [optimize
   operations](/transform-data/optimization/) like point lookups and [delta
   joins](/transform-data/optimization/#optimize-multi-way-joins-with-delta-joins)
   on the index column(s) as well as support ad-hoc queries.

1. Rerun the previous queries on `winning_bids`.

    ```mzsql
    SELECT * FROM winning_bids
    ORDER BY bid_time DESC
    LIMIT 10;
    ```

    ```mzsql
    SELECT * FROM winning_bids
    WHERE item = 'Best Pizza in Town'
    ORDER BY bid_time DESC
    LIMIT 10;
    ```

   The queries should be faster since they use the in-memory, already up-to-date
   results computed by the index.

## Step 5. Create views and a table to find flippers in real time

For this quickstart, auction flipping activities are defined as when a user buys
an item in one auction and resells the same item at a higher price within an
8-day period. This step finds auction flippers in real time, based on
auction flipping activity data and known flippers data. Specifically, this step
creates:

- A view to find auction flipping activities. Results are updated as new data
  comes in (at 1 second intervals) from the data generator.

- A table that maintains known auction flippers. You will manually enter new
  data to this table.

- A view to immediately see auction flippers based on both the flipping
  activities view and the known auction flippers table.

1. Create a view to detect auction flipping activities.

    ```mzsql
    CREATE VIEW flip_activities AS
    SELECT w2.seller as flipper_id,
           w2.item AS item,
           w2.amount AS sold_amount,
           w1.amount AS purchased_amount,
           w2.amount - w1.amount AS diff_amount,
           datediff('days', w2.bid_time, w1.bid_time) AS timeframe_days
     FROM  winning_bids AS w1
       JOIN winning_bids AS w2
         ON w1.buyer = w2.seller   -- Buyer and seller are the same
            AND w1.item = w2.item  -- Item is the same
     WHERE w2.amount > w1.amount   -- But sold at a higher price
       AND datediff('days', w2.bid_time, w1.bid_time) < 8;
    ```

    The `flip_activities` view can use the index created on `winning_bids` view
    to provide up-to-date data.

    To view a sample row in `flip_activities`, run the following
    [`SELECT`](/sql/select) command:

    ```mzsql
    SELECT * FROM flip_activities LIMIT 10;
    ```

1. Use [`CREATE TABLE`](/sql/create-table) to create a `known_flippers` table
   that you can manually populate with known flippers. That is, assume that
   separate from your auction activities data, you receive independent data
   specifying users as flippers.

   ```mzsql
   CREATE TABLE known_flippers (flipper_id bigint);
   ```

1. Create a view `flippers` to flag known flipper accounts if a user has more
   than 2 flipping activities or the user is listed in the `known_flippers`
   table.

   ```mzsql
    CREATE VIEW flippers AS
    SELECT flipper_id
    FROM (
        SELECT flipper_id
        FROM flip_activities
        GROUP BY flipper_id
        HAVING count(*) >= 2

        UNION ALL

        SELECT flipper_id
        FROM known_flippers
    );
   ```

> **Note:** Both the `flip_activities` and `flippers` views can use the index created on
> `winning_bids` view to provide up-to-date data. Depending upon your query
> patterns and usage, an existing index may be sufficient, such as in this
> quickstart. In other use cases, creating an index only on the view(s) from which
> you will serve results may be preferred.

## Step 6. Subscribe to see results change

[`SUBSCRIBE`](/sql/subscribe/) to `flippers` to see new flippers appear as new
data arrives (either from the known_flippers table or the flip_activities view).

1. Use [`SUBSCRIBE`](/sql/subscribe/) command to see flippers
   as new data arrives (either from the `known_flippers` table or the
   `flip_activities` view). [`SUBSCRIBE`](/sql/subscribe/) returns data from a
   source, table, view, or materialized view as they occur, in this case, the
   view `flippers`.

   ```mzsql
   SUBSCRIBE TO (
      SELECT *
      FROM flippers
   ) WITH (snapshot = false)
   ;
   ```

   The optional [`WITH (snapshot = false)`
   option](/sql/subscribe/#with-options) indicates that the command displays
   only the new flippers that come in after the start of the `SUBSCRIBE`
   operation, and not the flippers in the view at the start of the operation.

1. In the Materialize Console quickstart page, enter an id (for example `450`)
   into the text input field to insert a new user into the `known-flippers`
   table. You can specify any number for the flipper id.

   The flipper should immediately appear in the `SUBSCRIBE` results.

   You should also see flippers who are flagged by their flip activities.
   Because of the randomness of the auction data being generated, user
   activity data that match the definition of a flipper may take some time
   even though auction data is constantly being ingested. However, once
   new matching data comes in, you will see it immediately in the `SUBSCRIBE`
   results. While waiting, you can enter additional flippers into the
   `known_flippers` table.

1. To cancel out of the `SUBSCRIBE`, click the **Stop streaming** button.

## Step 7. Create views to verify that Materialize returns consistent data

To verify that Materialize serves **consistent results**, even as new
data comes in, this step creates the following views for completed auctions:

- A view to keep track of each seller's credits.

- A view to keep track of each buyer's debits.

- A view that sums all sellers' credits, all buyers' debits, and calculates the
  difference, which should be `0`.

1. Create a view to track credited amounts for sellers of completed auctions.

    ```mzsql
    CREATE VIEW seller_credits AS
    SELECT seller, SUM(amount) as credits
    FROM winning_bids
    GROUP BY seller;
    ```

1. Create a view to track  debited amounts for the winning bidders of completed
   auctions.

    ```mzsql
    CREATE VIEW buyer_debits AS
    SELECT buyer, SUM(amount) as debits
    FROM winning_bids
    GROUP BY buyer;
    ```

1. To verify that the total credit and total debit amounts equal for completed
   auctions (i.e., to verify that the results are correct and consistent even as
   new data comes in), create a `funds_movement` view that calculates the total
   credits across sellers, total debits across buyers, and the difference
   between the two.

    ```mzsql
    CREATE VIEW funds_movement AS
    SELECT SUM(credits) AS total_credits,
           SUM(debits) AS total_debits,
           SUM(credits) - SUM(debits) AS total_difference
    FROM (
      SELECT SUM(credits) AS credits, 0 AS debits
      FROM seller_credits

      UNION

      SELECT 0 AS credits, SUM(debits) AS debits
      FROM buyer_debits
    );

    ```

   To see that the sums always equal even as new data comes in, you can
   `SUBSCRIBE` to this query:

   ```mzsql
   SUBSCRIBE TO (
      SELECT *
      FROM funds_movement
   );
   ```

   Toggle `Show diffs` to see changes to `funds_movement`.

   - As new data comes in and auctions complete, the `total_credits` and
     `total_debits` values should change but the `total_difference` should
     remain `0`.
   - To cancel out of the `SUBSCRIBE`, click the **Stop streaming** button.

## Step 8. Clean up

To clean up the quickstart environment:

1. Use the [`DROP SOURCE ... CASCADE`](/sql/drop-source/) command to drop
   `auction_house` source and its dependent objects, including views and indexes
   created on the `auction_house` subsources.

   ```mzsql
   DROP SOURCE auction_house CASCADE;
   ```

1. Use the [`DROP TABLE`](/sql/drop-table) command to drop the separate
   `known_flippers` table.

   ```mzsql
   DROP TABLE known_flippers;
   ```

## Summary

In Materialize, [indexes](/concepts/indexes/) represent query results stored in
memory within a cluster. When you create an index on a view, the index
incrementally updates the view results (instead of recalculating the results
from scratch) as Materialize ingests new data. These up-to-date results are then
immediately available and computationally free for reads within the cluster.

### General guidelines

This quickstart created an index on a view to maintain in-memory up-to-date
results in the cluster. In Materialize, both materialized views and indexes on
views incrementally update the view results. Materialized views persist the
query results in durable storage and is available across clusters while indexes
maintain the view results in memory within a single cluster.

<p>Some general guidelines for usage patterns include:</p>
<table>
  <thead>
      <tr>
          <th>Usage Pattern</th>
          <th>General Guideline</th>
      </tr>
  </thead>
  <tbody>
      <tr>
          <td>View results are accessed from a single cluster only;<br>such as in a 1-cluster or a 2-cluster architecture.</td>
          <td>View with an <a href="/sql/create-index" >index</a></td>
      </tr>
      <tr>
          <td>View used as a building block for stacked views; i.e., views not used to serve results.</td>
          <td>View</td>
      </tr>
      <tr>
          <td>View results are accessed across <a href="/concepts/clusters" >clusters</a>;<br>such as in a 3-cluster architecture.</td>
          <td>Materialized view (in the transform cluster)<br>Index on the materialized view (in the serving cluster)</td>
      </tr>
      <tr>
          <td>Use with a <a href="/serve-results/sink/" >sink</a> or a <a href="/sql/subscribe" ><code>SUBSCRIBE</code></a> operation</td>
          <td>Materialized view</td>
      </tr>
      <tr>
          <td>Use with <a href="/transform-data/patterns/temporal-filters/" >temporal filters</a></td>
          <td>Materialized view</td>
      </tr>
  </tbody>
</table>

The quickstart used an index since:

- The examples did not need to store the results in durable storage.

- All activities were limited to the single `quickstart` cluster.

- Although used, `SUBSCRIBE` operations were for illustrative/validation
  purposes and were not the final consumer of the views.

### Best practices

Before creating an index (which represents query results stored in memory),
consider its memory usage as well as its [compute cost
implications](/administration/billing/#compute). For best practices when
creating indexes, see [Index Best Practices](/concepts/indexes/#best-practices).

### Additional information

- [Clusters](/concepts/clusters)
- [Indexes](/concepts/indexes)
- [Sources](/concepts/sources)
- [Views](/concepts/views/)
- [Idiomatic Materialize SQL
  chart](/transform-data/idiomatic-materialize-sql/appendix/idiomatic-sql-chart/)
- [Usage & Billing](/administration/billing/#compute)
- [`CREATE INDEX`](/sql/create-index/)
- [`CREATE SCHEMA`](/sql/create-schema/)
- [`CREATE SOURCE`](/sql/create-source/)
- [`CREATE TABLE`](/sql/create-table)
- [`CREATE VIEW`](/sql/create-view/)
- [`DROP VIEW`](/sql/drop-view)
- [`DROP SOURCE`](/sql/drop-source/)
- [`DROP TABLE`](/sql/drop-table)
- [`SELECT`](/sql/select)
- [`SUBSCRIBE`](/sql/subscribe/)

## Next steps

[//]: # "TODO(morsapaes) Extend to suggest third party tools. dbt, Census and Metabase could all fit here to do interesting things as a follow-up."

To get started ingesting your own data from an external system like Kafka, MySQL
or PostgreSQL, check the documentation for [sources](/sql/create-source/), and
navigate to **Data** > **Sources** > **New source** in the [Materialize Console](/console/)
to create your first source.

For help getting started with your data or other questions about Materialize,
you can schedule a [free guided
trial](https://materialize.com/demo/?utm_campaign=General&utm_source=documentation).

