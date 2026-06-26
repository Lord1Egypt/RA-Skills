## Description: <br>
Expert guidance for migrating Java projects from Spring Boot / Spring Cloud to the Solon framework, with comprehensive annotation mapping, dependency replacement, architecture differences, and step-by-step migration strategies for each layer (IoC, Web, Data, Cloud, Testing). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noear](https://clawhub.ai/user/noear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute migrations from Spring Boot or Spring Cloud applications to Solon, including dependency replacement, annotation mapping, configuration changes, web/data/cloud layer migration, and test migration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration examples may be copied into production with placeholder credentials or JWT secrets. <br>
Mitigation: Review generated code before applying it and replace all sample credentials and JWT secrets with environment or secret-manager values. <br>
Risk: Database migration examples may encourage automatic DDL changes in production. <br>
Mitigation: Avoid automatic DDL updates in production and route schema changes through the project's normal database review process. <br>
Risk: File upload or download migration examples may be unsafe if copied without hardening. <br>
Mitigation: Use safe filenames, path normalization, allowlists, and storage outside the web root for upload and download handlers. <br>


## Reference(s): <br>
- [Spring Boot Comparison](https://solon.noear.org/article/compare-springboot) <br>
- [Spring Cloud Comparison](https://solon.noear.org/article/compare-springcloud) <br>
- [Solon Website](https://solon.noear.org) <br>
- [Spring to Solon Annotation Mapping](references/annotation_mapping.md) <br>
- [Maven Dependency Mapping](references/dependency_mapping.md) <br>
- [IoC, AOP, and Component Migration](references/ioc_aop_migration.md) <br>
- [Configuration System Migration](references/config_system_migration.md) <br>
- [Controller and Request Context Migration](references/web_controller_migration.md) <br>
- [Filter, Interceptor, and Exception Migration](references/web_filter_interceptor_migration.md) <br>
- [Web Advanced Feature Migration](references/web_advanced_migration.md) <br>
- [Datasource and ORM Migration](references/datasource_orm_migration.md) <br>
- [Transaction and Cache Migration](references/transaction_cache_migration.md) <br>
- [Cloud Discovery and Config Migration](references/cloud_discovery_config_migration.md) <br>
- [Cloud Gateway and RPC Migration](references/cloud_gateway_rpc_migration.md) <br>
- [Cloud Observability Migration](references/cloud_observability_migration.md) <br>
- [Test Basics Migration](references/test_basics_migration.md) <br>
- [Test Advanced Migration](references/test_advanced_migration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown with Java, XML, YAML, and shell-oriented migration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May respond in Chinese with Chinese code comments when the user communicates in Chinese.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
