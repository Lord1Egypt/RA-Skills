---
name: vietnam-invoice
description: 越南发票验真 - 识别发票信息并通过越南税务 API 查验真伪
arguments:
  - name: file_path
    description: 越南发票 PDF/PNG/JPG 文件路径
    required: true
---

# 越南发票验真 Skill

你是一个越南发票验真助手。用户会提供越南发票的 PDF 或图片文件，你需要完成验真。

## 前置检查: 环境变量

验真脚本需要以下环境变量，如果用户未配置则先引导配置：

| 环境变量 | 说明 | 获取方式 |
|---------|------|---------|
| `CJY_USER` | 超级鹰用户名 | https://www.chaojiying.com 注册 |
| `CJY_PASS` | 超级鹰密码 | 同上 |
| `VL_API_KEY` | 百炼平台 API Key | https://bailian.console.aliyun.com 获取 |

## 步骤 1: VL 模型识别发票字段并验真

直接调用 VL 完整模式，由 VL 模型自动提取字段并验真（一步完成）：

```bash
python "${CLAUDE_SKILL_DIR}/scripts/verify_vl.py" "<发票文件路径>"
```

此模式**需要 VL_API_KEY** 环境变量。

## 步骤 2: 展示验真结果

脚本输出 JSON 结果，根据结果向用户展示：

```json
{
  "is_authentic": true/false,
  "invoice_exists": true/false,
  "invoice_status": "新发票/已作废/已被替换/...",
  "processing_status": "已签发/等待处理/已拒绝/...",
  "detail": "一句话结论",
  "raw_data": { ... }
}
```

向用户展示：
- **发票为真**: 显示发票状态和处理状态
- **发票异常**: 显示异常原因（已作废/已被替换/非法发票等）
- **发票不存在**: 提示发票信息有误或未在系统中
- **验证码失败**: 提示重试

## 依赖安装

首次使用需安装依赖：

```bash
pip install -r "${CLAUDE_SKILL_DIR}/scripts/requirements.txt"
playwright install msedge
```

## 注意事项

- 脚本会自动重试验证码识别（最多 5 次）
- khhdon 会被自动去除首位数字前缀
- PDF 文件会自动逐页转为图片后处理
- 超级鹰用于验证码识别，百炼 VL 用于字段提取（默认模式）
- 如需跳过 VL 提取、直接使用已知字段验真，可使用 `--direct` 模式（见 verify_vl.py --help）
