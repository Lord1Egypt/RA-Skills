---
name: skillguard
description: "使用场景: 用户要求审计第三方 Agent Skill 或进行安装前安全扫描时。"
license: MIT-0
metadata:
    {
        "packageVersion": "1.7.0",
        "openclaw": {
            "emoji": "🛡️",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "SKILLGUARD_API_KEY",
            "envVars": [
                {
                    "name": "AI_SKILLS_API_KEY",
                    "required": false,
                    "description": "通用平台 Key；与产品专用变量任选其一。"
                },
                {
                    "name": "SKILLGUARD_API_KEY",
                    "required": false,
                    "description": "兼容产品专用 Key；设置时优先使用。"
                }
            ]
        }
    }
---

# SkillGuard

## Skill 简介

SkillGuard 用于在安装第三方 Agent Skill 前审计其 SKILL.md、脚本和参考文件，识别提示词注入、敏感数据访问、危险命令及供应链风险，并提供可解释的风险结论。

## 平台入口与注册

1. 打开 [AI Skills 平台](https://ai-skills.open-idea.net/)，新用户可直接进入 [注册页面](https://ai-skills.open-idea.net/register)，已有账号进入 [登录页面](https://ai-skills.open-idea.net/login)。
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

兼容旧配置：如需隔离本产品，可改用 `openclaw config set env.SKILLGUARD_API_KEY "你的平台APIKey"`，然后重启 Gateway。调用时优先读取 `SKILLGUARD_API_KEY`，为空时读取 `AI_SKILLS_API_KEY`；两者均缺失时停止调用并引导创建密钥。不要输出、记录或要求用户在对话中粘贴完整密钥。


## 完成标准

- 在用户已授权范围内完成请求并检查实际响应；多文件任务逐项说明完成、失败和未处理部分，不把缺失或无法解析的结果视为成功。
- 错误按 HTTP-REQUESTS.md 与 BEHAVIOR-RULES.md 处理；超出重试预算或需要用户补充材料时，说明阻塞原因与下一步。

## 参考资料

按当前任务读取对应资料；无需预读全部文档。

- 首次配置或排查鉴权时：[API 密钥配置](https://ai-skills.open-idea.net/skill-docs/skillguard/API-KEY.md)
- 提交审计材料与解释风险时：[审计工作流](https://ai-skills.open-idea.net/skill-docs/skillguard/AUDIT-WORKFLOW.md)
- 调用 API 前，确认请求、响应与重试规则：[HTTP 请求与响应](https://ai-skills.open-idea.net/skill-docs/skillguard/HTTP-REQUESTS.md)
- 执行前，确认本次授权、安全与结果解释边界：[行为、错误与决策规则](https://ai-skills.open-idea.net/skill-docs/skillguard/BEHAVIOR-RULES.md)
