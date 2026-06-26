## Description: <br>
SecondMe Connect helps Baidu Miaoda React and Supabase applications add SecondMe OAuth2 login and API access using ready-to-copy templates and integration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building Baidu Miaoda, React, TypeScript, Vite, and Supabase applications use this skill to integrate SecondMe sign-in, manage the OAuth callback, initialize profile storage, and call SecondMe user, chat, memory, notes, plaza, and voice APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable SecondMe access and refresh tokens are stored in a client-readable Supabase profile table. <br>
Mitigation: Move tokens to backend-only storage or deny client SELECT on token columns and proxy SecondMe API calls through Edge Functions. <br>
Risk: Incorrect RLS policies could expose one user's SecondMe tokens to another user. <br>
Mitigation: Test RLS with multiple authenticated users and verify profile queries only return the current user's row before production use. <br>
Risk: Overly broad CORS settings could let untrusted origins invoke the OAuth callback flow. <br>
Mitigation: Set ALLOWED_ORIGINS to the exact production frontend origins and avoid wildcard origins. <br>
Risk: Browser-side bearer tokens increase impact from cross-site scripting or malicious dependencies. <br>
Mitigation: Harden the frontend against XSS, minimize token scopes and lifetimes, and provide clear consent and privacy notices for chat, memory, notes, and public posting features. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijinhongucl-pixel/secondme-connect-miaoda) <br>
- [Publisher profile](https://clawhub.ai/user/lijinhongucl-pixel) <br>
- [SecondMe OAuth authorization endpoint](https://go.second-me.cn/oauth/) <br>
- [SecondMe API base endpoint](https://api.mindverse.com/gate/lab/api/secondme) <br>
- [SecondMe OAuth token endpoint](https://api.mindverse.com/gate/lab/api/oauth/token/code) <br>
- [Integration guide](artifact/templates/INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with TypeScript, SQL, environment variable, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reusable React components, hooks, Supabase Edge Function code, database SQL, and OAuth/API integration guidance.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
