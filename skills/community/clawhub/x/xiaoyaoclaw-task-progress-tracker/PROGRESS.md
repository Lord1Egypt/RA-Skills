---
type: project
status: active
progress: 95
created: 2026-08-26
updated: 2026-10-14
docs:
  - path: DESIGN.md
    desc: 设计文档（数据模型 + 三条红线 + 三件套协同）
  - path: USER_GUIDE.md
    desc: 用户使用指南（站在使用者角度）
  - path: SKILL.md
    desc: 技能主体（意图识别 + 操作手册 + 边界）
  - path: README.md
    desc: 项目 README（含 hero）
  - path: assets/readme/hero.svg
    desc: README hero（PROGRESS.md 状态面板主题）
---

# xiaoyaoclaw-task-progress-tracker v2

> 🔁 2026-10-14工作区体检复核：状态保持 active（内容未变更，仅刷新审计时间）

## 目标 / 背景

重启同名项目（v1 因双轨制 + 全局钩子误报废弃）。v2 定位：管理 tasks/projects 目录生命周期的轻量进度卡系统——目录即容器，PROGRESS.md 即进度（状态 + 进度日志 + 文档索引），与 initializer + memory-distill 组成三件套。

## 当前状态

已发布：GitHub（main + MIT + topics×7 + 双语 desc + README hero）✅ + ClawHub v1.0.0 已提交（pending-publication）。实测通过。剩：ClawHub 公开后验证 + 姊妹项目互链。

## 进度日志

- 2026-08-26 11:36：调研交付，指挥官拍板自研方案
- 2026-08-26 18:22：设计确认（PROGRESS.md 命名 + 用户视角指南）
- 2026-08-26 18:37：模板 / SKILL.md / README / LICENSE / 全局技能同步完成，开始实测
- 2026-08-26 18:45：实测通过（task + project 双卡片：立项→进度→挂文档→完结→日志）
- 2026-08-26 18:50：发布完成——GitHub 仓库 + push（直连成功，代理 22307 挂）+ topics（gh CLI，API PUT 422 异常）+ ClawHub v1.0.0 提交
- 2026-08-26 18:55：README hero 完成（assets/readme/hero.svg，PROGRESS.md 状态面板主题，recognize.ps1 视觉校验通过，audit_readme.py 通过，push 5a5a287——直连被重置走代理恢复后成功）

## 文档索引

| 文档 | 说明 | 更新 |
|------|------|------|
| DESIGN.md | 设计文档 | 2026-08-26 |
| USER_GUIDE.md | 用户使用指南 | 2026-08-26 |
| SKILL.md | 技能主体 | 2026-08-26 |
| README.md | 项目说明（含 hero） | 2026-08-26 |
| assets/readme/hero.svg | README hero | 2026-08-26 |


