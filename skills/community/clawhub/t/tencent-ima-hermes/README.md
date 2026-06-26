# 腾讯 IMA (Hermes Edition)

> 基于腾讯 IMA 官方 OpenAPI 技能 v1.1.7 改造的 **Hermes Agent** 适配版。
> 原版来源：https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip

## 什么是这个 Skill

让 Hermes Agent 能通过腾讯 IMA OpenAPI 管理你的：

- **笔记**：搜、列、读、新建、追加
- **知识库**：搜库、列库、浏览、搜内容、收网页 / 微信文章到库、上传文件
- **凭证安全**：ClientID / API Key 只发往 `ima.qq.com`；COS 上传走临时凭证，不外泄主凭证

## 跟原版 / 商店其他版本的区别

| 维度 | 本版（Hermes） | clawhub `tencent-ima-skill` v1.0.1 | GitHub `tencent-ima-copilot-mcp` |
| --- | --- | --- | --- |
| 源 | 腾讯官方 v1.1.7 zip + 我们探针发现的 5 个端点 | 社区 hyddd | 社区 highkay (85⭐) |
| 凭证 | OpenAPI clientId + apiKey（**官方**） | 未公开 | cookie + bkn（**非官方**，有封号风险） |
| 实现路线 | **OpenAPI** 官方接口 | 桌面 UI 自动化 | 桌面 UI 自动化 |
| API 端点覆盖 | **22**（16 文档化 + 5 探针发现 + 1 便利封装） | 未公开 | 未公开 |
| CLI 桥接 | `bin/ima.sh` 18 个子命令 | 未知 | MCP server（不是 CLI） |
| COS 上传 | ✅ 走 COS 临时凭证 | 未知 | ✅ |
| 本地真验证 | ✅ 22 端点全跑通 | 未公开 | ✅（作者自验） |

## 安装

```bash
# 1) 下载官方 OpenAPI 包
curl -sS -o /tmp/ima.zip https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip

# 2) 解压到 hermes skills 目录
mkdir -p ~/.hermes/skills/ima
unzip -q /tmp/ima.zip -d /tmp/ima-extract
cp -r /tmp/ima-extract/ima-skill/* ~/.hermes/skills/ima/

# 3) 应用 hermes 适配（拿本仓的 SKILL.md / bin/ima.sh / _meta.json / skill-card.md 覆盖）
# 详见下方「Hermes 适配说明」

# 4) 配凭证
echo 'IMA_OPENAPI_CLIENTID=your-client-id' >> ~/.hermes/.env
echo 'IMA_OPENAPI_APIKEY=your-api-key' >> ~/.hermes/.env
chmod 600 ~/.hermes/.env

# 5) 验证
~/.hermes/skills/ima/bin/ima.sh list-kb
```

## Hermes 适配说明

我们做了 4 项改造（**不**修改原版任何 API 端点；**不**删改原版字段名）：

1. **OpenClaw 风格 frontmatter → Hermes 风格 frontmatter**
2. **增加 `bin/ima.sh` POSIX 桥接**（18 个子命令 + 1 个便利封装）
3. **探针发现并补充 5 个未文档化但真实存在的端点**（create_folder / create_knowledge_base / move_knowledge / add_notebook / rename_notebook）
4. **凭证路径对齐 Hermes `.env` 约定**（`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`）

原版约束（写入类工作流 MANDATORY RULES、UTF-8 强制、media_type 拒绝规则）**完全保留**。

## Roadmap

- 🟡 **删除 / 移动 / 重命名相关指令正在开发中**
  腾讯 OpenAPI 路由层经主动探针确认未暴露 delete 端点，需在桌面/移动端手工操作或通过 cookie 自动化曲线实现。
- ⚪ 标签管理、知识库分享/成员管理正在评估
- ⚪ 与腾讯桌面端/移动端的 UI 自动化集成（待评估）

## 凭证获取

- API Key 获取页：https://ima.qq.com/agent-interface
- 凭证作用域：`ima.qq.com` + `*.myqcloud.com`（COS 上传临时凭证域）

## 完整 API 覆盖

### 笔记（openapi/note/v1/*，8 个端点）

详见 `notes/GUIDE.md` 和 `notes/references/api.md`。

### 知识库（openapi/wiki/v1/*，14 个端点）

详见 `knowledge-base/GUIDE.md` 和 `knowledge-base/references/api.md`。

### 显式不支持（腾讯 OpenAPI 不暴露）

- 删除笔记 / 删除文档 / 删除 KB 内条目 / 删除文件夹
- 重命名 / 移动文件夹
- 标签管理（add/remove/list tags）
- 知识库分享 / 成员管理 / 权限管理

→ 这些操作需要在 ima 客户端手工完成。

## License

本仓基于 **MIT No Attribution (MIT-0)** 许可证发布。

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

**注意**：本仓库是基于腾讯 IMA 官方 OpenAPI 技能 v1.1.7 改造的适配版。
原版 zip（https://app-dl.ima.qq.com/skills/ima-skills-1.1.7.zip）的内容
沿用腾讯 IMA OpenAPI 使用条款。本 MIT-0 授权仅适用于本仓库新增的
改造代码（hermes frontmatter、bin/ima.sh CLI 桥接、_meta.json、skill-card.md、
探针发现说明等）。
