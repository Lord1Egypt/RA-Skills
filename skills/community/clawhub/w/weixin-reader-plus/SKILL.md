# weixin_reader

读取微信公众号文章内容。

## 触发条件

当用户提供微信公众号文章链接（mp.weixin.qq.com）并要求阅读、读取、查看文章内容时使用此 skill。

触发关键词：
- "读这篇微信文章"
- "看一下这个公众号文章"
- "帮我读取微信文章"
- 用户发送 mp.weixin.qq.com 链接

## 使用方法

```bash
python3 ~/.claude/skills/weixin_reader/weixin_reader.py "<微信文章URL>"
```

## 示例

```bash
python3 ~/.claude/skills/weixin_reader/weixin_reader.py "https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx"
```

## 输出格式

```
标题: 文章标题
公众号: 公众号名称

--- 正文内容 ---

文章正文内容...
```

## 依赖

- httpx
- beautifulsoup4

如未安装，运行：
```bash
pip install httpx beautifulsoup4
```

## 注意事项

1. 部分文章可能需要验证码，无法直接读取
2. 使用移动端 User-Agent 模拟微信内置浏览器访问
3. 支持自动跟随重定向
