# SpecQ v2.0 OpenCode Prompt

> 基准代码：https://github.com/daizehua-wq/Specq-mcp (v1.0, commit a4d968e)
> 设计文档：本地 `SpecQ_v2.0_设计规格.md` + 飞书 https://www.feishu.cn/docx/Us68dycZJosRIQxMQ5ccI3eInZb
> 目标：产出可本地部署验证的 v2.0 全套代码

---

## 一、任务总览

在 SpecQ MCP Server v1.0（4 个 tool）基础上，新增 2 个 Tool + 修改 4 个 Tool + 新增 4 个模块文件，使 Agent 具备记忆、搜索、多模态、多输出能力。

### Tool 变更清单

| Tool | 动作 | 关键变更 |
|---|---|---|
| `specq_memory` | 🆕 新增 | 三层记忆：recall / save / get_plan / set_plan |
| `specq_search` | 🆕 新增 | 联网搜索：web / news / scholar |
| `specq_generate_intel` | ✏️ 修改 | 增加 output_format / context_block / anonymize / 搜索注入 / 脱敏 |
| `specq_log_visit` | ✏️ 修改 | 增加 image_paths / audio_path / video_path 多模态 |
| `specq_extract_insights` | ✏️ 修改 | 增加 db_path + db_query / api_url + api_params |
| `specq_feedback` | ✏️ 修改 | 增加 uid + 自动写入 memory |

---

## 二、新增模块文件（4 个）

先创建模块文件，再修改主文件 `mcp_server.py`。

### 2.1 memory.py — 记忆模块

**职责**：ChromaDB 连接管理 + embedding + 工作记忆读写

**函数清单**：

```python
# 配置读取
get_memory_dir() -> str        # SPECQ_DATA_DIR 或 ~/.specq_data
get_chroma_dir() -> str        # {memory_dir}/chromadb
get_embedding_key() -> str     # ZHIPU_API_KEY

# ChromaDB 懒加载
get_chroma_collection() -> Collection
  # Path: {chroma_dir}
  # Collection: specq_memory
  # Settings: anonymized_telemetry=False
  # 不存在则自动创建
  # 缓存为模块级变量，避免重复初始化

# Embedding
embed_text(text: str) -> list[float]
  # API: https://open.bigmodel.cn/api/paas/v4/embeddings
  # Model: embedding-2, 1024维
  # Auth: Authorization: Bearer {ZHIPU_API_KEY}
  # Timeout: 10s
  # 错误抛出 RuntimeError
  # 同步函数（内部用 requests 非 httpx）

# 工作记忆
load_working_memory(uid: str) -> dict
  # Path: {memory_dir}/specq_working_memory_{uid}.json
  # 不存在返回: {"goal": None, "plan": [], "current_step": 0, "results": {}}
  # 目录自动创建

save_working_memory(uid: str, data: dict)
  # ensure_ascii=False, indent=2
  # 目录自动创建
```

**依赖**：`chromadb`, `requests`

### 2.2 search.py — 联网搜索模块

**职责**：调用搜索引擎 API，返回结构化结果

**函数**：

```python
async def web_search(query: str, limit: int = 5, source: str = "web") -> dict:
    """
    source: "web" | "news" | "scholar"
    
    使用 Brave Search API:
      https://api.search.brave.com/res/v1/web/search?q={query}&count={limit}
      Header: Accept: application/json, X-Subscription-Token: {SEARCH_API_KEY}
    
    如果 SEARCH_API_KEY 未配置，使用 requests + BeautifulSoup 做基础 Google 抓取作为 fallback
    
    返回格式:
    {
      "results": [
        {"title": "...", "url": "...", "snippet": "...", "published": "..."}
      ],
      "total": N,
      "source": "web"
    }
    
    超时: 10s
    错误不抛，返回 {"results": [], "total": 0, "source": source, "error": "..."}
    """
```

**环境变量**：`SEARCH_API_KEY`（Brave API Key）

### 2.3 multimodal.py — 多模态输入模块

**职责**：图片 OCR、语音转录、视频关键帧提取

**函数**：

```python
async def process_image(image_path: str) -> str:
    """OCR 提取图片文字，返回文本"""

async def process_audio(audio_path: str) -> str:
    """语音转文字，返回文本"""

async def process_video(video_path: str) -> str:
    """提取视频关键帧 + 语音转录，返回文本摘要"""
```

