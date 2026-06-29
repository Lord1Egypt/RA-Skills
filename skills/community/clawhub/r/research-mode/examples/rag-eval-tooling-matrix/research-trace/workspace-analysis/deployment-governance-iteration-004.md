# Iteration 004 - Deployment and Governance Evidence Notes

Focused question: which deployment and governance attributes are publicly verifiable enough to score in the RAG evaluation tooling workbook?

## Proposed workbook fields

Use separate columns for:

- `license_or_commercial_posture`
- `deployment_options`
- `self_hosting_evidence`
- `managed_saas_evidence`
- `access_control_evidence`
- `retention_or_data_control_evidence`
- `enterprise_controls_evidence`
- `governance_confidence`
- `governance_notes`

Recommended values should be compact and evidence-oriented: `Yes`, `No`, `Enterprise only`, `Cloud/managed`, `Self-hosted`, `Local/CLI`, `Unknown from public docs`, or `Not applicable`.

## Candidate evidence updates

### LangSmith

- Deployment: official enterprise docs list Cloud, Hybrid, and Self-hosted options. Cloud includes US/EU data residency; hybrid keeps the data plane in the customer's VPC; self-hosted can run with Docker Compose or Kubernetes.
- Access control: the same docs mention user roles, SCIM, SAML/OIDC SSO, and JIT provisioning.
- Retention: the administration overview describes trace retention tiers: Base at 14 days, Extended at 400 days, with enterprise customization.
- Workbook implication: strong governance score for enterprise teams, but open-source/self-host scoring should reflect that self-hosting is an enterprise deployment option, not a community OSS tool.
- Sources: https://docs.langchain.com/langsmith/enterprise and https://docs.langchain.com/langsmith/administration-overview

### Langfuse

- Access control: official RBAC docs list organization/project role concepts and roles including Owner, Admin, Member, Viewer, and None.
- Retention: official data-retention docs cover retention windows and note extra object-delete requirements for self-hosted S3-compatible storage.
- Self-hosting and enterprise: public docs/pricing show self-hosting and enterprise governance features such as project-level RBAC, data retention policies, and audit logs.
- Workbook implication: score self-hosting/RBAC/retention as verified, but distinguish OSS/core features from Enterprise Edition features.
- Sources: https://langfuse.com/docs/administration/rbac, https://langfuse.com/docs/administration/data-retention, and https://langfuse.com/pricing-self-host

### Phoenix

- Access control: Phoenix self-hosting docs describe user management when authentication is enabled and roles `admin`, `member`, and `viewer`.
- Privacy/data control: Phoenix self-hosting privacy docs state that self-hosted Phoenix does not send trace, evaluation, dataset, or other application data to Arize or third parties; the customer controls storage, access, retention, and compliance.
- Workbook implication: strong self-host/privacy evidence for Phoenix OSS; managed compliance/security should be represented separately through Arize AX/Phoenix Cloud, not inferred for OSS Phoenix.
- Sources: https://arize.com/docs/phoenix/self-hosting/features/authentication and https://arize.com/docs/phoenix/self-hosting/security/privacy

### W&B Weave

- Self-managed deployment: official docs provide a self-managed Weave deployment path, but it requires W&B Platform, a Weave-enabled W&B license, Kubernetes, ClickHouse, and S3-compatible storage.
- Workbook implication: mark self-managed as verified but enterprise/licensed/operationally heavy, not lightweight OSS self-hosting.
- Source: https://docs.wandb.ai/weave/guides/platform/weave-self-managed

### Evidently

- OSS/commercial posture: official docs say the Evidently library and Tracely library are OSS under Apache 2.0 and describe an Evidently Platform with OSS and commercial editions.
- Platform governance: docs say commercial platform editions include collaboration/scalability and security features such as role-based access control.
- Evidence risk: the same page currently contains confusing wording around Evidently Cloud availability: it says Evidently Cloud is no longer available as a SaaS product, while later describing Cloud/Enterprise commercial deployment options. Treat SaaS availability as `needs verification` unless another current source resolves it.
- Workbook implication: score OSS library and platform separately; do not overstate SaaS status.
- Source: https://docs.evidentlyai.com/faq/oss_vs_cloud

### DeepEval / Confident AI

- OSS/commercial split: GitHub describes DeepEval as an Apache-2.0 open-source framework for local/unit-test-style LLM evals; the enterprise page positions Confident AI as the team platform.
- Enterprise controls: Confident AI's public enterprise page claims cloud or self-hosted deployment, SSO, RBAC, granular permissions, audit logs, SOC 2 Type II, GDPR compliance, and custom retention.
- Workbook implication: split `DeepEval OSS` capability from `Confident AI platform` governance. If kept as one row, governance notes must say enterprise controls are platform-side, not the local OSS runner.
- Sources: https://github.com/confident-ai/deepeval and https://deepeval.com/enterprise

### MLflow GenAI

- Self-hosting: MLflow docs state MLflow is fully open-source and commonly self-hosted.
- Access control: MLflow self-hosting security docs describe basic HTTP authentication for experiments, registered models, and scorers, with APIs for managing users and permissions.
- Workbook implication: strong open-source/self-host score; governance depth depends on deployment architecture and whether teams use open-source MLflow alone or a managed platform such as Databricks/SageMaker.
- Sources: https://mlflow.org/docs/latest/self-hosting/ and https://mlflow.org/docs/latest/self-hosting/security/basic-http-auth/

### Promptfoo

- OSS/local posture: GitHub describes Promptfoo as MIT-licensed, CLI/library based, local/private by default, and CI/CD-friendly.
- Security model: Promptfoo's SECURITY.md says OSS Promptfoo is a local eval runner, not a sandbox for adversarial eval content; user-provided configs and code-executing fields must be treated as trusted code.
- Workbook implication: score highly for local/privacy/CI, but governance notes should flag no shared enterprise RBAC in the OSS runner and recommend isolated execution for untrusted eval packs.
- Sources: https://github.com/promptfoo/promptfoo and https://github.com/promptfoo/promptfoo/blob/main/SECURITY.md

### Giskard

- OSS/commercial split: the Giskard OSS repository identifies an Apache-2.0 open-source evaluation/testing library.
- Enterprise controls: Giskard's public site describes data residency/isolation, RBAC, audit trails, identity-provider integration, SOC 2 Type II, HIPAA, GDPR, and on-premise Hub availability for mission-critical workloads.
- Workbook implication: split OSS library capability from Giskard Hub governance, or mark enterprise controls as Hub-side only.
- Sources: https://github.com/Giskard-AI/giskard-oss and https://www.giskard.ai/

## Analysis implications

- Primary workbook rows can stay focused on practical evaluation stack choices, but governance fields need explicit evidence confidence rather than inferred values.
- The scoring model should assign capability scores independently from deployment/governance scores.
- Caveat rows should include framework-native tools and deprecated/legacy tools. Governance should not rescue a tool if the primary evaluation workflow is not a good standalone RAG stack fit.
- Unknowns should remain visible in the workbook rather than converted into low scores by default.
