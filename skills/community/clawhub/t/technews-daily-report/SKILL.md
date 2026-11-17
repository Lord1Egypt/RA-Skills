---
name: tech-news-daily
version: 0.4.0
description: "每日AI/科技热榜日报。从AIHOT单站读取近3天热榜，生成报告并同步飞书文档，只发链接不发全文。"
---

# 科技新闻日报 | Tech News Daily

> **版本：** 0.4.0（数据源切换为 AIHOT 单站，彻底解决 AI overload 问题；时效从一周缩短为近3天；cron 从每2天改为每天；飞书文档存入「科技新闻日报」知识库目录，node: `Iv9UwDW5viSJDWk12j7cBazYn8b`）

**v0.4.0 更新说明：**
- 数据源从 Tavily 全网搜索切换为 AIHOT（aihot.virxact.com）单站聚合
- 彻底移除 Tavily 搜索，大幅降低 token 消耗，避免 AI overload
- AIHOT 内容已经过质量筛选，直接整理使用

## 概述

每日从 AIHOT（aihot.virxact.com）读取已聚合整理的 AI/科技热榜，整理生成报告，同步到本地文件和飞书文档。

## 数据源

**AIHOT（aihot.virxact.com）** — AI 行业动态聚合站，每日提供精选热榜和日报。

**为什么用 AIHOT：**
- 单站聚合多源内容，无需全网搜索
- 内容已经过质量筛选（推荐度已标注）
- 彻底避免 Tavily 全网搜索带来的高 token 消耗和 AI overload 问题

---

## 工作流程

### 第一步：读取 AIHOT 近3天日报

使用 `tavily_extract` 读取 AIHOT `/daily` 页面，抓取近3天所有新闻：

```
URL: https://aihot.virxact.com/daily
query: "AI 科技 新闻 热榜 近3天"
extract_depth: "advanced"
chunks_per_source: 5
```

**时效范围：过去3天**（当日 + 前2天），确保内容充实。

### 第二步：整理与分类

AIHOT 已有分类（模型发布/更新、产品发布/更新、行业动态、论文研究、技巧与观点），直接采用其分类，并根据内容补充来源和标签。

整理后的文件按以下分类组织：
- 模型发布/更新
- 产品发布/更新
- 行业动态
- 论文研究
- 技巧与观点

### 第三步：写入本地文件

保存路径：`memory/YYYY-MM-DD-tech-news.md`

**文件格式要求：**
- 文件头包含整理时间、来源（AIHOT）和今日日期
- 保留 AIHOT 原有分类
- 每条新闻包含：标题、推荐度（如有）、摘要、来源、链接
- 底部包含数据总览表格
- 末尾同步记录（本地文件 ✅、飞书文档链接）

### 第四步：同步飞书文档

**必须用两步法：先创建 wiki 节点，再写入内容。不要用 `docs +create --wiki-node`（该方式创建的文档编码有问题且位置可能不对）。**

**正确流程：**

```bash
# 步骤 1：用 wiki +node-create 在「科技新闻日报」节点下创建 wiki 节点（返回 node_token 和 obj_token）
lark-cli wiki +node-create \
  --space-id "7621391289904516315" \
  --parent-node-token "Iv9UwDW5viSJDWk12j7cBazYn8b" \
  --title "科技新闻日报 | YYYY年MM月DD日"

# 返回示例：
# {"ok":true,"data":{"node_token":"OnBrwGTJciHcOjk90w7c1cMhn9c","obj_token":"JUqNdp3uSodBX1xF66fcNhcHnFh",...}}
# → 从返回中提取 obj_token（即 doc_token）

# 步骤 2：将本地 markdown 文件转成 XML 后，用 docs +update 写入文档
# 重要：内容必须用 XML 格式（--doc-format xml），禁止用 --doc-format markdown（会导致中文乱码）
# ⚠️ 重要：XML 内容必须以 <title>标题</title> 开头，否则文档标题默认为「Untitled」
# 格式：<title>科技新闻日报 | YYYY年MM月DD日</title><h1>科技新闻日报 | YYYY年MM月DD日</h1>...
# markdown 中的换行用 <br/>，< 用 &lt;，> 用 &gt;，& 用 &amp;
lark-cli docs +update \
  --api-version v2 \
  --doc "<obj_token>" \
  --command overwrite \
  --doc-format xml \
  --content @memory/YYYY-MM-DD-tech-news.xml

# 步骤 3：授予张公子 full_access 权限（用 Open API 直接调，绕过 lark-cli 交互限制）
ACCESS_TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id": "cli_a94b4a1e43781cc7", "app_secret": "NALleHubGWREfZJkXpYizwszPIBFIBq7"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))")

curl -s -X POST 'https://open.feishu.cn/open-apis/drive/v1/permissions' \
  -H 'Authorization: Bearer '$ACCESS_TOKEN \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "docx",
    "token": "<obj_token>",
    "member_id": "ou_d8ace8a146610ca26bc07d8e68a5620f",
    "member_type": "openid",
    "perm": "full_access"
  }'
```

