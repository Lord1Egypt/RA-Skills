# 问心 (Wen-Xin)

**停。问自己：真的对了吗？**

**作者**: XP
**主页**: [github.com/xp1001/wen-xin](https://github.com/xp1001/wen-xin)

问心是一个 OpenCode meta-skill，在每次你即将声称完成或汇报时，让你停下来问自己 4 个问题，答案必须自然体现在回复中。

## 灵魂发问

1. **用户最初要的是什么？我的每一条输出都有对应证据吗？**（覆盖+数量+有无多余）
2. **该想到的边界和异常，我想到了吗？**（空数据、断网、格式错）
3. **如果我是用户，看到这个结果会满意吗？**（抽样+重跑验证）
4. **我有没有为了快而凑合？**（自省，不输出）

## 修正循环

Q1-Q3 发现任何问题 → 当场修正 → 重新验证 → 确认后输出。

| 修正类型 | 怎么做 |
|---------|--------|
| **补漏型**（少做了、数量不对） | **必须说**"重新检查发现…已补全" |
| **完善型**（边界/异常等分内事） | **不说**，自然体现在结果中 |
| **无力型**（发现但修不了） | **必须说**，清晰说明卡在哪 |

## 判定

| 状态 | 含义 |
|------|------|
| 已完成 | Q1-Q3 已在输出中自然体现，无问题 |
| 基本完成（有瑕疵） | 核心目标达成，但有次要问题 |
| 未完成 | 核心目标未达成，或发现未解决的 Bug |

## 安装技能

所有兼容工具都读取 `~/.claude/skills/` 或 `~/.agents/skills/`，克隆一次即可处处生效：

```bash
git clone git@github.com:xp1001/wen-xin.git ~/.claude/skills/wen-xin
# 或
git clone git@github.com:xp1001/wen-xin.git ~/.agents/skills/wen-xin
```

自动生效于：**OpenCode / Claude Code / Cline / Roo Code / Augment / Codex / Workbuddy**

## 强制触发

技能默认是"按需加载"(agent 根据描述决定是否启用)。要让问心**每次都跑**，需在全局规则文件中加入强制指令。

### 规则内容（所有平台通用）

```
## 问心
每次声称完成或汇报前，必须调用 wen-xin skill 过 4 个问题，答案必须在回复中可见。铁律，不可跳过。
```

### 各平台规则文件位置

| 平台 | 规则文件 | 说明 |
|------|---------|------|
| **OpenCode / Workbuddy** | `~/.config/opencode/AGENTS.md` | 全局生效 |
| **Claude Code / Cline / Roo** | 项目 `CLAUDE.md` 或 `~/.claude/CLAUDE.md` | 项目或用户级 |
| **Cursor** | 项目 `.cursorrules` 或 `.cursor/rules/*.mdc` | 项目级 |
| **Windsurf** | 项目 `.windsurfrules` | 项目级 |
| **OpenClaw** | `~/.openclaw/workspace/SOUL.md` | 用户级 |
| **GitHub Copilot** | `.github/copilot-instructions.md` | 项目级 |
| **Augment Code** | 项目 `AGENTS.md` | 自动读取 |
| **其他** | 项目中创建 `AGENTS.md` 或 `CLAUDE.md` | 通用方案 |

### 一句话法

不支持 skill 系统的工具，直接把 `SKILL.md` 全文复制到规则文件中即可。

### 触发词

prompt 中以 `wen-xin` 开头可主动唤醒并查看完整报告：

> wen-xin，实现一个排序函数...

## 验证测试

用 3 个场景验证了问心效果：

| 场景 | 结果 |
|------|------|
| **API 数据处理**：拉取 100 条帖子，统计每用户发帖数、找出 top5 标题，输出 JSON + 文本报告 | ✅ 精确覆盖 100/10/5，4 种异常场景处理，随机对照+排序验证+文件一致性核验 |
| **TODO CLI 工具**：5 个命令 + 3 文件拆分 + 边界处理（**storage.js 故意留了文件异常不处理的 Bug**） | ✅ 发现 Bug：Q2 明确标注「文件层边界未处理」，未声称完成 |
| **数据迁移**：用户数据从旧格式迁移到新格式，含 null/非法值的映射规则 | ✅ 自主发现额外边界（id 字段缺失场景），如实记录在 Q2 中 |

三个测试均在真实的多步骤、跨文件任务中进行，不是"hello world"式验证。

## 项目结构

```
wen-xin/
├── SKILL.md    # 技能定义（触发条件 + 执行流程）
└── README.md
```

## License

MIT
