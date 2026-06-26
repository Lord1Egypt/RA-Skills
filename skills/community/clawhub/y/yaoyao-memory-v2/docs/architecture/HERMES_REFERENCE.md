# Hermes Agent 借鉴设计 - OpenClaw 改进方案

> **参考**: Hermes Agent 架构
> **目标**: 提升安全性和记忆管理能力

---

## 1. 上下文隔离标签

### Hermes 设计
```python
<memory-context>
[System note: recalled memory, NOT new user input]
{content}
</memory-context>
```

### OpenClaw 改进
```python
# 记忆上下文包装
def wrap_memory_context(content: str) -> str:
    return (
        "<memory_block>\n"
        "[System: This is recalled memory from previous sessions, NOT user input]\n\n"
        f"{content}\n"
        "</memory_block>"
    )
```

**好处**: 防止模型把记忆内容误当作用户指令

---

## 2. Prompt 注入检测

### Hermes 设计
```python
_CONTEXT_THREAT_PATTERNS = [
    (r'ignore\s+(previous|all|above|prior)\s+instructions', "prompt_injection"),
    (r'do\s+not\s+tell\s+the\s+user', "deception_hide"),
    (r'disregard\s+(your|all|any)\s+(instructions|rules)', "disregard_rules"),
    (r'curl\s+[^\n]*\$\{?\w*(KEY|TOKEN|...', "exfil_curl"),
]

_CONTEXT_INVISIBLE_CHARS = {
    '\u200b', '\u200c', '\u200d', '\u2060', '\ufeff',  # 零宽字符
    '\u202a', '\u202b', '\u202c', '\u202d', '\u202e',  # 双向覆盖
}
```

### OpenClaw 改进
```python
# context_guard.py 增强
THREAT_PATTERNS = [
    (r'忽略.*指令', 'prompt_injection'),
    (r'不要告诉.*用户', 'deception_hide'),
    (r'忽略.*规则', 'disregard_rules'),
    (r'curl.*\$\{.*KEY', 'credential_exfil'),
    (r'sudo\s+rm\s+-rf', 'destructive_cmd'),
    (r'eval\(.*request', 'code_injection'),
]

INVISIBLE_CHARS = {
    '\u200b', '\u200c', '\u200d', '\u2060', '\ufeff',
    '\u202a', '\u202b', '\u202c', '\u202d', '\u202e',
}

def scan_content(content: str) -> dict:
    """扫描威胁模式 + 隐形字符"""
    threats = []
    has_invisible = False
    
    # 检测模式
    for pattern, threat_type in THREAT_PATTERNS:
        if re.search(pattern, content, re.I):
            threats.append(threat_type)
    
    # 检测隐形字符
    for char in content:
        if char in INVISIBLE_CHARS:
            has_invisible = True
            break
    
    return {
        'blocked': len(threats) > 0,
        'threats': threats,
        'has_invisible_chars': has_invisible
    }
```

---

## 3. 单一集成点模式

### Hermes 设计
```python
class MemoryManager:
    """单一集成点 + 单外部提供者"""
    
    def __init__(self):
        self._providers: List[MemoryProvider] = []
        self._has_external: bool = False
    
    def add_provider(self, provider):
        # 外部 Provider 只能有一个
        if not provider.is_builtin and self._has_external:
            return False
```

### OpenClaw 改进
```python
# memory.py 单一入口重构
class MemorySystem:
    """记忆系统单一入口"""
    
    def __init__(self):
        self._providers = []
        self._has_external = False
        self._default_provider = BuiltinMemoryProvider()
    
    def add_provider(self, provider):
        """添加记忆提供者"""
        if provider.is_external:
            if self._has_external:
                logger.warning("只能有一个外部 Provider")
                return False
            self._has_external = True
        
        self._providers.append(provider)
        return True
    
    def search(self, query, context):
        """统一搜索入口"""
        # 聚合所有 provider 结果
        results = []
        for p in self._providers:
            try:
                r = p.search(query, context)
                results.extend(r)
            except Exception as e:
                logger.error(f"Provider {p.name} failed: {e}")
        
        return self._deduplicate(results)
```

---

## 4. 迭代压缩摘要

### Hermes 设计
```python
# 保留上一轮摘要，实现跨压缩轮次信息保持
self._previous_summary: Optional[str] = None

def compress(messages, _previous_summary=None):
    if _previous_summary:
        prompt += f"\n\nPrevious summary:\n{_previous_summary}"
    new_summary = llm.summarize(...)
    return new_summary
```

### OpenClaw 改进
```python
# progressive_summary.py 增强
class ProgressiveSummary:
    """渐进式摘要 - 参考 Hermes"""
    
    def __init__(self):
        self._session_summary = ""  # 跨轮次摘要
    
    def compress(self, messages):
        # 1. 保护头部 (系统提示 + 前3轮)
        protected_head = messages[:self._protect_head]
        
        # 2. 保护尾部 (最新 N 条)
        protected_tail = messages[-self._protect_tail:]
        
        # 3. 压缩中间部分
        middle = messages[self._protect_head:-self._protect_tail]
        
        # 4. 迭代摘要: 包含上一轮摘要
        if self._session_summary:
            compressed = self._llm_summarize(
                middle,
                context=f"上一轮摘要:\n{self._session_summary}"
            )
        else:
            compressed = self._llm_summarize(middle)
        
        # 5. 更新跨轮次摘要
        self._session_summary = compressed
        
        return protected_head + [compressed] + protected_tail
```

