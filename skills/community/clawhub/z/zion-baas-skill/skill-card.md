## Description: <br>
Instructions and authentication code for building headless BaaS applications with Zion.app (functorz.com). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timqin-m](https://clawhub.ai/user/timqin-m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect agent workflows to Zion.app projects as a headless backend, including schema lookup, GraphQL queries and mutations, subscriptions, and project runtime token setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext Zion credentials can expose developer, admin, or user tokens if .zion/credentials.yaml is committed, shared, or left readable in a shared workspace. <br>
Mitigation: Add .zion/credentials.yaml to .gitignore, restrict file permissions, avoid shared machines and workspaces, and rotate tokens after use. <br>
Risk: Runtime admin tokens can execute live backend queries, mutations, subscriptions, and production administrative actions. <br>
Mitigation: Install only for Zion projects you own or administer, require explicit review before mutations or production actions, and use least-privilege roles for routine checks. <br>
Risk: Email/password CLI authentication can expose account credentials through shell history, process listings, or recorded terminal sessions. <br>
Mitigation: Prefer OAuth login, avoid passing passwords on shared machines, and rotate tokens or credentials after sensitive sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timqin-m/zion-baas-skill) <br>
- [Zion.app](https://www.functorz.com) <br>
- [Zion runtime GraphQL endpoint pattern](https://zion-app.functorz.com/zero/{projectExId}/api/graphql-v2) <br>
- [Zion subscription endpoint pattern](wss://zion-app.functorz.com/zero/{projectExId}/api/graphql-subscription) <br>
- [Zion Meta API](https://zionbackend.functorz.com/api/graphql) <br>
- [Zion authentication](https://auth.functorz.com/login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline GraphQL, shell command examples, JSON output, and YAML credential configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes CLI scripts that can write .zion/credentials.yaml and execute authenticated Zion GraphQL operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
