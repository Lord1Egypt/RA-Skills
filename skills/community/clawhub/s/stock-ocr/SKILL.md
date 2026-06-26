---
name: stock-ocr
description: 从通达信金融终端窗口截取股票日K图，并使用OCR识别MA均线数值。当用户需要获取股票MA均线数值、分析均线支撑压力位、或需要对交易软件截图进行文字识别时使用此skill。触发词：MA、均线数值、截图识别、股票技术指标、通达信金融终端。
---

# Stock OCR

## 概述

这个skill帮助你从「通达信金融终端」窗口截取股票日K图，并自动识别提取MA5-MA60均线数值。

**完整工作流程：**
1. 输入股票代码 → 自动切换到对应股票
2. 按 **96** 切换到日K线界面
3. 截图左上角均线区域
4. OCR识别并提取MA20数值

## 使用场景

- "获取股票000001的MA20数值"
- "帮我查一下600000的MA20"
- "识别一下金长江窗口的MA20"
- "帮我截个图看看均线"

## 快速开始

```bash
# 使用默认OCR引擎
python scripts/capture_ma20_v2.py 000001

# 使用百度高精度OCR (推荐)
python scripts/capture_ma20_v2.py 000001 --engine baidu

# 对比所有OCR引擎效果
python scripts/capture_ma20_v2.py 000001 --compare-ocr

# 查看可用OCR引擎
python scripts/capture_ma20_v2.py --list-engines
```

**输出示例：**
```
正在查找窗口:通达信金融终端
✅ 找到窗口: 通达信金融终端- [分析图表-平安银行]

步骤1: 输入股票代码 000001
  ✅ 已输入股票代码

步骤2: 按96切换到日K线
  ✅ 已切换到日K线

步骤3: 截图均线区域
  区域: (0, 0) 450x100
  ✅ 截图成功: ma_region_20260329_120000.bmp (132.5KB)

步骤4: OCR识别MA20数值
  识别结果:
  MA5  12.35
  MA10 12.20
  MA20 11.98
  MA60 11.50

📊 找到的均线数值:
     MA5: 12.35
     MA10: 12.20
     MA20: 11.98
     MA60: 11.50

✅ MA20 = 11.98
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `-s, --stock-code` | **必填** 股票代码 | `000001`, `600000`, `07226` |
| `-w, --window-title` | 窗口标题关键词（默认：金长江） | `金长江网上交易财智版` |
| `-o, --output` | 截图保存路径 | `screenshot.bmp` |
| `--keep-screenshot` | 保留截图文件 | - |
| `--no-ocr` | 仅截图，不进行OCR识别 | - |
| `--delay` | 输入后等待时间(秒)，默认1.0 | `1.5` |

## 股票代码格式

支持以下格式：

| 类型 | 格式 | 示例 |
|------|------|------|
| A股 | 6位数字 | `000001`, `600000`, `300750` |
| 港股 | 1-5位数字 | `00700`, `07226` |
| 美股 | 1-5位字母 | `AAPL`, `TSLA` |

## 工作流程详解

### 1. 查找窗口
根据窗口标题模糊匹配「通达信金融终端」窗口。

### 2. 输入股票代码
```
┌─────────────────────────────────────┐
│  通达信金融终端                │
│  ┌─────────────────────────────────┐│
│  │ [股票代码输入框]                ││
│  │ 输入: 000001                   ││
│  │ 按回车确认                      ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

### 3. 按96回车切换日K线
**快捷键：96 + 回车**
- 输入 `96` 然后按回车
- 这是金长江软件切换到日K线界面的标准操作

### 4. 截图均线区域
截图窗口左上角区域（450x100像素），该区域包含均线数值：
```
┌─────────────────────────────────────┐
│ 日线 前复权  MA5 12.35 MA10 12.20...│  ← 截图区域
│ ┌─────────────────────────────────┐│
│ │                                 ││
│ │      K线图主体区域              ││
│ │                                 ││
│ └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

## OCR识别

支持多种OCR引擎,推荐使用 **百度OCR高精度版** 获得最佳数字识别效果。

### 可用OCR引擎

| 引擎 | 准确率 | 成本 | 推荐度 |
|------|--------|------|--------|
| **百度OCR高精度** | ⭐⭐⭐⭐⭐ | | ⭐⭐⭐⭐⭐ |
| **RapidOCR** | ⭐⭐⭐⭐ | 完全免费 | ⭐⭐⭐⭐ |
| **Windows内置OCR** | ⭐⭐⭐ | 完全免费 | ⭐⭐⭐ |
| **Tesseract** | ⭐⭐⭐ | 完全免费 | ⭐⭐ |

### 配置OCR引擎

详细配置步骤请参考: [OCR配置指南](docs/OCR配置指南.md)

**百度OCR配置 (推荐):**
```bash
# 方法1: 使用配置脚本 (推荐)
powershell -ExecutionPolicy Bypass -File scripts/configure_baidu_ocr.ps1 -ApiKey "your_api_key" -SecretKey "your_secret_key"

