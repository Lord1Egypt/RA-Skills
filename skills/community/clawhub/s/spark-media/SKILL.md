---
name: spark-media
description: "使用场景: 用户明确希望通过 AI Skills 平台 API 生成或编辑图片、生成视频或查询媒体任务，或明确要求将本人已生成素材发布到小红书时。"
license: MIT-0
metadata:
    {
        "packageVersion": "2.11.1",
        "openclaw": {
            "emoji": "✨",
            "homepage": "https://ai-skills.open-idea.net",
            "primaryEnv": "SPARK_MEDIA_API_KEY",
            "envVars": [
                {
                    "name": "AI_SKILLS_API_KEY",
                    "required": false,
                    "description": "优先使用的通用平台 Key；旧产品变量仅作兼容兜底。"
                },
                {
                    "name": "SPARK_MEDIA_API_KEY",
                    "required": false,
                    "description": "兼容旧产品 Key；仅通用变量为空时使用。"
                }
            ]
        }
    }
---

# Spark 媒体

## Skill 简介

Spark Media 用于根据文字生成图片和视频、基于最多五张图片共同参考创作图片、最多九张图片共同参考创作视频，并查询媒体任务进度与结果，适合广告图、商品图、海报和短视频素材制作。用户明确要求时，可将本人已成功生成的图片或视频发布到自己绑定的小红书账号；发布默认私密，不额外收费。

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

兼容旧配置：仅配置 `openclaw config set env.SPARK_MEDIA_API_KEY "你的平台APIKey"` 的用户仍可使用，然后重启 Gateway。调用时优先读取 `AI_SKILLS_API_KEY`，为空时读取 `SPARK_MEDIA_API_KEY`；两者均缺失时停止调用并引导创建密钥。两者同时存在且值不同时，提示已采用通用变量，仅显示变量名，不显示密钥。401 时停止自动重试，不自动换 Key；迁移与排查按参考资料中的 API 密钥配置执行。不要输出、记录或要求用户在对话中粘贴完整密钥。


### 小红书账号配置（仅发布时需要）

1. 使用创建上述 API Key 的同一个平台账号登录[媒体工作台](https://ai-skills.open-idea.net/dashboard/products/spark-media?tab=image)，点击“管理小红书账号”。
2. 在浏览器中登录要发布的小红书账号，打开开发者工具的 Network（网络）面板并刷新页面。在发往小红书的请求中，找到 Request Headers（请求标头）里的 Cookie，复制包含 `a1` 和 `web_session` 的完整值。仅由用户粘贴到工作台的“账号 Cookie”输入框，不发送给 Agent，也不粘贴到聊天中。
3. 填写“账号备注（自定义）”（例如小红书昵称、公司官方号），点击“绑定账号”。显示“已绑定”和账号备注后即可使用；需要解除关联时点击“解绑账号”，Cookie 失效或切换账号时，先解绑，再填写新的 Cookie 重新绑定。

Cookie 由平台加密保存，不回显。OpenClaw 或其他 Agent 只需配置同一平台账号的 API Key，无需配置 `XHS_COOKIE`。用户要求发布时，Agent 先查询绑定状态；未绑定则引导用户按上述步骤操作，绑定后再继续。发布接口、授权核对与状态查询见[小红书发布说明](https://ai-skills.open-idea.net/skill-docs/spark-media/XIAOHONGSHU.md)。

## 完成标准

- 在用户已授权范围内完成请求；收到异步任务时持续轮询任务状态，按 HTTP-REQUESTS.md 的终态与等待上限停止。未规定上限时，开始轮询前设定有限等待预算；超时保留任务 ID、最后状态与查询方式，不宣称成功或失败、不重复提交。
- 429/503 等可恢复错误按参考规则有限退避；同一逻辑请求复用原 `Idempotency-Key` 和相同输入。结果不确定或规则要求人工核对时停止自动重试；已授权范围内的安全续查无需重复确认。
- 多文件或多步骤任务完成后逐项交付结果；部分失败、仍在处理或等待人工核对的项目分别说明，并给出下一步。

发布属于独立的外部操作，仅在用户明确要求时执行；生成或展示素材不自动授权发布。Cookie 仅由用户在登录后的工作台配置，不索取或在对话中转发。发布结果不确定时保留发布编号，停止自动重复提交并引导核对原笔记。

## 参考资料

按当前任务读取对应资料；无需预读全部文档。

- 首次配置或排查鉴权时：[API 密钥配置](https://ai-skills.open-idea.net/skill-docs/spark-media/API-KEY.md)
- 生成或编辑图片时：[图片生成与编辑](https://ai-skills.open-idea.net/skill-docs/spark-media/IMAGE-GENERATION.md)
- 生成视频或查询视频任务时：[视频生成与轮询](https://ai-skills.open-idea.net/skill-docs/spark-media/VIDEO-GENERATION.md)
- 明确要求发布到小红书时：[账号配置、发布与查询](https://ai-skills.open-idea.net/skill-docs/spark-media/XIAOHONGSHU.md)
- 调用 API 前，确认请求、响应与重试规则：[HTTP 请求示例](https://ai-skills.open-idea.net/skill-docs/spark-media/HTTP-REQUESTS.md)
- 执行前，确认本次授权、安全与结果解释边界：[行为、错误与重试规则](https://ai-skills.open-idea.net/skill-docs/spark-media/BEHAVIOR-RULES.md)
