# 微信公众号文章解析器

解析微信公众号文章，自动提取标题、作者、正文内容，支持保存到飞书多维表格。

## 📦 安装

### 步骤 1：安装依赖

```bash
pip3 install requests beautifulsoup4 python-dotenv
```

或使用 requirements.txt：

```bash
pip3 install -r requirements.txt
```

### 步骤 2：验证安装

```bash
python3 scripts/wechat_parser.py
```

应该显示使用说明，表示安装成功。

## 🚀 快速开始

### 基本用法：解析文章

```bash
python3 scripts/wechat_parser.py "https://mp.weixin.qq.com/s/xxxxx"
```

无需任何配置，开箱即用！

## ⚙️ 飞书保存功能配置（可选）

如需将文章保存到飞书多维表格，需要额外配置。

### 步骤 1：创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn)
2. 创建企业自建应用
3. 获取 `App ID` 和 `App Secret`

### 步骤 2：开通权限

在应用的「权限管理」中开通：

- `bitable:app:readonly` - 查看多维表格
- `bitable:app` - 读写多维表格

### 步骤 3：创建多维表格

创建一个飞书多维表格，包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 文本 | 文本 | 文章标题 |
| 链接 | 超链接 | 文章 URL |
| 来源 | 单选 | 平台来源 |
| 保存时间 | 日期时间 | 保存时间 |
| 摘要 | 多行文本 | 摘要+正文 |

**单选「来源」的选项：**
- 微信公众号
- 知乎
- 今日头条
- 小红书
- B站
- 抖音
- 其他

### 步骤 4：获取表格信息

从表格 URL 中获取：
```
https://xxx.feishu.cn/base/APP_TOKEN?table=TABLE_ID
                            ↑                ↑
                       APP_TOKEN         TABLE_ID
```

### 步骤 5：配置环境变量

复制配置模板：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
FEISHU_APP_ID=cli_xxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxx
FEISHU_APP_TOKEN=xxxxxxxxx
FEISHU_TABLE_ID=tblxxxxxxxxx
```

### 步骤 6：验证配置

```bash
python3 scripts/save_to_feishu.py "https://mp.weixin.qq.com/s/xxxxx"
```

## 📖 使用指南

### 解析文章（无需配置）

```bash
# 基本解析
python3 scripts/wechat_parser.py "URL"

# 解析并保存到文件
python3 scripts/wechat_parser.py "URL" --save

# 指定输出文件名
python3 scripts/wechat_parser.py "URL" --save --output article.json
```

### 保存到飞书（需配置）

```bash
# 自动提取标题
python3 scripts/save_to_feishu.py "URL"

# 手动指定标题
python3 scripts/save_to_feishu.py "URL" "自定义标题"
```

## 📁 文件结构

```
wechat-article-parser/
├── README.md             # 本文档（安装说明）
├── SKILL.md              # Skill 描述文件
├── QUICKSTART.md         # 快速开始指南
├── requirements.txt      # Python 依赖
├── .env.example          # 配置模板
├── .gitignore            # Git 忽略文件
└── scripts/
    ├── wechat_parser.py       # 核心解析脚本
    └── save_to_feishu.py      # 飞书保存脚本
```

## ❓ 常见问题

### Q1: 提取的内容不完整？

微信有反爬机制，部分文章可能提取不完整。建议：
- 多尝试几次
- 手动复制重要段落

### Q2: 飞书保存失败？

检查：
1. `.env` 配置是否正确
2. 飞书应用权限是否开通
3. 表格字段名是否匹配

### Q3: 表格字段名和脚本不一致？

修改 `scripts/save_to_feishu.py` 中的字段名映射：

```python
fields = {
    "你的标题字段名": title,
    "你的链接字段名": {"link": url},
    ...
}
```

### Q4: 如何批量处理多个链接？

创建链接列表文件 `links.txt`，每行一个 URL：

```bash
while read url; do
  python3 scripts/wechat_parser.py "$url" --save
  sleep 2  # 避免请求过快
done < links.txt
```

## 📄 许可证

MIT License

## 🔗 相关链接

- [飞书开放平台](https://open.feishu.cn)
- [飞书多维表格 API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/bitable-v1/app-table-record/create)
