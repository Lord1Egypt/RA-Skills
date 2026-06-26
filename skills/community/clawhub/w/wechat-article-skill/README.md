# wechat-article

微信公众号文章正文提取工具。从 `mp.weixin.qq.com/s/` 链接抓取 HTML，解析 `#page-content` 正文并输出纯文本。

## 安装

```bash
pip install -r requirements.txt
```

## 用法

```bash
python scripts/get_content.py --url "https://mp.weixin.qq.com/s/xxx"
```

- **成功**：正文输出到 stdout
- **失败**：stderr 输出错误及建议（如改用浏览器）

## 依赖

- beautifulsoup4
- certifi（解决 macOS SSL 证书校验）

## License

MIT
