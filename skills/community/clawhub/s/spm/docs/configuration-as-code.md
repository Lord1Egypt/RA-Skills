# Configuration-as-Code — Externalizing Volatile Parameters

Configuration-as-Code means all tunable parameters live outside the codebase in declarative files (YAML/JSON), with typed accessors. This lets operators adjust behavior without rebuilding, A/B test different settings, and keep secrets out of source control.

---

## Why?

- **No code deploys for simple tweaks**: Change quality gate thresholds, heartbeat intervals, reviewer settings by editing a config file.
- **Environment-specific overrides**: `staging.yaml` can enable verbose logging; `production.yaml` holds real secrets (gitignored).
- **Validation and type safety**: Zod schema ensures config values are correct at startup.
- **Central source of truth**: No more "hard-coded 80" for coverage targets scattered in three files.

---

## Structure

```
your-project/
├── config/
│   ├── default.yaml        # Base configuration (committed)
│   ├── staging.yaml        # Staging overrides (gitignored or committed)
│   └── production.yaml     # Production overrides (gitignored)
├── src/config/
│   ├── index.ts            # Loader + get() helper
│   ├── schema.ts           # Zod validation schema
│   └── validators.ts       # Custom validation (if needed)
```

---

## The Default Config

Edit `config/default.yaml` to define your project's standard settings. The SPM-provided template covers:

- `project` (execution mode, parallel subagents)
- `quality` (gates enabled, coverage target, auto checkpoint)
- `tracking` (WBS ledger path, heartbeat interval)
- `review` (spec reviewer, quality reviewer)
- `deployment` (enabled, environment)
- `logging` (level, format)

Customize this file to your domain. Add new sections as needed; extend `ConfigSchema` in `src/config/schema.ts` accordingly.

```yaml
# Example SPM project config
project:
  execution_mode: subagent
  parallel_subagents: true
  max_parallel_subagents: 4

quality:
  gates_enabled: true
  coverage_target: 80
  auto_checkpoint: true

tracking:
  wbs_ledger_path: docs/spm/ledger.md
  heartbeat_interval: 10m

logging:
  level: info
  format: json
```

---

## Loading Configuration

In your application entry point:

```typescript
import { loadConfig, get } from './config';

// Load once at startup
const config = loadConfig(); // uses process.env.SPM_ENV or 'development'

// Access values
console.log('Execution mode:', get('project.execution_mode')); // 'subagent'
console.log('Coverage target:', get('quality.coverage_target')); // 80
```

### Environment Selection

```bash
export SPM_ENV=production
node dist/server.js

# Or via .env file
SPM_ENV=staging npm start
```

The loader merges: `default.yaml` < `{env}.yaml` < environment variables (`SPM_` prefix).

---

## Environment Variable Overrides

For secrets or per-deployment values, set environment variables with prefix `SPM_`:

| Config path | Env var name | Example |
|-------------|---------------|---------|
| `deployment.environment` | `SPM_DEPLOYMENT_ENVIRONMENT` | `production` |
| `quality.coverage_target` | `SPM_QUALITY_COVERAGE_TARGET` | `85` |
| `project.max_parallel_subagents` | `SPM_PROJECT_MAX_PARALLEL_SUBAGENTS` | `6` |

Dot notation converts to uppercase with underscores. The loader parses numeric and boolean strings automatically.

---

## Using Configuration in Code

```typescript
import { get, isProduction, isSubagentMode } from './config';

const COVERAGE_TARGET = get('quality.coverage_target');
const MAX_PARALLEL = get('project.max_parallel_subagents');

if (isProduction()) {
  // tighten validation rules
}

async function executeTask(task: Task) {
  if (isSubagentMode()) {
    return dispatchSubagent(task);
  }
  return executeInline(task);
}
```

---

## Validation

The `ConfigSchema` in `src/config/schema.ts` defines the shape. It uses Zod for runtime validation. On `loadConfig()`, the merged config is parsed against the schema; if invalid, the process exits with an error.

This catches:
- Missing required fields
- Wrong types (string instead of number)
- Out-of-range values (negative coverage targets)
- Invalid enumerations (unknown execution mode)

Extend the schema when you add custom config sections.

---

## Best Practices

1. **Keep defaults sensible**: The `default.yaml` should work for local development without overrides.
2. **Do not commit secrets**: Use environment variables for API keys, tokens, database URLs.
3. **Version your config schema**: If you make breaking changes to config structure, increment a `config_version` field and provide migration notes.
4. **Document each key**: Add comments in `default.yaml` explaining what each parameter does and its valid range.
5. **Share config between components**: Multiple services in a monorepo should reference the same config structure for consistency.

---

## Deployment Scenarios

### Locally

- Keep `config/default.yaml` committed.
- Use `SPM_ENV=development` (default).
- Override per-developer settings with a gitignored `config/local.yaml`.

### Docker / Kubernetes

- Mount config as a ConfigMap volume: `/app/config/default.yaml`
- Use `SPM_ENV=production` in container env
- Override with `config/production.yaml` in a secret volume if needed

### Monorepo with Multiple Services

If you have separate services, you can:
- Share the same `config/` directory via symlink or package
- Keep service-specific configs in subdirectories
- Use a common `src/config` package imported by all services

---

## Troubleshooting

**Q: `Config validation failed` on startup**  
A: Check the error message; likely a type mismatch in `config/default.yaml` or environment variable. Validate against `src/config/schema.ts`.

**Q: Config changes not taking effect**  
A: Ensure you restarted the service. Config is loaded once at startup; not hot-reloaded.

**Q: How to see effective config?**  
A: Add a debug endpoint or log `JSON.stringify(getAll(), null, 2)` at startup (but beware secrets). For production, mask sensitive fields.

**Q: Can I have nested overrides?**  
A: Currently one environment file (`{env}.yaml`) is supported. For complex overrides, use environment variables for fine-grained control.

---

## Next Steps

- Add `config/` and `src/config/` to your project
- Move hard-coded values from code into `default.yaml`
- Refactor code to use `get()` accessor
- Update `schema.ts` if you added custom sections
- Commit `config/default.yaml` (but not `*.yaml` with secrets)
