## Description:

Expert guidance for migrating Java projects from Spring Boot and Spring Cloud to the Solon framework, including annotation mapping, dependency replacement, architecture differences, and layer-by-layer migration strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noear](https://clawhub.ai/user/noear)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute migrations from Spring Boot or Spring Cloud applications to Solon. It provides reference mappings, code examples, dependency replacements, and checklists across IoC, web, data, cloud, and testing layers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copy-ready examples may teach unsafe authentication, file handling, and secret practices.

Mitigation: Review examples before using them in real code; replace file upload/download, login/session, authorization filter, and configuration examples with secure implementations using canonical path checks, real token validation, password hashing or an identity provider, and environment-backed secrets.

## Reference(s):

- [Solon Spring Boot comparison](https://solon.noear.org/article/compare-springboot)
- [Solon Spring Cloud comparison](https://solon.noear.org/article/compare-springcloud)
- [Solon website](https://solon.noear.org)
- [Spring to Solon annotation mapping](references/annotation_mapping.md)
- [Maven dependency mapping](references/dependency_mapping.md)
- [IoC and AOP migration reference](references/ioc_aop_migration.md)
- [Configuration system migration reference](references/config_system_migration.md)
- [Web controller migration reference](references/web_controller_migration.md)
- [Web filter and interceptor migration reference](references/web_filter_interceptor_migration.md)
- [Advanced web migration reference](references/web_advanced_migration.md)
- [Datasource and ORM migration reference](references/datasource_orm_migration.md)
- [Transaction and cache migration reference](references/transaction_cache_migration.md)
- [Cloud discovery and configuration migration reference](references/cloud_discovery_config_migration.md)
- [Cloud gateway and RPC migration reference](references/cloud_gateway_rpc_migration.md)
- [Cloud observability migration reference](references/cloud_observability_migration.md)
- [Basic testing migration reference](references/test_basics_migration.md)
- [Advanced testing migration reference](references/test_advanced_migration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Java, XML, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responds in Chinese, including code comments, when the user communicates in Chinese.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
