# Materialize v0.88
## v0.88

#### SQL

* Allow `LIMIT` expressions to contain parameters.

	```mzsql
	  PREPARE foo AS SELECT generate_series(1, 10) LIMIT $1;
	  EXECUTE foo (7::bigint);

	  generate_series
	  -----------------
	                 1
	                 2
	                 3
	                 4
	                 5
	                 6
	                 7
	```

#### Bug fixes and other improvements

* Fix a bug that potentially prevented timestamp with timezone data from being
  correctly parsed when ingested through PostgreSQL sources ([#25216](https://github.com/MaterializeInc/materialize/issues/25216)).

* Fix float parsing of certain zero values, such as `0.` and `.0` ([#25141](https://github.com/MaterializeInc/materialize/issues/25141)).

* Fix multiple bugs related to interval rounding ([#25202](https://github.com/MaterializeInc/materialize/issues/25202)).
