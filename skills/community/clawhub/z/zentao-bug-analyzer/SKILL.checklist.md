# 禅道 Bug 分析执行检查清单

> ⚠️ 硬约束：分析开始前通读本清单，每步必须逐项完成，缺一不可。
> 详细流程说明见 [SKILL.md](SKILL.md) 对应章节。

## 执行检查清单

- [ ] 步骤 1：消息解析（提取 Bug ID）→ [§步骤 1](SKILL.md#步骤-1消息解析)

- [ ] 步骤 2：重复分析检查 → [§步骤 2](SKILL.md#步骤-2重复分析检查)
  - 登录禅道（`zentao-login.js`，获取 WS endpoint，一个 Bug 全程复用）
  - 获取 Bug 详情 + 检查 API `comments` 字段中的重复评论（非 `historyChanges`）

- [ ] 步骤 3：模块分类 → [§步骤 3](SKILL.md#步骤-3模块分类)
  - 按 config aliases 子串硬匹配，不在范围 → 飞书通知 + 终止

- [ ] 步骤 4a：下载附件（`zentao-download-files.js`）→ [§步骤 4a](SKILL.md#4a-下载附件和日志)

- [ ] 步骤 4b：确定 Bug 发生时间 → [§步骤 4b](SKILL.md#4b-确定-bug-发生时间)
  - 优先：Bug 描述文本（steps + description）> 附件截图/视频系统时间 > 飞书询问
  - 禁止：文件名/创建时间/上传时间作为时间来源

- [ ] 步骤 4c-1：按 config commit_extract 规则提取 commit id → [§步骤 4c](SKILL.md#4c-分支定位)
  - 搜不到 → 飞书通知 + 终止，禁止近似匹配

- [ ] 步骤 4c-2：`git branch --contains <commit-id>` 记录分支信息

- [ ] 步骤 4c-3：分支检出（二选一）：仓库空闲 → `git checkout` + submodule update；被占用 → `git worktree add` 隔离

- [ ] 步骤 4d：AI 深度分析 → [§步骤 4d](SKILL.md#4d-ai-综合深度分析)
  - 结合 Bug 详情 + 日志 + 代码 + API `comments` 评论

- [ ] 🔴 步骤 5：输出报告 → [§步骤 5](SKILL.md#步骤-5结果输出)
  - ⚠️ 先检查 config 根级别 `auto_comment` 字段（未配置时默认视为 `true`）
  - `auto_comment === true` 或未配置：禅道评论（`zentao-build-comment.js` → `zentao-post-comment.js`）+ 飞书摘要
  - `auto_comment === false`：仅生成 `report.md` + 飞书摘要

- [ ] 🔴 步骤 6：清理 → [§步骤 6](SKILL.md#步骤-6清理)
  1. 杀 login 进程 + Chrome 树（Windows: `taskkill /PID <PID> /F /T`，macOS/Linux: `kill -9 <PID> && pkill -P <PID>`）
  2. `git worktree remove --force` 清理 worktree 残留
  3. 检查无 `zentao-*.js` 残留进程
  4. 确认只剩 OpenClaw 进程（gateway/worker）
