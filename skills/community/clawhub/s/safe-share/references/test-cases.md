# Representative Test Cases

Use these examples to smoke-test the skill after edits.

## GitHub Issue Example

Input:

```text
POST /v1/chat/completions
Authorization: Bearer super-secret-token
OPENAI_API_KEY=sk-examplesecret123456789
Contact: dev@example.com
```

Expected:

- Replace the bearer token
- Replace the OpenAI key
- Replace the email
- Keep the request shape readable

## README Example

Input:

```text
Set OPENAI_API_KEY=sk-examplesecret123456789 in your .env file.
Then call https://api.example.com/build?token=raw-demo-token&id=42
```

Expected:

- Replace the env value
- Replace the query token
- Preserve the rest of the example

## Chat Paste Example

Input:

```text
Cookie: sessionid=abc123def456
server ip: 10.1.2.3
call me at +1 (415) 555-0199
```

Expected:

- Replace cookie contents
- Replace the IP address
- Replace the phone number

## False-Positive Guardrails

Input:

```text
Build id: 8f4a8f4a
SHA256: 9f86d081884c7d659a2feaa0c55ad015
Path: C:\temp\tokenizer\notes.txt
```

Expected:

- Do not replace ordinary IDs, hashes, or file paths without sensitive context
