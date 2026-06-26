# 外贸资讯聚合器（多源 RSS + 翻译 + 飞书推送）

**Version:** 2.3.3

## 简介
自动抓取外贸相关 RSS 源（支持自定义关键词），调用百度翻译 API 生成中文标题，生成 Markdown 报告并可选推送到飞书群。

## 功能
- 抓取多个 RSS 源（默认使用 Bing News 搜索外贸关键词）
- 自动翻译标题（英 → 中，支持自动检测源语言）
- 生成 Markdown 报告：`~/trade-news.md`
- 飞书机器人推送（可选）
- 自动分类新闻（帽子/面料/运费/关税/电商/运动服饰/汇率/国际关系/合规/行业动态）
- 生成近7天趋势周报（各类别新闻数量及占比）

## 依赖
- `curl`, `jq`, `md5sum`, `xmlstarlet`（必须安装）
- 百度翻译 API（免费，每月 100 万字符）
- 飞书自定义机器人（可选）

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `BAIDU_APPID` | ✅ | 百度翻译 App ID |
| `BAIDU_SECRET` | ✅ | 百度翻译密钥 |
| `FEISHU_WEBHOOK` | ❌ | 飞书机器人 Webhook |

## 安全说明
本 Skill 不会自动加载任何外部 `.env` 文件。请通过环境变量或直接在 crontab 中设置密钥。

## 网络要求
本 Skill 需要访问 Bing News 和百度翻译 API。如果您的运行环境无法直接访问外网，请配置代理（例如 `export http_proxy=http://your-proxy:port`）。

## 安装与配置

### 1. 获取百度翻译 API 密钥
- 访问 [百度翻译开放平台](https://fanyi-api.baidu.com/)
- 注册/登录，申请通用翻译 API（免费版）
- 记录 **App ID** 和 **密钥**

### 2. 创建飞书机器人（可选）
- 在飞书群中添加“自定义机器人”
- 复制 **Webhook URL**

### 3. 设置环境变量
将以下内容添加到 `~/.bashrc` 或执行脚本前 export：
```bash
export BAIDU_APPID="你的AppID"
export BAIDU_SECRET="你的密钥"
export FEISHU_WEBHOOK="你的飞书Webhook地址"
