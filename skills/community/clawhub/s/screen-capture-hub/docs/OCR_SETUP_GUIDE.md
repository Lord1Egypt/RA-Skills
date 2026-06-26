# Tesseract OCR 安装和配置指南

## 📝 概述

**OPENCLAW(龙虾)-屏幕查看器** 的OCR功能依赖于Tesseract OCR引擎。Tesseract是一个开源的OCR引擎，支持100多种语言，包括中文、英文等。

## 🚀 快速安装（Windows）

### 方法1：自动安装脚本（推荐）

运行以下脚本自动下载和安装Tesseract OCR：

```bash
python scripts/install_tesseract.py
```

### 方法2：手动下载安装

1. **下载Tesseract OCR**
   - 访问：https://github.com/UB-Mannheim/tesseract/wiki
   - 下载最新版本的安装程序（如 `tesseract-ocr-w64-setup-5.4.0.20241124.exe`）

2. **安装步骤**
   - 运行下载的安装程序
   - 选择安装语言（建议选择英文）
   - 接受许可证协议
   - 选择安装路径（建议使用默认路径）
   - 等待安装完成

3. **配置环境变量**
   - 安装程序通常会自动添加环境变量
   - 如果没有，请手动将Tesseract安装目录添加到PATH
     - 默认路径：`C:\Program Files\Tesseract-OCR\`

## 🌍 语言包安装

### 中文支持（简体中文）

Tesseract安装时可以选择安装语言包。如果安装时未选择中文包，请按以下步骤安装：

1. **手动下载语言包**
   - 中文（简体）：https://github.com/tesseract-ocr/tessdata/blob/main/chi_sim.traineddata
   - 英文：https://github.com/tesseract-ocr/tessdata/blob/main/eng.traineddata

2. **安装语言包**
   - 下载的文件放置在Tesseract的`tessdata`目录下
   - 默认路径：`C:\Program Files\Tesseract-OCR\tessdata\`

## 🔧 验证安装

### 命令行验证

```bash
# 检查Tesseract版本
tesseract --version

# 列出支持的语言
tesseract --list-langs
```

### Python验证

```python
import pytesseract

# 设置Tesseract路径（如果需要）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 测试OCR功能
print(pytesseract.get_tesseract_version())
print(pytesseract.get_languages(config=''))
```

## 🛠️ 常见问题解决

### 问题1：找不到tesseract

**错误信息**：
```
TesseractNotFoundError: tesseract is not installed or it's not in your PATH
```

**解决方案**：
1. 检查Tesseract是否已安装
2. 检查环境变量是否配置正确
3. 或者在Python代码中指定路径：
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'完整路径\tesseract.exe'
   ```

### 问题2：不支持的语言

**错误信息**：
```
Error opening data file \tessdata\chi_sim.traineddata
```

**解决方案**：
1. 下载对应的语言包
2. 放置到正确的`tessdata`目录中

### 问题3：OCR识别效果差

**优化建议**：
1. **预处理图像**
   ```python
   # 转换为灰度图
   image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
   # 二值化
   _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
   ```

2. **调整参数**
   ```python
   # 使用更好的配置
   text = pytesseract.image_to_string(
       image,
       lang='chi_sim+eng',  # 中英文混合
       config='--psm 6 --oem 3'
   )
   ```

## 📚 语言代码参考

| 语言 | 代码 | 用途 |
|------|------|------|
| 英语 | `eng` | 英文文本识别 |
| 简体中文 | `chi_sim` | 简体中文识别 |
| 繁体中文 | `chi_tra` | 繁体中文识别 |
| 日语 | `jpn` | 日文识别 |
| 韩语 | `kor` | 韩文识别 |
| 多语言 | `eng+chi_sim` | 中英文混合识别 |

## 🎯 高级配置

### Tesseract配置参数

```python
# 常用的配置参数
config_params = {
    '--psm': '页面分割模式 (0-13)',
    '--oem': 'OCR引擎模式 (0-3)',
    '--dpi': '图像DPI设置',
    '--user-words': '用户词典文件',
    '--user-patterns': '用户模式文件'
}
```

### 推荐的PSM模式

- `3`：自动页面分割，但无方向检测
- `6`：假设为一个统一文本块
- `11`：尽量识别为单行文本

### 性能优化

1. **限制识别区域**
   ```python
   # 只识别特定区域
   region = image[y1:y2, x1:x2]
   text = pytesseract.image_to_string(region, lang='chi_sim')
   ```

2. **批量处理优化**
   ```python
   # 预加载模型
   import pytesseract
   from PIL import Image
   
   # 一次加载，多次使用
   def init_ocr():
       config = r'--oem 3 --psm 6'
       return lambda img: pytesseract.image_to_string(img, lang='chi_sim', config=config)
   
   ocr_engine = init_ocr()
   ```

## 🔗 资源链接

- **官方项目**: https://github.com/tesseract-ocr/tesseract
- **Windows安装**: https://github.com/UB-Mannheim/tesseract/wiki
- **语言包**: https://github.com/tesseract-ocr/tessdata
- **文档**: https://tesseract-ocr.github.io/

## 📊 支持的平台

| 平台 | 安装方法 | 备注 |
|------|----------|------|
| Windows | 自动安装脚本 | 支持64位系统 |
| macOS | `brew install tesseract` | 需要Homebrew |
| Linux | `apt-get install tesseract-ocr` | 根据发行版选择 |

## 🤝 社区支持

如果遇到问题，请：
1. 查看本项目的问题反馈区
2. 参考Tesseract官方文档
3. 加入相关技术社区讨论

---

**注意**: Tesseract OCR是独立的开源项目，安装和配置可能需要管理员权限。