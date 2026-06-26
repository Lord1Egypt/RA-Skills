# 微信公众号文章总结工具

## 项目结构

```
wechat-article-explainer/
├── scripts/wechat_reader.py        # Python 解析工具
├── SKILL.md #  Skill 定义
├── requirements.txt        # Python 依赖
└── README.md              # 说明文档
```

## 安装

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器（可选但推荐）
playwright install chromium
```

## 使用方法

### 命令行直接使用

```bash
# 使用浏览器模式（推荐，更稳定）
python3 wechat_reader.py "https://mp.weixin.qq.com/s/xxxx"

# 不使用浏览器
python3 wechat_reader.py "https://mp.weixin.qq.com/s/xxxx" --no-browser

# 输出到文件
python3 wechat_reader.py "https://mp.weixin.qq.com/s/xxxx" -o result.json
```

### Openclaw 中使用

1. 将 `SKILL.md` 放到 openclaw 的 skill 目录
2. 使用 `/wechat-article-explainer` 命令调用
3. 提供微信公众号链接，skill 会自动抓取并总结

## Skill 调用流程

1. 用户提供微信文章链接
2. Skill 调用 `wechat_reader.py` 抓取文章
3. 解析返回的 JSON 内容
4. 提供结构化总结

## 输出格式

```json
{
  "success": true,
  "url": "原始链接",
  "title": "文章标题",
  "author": "作者",
  "publish_date": "发布时间",
  "source": "来源公众号",
  "content": "文章内容"
}
```

## 注意事项

- 微信文章可能有防盗链限制
- 浏览器模式成功率更高
- 如遇抓取失败，建议用户在微信中打开文章并复制内容
