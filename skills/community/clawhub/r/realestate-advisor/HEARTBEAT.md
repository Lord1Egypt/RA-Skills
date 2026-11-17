# HEARTBEAT.md — 置安居定期维护任务

> 启用此文件：移除 `# Keep this file empty...` 注释，添加以下任务。
> 心跳周期：每天一次（由 OpenClaw 网关心跳触发）

---

## 每日任务（轻量）

- [ ] 检查 `memory/` 目录，删除 7 天前的临时日志（保留 `YYYY-MM-DD.md` 中的重要条目到 `MEMORY.md`）
- [ ] 检查 `examples/` 目录，确保示例报告模板存在

---

## 每周任务（周日）

- [ ] 审查 `self-improving/corrections.md`，将重复 3 次以上的模式提升到 `memory.md`（HOT 层）
- [ ] 检查 `self-improving/projects/realestate-advisor.md` 中的"待改进项"，更新进度
- [ ] 清理 `self-improving/archive/` 中超过 180 天的归档文件

---

## 每月任务（1 号）

- [ ] 统计上月分析次数（从 `memory/YYYY-MM-DD.md` 汇总）
- [ ] 检查 TOOLS.md 中的数据获取工具是否仍然有效（搜索 API 是否正常）
- [ ] 更新 `MEMORY.md` 中的"上次更新"日期

---

## 触发条件（事件驱动）

- **用户纠正** → 立即记录到 `self-improving/corrections.md`
- **搜索 API 失败** → 检查 `AUTH_GATEWAY_PORT` 环境变量，必要时更新 TOOLS.md
- **新小区分析方法** → 更新 `examples/` 和 `self-improving/projects/realestate-advisor.md`

---

_心跳任务由 OpenClaw 网关定期触发，无需手动执行。_
