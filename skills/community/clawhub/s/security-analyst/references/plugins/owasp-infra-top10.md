---
name: OWASP Top 10 Infrastructure Security Risks
detect:
  files: ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", "Vagrantfile", "Procfile", "nginx.conf", "haproxy.cfg", "ansible.cfg", "playbook.yml", "inventory.ini", "serverless.yml", "serverless.yaml", "cloudbuild.yaml", "appspec.yml", "buildspec.yml", "skaffold.yaml", "helmfile.yaml", "kustomization.yaml", "packer.json", "packer.pkr.hcl"]
  dependencies: ["@aws-sdk/client-ec2", "@aws-sdk/client-iam", "@aws-sdk/client-s3", "@google-cloud/compute", "@google-cloud/storage", "@azure/arm-compute", "@azure/arm-network", "@azure/identity", "boto3", "botocore", "pulumi", "cdktf", "aws-cdk-lib", "docker", "dockerode", "kubernetes-client", "fabric", "paramiko", "ansible", "mitogen"]
  keywords: ["Terraform", "Kubernetes", "Docker", "CloudFormation", "AWS", "GCP", "Azure", "Infrastructure as Code", "Ansible", "Helm", "Pulumi"]
---

## recon-agent

**OWASP Infrastructure Security — Asset & Configuration Discovery (ISR10, ISR03):**
1. Inventory all Infrastructure-as-Code files and cloud configuration:
   - Glob for `*.tf`, `*.tfvars`, `*.hcl` (Terraform)
   - Glob for `**/k8s/**`, `**/kubernetes/**`, `**/manifests/**`, `**/helm/**` for Kubernetes manifests (Deployments, Services, Ingresses, NetworkPolicies, RBAC)
   - Glob for `Dockerfile*`, `docker-compose*.yml`, `docker-compose*.yaml`
   - Glob for `**/cloudformation/**`, `*.template`, `*.cfn.json`, `*.cfn.yaml` (AWS CloudFormation)
   - Glob for `**/ansible/**`, `playbook*.yml`, `site.yml`, `inventory*` (Ansible)
   - Glob for `serverless.yml`, `serverless.yaml`, `sam-template.yaml` (Serverless Framework / AWS SAM)
   - Glob for `Pulumi.yaml`, `Pulumi.*.yaml`
2. Identify CI/CD pipeline definitions:
   - Glob for `.github/workflows/*.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`, `azure-pipelines.yml`, `bitbucket-pipelines.yml`, `.drone.yml`, `cloudbuild.yaml`, `buildspec.yml`
   - Record which pipelines deploy infrastructure and which have access to cloud credentials
3. Map cloud provider usage:
   - Grep for AWS account IDs (`\d{12}`), region strings (`us-east-1`, `eu-west-1`, etc.), GCP project IDs, Azure subscription/resource group patterns
   - Identify which cloud services are used (compute, storage, database, networking, IAM, KMS)
4. Catalog reverse proxy / load balancer configs:
   - Glob for `nginx.conf`, `nginx/*.conf`, `conf.d/*.conf`, `haproxy.cfg`, `traefik.yml`, `traefik.toml`, `caddy`, `Caddyfile`
   - Note TLS termination points and upstream definitions

## config-infrastructure

**ISR01 — Outdated Software:**
1. **Container Base Image Currency:**
   - Read every `Dockerfile` and check `FROM` directives:
     - **Critical**: Is the base image pinned to a tag known to be EOL? (e.g., `node:14`, `python:3.7`, `ubuntu:18.04`, `debian:stretch`, `alpine:3.14`)
     - **High**: Is the base image using `:latest` without a digest? (non-reproducible builds — the image content can change silently)
     - **High**: Are multi-stage builds discarding the build stage properly, or does the final image inherit build-time dependencies?
   - Check for `apt-get upgrade` / `apk upgrade` in Dockerfiles — these should NOT be relied on as the sole patching strategy; base image updates are required
