# Materialize v0.90
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
