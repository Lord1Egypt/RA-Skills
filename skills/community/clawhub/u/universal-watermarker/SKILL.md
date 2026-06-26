---
name: Universal Watermarker
slug: universal-watermarker
version: 2.0.0
author: Cribug
tags: [pdf, image, tool, security, watermark]
---

# Universal Watermarker Skill

一款具有高度工程化水准的文件防伪处理工具。支持 PDF 与图片混批，内置响应式排版引擎，字体自动映射与文件全内置，彻底解决乱码、水印移位与缩放兼容性问题。

## 核心模式 (Modes)

1. **`diagonal` (对角单水印 - 默认)**：水印从画面左下角贯穿至右上角。极客级三角函数计算，无论文档是横是竖，均能保证完美端对端覆盖。
2. **`center` (居中单水印)**：水平放置于文档核心视角的正中央。
3. **`tile` (全图平铺)**：满屏交叉斜向覆盖，极致防伪。

## 运行环境
- **Language**: Python 3.8+
- **Dependencies**: pypdf, reportlab, Pillow
- **OS Support**: Windows, macOS, Linux (无系统级底层 GUI 依赖)

## 参数定义 (Parameters)

| 参数名 | 类型 | 必填 | 默认值 | 描述 |
| :--- | :--- | :--- | :--- | :--- |
| `files` | list/string | 是 | 无 | 待处理的文件路径（支持单个路径字符串或路径列表）。 |
| `text` | string | 是 | 无 | 水印文字内容（如 "内部机密"）。 |
| `opacity` | float | 否 | `0.3` | 水印不透明度，范围 0.0 到 1.0。 |
| `scale` | float | 否 | `None (智能默认)` | 响应式字体比例 (0.0~1.0)。<br>`diagonal` 默认 `0.8`（占据对角线 80%）<br>`center` 默认 `0.5`（占据画面宽度 50%）<br>`tile` 默认 `0.25`。 |
| `mode` | string | 否 | `"diagonal"` | 渲染模式：`"diagonal"`, `"center"`, `"tile"`。 |
| `angle` | int | 否 | `30` | 水印倾斜角度（仅在 `mode="tile"` 时生效）。 |
| `auto_adjust` | bool | 否 | `True` | 自动背景亮度感应，在 `color` 为 `None` 时智能切换深色/浅色水印。 |
| `color` | string/tuple | 否 | `None` | 自定义水印颜色，可传入十六进制 `"#FF0000"` 或 RGB 元组 `(255,0,0)`。若设置，将无视自动亮度调节。 |
| `font_path` | string | 否 | `"./fonts/AlibabaPuHuiTi-3-65-Medium.ttf"` | 字体文件路径，支持 .ttf 和 .ttc。 |

## 输入与输出规范 (I/O)
- **存储位置**: 处理后的文件直接保存在原文件所在目录下。
- **命名约定**: 输出文件名为 `wm_` 前缀加上原文件名。

## AI 调用指令参考 (Instructions for LLM)
1. **语义推断**：如果用户要求“防伪”、“机密保护”、“铺满”，请自动设置 `mode="tile"`。如果用户要求“淡一点”，请将 `opacity` 调低至 0.1-0.2。
2. **确认闭环**：执行 `process_files` 完毕后，必须向用户明确播报输出文件的确切路径和名称，不要让用户自己去寻找。
