# yaoyaoya-memory

🦞 **Universal Memory System for AI Assistants**

 универсальная система памяти | 让 AI 助手拥有持久化记忆能力

---

## ✨ 特性

- 🏠 **三层记忆架构**：MEMORY.md + 每日日记 + learnings
- 🏷️ **完整标签系统**：#项目 #教训 #决策 #待办
- ☁️ **IMA 默认集成**：开箱即用的腾讯IMA知识库同步
- 📊 **可靠性标注**：★★★★★ 到 ★☆☆☆☆
- ⚙️ **完全可配置**：通过 config.json 自定义一切

---

## 功能

| 功能 | 触发词 | 说明 |
|------|--------|------|
| 主动记忆 | 我记得、之前说过 | 跨会话记忆检索 |
| 记忆写入 | 记住、记录、存档 | 持久化存储 |
| 记忆整理 | 整理记忆、总结 | 定期归纳 |
| IMA同步 | 同步IMA、上传知识库 | 双向同步 |

---

## 快速开始

### 1. 安装

```bash
npx clawhub install yaoyaoya-memory
```

### 2. 配置 IMA（可选，默认启用）

编辑 `config.json`：

```json
{
  "knowledge_sync": {
    "enabled": true,
    "platform": "ima",
    "client_id": "你的IMA_CLIENT_ID",
    "api_key": "你的IMA_API_KEY"
  }
}
```

### 3. 使用

```
# 搜索记忆
我记得之前关于...的讨论

# 保存新记忆
记住这个重要的决定...

# 同步到 IMA
同步IMA
```

---

## IMA 默认笔记矩阵

| 笔记 | 用途 |
|------|------|
| AI记忆库 | 总目录 |
| 日记 | 每日事件 |
| 决策库 | 重要决策 |
| 用户档案 | 用户偏好 |
| 经验总结 | 最佳实践 |
| 项目 | 项目详情 |

---

## 文件结构

```
├── MEMORY.md           # 长期记忆
├── memory/             # 每日日记
│   └── YYYY-MM-DD.md
├── .learnings/         # 错误教训
│   └── LEARNINGS.md
├── knowledge/           # 项目知识库
└── scripts/
    └── sync_ima.py     # IMA同步
```

---

## 与其他方案对比

| 特性 | 其他方案 | yaoyaoya-memory |
|------|----------|-----------------|
| 记忆分层 | ❌ | ✅ 三层架构 |
| 标签系统 | ❌ | ✅ 完整标签 |
| IMA同步 | ❌ | ✅ 默认集成 |
| 可靠性标注 | ❌ | ✅ ★评级 |
| 配置化 | ❌ | ✅ config.json |

---

## License

MIT
