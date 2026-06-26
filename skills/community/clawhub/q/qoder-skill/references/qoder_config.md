# Qoder Configuration Reference

## Environment Variables

### Required
- `QODER_API_KEY`: Your Alibaba Cloud API key for Qoder service
- `QODER_ENDPOINT`: API endpoint URL (default: https://dashscope.aliyuncs.com/api/v1)

### Optional  
- `QODER_MODEL`: Default model to use (default: qwen-max)
- `QODER_TIMEOUT`: Request timeout in seconds (default: 300)
- `QODER_MAX_TOKENS`: Maximum tokens for response (default: 4096)

## Configuration File

Qoder can also read from a configuration file at `~/.qoder/config.yaml`:

```yaml
api_key: "your-api-key-here"
endpoint: "https://dashscope.aliyuncs.com/api/v1"
model: "qwen-max"
timeout: 300
max_tokens: 4096
workspace: "~/projects"
```

## Model Options

### Coding Models
- `qwen-coder-plus`: Optimized for code generation and understanding
- `qwen-coder-max`: Highest performance coding model
- `qwen-max`: General purpose with strong coding capabilities

### General Models  
- `qwen-plus`: Balanced performance and cost
- `qwen-turbo`: Fast and economical for simple tasks

## Rate Limits

- **QPM (Queries Per Minute)**: Varies by subscription plan
- **TPM (Tokens Per Minute)**: Check your DashScope console for limits
- **Daily Quota**: Monitor usage in Alibaba Cloud console

## Error Handling

Common error codes and solutions:

- `401 Unauthorized`: Check API key validity
- `429 Too Many Requests`: Implement rate limiting or upgrade plan  
- `500 Internal Server Error`: Retry with exponential backoff
- `400 Bad Request`: Validate input format and parameters