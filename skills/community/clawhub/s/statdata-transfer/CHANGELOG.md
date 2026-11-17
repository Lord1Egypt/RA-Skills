# Changelog / 更新日志

## 2.2.1 (2026-08-02)

- **Security fixes (ClawHub SkillSpector audit)** / 安全修复（回应 ClawHub 安全审计）：
  - Pin `lxml>=6.1.0` (was `>=6.0`, which is itself vulnerable to CVE-2026-41066 XXE); corrected the misleading comment. / 将 lxml 钉死为 `>=6.1.0`（原 `>=6.0` 本身受 CVE-2026-41066 XXE 影响），并修正误导性注释。
  - Harden lxml XML parsing in `reader_legacy.py` (`.wdx`/`.opju`) with an explicit XXE-safe parser (`resolve_entities=False, no_network=True, huge_tree=False`) — defense in depth for any lxml version. / 在 `reader_legacy.py` 用显式防 XXE 解析器加固 `.wdx`/`.opju` 解析，任何 lxml 版本均安全。
  - Expand side-effect disclosure in SKILL.md frontmatter (`summary`/`description`) and `permissions.filesystem` to fully state the write surface: sidecar metadata (`<name>_metadata.json` beside CSV/TSV, embedded in Parquet/Arrow) and `.bak`/`.bak.1` backups when overwriting `.hyper`. Addresses SkillSpector finding Tp4 (understated disclosure). / 在 SKILL.md frontmatter 与 permissions 中补全写面披露：sidecar 元数据与 `.hyper` 覆盖备份，回应 Tp4 披露不足。

## 2.2.0 (2026-08-02)

- **Optimize user-facing docs & navigation (UI)** — README restructured to a user perspective:
  at-a-glance capability table, scenario index, conversation examples, and FAQ, so human
  ("carbon-based") users find it easier to use. / 优化面向用户的文档与导航：README 重构为用户视角，
  含能力速览表、场景索引、对话示例与 FAQ，让「碳基生物」用户更易上手。
- **Robustness fixes** / 健壮性修复：
  - CSV delimiter auto-detection (comma / semicolon / tab / pipe); warn when non-comma is used. / CSV 分隔符自动探测，非逗号时告警。
  - Add `.tsv` read support (now symmetric with write). / 新增 `.tsv` 读取（与写入对称）。
  - UTF-16 encoding auto-detection via BOM (no longer conflicts with GBK). / UTF-16 按 BOM 探测，避免与 GBK 冲突。
  - Fix XPT reader `NameError` (`reader_sas` now imports `_normalize_value_labels`). / 修复 XPT 读取 `NameError`。
  - Warn on silent variable-label truncation (SPSS 255 bytes / Stata 80 chars) instead of silently losing data. / 长变量标签超上限时返回截断告警，避免静默丢失。
  - Mixed-type columns no longer crash on Parquet write (fallback to nullable string). / 混合类型列写 Parquet 不再崩溃。
  - Clear error when a directory is mistaken for a Parquet partition. / 目录被误当 Parquet 分区时给出清晰报错。
  - Add SAS6 (`.ssp`) graceful degradation hint. / 补全 SAS6 (.ssp) 占位降级指引。

## 2.1.0 (2026-07)

- Bilingual (中文/English) compliance for SKILL.md frontmatter and docs.
- Security hardening: declare side effects, gate R-invoking fallback behind `allow_r_exec=True`.
