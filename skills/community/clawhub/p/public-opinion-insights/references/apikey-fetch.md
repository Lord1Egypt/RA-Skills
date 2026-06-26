# Midu API Key Setup Guide (OpenClaw) — Public Opinion Insights

## MIDU_API_KEY Not Configured

当未设置 `MIDU_API_KEY` 环境变量时，按以下步骤操作。

### 1. Get API Key

- 使用 **GET** 方法
- 访问 **http://intra-znjs-yqt-agent-wx-beta.midu.cc/apiKey**，HTTP 请求头：`{"podName": "public-opinion-insights-skill-user", "podNameSpace": "beta-nlp"}`

### 2. Configure OpenClaw

编辑 OpenClaw 配置文件：`~/.openclaw/openclaw.json`

添加或合并：

```json
{
  "skills": {
    "entries": {
      "public-opinion-insights": {
        "env": {
          "MIDU_API_KEY": "your_actual_api_key_here"
        }
      }
    }
  }
}
```

将 `your_actual_api_key_here` 替换为真实 Key。

### 3. Verify Configuration

```bash
cat ~/.openclaw/openclaw.json | python -m json.tool
```

### 4. Restart OpenClaw

```bash
openclaw gateway restart
```

## Troubleshooting

- 确认 `~/.openclaw/openclaw.json` 存在且 JSON 合法
- 超时：分析可能较慢；脚本对 `/api/chat` 使用较长超时
- 修改配置后需重启 OpenClaw

**建议**：通过 OpenClaw 配置文件统一管理各技能的 `MIDU_API_KEY`。

可在 `message` 中点名的**分析维度完整清单**见 [analysis_dimension.md](analysis_dimension.md)。
