# 多模型配置示例

## 豆包模型（默认）
```bash
$env:VIDEO_ANALYZER_API_KEY="你的豆包API密钥"
$env:VIDEO_ANALYZER_MODEL="doubao-seed-2-0-pro-260215"
$env:VIDEO_ANALYZER_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"
```

## 智谱 GLM-4V
```bash
$env:VIDEO_ANALYZER_API_KEY="你的智谱API密钥"
$env:VIDEO_ANALYZER_MODEL="glm-4v-plus"
$env:VIDEO_ANALYZER_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
```

## 通义千问 VL
```bash
$env:VIDEO_ANALYZER_API_KEY="你的通义API密钥"
$env:VIDEO_ANALYZER_MODEL="qwen-vl-plus"
$env:VIDEO_ANALYZER_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

## 注意事项
1. API Key 请勿泄露到公开仓库
2. 不同模型的输入格式可能略有差异，如遇到问题请提交 Issue
3. 建议先用免费额度测试，确认模型兼容性后再批量使用
