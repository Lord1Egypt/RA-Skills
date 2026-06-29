# QR Code Generator

生成和解析二维码，支持 URL / vCard / WIFI / 纯文本四种模式，可自定义颜色、嵌入 Logo。

## 安装依赖

```bash
pip install qrcode pillow
# 解析功能（可选）：
pip install opencv-python
```

## 使用方式

### URL 模式

```bash
python3 scripts/qr_code.py url "https://example.com" -o qrcode.png
python3 scripts/qr_code.py url "https://example.com" -o qrcode.png --fg black --bg white
# 带 Logo
python3 scripts/qr_code.py url "https://example.com" -o qrcode.png --logo logo.png --logo-size 0.2
```

### WIFI 模式

```bash
# 有密码
python3 scripts/qr_code.py wifi -s "MyWiFi" -p "12345678" -o wifi.png
# 无密码
python3 scripts/qr_code.py wifi -s "FreeWiFi" -o wifi.png
# 隐藏网络
python3 scripts/qr_code.py wifi -s "MyWiFi" -p "12345678" --hidden -o wifi.png
```

### vCard 模式

```bash
python3 scripts/qr_code.py vcard -n "张三" -t "13800138000" -e "zhang@example.com" -o card.png
python3 scripts/qr_code.py vcard -n "张三" -t "13800138000" -u "https://zhang.com" -o card.png
```

### 纯文本模式

```bash
python3 scripts/qr_code.py text "任意文本内容" -o text.png
# 带 Logo
python3 scripts/qr_code.py text "任意文本内容" -o text.png --logo logo.png
```

### 解析二维码

```bash
python3 scripts/qr_code.py decode qrcode.png
```

## Logo 注意事项

- Logo 覆盖面积建议不超过 30%，过大可能导致部分老旧扫码器无法识别
- Logo 周围会自动留白边，提升扫码成功率
- 嵌入 Logo 时建议使用 `ERROR_CORRECT_H` 纠错级别（脚本已自动处理）
