# Security

Use for a changed trust boundary, authentication, permissions, untrusted input or secrets. Review the specific path being changed; do not audit an unrelated application by default.

## Identify the failure to prevent

List the protected asset, who can influence the input, where authority changes and how the new path could be abused. Connect each material threat to a control and a check. A short PR note is enough when it captures the decision; reuse an existing threat model when one exists. For a new trust boundary, the short method in [threat modeling](threat-modeling.md) helps.

## Controls that must survive

| Boundary | Check |
|---|---|
| Object or tenant access | Enforce authorization server-side for the requested object. Test another owner's identifier, not just an unauthenticated request. Deny access if the policy check fails. |
| SQL or shell | Bind values or pass an argument list. Validate identifiers separately; escaping a shell string is not the default design. |
| HTML, files or exports | Use contextual encoding or a maintained sanitizer. Resolve paths within the authorized root, accounting for symlinks. Constrain upload size/type and prevent spreadsheet formula execution from untrusted cells. |
| Server-side URL fetch | Restrict destinations, validate resolved addresses and redirects, and prevent DNS rebinding. Do not let arbitrary input reach internal or metadata endpoints. |
| Serialized objects | Use data-only decoding and explicit allowed types. Do not deserialize untrusted input with pickle, unsafe YAML loaders, BinaryFormatter or unrestricted type activation. |
| Secrets | Use the existing secret store and least-privilege identity. Redact diagnostics. Revoke an exposed credential; removing its text does not revoke it. |

Test business operations against the [abuse cases](threat-modeling.md#abuse-cases), such as skipped or reordered steps. Assign owner, role, price and entitlement from authoritative server state; arbitrary client fields must not overwrite them. Bound expensive work reachable through cheap requests.

## Sign-in and sessions

Use a maintained identity library. For OpenID Connect, verify the installed library's authorization-code/PKCE setup, exact redirect URI matching, request correlation and ID-token validation: signature, allowed algorithm, issuer, audience, expiry and nonce when used. Decide how accounts link; an email claim alone is not a safe account-linking policy.

For sessions, preserve secure cookie settings, CSRF protection, session renewal at login/privilege changes and server-side expiry/revocation. A signed cookie can still expose its contents. Keep password policy and hashing parameters aligned with the project's current security requirements and the linked NIST/OWASP guidance rather than copying old defaults.

Use established cryptography and framework protections. Before adding blanket security headers or replacing an authentication system, identify the integrations it affects, such as embedded pages, third-party scripts, single sign-on and API clients, and check each one against the planned change. Replacing an authentication system is hard to undo, so get the user's confirmation before that step unless the request already covers it. Preserve existing access until the replacement has been verified within the authorized change.

## Verify the boundary

Exercise denial, malformed input and dependency failure, as well as the successful path. For outbound calls, test disallowed destinations and redirect handling. For state-changing operations, test the caller's authority and replay/concurrency behavior. Record an unresolved material exposure before release.

## Sources

- [OWASP authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [OWASP deserialization](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html)
- [OWASP business logic](https://cheatsheetseries.owasp.org/cheatsheets/Business_Logic_Security_Cheat_Sheet.html)
- [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST authentication guidance](https://pages.nist.gov/800-63-4/sp800-63b.html)
- [OAuth security, RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html)
- [OpenID Connect token validation](https://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation)
