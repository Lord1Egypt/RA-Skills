# Project Detection — Stack Fingerprinting

The agent MUST run this detection before any other step.

## Detection Rules (check in order)

| File/Signal | Stack | Recommended Path |
|---|---|---|
| `wp-content/` dir OR `wp-config.php` | WordPress | **xCloud Native** |
| `composer.json` + `artisan` file | Laravel | **xCloud Native** (or Docker if complex) |
| `composer.json` only | PHP Generic | **xCloud Native** (or Docker) |
| `package.json` + `next.config.js` or `next.config.ts` | Next.js | **Docker** (requires build step) |
| `package.json` + `nest-cli.json` | NestJS | **Docker** |
| `package.json` + `nuxt.config.*` | Nuxt.js | **Docker** |
| `package.json` only | Node.js / Express | **xCloud Native** (or Docker) |
| `requirements.txt` or `pyproject.toml` | Python | **Docker** |
| `go.mod` | Go | **Docker** |
| `Cargo.toml` | Rust | **Docker** |
| `docker-compose.yml` exists | Existing Docker stack | **Adapt** → run Scenario A/B/C detection |
| `Dockerfile` exists (no compose) | Build-from-source | **Generate** docker-compose.yml → Scenario A |
| None of the above | Unknown | Ask user for stack type |

## Output

After detection, state:
```
Detected: [STACK]
Recommended deployment path: [Native / Docker]
Reason: [one sentence]
```

Then read the appropriate reference file:
- Native WordPress → `references/xcloud-native-wordpress.md`
- Native Laravel → `references/xcloud-native-laravel.md`
- Native Node.js → `references/xcloud-native-nodejs.md`
- Native PHP → `references/xcloud-native-php.md`
- Docker → proceed with existing Scenario A/B/C logic from SKILL.md
- Generate Dockerfile → read `dockerfiles/` templates
