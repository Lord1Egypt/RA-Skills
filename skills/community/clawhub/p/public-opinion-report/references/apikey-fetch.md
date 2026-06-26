# Midu API Key Setup Guide (OpenClaw)

## Midu_API_KEY Not Configured

When the `Midu_API_KEY` environment variable is not set, follow these steps:

### 1. Get API Key

- Use the GET method 
- Visit **http://intra-znjs-yqt-agent-wx-beta.midu.cc/apiKey** with the following HTTP headers: {"podName": "public-opinion-report-skill-user", "podNameSpace": "beta-nlp"}

### 2. Configure OpenClaw
Edit the OpenClaw configuration file: `~/.openclaw/openclaw.json`

Add or merge the following structure:

```json
{
  "skills": {
    "entries": {
      "public-opinion-report": {
        "env": {
          "MIDU_API_KEY": "your_actual_api_key_here"
        }
      }
    }
  }
}
```

Replace `"your_actual_api_key_here"` with your actual API key.

### 3. Verify Configuration
```bash
# Check JSON format
cat ~/.openclaw/openclaw.json | python -m json.tool
```

### 4. Restart OpenClaw
```bash
openclaw gateway restart
```

### 5. Test
```bash
cd ~/.openclaw/workspace/skills/baidu-search
python3 skills/public-opinion-report/scripts/report.py '{"message": "编写法国旅游的快评"}'
```

## Troubleshooting
- Ensure `~/.openclaw/openclaw.json` exists with correct JSON format
- Timeout: Report generation may be slow; the script uses a longer timeout for /api/chat
- Restart OpenClaw after configuration changes

**Recommended**: Use OpenClaw configuration file for centralized management