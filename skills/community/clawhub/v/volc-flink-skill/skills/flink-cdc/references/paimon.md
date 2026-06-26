# Paimon sink notes

## Supported forms

- Filesystem catalog sink: `type: paimon`
- LAS / Hive metastore aligned sink (repo convention): `type: paimon-las`

## Filesystem catalog

Typical options:

- `catalog.properties.metastore: filesystem`
- `catalog.properties.warehouse`
- `commit.user`
- `partition.key`
- `catalog.properties.*`
- `table.properties.*`

## LAS catalog alignment

For LAS catalog, align with the existing Flink SQL Paimon LAS parameter style in this repo:

```yaml
sink:
  type: paimon-las
  name: Paimon LAS Sink
  commit.user: ${paimon_las_commit_user}
  catalog.properties.metastore: hive
  catalog.properties.hive.hms.client.is.public.cloud: true
  catalog.properties.hive.client.las.region.name: ${paimon_las_catalog_properties_region}
  catalog.properties.hive.metastore.uris: ${paimon_las_catalog_properties_uris}
  catalog.properties.hive.client.las.ak: ${paimon_las_catalog_properties_ak}
  catalog.properties.hive.client.las.sk: ${paimon_las_catalog_properties_sk}
  catalog.properties.metastore.catalog.default: ${paimon_las_catalog_properties_las_catalog}
  catalog.properties.warehouse: ${paimon_las_catalog_properties_warehouse}
```

## Notes

- Paimon pipeline sink only supports primary-key source tables
- The connector currently does not support exactly-once; it relies on at-least-once + primary-key idempotence
- Use `catalog.properties.*` to pass catalog options
- Use `table.properties.*` to pass table options

