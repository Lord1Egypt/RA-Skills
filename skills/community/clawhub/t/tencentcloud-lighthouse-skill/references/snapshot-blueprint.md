# Lighthouse Snapshots and Blueprints

## Snapshots

### Create a Snapshot

```bash
tccli lighthouse CreateInstanceSnapshot --region ap-guangzhou \
  --InstanceId lhins-xxxxxxxx \
  --SnapshotName "backup-before-upgrade"
```

### Query Snapshots

```bash
tccli lighthouse DescribeSnapshots --region ap-guangzhou \
  --Filters '[{"Name":"instance-id","Values":["lhins-xxxxxxxx"]}]'
```

### Apply a Snapshot (Restore)

```bash
tccli lighthouse ApplyInstanceSnapshot --region ap-guangzhou \
  --InstanceId lhins-xxxxxxxx \
  --SnapshotId snap-xxxxxxxx
```

> Applying a snapshot will overwrite the current system disk data. The instance will be restarted. Always confirm with the user before executing.

### Delete a Snapshot

```bash
tccli lighthouse DeleteSnapshots --region ap-guangzhou \
  --SnapshotIds '["snap-xxxxxxxx"]'
```

## Custom Blueprints (Images)

### Create a Blueprint from Instance

```bash
tccli lighthouse CreateBlueprint --region ap-guangzhou \
  --BlueprintName "my-custom-image" \
  --InstanceId lhins-xxxxxxxx \
  --Description "Custom image created from instance"
```

### List Blueprints

```bash
# All blueprints (system + custom)
tccli lighthouse DescribeBlueprints --region ap-guangzhou

# Custom blueprints only
tccli lighthouse DescribeBlueprints --region ap-guangzhou \
  --Filters '[{"Name":"blueprint-type","Values":["CUSTOM_IMAGE"]}]'
```

### Delete a Custom Blueprint

```bash
tccli lighthouse DeleteBlueprints --region ap-guangzhou \
  --BlueprintIds '["lhbp-xxxxxxxx"]'
```

## Workflow

1. Before any risky operation, create a snapshot as backup
2. Use `DescribeSnapshots` to verify the snapshot was created successfully
3. Custom blueprints can be used to create new instances with the same configuration
4. Snapshot and blueprint creation may take several minutes — check status before proceeding