**内容转 XML 注意事项：**
- **第一行必须是 `<title>标题</title>` 元素**，飞书会将其设为文档标题；否则默认为「Untitled」
- 标题后接 `<h1>正文一级标题</h1>` 作为正文开篇
- markdown 内容中的中文必须正确转义（`<` → `&lt;`，`>` → `&gt;`，`&` → `&amp;`，换行 → `<br/>`）
- 推荐用 Python 做 markdown → Feishu XML 的批量转义，避免手动转义出错
- 文件路径必须用相对路径（如 `@memory/2026-05-15-tech-news.xml`），不能是绝对路径
- **禁止**用 `--doc-format markdown` 写入（会导致中文乱码）

**飞书知识库存档目标（v0.4.0）：**
- space_id：`7621391289904516315`
- parent_node_token：`Iv9UwDW5viSJDWk12j7cBazYn8b`（科技新闻日报目录）
- 节点 token：从 `wiki +node-create` 返回的 `node_token`
- doc token：从 `wiki +node-create` 返回的 `obj_token`

**Fallback（当 lark-cli 不可用时）：**

如果 `wiki +node-create` 调用失败，自动切换到 Feishu Open API 直接调用：
```bash
# 1. 获取 tenant_access_token
ACCESS_TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id": "cli_a94b4a1e43781cc7", "app_secret": "<FEISHU_APP_SECRET>"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))")

# 2. 在知识库「科技新闻日报」节点下创建 wiki 节点
curl -s -X POST 'https://open.feishu.cn/open-apis/wiki/v2/spaces/7621391289904516315/nodes' \
  -H 'Authorization: Bearer '$ACCESS_TOKEN \
  -H 'Content-Type: application/json' \
  -d '{"parent_node_token": "Iv9UwDW5viSJDWk12j7cBazYn8b", "node_type": "origin", "obj_type": "docx", "title": "科技新闻日报 | YYYY年MM月DD日"}'
# → 获得 obj_token

# 3. 写入文档内容（batch create blocks，XML 格式）
curl -s -X POST 'https://open.feishu.cn/open-apis/docx/v1/documents/<obj_token>/blocks/<root_block_id>/children' \
  -H 'Authorization: Bearer '$ACCESS_TOKEN \
  -H 'Content-Type: application/json' \
  -d '{"children": [...]}'
```

> ⚠️ Fallback 需要 `app_secret`，优先确保 lark-cli 可用——只有当 lark-cli 不可用时才走 fallback。

### 第五步：发送飞书文档链接

**只发链接，不发完整报告内容。**

发送格式：
```
📰 科技新闻日报 | YYYY年MM月DD日
🔗 飞书文档：https://feishu.cn/docx/xxxxx
💾 本地文件：memory/YYYY-MM-DD-tech-news.md
```

使用 `message(action="send", channel="feishu", target="chat:oc_d591432cedf9a00c01878c24754cb050", message="...")`

### 第六步：更新本地文件同步记录

在本地文件末尾添加：
```
## 📋 同步记录
- ✅ 本地文件：`memory/YYYY-MM-DD-tech-news.md`
- ✅ 飞书文档：`科技新闻日报 | YYYY年MM月DD日`
  - 文档链接：https://feishu.cn/docx/xxxxx
  - 知识库：个人知识库
```

---

## 输出模板

