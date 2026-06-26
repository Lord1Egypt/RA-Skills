# Materialize v0.70
## v0.70.0

#### Sources and sinks

* Automatically check if there are tables not currently configured to use `REPLICA IDENTITY FULL` in a publication used with a [PostgreSQL source](/sql/create-source/postgres/).

* Support constraining the precision of the fractional seconds in timestamps. This allows users to construct Avro-formatted sinks that use the `timestamp-millis` logical type instead of the `timestamp-micros` logical type.

#### Bug fixes and other improvements

* Limit the amount of data that can be copied using `COPY FROM` to 1 GiB. Please [contact us](https://materialize.com/contact/) if you need this limit increased in your Materialize region.

* Restrict transactions to execute on a single cluster, in order to improve use case isolation. The first query in a transaction now determines the time domain of the entire transaction ([#21854](https://github.com/MaterializeInc/materialize/issues/21854)).
