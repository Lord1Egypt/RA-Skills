# Volcengine Configuration Guide

Detailed configuration options for Volcano Engine integration with OpenClaw.

## Authentication Methods

### 1. API Key Authentication (Recommended)

**Step 1: Get API Key**
1. Log in to [Volcano Engine Console](https://console.volcengine.com/ark)
2. Go to **Access Management** → **Access Keys**
3. Click **Create Access Key**
4. Copy the key (starts with `sk-`)

**Step 2: Configure OpenClaw**

```bash
# Interactive setup
openclaw onboard --auth-choice volcengine-api-key
```

Or manually in `openclaw.json`:

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "volcengine": {
        "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
        "api": "openai-completions",
        "apiKey": "your-api-key-here"
      },
      "volcengine-plan": {
        "baseUrl": "https://ark.cn-beijing.volces.com/api/coding/v3", 
        "api": "openai-completions",
        "apiKey": "your-api-key-here"
      }
    }
  }
}
```

### 2. Environment Variable (Secure)

```bash
# Set in shell profile
export VOLCANO_ENGINE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Reference in config
"apiKey": "VOLCANO_ENGINE_API_KEY"
```

### 3. .env File

Create `~/.openclaw/.env`:

```env
VOLCANO_ENGINE_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Complete Configuration Example

```json
{
  "meta": {
    "lastTouchedVersion": "2026.4.9",
    "lastTouchedAt": "2026-04-12T14:00:00.000Z"
  },
  "models": {
    "mode": "merge",
    "providers": {
      "volcengine": {
        "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
        "api": "openai-completions",
        "apiKey": "VOLCANO_ENGINE_API_KEY",
        "models": [
          {
            "id": "doubao-seed-1-8-251228",
            "name": "Doubao Seed 1.8",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 256000,
            "maxTokens": 8192
          },
          {
            "id": "glm-4-7-251222",
            "name": "GLM 4.7",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 200000,
            "maxTokens": 8192
          },
          {
            "id": "kimi-k2-5-260127",
            "name": "Kimi K2.5",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 256000,
            "maxTokens": 8192
          }
        ]
      },
      "volcengine-plan": {
        "baseUrl": "https://ark.cn-beijing.volces.com/api/coding/v3",
        "api": "openai-completions",
        "apiKey": "VOLCANO_ENGINE_API_KEY",
        "models": [
          {
            "id": "ark-code-latest",
            "name": "Ark Coding Plan",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 256000,
            "maxTokens": 8192
          },
          {
            "id": "kimi-k2-thinking",
            "name": "Kimi K2 Thinking",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 256000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "volcengine/doubao-seed-1-8-251228"
      },
      "models": {
        "volcengine/doubao-seed-1-8-251228": {
          "alias": "Doubao"
        },
        "volcengine/glm-4-7-251222": {
          "alias": "GLM4"
        },
        "volcengine-plan/ark-code-latest": {
          "alias": "ArkCode"
        },
        "volcengine-plan/kimi-k2-thinking": {
          "alias": "KimiThink"
        }
      },
      "workspace": "C:\\Users\\Andapeng\\.openclaw\\workspace",
      "compaction": {
        "mode": "safeguard"
      }
    }
  },
  "env": {
    "VOLCANO_ENGINE_API_KEY": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  }
}
```

## Region Configuration

Volcano Engine supports two verified API regions:

| Region | General Endpoint | Verified |
|--------|-----------------|----------|
| **Beijing** (default) | `ark.cn-beijing.volces.com/api/v3` | ✅ 115 models |
| **Shanghai** | `ark.cn-shanghai.volces.com/api/v3` | ✅ 115 models (same as Beijing) |

> **Note**: These are the only two regions validated as of 2026-04-25. Candidates like Guangzhou, Shenzhen, Hangzhou, Hong Kong, Singapore, and US West were tested and did not resolve. Both regions expose identical models (115 total).

To change region, update `baseUrl` in provider config:

```json
{
  "volcengine": {
    "baseUrl": "https://ark.cn-shanghai.volces.com/api/v3",
    // ... rest of config
  }
}
```

### Script: Apply Regional Config

Use the helper script to switch regions:

```powershell
# Switch to Shanghai (faster for eastern China)
pwsh ./scripts/regional-config.ps1 -Region Shanghai

# Switch back to Beijing (default)
pwsh ./scripts/regional-config.ps1 -Region Beijing
```

## Model Aliases Best Practices

### Recommended Aliases