```
# 科技新闻日报 | YYYY年MM月DD日

> 整理时间：YYYY-MM-DD HH:MM GMT+8
> 来源：AIHOT（aihot.virxact.com）

---

## 模型发布/更新

### [新闻标题]
- 摘要：[1-2句话描述]
- 来源：[媒体名称]
- 链接：[URL]

[...]

## 产品发布/更新

[...]

## 行业动态

[...]

## 论文研究

[...]

## 技巧与观点

[...]

---

## 📊 数据总览

- 模型发布/更新：X 条
- 产品发布/更新：X 条
- 行业动态：X 条
- 论文研究：X 条
- 技巧与观点：X 条
- 合计：XX 条

---

## 🔗 关键来源

- AIHOT：https://aihot.virxact.com
[...]

---

整理：牛管家 | 数据来源：AIHOT

## 📋 同步记录

- ✅ 本地文件：`memory/YYYY-MM-DD-tech-news.md`
- ✅ 飞书文档：`科技新闻日报 | YYYY年MM月DD日`
  - 文档链接：https://feishu.cn/docx/xxxxx
  - 知识库：个人知识库
```

---

## 参考资源

- **AIHOT：** https://aihot.virxact.com
- **飞书文档操作：** 见 `references/feishu-doc.md`

---

## 注意事项

1. **数据源优先**：直接从 AIHOT 读取，不主动进行全网搜索
2. **时效过滤**：只收录当日新闻，老旧新闻不再收录
3. **链接有效性**：优先使用原始来源链接，避免短链接
4. **飞书权限**：创建文档时必须传入 `owner_open_id` 确保用户有编辑权限
5. **文件命名**：使用 `YYYY-MM-DD-tech-news.md` 格式，便于排序检索

---

## 执行建议（重要）

**由于 token 消耗大幅降低（不再做全网搜索），v0.4.0 不再需要子会话拆分，整个流程在主会话完成即可。**

```markdown
1. 使用 tavily_extract 读取 AIHOT /daily 页面
2. 整理分类，写入本地文件 memory/YYYY-MM-DD-tech-news.md
3. 创建飞书 wiki 节点 + 写入文档内容
4. 发送飞书文档链接到群
5. 更新本地文件同步记录，标记完成
```

**进度 Checkpoint：每步必须写 checkpoint**

在每个关键步骤完成后，立即将进度写入 checkpoint 文件 `memory/YYYY-MM-DD-tech-news-checkpoint.json`：

```json
{
  "step": 4,
  "stepName": "飞书文档创建完成",
  "feishuDocUrl": "https://feishu.cn/docx/xxx",
  "localFile": "memory/2026-07-10-tech-news.md",
  "timestamp": 1752124800000,
  "pendingAction": "发送飞书链接"
}
```

**步骤说明：**
- step 1: AIHOT 读取完成 → 写入 checkpoint
- step 2: 本地文件写入完成 → 写入 checkpoint
- step 3: 飞书文档创建完成 → 写入 checkpoint
- step 4: **只发飞书文档链接到群** → 最后一步，**必须成功**，完成后写入 step: done

**⚠️ Fallback 触发条件：**
当 `feishu_wiki` 或 `feishu_doc` 工具调用失败（返回 ToolNotFoundError 或类似错误），自动切换到 direct Feishu Open API 调用（见第四步 fallback 说明）。

**⚠️ 关键规则（v0.4.0）：**
- 步骤4（发送飞书链接）是整个流程中**最后一步**，只发文档链接，不发完整报告内容
- 飞书群组 ID（目标）：`oc_d591432cedf9a00c01878c24754cb050`
- 消息格式：`📰 科技新闻日报 | YYYY年MM月DD日\n🔗 飞书文档：https://feishu.cn/docx/xxxxx\n💾 本地文件：memory/YYYY-MM-DD-tech-news.md`
- 必须使用 `message(action="send", channel="feishu", target="chat:oc_d591432cedf9a00c01878c24754cb050", message="...")`
- **禁止**在发送飞书消息之前结束会话——即使所有文件/文档操作都完成了，也要留足时间发送消息
- 飞书消息发送成功后，才更新 checkpoint 为 `step: done`
