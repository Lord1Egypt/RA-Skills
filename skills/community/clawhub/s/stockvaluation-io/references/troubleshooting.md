# Troubleshooting

## Useful Commands

Check container state:

```bash
docker compose -f docker-compose.local.yml ps
```

Tail logs:

```bash
docker compose -f docker-compose.local.yml logs -f valuation-service
docker compose -f docker-compose.local.yml logs -f valuation-agent
docker compose -f docker-compose.local.yml logs -f bullbeargpt
docker compose -f docker-compose.local.yml logs -f yfinance
```

Stop and clean up:

```bash
docker compose -f docker-compose.local.yml down
```

Reset local volumes only when the user explicitly wants to wipe local state:

```bash
docker compose -f docker-compose.local.yml down -v
```

## Common Issues

### Missing Environment Variables

Symptom:

- A service exits immediately on startup
- Compose errors mention `is required`

Fix:

- Recheck `.env.example`
- Fill the required key in `.env`
- Restart the stack

### CORS Or Browser Errors

Symptom:

- UI loads but requests fail with `403` or browser CORS errors

Fix:

- Verify `CORS_ORIGINS`
- Restart the affected services

### Weak Or Missing AI Output

Symptom:

- Research is sparse
- Narrative sections are weak or empty

Fix:

- Verify provider key validity, quota, and billing
- Add `TAVILY_API_KEY` if live research is expected
- Try a stronger model for the agent role

### Valuation Timeouts

Symptom:

- Long waits or request timeouts during analysis

Fix:

- Increase `VALUATION_SERVICE_TIMEOUT_SECONDS`
- Check `valuation-agent` and `valuation-service` logs
- Re-run with a single ticker and stable provider settings

### Installer Problems

Symptom:

- The one-line installer fails

Fix:

- Fall back to the manual Docker path from `{baseDir}/references/setup-and-run.md`
- If the failure is in the installer itself, inspect `install.sh` in the repo and rerun locally
- Avoid switching back to a remote `curl | bash` flow