**实现参考**：
- OCR: pytesseract 或 opencv + easyocr
- 音频: openai whisper API 或 faster-whisper 本地模型
- 视频: opencv 提取关键帧（每 30 秒一帧）+ 音频轨 → process_audio

### 2.4 output.py — 多格式输出模块

**职责**：Markdown → Word/PPT/邮件/聊天 格式转换

**函数**：

```python
def format_output(markdown_text: str, output_format: str, metadata: dict = None) -> str:
    """
    output_format:
      "markdown" → 原样返回
      "docx"     → 通知（"Word 文档模板已就绪，请用 python-docx 生成"）
      "ppt"      → 通知（"PPT 大纲已就绪，格式说明如下"）
      "email"    → 生成邮件格式（Subject + Body）
      "chat"     → 裁剪为 300 字精简版
    
    返回: 格式化后的文本字符串
    """
```

**依赖**：`python-docx`（用于 docx），`python-pptx`（用于 ppt）

---

## 三、mcp_server.py 修改详解

### 3.0 文件头修改

版本号 `v1.0` → `v2.0`，tool 数量 `4` → `6`，依赖说明增加 `chromadb requests python-docx`

新增 import：

```python
import uuid
from dotenv import load_dotenv
load_dotenv()

import memory as mem
import search as sch
import multimodal as mm
import output as out
```

### 3.1 新增 Tool：specq_memory

```python
@mcp.tool()
async def specq_memory(
    action: str,
    query: str | None = None,
    limit: int = 5,
    content: str | None = None,
    category: str | None = None,
    metadata: dict | None = None,
    goal: str | None = None,
    plan: list[str] | None = None,
    current_step: int = 0,
    uid: str = "default",
) -> str:
    """
    三层记忆操作接口。
    
    4 个 action：
    - recall: 语义搜索召回，需 query
    - save: 写入记忆，需 content + category + uid
    - get_plan: 读工作记忆，需 uid
    - set_plan: 设工作记忆，需 goal + plan + uid
    """
    if action == "recall":
        if not query:
            return json.dumps({"error": "recall 需要 query 参数"}, ensure_ascii=False)
        try:
            vec = mem.embed_text(query)
            collection = mem.get_chroma_collection()
            kwargs = {"query_embeddings": [vec], "n_results": limit}
            if uid != "default":
                kwargs["where"] = {"user_id": uid}
            results = collection.query(**kwargs)
            memories = []
            if results and results["ids"] and results["ids"][0]:
                for i, mid in enumerate(results["ids"][0]):
                    mmeta = results["metadatas"][0][i] if results["metadatas"] else {}
                    memories.append({
                        "memory_id": mid,
                        "content": results["documents"][0][i] if results["documents"] else "",
                        "category": mmeta.get("category", ""),
                        "metadata": {k: v for k, v in mmeta.items() if k not in ("category", "user_id")},
                        "score": round(results["distances"][0][i], 4) if results["distances"] else 0,
                    })
            return json.dumps({"memories": memories}, ensure_ascii=False, indent=2)
        except Exception as e:
            return json.dumps({"error": f"recall 失败: {e}"}, ensure_ascii=False)

    elif action == "save":
        if not content or not category:
            return json.dumps({"error": "save 需要 content + category"}, ensure_ascii=False)
        try:
            vec = mem.embed_text(content)
            collection = mem.get_chroma_collection()
            mid = f"mem_{uuid.uuid4().hex[:12]}"
            mmeta = {"category": category, "user_id": uid, "timestamp": str(date.today())}
            if metadata:
                mmeta.update({k: v for k, v in metadata.items() if v is not None})
            collection.add(ids=[mid], embeddings=[vec], documents=[content], metadatas=[mmeta])
            return json.dumps({"memory_id": mid, "status": "saved"}, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": f"save 失败: {e}"}, ensure_ascii=False)

    elif action == "get_plan":
        wm = mem.load_working_memory(uid)
        return json.dumps(wm, ensure_ascii=False, indent=2)

    elif action == "set_plan":
        if not goal:
            return json.dumps({"error": "set_plan 需要 goal"}, ensure_ascii=False)
        wm = mem.load_working_memory(uid)
        wm["goal"] = goal
        wm["plan"] = plan or []
        wm["current_step"] = current_step
        mem.save_working_memory(uid, wm)
        return json.dumps({"status": "saved", "goal": goal, "total_steps": len(plan or [])}, ensure_ascii=False)

    else:
        return json.dumps({"error": f"未知 action: {action}，支持 recall/save/get_plan/set_plan"}, ensure_ascii=False)
```