2. **IaC Provider & Module Versions:**
   - In Terraform files: are provider versions pinned (`required_providers` block)? Are module `source` references pinned to a specific version/tag or using `ref=main`?
   - **High**: Unpinned modules pull latest on every `terraform init` — a supply-chain risk if the module repo is compromised
   - In Helm charts: are chart dependencies pinned to specific versions in `Chart.yaml`?
3. **Runtime Version Pinning:**
   - Check `.node-version`, `.python-version`, `.ruby-version`, `.tool-versions`, `runtime.txt`, engine fields in `package.json`
   - Are specified runtime versions still receiving security updates from the vendor?

**ISR03 — Insecure Configurations:**
4. **Container Security Hardening:**
   - **Critical**: Do any Dockerfiles or Kubernetes pod specs run as root? (check for absence of `USER` directive in Dockerfile; check for `runAsNonRoot: false` or missing `securityContext` in pod specs)
   - **Critical**: Are containers running in `privileged: true` mode? (grants full host access)
   - **High**: Are Linux capabilities added unnecessarily? (check `securityContext.capabilities.add` — especially `SYS_ADMIN`, `NET_ADMIN`, `SYS_PTRACE`)
   - **High**: Is `readOnlyRootFilesystem` set to `true`? (prevents writes to the container filesystem — reduces post-exploitation impact)
   - Is `allowPrivilegeEscalation` explicitly set to `false`?
   - Are `hostNetwork`, `hostPID`, or `hostIPC` enabled? (breaks container isolation)
   - Is `seccompProfile` or `AppArmor` annotation set?
5. **Kubernetes Admission & Policy:**
   - Are Pod Security Standards (PSS) enforced via PodSecurity admission controller or a policy engine (OPA/Gatekeeper, Kyverno)?
   - Is there a `LimitRange` or `ResourceQuota` in each namespace?
   - Are `NetworkPolicy` resources defined to restrict pod-to-pod traffic? (ISR06 overlap — see below)
6. **Web Server / Reverse Proxy Hardening:**
   - Read nginx/Apache/Traefik/Caddy configs:
     - **High**: Is server version exposure disabled? (`server_tokens off` in nginx, `ServerTokens Prod` in Apache)
     - Are security headers configured? (CSP, HSTS with `includeSubDomains; preload`, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy)
     - Is HTTP redirected to HTTPS?
     - Are default/catch-all server blocks returning 444 or 403, not proxying to a backend?
     - Is directory listing disabled?
7. **Cloud Service Configuration:**
   - **Critical**: Are S3 buckets / GCS buckets / Azure Blob containers configured with public access? (Grep for `acl = "public-read"`, `public_access_prevention = "inherited"`, `allow_blob_public_access = true`)
   - **Critical**: Are database instances publicly accessible? (Grep for `publicly_accessible = true`, `authorized_networks` with `0.0.0.0/0`)
   - **High**: Are cloud storage buckets missing server-side encryption? (check for `sse_algorithm`, `encryption` blocks)
   - Are cloud logging services enabled? (CloudTrail, Cloud Audit Logs, Azure Activity Log)
8. **CI/CD Pipeline Security:**
   - **Critical**: Are secrets hardcoded in CI/CD config files? (Grep for `password:`, `secret:`, `token:`, API keys in `.github/workflows/*.yml`, `.gitlab-ci.yml`, etc.)
   - **High**: Are pipeline steps pulling unverified third-party actions/images? (e.g., `uses: some-random-user/action@main` instead of a pinned SHA)
   - Are pipeline runners using ephemeral/disposable environments, or do they persist state between runs?
   - Do pipeline service accounts follow least-privilege? (can a pipeline deploy to production AND read all secrets?)

**ISR05 — Insecure Use of Cryptography:**
9. **TLS Configuration in Infrastructure:**
   - Read TLS/SSL settings in nginx, HAProxy, Traefik, cloud load balancer configs:
     - **Critical**: Is SSLv3, TLS 1.0, or TLS 1.1 enabled? (Grep for `ssl_protocols`, `ssl-min-ver`, `MinimumProtocolVersion`, `min_tls_version`)
     - **High**: Are weak cipher suites allowed? (Grep for `RC4`, `DES`, `3DES`, `NULL`, `EXPORT`, `MD5` in cipher lists)
     - Is HSTS configured with `max-age` of at least 31536000 (1 year)?
     - Is OCSP stapling enabled? (`ssl_stapling on` in nginx)
   - For internal service-to-service communication:
     - Is mTLS configured? (check Kubernetes service mesh configs — Istio, Linkerd `PeerAuthentication`)
     - Are self-signed certificates managed with an internal CA and rotated automatically (cert-manager, Vault PKI)?
