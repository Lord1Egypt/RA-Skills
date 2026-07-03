# SkillHub.cn 技能上传操作指南

## 核心原则

**发布包与运行包必须分离**

| 类型 | 存放位置 | 上传 |
|:---|:---|:---|
| 发布包 | `D:\openclaw-data\workspace\skills\<slug>\` | ✅ |
| 运行包 | 真实路径（如 `D:\ollama-intel\`） | ❌ |

## 快速流程

1. 准备发布包（API Key 清空 + 路径占位符）
2. Web 上传：skillhub.cn/dashboard → 开发者中心 → 发布技能
3. 或 CLI 上传：`skillhub publish ./my-skill --namespace my-team`
4. 发布前检查清单（5 项必查）
5. 存档到 IMA
6. 通知 main

## 文件

- `SKILL.md` — 完整操作指南正文
- `README.md` — 本文件

## CLI

skillhub CLI（兼容 ClawHub）：
```bash
npm install -g @astron-team/skillhub
skillhub login --token sk_xxx
skillhub publish ./my-skill --namespace my-team
```

Registry：`https://skill.xfyun.cn`（skillhub.cn 兼容）