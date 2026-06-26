---
title: Use Direct Indexing for Required Dictionary Keys
impact: CRITICAL
impactDescription: Ensures missing keys fail fast with KeyError instead of masking bugs
tags: error-handling, dictionaries, debugging, fail-fast, api-validation
---

## Use Direct Indexing for Required Dictionary Keys

**Impact: CRITICAL (Ensures missing keys fail fast with KeyError instead of masking bugs)**

Use `d[key]` for required dictionary keys instead of `dict.get(key)` to ensure missing keys fail fast with `KeyError`. When a dictionary key is required for correct program behavior, using `dict.get(key)` masks the missing key as `None`, causing errors to appear far from the root cause and making debugging harder.

**When to Use Direct Indexing `d[key]`:**
- The key must exist for the program to function correctly
- Missing keys indicate a bug in calling code
- Function parameters or API inputs that are mandatory
- Configuration values that are required for system operation

**When to Use `dict.get(key, default)`:**
- The key is genuinely optional with a meaningful fallback value
- Default values are valid and safe for operation
- User preferences or optional configuration settings

**Implementation Requirements:**
- Use direct indexing `d[key]` when the key must exist
- Validate required keys explicitly at API boundaries
- Use `dict.get(key, default)` only for genuinely optional keys with meaningful defaults
- Never use `.get()` to guess or mask missing required data

**Incorrect (Required keys masked as optional, causing delayed errors):**

```python
# user_service.py
def process_user_request(payload: dict):
    # Required key masked as optional
    user_id = payload.get("user_id")
    return create_user_session(user_id)  # None causes error later

# config_loader.py
def load_timeout_config(config: dict):
    # Required key with meaningless default
    timeout = config.get("timeout", 0)
    return setup_connection(timeout)  # 0 is not a valid timeout

# service_manager.py
def start_services(data: dict):
    # Chained logic hides failure
    if data.get("enabled"):
        port = data.get("port")  # None if missing
        start_service(port)  # Error occurs here, not at source

# api_handler.py
def handle_webhook(event: dict):
    # API boundary misuse
    event_type = event.get("type")
    process_event(event_type)  # None breaks processing
```

**Correct (Required keys fail fast, explicit validation):**

```python
# user_service.py
def process_user_request(payload: dict):
    # Required key, fail fast
    user_id = payload["user_id"]  # KeyError if missing
    return create_user_session(user_id)

# config_loader.py
def load_timeout_config(config: dict):
    # Explicit validation
    if "timeout" not in config:
        raise ValueError("Missing required 'timeout' config")
    timeout = config["timeout"]
    return setup_connection(timeout)

# service_manager.py
def start_services(data: dict):
    # Validate all required keys upfront
    if data.get("enabled"):  # Optional flag
        port = data["port"]  # Required when enabled
        start_service(port)

# api_handler.py
def handle_webhook(event: dict):
    # Explicit validation at boundary
    event_type = event["type"]  # Fail fast if missing
    process_event(event_type)

# settings.py
def load_user_preferences(config: dict):
    # Genuinely optional with meaningful default
    debug_mode = config.get("debug", False)
    theme = config.get("theme", "light")
    return UserPreferences(debug_mode, theme)
```
