---
name: md-to-pdf
description: 报告输出自动转PDF。当向用户发送Markdown报告文件时，自动转换为PDF后再发送，确保微信和飞书用户可以直接查看。
metadata:
  {
    "openclaw": {
      "emoji": "📄"
    }
  }
---

# 报告输出自动转 PDF

当向用户发送 Markdown 报告时，自动转换为 PDF 格式，确保在微信、飞书等平台可以直接查看。

## 适用场景

- 通过飞书/微信向用户发送 .md 报告文件时
- 用户明确要求发送 PDF 时
- 渠道不支持 Markdown 渲染时（微信、飞书等）

## 执行规则

### 判断是否需要转 PDF

| 渠道 | 是否转PDF |
|---|---|
| 微信 (openclaw-weixin) | ✅ 总是转 |
| 飞书 (feishu) | ✅ 总是转 |
| Discord | ❌ 可以直接发 md 文件 |
| Telegram | ❌ Telegram 支持 Markdown 渲染 |

### 转换命令

```bash
export PATH="$HOME/.homebrew/bin:$PATH" && npx -y md-to-pdf@latest <输入文件.md> --pdf-options '{"format":"A4","margin":{"top":"20mm","bottom":"20mm","left":"15mm","right":"15mm"}}'
```

输出文件与输入文件同目录，扩展名 `.pdf`。

### 发送流程

1. 确认报告 .md 文件已生成
2. 执行 md-to-pdf 转换
3. 确认 .pdf 文件已生成（检查文件大小 > 0）
4. 通过当前渠道发送 .pdf 文件
5. 可选：同时发送一句简要说明（报告标题、核心结论）

### 失败处理

如果转换失败，降级为：
1. 发送原始 .md 文件
2. 告知用户"PDF转换失败，已发送原始文件"

## 注意事项

- md-to-pdf 首次运行会自动安装，耗时约5-10秒
- 中文内容需要系统有中文字体（macOS 默认有 PingFang SC）
- 如果报告中有复杂的表格或代码块，PDF 排版可能不完美，必要时可手动调整
- PDF 文件与 MD 文件放在同一目录，方便管理
