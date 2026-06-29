---
name: tcm-dietary
description: 中医食疗辨证 API 客户端。通过 HTTPS 调用 api.tcmplate.com 远端服务，提供体质辨证、食材属性查询、食疗方案推荐、茶饮配方检索。免费 10次/日，无需注册。这不是本地知识库，所有查询发送到远程服务器处理。仅供信息参考，不构成医疗建议。
version: 1.0.1
author: 饭去病
license: MIT-0
tags: [中医, 食疗, 辨证, 养生, 体质调理, 茶饮, API]
---

# tcm-dietary

**远程 API 客户端，不是本地知识库。** 所有查询通过 HTTPS 发送到 `api.tcmplate.com` 云端辨证引擎处理。免费 10 次/日，无需注册。

> [English docs](SKILL.md)

---

## 🔒 隐私与数据处理

**本 Skill 将你的查询内容（症状、体质类型、疾病名称、食材关键词）通过 HTTPS 发送至 api.tcmplate.com 云端处理。使用前请阅读本表。**

| 项目 | 说明 |
|------|------|
| 传输 | HTTPS 加密（TLS 1.2+） |
| 发送数据 | **仅症状描述/体质类型/疾病名称/食材名称。** 代码层字段白名单自动过滤意外传入的个人信息（姓名/身份证号/地址/电话号码等）——这些数据在客户端即被剥离，不会到达服务器 |
| 数据存储 | 查询内容（症状、关键词）仅在内存中处理，**不落盘**。不存在查询数据库 |
| 服务器日志 | IP 地址和时间戳保留在访问日志中，保留 **14 天**（用于限流和滥用防护）。查询内容**绝不写入日志** |
| 数据用途 | 仅用于当前请求的食疗建议生成。**不用于模型训练、分析、画像或任何二次用途** |
| 第三方共享 | **无。** 查询数据不与任何第三方共享、出售或披露 |
| 数据删除 | 由于查询内容不持久化存储，无可删除数据。访问日志（IP + 时间戳）14 天后自动过期 |
| 支付 | 付费订阅由 PayPal 独立处理，API 不接收也不存储支付卡信息 |
| 同意 | 使用本 Skill 即表示你已阅读本表，同意将查询数据通过 HTTPS 发送至 api.tcmplate.com 进行实时处理。**切勿在查询中包含姓名、身份证号、地址或电话号码** |

📧 隐私咨询 / 数据访问请求：privacy@tcmplate.com
📄 完整隐私政策：https://tcmplate.com/privacy

---

## ⚡ 零步开始（免费 10 次/日，无需 API Key）

> ⚠️ **注意：** 你的查询数据（症状、疾病、体质类型）将离开本地机器，通过 HTTPS 发送到 api.tcmplate.com 进行云端处理。切勿包含个人身份信息。请阅读上方[隐私与数据处理](#-隐私与数据处理)。

```bash
# 辨证诊断 — 症状通过 HTTPS 发送到 api.tcmplate.com
# ⚠️ 切勿在 symptoms 中包含姓名、身份证号、地址
curl -X POST https://api.tcmplate.com/api/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms":["口干","失眠","心烦"]}'

# 知识检索 — 关键词通过 HTTPS 发送到 api.tcmplate.com
curl -X POST https://api.tcmplate.com/api/search \
  -H "Content-Type: application/json" \
  -d '{"category":"ingredients","keywords":["生姜"]}'
```

每个 IP 每日 10 次免费额度。超额返回 429。

---

## Python 客户端

```python
import sys; sys.path.insert(0, "path/to/tcm-dietary")
from core.diagnose import diagnose
from core.search import search

# 免费：无需 API Key
result = diagnose(["失眠", "心悸", "食欲不振"])

# 付费：$5/月 不限次数
# core.set_api_key("tcm_xxxx")
```

本客户端将所有查询通过 HTTPS 发送到 `api.tcmplate.com`。请勿在查询中包含个人信息。

---

## API 端点

| 端点 | 免费 | 说明 |
|------|:--:|------|
| `/api/diagnose` | ✅ | 症状辨证 → 证型 + 食疗方案 |
| `/api/search` | ✅ | 9 个知识库全文检索 |
| `/api/health` | ✅ | 健康检查 |

### 定价

| 方案 | 额度 | 价格 |
|------|------|------|
| 免费 | 10 次/日 | $0 |
| 付费 | 不限 | $5/月 |

📖 文档：https://tcmplate.com/docs
🛒 订阅：https://api.tcmplate.com/subscribe

---

## ⚠️ 免责声明

**本 Skill 为信息参考工具，不提供医疗服务。**

- 所有输出仅供学习和信息参考，不构成医疗诊断、处方或治疗建议
- 如有健康问题，请咨询执业医师
- 本 Skill 是远程 API 客户端，你传入的症候描述将通过网络发送到 api.tcmplate.com 进行处理
- 请勿在查询中包含姓名、身份证号、住址等个人身份信息
- 使用本 Skill 即表示你已阅读并同意上述隐私与数据处理条款
