# openai Models for vwu.ai

vwu.ai 平台上的 openai 模型调用技能。

## 支持的模型

- gpt-4.1
- gpt-4o
- gpt-4o-2024-08-06
- gpt-4o-mini
- gpt-5-mini
- gpt-5.1
- gpt-5.1-chat
- gpt-5.2
- gpt-5.2-chat

共 9 个模型。

## 配置

使用前需要设置 vwu.ai API key:

```bash
export VWU_API_KEY="your-key-here"
```

获取 key: https://vwu.ai 控制台

## 使用示例

```bash
# 调用模型
vwu-chat --model gpt-4.1 "你的问题"
```

## API 兼容性

所有模型兼容 OpenAI API 格式，支持标准 chat completions 接口。

## 额度提示

如果使用时提示"额度不足"或类似错误：
1. 访问 https://vwu.ai
2. 在控制台充值或调整额度
3. 或生成新的 API key

---

由 Claw 自动生成 | 源数据: vwu.ai
