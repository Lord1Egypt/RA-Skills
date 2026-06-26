---
name: AWS / GCP / Azure Cloud
detect:
  files: ["terraform", "*.tf", "cloudformation", "cdk.json", "serverless.yml", "sam-template.yaml", "bicep"]
  dependencies: ["aws-sdk", "@aws-sdk/client-s3", "@google-cloud/storage", "google-cloud-storage", "@azure/storage-blob", "boto3", "aws-cdk-lib", "pulumi"]
  keywords: ["AWS", "GCP", "Azure", "Lambda", "Cloud Functions", "S3", "EC2", "ECS", "EKS", "GKE", "AKS"]
---

## recon-agent

**Cloud Infrastructure Discovery:**
1. Glob for `**/*.tf`, `**/*.tf.json` — Terraform configurations
2. Glob for `**/template.yaml`, `**/template.yml`, `**/sam-template*`, `**/cloudformation*` — CloudFormation/SAM
3. Glob for `**/cdk.json`, `**/lib/*.ts` (CDK stacks), `**/stacks/**`
4. Glob for `**/serverless.yml`, `**/serverless.ts` — Serverless Framework
5. Glob for `**/*.bicep`, `**/arm-template*` — Azure ARM/Bicep
6. Glob for `**/Pulumi.yaml`, `**/Pulumi.*.yaml` — Pulumi
7. Check for cloud-specific config: `~/.aws/`, environment variables (`AWS_*`, `GOOGLE_*`, `AZURE_*`)

## config-infrastructure

**IAM & Access Control:**
1. **Overly Permissive Policies:**
   - Grep for `"Action": "*"` or `"Action": ["*"]` in IAM policies — this grants full access
   - Grep for `"Resource": "*"` — is the policy scoped to specific resources?
   - Are there `AdministratorAccess` or `PowerUserAccess` policies attached to application roles?
   - Check for `iam:PassRole` with `*` resource — allows role assumption escalation
2. **Service Account / IAM Role Scope:**
   - Is the application's execution role using least privilege?
   - Are there unused permissions that could be removed?
   - Is cross-account access restricted to specific external IDs/conditions?
3. **Assume Role Chains:**
   - Can the application assume other roles? Is the trust policy restrictive?
   - Is MFA required for role assumption?

**Storage Security:**
4. **Public Buckets/Blobs:**
   - Grep for `"PublicRead"`, `"public-read"`, `publicAccess`, `AllUsers`, `allAuthenticatedUsers` in IaC
   - Are S3 bucket policies allowing public access? Is `BlockPublicAccess` enabled?
   - GCS: Is `allUsers` or `allAuthenticatedUsers` in IAM bindings?
   - Azure: Is blob container access level set to `blob` or `container`? (should be `private`)
5. **Encryption at Rest:**
   - Are storage buckets encrypted with customer-managed keys (CMK) or default encryption?
   - Is server-side encryption enforced via bucket policy? (deny PutObject without SSE header)
6. **Access Logging:**
   - Is access logging enabled for storage buckets? (audit trail for data access)

**Network Security:**
7. **Security Groups / Firewall Rules:**
   - Grep for `0.0.0.0/0` or `::/0` in ingress rules — overly permissive inbound access
   - Are there security groups allowing all traffic on all ports from any source?
   - Are SSH (22) or RDP (3389) ports open to the internet?
   - Are database ports (3306, 5432, 27017, 6379) accessible from outside the VPC?
8. **VPC Configuration:**
   - Is the application in a VPC? (services outside VPC have less network isolation)
   - Are there public subnets that should be private?
   - Is a NAT gateway used for outbound internet access from private subnets?

**Serverless Security:**
9. **Lambda/Cloud Functions:**
   - Is the function's execution role overly permissive?
   - Is the function URL publicly accessible without auth? (`AuthType: NONE`)
   - Are environment variables containing secrets encrypted with KMS?
   - Is reserved concurrency set? (prevent DoS via function invocation flooding)
10. **API Gateway:**
    - Is the API Gateway using authentication? (API key, IAM, Cognito, Lambda authorizer)
    - Is request validation enabled? (schema validation at the gateway level)
    - Are rate limits and throttling configured?
    - Is logging enabled? (CloudWatch/Cloud Logging for audit)

**Secrets & Key Management:**
11. **Hardcoded Credentials in IaC:**
    - Grep for `SecretString`, `password`, `api_key`, `access_key` in Terraform/CloudFormation
    - Are secrets referenced from Secrets Manager / Parameter Store / Key Vault instead of hardcoded?
    - Are KMS keys configured with key rotation?
12. **Terraform State:**
    - Is Terraform state stored remotely with encryption? (S3+DynamoDB, GCS, Azure Blob)
    - Is state file access restricted? (state contains all resource attributes including secrets)
    - Is state locking enabled to prevent concurrent modifications?

## attack-surface-http

**Cloud API Gateway Patterns:**
1. Check for API Gateway / Cloud Endpoints / Azure API Management configurations
2. Are there endpoints missing authentication at the gateway level?
3. Can the backend be accessed directly, bypassing the gateway? (check security groups / firewall rules)
4. Are request/response transformations exposing internal data?

## data-flow-tracer

**Cloud Data Flow Patterns:**
1. Trace data across cloud services: API Gateway → Lambda → DynamoDB/S3 → notification
2. Are there cross-service permissions that allow lateral movement? (Lambda with S3 full access)
3. Is data encrypted in transit between services? (VPC endpoints, TLS)
4. Are there event-driven flows where the event payload is not validated? (S3 event → Lambda, SNS → Lambda)

## dependency-audit

**Cloud IaC Dependency Concerns:**
1. Check Terraform provider versions for known vulnerabilities
2. Are Terraform modules from trusted sources? (registry vs git references)
3. Check CDK construct library versions
4. Are CloudFormation macros from trusted sources?
