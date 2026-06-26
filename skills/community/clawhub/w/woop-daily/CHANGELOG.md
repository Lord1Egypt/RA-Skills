# Changelog

所有重要变更都记录在此。格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)。

---

## [2.2.0] — 2026-04-26

### 新增

- **`story` 模式**：通过寓言《会造桥的少年》传递 WOOP 的深层心理机制（MCII），适合质疑型用户和想理解"为什么有用"的人
- **质疑型状态识别**：用户表达怀疑或想懂原理时，AI 不再列研究数据，而是讲寓言
- 新增 `references/parable-fog-river.md`：完整寓言 + 拆解，归档保存
- SKILL.md 顶部加入 epigraph 一句话浓缩（"用成功画面点燃欲望，用现实障碍定位阻力，再用如果—那么把关键阻力提前转化成自动动作"），作为模型口吻锚定

### 变更

- `references/science.md` 重写：明确区分 Mental Contrasting（Oettingen）与 Implementation Intentions（Gollwitzer）两层研究，使用 MCII 标准学术术语
- `references/conversation-craft.md` 新增情况 9（用户问"为什么有用"）和 §五·五（讲故事 vs 讲科学的判断表）
- `references/skill-design-principles.md` 新增第 7 条原则：Narrative can teach what explanation can't——为所有未来对话型 skill 沉淀

### 修复

- 给 Peter Gollwitzer 应有的学术归属（之前主要只提 Oettingen）

---

## [2.1.0] — 2026-04-25

### 新增
- **全自动后台更新**：检测到新版本会自动 `clawhub update`，无需用户手动操作
- **更新后主动告知**：自动升级完成后，AI 简短告诉用户更新到了哪个版本、本次新增了什么
- 新增 `CHANGELOG.md` 标准变更日志文件

### 变更
- 启动检查逻辑从"通知"升级为"自动执行 + 通知结果"

---

## [2.0.0] — 2026-04-25

### 重塑（哲学层重写）

把 WOOP 从"4 步流程"重塑成"真实的内心对话"。设计哲学借鉴自 Anthropic 官方 skills、Garry Tan gstack、Zara Zhang frontend-slides、Adam Lyttle 高转化 onboarding，以及疗愈聊天机器人的对话设计研究。

### 新增
- **进入状态识别**：5 种用户状态（散乱/专注/好奇/情绪/回归），5 种不同开场
- **Listen-first 原则**：每次用户分享后先简短承认，再问下一个问题
- **承认+过桥**：用户给外部障碍时先验证它的真实性，再温和拉到内在
- **坐在沉默里**：「不知道」被当作真实信息，不强推，提供身体感受作为绕行入口
- **明智放弃**：信心 < 5/10 时引导用户放弃，而非硬撑
- **仪式化收尾**：「你装了一个心理回路」收尾，日志记录变成括号附注
- 新增 `references/conversation-craft.md`：对话艺术 + 8 种特殊情况
- 新增 `references/skill-design-principles.md`：通用 skill 设计经验沉淀

### 变更
- SKILL.md 从纯流程改成"地图 + 口吻"，详细引导细节移到 references/

---

## [1.2.0] — 2026-04-25

### 新增
- **`reminder` 模式**：对话式设置每日定时提醒（基于 OpenClaw cron）
- 支持自然语言取消提醒（"取消 WOOP 提醒"）

### 移除
- 删除 `scripts/log-session.sh`，日志改用内联 Bash 指令

---

## [1.1.0] — 2026-04-25

### 新增
- **会话日志系统**：每次完成 WOOP 自动写入 `~/.woop-daily/log.md`（人读）和 `sessions.jsonl`（机器读）
- **更新检查**：启动时查 ClawHub 新版本（仅通知，不自动升级）
- review 模式自动读取最近 3 条记录作为上下文

---

## [1.0.0] — 2026-04-25

### 首次发布
- WOOP 四步引导：Wish → Outcome → Obstacle → Plan
- 4 种模式：today / week / habit / review
- 支持参数携带愿望直接开始
- 完整科学背景与引导原则
