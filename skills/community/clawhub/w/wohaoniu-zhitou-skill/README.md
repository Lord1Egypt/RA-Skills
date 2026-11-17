# 我好牛AI智投 · WorkBuddy Skill

让 WorkBuddy / Claw 系 Agent 直接使用 [我好牛AI智投](https://ai.wohaoniu.com) 的能力:

- **品牌 AI 可见度探测(GEO)**:你的品牌会不会被 DeepSeek/通义/豆包/Kimi/文心 推荐?(免费,5 次/天)
- **广告钩子**:10 条信息流前 3 秒钩子,广告法自检(1 次数)
- **口播素材脚本**:15s 分镜表 + 合规提示(1 次数)

## 安装

从 SkillHub / ClawHub 一键安装,或手动克隆本仓库到 skills 目录。

## 配置

1. 注册 [ai.wohaoniu.com](https://ai.wohaoniu.com) → 个人中心 → 开放接口 → 生成 API Key
2. 配置环境变量 `WOHAONIU_API_KEY=whn_你的密钥`

## 用法

对 Agent 直接说:

> 「查一下『川渝老灶火锅』在 AI 里的可见度」
> 「给我的扫地机器人出 10 条广告钩子,主打静音,投巨量」

零第三方依赖;密钥只存哈希、可随时吊销;生成消耗你自己账户的次数。
