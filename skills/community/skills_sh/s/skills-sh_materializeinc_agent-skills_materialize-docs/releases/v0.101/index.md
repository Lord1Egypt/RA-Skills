# Materialize v0.101
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
