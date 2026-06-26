# API 配置

## 环境变量

脚本从以下环境变量读取 API keys：

| API | 环境变量 | 端点 | 模型 |
|-----|---------|------|------|
| ModelScope | `NOVEL_MODELSCOPE_KEY` | https://api-inference.modelscope.cn/v1/chat/completions | deepseek-ai/DeepSeek-V3.2 |
| Fyra | `NOVEL_FYRA_KEY` | https://Fyra.im/v1/chat/completions | mistral-large-3-675b-instruct |
| Ph8 | `NOVEL_PH8_KEY` | https://ph8.co/v1/chat/completions | qwen3-235b-a22b-2507 |

至少设置一个。用户文本会发送到以上端点。

## 调用策略

1. 默认顺序：ModelScope → Fyra → Ph8
2. 429 限流：自动等 30 秒重试
3. 失败：自动切下一个 API
4. 未配置 key 的 API 自动跳过

## 示例

```bash
export NOVEL_MODELSCOPE_KEY="ms-xxxxxxxxx"
python3 scripts/batch_generate.py --outline outline.json --start 1 --end 10 --output chapters/
```
