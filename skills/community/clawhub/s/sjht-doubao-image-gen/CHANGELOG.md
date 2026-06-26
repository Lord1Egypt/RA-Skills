# Changelog

All notable changes to **doubao-image-gen** will be documented in this file.

---

## [1.0.0] - 2026-03-17

### Added
- 初始版本发布
- 基于火山引擎豆包 `doubao-seedream-5-0-260128` 模型实现文生图能力
- 支持并发批量生成，默认 4 线程同时调用 API（`--count` + `--workers` 参数）
- 支持多种图像尺寸：`1024x1024` / `2K` / `4K` / `1280x720` / `720x1280` / `2048x2048` 等
- API Key 三级读取机制：CLI 参数 → 环境变量 `ARK_API_KEY` → `~/.doubao-image-gen/.env` 文件
- 生成结果自动下载为 `.jpeg` 并按序号命名
- 自动输出 `prompts.json`（提示词与文件映射记录）
- 自动生成 `index.html` 图库预览页，暗色赛博风 UI，支持悬停动效
- `--dry-run` 模式：仅打印参数不消耗 API 调用
- `--watermark` 开关：默认关闭水印
- 输出 `GENERATED_IMAGE: 路径` 格式，便于 AI 直接引用图片发送到聊天
- 完整的 AI 使用指引：触发词识别、提示词优化建议、标准调用流程

### Notes
- 模型名称 `doubao-seedream-5-0-260128` 无需在火山方舟控制台创建推理接入点，直接用 API Key 即可调用
- 依赖：`openai>=1.0`、`requests`
