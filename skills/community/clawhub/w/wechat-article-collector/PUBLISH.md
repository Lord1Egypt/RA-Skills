# 微信公众号文章采集器

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

自动采集微信公众号文章到本地知识库，支持去重、全文下载、Markdown 存储。

## 特性

- ✅ 自动连接已登录的微信公众号后台
- ✅ 提取原创文章列表（标题、日期、链接）
- ✅ 智能去重（对比本地已收录文章）
- ✅ 批量下载文章全文
- ✅ 保存为 Markdown 格式
- ✅ 支持翻页获取所有文章

## 安装

### 前置条件

1. **Browser Harness**（浏览器自动化工具）

```bash
cd ~/.openclaw/workspace
git clone https://github.com/browser-use/browser-harness
cd browser-harness
uv tool install -e .
browser-harness --setup
```

2. **Chrome 浏览器**（已登录微信公众号后台）

### 安装 Skill

```bash
# 方式 1：通过 OpenClaw Skills 安装（推荐）
openclaw skills install wechat-article-collector

# 方式 2：手动克隆
cd ~/.openclaw/workspace/skills
git clone https://github.com/YOUR_USERNAME/wechat-article-collector
```

### 验证安装

```bash
cd ~/.openclaw/workspace/skills/wechat-article-collector
python3 scripts/test_install.py
```

## 使用

### 快速开始

```bash
# 1. 在 Chrome 中登录微信公众号后台
# 打开 https://mp.weixin.qq.com

# 2. 进入原创文章页面
# 点击"原创管理" → "原创声明"

# 3. 运行采集脚本
cd ~/.openclaw/workspace/skills/wechat-article-collector
python3 scripts/collect_articles.py
```

### 输出示例

```
=== 微信公众号文章采集器 ===

[1/5] 检查 Browser Harness...
✅ Browser Harness 就绪

[2/5] 连接微信公众号后台...
✅ 已连接公众号: gh_511119f160d8

[3/5] 提取文章列表...
✅ 提取到 10 篇文章

[4/5] 对比本地知识库去重...
✅ 需要下载 7 篇新文章

[5/5] 下载新文章全文...
[1/7] 给OpenClaw当爹日志0415之自动上下文管理
  ✅ 已保存

=== 完成 ===
成功下载: 7/7 篇
保存位置: ~/.openclaw/workspace/knowledge/wechat/gh_511119f160d8
```

## 配置

编辑 `config.json`：

```json
{
  "save_dir": "~/.openclaw/workspace/knowledge/wechat",
  "sleep_between_downloads": 1.5,
  "wait_after_page_load": 3,
  "max_pages": 50,
  "articles_per_page": 10
}
```

## 文件结构

```
wechat-article-collector/
├── SKILL.md                    # OpenClaw Skill 定义
├── README.md                   # 本文件
├── PUBLISH.md                  # 发布说明
├── config.json                 # 配置文件
└── scripts/
    ├── collect_articles.py    # 一键采集脚本
    ├── utils.py               # 工具函数
    └── test_install.py        # 安装测试
```

## 故障排查

详见 [README.md](README.md#故障排查)

## 扩展

### 定时采集

```bash
# 添加 cron 任务
0 2 * * * cd ~/.openclaw/workspace/skills/wechat-article-collector && python3 scripts/collect_articles.py
```

### 多公众号支持

修改 `utils.py` 中的 `get_account_id()` 函数。

## 许可

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

ZHAO - 2026-04-22

## 致谢

- [Browser Harness](https://github.com/browser-use/browser-harness)
- [OpenClaw](https://openclaw.ai)
