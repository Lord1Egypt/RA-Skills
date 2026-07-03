# Configuration — resolving ARK_API_KEY

The API key MUST be resolved before any request. Resolve it in this exact order
and stop at the first source that yields a non-empty value:

1. **Shell environment variable** `$ARK_API_KEY` (preferred — what the agent
   shell already exports).
2. **Env file** — source a dotenv-style file if present. Try these paths in
   order until one exists:
   - `$ARK_ENV_FILE` (explicit override, if set)
   - `~/.env_vars`
   - `/root/.env_vars`
3. If none of the above yields a non-empty `ARK_API_KEY`:
   - Do NOT make the API request.
   - Report to the user: *"ARK_API_KEY was not found. Set it via the
     ARK_API_KEY environment variable, or store it in ~/.env_vars as
     `ARK_API_KEY=...`."*

## Concrete resolution command

This logic is implemented in `scripts/resolve-key.sh`. The equivalent inline
form (run once per invocation):

```bash
: "${ARK_ENV_FILE:=}"
for f in "$ARK_ENV_FILE" "$HOME/.env_vars" "/root/.env_vars"; do
  [ -n "$f" ] && [ -f "$f" ] || continue
  set -a; . "$f"; set +a
  break
done
if [ -z "${ARK_API_KEY:-}" ]; then
  echo "ERROR: ARK_API_KEY not found" >&2; exit 1
fi
# Sanity check (do not print the value):
echo "ARK_API_KEY length: ${#ARK_API_KEY}"
```

## Example `~/.env_vars`

```
ARK_API_KEY=xxxxxxxxxxxxxxxx
```
