# Ingest（摄取）操作

> Karpathy 三大操作之首。完整覆盖"资料入库到 Wiki 演化"的全部过程。
> 核心理念：**一次 Ingest 可能级联更新多个导览（知识复利）**。

## 1. 子任务流水线

```
Collect（收集） → Check（检查） → Link（链接特性） → Compile（编译） → Write（写入） → Cascade（级联）
   ↓                ↓                ↓                ↓                ↓              ↓
 阶段 1.1          阶段 1.2          阶段 1.3          阶段 1.4          阶段 1.5       阶段 1.6
```

## 2. Collect（收集）

### 2.1 资料来源

- 用户上传的文件（PDF/DOCX/PPTX/XLSX 等）
- 已有 IMA 知识库的内容
- 联网搜索（用 `search(source="web")`）
- 网页链接（用 `import_urls`）

### 2.2 收集方式

| 来源 | API | 说明 |
|------|-----|------|
| 用户上传文件 | `upload_file` | 上传到指定知识库 |
| 导入网页 | `import_urls` | 批量导入 URL |
| 已有知识库 | `get_knowledge_list` | 逐级浏览 |
| 用户上传笔记 | `add_knowledge` | 关联到知识库 |
| 联网搜索 | `search(source="web")` | 补充资料 |

### 2.3 资料完整性原则

> "此阶段追求完整性，不追求结构" — 所有资料都是后续编译的"原材料"

详见 [link-handling.md](link-handling.md) 第 1 节和 [api-reference.md](api-reference.md) 第 5.1 节

## 3. Check（检查）

### 3.1 是否有旧导览？

```bash
# 在目标文件夹搜索标题包含"主题导览"的笔记
curl -s -X POST "https://ima.qq.com/openapi/note/v1/search_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"search_type": 0, "query_info": {"title": "主题导览"}, "start": 0, "end": 20}'
```

或者用标签筛选（推荐）：
```bash
# 列出所有带"状态:已编译"标签的导览
get_knowledge_list(kb_id=X, tags=["状态:已编译"])
```

### 3.2 判断

| 情况 | 处理方式 |
|------|---------|
| 有旧导览（目标主题） | **增量更新**：Compile 模式 2 |
| 有其他主题导览 | **新建**：Compile 模式 1 |
| 没有任何知识导览 | **新建**：Compile 模式 1 |

详见 [versioning.md](versioning.md) 第 4 节

## 4. Link（链接特性）

每个文件能否在导览中链接？这是 Karpathy **"可追溯到 raw"** 的核心要求。

### 4.1 media_type 速查表（IMA 完整版）

| 值 | 类型 | 链接策略 |
|----|------|---------|
| 1 | PDF 文件 | ⚠️ 标注"请在知识库查看" |
| 2 | 网页 | ✅ 获取真实 URL |
| 3 | Word 文件 | ⚠️ 标注"请在知识库查看" |
| 4 | PPT 文件 | ⚠️ 标注"请在知识库查看" |
| 5 | Excel 文件 | ⚠️ 标注"请在知识库查看" |
| 6 | 公众号文章 | ✅ 获取真实 URL |
| 7 | Markdown | ⚠️ 不内嵌链接，写为纯文本 |
| 9 | 图片 | ⚠️ 标注"请在知识库查看" |
| 11 | 笔记 | ⚠️ 不内嵌链接，写为纯文本 |
| 12 | QA 对话 | ⚠️ 标注"请在知识库查看" |
| 13 | TXT 文本 | ⚠️ 不内嵌链接，写为纯文本 |
| 14 | Xmind | ⚠️ 标注"请在知识库查看" |
| 15 | 录音 | ⚠️ 标注"请在知识库查看" |
| 16 | 网页视频 | ⚠️ 标注"请在知识库查看" |
| 17 | 对话 | ⚠️ 标注"请在知识库查看" |
| 18 | 视频 | ⚠️ 标注"请在知识库查看" |
| 19 | 播客 | ⚠️ 标注"请在知识库查看" |
| 20 | HTML | ⚠️ 标注"请在知识库查看" |
| 21 | EPUB 文件 | ⚠️ 标注"请在知识库查看" |
| 99 | 文件夹 | ❌ 不可链接 |

