# WebSearch Search v2.0

_Agent 专用搜索工具 - 基于 SearchAPI_

## 功能

- **多种搜索类型**: 网页、新闻、视频、财经、地图、酒店、航班
- **自动重试**: 网络错误自动重试，提高稳定性
- **结构化返回**: Agent 直接可用的 JSON 格式
- **零外部依赖**: 纯 Node.js，无需安装额外包

## 搜索类型

| 类型 | 命令 | 说明 |
|------|------|------|
| 网页 | `web` 或默认 | 通用网页搜索 |
| 新闻 | `news` | 最新新闻 |
| 视频 | `video` | 视频搜索 |
| 财经 | `finance` | 股票/金融信息 |
| 地图 | `maps` | 地点/商户 |
| 酒店 | `hotels` | 酒店搜索 |
| 航班 | `flights` | 航班搜索 |

## 安装

```bash
cd /home/ubuntu/.openclaw/workspace/tools/websearch

# 配置 API Key (只需一次)
node websearch.js config set-key YOUR_API_KEY
```

## 使用方法

### 基本搜索

```bash
# 网页搜索 (默认)
node websearch.js search "关键词"
node websearch.js s "关键词"

# 指定搜索类型
node websearch.js news "AI 发展"
node websearch.js finance "AAPL"
node websearch.js video "Python 教程"
```

### 选项

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--num` | 结果数量 | 5 |
| `--lang` | 语言 | zh-CN |
| `--gl` | 地区 | cn |
| `--json` | JSON 输出 | 文本 |
| `--retry` | 最大重试次数 | 3 |

### 示例

```bash
# 新闻搜索
node websearch.js news "人工智能" --num=5

# 财经搜索 (用股票代码)
node websearch.js finance "AAPL"
node websearch.js finance "特斯拉"

# JSON 格式 (Agent 使用)
node websearch.js s "MCP" --json

# 调整结果数量
node websearch.js news "科技" --num=10
```

## 配置

```bash
# 查看配置
node websearch.js config

# 修改默认设置
node websearch.js config set-key YOUR_KEY
node websearch.js config set-num 10
node websearch.js config set-lang en
node websearch.js config set-gl us
node websearch.js config set-retry 5
```

## Agent 调用

```javascript
// 在 exec 中使用
exec('node /path/to/websearch.js s "关键词" --json', 
  (error, stdout, stderr) => {
    const result = JSON.parse(stdout);
    // result.results[0].title
    // result.results[0].snippet
    // result.results[0].link
  });
```

## 文件结构

```
websearch/
├── websearch.js    # 主程序
├── config.json         # 配置文件
├── install.sh          # 安装脚本
└── README.md           # 文档
```

## 迁移部署

```bash
# 1. 复制文件夹到新机器
scp -r ./websearch user@new-server:/path/to/tools/

# 2. 配置 API Key
cd /path/to/websearch
node websearch.js config set-key YOUR_API_KEY

# 3. 测试
node websearch.js test
```

## 故障排除

### 搜索失败
- 检查 API Key 是否正确
- 检查网络连接

### 财经搜索无结果
- 尝试用股票代码: `finance "AAPL"`
- 尝试英文: `finance "Tesla stock"`

### 视频搜索无结果
- 尝试用英文关键词

---

**提示**: API Key 可在 https://searchapi.io 免费注册获取