10. **Encryption at Rest in IaC:**
    - For every database, storage, and volume resource in Terraform/CloudFormation:
      - Is encryption enabled? (check `storage_encrypted`, `kms_key_id`, `encryption_configuration`)
      - **High**: Is the default cloud-managed key used when a customer-managed key (CMK) is required by policy?
    - For Kubernetes: are etcd secrets encrypted at rest? (check `EncryptionConfiguration` in API server args)
    - Are EBS volumes, persistent disks, and managed disks encrypted by default?

**ISR06 — Insecure Network Access Management:**
11. **Network Segmentation in IaC:**
    - **Critical**: Are security groups / firewall rules allowing `0.0.0.0/0` (any source) to sensitive ports? (SSH/22, RDP/3389, database ports 3306/5432/27017/6379)
    - **High**: Is there a single flat VPC/VNet with no subnet separation between public, private, and data tiers?
    - Are NACLs or VPC flow logs enabled?
    - For Kubernetes: are `NetworkPolicy` resources defined? (no NetworkPolicies = all pods can talk to all pods)
12. **Egress Controls:**
    - Can containers/pods make unrestricted outbound connections? (no egress NetworkPolicy = data exfiltration risk)
    - Is a NAT gateway or proxy used for outbound traffic from private subnets?
    - Are DNS queries controlled? (DNS exfiltration is a common C2 channel)
13. **VPN / Bastion Configuration:**
    - Are bastion hosts / jump boxes hardened and audited?
    - Are VPN concentrators using IKEv2 or WireGuard? (IKEv1 aggressive mode leaks credentials)
    - Is split tunneling disabled on VPN clients? (prevents direct internet access bypassing corporate controls)

**ISR07 — Insecure Authentication Methods and Default Credentials:**
14. **Default Credentials in Infrastructure:**
    - **Critical**: Are database instances deployed with default credentials? (Grep for `master_password`, `admin_password`, common defaults like `admin/admin`, `root/root`, `postgres/postgres` in IaC and config files)
    - **Critical**: Are management interfaces (Grafana, Kibana, Jenkins, Prometheus, Traefik dashboard) protected by auth or exposed with defaults?
    - Check for hardcoded SSH keys or passwords in cloud-init / user-data scripts
    - Are there `.htpasswd` files with weak password hashes (MD5, SHA1)?
15. **SSH Configuration:**
    - Is password authentication disabled? (`PasswordAuthentication no` in sshd_config or cloud-init)
    - Is root login disabled? (`PermitRootLogin no`)
    - Are only Ed25519 or RSA-4096+ keys accepted?
    - Is SSH agent forwarding disabled unless explicitly needed? (`AllowAgentForwarding no`)

**ISR09 — Insecure Access to Resources and Management Components:**
16. **Management Interface Exposure:**
    - **Critical**: Are Kubernetes API servers exposed to the public internet? (check `authorized_networks`, `master_authorized_networks_config`, or absence of private cluster config)
    - **Critical**: Are cloud console / API management ports reachable from untrusted networks?
    - Are admin dashboards (Kubernetes Dashboard, Grafana, Kibana, phpMyAdmin, Adminer, pgAdmin) behind authentication and network restrictions?
    - Is the Docker socket (`/var/run/docker.sock`) mounted into any container? (equivalent to root access on the host)
17. **IAM & Service Account Over-Privilege:**
    - **Critical**: Are IAM policies using `"Action": "*"` or `"Resource": "*"`? (overly permissive — violates least privilege)
    - **High**: Are service accounts shared across environments (dev/staging/prod)?
    - Are Kubernetes ServiceAccounts using the default account with auto-mounted tokens?
    - Is IRSA (AWS), Workload Identity (GCP), or Managed Identity (Azure) used instead of static credentials for pod-to-cloud access?

