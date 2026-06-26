# URL Toolkit

URL 编码、解码、解析和构建工具包。

## 功能

- URL 编码/解码
- URL 解析（提取 scheme、host、path、query 等）
- 查询字符串解析/构建

## 安装

```bash
clawhub install url-toolkit
```

## 使用

```bash
# URL 编码
python3 skills/url-toolkit/scripts/url_toolkit.py encode --input "hello world"

# URL 解码
python3 skills/url-toolkit/scripts/url_toolkit.py decode --input "hello%20world"

# 解析 URL
python3 skills/url-toolkit/scripts/url_toolkit.py parse --input "https://example.com/path?q=test"

# 解析查询字符串
python3 skills/url-toolkit/scripts/url_toolkit.py query-parse --input "q=test&id=123"

# 构建查询字符串
python3 skills/url-toolkit/scripts/url_toolkit.py query-build --input '{"q":"test","id":123}'
```
