---
name: report-generation
description: "使用场景: 用户要求从 CSV/XLSX 生成可核验指标、图表、经营解读和多格式报告时。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.2.0",
        "openclaw": {
            "emoji": "📊",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "REPORT_GENERATION_API_KEY",
            "requires": {
                "bins": ["curl"]
            },
            "envVars": [
                {
                    "name": "AI_SKILLS_API_KEY",
                    "required": false,
                    "description": "通用平台 Key；与产品专用变量任选其一。"
                },
                {
                    "name": "REPORT_GENERATION_API_KEY",
                    "required": false,
                    "description": "AI Skills 平台经营报告 API 密钥。"
                },
                {
                    "name": "AI_SKILLS_API_URL",
                    "required": false,
                    "description": "可选 API 根地址。"
                }
            ]
        }
    }
---

# 经营报告生成

## Skill 简介

经营报告生成 Skill 从 CSV/XLSX 确定性计算指标和图表，再让模型仅解释已验证的 `metric_id`。任何数值不一致都会阻断模型解读；模型不可用时仍可返回明确标记的确定性部分，并可导出 Markdown、XLSX、PNG 与 PDF。

## 平台入口与注册

1. 打开 [AI Skills 平台](https://ai-skills.open-idea.net/)，新用户进入 [注册页面](https://ai-skills.open-idea.net/register)，已有账号进入 [登录页面](https://ai-skills.open-idea.net/login)。
2. 登录后进入 [产品管理](https://ai-skills.open-idea.net/dashboard/products) 开通本 Skill，再到 [API 密钥管理](https://ai-skills.open-idea.net/dashboard/keys) 创建密钥。

## Skill 安装与配置

当前控制台直接创建通用 Key，无需选择产品；每个账号最多保留一把未撤销的通用 Key，已有时直接复制复用，更换时先撤销旧 Key。下列产品选择说明适用于旧版控制台。

1. 在 [API 密钥管理](https://ai-skills.open-idea.net/dashboard/keys)中选择已开通的产品，创建并复制 API 密钥。
2. 在 OpenClaw 中安装本 Skill。
3. 将复制的密钥配置到本 Skill 的 API 密钥环境变量，然后重启 Gateway：

```sh
openclaw config set env.AI_SKILLS_API_KEY "你的平台APIKey"
openclaw gateway restart
```

推荐创建账号通用 Key，以上全局变量只需配置一次即可供各 Skill 使用；仍需在产品管理中开通目标产品。原有产品专用 Key 仅能调用对应产品。

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.REPORT_GENERATION_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `REPORT_GENERATION_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## Agent 执行规则

1. 依次执行 `report.inspect`（检查报表数据）、`report.generate`（生成经营报告）、按需执行 `report.export`（导出经营报告）。
2. `column_mappings` 必须显式映射源字段；`metric_requests` 指定指标，筛选和图表最多使用平台允许的结构，不把自然语言当作可执行公式。
3. 所有展示数字以平台确定性指标为准；不得让模型新增数字、修改指标或让图表引用不存在的 `metric_id`。
4. `partial` 表示只有确定性部分可交付，不得伪装为完整模型解读。

## 完成标准

- 异步任务轮询到终态；网络不确定时复用原 `Idempotency-Key` 和完全相同输入。
- 交付时列出数据范围、字段映射、指标、筛选、图表、数值校验状态与限制。
- 导出格式限 `markdown`、`xlsx`、`png`、`pdf`；私有 `artifacts` 只交付当前用户。

## 参考资料

按当前任务读取对应资料；无需预读全部文档。

- [API 密钥配置与价格](https://ai-skills.open-idea.net/skill-docs/report-generation/API-KEY.md)
- [HTTP 请求、上传与任务轮询](https://ai-skills.open-idea.net/skill-docs/report-generation/HTTP-REQUESTS.md)
- [操作字段、指标与导出](https://ai-skills.open-idea.net/skill-docs/report-generation/OPERATIONS.md)
- [数值校验、安全与解释边界](https://ai-skills.open-idea.net/skill-docs/report-generation/BEHAVIOR-RULES.md)