## attack-surface-http

**Infrastructure Management Endpoint Exposure (ISR09, ISR07):**
1. Search for management / health / debug endpoints that may be exposed:
   - Grep for route patterns: `/healthz`, `/readyz`, `/livez`, `/metrics`, `/debug/pprof`, `/admin`, `/actuator`, `/manage`, `/_internal`, `/status`, `/server-status`, `/server-info`
   - Are these endpoints behind authentication or restricted to internal networks only?
   - **High**: Is the Prometheus `/metrics` endpoint publicly accessible? (leaks service topology, version info, and internal state)
   - **High**: Is the Go pprof debug endpoint (`/debug/pprof`) reachable? (enables CPU profiling, heap dumps, goroutine traces — can leak secrets from memory)
2. Are infrastructure-generated error pages leaking server software versions, stack traces, or internal paths?

## attack-surface-authz

**Infrastructure Access Control Audit (ISR04, ISR09):**
1. **Kubernetes RBAC:**
   - Read all `ClusterRole`, `ClusterRoleBinding`, `Role`, `RoleBinding` manifests:
     - **Critical**: Any binding granting `cluster-admin` to a ServiceAccount or non-admin user?
     - **High**: Any role with `verbs: ["*"]` or `resources: ["*"]`?
     - Are roles scoped to namespaces where possible (Role) vs cluster-wide (ClusterRole)?
   - Is the default ServiceAccount in each namespace given excessive permissions?
   - Are there pods with `automountServiceAccountToken: true` that don't need API access?
2. **Cloud IAM Analysis:**
   - For Terraform IAM resources (`aws_iam_policy`, `google_project_iam_member`, `azurerm_role_assignment`):
     - Are policies granting admin-level access to non-admin roles?
     - Are there cross-account trust relationships that are overly broad?
     - Are there IAM users with long-lived access keys instead of assuming roles via STS/Workload Identity?
3. **Resource Sharing & Tenancy (ISR04):**
   - Are there shared databases, message queues, or storage buckets between services that should be isolated?
   - Is tenant isolation enforced at the infrastructure level (separate VPCs, separate accounts/projects) or only at the application level?
   - Can a compromised service access another service's secrets in the same secret manager namespace?

## dependency-audit

**Infrastructure Dependency Currency (ISR01):**
1. **IaC Module & Provider Supply Chain:**
   - Are Terraform modules sourced from the public registry with version constraints, or from unverified Git repos?
   - Are Helm chart repositories using HTTPS and are chart signatures verified (`helm verify`)?
   - For GitHub Actions: are actions pinned to SHA digests or mutable tags? (`uses: actions/checkout@v4` is mutable — `uses: actions/checkout@<sha>` is safe)
   - For Docker images: are base images pulled from verified publishers / official images?
2. **Infrastructure Tool Versions:**
   - Is the Terraform version pinned in `required_version`? Is it within the supported/latest minor release?
   - Are Helm, kubectl, and other IaC tool versions pinned in CI/CD and developer environments?
   - Are there Ansible Galaxy roles installed without version pins?
3. **Container Image Scanning:**
   - Is container image scanning integrated into CI/CD (Trivy, Grype, Snyk Container, Clair)?
   - Are there `COPY` directives in Dockerfiles pulling from unverified URLs?
   - Do multi-stage builds discard build dependencies from the final image?

## data-flow-tracer

**Infrastructure Data Transit Security (ISR05, ISR08):**
1. **Internal Communication Encryption:**
   - Trace service-to-service communication paths defined in IaC (Kubernetes Services, security group rules, VPC peering):
     - Are internal services communicating over plaintext HTTP? (check `targetPort`, backend service definitions, upstream blocks)
     - Is a service mesh enforcing mTLS for all internal traffic, or only for some services?
   - For message queues and event buses (SQS, Pub/Sub, Kafka, RabbitMQ, Redis):
     - Is in-transit encryption enabled? (check `transit_encryption_enabled`, TLS listener configs)
     - Can messages be intercepted by a compromised pod/service on the same network?
