---
name: vultr
description: Manage Vultr cloud infrastructure including VPS instances, bare metal, Kubernetes clusters, databases, DNS, firewalls, VPCs, object storage, and more. Use when asked to deploy, manage, list, or modify Vultr resources. Handles instances, bare-metal, kubernetes, databases, load-balancers, dns, firewall, vpc, snapshots, ssh-keys, block-storage, object-storage, reserved-ips, and billing.
---

---
name: vultr
version: 1.3.0
description: Manage Vultr cloud infrastructure including VPS instances, bare metal, Kubernetes clusters, databases, DNS, firewalls, VPCs, object storage, and more. Use when asked to deploy, manage, list, or modify Vultr resources.
author: Erwin Evans
tags:
  - vultr
  - cloud
  - infrastructure
  - kubernetes
  - vps
---

# Vultr Cloud Infrastructure Management

Manage Vultr cloud resources via the Vultr API v2.

## Setup

Store your API key in `~/.config/vultr/api_key`:

```bash
mkdir -p ~/.config/vultr
echo -n "YOUR_API_KEY" > ~/.config/vultr/api_key
chmod 600 ~/.config/vultr/api_key
```

Generate API keys at: https://my.vultr.com/settings/#settingsapi

## Usage

```bash
python3 scripts/vultr.py <resource> <action> [options]
```

## Quick Reference

### Account
```bash
vultr.py account get              # Account info, balance
vultr.py account bgp              # BGP configuration
vultr.py account bandwidth        # Bandwidth usage
```

### Instances (VPS)
```bash
vultr.py instances list                                    # List all instances
vultr.py instances get --id abc123                         # Get instance details
vultr.py instances create --region ewr --plan vc2-1c-1gb --os 174   # Create instance
vultr.py instances start --id abc123                       # Start instance
vultr.py instances stop --id abc123                        # Stop instance
vultr.py instances reboot --id abc123                      # Reboot instance
vultr.py instances delete --id abc123                      # Delete instance
```

### Bare Metal
```bash
vultr.py bare-metal list                                   # List bare metal
vultr.py bare-metal create --region ewr --plan vbm-4c-32gb --os 174
```

### Kubernetes (VKE)
```bash
vultr.py kubernetes list                                   # List clusters
vultr.py kubernetes create --region ewr --version v1.28 --label my-cluster
vultr.py kubernetes kubeconfig --id abc123                 # Get kubeconfig
vultr.py kubernetes versions                               # Available versions
```

### Databases
```bash
vultr.py databases plans                                   # List plans
vultr.py databases list                                    # List databases
vultr.py databases create --region ewr --type pg --plan <plan>
```

### DNS
```bash
vultr.py dns list                                          # List domains
vultr.py dns create --domain example.com --ip 192.0.2.1   # Create domain
vultr.py dns records --domain example.com                  # List records
vultr.py dns create-record --domain example.com --record-type A --record-name www --record-data 192.0.2.1
```

### Firewall
```bash
vultr.py firewall list                                     # List groups
vultr.py firewall create --description "Web servers"
vultr.py firewall rules --id abc123                        # List rules
vultr.py firewall create-rule --id abc123 --ip-type v4 --protocol tcp --port 22 --subnet 10.0.0.0/8
```

### VPC
```bash
vultr.py vpc list                                          # List VPCs
vultr.py vpc create --region ewr --description "Private network" --subnet 10.0.0.0/24
```

### Snapshots
```bash
vultr.py snapshots list                                    # List snapshots
vultr.py snapshots create --instance-id abc123 --description "Backup"
```

### SSH Keys
```bash
vultr.py ssh-keys list                                     # List keys
vultr.py ssh-keys create --name "my-key" --key "ssh-rsa AAAA..."
```

### Regions & Plans
```bash
vultr.py regions list                                      # List regions
vultr.py plans list                                        # List VPS plans
vultr.py plans bare-metal                                  # Bare metal plans
```

### Block Storage
```bash
vultr.py block-storage list                                # List volumes
vultr.py block-storage create --region ewr --size 100 --label "data"
vultr.py block-storage attach --id abc123 --instance xyz789
```

### Object Storage
```bash
vultr.py object-storage clusters                           # List clusters
vultr.py object-storage create --cluster abc123 --label "my-bucket"
```

### Reserved IPs
```bash
vultr.py reserved-ips list                                 # List reserved IPs
vultr.py reserved-ips create --region ewr --ip-type v4 --label "frontend"
```

### Billing
```bash
vultr.py billing history                                   # Billing history
vultr.py billing invoices                                  # List invoices
vultr.py billing pending-charges                           # Current charges
```

## Common Workflows

### Deploy a Web Server
```bash
# 1. Get available regions and plans
vultr.py regions list
vultr.py plans list

# 2. Create instance with Ubuntu 24.04
vultr.py instances create \
  --region ewr \
  --plan vc2-2c-4gb \
  --os 174 \
  --label "web-server" \
  --hostname "web01" \
  --ipv6 \
  --ssh-keys ssh-key-id

# 3. Configure firewall
vultr.py firewall create --description "Web servers"
vultr.py firewall create-rule --id fw-id --ip-type v4 --protocol tcp --port 22 --subnet your-ip/32
vultr.py firewall create-rule --id fw-id --ip-type v4 --protocol tcp --port 80
vultr.py firewall create-rule --id fw-id --ip-type v4 --protocol tcp --port 443
```

### Create a Kubernetes Cluster
```bash
# 1. Get available versions
vultr.py kubernetes versions

# 2. Create cluster
vultr.py kubernetes create \
  --region ewr \
  --version v1.28.0 \
  --label "prod-cluster"

# 3. Get kubeconfig
vultr.py kubernetes kubeconfig --id cluster-id > kubeconfig
```

### Set Up Managed Database
```bash
# 1. List plans
vultr.py databases plans

# 2. Create PostgreSQL database
vultr.py databases create \
  --region ewr \
  --type pg \
  --plan vdb-1-4-2 \
  --label "prod-db"
```

## Full API Reference

See [references/api-reference.md](references/api-reference.md) for complete endpoint documentation.

## Response Format

All commands return JSON. Successful responses include the resource data. Errors include an `error` field with details.

Example success:
```json
{
  "instance": {
    "id": "abc123",
    "label": "web-server",
    "region": "ewr",
    "status": "active",
    "main_ip": "192.0.2.1"
  }
}
```

Example error:
```json
{
  "error": "Invalid API key",
  "status": 401
}
```
