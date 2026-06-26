---
name: svg-to-png
description: 将 SVG 矢量图片转换为 PNG 格式，支持指定尺寸。使用场景：(1) 将 SVG 图标转换为 PNG，(2) 调整图片尺寸，(3) 前端资源格式转换。使用前需在当前目录安装 sharp 依赖。
---

# SVG 转 PNG 技能 🖼️

## 安装依赖

在使用该技能前，需要在当前目录安装 sharp：

```bash
npm install sharp
```

## 使用方法

```bash
node <skill>/scripts/convert.js <输入SVG路径> [输出PNG路径] [尺寸]
```

### 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|-----|-----|-------|------|
| 输入SVG路径 | ✅ | - | 要转换的 SVG 文件路径 |
| 输出PNG路径 | ❌ | 同名 .png | 输出文件路径 |
| 尺寸 | ❌ | 1024 | 输出图片宽高（正方形） |

### 示例

```bash
# 转换并输出 1024x1024
node skills/svg-to-png/scripts/convert.js icon.svg icon.png 1024

# 使用默认尺寸 1024
node skills/svg-to-png/scripts/convert.js icon.svg icon.png

# 指定不同尺寸
node skills/svg-to-png/scripts/convert.js logo.svg logo.png 512
```

## 工作原理

使用 sharp 库读取 SVG 文件，调整为指定尺寸后输出为 PNG 格式。