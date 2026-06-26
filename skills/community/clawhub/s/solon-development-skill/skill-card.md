## Description: <br>
Provides specialized guidance for developing Java applications with the Solon framework, including core concepts, web, data, security, remoting, AI, flow orchestration, cloud-native, testing, and Solon-specific architecture rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noear](https://clawhub.ai/user/noear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or review Java applications using Solon, with emphasis on Solon's own annotations, configuration, dependency model, and plugin ecosystem rather than Spring patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security, remoting, credential, and AI tool snippets may be copied into real applications without production hardening. <br>
Mitigation: Treat examples as reference patterns only; restrict CORS to trusted origins, implement real authorization checks, avoid hardcoded tokens or vault passwords, and sandbox or narrowly scope agent tools before adopting similar patterns. <br>
Risk: Incorrectly mixing Spring concepts or dependencies into Solon projects can produce broken or misleading implementations. <br>
Mitigation: Follow the skill's Solon-specific rules for annotations, configuration files, entry points, parent POM, and org.noear dependencies. <br>


## Reference(s): <br>
- [Solon official website](https://solon.noear.org) <br>
- [Solon GitHub repository](https://github.com/opensolon/solon) <br>
- [Quick Start](references/quick_start.md) <br>
- [Core Concepts](references/core_concepts.md) <br>
- [Modules Reference](references/modules_reference.md) <br>
- [API & Annotations Reference](references/api_annotations.md) <br>
- [Common Patterns](references/common_patterns.md) <br>
- [Web Advanced](references/web_advanced.md) <br>
- [Security](references/security.md) <br>
- [Remoting](references/remoting.md) <br>
- [Logging](references/logging.md) <br>
- [Testing](references/testing.md) <br>
- [Cloud Native](references/cloud_native.md) <br>
- [AI Development](references/ai_development.md) <br>
- [Flow Orchestration](references/flow_orchestration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline Java, YAML, XML, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May provide Chinese responses and code comments when the user communicates in Chinese.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
