# RAM Policies for qwencloud-deploy

Deployment creates cloud resources (ECS/EIP/VPC/SG via ROS, an OSS bucket for artifacts), so it
needs write permissions. The same credential is reused for hot updates and cleanup. The optional
**Domain & HTTPS** flow additionally needs domain-registration and AliDNS permissions.

## Core deployment

| Action | Purpose |
|--------|---------|
| `sts:GetCallerIdentity` | Identity probe during env check |
| `ecs:DescribeAvailableResource` | Fetch live in-stock types and zones for the region |
| `ecs:DescribeInstanceTypes` | Fill in vCPU / memory for each type |
| `ecs:RunCommand` | Send bootstrap / health-check / hot-update commands |
| `ecs:DescribeInvocations` | Read Cloud Assistant command status |
| `ecs:DescribeInvocationResults` | Read Cloud Assistant command output |
| `rds:DescribeAvailableClasses` | Validate the RDS class in the zone (when RDS is needed) |
| `ros:ValidateTemplate` | Validate the template before creating the stack |
| `ros:GetTemplateEstimateCost` | Cost estimate |
| `ros:CreateStack` | Create the full stack |
| `ros:GetStack` | Poll stack status |
| `ros:ListStacks` | Existing-deployment scan |
| `ros:ListStackResources` | Locate ECS/RDS/EIP physical resources in the stack |
| `ros:DeleteStack` | Clean up the stack |
| `oss:PutObject` / `oss:GetObject` / `oss:ListObjects` | Upload and verify artifacts |
| `oss:PutBucket` / `oss:DeleteBucket` / `oss:GetBucketInfo` | Create and clean up the temporary bucket |

ROS creates the ECS, EIP, VPC, and SecurityGroup (and optional RDS MySQL) tagged `from=qwencloud`;
the credential needs the corresponding `ecs:*` / `vpc:*` / `rds:*` create/delete permissions, or use
`AliyunROSFullAccess` + `AliyunECSFullAccess` + `AliyunVPCFullAccess` + `AliyunRDSFullAccess`.

## Domain & HTTPS (optional)

| Action | Purpose |
|--------|---------|
| `domain:CheckDomain` | Check domain availability |
| `domain:QueryRegistrantProfiles` | List registrant profiles |
| `domain:SaveRegistrantProfile` | Create a registrant profile |
| `domain:SaveSingleTaskForCreatingOrderActivate` | Submit a registration order |
| `domain:SubmitEmailVerification` | Send registrant email verification |
| `domain:QueryEmailVerification` | Poll registrant email verification |
| `alidns:AddDomain` | Ensure the AliDNS zone exists |
| `alidns:DescribeDomainNs` | Read the zone's NS for delegation checks |
| `alidns:DescribeDomainRecords` | Look up A / `_acme-challenge` TXT records |
| `alidns:AddDomainRecord` | Create the A record and DNS-01 TXT record |
| `alidns:UpdateDomainRecord` | Update an existing record |
| `alidns:DeleteDomainRecord` | Clean up the TXT record after issuance |

Certbot itself runs on the ECS via Cloud Assistant, so certificate issuance needs no extra RAM
action beyond the AliDNS record management above.

## Convenience (managed policies)

To get started fast, attach: `AliyunROSFullAccess`, `AliyunECSFullAccess`, `AliyunVPCFullAccess`,
`AliyunOSSFullAccess`, `AliyunRDSFullAccess` (with RDS), `AliyunSTSAssumeRoleAccess`, plus
`AliyunDomainFullAccess` and `AliyunDNSFullAccess` for the Domain & HTTPS flow. Tighten to the
least-privilege actions above for production.

## On permission failure

A `Forbidden.RAM` on a create call (`CreateStack` / `oss mb` / RDS instance creation) → stop before
the write, report the missing action, do not silently retry. A read-only failure → mark the item
unknown and continue.