详见 [link-handling.md](link-handling.md) 第 2 节

### 4.2 链接特性表模板

```markdown
| media_id | title | media_type | 链接策略 | URL/备注 |
|---------|-------|-----------|---------|---------|
| xxx | 文章A | 2 | ✅ 可内嵌 | https://... |
| xxx | 文章B | 6 | ✅ 可内嵌 | https://... |
| xxx | 文章C | 7 | ⚠️ 不内嵌 | 请在知识库中查看 |
```

## 5. Compile（编译）

### 5.1 模式 1：新建（5 步法）

1. **明确主题** — 确定核心概念（主题定位、核心概念、边界范围）
2. **梳理关键词** — 提取关键要素（每概念 3-5 个子主题）
3. **发现关系** — 找出逻辑关联（层级、并列、因果、对立）
4. **呈现结构** — 可视化知识网络（表格 + 学习路径）
5. **美化优化** — 提升可读性（标题规范、排版、信息密度）

### 5.2 模式 2：增量更新（6 步法）

1. **读旧版** — `export_note` 获取旧版本内容
2. **提取版本信息** — 从 frontmatter 读取 version/changelog
3. **对比增量** — 比对文件夹中文件与导览 sources[]
4. **识别变化** — 新增/删除/概念变化
5. **更新导览** — `append_doc`（推荐）或 `update_note`（精细）
6. **更新版本号** — patch/minor/major

详见 [guide-template.md](guide-template.md) 和 [versioning.md](versioning.md)

## 6. Write（写入）

### 6.1 选项 A：新建笔记（最简单）

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/import_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content_format": 1,
    "content": "<完整 Markdown>",
    "title": "📖 主题导览：[主题名称]",
    "folder_id": "<目标笔记本 ID>"
  }'
# 返回: {"code": 0, "data": {"note_id": "xxx"}}
```

### 6.2 选项 B：追加内容（增量推荐）

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/append_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "note_id": "<已有导览 ID>",
    "content_format": 1,
    "content": "<追加内容>"
  }'
```

**优势**：不破坏原有结构，原子化操作。

### 6.3 选项 C：按 block 编辑（精细修改）

```bash
# 第一步：导出 block 结构
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note_blocks" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id": "<note_id>"}'

# 第二步：按 block_id 修改
curl -s -X POST "https://ima.qq.com/openapi/note/v1/update_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "note_id": "<note_id>",
    "block_id": "<block_id>",
    "content": "<新内容>"
  }'
```

详见 [write-and-verify.md](write-and-verify.md)

### 6.4 立即验证

> **重要**：笔记创建接口返回成功不代表内容完整，必须立即验证。

```bash
# 导出并比对
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id":"<note_id>","target_content_format":1}' | \
python3 -c "
import sys, json, urllib.request
d = json.load(sys.stdin)
if d['code'] == 0:
    url = d['data']['content_url']  # COS 链接，3 小时时效
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    print(resp.read().decode('utf-8'))
"
```

## 7. Cascade（级联）— **Karpathy 核心机制（IMA 实际可实现版）**

> 一次 Ingest 可能触动多个导览（不仅是新文件所在的那个）— 这是 wiki 知识复利的关键。

### 7.1 ⚠️ IMA 平台实际限制（2026-09）

> **v5.0.1 的 Cascade 算法与 IMA 平台实际能力有差距**。本节是修正版。

| 操作 | IMA 支持 | 说明 |
|------|---------|------|
| 修改导览 frontmatter（version / updated / changelog）| ❌ **不支持** | frontmatter 是"创建时设定"，不可后续修改 |
| `append_doc` 改 frontmatter | ❌ | 只能追加正文内容 |
| `update_note` 改 frontmatter | ❌ | 只能改 block，不改 frontmatter |
| `delete_note` 删除旧版本 | ❌ **不支持** | 只能客户端手动 |
| `import_doc` 创建新笔记 | ✅ | **唯一的版本演进方式** |
| `append_doc` 在旧笔记末尾追加标记 | ✅ | 用于"已被新版本替代"提示 |

**结论**：每次 Cascade 必须**创建新笔记**（不是修改旧笔记）。

### 7.2 Cascade 触发条件

- 新文件被 Ingest 后
- 自动计算它与所有现有导览的相关性
- 相关度 > 阈值 的导览加入"待更新列表"