# 方法2: 手动设置环境变量
setx BAIDU_API_KEY "your_api_key"
setx BAIDU_SECRET_KEY "your_secret_key"

# 或者直接设置Access Token
setx BAIDU_ACCESS_TOKEN "your_access_token"
```

**当前配置状态: ✅ 已配置**
- API Key: `dNJctHLwok76vebSk8EP8aPG`
- Secret Key: 已设置
- 免费额度: 1000次/月

**RapidOCR配置:**
```bash
pip install rapidocr-onnxruntime
```

**安装依赖：**
```bash
# 基础依赖
pip install Pillow

# RapidOCR (可选)
pip install rapidocr-onnxruntime
```

## 常见问题

### 找不到窗口

**症状：** 提示"未找到包含 '通达信金融终端' 的窗口"

**解决方法：**
1. 确认金长江软件已打开
2. 检查窗口标题是否正确：
   ```bash
   # 列出所有窗口
   python -c "import ctypes; ..."
   ```

### 股票代码输入失败

**可能原因：**
1. 窗口未获得焦点 - 脚本会自动处理
2. 输入法干扰 - 切换到英文输入法
3. 延迟不够 - 增加 `--delay` 参数

**解决方法：**
```bash
# 增加等待时间
python scripts/capture_ma20.py -s 000001 --delay 2.0
```

### 日K线切换失败

**可能原因：**
1. 快捷键96被占用
2. 软件版本不同

**解决方法：**
手动切换到日K线后运行：
```bash
python scripts/capture_ma20.py -s 000001 --keep-screenshot
```

### OCR识别不准确

**解决方法：**
1. **使用百度高精度OCR** (推荐):
   ```bash
   python scripts/capture_ma20_v2.py 000001 --engine baidu
   ```
2. **对比所有引擎效果**:
   ```bash
   python scripts/capture_ma20_v2.py 000001 --compare-ocr
   ```
3. 使用 `--keep-screenshot` 保留截图检查质量
4. 确保金长江窗口在前台且清晰可见
5. 检查截图区域是否包含均线信息

### MA20提取失败

查看OCR识别的原始文本，确认MA20格式。如需调整匹配模式，可修改 `extract_ma20` 函数。

## 文件结构

```
stock-ma20-ocr/
├── SKILL.md                    # 本文档
├── docs/
│   └── OCR配置指南.md          # OCR引擎详细配置指南
├── scripts/
│   ├── capture_ma20_v2.py      # 核心脚本v2 (多OCR引擎支持)
│   ├── capture_ma20.py         # 原版脚本 (OCR.space)
│   ├── ocr_engines.py          # OCR引擎集成模块
│   ├── win_ocr_v2.py           # Windows OCR优化版
│   ├── capture_ma20_ctypes.py  # ctypes版本
│   ├── ocr_with_api.py         # 在线OCR API封装
│   ├── list_windows_file.py    # 列出所有窗口
│   └── test_ocr.py             # OCR测试脚本
└── references/
    └── ocr_config_guide.md     # OCR配置参考
```

## 依赖清单

```bash
# 基础依赖（必需）
pip install Pillow

# 可选：更好的图片处理
pip install pywin32
```

## 扩展功能

可轻松扩展识别其他指标：

```python
def extract_all_ma(text):
    """提取所有均线数值"""
    import re
    result = {}
    patterns = {
        'MA5': r'MA5[:\s]*(\d+\.?\d*)',
        'MA10': r'MA10[:\s]*(\d+\.?\d*)',
        'MA20': r'MA20[:\s]*(\d+\.?\d*)',
        'MA60': r'MA60[:\s]*(\d+\.?\d*)',
    }
    for name, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            result[name] = match.group(1)
    return result
```

## 版本历史

- **v2.1** - 集成多种OCR引擎 (百度高精度/RapidOCR/Windows/Tesseract),新增OCR对比功能
- **v2.0** - 使用96切换日K线，调整截图区域到左上角均线位置
- **v1.0** - 初始版本，使用F5+F8切换K线
