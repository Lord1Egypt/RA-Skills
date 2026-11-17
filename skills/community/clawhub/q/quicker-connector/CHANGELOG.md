# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-10-06

### Added
- **批量图标导出器** `scripts/icon_exporter.py` - `export_icons()` 把每个动作图标导出为独立 PNG（`001_动作名_图标短key.png`）并生成 `icons_manifest.json`；支持 CLI `--out/--size/--workers/--no-manifest`
- **图标解析并发接口** `IconResolver.resolve_many()` - 去重后只对需要下载/渲染的取值启用 `ThreadPoolExecutor`（纯标准库）；新增 `try_local()` 本地快速通道、`kind_of()` 来源查询、`records` 明细、`max_workers` 参数
- **Excel 三种图标模式** - `icon_mode=embedded`（嵌图，默认）/ `path`（图标列只写相对路径）/ `none`；CLI `--icon-mode`、`--icons-dir`、`--icons-only`、`--no-dedupe`、`--workers`
- **便捷方法** - `QuickerConnector.export_icons()`；`QuickerConnector.export_to_excel()` 支持 `icon_mode` / `icons_dir`
- **统计增强** - `resolver.stats` 新增 `reused`（去重复用计数）、`elapsed_sec`、`local_file`

### Changed
- **图标解析去重** - 同一图标取值只解析一次（357 动作 → 239 唯一图标），同一 PNG 用 `shutil.copyfile` 复用到每个动作文件
- **xlsx 图片媒体压缩** - `embedded` 模式下相同内容的 `xl/media/*` 只保留一份（350 → 232 媒体，903.3 KB → 627.5 KB）；保存后校验能被 openpyxl 读回且图片数量一致，校验失败自动保留原文件；可用 `--no-dedupe` 关闭

### Fixed
- 修复「复用同一 openpyxl Image 对象导致所有行锚点塌陷」的隐患：每行独立新建 Image 对象，媒体去重改为包级后处理
- 图标尺寸参数校验：`size` 必须为 ≥ 1 的整数（`size=0` 此前会静默产出 0 个图标，现在明确报错）
- 目标 xlsx 被占用时给出友好提示（先写同目录临时文件再原子替换，失败不破坏原文件、不留半成品）

## [1.4.0] - 2026-10-06

### Added
- **Excel 导出（含真实图标）** - `QuickerConnector.export_to_excel()` 与命令行 `scripts/export_actions_excel.py`，在「图标」列嵌入真实图标图片
- **图标解析器** `scripts/icon_resolver.py` - URL 图标优先命中 Quicker 本地 ImageCache（SHA1(URL).png，完全离线），未命中自动下载；`fa:` 字体图标渲染为 PNG
- **SVG 栅格化** `scripts/svg_raster.py` - 纯 Python + Pillow 实现 SVG path / SVG 文件 → PNG（贝塞尔、圆弧、even-odd 填充、4x 超采样抗锯齿）
- **FontAwesome5 图标库** `scripts/fa_icons.py` + `data/fontawesome5_svg_index.json.gz` - 从 Quicker 自带 `FontAwesomeIconsWpf.dll` 预提取的 5996 个图标 SVG 路径（Solid/Regular/Light/Brands）
- **索引重建工具** `scripts/build_fa_index.py`

## [1.2.0] - 2026-03-28

### Added
- **Advanced Skill Creator optimization** - Complete modernization of skill structure
- **YAML frontmatter** - Full OpenClaw SKILL.md specification compliance
- **Natural language trigger** - 7 trigger keywords for better user interaction
- **System prompt** - Professional role definition for AI assistants
- **Thinking model** - Multi-stage cognitive pipeline for transparent decisions
- **Enhanced settings** - auto_select_threshold, max_results, and more
- **Declarative permissions** - Complete permission model with platform restrictions
- **Version history** - Clear changelog in skill metadata
- **GitHub ready** - LICENSE, README, CONTRIBUTING, .gitignore files
- **Security audit info** - Embedded skill-vetting results

### Changed
- **SKILL.md** - Complete rewrite with modern structure and examples
- **skill.json** - Modernized metadata with parameters, examples, permissions
- **Documentation** - Improved navigation and user guidance
- **Error handling** - Enhanced user feedback and troubleshooting

### Fixed
- **Trigger precision** - Better natural language understanding
- **Configuration validation** - Clear parameter definitions and ranges

## [1.1.0] - 2026-03-27

### Added
- **Initialization wizard** - User-friendly setup process
- **Database support** - SQLite database as alternative data source
- **Smart matching** - AI-powered action matching based on user needs
- **Fuzzy search** - Improved search capabilities
- **Encoding optimization** - Better encoding detection logic

### Changed
- **CSV reading** - Improved encoding detection and error handling
- **Performance** - Optimized action loading and searching

## [1.0.0] - 2026-03-27

### Added
- **Initial release** - Core Quicker integration functionality
- **CSV reading** - Support for Quicker exported CSV files
- **Multi-field search** - Search by name, description, type, panel
- **Action execution** - Execute Quicker actions via QuickerStarter
- **Basic testing** - Initial test suite

### Known Limitations
- Windows only (requires Quicker software)
- Requires manual CSV export from Quicker
- No cloud synchronization

---

## Upgrade Guide

### From 1.0.0 to 1.1.0
- Run initialization wizard again for new features
- Database mode requires additional setup
- Smart matching threshold may need adjustment

### From 1.1.0 to 1.2.0
- Copy optimized SKILL.md and skill.json
- Restart OpenClaw gateway
- New trigger keywords will be available automatically

---

## Deprecations

No deprecations in current version.

---

## Security Notes

- All versions pass skill-vetting security audit
- File operations restricted to user-specified paths
- No network access or data collection
- Subprocess calls limited to QuickerStarter.exe