### 7.3 Cascade 算法（纯 IMA API 可实现版）

```python
def cascade_update_imap(new_file, all_guides, kb_id):
    """Cascade 算法：纯 IMA API 实现"""
    affected = []

    # === 阶段 1：标签 Jaccard 粗筛（纯 API）===
    new_tags = set(new_file.get("tags", []))
    candidate_guides = []

    for guide in all_guides:
        guide_tags = set(guide.get("tags", []))
        if not (new_tags | guide_tags):
            continue
        # Jaccard 相似度
        jaccard = len(new_tags & guide_tags) / len(new_tags | guide_tags)

        # 文件夹归属加分（权重 0.3）
        folder_bonus = 0.3 if new_file.get("parent_folder_id") == guide.get("parent_folder_id") else 0

        # 标题关键词匹配加分（权重 0.3）
        keyword_bonus = 0.3 if any(
            kw in guide["title"] for kw in extract_keywords(new_file["title"])
        ) else 0

        total_score = jaccard + folder_bonus + keyword_bonus
        if total_score > 0.5:  # 阈值
            candidate_guides.append({
                "guide": guide,
                "score": total_score,
                "reason": "tag_overlap" if jaccard >= 0.4 else ("folder_match" if folder_bonus else "title_match")
            })

    # 排序 + 限制
    candidate_guides.sort(key=lambda x: -x["score"])
    candidate_guides = candidate_guides[:3]  # 最多 3 个导览

    # === 阶段 2：用户确认（必选）===
    print(f"📋 Cascade 候选导览：{len(candidate_guides)} 个")
    for c in candidate_guides:
        print(f"  - {c['guide']['title']} (相关度: {c['score']:.2f}, 原因: {c['reason']})")

    if not user_confirms():
        print("❌ 用户未确认，跳过 Cascade")
        return []

    # === 阶段 3：创建新版本导览（关键）===
    affected = []
    for candidate in candidate_guides:
        old_guide = candidate["guide"]
        new_guide = create_new_guide_version(old_guide, new_file)
        affected.append({
            "old_note_id": old_guide["note_id"],
            "new_note_id": new_guide["note_id"],
            "score": candidate["score"]
        })

    return affected


def create_new_guide_version(old_guide, new_file):
    """创建新版本导览（旧笔记保留作为历史）"""
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")

    # 1. 读旧导览（从 COS URL 下载）
    old_content = download_note(old_guide["note_id"])

    # 2. 提取旧 frontmatter
    old_fm = parse_frontmatter(old_content)
    old_version = old_fm.get("version", "1.0.0")
    old_changelog = old_fm.get("changelog", [])
    old_confidence = old_fm.get("confidence", "medium")
    old_created = old_fm.get("created", today)

    # 3. 计算新版本号（patch）
    new_version = bump_patch_version(old_version)  # v1.5 → v1.6

    # 4. LLM 生成新正文（增量更新 + 包含新文章引用）
    new_body = llm_generate_updated_body(old_content["body"], new_file)

    # 5. 构建新 frontmatter
    new_frontmatter = f"""---
title: {old_fm.get("title", "📖 主题导览")}
type: guide
confidence: {reassess_confidence(old_confidence, new_file)}
created: {old_created}
updated: {today}
version: {new_version}
changelog:
  - v{new_version}: [Ingest {today}] Cascade 级联更新，新增《{new_file["title"]}》
{chr(10).join(f"  - {entry}" for entry in old_changelog)}
sources:
  - 《{new_file["title"]}》{("(" + new_file.get("url", "") + ")") if new_file.get("url") else ""}
{chr(10).join(f"  - {s}" for s in old_fm.get("sources", []))}
---"""

    # 6. 创建新笔记（关键步骤）
    result = ima_api("openapi/note/v1/import_doc", {
        "content_format": 1,
        "content": new_frontmatter + "\n\n" + new_body,
        "folder_id": old_guide.get("folder_id", "")
    })
    new_note_id = result["data"]["note_id"]

    # 7. 在旧笔记末尾追加"已被替代"标记（可逆操作）
    ima_api("openapi/note/v1/append_doc", {
        "note_id": old_guide["note_id"],
        "content_format": 1,
        "content": f"""

---

> ⚠️ **本导览已被新版本替代**
> 新版本：note_id={new_note_id} (v{new_version}, {today})
> 旧版本保留作为历史记录。请在新版本基础上继续编辑。
"""
    })

    return {
        "note_id": new_note_id,
        "version": new_version,
        "old_note_id": old_guide["note_id"]
    }


def download_note(note_id):
    """从 COS URL 下载笔记内容"""
    result = ima_api("openapi/note/v1/export_note", {
        "note_id": note_id,
        "target_content_format": 1  # Markdown
    })
    if result["code"] != 0:
        raise Exception(f"export_note failed: {result}")
    content_url = result["data"]["content_url"]

    # 二次下载（3 小时时效）
    import urllib.request
    req = urllib.request.Request(content_url)
    with urllib.request.urlopen(req) as resp:
        markdown = resp.read().decode("utf-8")

    return parse_note(markdown)  # 解析 frontmatter + body


def bump_patch_version(version_str):
    """v1.5 → v1.6, v1.0.1 → v1.0.2"""
    parts = version_str.split(".")
    if len(parts) == 2:
        # v1.5 → v1.6
        return f"{parts[0]}.{int(parts[1]) + 1}"
    elif len(parts) == 3:
        # v1.5.0 → v1.5.1
        return f"{parts[0]}.{parts[1]}.{int(parts[2]) + 1}"
    else:
        return "1.0.1"
```

