# Debezium
How to propagate Change Data Capture (CDC) data from a database to Materialize using Debezium
For databases that are not natively supported, like Oracle or MongoDB, you can
use [Debezium](https://debezium.io/) to propagate Change Data Capture (CDC) data
to Materialize.

| Database   | Natively supported? | Integration guide                                                                              |
|------------|---------------------| ---------------------------------------------------------------------------------------------- |
| Oracle     |                     | [Kafka + Debezium](https://debezium.io/documentation/reference/stable/connectors/oracle.html)  |
| MongoDB    |                     | [Kafka + Debezium](/ingest-data/mongodb/) |

Debezium captures row-level changes resulting from `INSERT`, `UPDATE`, and
`DELETE` operations in the upstream database and publishes them as events to
Kafka (and other Kafka API-compatible brokers) using Kafka Connect-compatible
connectors.

<div class="note">
  <strong class="gutter">NOTE:</strong> Currently, Materialize only supports Avro-encoded Debezium records. If you're interested in JSON support, please reach out in the community Slack or submit a <a href="https://github.com/MaterializeInc/materialize/discussions/new?category=feature-requests">feature request</a>.
</div>

For more details on CDC support in Materialize, check the
[Kafka source](/sql/create-source/kafka/#debezium-envelope) reference
documentation.
