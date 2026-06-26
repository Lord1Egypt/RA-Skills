# Security Policy

## Reporting a Vulnerability

QA Pilot is a methodology document, not executable software. However, if you find issues with the approach that could lead to problems (e.g., testing patterns that might expose sensitive data), please:

1. **Do not** open a public issue
2. Email [helal-muneer](https://github.com/helal-muneer) directly via GitHub
3. Include a description of the concern and suggested fix

## Best Practices for Agents

When using QA Pilot, agents should:

- **Never test against production systems** without explicit permission
- **Avoid submitting real user data** in test forms
- **Use test credentials**, never real ones
- **Respect rate limits** and server resources during testing
- **Clean up test data** after testing is complete
