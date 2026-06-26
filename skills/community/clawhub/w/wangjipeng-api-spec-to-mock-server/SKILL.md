---
name: api-spec-to-mock-server
description: >
  Use when (1) user provides API spec in OpenAPI or Swagger format and needs a runnable mock server. 
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# Api Spec To Mock Server

Use when (1) user provides API spec in OpenAPI or Swagger format and needs a runnable mock server. 

## Core Position

This skill solves the specific engineering problem of: *user provides API spec in OpenAPI or Swagger format and needs a runnable mock server*

This skill is NOT:
- A general-purpose capability that activates on anything
- A replacement for manual human judgment
- A tool that stores state or remembers across sessions

This skill IS activated ONLY when the trigger conditions are explicitly met.

## Modes

### `/api-spec-to-mock-server`

**Default mode.** Performs the core task end-to-end.

When to use: User provides input matching the trigger conditions above.


## Execution Steps

1. **Receive API spec** — User provides an API specification document
   - Accepted formats: OpenAPI 3.x, Swagger 2.x, raw API description text
   - If the input is not recognizable as an API spec, state: "This skill generates a runnable mock server from an API specification (OpenAPI/Swagger). Please provide an API spec document."

2. **Parse spec structure** — Extract the API contract:
   - Identify all endpoints (paths) and their HTTP methods (GET, POST, PUT, DELETE)
   - Extract request/response schemas and parameter definitions
   - Note authentication requirements, headers, and content types
   - Identify response status codes and example payloads

3. **Generate mock server** — Create a runnable server with the spec:
   - Use a common mock server library (e.g., Prism, Mockoon, or a simple Express/Flask server)
   - Generate endpoint handlers that return realistic mock responses
   - Implement request validation matching the spec
   - Serve the mock server on a configurable port (default: 8080)

4. **Test endpoints** — Verify the mock server behaves correctly:
   - Run a smoke test against the generated endpoints
   - Confirm response status codes match the spec
   - Verify content-type headers are correctly set

5. **Deliver with run instructions** — Provide the server code and usage:
   - State how to start the server (command + port)
   - Provide example curl requests for key endpoints
   - Note any configuration needed (base URL, auth tokens)
   - Offer to adjust response payloads or add custom scenarios

## Mandatory Rules

### Do not

- Do not make up facts or claim actions were taken that were not
- Do not hardcode API keys — use `os.getenv("API_KEY")` instead
- Do not store sensitive user data beyond the current session
- Do not exceed token budget without warning the user first
- Do not activate for off-topic requests — return a brief decline message

### Do

- Validate all inputs before acting
- Handle errors gracefully with actionable error messages
- Log actions taken for auditability
- State explicitly when you are uncertain or data is insufficient

## Quality Bar

**A good output:**
- Solves exactly the problem described in the trigger conditions
- Provides actionable result in the expected format within 3 turns
- Handles error cases with specific guidance, not generic "try again"
- States assumptions explicitly when input is ambiguous

**A bad output:**
- Solves a different problem than the one triggered
- Provides a generic "I can't help with that" without explaining why
- Crashes, hangs, or returns malformed output on valid input
- Activates for off-topic requests (false positive)

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| Trigger matched | "I can help with that." + no action | Correct transformation delivered in structured format |
| Invalid input | Crash or wrong result | "Missing required field: [X]. Please provide [Y]." |
| Ambiguous input | Guesses and might be wrong | States assumption and asks for confirmation |
| Off-topic request | Attempts to help anyway | "This skill activates when [trigger]. Please restate your request." |

## References

- `references/` — Detailed templates, schemas, and edge-case rules for this skill
