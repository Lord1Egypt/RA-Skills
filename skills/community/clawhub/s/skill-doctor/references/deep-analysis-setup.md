# Deep Analysis Setup (Optional)

`--deep` adds a short AI-narrated summary on top of the rule-based
diagnostics. This is entirely optional — the core check-up works fully
without it.

## What Gets Sent

Only a compact JSON summary per skill/plugin:

```json
{
  "key": "proof-of-contribution",
  "status": "healthy",
  "vitals": {
    "downloads": 73,
    "installs_all_time": 3,
    "active_installs": 1,
    "stars": 0,
    "verdict": "clean"
  },
  "findings": ["..."]
}
```

**Never sent**: API keys, tokens, raw `clawhub inspect` payloads, file
contents, or anything beyond the metrics already computed locally.

## Configuration

Add your Anthropic API key to `~/.skill-doctor/config.json`:

```json
{
  "slugs": ["your-skill-slug"],
  "plugins": ["@you/your-plugin"],
  "anthropic_api_key": "sk-ant-..."
}
```

Get a key from [console.anthropic.com](https://console.anthropic.com).

## Cost

Each `--deep` run is a single API call with a small prompt (~400 max output
tokens). For a typical portfolio of 5-10 items this costs a fraction of a
cent per check-up. Skill Doctor does not loop or retry on failure — one
call per run, fails silently with a warning if the request errors out.

## Disabling

Either omit `--deep` from the command, or set `"anthropic_api_key": null`
in the config. Skill Doctor checks for a configured key before attempting
any network call and skips cleanly if absent.

## Security Notes

- Store the key only in `~/.skill-doctor/config.json`, which is created
  with default user-only permissions by the OS. Do not commit this file to
  any repository.
- If you rotate or revoke the key, just update the config — no other state
  needs to change.
- The deep analysis step uses `urllib` from the Python standard library —
  no third-party HTTP dependency required for this feature.
