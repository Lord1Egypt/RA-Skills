---
name: typecho-publisher
description: 通过 typecho-cli 直接管理 Typecho 博客文章 — 创建、查询、更新、删除、查询分类。当用户要求发布文章到博客、保存内容到 Typecho、查询或修改博客文章时触发此技能。涉及"发博客""归档""知识库""Typecho""我的博客"等关键词时均应使用。
version: 4.1.0
---

# Typecho Publisher

让 AI 通过 `typecho-cli` 命令行工具直接管理 Typecho 博客文章。

> **代码仓库**：https://github.com/CoolingRabbit/Typecho-Publisher （插件源码、安装说明、Release 下载均在此）

---

## 前置条件

- 用户已部署 Typecho 博客，并安装本插件 v4.1.0+（从代码仓库下载 `Plugin.php`、`Action.php`、`panel.php` 三个文件安装）
- 站长已在博客后台「管理 → AI Token」为本 Agent 对应的用户账户生成 Token

如果用户尚未提供 Token，提醒用户找站长生成。

## 配置

写入配置文件 `~/.config/typecho-cli/config.json`：

```json
{
  "domain": "https://www.example.com",
  "token": "your-token-here"
}
```

也可用环境变量 `TYPECHO_DOMAIN` / `TYPECHO_TOKEN`，或命令行参数 `--domain` / `--token` 覆盖。配置一次后无需重复询问。

## 行为边界

博客支持多个 AI Agent 同时接入，每个 Agent 持有独立 Token：

| 边界 | 规则 |
|------|------|
| **身份** | 一个 Token 绑定一个 Typecho 用户账户，文章归属于该账户 |
| **读** | 可查询博客中的**所有**文章（知识库检索需要） |
| **写** | 只能创建到本账户名下；只能更新、删除本账户名下的文章，操作他人文章返回 403 |
| **分类** | 只能从**现有分类**中选择，不能新建分类 |
| **Token** | 专属凭据，不要与其他 Agent 共享，不要写入文章正文 |

`list` 返回结果中的 `authorName` 标识文章归属账户，用于判断文章是否归本 Agent 管理。

## 命令

通过 `typecho-cli` 操作博客，**不要**直接拼凑 HTTP 请求。

```bash
# 查询文章列表
typecho-cli list [--page N] [--page-size N] [--status STATUS] [--category CATEGORY]

# 查询单篇文章
typecho-cli get --cid <文章ID>

# 查询现有分类列表
typecho-cli categories

# 创建文章
typecho-cli submit \
  --title "文章标题" \
  --text "Markdown 正文" \
  --category "分类名" \
  --tags "标签1,标签2,标签3" \
  --status publish

# 更新文章
typecho-cli update \
  --cid <文章ID> \
  --title "新标题" \
  --text "新正文（完整替换）" \
  --tags "新标签1,新标签2"

# 删除文章
typecho-cli delete --cid <文章ID>
```

**三个必须记住的要点：**

1. **发布前必须先执行 `typecho-cli categories`**，分类只能从返回结果中选择。如果所有现有分类都不合适，不要强行选择、不要编造分类名——与用户沟通，由用户在后台手动新建后再发布。
2. **`update` 的 `--text` 是整体替换**，不是增量追加。更新前必须先 `get` 获取完整原文，在完整原文基础上修改后传回。
3. **不传 `--status` 时 API 默认 `waiting`（待审核）**，需要直接发布必须显式传 `--status publish`。

## 操作流程

### 新建文章

1. 确认配置已就绪
2. `list` 检索已有文章，确认无同主题文章；有则转为更新流程
3. `categories` 查询现有分类并选择；都不合适则与用户沟通
4. `submit` 发布
5. 反馈结果：告知用户已发布，返回文章链接和 cid

### 更新文章

1. `list` 定位目标文章，通过 `authorName` 确认归本账户管理
2. `get` 获取完整原文
3. 在完整原文基础上修改
4. `update` 传回完整正文
5. 反馈结果

同主题的内容修改应更新已有文章，不要新建。同主题文章属于其他账户时不要直接更新，与用户沟通处理方式，不要尝试绕过 403。

### 删除文章

1. 通过 cid 定位文章，确认归本账户管理
2. 二次确认：提醒用户删除不可逆
3. `delete` 执行
4. 反馈结果

## 响应与错误

`typecho-cli` 统一返回 JSON：

```json
{"success": true, "action": "submit", "cid": 42, "message": "文章已创建", "status": "publish"}
```

```json
{"success": false, "message": "错误描述"}
```

| HTTP 状态码 | 错误信息 | 处理方式 |
|-------------|---------|---------|
| 401 | Token 缺失、无效或已吊销 | 检查配置；提醒用户到后台「管理 → AI Token」检查或重新生成 |
| 403 | 只能更新/删除本人账户名下的文章 | 不要重试，与用户沟通处理方式 |
| 400 | 标题/正文不能为空 | 补全字段 |
| 400 | 文章不存在：cid X 未找到 | 确认 cid 正确 |
| 400 | 分类不存在：xxx | 执行 `categories` 核对；都不合适则与用户沟通人工新建 |
| 400 | 内容疑似包含敏感信息 | 正文命中手机号/身份证/银行卡拦截规则，替换为占位符后重试 |
| 400 | 没有需要更新的字段 | update 至少传入一个修改字段 |

## 技术限制

- **正文长度**：不超过 50000 字符，超长应分多篇
- **图片**：不支持上传，使用外部图床 URL + Markdown 图片语法引用
- **Markdown**：插件自动添加 `<!--markdown-->` 前缀，只需提供标准 Markdown 正文
- **敏感信息**：插件自动拦截手机号、身份证号、银行卡号
- **删除不可逆**：永久删除文章及关联关系
