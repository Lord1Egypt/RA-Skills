# Lighthouse Instance Management

## Query Instances

```bash
# List all Lighthouse instances in a region
tccli lighthouse DescribeInstances --region ap-guangzhou

# Query a specific instance
tccli lighthouse DescribeInstances --region ap-guangzhou \
  --InstanceIds '["lhins-xxxxxxxx"]'

# Query instance login URL
tccli lighthouse DescribeInstanceLoginUrl --region ap-guangzhou \
  --InstanceId lhins-xxxxxxxx
```

## Start / Stop / Reboot

All operations require user confirmation before execution.

```bash
# Start instance
tccli lighthouse StartInstances --region ap-guangzhou \
  --InstanceIds '["lhins-xxxxxxxx"]'

# Reboot instance
tccli lighthouse RebootInstances --region ap-guangzhou \
  --InstanceIds '["lhins-xxxxxxxx"]'

# Stop instance
tccli lighthouse StopInstances --region ap-guangzhou \
  --InstanceIds '["lhins-xxxxxxxx"]'
```

## Reset Instance Password

```bash
tccli lighthouse ResetInstance --region ap-guangzhou \
  --InstanceId lhins-xxxxxxxx \
  --LoginConfiguration '{"Password":"NewPassword123!"}'
```

> Password must meet complexity requirements: 8-30 characters, containing uppercase, lowercase, digits, and special characters.

## Create a New Instance

When user asks to "create" / "deploy" / "set up" a Lighthouse instance, create a NEW instance by default.

```bash
# Step 1: List available bundles (instance plans)
tccli lighthouse DescribeBundles --region ap-guangzhou

# Step 2: List available blueprints (OS images)
tccli lighthouse DescribeBlueprints --region ap-guangzhou

# Step 3: Create the instance
tccli lighthouse CreateInstances --region ap-guangzhou \
  --BundleId bundle_xxxx \
  --BlueprintId lhbp_xxxx \
  --InstanceName "my-instance"
```

> Run `tccli lighthouse CreateInstances --help` to check all available parameters (BundleId, BlueprintId, InstanceName, etc.).

### Common Blueprints

| BlueprintId | Description |
|-------------|-------------|
| lhbp-ubuntu20 | Ubuntu 20.04 |
| lhbp-centos7 | CentOS 7.9 |
| lhbp-docker | Docker |
| lhbp-wordpress | WordPress |

Use `DescribeBlueprints` to get the full list and exact IDs.

## Blueprints (Images)

```bash
# List all available blueprints
tccli lighthouse DescribeBlueprints --region ap-guangzhou

# List available bundles (instance plans)
tccli lighthouse DescribeBundles --region ap-guangzhou
```

## Workflow

1. Always run `DescribeInstances` first to get the actual InstanceId
2. Confirm the instance status before performing start/stop/reboot
3. For password reset, warn the user that the instance will be restarted