```json
{
  "agents": {
    "defaults": {
      "models": {
        "volcengine/doubao-seed-1-8-251228": {
          "alias": "Doubao"
        },
        "volcengine/glm-4-7-251222": {
          "alias": "GLM4"
        },
        "volcengine/kimi-k2-5-260127": {
          "alias": "Kimi"
        },
        "volcengine/deepseek-v3-2-251201": {
          "alias": "DeepSeekVE"
        },
        "volcengine-plan/ark-code-latest": {
          "alias": "ArkCode"
        },
        "volcengine-plan/kimi-k2-thinking": {
          "alias": "KimiThink"
        }
      }
    }
  }
}
```

### Alias Naming Conventions

- Keep aliases short but descriptive
- Include provider hint if needed (e.g., `DeepSeekVE` vs `DeepSeek`)
- Use consistent casing (CamelCase recommended)
- Avoid special characters

## Cost Configuration

Configure token costs for accurate usage tracking:

```json
{
  "models": [
    {
      "id": "doubao-seed-1-8-251228",
      "cost": {
        "input": 0.000002,  // $ per token
        "output": 0.000008,  // $ per token
        "cacheRead": 0.000001,
        "cacheWrite": 0.000001
      }
    }
  ]
}
```

**Current pricing** (check official site for updates):
- Doubao: ~$0.002/1K input tokens, $0.008/1K output tokens
- GLM-4: ~$0.0015/1K input tokens, $0.006/1K output tokens
- DeepSeek: ~$0.001/1K input tokens, $0.004/1K output tokens

**Reasoning Tokens**: For models that support thinking chains (like Kimi K2 Thinking), reasoning tokens may be billed separately. Check the official pricing page for current rates.

## Advanced Settings

### Custom Headers

```json
{
  "volcengine": {
    "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
    "api": "openai-completions",
    "apiKey": "VOLCANO_ENGINE_API_KEY",
    "headers": {
      "X-Custom-Header": "value",
      "User-Agent": "OpenClaw/2026.4.9"
    }
  }
}
```

### Timeout Configuration

```json
{
  "volcengine": {
    "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
    "timeout": 30000,  // milliseconds
    "connectTimeout": 10000,
    "readTimeout": 30000
  }
}
```

### Streaming Configuration

For long responses, use streaming to receive data incrementally:

```json
{
  "volcengine": {
    "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
    "stream": true  // Enable streaming responses
  }
}
```

**Streaming Benefits**:
- Reduced latency for long responses
- Memory efficient for large outputs
- Better user experience with progressive display

**Usage with OpenClaw CLI**:
```bash
openclaw --model Doubao --stream "Generate a long story"
```

### Retry Configuration

```json
{
  "volcengine": {
    "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
    "retry": {
      "maxAttempts": 3,
      "baseDelay": 1000,
      "maxDelay": 10000
    }
  }
}
```

## Testing Configuration

### Validate Config

```bash
# Validate openclaw.json
openclaw config validate

# Test connection
openclaw models list --provider volcengine
```

### Quick Test Script

Create `test-volcengine.ps1`:

```powershell
$apiKey = $env:VOLCANO_ENGINE_API_KEY
if (-not $apiKey) {
    Write-Error "Set VOLCANO_ENGINE_API_KEY environment variable"
    exit 1
}

$url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

$body = @{
    model = "doubao-seed-1-8-251228"
    messages = @(@{role = "user"; content = "Hello, test"})
    max_tokens = 50
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body
    Write-Host "✅ Connection successful"
    Write-Host "Response: $($response.choices[0].message.content)"
} catch {
    Write-Error "❌ Connection failed: $_"
}
```

## Migration from Other Providers

### From OpenAI

1. Change baseUrl from `api.openai.com/v1` to `ark.cn-beijing.volces.com/api/v3`
2. Update API key
3. Adjust model IDs
4. Update cost configuration

### From Azure OpenAI

1. Change authentication method to API key
2. Update endpoint
3. Remove Azure-specific headers
4. Update model naming convention

## Security Considerations

### API Key Protection

1. **Never commit keys** to version control
2. Use environment variables or secret management
3. Rotate keys periodically (every 90 days recommended)
4. Restrict key permissions to minimum required

### API Quotas and Limits

Based on official Volcano Engine documentation:

1. **API Key Quotas**:
   - Each main account supports up to **50 API Keys**
   - Additional quotas require submitting a support ticket
   - API Keys are counted per account, not per project

