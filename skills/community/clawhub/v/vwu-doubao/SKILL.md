# doubao Models for vwu.ai

vwu.ai 平台上的 doubao 模型调用技能。

## 支持的模型

- doubao-1-5-pro-32k
- doubao-seed-1-6-flash
- doubao-seed-1-6-lite
- doubao-seed-1-8
- doubao-seed-2-0-pro
- doubao-seedance-1-5-pro-251215
- doubao-seedream-4-5-251128

共 7 个模型。

## 配置

使用前需要设置 vwu.ai API key:

```bash
export VWU_API_KEY="your-key-here"
```

获取 key: https://vwu.ai 控制台

## 使用示例

```bash
# 调用模型
vwu-chat --model doubao-1-5-pro-32k "你的问题"
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
