# Changelog

## 1.1.0 (2025-03-11)

### Added
- 新增「小红书」平台策略列，覆盖所有 4 个目标平台
- 新增 AI 工具参数包：Sora / Vidu / 即梦 / Kling（可灵）
- 新增测试用例：B站3分钟专业科普、视频号15秒剧情反转、边界测试
- `tone_style` 枚举值新增「生活记录」以保持与 schema 同步
- 扩写 README.md 文档内容（版本标识、平台列表、参数说明、AI 工具等）
- 新增边界测试用例：缺 target_platform、空字符串、非法 platform/duration/tone_style

### Fixed
- SKILL.md 版本号从 `1.0.0` 修正为 `1.1.0`（匹配目录名）
- examples.json 版本号从 `1.0` 修正为 `1.1.0`
- `tone_style` 参数描述同步 schema 中的 5 个枚举值
- SKILL.md 工作流指令第3点同步 AI 工具列表（补充 Kling/Sora/Vidu/即梦）
- 平台策略表格现在包含「小红书」列

## 1.0.0 (2025-02-20)

### Added
- 初始版本发布
- 支持抖音 / B站 / 视频号 三大平台
- 分镜脚本表、AI 生成参数包、平台运营策略、合规校验四大模块
