---
name: unraid-xml-generator
description: |
  Generate Unraid DockerMan user template XML files from structured input.

  Use when: the user asks to "生成 Unraid XML 模板", "创建 Docker 模板",
  "为 XXX 写 Unraid 模板", or "生成 DockerMan XML" for any container.

  Key technique learned (2026-04-02):
    Unraid DockerMan templates support <ExtraParams>--entrypoint /bin/sh</ExtraParams>
    + <PostArgs> to bypass the container image's ENTRYPOINT. This allows
    overriding any image's startup command from the template.

  Config variables use: <Config Name="..." Target="ENV_VAR" Default="..." Type="..." Display="..." Required="..." Mask="...">
    These become environment variables passed into the container.

  The skill generates a complete, valid XML and optionally deploys it to
  /boot/config/plugins/dockerMan/templates-user/my-<name>.xml
  (requires user confirmation before writing).
---

# Unraid XML Generator

## Core Pattern

The key insight for Unraid Docker templates:

```xml
<Container version="2">
  <Name>mycontainer</Name>
  <Repository>image:tag</Repository>
  <Network>bridge</Network>

  <!-- KEY: override ENTRYPOINT to /bin/sh -->
  <ExtraParams>--entrypoint /bin/sh</ExtraParams>

  <!-- KEY: pass real startup command through shell -ec -->
  <PostArgs>-ec 'real startup command here'</PostArgs>

  <!-- User-configurable variables -->
  <Config Name="Display Name" Target="ENV_VAR" Default="..." Type="Variable" Display="always" Required="false" Mask="true">default_value</Config>
  <Config Name="Port" Target="PORT" Default="8080" Mode="tcp" Type="Port" Display="always" Required="true">8080</Config>
  <Config Name="Data Path" Target="/data" Default="/mnt/user/appdata/mycontainer" Mode="rw" Type="Path" Display="always" Required="true">/mnt/user/appdata/mycontainer</Config>
</Container>
```

## Template Field Reference

| Field | Purpose |
|-------|---------|
| `<Name>` | Unique container identifier |
| `<Repository>` | Docker image with tag |
| `<Registry>` | Registry URL (optional, informational) |
| `<Network>` | Network mode: `bridge`, `host`, `none` |
| `<Shell>` | Default shell (`bash` / `sh`) |
| `<ExtraParams>` | Extra docker run flags (e.g. `--entrypoint /bin/sh`) |
| `<PostArgs>` | Startup command passed to shell `-ec` |
| `<WebUI>` | Format: `http://[IP]:[PORT:nnnn]/` — shows button in Unraid UI |
| `<Icon>` | URL to icon image |
| `<Category>` | Unraid category string |
| `<Config>` | User-configurable parameter |

## Config Types

| Type | Example |
|------|---------|
| `Variable` | Environment variable (`Target` = env var name) |
| `Port` | Port mapping (`Mode="tcp"/"udp"`) |
| `Path` | Volume path (`Mode="rw"/"ro"`) |
| `Slider` | Numeric slider (requires `Min`, `Max`, `Step`) |
| `Description` | Read-only description text |

## Config Display Options

| Display value | When shown |
|----------------|-----------|
| `always` | Always visible in UI |
| `advanced` | Hidden behind "Advanced" toggle |
| `hidden` | Never shown (manual config) |

## Masked Variables (secrets)

Set `Mask="true"` on `Type="Variable"` Config entries to:
- Hide the value from the UI (shown as `••••••`)
- Treat as sensitive (API keys, tokens, passwords)

## PostArgs Shell Pattern

```bash
# Correct way to write PostArgs in XML:
<PostArgs>-ec 'export VAR1="value1" && export VAR2="value2" && exec real_command --flag arg'</PostArgs>

# Breaking down:
# -e  : exit on error
# -c  : read command from string (not stdin)
# '...' : single-quoted command string
```

## Standard Config Variables to Include

For any container:

```xml
<Config Name="HTTP Proxy" Target="HTTP_PROXY" Default="" Type="Variable" Display="advanced" Required="false" Mask="false">http://192.168.8.30:7893</Config>
<Config Name="HTTPS Proxy" Target="HTTPS_PROXY" Default="" Type="Variable" Display="advanced" Required="false" Mask="false">http://192.168.8.30:7893</Config>
<Config Name="NO Proxy" Target="NO_PROXY" Default="" Type="Variable" Display="advanced" Required="false" Mask="false">localhost,127.0.0.1,192.168.0.0/16</Config>
<Config Name="TZ" Target="TZ" Default="Asia/Shanghai" Type="Variable" Display="advanced" Required="false" Mask="false">Asia/Shanghai</Config>
```

## Script Usage

```bash
python3 scripts/generate_template.py \
  --name opencode \
  --image ghcr.io/anomalyco/opencode:latest \
  --port 4096 \
  --web-port 4097 \
  --output /tmp/opencode.xml

# Generate with all standard env vars:
python3 scripts/generate_template.py \
  --name opencode \
  --image ghcr.io/anomalyco/opencode:latest \
  --port 4096 \
  --web-port 4097 \
  --proxy 192.168.8.30:7893 \
  --tz Asia/Shanghai \
  --output /tmp/opencode.xml
```

## Common Pitfalls

1. **Double quotes in PostArgs** → escape as `&quot;` in XML
2. **ENTRYPOINT bypass** → always use `<ExtraParams>--entrypoint /bin/sh</ExtraParams>`
3. **Shell variable substitution** → use single quotes for PostArgs to prevent `$VAR` expansion by XML parser
4. **Template filename** → must start with `my-` and end with `.xml`
5. **Path permissions** → Unraid runs containers as PUID/PGID = 99/100 by default

## Output

The generated XML file is placed at:
```
/boot/config/plugins/dockerMan/templates-user/my-<name>.xml
```

User must confirm before deploying (writing) to that path.
