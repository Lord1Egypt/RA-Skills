---
name: load-env
description: >-
  How to load environment variables from .env files into a Harper application
  using the loadEnv plugin.
metadata:
  mode: generate
  sources:
    - reference/v5/environment-variables/overview.md
  sourceCommit: 42231db17c025a4a455e3d91875fad4084a01cb5
  inputHash: fe610fc245226357
---

# Load Environment Variables with loadEnv

Instructions for the agent to follow when loading environment variables from `.env` files into a Harper application using the `loadEnv` plugin.

## When to Use

Apply this rule when a Harper application needs to load secrets or configuration values from `.env` files into `process.env` at startup. Use it whenever hardcoding values must be avoided and environment-specific configuration must be supplied to Harper components.

## How It Works

1. **Declare `loadEnv` in `config.yaml`**: Add `loadEnv` as a top-level key. It is built into Harper and requires no installation.

   ```yaml
   loadEnv:
     files: '.env'
   ```

2. **Place `loadEnv` first**: Always list `loadEnv` before any other components in `config.yaml` so that environment variables are available on `process.env` before dependent components start.

   ```yaml
   # config.yaml — loadEnv must come first
   loadEnv:
     files: '.env'

   rest: true

   myApp:
     files: './src/*.js'
   ```

3. **Configure the `files` option**: Provide one or more paths or glob patterns pointing to the env files to load. This option is required.

4. **Set `override` if needed**: By default, existing environment variables take precedence over values in `.env` files. Set `override: true` to reverse this and have loaded values win.

   ```yaml
   loadEnv:
     files: '.env'
     override: true
   ```

5. **Load multiple files when required**: Supply a list of files or a glob pattern. Files are loaded in the order specified.
   ```yaml
   loadEnv:
     files:
       - '.env'
       - '.env.local'
   ```
   or
   ```yaml
   loadEnv:
     files: 'env-vars/*'
   ```

### Configuration Options

| Option     | Type                 | Required | Description                                                                            |
| ---------- | -------------------- | -------- | -------------------------------------------------------------------------------------- |
| `files`    | `string \| string[]` | **Yes**  | Path(s) or glob pattern(s) to the env file(s) to load.                                 |
| `override` | `boolean`            | No       | If `true`, loaded values override existing environment variables. Defaults to `false`. |

## Examples

**Minimal setup — single `.env` file:**

```yaml
loadEnv:
  files: '.env'
```

**Full `config.yaml` with load order, multiple files, and override:**

```yaml
# config.yaml — loadEnv must come first
loadEnv:
  files:
    - '.env'
    - '.env.local'
  override: true

rest: true

myApp:
  files: './src/*.js'
```

**Glob pattern:**

```yaml
loadEnv:
  files: 'env-vars/*'
```

## Notes

- `loadEnv` is built into Harper — do not install it separately; only declare it in `config.yaml`.
- Because Harper is a single-process application, variables loaded onto `process.env` are shared across all components.
- Without `override: true`, variables already set in the shell or container environment will not be overwritten by values in `.env` files.
- `files` is the only required option; omitting it will produce an invalid configuration.