### 7.4 Cascade 完整示例

**场景**：用户上传"遗传算法在量化交易中的应用"到"AI 量化与深度学习"文件夹。

**已有导览清单**：
- 📖 主题导览：AI 量化与深度学习（v1.5, confidence: medium）
- 📖 主题导览：因子与资产定价（v2.3, confidence: high）
- 📖 主题导览：高频交易与微观结构（v3.0, confidence: high）

**Cascade 过程**：

| 导览 | 标签匹配 | Jaccard | 文件夹 | 总分 | 是否 Cascade |
|------|---------|---------|--------|------|-------------|
| AI 量化与深度学习 | ✅ `机器学习` `AI` | 0.7 | ✅ 同文件夹 | 1.3 | ✅ |
| 因子与资产定价 | ❌ 不匹配 | 0 | ❌ | 0 | ❌ |
| 高频交易 | ❌ 不匹配 | 0 | ❌ | 0 | ❌ |

**执行结果**：
- 创建新笔记 "📖 主题导览：AI 量化与深度学习"（v1.6）
  - 新 frontmatter（version 1.6, updated 2026-09-28, changelog 新增 v1.6 条目）
  - 新 body 包含"遗传算法在量化交易中的应用"文章引用
- 在旧笔记（v1.5）末尾追加"已被 v1.6 替代"标记
- **旧笔记保留**，作为历史版本

### 7.5 Cascade 的产物

**新笔记的 frontmatter**：
```yaml
---
title: 📖 主题导览：AI 量化与深度学习
type: guide
confidence: medium  # 可能因新文章加入而调整
created: 2026-05-13   # 保留原创建日期
updated: 2026-09-28   # 更新
version: 1.6          # patch
changelog:
  - v1.6: [Ingest 2026-09-28] Cascade 级联更新，新增《遗传算法在量化交易中的应用》
  - v1.5: 之前的更新...
sources:
  - 《遗传算法在量化交易中的应用》(URL)
  - [原有 sources...]
---
```

**旧笔记末尾追加**：
```markdown
---

> ⚠️ **本导览已被新版本替代**
> 新版本：note_id=xxx (v1.6, 2026-09-28)
> 旧版本保留作为历史记录。
```

### 7.6 Cascade 的成本控制

| 控制项 | 措施 |
|--------|------|
| 阈值 | Jaccard + 文件夹 + 标题匹配，阈值 0.5 |
| 范围 | 仅"有标签交集"的候选导览（避免遍历全部） |
| 数量限制 | 最多 3 个导览 |
| 用户确认 | 必选，不自动执行（避免误更新） |
| 可关闭 | 用户可设置 `cascade_enabled: false` 关闭 |

### 7.7 IMA 限制下的取舍

