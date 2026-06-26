# Skywork API Key Setup Guide

## SKYWORK_API_KEY Not Configured

When the `SKYWORK_API_KEY` environment variable is not set, follow these steps:

### 1. Get API Key

Visit the Skywork website and sign in to your account:

**https://skywork.ai**

- Log in with your Skywork account
- Open account / Settings / API Key (**https://skywork.ai/?openApiKeySetting=1**)
- Create or copy your **API key**

If your organization uses a separate console or test environment, use the URL and credentials your team provides.

### 2. Configure OpenClaw

Edit the OpenClaw configuration file: `~/.openclaw/openclaw.json`

In current OpenClaw, Skywork skills store the key under `skills.entries.<Skill Name>.apiKey` (not under `env`).
OpenClaw will inject this value into the skill's `SKYWORK_API_KEY` environment when `primaryEnv` matches.
Add or merge the following structure (adjust the skill name to match the installed skill):

```json
{
  "skills": {
    "entries": {
      "Skywork Search": {
        "enabled": true,
        "apiKey": "your_actual_skywork_api_key_here"
      }
    }
  }
}
```

Replace `"your_actual_skywork_api_key_here"` with your real key.

For multiple Skywork skills, repeat the same `apiKey` field on each skill entry.

### 3. Configure Claude Code

If you are using Claude Code, use one of these lightweight options:

**Option A — shell environment**

Export the API key before running the skill:

```bash
export SKYWORK_API_KEY="your_actual_skywork_api_key_here"
```

To persist it across sessions, add the same line to `~/.zshrc` or `~/.bashrc`, then reload the shell.

**Option B — Claude Code settings**

Add the variable to `~/.claude/settings.json`:

```json
{
  "env": {
    "SKYWORK_API_KEY": "your_actual_skywork_api_key_here"
  }
}
```

Use the method that best matches how you run Claude Code.

### 4. Verify Configuration

```bash
# Check that the environment variable is available
echo "$SKYWORK_API_KEY"
```

For OpenClaw, you can also validate the config file:

```bash
cat ~/.openclaw/openclaw.json | python3 -m json.tool
```

### 5. Restart OpenClaw

```bash
openclaw gateway restart
```

## Troubleshooting

- Ensure `~/.openclaw/openclaw.json` exists and is valid JSON
- Ensure `SKYWORK_API_KEY` is available in Claude Code through your shell or `~/.claude/settings.json`
- Confirm the API key is active and not expired
- Check Skywork account status, membership, or quota if requests fail with auth or benefit errors
- Restart OpenClaw after configuration changes

**Recommended**: Use the setup method that matches your runtime. OpenClaw should use the OpenClaw config file; Claude Code can use either the shell environment or `~/.claude/settings.json`.
