# Web Novel Creator — 网文创作兼容协调层

不再是一个独立的创作引擎，而是让 SkillHub 上优秀的网文创作 Skill 都能无缝对接 **Memory Manager Pro** 的索引系统。

## 定位

```
      novel-generator     open-novel-writing     novel-orchestrator
      （从零生成爽文）    （全流程设定管理）      （多角色协作）
              │                    │                     │
              └────────────────────┼─────────────────────┘
                                   ▼
                          web-novel-creator
                    （兼容协调层 + 索引归档入口）
                                   │
                                   ▼
                          Memory Manager Pro
                      （语义推导 + 全量索引更新）
```

## 不做的事

- ❌ 不自建创作引擎（用 `novel-generator`）
- ❌ 不替代多角色协作（用 `novel-orchestrator`）
- ❌ 不管理世界观/人设（用 `open-novel-writing`）
- ❌ 不生成图片（用 `nano-banana-pro`）
- ❌ 不做索引管理（由 `Memory Manager Pro` 执行）

## 做的事

- ✅ **统一目录规范** — 让各 Skill 产出存到同一位置
- ✅ **兼容检测** — 自动识别当前使用了哪些外部 Skill
- ✅ **创作后归档** — 迁移正文、补充规划、更新标题库
- ✅ **对接 Memory Manager Pro** — 统一入口完成全量索引更新

## 兼容的 Skill

| Skill | 原生产出位置 | 兼容层介入 |
|-------|-------------|-----------|
| novel-generator | output/ + .learnings/ | 迁移正文+补充规划 |
| open-novel-writing | 正文/ + 设定/ + 规划/ | 命名微调+补录标题库 |
| novel-orchestrator | 正文/ + 规划/ | 补录标题库+索引归档 |
| cq-novel-writer | 根目录 | 迁移+重命名+归档 |
| 其他 | 待检测 | 通用对接流程 |

## 统一目录规范

```
novel/{项目名}/
├── 正文/             # 各Skill共同读写
├── 规划/             # 标题库+章节规划
├── 设定/             # 世界观/人设（open-novel-writing）
├── 总纲/             # 故事总纲（cq-novel-writer）
├── .learnings/       # 记忆系统（novel-generator）
└── output/           # 输出（novel-generator）
```

## 安装

```bash
# 本地安装
cp -r web-novel-creator ~/.openclaw/workspace/skills/

# 从 SkillHub 安装
clawhub install web-novel-creator
```

## 更新日志

### v2.0.0 (2026-04-26)
- **重构为兼容协调层**：不再自己做创作引擎
- 兼容 novel-generator、open-novel-writing、novel-orchestrator、cq-novel-writer
- 统一目录规范，让各 Skill 共享项目空间
- 自动检测外部 Skill，自动迁移产出
- 对接规范文档（references/对接规范.md）
- 配套 Memory Manager Pro v1.1.0

### v1.1.1 (2026-04-26)
- 修复：创作时不再重复读取上一章正文

### v1.1.0 (2026-04-26)
- 索引更新委托给 Memory Manager Pro

### v1.0.0 (2026-04-26)
- 初始版本
