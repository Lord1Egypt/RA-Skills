# 标签体系（标签设计 + 应用 + 审查）

## 1. 设计原则

- 每篇文章 3-5 个关键词作为主题标签，不是固定词表
- 文章级标签反映内容的"涉及主题"，文件夹反映"归属主题"，二者互补
- 标签创建前不需要完整词表，可渐进添加

## 2. 标签分类

| 类型 | 用途 | 示例 |
|------|------|------|
| **主题标签** | 文章涉及的主题 | 风险因子 / 量化策略 / 机器学习 |
| **属性标签** | 文章固有属性 | 科普 / 进阶 / 待补充 / 已验证 |
| **状态标签** | 维护状态 | 已编译 / 待审核 / 草稿 |

## 3. 设计流程

1. **拉取文件清单**：`get_knowledge_list` 用 `limit=50` + cursor 分页
2. **LLM 提取关键词**：对每篇文章调用 LLM，提取 3-5 个主题关键词
3. **用户审核**：展示标签清单给用户，支持修改/删除/补充
4. **批量打标**：用 `tag_add` 给每个文件打标签
5. **验证**：`get_knowledge_list(tags=[...])` 验证筛选效果

## 4. LLM 提取关键词的 Prompt 模板

```text
你是一个知识管理专家。请阅读下面的文章，提取 3-5 个最能代表其内容主题的关键词。

要求：
1. 每个关键词 2-6 个中文字
2. 关键词应该是可复用的主题概念（不是专有名词）
3. 必要时可少于 3 个，但不要超过 5 个
4. 输出 JSON 数组

文章标题：<title>
（如有摘要：文章摘要：<summary>）

示例输入：标题="Fama-French 三因子模型详解"
示例输出：["多因子模型", "资产定价", "风险因子"]
```

## 5. 标签命名规范

✅ 推荐：
- `主题-XXX`：文章主题
- `属性-XXX`：文章属性
- `状态-XXX`：维护状态

❌ 避免：
- 过长（> 6 个汉字）
- 与文件夹名完全重复
- 一词多义（如"苹果"指水果还是公司）
- 临时标签不清理（如 `TODO`、`test`）

## 6. 应用标签

### ⚠️ 关键 API 规范

- `item_name` 必须严格匹配 `get_knowledge_list` 返回的**完整标题**（含扩展名和括号内容）
- `limit` 范围 `(0, 50]`，超出返回错误
- 调用前必须确认用户对该知识库有写权限（创建者/协作成员/管理员）

### 单文件打标

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_add" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "knowledge_base_id": "<kb_id>",
    "item_id": "<file_media_id>",
    "item_name": "<get_knowledge_list 返回的完整 title>",
    "tag_name": "<标签名>"
  }'
```

### 批量打标（推荐 Python）

```python
import urllib.request
import json

def api_call(path, data):
    url = f"https://ima.qq.com/{path}"
    headers = {
        "ima-openapi-clientid": "...",
        "ima-openapi-apikey": "...",
        "Content-Type": "application/json",
    }
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"),
        headers=headers, method="POST"
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def batch_tag_files(kb_id: str, file_tag_map: dict[str, list[tuple[str, str]]]):
    """批量打标。file_tag_map: {media_id: [(title, tag), ...]}"""
    for item_id, items in file_tag_map.items():
        for title, tag in items:
            api_call("openapi/wiki/v1/tag_add", {
                "knowledge_base_id": kb_id,
                "item_id": item_id,
                "item_name": title,  # ⚠️ 必须用完整标题
                "tag_name": tag,
            })
```

### 重要特性

- **重复操作不报错**：`tag_add` 重复打、`tag_remove` 移除不存在的，都直接返回成功
- **文件夹不支持打标签**（`media_type=99` 会被 API 拒绝）
- **幂等性**：适合断点续传，无需先查状态

## 7. 标签审查

当用户说"审查标签" / "整理标签"时执行。

### 7.1 列出所有标签

```bash
cursor = ""
while True:
    r = api_call("openapi/wiki/v1/tag_list", {
        "knowledge_base_id": "<kb_id>",
        "cursor": cursor,
        "limit": 100,
    })
    items.extend(r["data"]["items"])
    if r["data"]["is_end"]: break
    cursor = r["data"]["next_cursor"]
```

### 7.2 检查命名规范

识别近似标签（关键词重叠 > 60%）：
- "机器学习" vs "ML" vs "Machine Learning"
- "风险" vs "风险因子" vs "风险类"

### 7.3 识别孤儿标签

对每个标签，用 `get_knowledge_list(tags=[...])` 检查关联文件数：
- 0 个 → 孤儿标签，建议删除
- < 3 个 → 弱标签，考虑合并
- > 100 个 → 热门标签，考虑细分

### 7.4 标签健康指标

| 指标 | 健康值 | 异常处理 |
|------|:-----:|---------|
| 每个标签的关联文件数 | 5-50 | < 3 考虑删除；> 100 考虑细分 |
| 标签总数 | < 50 | > 100 提示用户清理 |
| 近似标签对数 | 0 | 建议合并 |

## 8. 破坏性操作保护

详见 [security.md](security.md)。`tag_delete` 和 `tag_rename` 是不可逆操作，必须先：
1. 列出受影响文件数
2. 用户显式确认
3. 操作日志记录
