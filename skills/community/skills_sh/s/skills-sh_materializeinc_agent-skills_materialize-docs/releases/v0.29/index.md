# Materialize v0.29
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
