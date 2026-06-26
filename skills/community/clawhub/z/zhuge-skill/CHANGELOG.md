# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/) 精神 + [Semantic Versioning](https://semver.org/lang/zh-CN/)。

---

## [v1.1.1] — 2026-04-19 凌晨 · 新手踩坑修复 (LLM_PROVIDER 必写) + 文档一致性

### Fixed
- **坑 #15**: `.env` 只填 `DEEPSEEK_API_KEY` 但没写 `LLM_PROVIDER=deepseek` → LLM 静默不调用 (2026-04-18 晚朋友实测踩到)
- **缺失 `.env.example`**: README 引用它但文件不存在 (朋友无从下手) · 补上 · 把 LLM_PROVIDER 必要性 + Windows 编码坑都标红
- **README 30 秒上手**: 重写成 5 步真实流程 (clone / 装依赖 / .env / 编码 / 启动), 加两个坑显著提示
- **sync.py docstring**: 陈旧远程 URL `taijios9/zhuge-crystals` → `yangfei222666-9/zhuge-crystals`

### Note
- v1.1.0 "触发虾评重扫" 描述不准 — 实际靠重建 skill_id (`f0cb5f86`) 解决, `POST /api/upload` 不重扫 security. 已记入 memory.

---

## [v1.1.0] — 2026-04-18 晚 · 品牌视觉定稿 (v15) + 发新 skill

### Added
- `assets/brand.png` — TaijiOS 视觉品牌定稿 (v15: 孔明剪影 × 金八卦 × 青电路 × 浮空进化大脑 · 深海军蓝基调)
- README.md / README.en.md 顶部加品牌图

### Why this version matters
- 虾评 `security_status=warning` 自 v0.1.0 起挂着 (根因: 初版 zip 用反斜杠路径, 平台扫描器解压失败)
- 所有 v0.1.1~v1.0.5 被降权, downloads 归零 (仅 v0.1.2 拿到 3 次)
- 这次以 1.1.0 重发干净 zip, 目标是 override 掉 v0.1.0 的 warning

---

## [v1.0.9] — 2026-04-18 晚 · 响应虾评首条 review (A3-1) + DEMO LLM

### Fixed (livestream-critical)
- DEMO 模式所有比赛返回同一卦 → 改为按队名 hash 确定性变化 (解/大有/需 各不同)
- DEMO 不标注是演示数据 → 加 `⚠ DEMO 模式 · 非真实预测` 粉红 banner
- 版本字符串硬编码 v0.1.0 → v1.0.9
- 品牌三不一致 ("数字孪生"/"虾猜 AI 军师"/"推演军师") → 统一 "诸葛亮 · AI 推演军师"
- `predict "单词"` 抛 Python Traceback → 友好 ⚠ 提示 + 用法示例
- `core/llm.py` Semgrep MEDIUM 提示词注入: 新增 `_sanitize` (ctrl char strip + length clamp) + `_call_gemini` 改用 `systemInstruction` 结构化不拼接
- `publish_xiaping.py` 发布时未排除 `.env` → 加 `SENSITIVE_FILES` 黑名单防密钥泄漏

### Added
- **DEMO 模式也调用 LLM** 生成孔明亲笔古文评 (之前只有真 API key 路径有) — 回应虾评 "易用 3.0 · 需配置多个 API 才能完整使用" 反馈

### 致谢
- 虾评首评来自 `Coze主智能体 A3-1` (2026-04-18 19:30, 4.0/5, 稀缺 5.0): "独特的决策辅助技能, 把 90% 决策留在 CPU"。建议的"预设场景模板"列入 v1.1 roadmap (股票/招聘选型等)。晶体可视化也在考虑。

---

## [v1.0.5] — 2026-04-18 · 本地 Ollama 零成本路径 + 虾评重扫

### Added
- **本地 Ollama 三行启动**（README §三档落地）— `ollama pull qwen2.5:7b` + 一行 env 即可零成本跑「孔明亲笔古文评」。实测 10/10 通过 · p50 ~12s/场
- README §12 云商 + 本地 Ollama 双栈并列，新用户零门槛试水

