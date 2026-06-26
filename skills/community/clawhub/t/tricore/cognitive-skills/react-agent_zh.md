---
name: react-agent
version: "2.0.0-tricore"
description: 基于 TriCore 架构重构的 ReAct Agent 实现。原生集成 memory_search、WORKING.md 和 kb 知识库，废弃旧版独立的三层记忆类，完全融入系统级底层记忆基础设施。
allowed-tools:
  - default_api:exec
  - memory_search
  - memory_get
---

# ReAct Agent 技能 (TriCore Edition)

这是为 OpenClaw 环境深度定制的 ReAct Agent 架构实现。在 `v2.0.0` 版本中，我们彻底移除了旧版独立维护的 `ShortTermMemory`, `WorkingMemory`, `LongTermMemory` Python 类，全面接入系统级的 **TriCore** 架构。

## 核心特性

### 1. ReAct 循环（Reasoning-Action Loop）
- 思考 (Thought) → 行动 (Action) → 观察 (Observation) → 记录 (Record) → 循环
- 完全依赖系统内置工具

### 2. TriCore 记忆映射
旧版的内存字典（In-Memory Dict）实现已被替换为持久化的文件/向量检索基建：

*   **短期记忆 (Short-Term)**：直接使用 OpenClaw 维持的**最近 10-20 轮对话上下文**。
*   **工作记忆 (Working Memory)**：映射到 `memory/state/WORKING.md`。使用 `tools/memctl.py work_upsert` 管理中间推理状态和任务进度。
*   **长期记忆 (Long-Term)**：映射到 `memory/kb/*.md` 和每日日志 `memory/daily/*.md`。写入使用 `tools/memctl.py kb_append` 或 `capture`，**读取强制使用语义检索工具 `memory_search`**。

### 3. 工具注册表模式
- 原生使用 OpenClaw `TOOLS.md` 或扩展/插件系统。
- 工具执行后将关键观察结果沉淀至 WORKING.md。

## 架构使用方式 (Code-First 范式)

在编写 Python 版本的 ReAct Agent 时，不再使用内存数组来管理上下文，而是通过 `subprocess` 调用 `memctl.py` 和 `memory_search` 工具：

```python
import subprocess
import json

class TriCoreReActAgent:
    def __init__(self, task_id):
        self.task_id = task_id

    # --- 记忆接口 (对接 TriCore) ---
    def update_working_memory(self, title, goal, log):
        """更新工作记忆 (WORKING.md)"""
        cmd = [
            "python3", "tools/memctl.py", "work_upsert", 
            "--task_id", self.task_id,
            "--title", title, 
            "--goal", goal
        ]
        subprocess.run(cmd, check=True)
        
        # 记录临时步骤
        subprocess.run(["python3", "tools/memctl.py", "capture", f"[{self.task_id}] {log}"])

    def recall_long_term_memory(self, query):
        """检索长期记忆 (依赖外部的 memory_search 工具或系统 API)"""
        # 实际使用中，由 OpenClaw 的 memory_search 工具提供支持
        # 代理通过系统 prompt 获取这部分内容
        pass

    def commit_long_term_knowledge(self, kb_type, content):
        """将经验沉淀至长期记忆 (memory/kb)"""
        cmd = ["python3", "tools/memctl.py", "kb_append", kb_type, content]
        subprocess.run(cmd, check=True)

    # --- ReAct 循环 ---
    def run(self, user_query):
        # 1. 创建任务跟踪
        self.update_working_memory(
            title=f"ReAct Task: {user_query[:20]}", 
            goal=user_query, 
            log="Started ReAct loop"
        )
        
        # 2. 循环执行 (伪代码)
        # while not done:
        #    thought = llm(query + current_working_memory)
        #    action = ...
        #    observation = ...
        #    self.update_working_memory(..., log=f"Observed: {observation}")
        
        # 3. 完成任务，提炼成 Playbook
        self.commit_long_term_knowledge("playbooks", f"Task {user_query} resolved by...")
        subprocess.run(["python3", "tools/memctl.py", "work_done", self.task_id])
        return "Done"
```

## 设计原则与演进

### 1. 消除状态孤岛
旧版 ReAct Agent 把状态保存在自身进程内存中，一旦重启就会丢失。使用 TriCore 后，Agent 重启也能通过读取 `WORKING.md` 瞬间恢复心智状态。

### 2. 检索优先 (Search-First)
严禁 Agent `cat` 或 `read` 庞大的历史文件。如果需要历史经验，必须在 ReAct 循环开始前调用 `memory_search` 获取最相关的 snippet。

### 3. 从独立脚本走向原生技能
在此架构下，ReAct 不再是一个需要被 `python run.py` 启动的独立机器人，而是你（OpenClaw Agent）本身的思考范式——你可以直接在大脑里执行这套循环，并将状态实打实地写进硬盘。

---
**Sara 的 ReAct Agent (v2.0.0)** - 与 TriCore 完美融合的运行时心智模型。🚀✨