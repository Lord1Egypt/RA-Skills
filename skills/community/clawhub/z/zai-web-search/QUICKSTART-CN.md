# Z.AI Web Search API - 快速上手

> 想要更详细的配置说明？请查看 [README.md](README.md)

## 30 秒快速配置

### 1. 获取 API Key

访问 [https://open.bigmodel.cn](https://open.bigmodel.cn) 注册并获取 API Key

### 2. 创建配置文件

```bash
# 进入 skill 文件夹
cd ~/.openclaw/skills/zai-web-search

# 复制示例并编辑
cp config.json.example config.json
```

**⚠️ 重要**：`config.json.example` 包含注释，复制后请删除所有 `//` 注释，否则会报错

### 3. 填写 API Key

打开 `config.json`，替换 `apiKey` 字段：

```json
{
  "apiKey": "把你的API Key粘贴到这里"
}
```

## 立即使用

```bash
# 搜索
zai-search "哈尔滨冰雪大世界 2026"

# 更多结果
zai-search "React 教程" --count 20

# 指定引擎
zai-search "人工智能" --engine search_pro
```

## 速查表

| 命令 | 说明 |
|------|------|
| `-e, --engine` | 搜索引擎：`search_std` / `search_pro` / `search_pro_sogou` / `search_pro_quark` |
| `-c, --count` | 结果数量：1-50 |
| `-r, --recency` | 时间：`oneDay` / `oneWeek` / `oneMonth` / `oneYear` / `noLimit` |
| `-s, --content` | 内容长度：`medium` / `high` |
| `-d, --domain` | 限定域名 |
| `-i, --intent` | 启用意图识别 |
| `-j, --json` | JSON 输出 |
| `-k, --compact` | 紧凑输出 |
| `-h, --help` | 帮助 |

## 引擎选择

| 引擎 | 说明 |
|------|------|
| `search_std` | 智谱基础版，速度快 |
| `search_pro` | 智谱高阶版，质量最佳 |
| `search_pro_sogou` | 搜狗搜索 |
| `search_pro_quark` | 夸克搜索 |

## 价格查看

官方定价：[https://open.bigmodel.cn/pricing](https://open.bigmodel.cn/pricing)