| 取舍 | 原因 |
|------|------|
| **每次 Cascade = 创建新笔记** | IMA 不允许修改 frontmatter，必须新建才能准确记录 version/changelog |
| **旧笔记保留不删除** | IMA 不支持删除 API（用户可在客户端手动清理） |
| **每次 Cascade 成本较高** | 创建笔记 + 在旧笔记追加标记 = 2 次 API 调用 |
| **可能产生"笔记碎片"** | 同一导览可能有多个历史版本（v1.4, v1.5, v1.6 都存在） |

**优势**：版本历史天然保留，符合 Karpathy "git 提交"哲学，且不影响 Lint 检查（看 updated 字段）。

### 7.8 为什么不修改旧笔记？

> 因为 IMA 平台 frontmatter 是"创建时设定"，**没有任何 API 可以修改它**。

这意味着：
- ❌ 不能更新旧笔记的 `version: 1.5` → `1.6`
- ❌ 不能在旧笔记的 `changelog:` 里追加新条目
- ❌ 不能修改旧笔记的 `updated:` 字段

只能：
- ✅ 在旧笔记**正文**末尾追加标记（`append_doc`）
- ✅ 创建新笔记（新 frontmatter 完全可控）

**这就是为什么 Cascade = 创建新笔记 + 旧笔记追加标记**。

## 8. 导览清单（Index）

> Karpathy 的 `index.md` 在 IMA 平台没有等价物，但我们用"主题导览清单"代替。

### 8.1 如何获取

```bash
# 方法 1：用标签筛选所有"已编译"导览
get_knowledge_list(kb_id=X, tags=["状态:已编译"])

# 方法 2：用 search_note 按标题定位
search_note(search_type=0, query_info={title: "主题导览"})
```

### 8.2 清单示例

| 主题导览 | 位置 | 版本 | 最后更新 | confidence |
|---------|------|:----:|:--------:|:----------:|
| 📖 主题导览：因子与资产定价 | 因子与资产定价/ | v2.3 | 2026-08-01 | high |
| 📖 主题导览：AI 量化与深度学习 | AI 量化与深度学习/ | v1.5 | 2026-07-15 | medium |
| 📖 主题导览：高频交易 | 高频交易与微观结构/ | v3.0 | 2026-06-20 | high |

### 8.3 清单的用途

- LLM 评估新文件该更新哪些导览（Cascade 算法输入）
- Lint 报告展示知识库全貌
- 用户了解"我有哪些导览"

## 9. 完整工作流示例

**场景**：用户在"AI 量化与深度学习"知识库上传一篇新文章"遗传算法在量化交易中的应用"。

```
[Ingest 触发]
   ↓
[Collect] upload_file 上传文件 → 等待完成
   ↓
[Check] 在该文件夹搜索"主题导览"：
  - 找到 "📖 主题导览：AI 量化与深度学习"（v1.5）
  - 找到 "📖 主题导览：高频交易"（v3.0）— 但不在该文件夹，跳过
   ↓
[Link] export_media_for_ima_sandbox 获取永久 URL（如适用）
   ↓
[Compile] 增量更新模式：
  - 读旧版 → 提取版本信息（v1.5）
  - 对比增量 → 1 篇新增
  - 在"机器学习理论方法"核心概念的关键要素中补充遗传算法文章
  - 评估 confidence：medium → medium（无变化）
   ↓
[Write] 用 append_doc 追加内容（不重建整个笔记）
  - note_id: xxx
  - content: <新的关键要素块>
   ↓
[Cascade] 检查其他导览：
  - "因子与资产定价" → 相关度 0.3，不更新
  - "高频交易" → 相关度 0.4，不更新
  - 没有其他受影响导览
   ↓
[报告] 告诉用户：
  - 主更新：1 个导览更新（v1.5 → v1.6）
  - 级联：0 个其他导览受影响
  - 下次建议：可考虑建"遗传算法"独立导览
```

## 10. 关键原则总结

1. **可追溯**：每个导览的 sources[] 必须能追到 raw 资料
2. **复利**：一次 Ingest 影响多个导览（不只一个）
3. **原子化**：用 append_doc 而非重建整个笔记
4. **schema 强制**：frontmatter 必填字段（confidence/sources/version）
5. **人类策展**：用户决定收录什么，LLM 维护导览
