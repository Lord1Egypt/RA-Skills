# Materialize v0.66
## v0.66.0

This release focuses on stabilization work and performance improvements. It does
not introduce any new user-facing features. 👷

#### Bug fixes and other improvements

* Fix a bug that prevented [`ALTER SOURCE...`](/sql/alter-source/) from
  completing in PostgreSQL sources when existing tables were listed in a
  publication in a different order than that observed when Materialize first
  processed them.
