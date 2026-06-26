# Workflow Orchestrator 正则排坑记录

> 跨 3 个 session（6/10-6/13）才彻底修好的正则 bug，记录根因和修复方案供未来参考。

## Bug 1: 阶段名吃进整个 body

### 根因

`STAGE_REGEX` 原始写法：

```python
STAGE_REGEX = re.compile(
    r'###\s+(?:阶段|Stage)\s+(\d+)\s*[:：]\s*(.+?)(?=\n###|\n##|\n\Z)',
    re.DOTALL
)
```

问题：`(.+?)` 配合 `re.DOTALL`（让 `.` 匹配换行）、再加上 `(?=\n###|\n##|\Z)` 前瞻——
`(.+?)` 是 lazy 但最小匹配依然是整行到第一个换行，而 `.+` 在 DOTALL 下可以吃进多行。
由于前瞻 `(?=\n###|\n##|\Z)` 要到很远才停，`name` 组把整个 body 文本都吃进去了。

### 症状

```python
parsed["workflow"][0]["name"]
# 期望: "需求分析"
# 实际: "需求分析\n\n**使用的 Skills**:\n- writing-plans\n\n**任务**:\n- 分析需求\n..."
```

### 修复

拆成两个独立捕获组：name 只取标题行 `([^\n]+)`，body 取到下一个同级标题：

```python
STAGE_HEADING_REGEX = re.compile(
    r'###\s+(?:阶段|Stage)\s+(\d+)\s*[:：]\s*([^\n]+)\n(.*?)(?=\n###|\n##|\Z)',
    re.DOTALL
)
```

关键点：`[^\n]+` 严禁跨行，确保 name 就是标题行余下文字；body 用 `(.*?)` 配合 DOTALL 吃到下一个 `###` 或 `##`。

---

## Bug 2: 加粗星号导致列表提取失败

### 根因

DESIGN.md 里阶段内的列表标题用了 Markdown 加粗：

```markdown
**使用的 Skills**:
- writing-plans
```

而原始正则只认无格式的写法：

```python
r'(?:使用的\s*)?[Ss]kills?[:：]\s*\n...'
```

`**使用的 Skills**:` 前面有 `**`，正则直接失配 → skills/tasks/outputs 全部为空列表。

### 症状

```python
parsed["workflow"][0]["skills"]   # 期望: ["writing-plans"]
parsed["workflow"][0]["tasks"]    # 期望: ["分析需求", "编写用户故事"]
parsed["workflow"][0]["outputs"]  # 期望: ["requirements.md"]
# 实际全都是: []
```

### 修复

在关键词前后加 `\*{0,2}` 匹配可选的 Markdown 加粗星号（0或2个星号）：

```python
r'\*{0,2}(?:使用的\s*)?[Ss]kills?\*{0,2}[:：]\s*\n...'
#  ^^^^^^^^^                       ^^^^^^^^^
#  左侧星号                        右侧星号
```

三行正则都需要同样处理：skills、tasks/任务、outputs/输出。

### 注意

`\*{0,2}` 而不是 `\*{0,3}`——Markdown 加粗用**两个**星号，`{0,2}` 足以匹配 `**` 或无星号。
不要用 `\*?` 或 `\**`，因为 `\*?` 只匹配0或1个星号（不够），`\**` 在某些引擎中是非法重复。

---

## Bug 3: `write_file` 写入了占位符文字

### 根因

在 6/11 的会话中，agent 用 `write_file` 写入脚本时，第二个和第三个文件的 content 参数
被错误地传入了占位符文字如 `(see file already created)` 而非真正代码。
（这是 agent 自身的 write_file 参数构造错误，不是 Hermes 工具 bug。）

### 症状

```python
# workflow_orchestrator.py 第1行:
# (see file already created)    ← 占位符文字，不是 Python 代码
```

### 修复

重新调用 `write_file`，确保 content 参数是完整的 Python 脚本代码。

### 教训

对大型文件连续调用 `write_file` 时，要逐个确认写入结果——第 N 个成功不代表第 N+1 个
content 参数没被截断或替换。用 `read_file` 验证前几行即可。
