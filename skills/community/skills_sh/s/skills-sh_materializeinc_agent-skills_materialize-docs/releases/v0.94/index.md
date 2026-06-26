# Materialize v0.94
## v0.94

#### Sources and sinks

* Set subsources into an errored state in the [PostgreSQL source](/sql/create-source/postgres/)
  if the corresponding table is dropped from the publication upstream.

* Add a `KEY VALUE` load generator source,
  which produces keyed data that can be passed through to [`ENVELOPE UPSERT`](/sql/create-source/kafka/).
  This is useful for internal testing.
