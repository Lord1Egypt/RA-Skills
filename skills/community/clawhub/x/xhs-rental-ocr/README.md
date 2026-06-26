# 小红书数据提取 OCR (XHS Rental OCR)

从小红书笔记图片中提取结构化数据（租金/面积/单价等），支持自动裁切长图、OCR 识别、导出 Excel。

## 🎯 功能特点

- ✅ **离线 OCR**：使用 Apple Vision 框架，无需网络
- ✅ **中文优化**：针对中文识别优化，准确率>90%
- ✅ **长图裁切**：自动裁切长图，提高识别率
- ✅ **结构化提取**：自动识别租金、面积、单价等字段
- ✅ **Excel 导出**：专业格式，包含边框、表头、统计

## 📦 安装

```bash
# 1. 克隆仓库
git clone https://github.com/zhuobao/xhs-rental-ocr.git
cd xhs-rental-ocr

# 2. 安装依赖
pip3 install -r requirements.txt
```

## 🚀 快速开始

### 基础用法

```bash
# 从本地图片提取
python3 scripts/extract_data.py --images image.jpg --output data.xlsx

# 裁切长图后识别（9 等分）
python3 scripts/extract_data.py --images long_image.jpg --slice 9 --output data.xlsx
```

### 高级用法

```bash
# 多张图片批量处理
python3 scripts/extract_data.py --images img1.jpg img2.jpg img3.jpg --output data.xlsx

# 指定识别语言
python3 scripts/extract_data.py --images image.jpg --languages "zh-Hans,en-US" --output data.xlsx

# 调整置信度阈值
python3 scripts/extract_data.py --images image.jpg --confidence 0.5 --output data.xlsx
```

## 📋 完整参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url` | 小红书笔记 URL（待实现） | - |
| `--images` | 本地图片路径（可多个） | - |
| `--output` | 输出文件路径 | `output.xlsx` |
| `--slice` | 长图裁切份数 | 1（不裁切） |
| `--languages` | OCR 语言 | `zh-Hans,en-US` |
| `--confidence` | 最低置信度 | 0.3 |

## 📤 输出示例

生成的 Excel 包含以下字段：

| 序号 | 图片 | 区域 | 板块 | 户型 | 面积 (平) | 月租金 (元) | 单价 (元/平) | 备注 |
|------|------|------|------|------|-----------|-------------|--------------|------|
| 1 | image-1 | 南山区 | 科技园 | 2 居室 | 65 | 6500 | 100 | |
| 2 | image-1 | 南山区 | 后海 | 3 居室 | 89 | 8900 | 100 | |
| 3 | image-2 | 福田区 | 车公庙 | 1 居室 | 35 | 4500 | 128 | |

## 🔧 依赖

- **Python 3.9+**
- **Pillow**（图片处理）
- **pyobjc-framework-Vision**（macOS OCR）
- **pyobjc-framework-Cocoa**
- **openpyxl**（Excel 导出）

## ⚠️ 注意事项

1. **macOS 专属**：依赖 Apple Vision 框架，仅支持 macOS
2. **图片质量**：建议使用高清原图（宽度>1000px）
3. **长图处理**：超过 2000px 高度的图片建议使用 `--slice` 参数裁切
4. **数据验证**：OCR 结果可能包含异常值，建议手动检查过滤

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License
