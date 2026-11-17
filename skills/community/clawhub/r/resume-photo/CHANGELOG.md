# Changelog

## 1.1.0

- 新增模型自动挑选：`scripts/pick_image_model.py` 按效果优先级选出最佳**可用**生图模型
- 新增一键脚本：`scripts/generate_resume_photo.sh`（选模型 → 参考图编辑 → 落盘），自动适配各 provider 几何差异
- 明确 **DeepSeek V4 不产图**：其 API 全部模型 `output_modalities` 为 `["text"]`，仅支持图片输入；出图由图像模型承担
- 补充凭证配置方式与 `models set-image` / `models image-fallbacks` 用法

## 1.0.0

- 首次发布：生活照 → 专业简历照工作流
- 中英双版提示词模板 + 负向约束
- 背景 / 服装 / 场景预设
- 标准证件照尺寸裁剪脚本（magick / convert / ffmpeg / sips）
- 保身份、抗过度美颜的硬性约束与故障排查表
