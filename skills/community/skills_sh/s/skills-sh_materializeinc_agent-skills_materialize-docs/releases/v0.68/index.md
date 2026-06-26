# Materialize v0.68
## v0.68.0

[//]: # "NOTE(morsapaes) v0.68 includes a first version of the COMMENT ON syntax
released behind a feature flag."

#### SQL

* Enable Role-based access control (RBAC) for all new environments. Check the
  [updated documentation](/security/access-control/) for guidance on setting up
  RBAC in your Materialize organization.

* Extend the [`EXPLAIN PLAN`](/sql/explain-plan/) syntax to allow explaining
  plans used for index maintenance.

#### Bug fixes and other improvements

* Extend `pg_catalog` and `information_schema` system catalog coverage for
  compatibility with Power BI.
