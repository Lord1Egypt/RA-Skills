# TypeScript Backend Review Pack

Apply this pack to Node.js and Bun server code, APIs, jobs, workers, and data-access layers.

## Focus Areas

### Validation and trust boundaries

- All external input should be validated at the edge: body, params, query, headers, webhook payloads, queue messages.
- Prefer schema validation and typed parsing over ad hoc field checks.
- Allowlisting beats denylisting for constrained values.

### Query and command safety

- User input must not be interpolated into SQL, shell commands, or filesystem paths.
- Parameterization must happen server-side, not just in a client helper.
- Watch for unsafe child process usage with user-controlled arguments.

### Auth, authz, and multi-step writes

- Authentication is not authorization.
- State-changing endpoints need explicit permission checks.
- Multi-step writes should consider transactions, idempotency, and duplicate delivery behavior.

### Async correctness

- Floating promises are real defects when they hide failures or reorder side effects.
- Misused async callbacks in request handlers, event listeners, or array helpers often drop errors.
- Outbound HTTP should usually have timeout or cancellation behavior.
- Detached background work needs clear ownership and failure handling.

### Data and operations

- New list endpoints should be paginated or bounded.
- Avoid N+1 query patterns in hot paths.
- Avoid logging secrets, tokens, full credentials, or raw sensitive payloads.
- Review error responses for internal detail leakage.

### Dead code and abandoned backends

- Look for handlers, workers, cron jobs, queues, or repositories with no remaining registrations or callers.
- Stale feature flags and superseded migration paths often leave dead write paths behind.
- Treat dead auth or webhook handlers as higher-risk than ordinary unused helpers because they preserve stale boundary code.
- Beware of false positives from reflection-based registration, framework auto-discovery, and generated clients.

### Web security

- Cookie-auth flows need CSRF-aware design.
- CORS should be explicit, not wide open by accident.
- User-controlled outbound URLs can create SSRF paths.

## High-Signal Findings

Report issues such as:

- missing schema validation on new request input
- string-built SQL or shell commands
- permission checks missing on a new write path
- unbounded external call with no timeout or abort path
- dropped promise or async callback error path
- secret-bearing logs
- unbounded pagination or fan-out query explosion
- orphan API endpoint, worker, or migration path with no reachable registration

## Usually Skip

- generic "needs service layer" advice
- framework-preference arguments
- style-only complaints around handler structure
- exports that appear unused only because they are wired by framework discovery or metadata-based registration

## Source Notes

- `no-floating-promises`: https://typescript-eslint.io/rules/no-floating-promises/
- `no-misused-promises`: https://typescript-eslint.io/rules/no-misused-promises/
- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP SQL Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- OWASP Query Parameterization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html
- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- OWASP SSRF Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
- OWASP OS Command Injection Defense Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
- TypeScript `noUnusedLocals`: https://www.typescriptlang.org/tsconfig/noUnusedLocals.html
- TypeScript `allowUnreachableCode`: https://www.typescriptlang.org/tsconfig/allowUnreachableCode.html
- ESLint `no-unused-vars`: https://eslint.org/docs/latest/rules/no-unused-vars
