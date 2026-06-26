# 新媒体内容创作专家 - 安装指南

## 简介

这是一个具备热点追踪、写作创作、发布一体化能力的自媒体内容创作助手。

## 功能特点

- 热点追踪：自动搜索热门话题
- 文风学习：支持自定义写作画像
- 内容撰写：按画像风格生成文章
- 质量检查：AI味去除、口语化优化
- 多角色评审：AI审计员、高级读者、模拟读者
- 事实核查：核实关键数据
- 发布同步：腾讯文档备份 + 公众号草稿

## 文件结构

```
新媒体内容创作专家/
├── 新媒体内容创作专家.md    # 技能文档
├── 文风参考库/
│   └── 写作画像库/
│       ├── Norrona-小红书大字报-20260310.json
│       └── 技能介绍-公众号-20260310.json
└── README.md              # 本文件
```

## 安装步骤

### 1. 复制技能文件

将 `新媒体内容创作专家.md` 复制到你的 OpenClaw 技能目录：

```bash
# 方式一：复制到全局技能目录
cp 新媒体内容创作专家.md ~/.openclaw/skills/

# 方式二：复制到工作空间
cp 新媒体内容创作专家.md ~/.openclaw/workspace/expert-skills/
```

### 2. 复制写作画像库（可选）

```bash
mkdir -p ~/.openclaw/workspace/文风参考库/写作画像库
cp -r 文风参考库/* ~/.openclaw/workspace/文风参考库/
```

### 3. 配置公众号 API（可选）

如需发布到公众号，需要配置：

在公众号后台获取：
- AppID
- AppSecret
- 添加 IP 白名单：`你的服务器IP`

### 4. 配置腾讯文档 MCP（可选）

在 `~/.openclaw/workspace/config/mcporter.json` 中添加：

```json
{
  "mcpServers": {
    "tencent-docs": {
      "enabled": true,
      "url": "https://docs.qq.com/openapi/mcp",
      "headers": {
        "Authorization": "Bearer 你的MCP_TOKEN"
      }
    }
  }
}
```

获取 MCP Token：https://docs.qq.com/desktop/wikispace?tab=1 → 「≡」→ 「使用MCP」

## 使用方法

在 OpenClaw 中调用：

```
写一篇关于xxx的公众号文章
帮我追踪xxx热点
```

## 写作画像

可在 `文风参考库/写作画像库/` 中添加自定义画像，格式：

```json
{
  "name": "画像名称-平台-日期",
  "platform": "公众号/小红书/知乎",
  "target_audience": "目标受众描述",
  "language_style": "语言风格",
  "title_style": {
    "features": ["特点1", "特点2"]
  }
}
```

## 更新日志

### 2026-03-10
- 初始版本
- 8步工作流程
- 多角色评审
- 公众号+腾讯文档发布
