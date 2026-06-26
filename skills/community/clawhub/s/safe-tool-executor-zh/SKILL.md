---
name: safe-tool-executor-zh
description: |
  安全工具执行器 — 通过分层访问控制强制最低权限执行。
  使用场景：(1) 执行具有破坏潜力的工具，(2) 执行前验证工具安全性，(3) 危险操作需要人工审批，(4) 防止不安全的文件删除。
triggers:
  - "工具安全"
  - "工具执行"
  - "危险命令"
  - "破坏性操作"
  - "人工审批"
  - "最低权限"
author: "Axioma Cluster"
date: "2026-05-17"
version: 1.0.0
tags:
  - 工具安全
  - 执行控制
  - 安全性
  - 最低权限
  - 审批工作流
status: "active"
---

# 安全工具执行器

通过分层访问控制和危险操作人工审批强制安全工具执行。

## 问题：不安全的工具使用

```
症状：
├── 工具权限过高
├── 破坏性操作未被检测
├── 删除重要数据
└── 看门狗警告不够严重
```

## 解决方案

### 1. 最低权限原则

```python
class SafeToolExecutor:
    tool_tiers = {
        '只读': ['ls', 'cat', 'head', 'tail', 'grep'],
        '写入': ['write', 'edit', 'mkdir', 'touch'],
        '删除': ['rm', 'rmdir', 'unlink']
    }
    
    required_approval = ['DELETE', 'DROP', 'TRUNCATE', 'FORMAT']
```

### 2. 审批工作流

```python
def execute_dangerous_tool(action, tool, args):
    if tool in required_approval:
        request_human_approval(f"危险: {tool} {args}")
        wait_for_approval(timeout=60)
        if not approved:
            return {'status': 'BLOCKED', 'reason': 'No approval'}
    return execute_tool(tool, args)
```

### 3. 分层分离

```python
def validate_tool_access(tool, operation):
    # 只读工具不能写入
    if operation == 'WRITE' and tool in tool_tiers['只读']:
        return False
    # 删除工具默认需要审批
    if tool in tool_tiers['删除']:
        return require_approval(tool)
    return True
```

## 看门狗

| 看门狗 | 角色 | 阈值 |
|--------|------|------|
| **VLS** | 逻辑验证 | >0.700 = 阻止 |
| **ABS** | 架构 | 任何删除 = 审批 |
| **STC** | 紧张度 | >0.600 = 警告 |

## 使用方法

```python
from safe_tool_executor import SafeToolExecutor

executor = SafeToolExecutor()

# 只读工具 - 直接通过
result = executor.execute('cat', '/etc/passwd')

# 写入工具 - 警告
result = executor.execute('write', '/project/config.py')

# 删除工具 - 无审批则阻止
result = executor.execute('rm', '/important/file.txt')
# → 阻止: 需要人工审批
```

## 危险模式（阻止）

| 模式 | 操作 |
|------|------|
| `rm -rf /*` | 阻止 + 警报 |
| `DROP TABLE` | 需要审批 |
| `TRUNCATE` | 需要审批 |
| `DELETE /system` | 审批 + 记录 |
| `format` | 完全阻止 |

## 前置条件

| 条件 | 要求 | 检查命令 |
|------|------|----------|
| Python | >= 3.8 | `python3 --version` |
| VLS 看门狗 | 活跃 | `curl -s http://localhost:6333/collections/vls_watchdog` |
| ABS 看门狗 | 活跃 | `curl -s http://localhost:6333/collections/abs_watchdog` |
| Qdrant | 运行中 | `curl -s http://localhost:6333/collections` |

## 文件结构

```
safe-tool-executor/
├── SKILL.md
├── scripts/
│   ├── safe_tool_executor.py
│   ├── main.py
│   └── utils.py
├── data/
├── models/
└── tests/
```