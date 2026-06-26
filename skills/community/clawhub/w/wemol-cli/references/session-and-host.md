# Session And Host

Use these commands first when runtime context is unclear.

## Check Host

```bash
wemol-cli host
```

Set host:

```bash
wemol-cli host --set https://wemol.wecomput.com
```

The CLI persists the current host and caches sessions per host.

One-off overrides for current invocation:

```bash
WEMOL_HOST=https://wemol.wecomput.com wemol-cli module search antibody
wemol-cli --host https://wemol.wecomput.com module search antibody
WEMOL_SESSION_ID=<session_id> wemol-cli job list
wemol-cli --session-id <session_id> job list
WEMOL_USER_AGENT=WeMol-CLI/1.0.0 wemol-cli module list
wemol-cli --user-agent WeMol-CLI/1.0.0 module list
```

Use these overrides for temporary routing/debugging. Prefer persisted `host --set` and cached login for routine work.

## Check Language

```bash
wemol-cli lang
```

Set language:

```bash
wemol-cli lang --set en
wemol-cli lang --set cn
```

`module get` and `module get --params-json` descriptions follow this language.

## Login

Interactive:

```bash
wemol-cli login
```

Non-interactive:

```bash
wemol-cli login --username alice --password secret
```

Do not mix the two modes. `--username` and `--password` must be provided together.

## Logout

```bash
wemol-cli logout
```

This clears the cached session and host-local cache for the current host.

## Account

```bash
wemol-cli account
```

Use this to inspect current account identity, token usage, and storage summary.

## Authentication Errors

If the CLI prints a message like:

```text
Authentication required for <host>. Run 'wemol-cli login'.
```

stop and log in before continuing.
