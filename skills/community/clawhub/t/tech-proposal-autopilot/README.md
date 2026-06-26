# 技术方案书全自动写作 - 快速指南

## 一分钟快速上手

### 启动新项目

```
请使用技术方案书自动写作技能，为"智慧城市数据中台项目"生成技术方案书。

要求：
- 规模：约30万字，18个章节
- 参考资料：[附上路径或URL]

章节大纲：
1. 项目概述与发展背景
2. 政策环境与市场分析
3. 系统总体架构设计
...
```

**就这样！剩下的全自动完成。**

---

## 核心特性

✅ **完全自动化** - 从启动到完成，全程无人工干预
✅ **断点自动续作** - 上下文超限时自动续作，不丢失进度
✅ **多智能体协作** - 4个智能体分工协作，效率提升5-10倍
✅ **进度持久化** - 所有进度保存到文件，支持跨会话恢复

---

## 自动续作机制

### 三重保障

| 触发方式 | 频率 | 优先级 |
|---------|------|--------|
| 心跳检查 | 用户交互时 | 高 |
| Cron 定时 | 每5分钟 | 中 |
| 主动请求 | 上下文>70%时 | 最高 |

### 工作流程

```
启动项目
    ↓
生成章节 1-N
    ↓
检测到上下文>70%？
    ├─ 是 → 保存进度 → 创建触发文件 → 结束会话
    └─ 否 → 继续生成
    ↓
心跳/Cron 检测到触发文件
    ↓
spawn 新会话 → 读取续作指令 → 继续生成
    ↓
所有章节完成 → 合并输出 → 通知用户
```

---

## 监控命令

```bash
# 查看所有项目状态
查看技术方案书项目列表

# 查看特定项目进度
查看 {project-name} 项目进度

# 手动触发续作
继续执行 {project-name}
```

---

## 技能迁移

将此技能迁移到其他 OpenClaw 实例：

### 步骤 1: 复制技能

```bash
cp -r skills/tech-proposal-autopilot /目标OpenClaw/skills/
```

### 步骤 2: 复制智能体

```bash
cp -r ~/.openclaw/agents/milo /目标OpenClaw/agents/
cp -r ~/.openclaw/agents/josh /目标OpenClaw/agents/
cp -r ~/.openclaw/agents/dev /目标OpenClaw/agents/
cp -r ~/.openclaw/agents/marketing /目标OpenClaw/agents/
```

### 步骤 3: 更新 HEARTBEAT.md

将以下内容添加到目标实例的 HEARTBEAT.md：

```markdown
- [x] **技术方案书项目检查** (已自动化)
  - 扫描 projects/*/progress.json
  - 筛选 status="in_progress" 且 autoContinue=true
  - 自动续作（详见 skills/tech-proposal-autopilot/SKILL.md）
```

### 步骤 4: 配置 Cron（可选）

```json
{
  "name": "tech-proposal-auto-continue",
  "schedule": { "kind": "every", "everyMs": 300000 },
  "payload": {
    "kind": "agentTurn",
    "message": "检查未完成的技术方案书项目并自动续作"
  }
}
```

---

## 已验证项目

| 项目 | 规模 | 状态 |
|------|------|------|
| 深圳市数据流通利用基础设施 | 15万字/10章 | ✅ 100%自动化 |
| 智慧养老餐饮综合服务平台 | 20万字/18章 | ✅ 100%自动化 |
| 工业互联网与智能制造平台 | 31万字/12章 | ✅ 100%自动化 |

---

## 文件结构

```
skills/tech-proposal-autopilot/
├── SKILL.md                    # 完整技能文档（必读）
├── README.md                   # 本文件（快速指南）
├── scripts/
│   ├── check-and-continue.js   # 自动续作检查脚本
│   └── extract-keypoints.js    # 参考资料提取脚本
└── templates/
    ├── outline-template.md     # 大纲模板
    └── progress-template.json  # 进度文件模板
```

---

## 常见问题

**Q: 上下文超限怎么办？**
A: 自动续作机制会自动处理，无需人工干预。

**Q: 如何查看进度？**
A: 查看 projects/{project-name}/progress.json 或询问"查看项目进度"。

**Q: 可以暂停项目吗？**
A: 可以，在 progress.json 中设置 `autoContinue: false`。

**Q: 支持哪些参考资料格式？**
A: PDF、Word、网页URL、纯文本、Markdown。

---

**详细文档**: [SKILL.md](./SKILL.md)
