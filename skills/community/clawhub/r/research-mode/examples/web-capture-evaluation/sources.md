# Sources

This example favors official or primary references for safety-relevant claims.

## Primary References

- [RFC 9309: Robots Exclusion Protocol](https://datatracker.ietf.org/doc/html/rfc9309) - robots.txt coordination, matching, redirects, caching, and the distinction between crawler politeness and access control.
- [RFC 9110: HTTP Semantics](https://datatracker.ietf.org/doc/html/rfc9110) - safe methods, redirects, Location handling, and user-agent guidance.
- [Python `urllib.parse` documentation](https://docs.python.org/3/library/urllib.parse.html) - URL parsing behavior and the warning that security-sensitive URL handling requires defensive validation.
- [OWASP Server-Side Request Forgery Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) - risks and controls for URL-controlled server-side fetches, allowlists, parser issues, and network-layer containment.
- [OWASP LLM Prompt Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) - guidance for treating external content as untrusted input and screening model-driven actions.
- [CommonMark Spec 0.31.2](https://spec.commonmark.org/0.31.2/) - Markdown syntax, including raw HTML constructs that matter when Markdown might be rendered.

## Illustrative Converter Reference

- [Microsoft MarkItDown repository](https://github.com/microsoft/markitdown) - an example of a document-to-Markdown converter used for text analysis workflows. It is illustrative, not a required dependency for this example.

## How These Sources Are Used

- HTTP and redirect behavior: RFC 9110.
- Robots and crawler politeness: RFC 9309.
- URL parsing and validation caution: Python documentation and OWASP SSRF guidance.
- Prompt-injection handling: OWASP LLM guidance.
- Markdown safety boundaries: CommonMark and converter documentation.