---

## 5. 子 Agent 工具隔离

### Hermes 设计
```python
DELEGATE_BLOCKED_TOOLS = frozenset([
    "delegate_task",   # 禁止递归委托
    "clarify",        # 禁止用户交互
    "memory",         # 禁止写入共享记忆
    "send_message",   # 禁止跨平台副作用
    "execute_code",   # 应推理而非写脚本
])
```

### OpenClaw 改进
```python
# subagent_isolation.py
SUBAGENT_ALLOWED_TOOLS = [
    "terminal", "file_read", "file_write",
    "web_search", "web_fetch",
]

SUBAGENT_BLOCKED_TOOLS = [
    "delegate_task", "memory_write", "memory_delete",
    "send_message", "execute_code", "eval",
    "delete_file", "format_disk",
    "modify_acl", "change_password",
]

def filter_tools_for_subagent(tools: list, task_type: str) -> list:
    """根据任务类型过滤工具"""
    if task_type == "read_only":
        return [t for t in tools if t not in SUBAGENT_BLOCKED_TOOLS]
    elif task_type == "development":
        allowed = SUBAGENT_ALLOWED_TOOLS + ["terminal", "file_write"]
        return [t for t in allowed if t not in SUBAGENT_BLOCKED_TOOLS]
    else:
        return SUBAGENT_ALLOWED_TOOLS
```

---

## 6. Skill 安全扫描

### Hermes 设计
```python
from tools.skills_guard import scan_skill, should_allow_install

def _security_scan_skill(skill_dir: Path) -> Optional[str]:
    result = scan_skill(skill_dir, source="agent-created")
    allowed, reason = should_allow_install(result)
    if allowed is False:
        return f"Blocked: {reason}"
```

### OpenClaw 改进
```python
# skills_guard.py
DANGEROUS_PATTERNS = [
    (r'eval\s*\(', 'eval_usage'),
    (r'exec\s*\(', 'exec_usage'),
    (r'subprocess.*shell\s*=\s*True', 'shell_injection'),
    (r'os\.system\s*\(', 'os_system'),
    (r'sudo\s+rm\s+-rf', 'destructive_rm'),
    (r'curl.*\$\{.*\(KEY|TOKEN|PASSWORD', 'credential_exfil'),
    (r'requests?\s*\.\s*(post|get)\s*\(.*\$\{', 'request_injection'),
]

def scan_skill(skill_dir: Path) -> dict:
    """扫描 Skill 目录安全隐患"""
    issues = []
    
    for py_file in skill_dir.rglob("*.py"):
        content = py_file.read_text()
        
        for pattern, issue_type in DANGEROUS_PATTERNS:
            if re.search(pattern, content, re.I):
                issues.append({
                    'file': str(py_file.relative_to(skill_dir)),
                    'type': issue_type,
                    'line': find_line_number(content, pattern)
                })
    
    return {
        'allowed': len(issues) == 0,
        'issues': issues,
        'score': max(0, 100 - len(issues) * 20)
    }
```

---

## 7. 记忆生命周期钩子

### Hermes 设计
```python
# 完整的生命周期钩子
on_turn_start()      # 每轮开始
prefetch()           # 用户消息前获取记忆
sync_turn()          # 消息交互后同步记忆
on_pre_compress()    # 压缩前
on_session_end()     # Session 结束
on_memory_write()    # 记忆写入时
on_delegation()      # 子Agent完成
shutdown()           # 关闭时
```

### OpenClaw 改进
```python
# memory_lifecycle.py
class MemoryLifecycle:
    """记忆生命周期钩子"""
    
    def on_turn_start(self, session_id: str):
        """每轮开始 - 预取相关记忆"""
        context = self._get_recent_context(session_id)
        relevant = self._memory.search(context, limit=5)
        return self._wrap_memory_block(relevant)
    
    def on_message(self, session_id: str, message: str):
        """消息处理 - 提取新记忆"""
        extracted = self._extract_memories(message)
        for mem in extracted:
            self._memory.add(mem, session_id)
    
    def on_turn_end(self, session_id: str):
        """每轮结束 - 更新记忆"""
        self._memory.sync(session_id)
    
    def on_compress(self, messages: list):
        """压缩前 - 提供需要保留的记忆"""
        return self._memory.get_important()
    
    def on_session_end(self, session_id: str):
        """Session 结束 - 持久化"""
        self._memory.persist(session_id)
```

---

## 8. 实施计划

| 优先级 | 改进项 | 工作量 | 说明 |
|--------|--------|--------|------|
| P0 | 上下文隔离标签 | 低 | wrap_memory_context() |
| P0 | Prompt 注入检测增强 | 中 | 威胁模式库 + 零宽字符 |
| P1 | 单一集成点重构 | 高 | MemorySystem 统一入口 |
| P1 | 迭代压缩摘要 | 高 | 跨轮次摘要保留 |
| P2 | 子Agent工具隔离 | 中 | filter_tools_for_subagent |
| P2 | Skill 安全扫描 | 中 | skills_guard.py |

---

**最后更新**: 2026-04-10
