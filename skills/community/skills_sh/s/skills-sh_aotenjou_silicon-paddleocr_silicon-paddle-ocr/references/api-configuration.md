# API Configuration

## SiliconFlow API

This skill uses the SiliconFlow API for OCR operations.

### API Endpoint

```
https://api.siliconflow.cn/v1
```

### Authentication

Use the SILICONFLOW_API_KEY environment variable:
```bash
export SILICONFLOW_API_KEY="sk-xxxxxxxxxxxxx"
```

### Default Model

```
PaddlePaddle/PaddleOCR-VL-1.5
```

### Supported Models

- `PaddlePaddle/PaddleOCR-VL-1.5` (default)
- Other multilingual VL models compatible with the API

### Rate Limits

- Requests per minute: 60 (configurable)
- Max concurrent requests: 5

### API Response Format

The API returns a chat completion JSON with the recognized text in the message content.
