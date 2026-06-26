# 摇摇记忆系统 (yaoyao-memory)

> 四层渐进式长时记忆系统，让 AI 跨会话保持上下文、沉淀知识、持续进化

## ✨ 核心特性

- **智能确认** — AI 自动识别重要记忆，记录前确认
- **四层架构** — 短期 → 中期 → 长期 → 档案，渐进式沉淀
- **重要性分级** — Critical / High / Normal / Low 四级
- **记忆分类** — decision / preference / learning / task 等 8 种类型
- **混合检索** — 向量搜索 + 全文搜索，精准召回
- **IMA 同步** — 可选云端备份到 IMA 知识库

## 📖 新手入门

**👉 首先阅读：[QUICKSTART.md](./QUICKSTART.md)** - 小白友好指南

---

## 🚀 快速开始

### 安装

```bash
npx clawhub@latest install yaoyao-memory
```

### 查看新手教程

```bash
# 小白入门（推荐先看）
cat ~/.openclaw/workspace/skills/yaoyao-memory-v2/QUICKSTART.md

# 高级配置
cat ~/.openclaw/workspace/skills/yaoyao-memory-v2/ADVANCED.md
```

---

## 📚 记忆层级

| 层级 | 存储位置 | 保留时长 | 用途 |
|:---|:---|:---|:---|
| 短期 | 对话上下文 | 当前会话 | 即时交互 |
| 中期 | memory/*.md | 7-30 天 | 近期事项 |
| 长期 | MEMORY.md | 30 天+ | 核心知识 |
| 档案 | IMA 知识库 | 永久 | 知识沉淀 |

---

## 🔧 常用命令

| 命令 | 用途 |
|------|------|
| `python3 scripts/warmup.py` | 预热缓存 |
| `python3 scripts/health_check.py` | 健康检查 |
| `python3 scripts/benchmark.py` | 性能测试 |

详细命令请查看 [ADVANCED.md](./ADVANCED.md)

---

## 📁 文档目录

| 文件 | 用途 |
|------|------|
| [QUICKSTART.md](./QUICKSTART.md) | 🎓 小白入门指南 |
| [ADVANCED.md](./ADVANCED.md) | 🔧 高级配置参考 |
| [BOOTSTRAP.md](./BOOTSTRAP.md) | 🚀 首次使用引导 |
| [CHANGELOG.md](./CHANGELOG.md) | 📜 完整更新日志 |
| [SKILL.md](./SKILL.md) | 📄 技能完整文档 |

---

## 🔗 相关链接

- [ClawHub](https://clawhub.ai/skills/yaoyao-memory)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [IMA 知识库](https://ima.qq.com)

---

## 📄 License

MIT
