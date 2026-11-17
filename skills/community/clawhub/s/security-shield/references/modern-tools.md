# Modern Security Tools Reference

## Container Scanning
- Trivy: Comprehensive vulnerability scanner for containers and filesystem
  - GitHub: https://github.com/aquasecurity/trivy
  - Install: 
    - **Preferred**: Use official package managers (apt, brew, chocolatey, etc.) when available
    - **Alternative**: Download verified binary from the [releases page](https://github.com/aquasecurity/trivy/releases)
    - **Always**: Verify checksums/signatures of downloaded binaries before execution
  - Usage: `trivy image <image>` or `trivy fs <path>`
  
- Grype: Vulnerability scanner with strong pedigree tracking from Anchore
  - GitHub: https://github.com/anchore/grype
  - Install: 
    - **Preferred**: Use official package managers (apt, brew, chocolatey, etc.) when available
    - **Alternative**: Download verified binary from the [releases page](https://github.com/anchore/grype/releases)
    - **Always**: Verify checksums/signatures of downloaded binaries before execution
  - Usage: `grype <image>:<tag>` or `grype dir:<path>`
  
- Clair: Open-source container vulnerability scanner from Red Hat
  - GitHub: https://github.com/quay/clair
  - Best for: Integrated scanning in container registries
  
- Snyk: Developer-first security for finding and fixing vulnerabilities
  - Website: https://snyk.io/
  - Install: Use official package managers (npm, brew, etc.) or installers from the website

## SBOM Generation
- Syft: Generate SBOMs from containers and filesystems (from Anchore)
  - GitHub: https://github.com/anchore/syft
  - Install: 
    - **Preferred**: Use official package managers (apt, brew, chocolatey, etc.) when available
    - **Alternative**: Download verified binary from the [releases page](https://github.com/anchore/syft/releases)
    - **Always**: Verify checksums/signatures of downloaded binaries before execution
  - Usage: `syft packages -o spdx-json > sbom.spdx` or `syft <image> -o cyclonedx-json > sbom.json`
  
- CycloneDX: SBOM generation and consumption toolkit
  - GitHub: https://github.com/CycloneDX/cyclonedx
  - Usage: Various language-specific generators available
  
- SPDX Tools: Official SPDX format utilities
  - GitHub: https://github.com/spdx/tools
  - Used for: Creating, validating, and converting SPDX documents
  
- GitHub SBOM Generation: Built-in dependency graph export
  - Available via: GitHub REST API or GitHub Advanced Security

## Secrets Management
- HashiCorp Vault: Dynamic secrets and encryption as a service
  - Website: https://www.vaultproject.io/
  - Features: Dynamic secrets, encryption as a service, identity-based access
  - Install: Official packages from HashiCorp repositories or verified binaries
  - CLI: `vault read secret/path`
  
- AWS Secrets Manager: Managed secret storage and rotation
  - Website: https://aws.amazon.com/secrets-manager/
  - Features: Automatic rotation, integration with AWS services
  - Access: Through AWS SDK, CLI, or console
  
- Azure Key Vault: Cloud-based secret management
  - Website: https://azure.microsoft.com/services/key-vault/
  - Features: Managed HSM, certificate management, integration with Azure services
  - Access: Through Azure SDK, CLI, or portal
  
- GCP Secret Manager: Google Cloud Platform secret management
  - Website: https://cloud.google.com/secret-manager
  - Features: Automatic replication, customer-managed encryption keys
  - Access: Through Google Cloud SDK or client libraries
  
- Mozilla SOPS: Encrypted file secrets management
  - GitHub: https://github.com/mozilla/sops
  - Features: Encrypts YAML, JSON, ENV, INI, BINARY files with PGP, AWS KMS, GCP KMS, Azure Key Vault
  - Install: Official package managers or verified binaries from releases
  - Usage: `sops --encrypt --encryption-command 'age -r age1...' file.yaml`
  
- Doppler: Secrets management platform for developers
  - Website: https://doppler.com/
  - Features: Real-time sync, environment management, audit logs
  - Install: Official package managers or verified installers from website
  - CLI: `doppler secrets get MY_SECRET`

## Policy as Code
- Open Policy Agent (OPA): Universal policy engine
  - Website: https://www.openpolicyagent.org/
  - Language: Rego
  - Use cases: Kubernetes admission control, Terraform validation, API authorization
  - Install: Official package managers or verified binaries from releases
  - CLI: `opa eval -i input.json -d policy.rego "data.example.allow"`
  
- HashiCorp Sentinel: Policy-as-code for infrastructure
  - Website: https://www.hashicorp.com/products/sentinel
  - Use cases: Terraform Cloud/Enterprise, Kubernetes admission, Docker Enterprise
  - Language: Sentinel policy language
  - Install: Official distributions from HashiCorp
  
- Conftest: Test structured data using OPA policies
  - GitHub: https://github.com/open-policy-agent/conftest
  - Use cases: Testing Kubernetes manifests, Terraform plans, Dockerfiles, etc.
  - Install: Official package managers or verified binaries from releases
  - CLI: `conftest test k8s-deployment.yaml`
  
- Checkov: Static code analysis for infrastructure as code
  - GitHub: https://github.com/bridgecrewio/checkov
  - Supports: Terraform, CloudFormation, Kubernetes, Serverless, ARM templates
  - Install: Official package managers (pip, etc.) or verified binaries
  - CLI: `checkov -f terraform.tf`
  
- tfsec: Security scanner for Terraform code
  - GitHub: https://github.com/aquasecurity/tfsec
  - CLI: `tfsec .`
  - Install: Official package managers or verified binaries from releases

## Supply Chain Security
- Sigstore: Framework for verifying software signatures
  - Website: https://www.sigstore.dev/
  - Components: Cosign (container signing), Fulcio (CA), Rekor (transparency log)
  - Provides: Keyless signatures, transparent logs, trust verification
  
- Cosign: Container signing, verification, and storage
  - GitHub: https://github.com/sigstore/cosign
  - CLI: `cosign sign --key cosign.key <image>` and `cosign verify --key cosign.pub <image>`
  - Install: Official package managers or verified binaries from releases
  
- SLSA Framework: Supply-chain Levels for Software Artifacts
  - Website: https://slsa.dev/
  - Provides: Framework, guidelines, and tools for securing supply chains
  - Tools: slsa-verifier, slsa-github-generator
  
- In-toto: Framework for ensuring integrity of supply chain
  - Website: https://in-toto.io/
  - Provides: Framework for verifying that steps in a supply chain were executed as intended
  - Used by: Docker, Google, NYU, and others
  
- Tekton Chains: Supply chain security for Tekton
  - Website: https://tekton.dev/docs/chains/
  - Provides: Signing and verification of Tekton task runs and pipeline runs
  
- GitHub Dependency Graph & Alerts: Built-in supply chain security
  - Features: Dependency review, vulnerability alerts, security updates
  
- Dependabot: Automated dependency updates
  - Website: https://dependabot.com/
  - Features: Automatic PRs for dependency updates, security updates

## Runtime Security
- Falco: Cloud-native runtime security
  - Website: https://falco.org/
  - Features: System call-based threat detection, Kubernetes-native
  - Install: Official package managers or verified binaries from releases
  - CLI: `falco -r /etc/falco/falco_rules.yaml`
  
- Tracee: Runtime security and forensics tool
  - GitHub: https://github.com/aquasecurity/tracee
  - Uses: eBPF for runtime security monitoring
  - Install: Official package managers or verified binaries from releases
  
- Tetragon: eBPF-based security observability and runtime enforcement
  - GitHub: https://github.com/cilium/tetragon
  - Install: Official package managers or verified binaries from releases
  
- Trivy Runtime Scanner: Runtime vulnerability and malware scanner
  - From: Aqua Security (same as Trivy)
  - Website: https://aquasecurity.github.io/trivy-runtime-scanner/

## Software Composition Analysis (SCA)
- OWASP Dependency-Check: Identifies project dependencies and checks for known vulnerabilities
  - Website: https://owasp.org/www-project-dependency-check/
  - CLI: `dependency-check --project <project> --scan <scan> --format HTML --out <output>`
  - Install: Official distributions or verified binaries
  
- Snyk Open Source: Find and fix vulnerabilities in open-source dependencies
  - Website: https://snyk.io/test
  - CLI: `snyk test`
  - Install: Official package managers or verified installers
  
- WhiteSource: Continuous open source management
  - Website: https://www.whitesourcesoftware.com/
  
- Black Duck: Comprehensive security and risk analysis for open source
  - Website: https://www.synopsys.com/software-integrity/security-testing/software-composition-analysis.html

## API Security
- Postman: API platform for building and using APIs
  - Website: https://www.postman.com/
  - Security features: API monitoring, automated testing, mock servers
  - Install: Official applications for desktop, mobile, or web
  
- OWASP ZAP: Web application security scanner
  - Website: https://www.zaproxy.org/
  - Features: Automated scanner, passive scanner, traditional and AJAX spiders
  - Install: Official package managers or verified binaries from releases
  
- Burp Suite: Web vulnerability scanner and penetration testing tool
  - Website: https://portswigger.net/burp
  - Editions: Community, Professional, Enterprise
  - Install: Official installers from website
  
- Kong API Gateway: Cloud-native API gateway
  - Website: https://konghq.com/
  - Features: Authentication, rate limiting, analytics, transformation
  - Install: Official package managers or verified binaries from releases
  
- AWS API Gateway: Fully managed service for creating, publishing, maintaining APIs
  - Website: https://aws.amazon.com/api-gateway/
  - Features: Authentication, authorization, throttling, monitoring
  - Access: Through AWS SDK, CLI, or console

## Security Information and Event Management (SIEM)
- Elastic SIEM: Security information and event management
  - Website: https://www.elastic.co/security/siem
  - Part of: Elastic Stack (ELK)
  - Install: Official distributions or verified binaries
  
- Splunk Enterprise Security: Security information and event management
  - Website: https://www.splunk.com/en_us/products/enterprise-security.html
  - Install: Official installers or verified binaries
  
- IBM QRadar: Enterprise security intelligence platform
  - Website: https://www.ibm.com/products/qradar-siem
  - Install: Official distributions or verified binaries
  
- Microsoft Sentinel: Cloud-native SIEM
  - Website: https://azure.microsoft.com/services/sentinel/
  - Access: Through Azure portal
  
- Graylog: Open-source log management
  - Website: https://www.graylog.org/
  - Install: Official package managers or verified binaries from releases
  
- Wazuh: Open-source security platform
  - Website: https://wazuh.com/
  - Features: Log analysis, file integrity monitoring, intrusion detection, vulnerability detection
  - Install: Official package managers or verified binaries from releases

## Vulnerability Management
- Tenable.io: Vulnerability management platform
  - Website: https://www.tenable.io/
  
- Qualys Cloud Platform: Integrated security and compliance solutions
  - Website: https://www.qualys.com/
  
- Rapid7 InsightVM: Vulnerability risk management and remediation
  - Website: https://www.rapid7.com/products/insightvm/
  
- OpenVAS: Open-source vulnerability scanner and manager
  - Website: https://www.openvas.org/
  - Part of: Greenbone Vulnerability Management (GVM)
  - Install: Official distributions or verified binaries

## Container Security Runtime
- Aqua Security: Container-native application security platform
  - Website: https://www.aquasec.com/
  
- Twistlock (now Prisma Cloud by Palo Alto): Cloud-native application protection
  - Website: https://www.paloaltonetworks.com/prisma/prisma-cloud
  
- StackRox (now Red Hat Advanced Cluster Security for Kubernetes): Kubernetes and container security
  - Website: https://www.stackrox.com/
  
- Sysdig Secure: Container and cloud security platform
  - Website: https://sysdig.com/

## Infrastructure as Code (IaC) Security
- Checkov: Static code analysis for infrastructure as code
  - Already mentioned above
  
- tfsec: Security scanner for Terraform code
  - Already mentioned above
  
- Terrascan: Static code analyzer for Infrastructure as Code
  - Website: https://runterrascan.io/
  - Supports: Terraform, Kubernetes, Helm, Kustomize, AWS CloudFormation, ARM Templates
  - Install: Official package managers or verified binaries from releases
  
- TFLint: Terraform linter
  - GitHub: https://github.com/terraform-linters/tflint
  
- Checkov: Already mentioned above
  
- GitHub Code Scanning: Automated code scanning within GitHub
  - Website: https://docs.github.com/en/code-security/code-scanning

## Secrets Detection
- GitGuardian: Detect secrets in code and prevent leaks
  - Website: https://www.gitguardian.com/
  
- TruffleHog: Searches through git repositories for secrets
  - GitHub: https://github.com/trufflesecurity/trufflehog
  - CLI: `trufflehog git https://github.com/user/repo`
  - Install: Official package managers or verified binaries from releases
  
- Gitleaks: SAST tool for detecting hardcoded secrets
  - GitHub: https://github.com/gitleaks/gitleaks
  - CLI: `gitleaks detect --source .`
  - Install: Official package managers or verified binaries from releases
  
- Detect Secrets: Detect secrets in codebase
  - GitHub: https://github.com/Yelp/detect-secrets
  - Install: Official package managers or verified binaries from releases

## Security Headers & CSP Tools
- securityheaders.com: Analyze HTTP security headers
  - Website: https://securityheaders.com/
  
- CSP Evaluator: Evaluate Content Security Policies
  - Website: https://csp-evaluator.withgoogle.com/
  
- Observatory by Mozilla: Website security observatory
  - Website: https://observatory.mozilla.org/

## Network Security
- Wireshark: Network protocol analyzer
  - Website: https://www.wireshark.org/
  - Install: Official package managers or verified binaries from releases
  
- Zeek (formerly Bro): Network security monitor
  - Website: https://www.zeek.org/
  - Install: Official package managers or verified binaries from releases
  
- Suricata: Open source intrusion detection and prevention system
  - Website: https://suricata.io/
  - Install: Official package managers or verified binaries from releases
  
- Snort: Open source network intrusion detection system
  - Website: https://www.snort.org/
  - Install: Official package managers or verified binaries from releases

## Password Security
- Have I Been Pwned: Check if accounts have been compromised in data breaches
  - Website: https://haveibeenpwned.com/
  - API: https://haveibeenpwned.com/API/v2
  
- Password Pwd: Password auditing and recovery tool
  - Website: https://hashcat.net/
  
- John the Ripper: Password cracking tool (for authorized testing only)
  - Website: https://www.openwall.com/john/
  
- Hashcat: Advanced password recovery tool
  - Website: https://hashcat.net/hashcat/

## Encryption Tools
- GnuPG (GPG): Complete and free implementation of OpenPGP standard
  - Website: https://gnupg.org/
  - Install: Official package managers or verified binaries from releases
  
- Age: Simple, modern and secure encryption tool
  - Website: https://github.com/FiloSottile/age
  - Install: Official package managers or verified binaries from releases
  
- SOPS: Already mentioned above (uses age, PGP, KMS services)
  
- Vault: Already mentioned above (encryption as a service)

## Container Admission Control
- Open Policy Agent (OPA): Already mentioned above
  
- Kyverno: Kubernetes native policy management
  - Website: https://kyverno.io/
  - Features: Policy as Kubernetes resources, automatic mutation, validation
  - Install: Official package managers or verified binaries from releases
  
- Gatekeeper: Kubernetes admission controller webhook
  - Website: https://open-policy-agent.github.io/gatekit/website/
  - Built on top of OPA
  
- K-rail: Kubernetes admission controller for CIS benchmark
  - GitHub: https://github.com/tokenbond/k-rail
  - Install: Official package managers or verified binaries from releases

## Image Signing & Verification
- Notary: Project for publishing and managing trusted collections of content
  - Website: https://theupdateframework.github.io/notary/
  
- Cosign: Already mentioned above
  
- Docker Content Trust: Deprecated in favor of Cosign/Sigstore
  
- Harbor: Open source cloud native registry that stores, signs, and scans content
  - Website: https://goharbor.io/

## Development Security
- Pre-commit: Framework for managing and maintaining multi-language pre-commit hooks
  - Website: https://pre-commit.com/
  
- Husky: Git hooks made easy
  - Website: https://typicode.github.io/husky/#/
  
- Lefthook: Fast and powerful Git hooks manager for any type of projects
  - Website: https://github.com/evilmartians/lefthook
  
- Semgrep: Fast, portable static analysis for many languages
  - Website: https://semgrep.dev/
  
- Bandit: Security linter for Python
  - Website: https://bandit.readthedocs.io/en/latest/
  
- ESLint Security Plugins: Security-focused ESLint plugins
  - Examples: eslint-plugin-security, eslint-plugin-no-unsanitized

## Database Security
- pgAudit: PostgreSQL extension for providing detailed session or object audit logging
  - Website: https://www.pgaudit.org/
  
- MongoDB Database Auditing and Filtering: Native MongoDB auditing
  - Website: https://docs.mongodb.com/manual/administration/auditing/
  
- Oracle Audit Vault and Database Firewall: Consolidated audit monitoring
  - Website: https://www.oracle.com/database/security/audit-vault-and-database-firewall/
  
- SQL Server Audit: Auditing for Microsoft SQL Server
  - Website: https://docs.microsoft.com/sql/relational-databases/security/auditing/sql-server-audit-database-engine?view=sql-server-ver16

## Cloud Security Posture Management (CSPM)
- AWS Security Hub: Centralized view of security alerts and compliance status
  - Website: https://aws.amazon.com/security-hub/
  
- Azure Security Center: Unified infrastructure security management system
  - Website: https://azure.microsoft.com/services/security-center/
  
- Google Cloud Security Command Center: Security and risk data platform
  - Website: https://cloud.google.com/security-command-center
  
- Prisma Cloud by Palo Alto: Cloud security platform
  - Website: https://www.paloaltonetworks.com/prisma/prisma-cloud
  
- Dome9 (now Check Point CloudGuard): Cloud security posture management
  - Website: https://www.checkpoint.com/cloudguard/

## Identity and Access Management (IAM)
- HashiCorp Boundary: Identity-based secure remote access
  - Website: https://www.boundaryproject.io/
  
- AWS IAM Identity Center (formerly AWS SSO): Centralized access management
  - Website: https://aws.amazon.com/singlesignon/
  
- Azure Active Directory: Cloud-based identity and access management service
  - Website: https://azure.microsoft.com/services/active-directory/
  
- Okta: Enterprise identity management
  - Website: https://www.okta.com/
  
- JumpCloud: Cloud directory platform
  - Website: https://jumpcloud.com/
  
- Keycloak: Open source identity and access management
  - Website: https://www.keycloak.org/
  
## Zero Trust Implementation
- Zscaler Zero Trust Exchange: Cloud-native zero trust platform
  - Website: https://www.zscaler.com/
  
- Palo Alto Prisma Access: Secure access service edge (SASE)
  - Website: https://www.paloaltonetworks.com/prisma/prisma-access
  
- Cisco Zero Trust: Zero trust security solutions
  - Website: https://www.cisco.com/c/en_os/solutions/zero-trust-security/index.html
  
- Cloudflare Zero Trust: Secure access for teams
  - Website: https://www.cloudflare.com/access/

## Additional References
- OWASP (Open Web Application Security Project): https://owasp.org/
  - Provides: Top 10, testing guides, cheat sheets, and numerous security resources
  
- NIST Cybersecurity Framework: https://www.nist.gov/cyberframework
  - Provides: Framework for improving critical infrastructure cybersecurity
  
- CIS Controls: https://www.cisecurity.org/controls/v8
  - Provides: Prioritized set of actions for cyber defense
  
- MITRE ATT&CK: https://attack.mitre.org/
  - Provides: Globally-accessible knowledge base of adversary tactics and techniques
  
- SANS Institute: https://www.sans.org/
  - Provides: Security training, certifications, and research
  
- The Center for Internet Security (CIS): https://www.cisecurity.org/
  - Provides: Benchmarks, controls, and best practices
  
- First.org (Forum of Incident Response and Security Teams): https://www.first.org/
  - Provides: Standards, best practices, and collaboration for incident response teams