### 3.2 新增 Tool：specq_search

```python
@mcp.tool()
async def specq_search(
    query: str,
    limit: int = 5,
    source: str = "web",
) -> str:
    """
    联网搜索，补充公开数据。
    
    Args:
        query: 搜索关键词
        limit: 结果数上限（默认5）
        source: 搜索源 — web / news / scholar
    
    Returns:
        结构化搜索结果 JSON
    """
    try:
        result = await sch.web_search(query, limit, source)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"results": [], "total": 0, "source": source, "error": str(e)}, ensure_ascii=False)
```

### 3.3 修改 Tool：specq_generate_intel

**在原有参数基础上新增**：

```python
async def specq_generate_intel(
    product: str,
    application: str,
    scenario: str,
    output_format: str = "markdown",       # 🆕
    context_block: str | None = None,       # 🆕
    anonymize: bool = True,                 # 🆕
) -> str:
```

**新增处理逻辑（插在原有 LLM 调用之前）**：

```python
# 🆕 构建增强 prompt
enhanced_prompt = scenario

# 注入联网搜索结果
try:
    search_query = f"{product} {application} 技术参数 竞品"
    search_result = await sch.web_search(search_query, limit=3)
    if search_result["results"]:
        web_snippets = "\n".join(
            f"- [{r['title']}]({r['url']}): {r['snippet'][:150]}"
            for r in search_result["results"]
        )
        enhanced_prompt += f"\n\n【联网搜索补充数据】\n{web_snippets}"
except Exception:
    pass  # 搜索失败降级，不阻塞主流程

# 注入历史记忆上下文块
if context_block:
    enhanced_prompt += f"\n\n【历史记忆】\n{context_block}"
```

**脱敏后处理**：

```python
# 🆕 输出后脱敏
if anonymize and data.get("reply"):
    import re
    # 替换模式：真实公司名 → [行业标签]
    # 简化实现：如 reply 中出现已知客户名，替换为行业标签
    # 完整实现依赖 CRM 客户名→脱敏标签映射表
    pass  # MVP 阶段先靠 Prompt 约束，不写正则硬替换
```

**多格式输出**：
```python
# 🆕 按 output_format 格式化
reply_text = data.get("reply", "（情报包生成失败）")
formatted = out.format_output(reply_text, output_format, {
    "product": product,
    "application": application,
    "timestamp": str(date.today()),
})
return formatted
```

### 3.4 修改 Tool：specq_log_visit

**新增参数**：

```python
async def specq_log_visit(
    customer_id: int,
    content: str,
    visit_date: str | None = None,
    visit_type: str = "in_person",
    image_paths: list[str] | None = None,    # 🆕
    audio_path: str | None = None,           # 🆕
    video_path: str | None = None,           # 🆕
    api_key: str | None = None,
) -> str:
```

**新增多模态处理（插在存储之前）**：

```python
# 🆕 多模态处理
extra_text = []
if audio_path and os.path.exists(audio_path):
    try:
        audio_text = await mm.process_audio(audio_path)
        extra_text.append(f"【语音转录】{audio_text[:500]}")
    except Exception:
        pass

if image_paths:
    for img in image_paths[:5]:  # 最多处理 5 张
        if os.path.exists(img):
            try:
                img_text = await mm.process_image(img)
                extra_text.append(f"【图片 OCR】{img_text[:300]}")
            except Exception:
                pass

if video_path and os.path.exists(video_path):
    try:
        vid_text = await mm.process_video(video_path)
        extra_text.append(f"【视频摘要】{vid_text[:500]}")
    except Exception:
        pass

if extra_text:
    content = content + "\n\n" + "\n\n".join(extra_text)
```

**自动写入记忆（存储成功后）**：

