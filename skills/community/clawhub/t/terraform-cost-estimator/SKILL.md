---
name: terraform-cost-estimator
description: Estimate infrastructure costs from Terraform plans — analyze resource changes, predict monthly spend, compare alternatives, and identify cost optimization opportunities.
metadata:
  tags: ["terraform", "cost", "cloud", "finops", "infrastructure"]
---

# Terraform Cost Estimator

Estimate infrastructure costs from Terraform plans before applying. Analyze planned resource changes, predict monthly spend impact, compare pricing alternatives, and identify cost optimization opportunities. Works with AWS, GCP, and Azure resources.

## Usage

```
"Estimate the cost of this Terraform plan"
"How much will this infrastructure change cost?"
"Compare cost of different instance types for my Terraform config"
"Find cost optimization in my Terraform modules"
```

## How It Works

### 1. Plan Analysis

```bash
terraform plan -out=plan.tfplan 2>/dev/null
terraform show -json plan.tfplan 2>/dev/null | python3 -c "
import json, sys
plan = json.load(sys.stdin)
changes = plan.get('resource_changes', [])
for c in changes:
    action = c['change']['actions']
    print(f'{\" \".join(action):12s} {c[\"type\"]:40s} {c[\"address\"]}')
"
```

### 2. Resource Pricing

Map each resource to estimated monthly cost:

**Compute:**
- EC2/GCE/Azure VM: instance type → hourly rate × 730 hours
- Lambda/Cloud Functions: estimated invocations × duration × memory
- ECS/EKS/GKE: task/pod resources × cluster overhead
- App Runner/Cloud Run: vCPU-seconds + memory-seconds

**Storage:**
- S3/GCS/Blob: storage class × GB + request costs
- EBS/Persistent Disk: volume type × size × IOPS
- RDS/Cloud SQL: instance + storage + backup + I/O

**Network:**
- NAT Gateway: hourly + data processing
- Load Balancer: hourly + LCU/data
- Data transfer: inter-region, internet egress
- VPN/Direct Connect: hourly + data

### 3. Cost Impact Report

For each planned change, show:
- Current monthly cost (if modifying existing resource)
- New monthly cost
- Delta (increase/decrease)
- Annual projection

### 4. Optimization Suggestions

- Compute: rightsizing, Reserved Instances, Savings Plans, Spot
- Storage: lifecycle policies, intelligent tiering
- Network: VPC endpoints instead of NAT, regional vs cross-region
- Database: reserved capacity, serverless options
- Unused: resources created but potentially idle

## Output

```
## Terraform Cost Estimate

**Provider:** AWS (us-east-1)
**Resources:** 12 planned changes

### Cost Breakdown
| Resource | Type | Action | Monthly Cost |
|----------|------|--------|-------------|
| web-server | aws_instance (t3.large) | create | $60.74 |
| db-primary | aws_db_instance (db.r6g.xl) | create | $345.60 |
| db-replica | aws_db_instance (db.r6g.large) | create | $172.80 |
| cache | aws_elasticache (r6g.large) | create | $131.40 |
| alb | aws_lb | create | $22.27 |
| nat | aws_nat_gateway | create | $32.40 |
| s3-assets | aws_s3_bucket (100GB est) | create | $2.30 |
| **Total** | | | **$767.51/mo** |

### 💰 Optimization Opportunities
1. NAT Gateway → VPC endpoints: save $25/mo
2. db.r6g.xlarge → db.r6g.large + read replica: save $50/mo if read-heavy
3. Consider Reserved Instances: save 30-40% (~$230/mo)
4. S3 Intelligent-Tiering: save 20-40% on infrequent access

### Annual Projection
- On-Demand: $9,210/yr
- With Reserved (1yr): $6,447/yr (30% savings)
- With Reserved (3yr): $5,526/yr (40% savings)
```
