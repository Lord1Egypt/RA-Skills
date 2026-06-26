# WeChat Article Analyzer

微信公众号文章深度分析工具。自动提取关键信息：时间线、关键人物、核心事实、主题分析。

## 功能

- 📖 **自动读取**微信公众号文章内容
- 📅 **提取时间线** - 识别关键事件和时间节点
- 👥 **识别关键人物** - 提取公司、组织、个人
- 📊 **提取核心事实** - 金额、百分比、漏洞编号等
- 🎯 **主题分析** - 识别文章核心议题
- 💬 **引语提取** - 收集重要引语

## 输出格式

- **Markdown** - 人类可读的报告
- **OpenCLI Adapter** - YAML 格式的 CLI 适配器
- **JSON** - 结构化数据，便于程序处理

## 安装

```bash
# 克隆仓库
git clone https://github.com/teenyboy/wechat-article-analyzer.git
cd wechat-article-analyzer

# 安装依赖
pip install requests pyyaml
```

## 使用方法

### 命令行

```bash
# 基本使用 - 输出到控制台
python3 scripts/analyze_wechat.py <微信公众号链接>

# 生成 Markdown 报告
python3 scripts/analyze_wechat.py <链接> --format markdown --output report.md

# 生成 OpenCLI 适配器
python3 scripts/analyze_wechat.py <链接> --format opencli --output adapter.yaml

# 生成 JSON 数据
python3 scripts/analyze_wechat.py <链接> --format json --output data.json

# 生成所有格式
python3 scripts/analyze_wechat.py <链接> --format all

# 显示详细过程
python3 scripts/analyze_wechat.py <链接> --verbose
```

### 示例

```bash
python3 scripts/analyze_wechat.py "https://mp.weixin.qq.com/s/pr6pCoRCFKeWDyr5xoBrjQ" --format markdown --output report.md --verbose
```

## 作为 OpenClaw Skill 使用

```python
from skills.wechat_article_analyzer import analyze_wechat

result = analyze_wechat.analyze_article("https://mp.weixin.qq.com/s/xxx")
print(result['timeline'])
print(result['stakeholders'])
```

## 分析维度

| 维度 | 说明 |
|------|------|
| **Timeline** | 事件时间线，关键节点 |
| **Stakeholders** | 关键人物、公司、角色 |
| **Facts** | 核心事实、数据、日期 |
| **Themes** | 主题分析、战略意义 |
| **Quotes** | 重要引语 |

## 技术方案

- **读取**: Python `requests` + Mac Chrome UA
- **解析**: 正则表达式提取结构化数据
- **输出**: Markdown / YAML / JSON

## 依赖

- Python 3.7+
- requests
- pyyaml

## 许可证

MIT

## 作者

Created by OpenClaw