```python
# 🆕 自动写入长期记忆
try:
    import memory as mem
    summary = content[:300] if len(content) > 300 else content
    vec = mem.embed_text(summary)
    collection = mem.get_chroma_collection()
    mid = f"mem_{uuid.uuid4().hex[:12]}"
    collection.add(
        ids=[mid],
        embeddings=[vec],
        documents=[summary],
        metadatas=[{
            "category": "visit",
            "user_id": "default",
            "customer_id": str(customer_id),
            "timestamp": visit_date or str(date.today()),
        }],
    )
except Exception:
    pass  # 记忆写入失败不阻塞主流程
```

### 3.5 修改 Tool：specq_extract_insights

**新增参数**：

```python
async def specq_extract_insights(
    customer_id: int | None = None,
    limit: int = 10,
    db_path: str | None = None,              # 🆕
    db_query: str | None = None,             # 🆕
    api_url: str | None = None,              # 🆕
    api_params: dict | None = None,          # 🆕
    api_key: str | None = None,
) -> str:
```

**新增数据源处理（插在 LLM 调用之前）**：

```python
# 🆕 本地数据库
db_data = []
if db_path and db_query and os.path.exists(db_path):
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(db_query).fetchall()
        db_data = [dict(r) for r in rows[:100]]  # 限 100 行
        conn.close()
    except Exception:
        pass

# 🆕 在线 API
api_data = []
if api_url:
    try:
        import httpx
        async with httpx.AsyncClient(timeout=10.0) as c:
            r = await c.get(api_url, params=api_params or {})
            if r.status_code == 200:
                api_data = r.json() if isinstance(r.json(), list) else [r.json()]
    except Exception:
        pass

# 注入 LLM prompt
db_text = json.dumps(db_data[:20], ensure_ascii=False, indent=2) if db_data else ""
api_text = json.dumps(api_data[:20], ensure_ascii=False, indent=2) if api_data else ""
# 拼到原有的 user_prompt 中
```

### 3.6 修改 Tool：specq_feedback

**新增参数**：

```python
async def specq_feedback(
    product: str,
    application: str,
    outcome: str,
    lesson: str | None = None,
    accuracy_notes: str | None = None,
    uid: str = "default",                   # 🆕
    api_key: str | None = None,
) -> str:
```

**新增处理（存储成功后）**：

```python
# 🆕 自动写入长期记忆
if outcome and lesson:
    try:
        import memory as mem
        memory_content = f"[{outcome}] {product} - {application}: {lesson}"
        vec = mem.embed_text(memory_content)
        collection = mem.get_chroma_collection()
        mid = f"mem_{uuid.uuid4().hex[:12]}"
        collection.add(
            ids=[mid],
            embeddings=[vec],
            documents=[memory_content],
            metadatas=[{
                "category": "feedback",
                "user_id": uid,
                "product": product,
                "outcome": outcome,
                "timestamp": str(date.today()),
            }],
        )
    except Exception:
        pass

# 🆕 成交率埋点日志（简单写入文件，不做聚合）
try:
    import memory as mem
    analytics_file = os.path.join(mem.get_memory_dir(), "analytics.jsonl")
    with open(analytics_file, "a") as f:
        f.write(json.dumps({
            "event": "feedback",
            "uid": uid,
            "product": product,
            "outcome": outcome,
            "timestamp": str(date.today()),
        }, ensure_ascii=False) + "\n")
except Exception:
    pass
```

---

## 四、SKILL.md 更新

**基于 v1.0 SKILL.md，变更如下**：

1. 标题版本号 `v1.0` → `v2.0`
2. MCP Tool 清单：增加 `specq_memory`（4 action）+ `specq_search`（3 source）
3. 触发条件：增加多任务触发（"帮我做三个情报包"）
4. 工作流：在用户输入后增加 4 步：
   - ① 多模态处理（图片/语音/视频 → 文本）
   - ② 工作记忆检查（get_plan）
   - ③ 长期记忆召回（recall）
   - ④ 联网搜索补充（search）
5. 分支场景：新增场景 E（多任务管理）、场景 F（多模态输入）
6. 新增章：Memory 分类体系表、脱敏规则、多格式输出路由、场景判断规则
7. 重要规则新增：记忆优先、脱敏强制、多模态透明

