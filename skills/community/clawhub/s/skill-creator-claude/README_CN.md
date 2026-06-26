# skill-creator-claude

> Anthropic 最优秀的 skill 创作方法论——现在可以在任何 agent 平台使用。

Anthropic 在 Claude Code 中内置了一套卓越的 skill-creator：完整涵盖起草、测评、迭代、benchmark 和 description 优化的开发闭环。本仓库是对原版的最小改动适配，移除了 Claude Code 专有依赖，让任何 agent 平台的用户都能使用——无论你用的是哪个平台。

---

## 原版出处与归属

- **原作者**：Anthropic
- **许可证**：Apache 2.0（见 [LICENSE](./LICENSE)）
- **原始来源**：Claude Code 内置插件（`~/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator`）
- **完整体验**：[Claude Code](https://claude.ai/code) — 免费使用，100% 的功能都在那里

本仓库是基于 Apache 2.0 的 derivative work，所有知识产权归 Anthropic 所有。

---

## 我们的理念

- **最小改动**：只移除无法跨平台运行的硬依赖，方法论、脚本和工具链完整保留
- **保留归属**：完整保留所有版权声明和 LICENSE 文件，这既是 Apache 2.0 的要求，也是我们的原则
- **普惠大众**：原版 skill-creator 非常优秀，不应该只有 Claude Code 用户才能用到
- **入口而非替代**：如果你想体验 100% 的功能，去用 Claude Code——这个版本是入口，不是替代品

---

## 与原版的差异

只对 `SKILL.md` 做了 **4 处修改**，改动量 < 10%，其余完全一致。

| # | 修改内容 | 原因 |
|---|---|---|
| 1 | 文件头添加修改声明注释 | Apache 2.0 要求在修改的文件中注明变更 |
| 2 | Description Optimization Step 3：添加平台说明，注明 `run_loop.py` 需要 `claude -p` CLI，提供无 CLI 时的手动替代方案 | `claude -p` 是 Claude Code 专有命令行工具 |
| 3 | "Package and Present" 章节：移除 `present_files` 工具的条件判断，直接运行 `package_skill.py` | `present_files` 是 Claude Code 专有工具 |
| 4 | 合并"Claude.ai-specific"和"Cowork-Specific"两个平台章节为统一的"Platform Notes"，移除末尾 TodoList 提示 | 统一跨平台说明，移除 Claude Code UI 专有功能引用 |

**未改动的内容**（即全部核心内容）：
- 完整的 skill 开发方法论
- 所有 Python 脚本（`run_eval.py`、`run_loop.py`、`improve_description.py` 等）
- eval viewer 和 benchmark 系统
- grading 和 blind comparison 工作流
- 所有 agent 子文件（`agents/grader.md`、`agents/comparator.md`、`agents/analyzer.md`）
- `references/schemas.md`

---

## 功能对比

| 功能 | 本版本 | Claude Code 原版 |
|---|---|---|
| Skill 起草与迭代 | ✅ | ✅ |
| 测评与 eval viewer | ✅（需 Python） | ✅ |
| Benchmark 对比 | ✅（需 subagents） | ✅ |
| Description 优化（improve） | ✅（需 `ANTHROPIC_API_KEY`） | ✅ |
| Description 触发率测试 | ❌ 需 `claude -p` CLI | ✅ |
| 打包 `.skill` 文件 | ✅ | ✅ |

---

## 安装方式

### 通过 ClawHub 安装
```bash
clawhub install plabzzxx/skill-creator-claude
```

### 手动安装
Clone 或复制整个仓库到你的 agent 平台的 skills 目录即可。

### Description 优化脚本（可选）
`improve_description.py` 直接调用 Anthropic API，任何平台均可使用，需设置：
```bash
export ANTHROPIC_API_KEY=your_key_here
```

---

## 致谢

所有设计思想、代码和方法论版权归 Anthropic 所有，基于 Apache 2.0 许可证开放。  
如果这个 skill 对你有价值，去试试 [Claude Code](https://claude.ai/code) 吧——那里有完整的体验。
