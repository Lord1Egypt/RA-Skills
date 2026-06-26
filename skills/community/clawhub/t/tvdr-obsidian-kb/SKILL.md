# SKILL.md - Obsidian知识库 API

与Obsidian知识库交互，支持创建笔记、语义搜索、笔记管理。

## 基本信息
- **API地址**: `http://192.168.18.15:5000`
- **健康检查**: `http://192.168.18.15:5000/health`
- **嵌入模型**: qwen3-embedding:8b (通过Ollama)
- **笔记库路径**: `/mnt/share2win/openclaw_datas/obsidian_db/`

## 使用前提

1. 确认API服务运行中：`curl -s http://192.168.18.15:5000/health`
2. 如果服务未启动，需要韩老板手动启动（需要sudo）

## API接口

### 健康检查
```bash
curl -s http://192.168.18.15:5000/health
```

### 创建笔记
```bash
curl -s -X POST http://192.168.18.15:5000/api/note \
  -H "Content-Type: application/json" \
  -d '{
    "title": "笔记标题",
    "content": "# 内容\n\n正文...",
    "tags": ["标签1", "标签2"]
  }'
```

### 搜索笔记（语义搜索）
```bash
curl -s -X POST http://192.168.18.15:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "搜索内容"}'
```

### 获取单个笔记
```bash
curl -s "http://192.168.18.15:5000/api/note?file=笔记文件名.md"
```

### 列出所有笔记
```bash
curl -s http://192.168.18.15:5000/api/notes
```

### 统计信息
```bash
curl -s http://192.168.18.15:5000/api/stats
```

### 重建索引
```bash
curl -s -X POST http://192.168.18.15:5000/api/build
```
> 注：创建笔记后通常会自动索引，如搜索不到新笔记可手动重建。

## 使用场景

1. **保存经验**：将工作中学到的经验、教训写入知识库
2. **知识检索**：搜索历史经验和相关知识
3. **项目文档**：创建和管理项目相关文档
4. **跨agent共享**：所有agent通过同一个API访问同一份知识库

## 身份标识规范（2026-03-24）

每篇笔记**必须**包含 YAML frontmatter 标注来源主机：
```markdown
---
host: 4090服务器 (192.168.18.15)
agent: pm-agent
created: 2026-03-24
updated: 2026-03-24
---
```

### 主机标识
| 称呼 | IP | 说明 |
|------|-----|------|
| 4090服务器/15主机 | 192.168.18.15 | 本机，pm-agent所在 |
| 其他主机 | 待补充 | 韩老板后续添加 |

知识库完全共享，跨主机查询无限制。

## 知识库目录规范

```
obsidian_db/
├── claw_memory/       ← Claw 长期记忆（决策/铁律/角色设定）
├── claw_daily/        ← 每日工作日志（按日期命名）
├── wf_overview/       ← 执行规范总览（EXECUTION_GUIDE 等）
├── wf_composite/      ← 拼图工作流文档
├── wf_i2v/            ← I2V 视频生成工作流（LTX/wan2.2）
├── wf_audio/          ← 音频工作流（TTS/MMAudio）
├── openclaw_ops/      ← OpenClaw 运维/调度经验
├── project_lessons/   ← 项目经验教训（按项目名）
├── Templates/         ← Obsidian 笔记模板
└── _system/           ← 系统文件（API文档/脚本/配置）
```

**铁律**：
- **禁止在根目录创建 md 文件** — 必须放入对应子目录
- 子 agent 创建笔记时必须指定 `folder` 参数
- 目录命名用英文，笔记标题用中文
- 文件命名：`标题.md`（不加点号/空格，用连字符）

## 注意事项
- 笔记保存后会自动索引用于语义搜索
- 语义搜索基于向量相似度，相似度>0.5通常表示高度相关
- tags字段可选，建议添加便于分类检索

## 为小编适配的功能脚本

### 创建编剧工作笔记函数
```bash
create_obsidian_note() {
    local title="$1"
    local content="$2"
    local folder="$3"
    local tags="$4"
    
    local json_data='{
        "title": "'"$title"'",
        "content": "'"$content"'",
        "folder": "'"$folder"'",
        "tags": ['"$tags"']
    }'
    
    curl -s -X POST http://192.168.18.15:5000/api/note \
        -H "Content-Type: application/json" \
        -d "$json_data"
}
```

### 搜索知识库函数
```bash
search_obsidian() {
    local query="$1"
    
    local json_data='{"query": "'"$query"'"}'
    
    curl -s -X POST http://192.168.18.15:5000/api/search \
        -H "Content-Type: application/json" \
        -d "$json_data"
}
```

### 创建编剧工作笔记
```bash
create_script_note() {
    local project_name="$1"
    local note_title="$2"
    local content="$3"
    
    # 编剧专用目录
    local folder="project_${project_name}/scripts"
    
    # 添加来源标识
    local content_with_metadata=$(cat <<EOF
---
host: 4090服务器 (192.168.18.15)
agent: 小编 (编剧)
created: $(date +%Y-%m-%d)
updated: $(date +%Y-%m-%d)
---

${content}
EOF
)
    
    local json_data='{
        "title": "'"$note_title"'",
        "content": "'"$content_with_metadata"'",
        "folder": "'"$folder"'",
        "tags": ["编剧", "'"$project_name"'"]
    }'
    
    echo "创建编剧笔记: $note_title"
    curl -s -X POST http://192.168.18.15:5000/api/note \
        -H "Content-Type: application/json" \
        -d "$json_data"
}
```

### 查看编剧相关笔记
```bash
list_script_notes() {
    local project_name="$1"
    
    curl -s "http://192.168.18.15:5000/api/notes?folder=project_${project_name}/scripts"
}
```

## 使用示例

### 示例1：保存编剧经验
```bash
create_script_note "project_001" "角色塑造技巧" "
# 角色塑造技巧

## 背景
在现代都市剧中的角色塑造...

## 心得
1. 主角要有明确的目标和动机
2. 配角的性格要符合剧情需求
3. 关系网设计要合理...
"
```

### 示例2：搜索相关知识
```bash
search_obsidian "角色塑造经验"
```

### 示例3：创建项目文档
```bash
create_obsidian_note "项目文档" "项目规划" "# 项目规划\n\n## 目标\n\n## 进度\n\n## 问题\n" "project_docs" "项目"
```

### 示例4：编剧工作日志
```bash
create_script_note "work_log" "$(date +%Y-%m-%d)" "
# $(date +%Y-%m-%d) 工作日志

## 今日完成
- 完成了项目001第一集剧本初稿
- 与美术团队讨论场景设计

## 明日计划
- 完善角色对话
- 开始第二集大纲设计
"
```

## 为小编特别优化的功能

### 快速保存创作灵感
```bash
save_idea() {
    local title="$1"
    local idea="$2"
    
    create_script_note "ideas" "灵感_$title" "
# $title

## 灵感内容
${idea}

## 适用场景
## 发展方向
" "灵感" "创意"
}
```

### 记录创作问题
```bash
record_problem() {
    local project="$1"
    local problem="$2"
    local solution="$3"
    
    create_script_note "problems" "${project}_问题记录" "
# ${project} - 问题记录

## 问题描述
${problem}

## 解决方案
${solution}

## 验证方法
" "问题" "经验"
}
```