---

## 五、requirements.txt 更新

新增依赖：
```
chromadb>=0.5.0
requests>=2.31.0
python-docx>=1.1.0
python-pptx>=0.6.23
openai>=1.0.0
httpx>=0.25.0
fastmcp>=1.0.0
python-dotenv>=1.0.0
```

## 六、.env.example 更新

新增：
```ini
SPECQ_DATA_DIR=/home/ubuntu/specq_data
ZHIPU_API_KEY=your-z…-key
SEARCH_API_KEY=your-b…-key
```

保留已有字段不变。

---

## 七、文件结构总览

```
specq-mcp/
├── mcp_server.py          # 6 个 tool 主入口（~900 行）
├── memory.py              # 🆕 记忆模块（ChromaDB + embedding + 工作内存）
├── search.py              # 🆕 联网搜索模块
├── multimodal.py          # 🆕 多模态输入模块（OCR/语音/视频）
├── output.py              # 🆕 多格式输出模块
├── SKILL.md               # ✏️ 更新为 v2.0
├── requirements.txt       # ✏️ 新增 chromadb requests python-docx python-pptx
├── .env.example           # ✏️ 新增 ZHIPU_API_KEY SEARCH_API_KEY SPECQ_DATA_DIR
├── LICENSE                # 不动
└── README.md              # 不动
```

---

## 八、验收条件

### 8.1 memory 模块

```python
import memory as mem
import uuid

# 测试 embedding
vec = mem.embed_text("电镀铜溶液粗糙度测试")
assert len(vec) == 1024

# 测试 ChromaDB
col = mem.get_chroma_collection()
assert col.name == "specq_memory"

# 测试工作记忆读写
uid = str(uuid.uuid4())[:8]
mem.save_working_memory(uid, {"goal": "测试", "plan": ["A","B"], "current_step": 1, "results": {}})
wm = mem.load_working_memory(uid)
assert wm["goal"] == "测试"
```

### 8.2 MCP Server 启动

```bash
python mcp_server.py
# → 服务运行在 http://0.0.0.0:8001/mcp
# → tools/list 应返回 6 个 tool
```

### 8.3 specq_memory 验证

```json
// recall
{"action": "recall", "query": "深南电路", "limit": 3, "uid": "test"}

// save
{"action": "save", "content": "拜访深南，粗糙度不达标", "category": "visit", "uid": "test"}

// set_plan
{"action": "set_plan", "goal": "三个情报包", "plan": ["A","B","C"], "current_step": 1, "uid": "test"}

// get_plan
{"action": "get_plan", "uid": "test"}
```

### 8.4 specq_search 验证

```json
{"query": "电镀铜溶液 安美特 竞品", "limit": 3, "source": "web"}
```

### 8.5 specq_generate_intel（新参数）

```json
{
  "product": "电镀铜溶液",
  "application": "PCB电镀",
  "scenario": "深南电路，降低粗糙度",
  "output_format": "email",
  "context_block": "- 上次拜访：粗糙度不达标",
  "anonymize": true
}
```

---

## 九、实现顺序

1. `memory.py`（先建，因为 generate_intel/feedback 会用到）
2. `search.py`
3. `multimodal.py`
4. `output.py`
5. `mcp_server.py`（最后，依赖以上 4 个模块）
6. `SKILL.md`
7. `requirements.txt` + `.env.example`
8. 本地启动验证

---

## 十、降级策略

| 模块 | 异常处理 |
|---|---|
| memory | embedding 失败 → 返回空结果，不抛异常 |
| search | API 不可用 → 返回空列表，不阻塞主流程 |
| multimodal | 图片/音频/视频处理失败 → 跳过，用原始 content |
| output | 不支持格式 → fallback 到 markdown |
| ChromaDB | 连接失败 → 内存模式 fallback |

**核心原则**：任何非核心模块失败不应阻塞情报包生成主流程。

---

## 十一、代码规范

- 新文件 ≤ 200 行，函数 ≤ 40 行
- 异常不静默吞，至少 return 错误信息或 json.dumps({"error": ...})
- 注释用中文
- 同步操作用 `requests`，异步操作用 `httpx`
- 模块级变量用于缓存（如 ChromaDB collection），模块首次导入时初始化
