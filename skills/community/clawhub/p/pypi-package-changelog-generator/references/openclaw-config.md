# OpenClaw Config

Example `~/.openclaw/openclaw.json` snippet:

```json
{
  "skills": {
    "entries": {
      "pypi-package-changelog-generator": {
        "enabled": true,
        "apiKey": { "source": "env", "provider": "default", "id": "GITHUB_TOKEN" }
      }
    }
  }
}
```

You can also inject the token directly:

```json
{
  "skills": {
    "entries": {
      "pypi-package-changelog-generator": {
        "enabled": true,
        "env": {
          "GITHUB_TOKEN": "ghp_example"
        }
      }
    }
  }
}
```

Start a new OpenClaw session after changing the skill config so the refreshed skill snapshot is used.

## Network Proxies

The Python wrapper inherits standard proxy environment variables from the host process:

- `HTTP_PROXY`
- `HTTPS_PROXY`
- `NO_PROXY`

If your OpenClaw gateway or agent runtime is behind a corporate proxy, set those environment variables on the host or inject them through the agent runtime so PyPI and GitHub requests use the expected outbound route.