2. **Permission Control**:
   - API Keys can be restricted to specific **Model IDs**
   - API Keys can be limited to specific **IP addresses**
   - Keys created in one project space cannot access resources in other projects

3. **Project Space Isolation**:
   - API Keys are created within specific project spaces
   - Keys only have access to resources (models and applications) within that project
   - **Important**: API Keys do NOT support cross-project access
   - If you migrate endpoints between projects, existing API Keys will become invalid

4. **Rate Limiting**:
   - Implement exponential backoff for rate limit errors
   - Monitor usage through Volcano Engine Console
   - Set up alerts for quota approaching limits

### API Key Management Best Practices

1. **Quota Awareness**:
   - Monitor your API key count (max 50 per account)
   - Delete unused keys to free up quota
   - Request additional quota via support ticket if needed

2. **Permission Granularity**:
   - Restrict keys to specific Model IDs for security
   - Use IP whitelisting for production environments
   - Create separate keys for different applications

3. **Project Space Management**:
   - Ensure API keys are created in the correct project
   - Note that keys cannot access resources across projects
   - Plan project structure to avoid cross-project access needs

4. **Key Rotation**:
   - Rotate keys periodically (every 90 days recommended)
   - Update all configurations when rotating keys
   - Monitor for any disruptions during rotation

### Network Security

1. Verify SSL certificate validity
2. Use HTTPS only
3. Consider network segmentation for production
4. Monitor for unusual access patterns

### Audit Logging

Enable logging in `openclaw.json`:

```json
{
  "logging": {
    "level": "info",
    "providers": {
      "volcengine": "debug"
    }
  }
}
```

## Error Handling

### Common Error Codes

Based on official API documentation:

#### 400 Bad Request

| Error Code | Description | Solution |
|------------|-------------|----------|
| `MissingParameter.{{Parameter}}` | Required parameter is missing | Check request parameters |
| `InvalidParameter.{{Parameter}}` | Parameter value is invalid | Validate parameter values |
| `SensitiveContent.Detected.SevereViolation` | Input may contain severe violation | Use different prompt |
| `SensitiveContent.Detected.Violence` | Input may contain violence info | Use different prompt |
| `InputTextSensitiveContentDetected` | Input text contains sensitive info | Modify input content |
| `InputImageSensitiveContentDetected` | Input image contains sensitive info | Use different image |
| `OutputTextSensitiveContentDetected` | Output may contain sensitive info | Modify input to get different output |

#### 429 Too Many Requests

| Error Code | Description | Solution |
|------------|-------------|----------|
| `ModelAccountRpmRateLimitExceeded` | Exceeded RPM (Requests Per Minute) limit | Implement backoff, reduce request rate |
| `ModelAccountTpmRateLimitExceeded` | Exceeded TPM (Tokens Per Minute) limit | Reduce token usage or upgrade plan |
| `ModelAccountIpmRateLimitExceeded` | Exceeded IPM (Images Per Minute) limit | Reduce image requests |
| `QuotaExceeded` | Free trial quota exhausted | Upgrade to paid plan |

#### 401/403 Authentication

| Error Code | Description | Solution |
|------------|-------------|----------|
| `Unauthorized` | Invalid or missing API key | Verify API key |
| `AccessDenied` | Insufficient permissions | Check project access and IP restrictions |
| `Forbidden` | Resource access denied | Ensure key has required permissions |

### Best Practices for Error Handling

1. **Implement retry logic** for transient errors (429, 500, 502, 503, 504)
2. **Log detailed error information** for debugging
3. **Set up monitoring** for error rate thresholds
4. **Provide user-friendly error messages** based on error codes
5. **Validate inputs** before sending requests to avoid 400 errors

## Troubleshooting Configuration

### Common Issues

| Issue | Solution |
|-------|----------|
| "Invalid API key" | Verify key format, check permissions |
| "Endpoint not found" | Check baseUrl, verify region |
| "Model not available" | Check model ID, verify region support |
| "Rate limit exceeded" | Check quotas, implement backoff |
| "SSL certificate error" | Update CA certificates, check system time |
| "Cross-project access denied" | Ensure API key was created in the same project as the resource |

### Debug Mode

Enable debug logging:

```bash
openclaw --log-level debug gateway start
```

Check logs for detailed error messages:

```bash
Get-Content "$env:TEMP\openclaw\openclaw-$(Get-Date -Format 'yyyy-MM-dd').log" -Tail 100
```
