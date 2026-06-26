# OCR配置指南

## Tesseract-OCR 安装与配置

### Windows安装步骤

1. **下载安装包**
   - 访问: https://github.com/UB-Mannheim/tesseract/wiki
   - 下载最新版安装程序（如 tesseract-ocr-w64-setup-5.3.0.20221219.exe）

2. **安装时选择语言包**
   - 勾选 `Chinese - Simplified` (chi_sim)
   - 勾选 `Chinese - Traditional` (chi_tra) 如需要

3. **添加环境变量**
   ```powershell
   # 添加到PATH
   $env:PATH += ";C:\Program Files\Tesseract-OCR"
   
   # 或在Python代码中设置
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

4. **验证安装**
   ```bash
   tesseract --version
   tesseract --list-langs
   ```

### 提高识别准确率

1. **图片预处理**
   ```python
   from PIL import Image, ImageEnhance, ImageFilter
   
   # 打开图片
   img = Image.open('screenshot.png')
   
   # 转为灰度
   img = img.convert('L')
   
   # 增强对比度
   enhancer = ImageEnhance.Contrast(img)
   img = enhancer.enhance(2.0)
   
   # 锐化
   img = img.filter(ImageFilter.SHARPEN)
   
   # 保存预处理后的图片
   img.save('screenshot_enhanced.png')
   ```

2. **Tesseract配置选项**
   ```python
   import pytesseract
   
   # 自定义配置
   custom_config = r'--oem 3 --psm 6 -l chi_sim+eng'
   text = pytesseract.image_to_string(img, config=custom_config)
   ```
   
   参数说明：
   - `--oem 3`: 使用LSTM神经网络引擎
   - `--psm 6`: 假设图片是统一的文本块
   - `-l chi_sim+eng`: 中英文混合识别

## 在线OCR服务对比

| 服务商 | 免费额度 | 准确率 | 响应速度 | 中文支持 |
|--------|----------|--------|----------|----------|
| 百度OCR | 每月1000次 | 高 | 快 | 优秀 |
| 腾讯云OCR | 每月1000次 | 很高 | 快 | 优秀 |
| 阿里云OCR | 每月500次 | 高 | 很快 | 优秀 |

### 百度OCR配置

1. **获取Access Token**
   - 注册百度智能云: https://cloud.baidu.com
   - 创建OCR应用
   - 获取API Key和Secret Key
   - 通过API获取Access Token:
     ```bash
     curl -X POST 'https://aip.baidubce.com/oauth/2.0/token' \
       -d 'grant_type=client_credentials' \
       -d 'client_id=YOUR_API_KEY' \
       -d 'client_secret=YOUR_SECRET_KEY'
     ```

2. **设置环境变量**
   ```powershell
   $env:BAIDU_ACCESS_TOKEN = "your_access_token"
   ```

### 腾讯云OCR配置

1. **获取密钥**
   - 注册腾讯云: https://cloud.tencent.com
   - 开通OCR服务
   - 获取SecretId和SecretKey

2. **设置环境变量**
   ```powershell
   $env:TENCENT_SECRET_ID = "your_secret_id"
   $env:TENCENT_SECRET_KEY = "your_secret_key"
   ```

3. **安装SDK**
   ```bash
   pip install tencentcloud-sdk-python-ocr
   ```

### 阿里云OCR配置

1. **获取密钥**
   - 注册阿里云: https://www.aliyun.com
   - 开通OCR服务
   - 获取AccessKey ID和AccessKey Secret

2. **设置环境变量**
   ```powershell
   $env:ALIYUN_ACCESS_KEY_ID = "your_access_key_id"
   $env:ALIYUN_ACCESS_KEY_SECRET = "your_access_key_secret"
   ```

3. **安装SDK**
   ```bash
   pip install alibabacloud-ocr-api20210707
   ```

## MA20数值提取模式

根据不同的显示格式，可以使用以下正则表达式：

```python
import re

# 模式1: MA20: 12.34 或 MA20 12.34
pattern1 = r'MA20[：:\s]*(\d+\.?\d*)'

# 模式2: MA20(12.34) 或 MA20[12.34]
pattern2 = r'MA20[\(\[]?(\d+\.?\d*)[\)\]]?'

# 模式3: 20日均线: 12.34 (中文格式)
pattern3 = r'20日均线[：:\s]*(\d+\.?\d*)'

# 模式4: MA20=12.34
pattern4 = r'MA20\s*=\s*(\d+\.?\d*)'

# 模式5: 20MA: 12.34 (变体格式)
pattern5 = r'20MA[：:\s]*(\d+\.?\d*)'

# 组合所有模式
def extract_ma20(text):
    patterns = [pattern1, pattern2, pattern3, pattern4, pattern5]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None
```

## 故障排除

### Tesseract找不到

**错误信息：**
```
TesseractNotFoundError: tesseract is not installed or it's not in your PATH
```

**解决方法：**
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 中文识别乱码

**原因：** 未安装中文语言包

**解决方法：**
1. 运行安装程序，选择修改
2. 勾选 Chinese - Simplified
3. 或手动下载语言包到 tessdata 目录

### 窗口截图黑屏

**原因：** 窗口最小化或被遮挡

**解决方法：**
1. 确保窗口可见且在前台
2. 脚本已包含 `SetForegroundWindow` 自动激活窗口

### API调用失败

**常见错误：**
- `401 Unauthorized`: Access Token过期或错误
- `403 Forbidden`: 未开通对应服务
- `429 Too Many Requests`: 超过调用频率限制

**解决方法：**
1. 检查API密钥是否正确
2. 确认已开通OCR服务
3. 查看剩余配额
