# Materialize v0.100
## v0.100

#### SQL

* Add a [`MAP` expression](/sql/types/map/#construction) that allows constructing a `map`
  from a list of key–value pairs or a subquery.

  ```mzsql
  SELECT MAP['a' => 1, 'b' => 2];

       map
  -------------
   {a=>1,b=>2}
  ```

#### Bug fixes and other improvements

* Support the [`COPY TO`](/sql/copy-to/) command in the WebSocket API, so it's
  possible to run it from the SQL Shell.
