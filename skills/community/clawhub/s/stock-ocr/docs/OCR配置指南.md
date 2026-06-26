# OCR引擎配置指南

本文档介绍如何配置不同OCR引擎以提高数字识别准确率。

## 📊 OCR引擎对比

| 引擎 | 准确率 | 速度 | 成本 | 安装难度 | 推荐度 |
|------|--------|------|------|----------|--------|
| **百度OCR高精度版** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 免费1000次/月 | 简单 | ⭐⭐⭐⭐⭐ |
| **RapidOCR** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 完全免费 | 中等 | ⭐⭐⭐⭐ |
| **Windows内置OCR** | ⭐⭐⭐ | ⭐⭐⭐ | 完全免费 | 无需安装 | ⭐⭐⭐ |
| **Tesseract** | ⭐⭐⭐ | ⭐⭐⭐⭐ | 完全免费 | 复杂 | ⭐⭐ |

---

## 🚀 方案一: 百度OCR高精度版 (推荐)

**优点:**
- 数字识别准确率最高 (99%+)
- 每月免费1000次调用
- 支持中英文混合
- 响应速度快

**配置步骤:**

1. **注册百度智能云账号**
   - 访问: https://cloud.baidu.com/
   - 注册并登录

2. **创建OCR应用**
   - 进入控制台: https://console.bce.baidu.com/ai/#/ai/ocr/overview/index
   - 点击"创建应用"
   - 应用名称: `stock-ma20-ocr`
   - 选择"通用文字识别"
   - 确认创建

3. **获取密钥**
   - 在应用详情页找到:
     - API Key
     - Secret Key
   - 或者使用Access Token

4. **配置环境变量**
   
   **Windows PowerShell (临时):**
   ```powershell
   $env:BAIDU_API_KEY = "your_api_key"
   $env:BAIDU_SECRET_KEY = "your_secret_key"
   ```
   
   **Windows PowerShell (永久):**
   ```powershell
   [System.Environment]::SetEnvironmentVariable('BAIDU_API_KEY', 'your_api_key', 'User')
   [System.Environment]::SetEnvironmentVariable('BAIDU_SECRET_KEY', 'your_secret_key', 'User')
   ```
   
   **或者直接使用Access Token:**
   ```powershell
   $env:BAIDU_ACCESS_TOKEN = "your_access_token"
   ```

5. **测试**
   ```bash
   python ocr_engines.py ma_region.bmp --engine baidu
   ```

---

## 🎯 方案二: RapidOCR (本地运行)

**优点:**
- 完全免费,无限制
- 本地运行,无需网络
- 基于PaddleOCR优化
- 中文识别优秀

**安装步骤:**

1. **安装依赖**
   ```bash
   pip install rapidocr-onnxruntime
   # 或者安装完整版
   pip install rapidocr
   ```

2. **验证安装**
   ```bash
   python -c "from rapidocr_onnxruntime import RapidOCR; print('OK')"
   ```

3. **测试**
   ```bash
   python ocr_engines.py ma_region.bmp --engine rapidocr
   ```

**注意事项:**
- 首次运行会下载模型文件 (~100MB)
- 需要网络连接下载模型
- 之后可离线使用

---

## 🪟 方案三: Windows内置OCR

**优点:**
- 无需安装
- 完全免费
- Windows 10/11内置

**缺点:**
- 数字识别准确率一般
- PowerShell调用较慢
- 需要Windows 10/11

**使用方法:**

直接使用,无需配置:
```bash
python ocr_engines.py ma_region.bmp --engine windows
```

**故障排除:**

如果出现编码错误:
1. 确保系统语言支持中文
2. 使用 `win_ocr_v2.py` 优化版本
3. 检查Windows版本 (需要1703+)

---

## 🔧 方案四: Tesseract OCR

**优点:**
- 开源免费
- 支持多语言
- 可训练自定义模型

**安装步骤:**

1. **下载安装包**
   - 访问: https://github.com/UB-Mannheim/tesseract/wiki
   - 下载最新版本 (推荐5.x)
   - 安装时勾选"Additional language data" -> "Chinese - Simplified"

2. **添加到PATH**
   - 默认路径: `C:\Program Files\Tesseract-OCR`
   - 添加到系统环境变量PATH

3. **验证安装**
   ```bash
   tesseract --version
   ```

4. **测试**
   ```bash
   python ocr_engines.py ma_region.bmp --engine tesseract
   ```

**优化数字识别:**

创建配置文件 `digits.conf`:
```
tessedit_char_whitelist 0123456789.MA
psm 6
```

使用配置:
```bash
tesseract image.png stdout digits.conf
```

---

## 📝 推荐配置方案

### 个人使用 (免费)
1. **首选:** 百度OCR高精度版 (每月1000次免费额度)
2. **备选:** RapidOCR (本地运行)

### 企业使用 (大量调用)
1. **首选:** 百度OCR高精度版 (付费套餐)
2. **备选:** RapidOCR集群部署

### 完全离线环境
1. **首选:** RapidOCR
2. **备选:** Tesseract OCR

---

## 🔍 对比测试

使用 `--compare` 参数对比所有引擎:

```bash
python capture_ma20_v2.py 07226 --compare-ocr
```

输出示例:
```
==================================================
引擎: WINDOWS
==================================================
MA5  3.720  MA10  3.922  MA20  3.953  MA60  4.780

==================================================
引擎: BAIDU
==================================================
MA5:3.720  MA10:3.922  MA20:3.953  MA60:4.780

==================================================
引擎: RAPIDOCR
==================================================
MA5:3.720 MA10:3.922 MA20:3.953 MA60:4.780
```

---

## ❓ 常见问题

### Q1: 百度OCR提示"Access token expired"
**A:** Access Token有效期30天,需要重新获取或使用API Key自动获取。

### Q2: RapidOCR模型下载失败
**A:** 
1. 检查网络连接
2. 手动下载模型: https://github.com/RapidAI/RapidOCR
3. 放到 `~/.rapidocr/` 目录

### Q3: Windows OCR识别乱码
**A:** 
1. 使用 `win_ocr_v2.py` 优化版本
2. 确保系统安装了中文语言包
3. 尝试转换图片为PNG格式

### Q4: 如何提高数字识别准确率?
**A:** 
1. **截图优化:**
   - 确保均线区域清晰
   - 避免截图压缩
   - 适当放大窗口

2. **OCR引擎选择:**
   - 百度高精度版 > RapidOCR > Windows OCR

3. **图片预处理:**
   - 转换为PNG格式
   - 调整对比度
   - 二值化处理

---

## 📞 技术支持

如有问题,请检查:
1. 环境变量是否正确配置
2. 网络连接是否正常
3. Python依赖是否完整安装

**依赖清单:**
```bash
pip install Pillow requests
pip install rapidocr-onnxruntime  # 可选
pip install tencentcloud-sdk-python-ocr  # 可选(腾讯云OCR)
```
