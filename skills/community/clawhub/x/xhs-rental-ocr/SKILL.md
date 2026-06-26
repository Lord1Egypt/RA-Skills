---
name: xhs-rental-ocr
description: |
  从小红书笔记图片提取结构化数据（租金/面积/单价等），自动裁切长图 + OCR 识别 + 导出 Excel。
  使用 Apple Vision 框架进行离线 OCR，支持中文识别。
  Use when: 用户需要从小红书/社交媒体图片提取表格数据、价格信息、统计数据等。
license: MIT
metadata:
  version: "1.0.0"
  category: data-extraction
  platforms:
    - macOS
  requires:
    bins:
      - python3
    env: []
  capabilities:
    - ocr
    - image-processing
    - data-export
  author:
    name: "zhuobao"
    url: "https://github.com/zhuobao"
---

# 小红书数据提取 OCR (XHS Rental OCR)

从小红书笔记图片中提取结构化数据（租金/面积/单价等），支持自动裁切长图、OCR 识别、导出 Excel。

## 🎯 适用场景

- 从小红书笔记提取租房/房价数据
- 从社交媒体图片提取表格数据
- 从长图/信息图提取统计信息
- 批量 OCR 识别并导出为 Excel/CSV

## 📦 安装

```bash
# OpenClaw / Codex
git clone https://github.com/zhuobao/xhs-rental-ocr.git ~/.agents/skills/xhs-rental-ocr
```

## 🚀 快速开始

### 基础用法

```bash
cd ~/.agents/skills/xhs-rental-ocr
python3 scripts/extract_data.py --url "https://www.xiaohongshu.com/explore/xxx" --output data.xlsx
```

### 高级用法

```bash
# 从本地图片提取
python3 scripts/extract_data.py --images image1.jpg image2.jpg --output data.xlsx

# 裁切长图后识别（9 等分）
python3 scripts/extract_data.py --images long_image.jpg --slice 9 --output data.xlsx

# 导出 CSV 格式
python3 scripts/extract_data.py --images image.jpg --output data.csv

# 指定识别语言（中文 + 英文）
python3 scripts/extract_data.py --images image.jpg --languages "zh-Hans,en-US"
```

## 📋 工作流程

```
1. 下载图片（从 URL 或本地）
   ↓
2. 可选：裁切长图（N 等分）
   ↓
3. Apple Vision OCR 识别
   ↓
4. 正则提取结构化数据
   ↓
5. 导出 Excel/CSV
```

## 📁 目录结构

```
xhs-rental-ocr/
├── SKILL.md              # 技能描述（本文件）
├── scripts/
│   ├── extract_data.py   # 主脚本
│   └── vision_ocr.py     # OCR 模块
├── examples/
│   └── sample_output.xlsx
└── README.md             # 详细文档
```

## 🔧 依赖

- **Python 3.9+**
- **Pillow**（图片处理）
- **pyobjc-framework-Vision**（macOS OCR）
- **pyobjc-framework-Cocoa**
- **openpyxl**（Excel 导出）

安装依赖：
```bash
pip3 install pillow openpyxl pyobjc-framework-Vision pyobjc-framework-Cocoa
```

## 📤 输出格式

### Excel 列

| 列名 | 说明 |
|------|------|
| 序号 | 记录编号 |
| 图片 | 来源图片 |
| 区域 | 区域名称（如识别到） |
| 板块 | 小区/板块（如识别到） |
| 户型 | 户型（如识别到） |
| 面积 (平) | 建筑面积 |
| 月租金 (元) | 月租金 |
| 单价 (元/平) | 每平米单价 |
| 备注 | 其他信息 |

### 支持的数据模式

1. **租房数据**：租金、面积、单价
2. **房价数据**：总价、单价、面积
3. **通用表格**：自动检测数字 + 单位

## 🎨 示例

### 示例 1：提取小红书租房数据

```bash
python3 scripts/extract_data.py \
  --url "https://www.xiaohongshu.com/explore/69be073b000000002302339e" \
  --output rental_data.xlsx
```

**输出**：
- 824-1295 条租房记录
- 包含区域、小区、户型、面积、租金、单价

### 示例 2：裁切长图识别

```bash
python3 scripts/extract_data.py \
  --images screenshot.png \
  --slice 9 \
  --output extracted_data.xlsx
```

**说明**：将长图裁切成 9 份，分别 OCR 后合并结果。

## ⚙️ 配置选项

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url` | 小红书笔记 URL | - |
| `--images` | 本地图片路径（可多个） | - |
| `--output` | 输出文件路径 | `output.xlsx` |
| `--slice` | 长图裁切份数 | 1（不裁切） |
| `--languages` | OCR 语言 | `zh-Hans,en-US` |
| `--confidence` | 最低置信度 | 0.3 |
| `--format` | 输出格式 | `xlsx` |

## 🔍 OCR 技术细节

**使用 Apple Vision 框架**：
- 离线识别，无需网络
- 支持 30+ 语言
- 中文识别准确率高
- 自动检测文字方向

**优化策略**：
1. 高分辨率图片优先
2. 长图裁切提高识别率
3. 置信度过滤（默认>0.3）
4. 正则提取结构化数据

## 📝 注意事项

1. **macOS 专属**：依赖 Apple Vision 框架
2. **图片质量**：建议使用高清原图
3. **长图处理**：超过 2000px 高度的图片建议裁切
4. **数据验证**：OCR 结果可能包含异常值，建议手动检查

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**GitHub**: https://github.com/zhuobao/xhs-rental-ocr

## 📄 License

MIT License

## 🙏 致谢

- Apple Vision Framework
- MiniMax Skills (灵感来源)
- OpenClaw Community