### Changed
- 重新发布触发虾评侧完整 security scan（v0.1.0 sticky flag 修复）

---

## [v1.0.4] — 2026-04-17 · UX + 工具批

### Added
- `scripts/error_log.py` — 轻量 JSONL 错误日志（含 `--resolve` CLI + priority/status 字段），接入 `backfill` 守护循环、`fetch_actual_result`、`core/llm.py` 三个 except 点
- 晶体 schema v2：新增 `first_seen` / `last_seen` / `recurrence_count` 字段；`match_crystal` 命中时回写 `crystals_local.jsonl`（实战复用次数可观测）
- `scripts/predict.py` 预测输出显示晶体被复用次数 + 首见年龄（高复用标 ⭐）
- `scripts/crystallize.py --dry-run` 预览结晶结果不写入
- `scripts/stats.py --crystals` 晶体排行 + stale 监控
- `scripts/stats.py --errors` 最近错误摘要
- `README.en.md` 英文版（为国际用户 / Show HN 准备）
- README.md §📬 反馈与联系 段（邮箱优先、微信辅）
- README.md §全平台兼容 扩展为每宿主（Claude Code / Cursor / OpenClaw / Hermes / 纯 Python）可复制的接入片段
- 本文件 `CHANGELOG.md` 独立

### Changed
- 内部：`crystallize(verbose, write=True)` 新增 `write` 参数支持 dry-run
- 内部：`match_crystal()` 返回带更新后 counters 的副本（调用方能拿到最新 recurrence_count）

### Notes
- 向后兼容：旧的 v1 晶体无 new 字段时 load 正常；error_log 老条目无 priority/status 时 summary 显示 `?`

---

## [v1.0.3] — 2026-04-17 · 视觉素材升级

- 新增 `assets/demo.png` — 诸葛亮推演引擎实录截图（启动动画 + 6 维爻位实时评分）
- README 顶部嵌入演示截图，一眼看清 skill 的"一句话预测闭环"
- 无代码变更

## [v1.0.2] — 2026-04-17 · 文档一致性修正

- 修复 SKILL.md 与 PRIVACY.md 自相矛盾点：原 §晶体共享 节仍沿用 v1.0.0 "有上传功能、默认关闭"的旧描述，与 v1.0.1 的代码事实（`push` 已移除）不一致，已重写为 §晶体拉取 与本地导出，对齐代码
- 数据流向表：`sync.py` 改为 `pull`（只 GET），`share.py` 标为纯本地导出
- 自学习闭环图修正：`sync 推/拉` → `sync 拉公共晶体（只入）`
- 审计 grep 命令扩展到 4 条，加入"全仓库扫上传端点"一项
- 代码层面零变更，仅文档修正

## [v1.0.1] — 2026-04-17 · 透明度升级

- 新增 §环境变量清单（12 个 LLM + 2 个数据源，每个用途 / 获取地址 / 降级行为说明）
- 新增 §安全与隐私（数据流向表 + 每个脚本是否向外发数据）
- 明确 LLM 中转风险（relay 模式数据流向第三方）
- **架构级隐私合约**：`sync.py` 的 `push` 函数从代码中移除，固化为单向消费架构（只 pull 不 push）
- `sync.py` 子命令简化为 `pull`（从公开 URL 只读拉取）和 `status`（本地查看）
- `share.py` 明确为本地导出工具（生成 `exports/*.md|json`），不联网
- 新增 [PRIVACY.md](./PRIVACY.md)：详细列出网络调用清单、作者数据可见度矩阵、fork 者脱敏白名单
- 新增 §如何审计（4 行 grep 命令自查）

## [v1.0.0] — 2026-04-17 · Initial release on ClawHub

- 5-source data fusion + 64-hexagram reasoning + experience crystallization
- 12+ LLM provider support
- Guardian mode + crystal pool (pull-only from v1.0.1)

---

*SKILL.md 的 "## 更新日志" 一节将在下一次发版时裁剪为只保留最新 2 个版本，其余迁移到本文件。*
