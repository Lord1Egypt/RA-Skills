# Materialize v0.85
## v0.85

#### SQL

* Add [`mz_internal.mz_recent_activity_log`](/reference/system-catalog/mz_internal/#mz_recent_activity_log)
  to the system catalog. This view contains a log of the SQL statements that have
  been issued to Materialize in the past 3 days, along with various metadata
  about them. Querying this view is typically much faster than querying
  `mz_internal.mz_activity_log`.

#### Bug fixes and other improvements

* Fix a bug where [`DISCARD ALL`](/sql/discard/) did not consider system or role
  defaults ([#24601](https://github.com/MaterializeInc/materialize/issues/24601)).

* Fix a bug causing the `mz_monitor` and `mz_monitor_redacted` system roles to
  not show up in the `mz_roles` system catalog table ([#24617](https://github.com/MaterializeInc/materialize/issues/24617)).
