# Sources
Learn about sources in Materialize.
## Overview

A source in Materialize represents an external data source. More concretely, it
specifies the connection and the ingestion configuration to use for a particular
external data source (e.g., PostgreSQL, Kafka). For those familiar with
PostgreSQL's foreign servers and foreign tables, a source is like a foreign
server, and the tables (or subsources) created from the source are like foreign
tables.

Before creating a source in Materialize, you must ensure that the external data
source is properly configured and accessible so that Materialize can establish a
connection and ingest its data. The exact configuration depends on the type of
data source.

### Connectors

Materialize bundles native connectors for the following external systems:

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

## Sources and clusters

Sources require compute resources in Materialize, and so need to be associated
with a [cluster](/concepts/clusters/). If possible, dedicate a cluster just for
sources.

See also [Operational guidelines](/manage/operational-guidelines/).

## Related pages

- [`CREATE SOURCE`](/sql/create-source)
