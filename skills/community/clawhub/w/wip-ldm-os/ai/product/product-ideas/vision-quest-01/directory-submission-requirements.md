# MCP Directory Submission Requirements

## Anthropic Connectors Directory

### Technical Requirements
- Streamable HTTP transport (mandatory, SSE deprecated)
- Max 25,000 tokens per tool result
- 300 second timeout (claude.ai/Desktop)
- Max 64 char tool names
- Every tool MUST have readOnlyHint and destructiveHint annotations (30% of rejections from this)
- HTTPS with valid TLS certificates
- CORS configured for browser clients
- Must allowlist Claude IPs from https://docs.claude.com/en/api/ip-addresses
- Server must be production-grade (no beta/alpha status)

### OAuth Requirements
- OAuth 2.0 Authorization Code Flow
- Callback URLs to allowlist:
  - http://localhost:6274/oauth/callback
  - http://localhost:6274/oauth/callback/debug
  - https://claude.ai/api/mcp/auth_callback
  - https://claude.com/api/mcp/auth_callback
- Must handle HEAD requests without tokens gracefully post-OAuth
- Return 401 for expired/invalid sessions
- Tokens removed from Anthropic systems on disconnect

### Metadata
- Favicon auto-pulled from domain (test at 16/32/48/64/96/128px)
- Required docs sections: Description, Features, Setup, Auth, Usage Examples (min 3), Privacy Policy, Support
- Must include account requirement language with sign-up links

### Review Process
- Submission via Google Form: https://docs.google.com/forms/d/e/1FAIpQLSeafJF2NDI7oYx1r8o0ycivCSVLNq92Mpc1FPxMKSw1CzDkqA/viewform
- Provide test credentials (share via 1Password)
- No guaranteed timeline
- Common rejections: missing tool annotations (30%), OAuth issues, <3 examples, beta status, missing privacy policy
- Periodic post-admission reviews

### Content Policy
- PROHIBITED: financial transactions, AI image/video/audio gen, ads, cross-service automation, accessing user chats/memory/uploads
- Tool descriptions must narrowly describe function
- Prioritize user privacy, collect only necessary data

### Legal
- Must verify ownership of API endpoints/domains
- Grant Anthropic license to display branding
- Allow Anthropic security testing
- Implement vulnerability disclosure mechanism
- Anthropic can remove at any time without liability

---

## ChatGPT Apps Directory (OpenAI)

### Technical Requirements
- Endpoint path: /mcp (required)
- HTTP methods: POST, GET, DELETE
- Recommended: GET / health check
- Domain verification: place token at /.well-known/openai-apps-challenge (plain text)
- Tool annotations: readOnlyHint, destructiveHint, openWorldHint (all three)
- destructiveHint requires justification (what's irreversible, conditions, safeguards)
- Do NOT request conversation history, raw transcripts, broad context
- Do NOT return PII, telemetry IDs, auth secrets, debug payloads in responses
- HTTPS required, publicly accessible

### OAuth Requirements
- OAuth 2.1 with PKCE (S256 mandatory)
- Dynamic Client Registration (DCR) currently mandatory
- Protected Resource Metadata required (RFC 9728) at /.well-known/oauth-protected-resource
- Authorization Server Discovery required at /.well-known/oauth-authorization-server or /.well-known/openid-configuration
- Must include: authorization_endpoint, token_endpoint, registration_endpoint, code_challenge_methods_supported (must include S256)
- Resource parameter: ChatGPT appends resource= to auth/token requests, must copy to access token (aud claim)
- Token verification on every request: signature, issuer, expiration, audience, scope
- Redirect URIs:
  - Production: https://chatgpt.com/connector/oauth/{callback_id}
  - Review: https://platform.openai.com/apps-manage/oauth

### Metadata
- Logo: 64x64px (light + dark mode versions)
- Up to 4 screenshots (no ChatGPT prompts in them)
- Video demo required (web + Android + iOS)
- Privacy policy URL mandatory
- Terms of service URL
- Category (12 options)
- Multi-language support (English mandatory)
- Country allowlist/blocklist available

### Review Process
- Submit via OpenAI Platform Dashboard
- 5 positive test cases (scenario, prompt, expected tool, expected output)
- 3 negative test cases (out-of-scope prompts app should NOT respond to)
- Test account: username/password, NO MFA, NO SMS codes, works outside company network
- One version in review at a time
- Contact press@openai.com before press releases

### Business Requirements
- Developer verification (individual or business) via Platform Dashboard
- Must have Owner role in organization
- EU data residency projects cannot submit

### Content Policy
- Suitable for ages 13+
- PROHIBITED: adult content, gambling, drugs, weapons, counterfeit goods, malware, surveillance, ads, digital product upsells
- Cannot collect PCI, PHI, government IDs, access credentials
- Cannot scrape external sites without authorization
- Apps must be complete (no trials/demos)

### Legal
- Grant OpenAI license to display branding
- OpenAI can remove at any time without notice
- Must provide customer support contact

---

## Key Differences

| Aspect | Anthropic | OpenAI |
|--------|-----------|--------|
| OAuth | 2.0 | 2.1 + PKCE (S256 mandatory) |
| DCR | Not mentioned | Mandatory |
| Resource Metadata | Not required | Required (RFC 9728) |
| Domain Verification | Not required | Required (.well-known) |
| Tool Annotations | readOnlyHint, destructiveHint | + openWorldHint |
| Test Cases | 3 examples | 5 positive + 3 negative |
| Logo | Auto-pulled favicon | 64x64 upload |
| Video Demo | Not required | Required |
| Financial Transactions | Prohibited | Digital products prohibited |

---

## Our Auth Strategy: Passkeys Inside OAuth

OAuth is the protocol Claude/ChatGPT use to talk to us (required by both directories). But inside the OAuth redirect, OUR login page uses passkeys (Face ID / QR code). No email/password.

User flow:
1. Click "Connect Memory Crystal" in Claude/ChatGPT
2. OAuth redirect to our auth page
3. Our page: "Sign in with passkey" + QR code
4. Scan with iPhone, Face ID, done
5. Redirect back. Connected.

No passwords. Ever. OAuth is the plumbing. Passkeys are the experience.

---

Sources:
- Anthropic Remote MCP Server Submission Guide: https://support.claude.com/en/articles/12922490
- Anthropic Connectors Directory FAQ: https://support.claude.com/en/articles/11596036
- Anthropic Software Directory Policy: https://support.claude.com/en/articles/13145358
- Anthropic MCP Directory Terms: https://support.claude.com/en/articles/11697081
- OpenAI Submit and maintain your app: https://developers.openai.com/apps-sdk/deploy/submission
- OpenAI App submission guidelines: https://developers.openai.com/apps-sdk/app-submission-guidelines
- OpenAI Building MCP servers: https://developers.openai.com/api/docs/mcp
- OpenAI Authentication (Apps SDK): https://developers.openai.com/apps-sdk/build/auth
- OpenAI UI Guidelines: https://developers.openai.com/apps-sdk/concepts/ui-guidelines

Compiled April 1, 2026.
