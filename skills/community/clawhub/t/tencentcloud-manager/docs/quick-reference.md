# Tencent Cloud Resource Management - Quick Reference

---

## Quick Start

### 1. Install Dependencies

```bash
pip3 install --break-system-packages \
  tencentcloud-sdk-python \
  cos-python-sdk-v5 \
  python-dotenv
```

### 2. Configure Credentials

```bash
cp skills/tencentcloud-manager/config/.env.example \
   skills/tencentcloud-manager/config/.env
```

Edit `.env` file and fill in SecretId and SecretKey.

### 3. Verify Configuration

```bash
cd skills/tencentcloud-manager/src
python3 tencentcloud_manager.py verify
```

---

## Common Commands

### Query Promotions

```python
from tencentcloud_manager import TencentCloudManager
tcm = TencentCloudManager()

tcm.show_promotions(service='lighthouse')
tcm.show_promotions(service='cvm')
```

### Create Resources

```python
# Create Lighthouse instance
instance = tcm.create_resource(
    service='lighthouse',
    plan_id='new-2c4g',
    blueprint_id='bp-ubuntu-2204',
    instance_name='my-server'
)

# Create COS bucket
bucket = tcm.create_resource(
    service='cos',
    bucket_name='my-bucket',
    storage_class='STANDARD'
)
```

### Manage Instances

```python
# List all instances
instances = tcm.list_all_instances()

# Query instance status
status = tcm.get_resource_status('lighthouse', instance_id)

# Start/Stop/Restart
tcm.start_resource('lighthouse', instance_id)
tcm.stop_resource('lighthouse', instance_id)
tcm.restart_resource('lighthouse', instance_id)
```

### COS Operations

```python
# Upload file
tcm.upload_to_cos(
    bucket='bucket.cos.ap-singapore.myqcloud.com',
    local_path='/tmp/file.txt',
    key='path/file.txt'
)

# Set lifecycle
tcm.set_cos_lifecycle('bucket', [
    {
        'id': 'rule1',
        'prefix': 'data/',
        'transitions': [
            {'days': 7, 'storage_class': 'STANDARD_IA'},
            {'days': 30, 'storage_class': 'ARCHIVE'}
        ]
    }
])
```

---

## Promotion Plans

### Lighthouse New User Special

| Plan ID | Config | Price | Use Case |
|---------|--------|-------|----------|
| new-1c1g | 1 vCPU 1GB/30GB/30M | ¥60/year | Personal blog |
| new-2c2g | 2 vCPU 2GB/50GB/30M | ¥95/year | Small website |
| new-2c4g | 2 vCPU 4GB/60GB/30M | ¥168/year | Data collection |
| new-4c8g | 4 vCPU 8GB/80GB/30M | ¥338/year | Large application |

### CVM Pay-As-You-Go

| Plan ID | Config | Monthly Cost | Use Case |
|---------|--------|--------------|----------|
| payg-2c2g | 2 vCPU 2GB | ~¥86/month | Test environment |
| payg-2c4g | 2 vCPU 4GB | ~¥130/month | Development environment |
| payg-4c8g | 4 vCPU 8GB | ~¥259/month | Production environment |

---

## Documentation

- [Skill Description](../SKILL.md)
- [Permission Config](permission-policy.md)
