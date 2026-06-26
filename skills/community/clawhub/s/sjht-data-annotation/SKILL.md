---
name: data-annotation
description: >
  通用数据标注处理工具。当用户提到需要数据标注、有标注任务、数据处理、数据集生成、
  标注查看/编辑时使用此 skill。支持图像、视频、文本等多种数据类型，调用模型进行内容理解
  和标注，生成结构化标注数据，提供 Web 查看编辑界面。
  触发短语：「标注」「annotation」「数据集」「label」「tag data」「数据处理」。
---

# Data Annotation Skill — 数据标注处理工具

完整的数据标注工作流：需求确认 → 制定计划 → 逐条处理 → 结果存储 → Web 查看/编辑 → 部署访问。

## ⚠️ 核心原则：计划驱动，逐条处理，永不超时

**绝对不要一次性批量处理所有数据！** 超时（通常 10 分钟）会导致任务中断、数据丢失。

正确做法：
1. **先制定标注计划**（JSON 格式），列出所有待处理数据
2. **每次只处理 1 条数据**，处理完立即保存
3. **更新计划进度**（标记已完成/失败）
4. **汇报当前进度**（已处理 X/Y，耗时 N 秒）

如果感觉快超时了，**立即保存当前进度并汇报**，下次从计划中未完成的位置继续。

---

## 工作流程

### Step 1: 确认需求

收到标注任务后，**必须先确认**以下信息：

1. **需求文档位置** — 问用户标注需求文档在哪里（路径或 URL）
2. **待标注数据位置** — 问用户原始数据存放在哪个目录
3. **数据类型** — 图像/视频/文本/混合
4. **输出格式** — 如果需求文档中没有说明，询问期望的输出格式

如果用户已提供以上信息，跳过确认直接进入下一步。

### Step 2: 读取需求文档

读取并理解需求文档，提取关键信息。

**docx 文件读取：**
```bash
pip install python-docx
python3 -c "
from docx import Document
doc = Document('<需求文档路径>')
for p in doc.paragraphs: print(p.text)
for table in doc.tables:
    for row in table.rows:
        print(' | '.join(cell.text for cell in row.cells))
"
# 备选方案（python-docx 失败时）：
pandoc <需求文档路径> -t plain  # 需 apt install -y pandoc
```

提取并确认：
- **标注要求** — 需要标注哪些内容（类别、属性、字段）
- **输出格式** — JSONL schema 定义
- **标注规范** — 分类体系、评分标准、特殊规则
- **标签列表** — 需求文档附录中的标签表

**向用户复述需求**，特别是字段、输出结构、标签列表，确认无误后继续。

### Step 3: 扫描数据 + 制定标注计划

扫描数据目录，统计文件数量和类型：

```bash
find <数据目录> -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \
  -o -name "*.mp4" -o -name "*.avi" -o -name "*.txt" \) | wc -l
```

**制定标注计划**，保存为 `<数据目录>/results/plan.json`：

```json
{
  "task_name": "任务描述",
  "created_at": "2026-03-19T14:00:00Z",
  "total_items": 10,
  "processed": 0,
  "failed": 0,
  "items": [
    { "id": 1, "source": "video1.mp4", "type": "video", "status": "pending", "result_file": null },
    { "id": 2, "source": "image_001.jpg", "type": "image", "status": "pending", "result_file": null }
  ]
}
```

对于视频数据，此阶段也执行抽帧（抽帧不计入逐条标注耗时）。

**视频抽帧要求：**
- 每秒至少 2 帧（`ffmpeg -vf fps=2`）
- 短视频（<10s）至少 15 帧
- 中视频（10-30s）至少 20 帧
- 长视频（>30s）至少 30 帧
- 抽帧保存到 `<数据目录>/results/frames/<文件名不含扩展名>/`

**制定计划后向主 Agent 汇报：**
- 数据总量
- 数据类型分布
- 计划处理顺序
- 预估耗时

### Step 4: 逐条处理标注（核心步骤）

**每次只处理 1 条数据！** 处理流程：

```
读取 plan.json → 取下一条 status=pending → 调用模型标注 → 保存结果 → 更新 plan.json → 汇报进度 → 取下一条
```

#### 模型选择策略

| 数据类型 | 处理方式 | 推荐模型 |
|---------|---------|---------|
| **图像** | VL 模型分析图片内容 | `qwen3.5-plus`、`kimi-k2.5`、`doubao-seed-2.0-pro` |
| **视频** | 抽帧后逐帧用 VL 模型 | 同上 |
| **文本** | LLM 文本分析 | 任意文本模型 |
| **音频** | whisper 转写 + LLM | `whisper` + LLM |
| **混合** | 按类型分别处理 | 组合上述方法 |

查看 TOOLS.md 获取已配置的模型 API 信息。

#### 模型 API 调用示例（VL 模型）

```bash
# 使用阿里百炼 qwen3.5-plus 分析图片
curl -s https://coding.dashscope.aliyuncs.com/v1/chat/completions \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-plus",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,<BASE64>"}},
        {"type": "text", "text": "请按照标注要求分析这张图片..."}
      ]
    }]
  }'
```

#### 每条数据处理后立即：

