# Tencent Cloud Platform

Use this file when the request is really about Tencent Cloud, not Tencent broadly.

## Map The Workload First

| Workload | Tencent Cloud direction | Notes to call out |
|----------|-------------------------|-------------------|
| VM-based application | CVM plus VPC and CLB | Check region, image support, and ops ownership |
| Container platform | TKE or Serverless workloads | Confirm operational maturity and observability needs |
| Object storage | COS | Separate public delivery, archive, and private data patterns |
| Relational database | CDB or compatible managed database | Check region support, backups, and migration tooling |
| CDN and acceleration | Tencent Cloud CDN and edge services | Verify target markets and origin design |
| Media pipeline | MPS and adjacent media services | Region support and cost model vary materially |
| Messaging and queueing | Native Tencent Cloud messaging services | Compare managed simplicity vs portability |

## AWS Analogy Trap

Do not say "Tencent Cloud is basically AWS with different names."

Use analogies only as orientation:
- CVM is closer to EC2-style compute
- COS is an object-storage surface
- TKE is a managed Kubernetes direction

Then immediately explain the Tencent-specific differences:
- region availability
- account and IAM shape
- managed-service maturity
- documentation language gaps
- console and operational workflows

## Region-Sensitive Questions

Ask these before naming architecture:
- Does data need to stay in mainland China?
- Is cross-border latency acceptable?
- Does the team need mainland-only products?
- Who will operate the environment after launch?

## Operational Minimums

Every Tencent Cloud recommendation should include:
- target region
- network boundary
- logging and monitoring plan
- backup and rollback plan
- cost and quota caveats

If those are unknown, stop at planning and produce a gap list instead of pretending the architecture is ready.
