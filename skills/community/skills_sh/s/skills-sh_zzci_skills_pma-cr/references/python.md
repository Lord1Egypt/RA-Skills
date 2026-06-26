# Python Review Pack

Apply this pack to Python services, CLIs, libraries, and async applications.

## Focus Areas

### Input validation and trust boundaries

- All external input should be validated at the edge: request bodies, query params, headers, webhook payloads, queue messages.
- Prefer schema validation (Pydantic, marshmallow, attrs) over ad hoc field checks.
- Do not trust deserialized data from pickles, YAML `load()`, or `eval()`/`exec()` on user input.

### Query and command safety

- User input must not be interpolated into SQL, shell commands, or filesystem paths.
- Use parameterized queries for all database access.
- Use `subprocess` with list arguments, never `shell=True` with user-controlled input.
- Watch for path traversal via `os.path.join` with absolute user input.

### Auth and permissions

- Authentication is not authorization.
- State-changing endpoints need explicit permission checks.
- Decorator-based auth should be verified on every new route, not assumed by convention.

### Async correctness

- Blocking I/O in async functions starves the event loop.
- Fire-and-forget tasks (`asyncio.create_task` without holding the reference) lose errors silently.
- Outbound HTTP should have timeout configuration.
- Watch for mixing sync and async database drivers incorrectly.

### Error handling

- Bare `except:` or `except Exception:` that swallows errors silently is a defect.
- Avoid returning `None` as an implicit error signal when the caller cannot distinguish it from a valid result.
- Do not log secrets, tokens, or raw credentials in exception handlers.

### Type safety

- New code should use type hints for function signatures.
- `Any` should not be used to silence type errors on well-typed boundaries.
- Optional fields need explicit `None` handling, not implicit attribute access.

### Dead code and stale modules

- Look for modules, views, management commands, or Celery tasks with no remaining registrations or callers.
- Stale feature flags and superseded migration paths often leave dead write paths behind.
- Beware of false positives from dynamic imports, decorator-based registration, and Django URL autodiscovery.

## High-Signal Findings

Report issues such as:

- `pickle.loads` or `yaml.load` on untrusted input
- string-formatted SQL or shell commands
- missing permission checks on new write endpoints
- blocking I/O inside async handlers
- bare exception swallowing with no logging or re-raise
- unbounded queries without pagination or limits
- orphan views, tasks, or management commands with no remaining callers

## Usually Skip

- PEP 8 style nits already enforced by formatters (black, ruff)
- personal preferences on project structure
- broad "add type hints everywhere" on unchanged legacy code
- code that only looks unused because of dynamic registration or framework autodiscovery

## Source Notes

- OWASP Input Validation Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP SQL Injection Prevention Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- OWASP OS Command Injection Defense Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
- OWASP Deserialization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html
- Bandit security linter: https://bandit.readthedocs.io/en/latest/
- mypy documentation: https://mypy.readthedocs.io/en/stable/
