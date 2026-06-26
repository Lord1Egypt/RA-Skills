---
name: software-ui-design
description: 软件UI设计辅助技能，涵盖设计文件解析（Figma/Sketch/Adobe XD）、自动标注、切图整理、UI规范检查、设计稿对比、设计系统文档生成。触发场景：解析设计稿、自动标注、设计资产导出、UI规范验证、切图整理、设计转代码、颜色/字体规范提取。
---

# Software UI Design - UI设计自动化

## 核心能力

### 设计文件解析
- **Figma**：通过 Figma API / figma-python 解析文件，提取图层、组件、样式
- **Sketch**：解析 .sketch 文件（JSON 格式），提取画板、符号、样式
- **Adobe XD**：解析 .xd 文件（ZIP + JSON），提取 artboard、组件

### 自动标注
- 提取元素位置、尺寸、间距、颜色、字体信息
- 生成标注文档（Markdown / HTML / JSON）
- 支持多状态标注（默认/悬停/激活/禁用）

### 切图 & 资产导出
- 自动识别需要导出的元素
- 支持多分辨率导出（1x / 2x / 3x）
- 输出格式：PNG / SVG / PDF / WebP
- 整理为规范目录结构

### UI 规范检查
- 颜色规范验证（品牌色是否正确使用）
- 字体规范验证（字号/字重/行高）
- 间距规范验证（8px 栅格系统）
- 输出规范差距报告

### 设计转代码
- 生成 CSS / Tailwind / Flutter / SwiftUI / Jetpack Compose 代码片段
- 从设计稿提取组件结构和样式属性

### 关键脚本
- `scripts/figma_parser.py` - Figma API 文件解析
- `scripts/sketch_parser.py` - Sketch 文件解析
- `scripts/annotate.py` - 自动标注生成
- `scripts/export_assets.py` - 批量导出切图
- `scripts/ui_checker.py` - UI 规范检查
- `scripts/design_to_code.py` - 设计转代码片段

### 参考资源
- `references/figma-api.md` - Figma API 文档
- `references/design-systems.md` - 主流设计系统规范参考

## 工作流程

1. **获取设计文件**：用户提供 Figma 链接 / Sketch / XD 文件路径
2. **解析提取**：调用解析脚本获取图层结构
3. **执行任务**：标注 / 切图 / 规范检查 / 代码生成
4. **输出交付**：文档 / 资产包 / 报告

## 注意事项
- Figma 需要用户提供 Personal Access Token
- Sketch/XD 文件较大，建议压缩或提供具体画板范围
- 切图优先导出 SVG 再转 PNG
- 代码生成仅作参考，需人工审核