2. **Log & Monitoring Data Paths (ISR08):**
   - Where do application logs flow? (stdout → log aggregator → storage)
   - Are logs encrypted in transit and at rest?
   - **High**: Can a compromised container read another container's log stream via a shared logging sidecar or volume?
   - Are structured logging frameworks configured to redact sensitive fields before shipping?
3. **Backup & Snapshot Exposure (ISR08):**
   - Are database snapshots, VM snapshots, or volume backups accessible to roles beyond the backup operator?
   - Are backups encrypted with a separate key from the primary data?
   - Are cross-region backup copies subject to the same access controls as the primary?

## git-history-data-exposure

**Historical Infrastructure Secret Exposure (ISR08, ISR07):**
1. Search git history for committed infrastructure secrets:
   - `git log --all -p -S "AKIA"` (AWS access key prefix)
   - `git log --all -p -S "aws_secret_access_key"` / `"aws_access_key_id"`
   - `git log --all -p -S "GOOG"` / `"private_key_id"` (GCP service account keys)
   - `git log --all -p -S "password"` in `*.tf`, `*.tfvars`, `*.yml`, `*.yaml` files
   - `git log --all --diff-filter=D -- "*.pem" "*.key" "*.pfx" "*.p12" "*.jks" "*.keystore"` (deleted key files)
   - `git log --all --diff-filter=D -- "*.tfvars" "*.env" "terraform.tfstate"` (deleted state/var files)
2. Check for Terraform state files committed to the repo:
   - **Critical**: `terraform.tfstate` or `*.tfstate` in git history contains all resource attributes in plaintext — including database passwords, API keys, and private endpoints
   - Even if removed later, the state file persists in git history unless force-purged
3. Check for overly permissive `.gitignore` changes:
   - Was `*.tfvars` or `*.tfstate` added to `.gitignore` AFTER it was already committed? (secrets already in history)
   - Were cloud credential files (`.aws/credentials`, `gcloud/application_default_credentials.json`) ever committed?

## logic-dos

**Infrastructure Resource Exhaustion (ISR03, ISR06):**
1. **Kubernetes Resource Limits:**
   - **High**: Are pod resource `requests` and `limits` defined for CPU and memory? (missing limits = a single pod can consume all node resources)
   - Is a `LimitRange` defined per namespace to enforce defaults?
   - Is a `ResourceQuota` defined to cap total resource consumption per namespace?
   - Can a user create unlimited PersistentVolumeClaims, consuming all available storage?
2. **Auto-Scaling Guardrails:**
   - Is HorizontalPodAutoscaler (HPA) configured with `maxReplicas`? (unbounded scaling = cost explosion)
   - Are cloud auto-scaling groups configured with maximum instance counts?
   - Are there budget alerts / spending caps to detect abnormal scaling?
3. **Rate Limiting at Infrastructure Layer:**
   - Is rate limiting configured in the reverse proxy / API gateway / ingress controller? (check nginx `limit_req_zone`, Traefik `rateLimit`, cloud API Gateway throttling)
   - Are there WAF rules to block volumetric attacks before they reach the application?
   - Is connection throttling configured for databases to prevent connection pool exhaustion?

## logic-race-conditions

**Infrastructure Deployment Races (ISR03):**
1. **IaC State Locking:**
   - Is Terraform state backend configured with locking? (S3+DynamoDB, GCS, Azure Blob with lease)
   - **High**: Can two concurrent `terraform apply` runs corrupt the state file?
   - Are Helm releases using atomic installs (`--atomic`) to prevent partial deployments?
2. **Rolling Deployment Consistency:**
   - During Kubernetes rolling deployments, can requests be routed to both old and new versions simultaneously?
   - If database migrations run during deployment, can the old version's code be incompatible with the new schema?
   - Are readiness probes configured to prevent traffic to pods that haven't completed initialization?
3. **Secret Rotation During Deployment:**
   - If secrets are rotated via a deployment (new ConfigMap/Secret), can some pods still reference the old secret while others use the new one?
   - Are external secret operators (External Secrets Operator, Vault Agent) configured with proper refresh intervals to avoid split-brain?