1. **保存到 dataset.jsonl**（追加写入，不要每次重写全量）
2. **更新 plan.json**（标记 status=done，记录耗时）
3. **检查剩余时间**：如果已用超过 60% 的总时间，暂停并汇报进度
4. **汇报当前进度**：`已处理 X/Y（Z%），本条耗时 N 秒`

#### 进度汇报格式

每处理完几条数据后，输出进度：
```
📊 进度：已处理 3/10（30%）
- ✅ video1.mp4 — 完成（耗时 12s）
- ✅ video2.mp4 — 完成（耗时 15s）
- ✅ image_001.jpg — 完成（耗时 3s）
- ⏳ image_002.jpg — 处理中...
```

### Step 5: 保存标注结果

标注结果保存到 **`<数据目录>/results/`** 目录：

```
<数据目录>/
├── data/                  # 原始数据
├── results/
│   ├── plan.json          # 标注计划（进度追踪）
│   ├── dataset.jsonl      # 标注结果（逐条追加）
│   ├── summary.json       # 统计摘要（全部完成后生成）
│   ├── viewer.html        # Web 查看编辑页面
│   ├── frames/            # 视频抽帧图片
│   │   ├── video1/
│   │   └── video2/
│   └── videos/            # 视频副本（供 Web 引用）
└── ...
```

**输出格式要求：**
- 每条标注一个 JSON 对象，一行一条（JSONL）
- 必须包含 `source_file` 和 `annotation_time`
- 字段结构严格遵循需求文档 schema

### Step 6: 生成 Web 查看/编辑页面

参考 `templates/annotation-viewer.html` 模板，根据实际数据生成定制页面。

**页面关键要求（实战经验）：**

1. **三栏布局**：左侧文件列表 | 中间数据展示 | 右侧标注结果
2. **apiBase 必须用 nginx 反代路径**（`/annotation-api/`），不要硬编码 `127.0.0.1:8888`
3. **所有文本字段 contentEditable**，点击即可编辑
4. **标签支持增删**（添加按钮 + × 删除按钮）
5. **保存按钮在右上角**，调用 `POST /annotation-api/` 保存
6. **未保存修改时离开页面要有警告**（`beforeunload` 事件）
7. **标注区块可折叠/展开**
8. **保存成功要有 Toast 提示**

**视频文件处理**：Web 页面引用视频时使用相对路径（`../video.mp4`），通过 nginx 静态服务直接访问，不要走 API。

### Step 7: Nginx 部署

#### ⚠️ 实战经验教训

1. **不要创建独立 server 块监听 80** — 会和已有站点冲突。改为在已有站点配置中添加 location 块
2. **使用 `^~` 前缀匹配** — 避免 nginx 正则 location（如静态文件缓存）优先匹配导致 404
3. **不要在静态缓存规则中包含 mp4** — 大文件不适合强缓存
4. **nginx reload 可能不够，必要时 restart**
5. **`/root` 目录权限必须 755** — 否则 nginx worker 无法访问（root 下默认 700）

#### 正确配置方式

在已有的 nginx 站点配置中添加（如 `/etc/nginx/sites-enabled/default`）：

```nginx
# 标注数据查看（^~ 优先级高于正则，确保 mp4/jpg 不被其他规则劫持）
location ^~ /annotation/ {
    alias /root/annotation-data/;
    autoindex on;
    index viewer.html index.html;
    charset utf-8;
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
    add_header Access-Control-Allow-Headers "Content-Type";
}

# 标注 API 反代
location ^~ /annotation-api/ {
    proxy_pass http://127.0.0.1:8888/;
}
```

**不要删除已有的其他 location 块，只追加。**

#### 数据目录软链接

```bash
mkdir -p /root/annotation-data/
ln -sf <实际数据目录> /root/annotation-data/<项目名>
chmod 755 /root  # 关键！否则 nginx 无法访问
```

#### 启动 API 服务

```bash
fuser -k 8888/tcp 2>/dev/null
nohup python3 <skill路径>/scripts/annotation-api.py --port 8888 --data-dir <数据目录> > <数据目录>/results/api.log 2>&1 &
```

#### 验证

```bash
# 必须完全 restart 而不是 reload
systemctl restart nginx
# 验证 HTML、图片、视频、API 都能正常访问
curl -s -o /dev/null -w "%{http_code}" http://localhost/annotation/<项目名>/results/viewer.html  # 期望 200
curl -s -o /dev/null -w "%{http_code}" http://localhost/annotation/<项目名>/<视频文件>.mp4      # 期望 200
curl -s "http://localhost/annotation-api/" | python3 -c "import sys,json;print(len(json.load(sys.stdin).get('files',[])))"  # 文件数>0
```

## 完成后汇报

每次完成或暂停时，向主 Agent/用户汇报：

1. **进度统计** — 已处理 X/Y（Z%），失败 N 条
2. **本批次耗时**
3. **结果文件位置**
4. **Web 访问地址**
5. **失败数据原因**（如有）
6. **下次续做位置** — 如果未全部完成，说明 plan.json 中从哪个 ID 继续
7. **改进建议**

## 引用文件

- **Web 页面模板**：`templates/annotation-viewer.html`
- **API 服务脚本**：`scripts/annotation-api.py`
- **标注格式参考**：`references/output-formats.md`
