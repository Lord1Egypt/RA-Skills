## Description:

SecondMe Connect helps Baidu Miaoda React applications add SecondMe OAuth2 login and SecondMe API access using Supabase templates and integration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Baidu Miaoda or React applications use this skill to integrate SecondMe OAuth2 sign-in, Supabase-backed account handling, and typed helper code for SecondMe chat, memory, notes, plaza, and voice APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SecondMe access and refresh tokens may be exposed if frontend code reads bearer tokens or if the application is compromised or misconfigured.

Mitigation: Keep SecondMe tokens in server-only storage and expose scoped backend endpoints for frontend API calls.

Risk: OAuth state handling may be insufficient if state is generated or validated only in frontend browser storage.

Mitigation: Generate cryptographically strong OAuth state values and validate them server-side during the callback exchange.

Risk: Profile update permissions could allow credential columns to be modified by users.

Mitigation: Ensure profile update policies exclude SecondMe credential columns and verify Row Level Security behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijinhongucl-pixel/skills/secondme-connect-miaoda)
- [SecondMe authorization endpoint](https://go.second-me.cn/oauth/)
- [SecondMe API base endpoint](https://api.mindverse.com/gate/lab/api/secondme)
- [SecondMe OAuth token endpoint](https://api.mindverse.com/gate/lab/api/oauth/token/code)
- [Integration guide](artifact/templates/INTEGRATION.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, SQL]

**Output Format:** [Markdown documentation with TypeScript, SQL, environment variable, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable React, Supabase Edge Function, API wrapper, hook, and database template files.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
