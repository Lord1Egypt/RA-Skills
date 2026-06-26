"""
================================================================================
   🤖 极简万能 Agent (Minimal Universal Agent) v1.0.0
================================================================================

   Author: 王教成 Wang Jiaocheng (波动几何)
   License: MIT

【架构总览】
    本脚本实现了一个"极简万能 AI Agent"，核心理念只有一行公式：

        LLM（大脑） + 命令执行器（手脚） = 万能通用 AI Agent

    为什么"万能"？
    - LLM 能理解任意自然语言任务，并生成对应的代码或命令
    - 命令执行器能运行任何 shell 命令或 Python 脚本
    - Python 脚本能做任何事情（数据处理、网络请求、文件操作、调用 API...）
    - 所以：LLM 生成 Python → Python 能做任何事 → Agent 就能做任何事

【代码结构 — 六大部分】

    第一部分：LLM 接口层（大脑）
      ├── AgentBridge    — 桥接模式：接收外部 Agent 的 LLM 输出（无需 API Key）
      └── LLMBrain       — 独立模式：通过 HTTP API 调用大语言模型

    第二部分：通用命令执行器（手脚）
      └── UniversalExecutor — 执行 shell 命令 / Python 脚本，含安全检测

    第三部分：上下文管理器（记忆系统）
      └── ContextManager — 记录执行历史、学到的知识、用户变量，支持持久化

    第四部分：主 Agent 类 — 编排者
      └── UniversalAgent — 组合以上三者，实现完整的工作流程

    第五部分：预设配置模板
      └── PRESETS — 常用 LLM 提供商的快捷配置

    第六部分：启动入口
      ├── main()              — 交互式引导启动
      ├── parse_args()        — 命令行参数解析
      └── __main__            — 根据参数分发到不同运行模式

【三种运行模式】

    Mode 1 - 独立运行（Standalone）:
        用户直接运行脚本，脚本自己调 LLM API + 自己执行命令
        启动方式: python universal_agent.py --run "任务"
        特点: 完全自包含，需要 API Key

    Mode 2 - 桥接执行（Bridge）:
        外部 Agent（如 WorkBuddy/Cursor）提供"大脑"，脚本负责"手脚"
        启动方式: python universal_agent.py --backend bridge --run "任务"
        特点: 不需要 API Key，复用脚本的安全/重试/记忆功能

    Mode 3 - Skill 模拟（Simulation）:
        外部 Agent 阅读 SKILL.md 后，用自己的能力模拟整个流程
        特点: 不运行此脚本，仅作为架构参考

【工作流详解 — run() 方法的四个阶段】

    阶段1 - 思考 (Think):
        LLM 接收用户的自然语言输入，分析任务复杂度，决定生成什么：
        - 简单任务（如"列出文件"）→ 生成一条 shell 命令（type=command）
        - 复杂任务（如"分析CSV趋势"）→ 生成完整 Python 脚本（type=script）
        - 多步任务（如"打包部署"）→ 生成多行命令序列（type=multi_step）

    阶段2 - 执行 (Execute):
        根据决策结果，调用 UniversalExecutor 执行：
        - command 类型 → _execute_command() 通过 subprocess 调用 shell
        - script 类型  → _execute_script() 写入临时 .py 文件后用 python 执行
        执行前会先经过 _check_danger() 安全检查

    阶段3 - 修复 (Fix) — 可选循环:
        如果执行失败（返回码非0或有错误输出），进入自动修复回路：
        - 将错误信息 + 原始代码发送给 LLM
        - LLM 分析错误原因，生成修复后的代码
        - 重新执行修复后的代码
        - 最多重试 max_retries 次（默认2次）

    阶段4 - 总结 (Summarize):
        LLM 将原始执行输出翻译成人类友好的自然语言总结，
        包含：完成状态、关键数据、发现的问题、后续建议

【跨平台策略】
    Windows: 使用 cmd.exe /c 执行命令，CREATE_NO_WINDOW 避免弹窗
    macOS/Linux: 使用 shell=True 执行命令（bash/zsh）
    Python 脚本: 统一使用 sys.executable（当前解释器），确保跨平台一致

【依赖说明】
    零外部依赖 — 仅使用 Python 标准库（os, sys, json, re, subprocess, time...）
    可选依赖: requests 库（优先使用，比 urllib 更方便；未安装时自动降级到 urllib）

【使用方式】
    # 作为独立程序运行
    python universal_agent.py                          # 交互模式
    python universal_agent.py --run "列出当前目录文件"   # 单次任务

    # 作为模块导入使用
    from scripts.universal_agent import UniversalAgent
    agent = UniversalAgent(api_key="your-key")
    agent.run("帮我分析这个数据集")

    # Bridge 模式（供外部 Agent 调用）
    python universal_agent.py --backend bridge --run "任务描述"
"""
import os
import sys

# ---------------------------------------------------------------------------
# SCRIPT_DIR — 脚本所在目录的绝对路径
# ---------------------------------------------------------------------------
# 作用：确保配置文件（config.json）的路径始终相对于脚本自身位置，
#       而不是相对于用户当前的工作目录（cwd）。
#
# 为什么需要这样做？
#   用户可能从任意目录运行此脚本，例如：
#     cd /home/user/projects && python /path/to/scripts/universal_agent.py
#   如果用相对路径 'config.json'，Python 会在 cwd（/home/user/projects）下查找，
#   而不是在脚本所在目录下查找，导致 "FileNotFoundError"。
#
# 解决方案：
#   os.path.abspath(__file__) 获取脚本的绝对路径
#   os.path.dirname() 取其所在目录 → 无论从哪里运行都能正确定位 config.json
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
import json
import re
import subprocess
import time
from datetime import datetime
from typing import Optional, Dict, List, Any


# ============================================================
# 第一部分：LLM 接口层（大脑）
# ============================================================
# 本部分定义了两种"大脑"实现：
#   1. AgentBridge — 桥接模式，从外部 Agent 接收 LLM 输出
#   2. LLMBrain    — 独立模式，通过 HTTP API 调用 LLM
#
# 两者实现了相同的接口方法（think / generate_script / summarize / debug_and_fix），
# 所以 UniversalAgent 可以在运行时通过 backend 参数切换"大脑"，而无需修改其他代码。
# 这种设计模式叫做"策略模式（Strategy Pattern）".
# ============================================================

class AgentBridge:
    """
    通用 Agent Bridge 模式 LLM 接口
    
    供任何加载了此 Skill 的 Agent 使用。
    
    工作原理：
    - 外部 Agent（如 WorkBuddy、Cursor、任何 AI IDE/工具）充当"大脑"
    - 脚本通过标准输入/环境变量/临时文件接收 Agent 生成的命令或脚本
    - 脚本自身的 UniversalExecutor 负责执行（含安全检测、自动重试）
    - 执行结果返回给外部 Agent 进行总结
    
    优势：
    - 复用脚本内置的安全机制（_check_danger）
    - 复用脚本的自动重试能力（debug_and_fix 回路）
    - 复用脚本的记忆持久化系统（ContextManager）
    - 不需要额外的 API Key
    - 任何有 LLM + 命令执行能力的 Agent 都可使用
    
    通信协议：
    - 输入：JSON 格式，包含 think/generate_script/summarize/debug_and_fix 的结果
    - 输出：JSON 格式，包含执行结果和状态
    """
    
    def __init__(self, input_source: str = "env", work_dir: str = None):
        """
        初始化 Bridge 模式
        
        Args:
            input_source: 输入来源
                - "env": 从环境变量读取（默认，适合 execute_command 调用）
                - "stdin": 从标准输入读取（适合管道调用）
                - "file": 从临时文件读取（适合复杂场景）
            work_dir: 工作目录（默认为当前目录）
        self.input_source = input_source
        self.work_dir = work_dir or os.getcwd()
        self._pending_request = None
        self._response_cache = {}
    
    def _read_bridge_input(self, request_type: str) -> str:
        """
        从外部 Agent 读取输入 — Bridge 模式的核心通信方法
        
        【四种输入方式及优先级（从高到低）】
        
        ① 环境变量 (env) — 最常用：
           外部 Agent 在执行脚本前 set UA_THINK=...
           大多数 Agent 的 execute_command 都支持设置环境变量
           
        ② 标准输入 (stdin) — 管道调用：
           echo '...' | python ... --backend bridge
           
        ③ 临时文件 (.ua_bridge_request.json) — 复杂场景：
           写入 JSON 文件 → 脚本读取后自动删除
           
        ④ 程序化缓存 (_response_cache) — 模块导入：
           通过 bridge.set_response() 预先设置（见 README 模块示例）
            
        Args:
            request_type: 请求类型 (think / generate_script / summarize / debug_and_fix)
            
        Returns:
            外部 Agent 提供的文本内容
            
        Raises:
            BridgeInputError: 当所有来源都没有找到输入时抛出，附带详细的使用提示
        """
        # 方式1：环境变量（最常用，execute_command 可设置环境变量）
        env_value = os.environ.get(f'UA_{request_type.upper()}')
        if env_value:
            return env_value
        
        # 方式2：stdin
        if self.input_source == "stdin" and not sys.stdin.isatty():
            try:
                data = sys.stdin.read()
                if data and data.strip():
                    return data.strip()
            except:
                pass
        
        # 方式3：临时文件
        bridge_file = os.path.join(self.work_dir, '.ua_bridge_request.json')
        if os.path.exists(bridge_file):
            try:
                with open(bridge_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                result = data.get(request_type, data.get('content', ''))
                if result:
                    # 读取后清理
                    os.remove(bridge_file)
                    return result
            except:
                pass
        
        # 方式4：直接缓存（程序化调用时使用）
        if request_type in self._response_cache:
            return self._response_cache.pop(request_type)
        
        raise BridgeInputError(
            f"未收到外部 Agent 的 [{request_type}] 输入。\n"
            f"请通过以下任一方式提供：\n"
            f"  环境变量: set UA_{request_type.upper()}=<内容>\n"
            f"  临时文件: 写入 .ua_bridge_request.json\n"
            f"  标准输入: echo <内容> | python ... --backend bridge\n"
            f"  程序化: bridge.set_response('{request_type}', '<内容>')"
        )
    
    def set_response(self, request_type: str, content: str):
        """程序化设置响应内容（供模块化调用）"""
        self._response_cache[request_type] = content
    
    def think(self, user_input: str, context: str = None) -> Dict[str, str]:
        """
        理解用户意图 — 由外部 Agent 完成
        
        期望外部 Agent 返回 JSON 格式的决策结果
        
        Returns:
            {"type": "command|script|multi_step", "content": "...", "explanation": "..."}
        raw_response = self._read_bridge_input('think')
        
        # 尝试解析 JSON
        if raw_response.startswith('{'):
            try:
                return json.loads(raw_response)
            except json.JSONDecodeError:
                pass
        
        # 智能判断类型
        if any(kw in raw_response for kw in ['def ', 'import ', 'class ', 'for ', 'while ', 'if __name__']):
            return {"type": "script", "content": raw_response}
        
        return {"type": "command", "content": raw_response}
    
    def generate_script(self, task_description: str, requirements: str = None) -> str:
        """
        生成 Python 脚本 — 由外部 Agent 完成
        raw_response = self._read_bridge_input('generate_script')
        
        # 清理可能的 markdown 标记
        code = re.sub(r'^```python\s*', '', raw_response.strip())
        code = re.sub(r'^```\s*', '', code.strip())
        code = re.sub(r'\s*```\s*$', '', code.strip())
        
        return code.strip()
    
    def summarize(self, execution_result: str, original_task: str) -> str:
        """
        总结执行结果 — 由外部 Agent 完成
        return self._read_bridge_input('summarize')
    
    def debug_and_fix(self, error_output: str, original_code: str, task: str) -> str:
        """
        修复错误代码 — 由外部 Agent 完成
        raw_response = self._read_bridge_input('debug_and_fix')
        
        code = re.sub(r'^```python\s*', '', raw_response.strip())
        code = re.sub(r'^```\s*', '', code.strip())
        code = re.sub(r'\s*```\s*$', '', code.strip())
        
        return code.strip()


class BridgeInputError(Exception):
    """Bridge 模式下缺少外部 Agent 输入时抛出"""
    pass


class LLMBrain:
    """
    大语言模型接口 - 负责理解、推理、生成
    
    这是Agent的"大脑"，提供：
    - 自然语言理解能力
    - 任务分解与规划能力
    - 命令/代码生成能力
    - 结果分析与总结能力
    """
    
    def __init__(self, 
                 api_key: str, 
                 model: str = "gpt-4o", 
                 base_url: str = None,
                 timeout: int = 120):
        """
        初始化LLM大脑
        
        Args:
            api_key: API密钥（Ollama可填任意值如"ollama"）
            model: 模型名称，如 "gpt-4o", "deepseek-chat", "llama3"
            base_url: API端点URL
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key
        self.model = model
        self.base_url = (base_url or "https://api.openai.com/v1").rstrip('/')
        self.timeout = timeout
        
        # 尝试导入requests，如果没有则用urllib
        try:
            import requests as req_lib
            self._http = req_lib
            self._use_requests = True
        except ImportError:
            import urllib.request
            self._http = urllib.request
            self._use_requests = False
    
    def think(self, user_input: str, context: str = None) -> Dict[str, str]:
        """
        核心方法：理解用户意图，自动决定生成命令还是脚本
        
        【这是 Agent "智能" 的体现 — LLM 在这里做任务规划决策】
        
        工作原理：
          1. 构建一个详细的 system prompt，包含：
             - 当前运行环境信息（OS、Python版本、当前目录等）
             - 输出格式规范（必须是 JSON）
             - 三种类型的判断标准
             - 安全规则
             
          2. 将用户的自然语言输入 + 上下文（如有）一起发送给 LLM
          
          3. LLM 返回 JSON 决策结果：
             {"type": "command|script|multi_step", "content": "...", "explanation": "..."}
          
          4. 用 _parse_response() 解析 LLM 的返回（处理各种格式变体）
        
        【为什么要把环境信息注入 prompt？】
          因为 LLM 需要知道运行环境才能生成正确的命令：
          - Windows 下生成 "dir /b"，Linux/Mac 下生成 "ls"
          - 知道 Python 版本才能决定用 f-string 还是 format
          - 知道当前目录才能生成相对路径
        
        Args:
            user_input: 用户的自然语言输入（如"列出当前目录的文件"）
            context: 当前上下文信息（历史任务、学到的知识、变量等）
            
        Returns:
            {"type": "command|script|multi_step", "content": "...", "explanation": "..."}
        """
        
        system_prompt = f"""你是一个通用任务执行助手（Universal Task Executor）。

## 你的核心能力
你能将用户的自然语言请求转化为可执行的命令序列或Python脚本。

## 当前运行环境
- 操作系统：{self._detect_os()}
- 系统平台：{sys.platform}
- 当前目录：{os.getcwd()}
- Python版本：{sys.version.split()[0]}
- Python解释器：{sys.executable}

## 工作流程
1. 理解用户想要做什么
2. 判断任务的复杂度
3. 决定最佳执行方式：
   - **简单任务**（单条命令能完成）：生成 shell 命令
   - **复杂任务**（需要逻辑/循环/条件）：生成完整Python脚本
   - **多步骤任务**（需要多步操作）：生成命令序列
4. 输出规范的JSON格式响应

## 输出格式要求
你必须严格输出JSON格式：
```json
{{
  "type": "command 或 script 或 multi_step",
  "content": "...",
  "explanation": "简要说明你的决策理由"
}}
```

### type字段说明：
- `command`: 单条shell命令（适合简单文件操作、系统查询等）
- `script`: 完整Python脚本（适合数据处理、复杂逻辑、需要调用库的任务）
- `multi_step`: 多步命令序列，每步用换行分隔（适合需要按顺序执行多个独立命令）

### content字段说明：
- 如果是command：直接写shell命令文本
- 如果是script：写完整的、可直接运行的Python代码
- 如果是多步：写多条命令，每行一条，按执行顺序排列

## 安全规则
- 危险操作在输出中标注 [DANGER] 前缀
- 涉及数据删除的操作要特别谨慎
- 不要执行未经确认的破坏性操作
"""
        
        if context:
            system_prompt += f"\n\n--- 当前上下文 ---\n{context}\n"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        response = self._call_api(messages)
        
        # 解析JSON响应
        return self._parse_response(response)
    
    def generate_script(self, task_description: str, requirements: str = None) -> str:
        """
        专门用于生成Python脚本的接口
        
        Args:
            task_description: 任务描述
            requirements: 额外的需求说明
            
        Returns:
            完整的Python脚本代码
        """
        
        prompt = f"""请为以下任务生成一个完整、可直接运行的Python脚本：

任务：{task_description}

{'额外需求：' + requirements if requirements else ''}

要求：
1. 脚本必须完整，包含所有必要的import语句
2. 添加适当的错误处理（try-except）
3. 在关键步骤打印进度信息
4. 最终输出清晰的执行结果
5. 使用标准库优先，如果需要第三方库请注释说明安装方式
6. 脚本开头添加中文注释说明功能

请直接输出Python代码，不要用markdown包裹。"""
        
        messages = [{"role": "user", "content": prompt}]
        raw_response = self._call_api(messages)
        
        # 清理可能的markdown标记
        code = re.sub(r'^```python\s*', '', raw_response.strip())
        code = re.sub(r'^```\s*', '', code.strip())
        code = re.sub(r'\s*```\s*$', '', code.strip())
        
        return code.strip()
    
    def summarize(self, execution_result: str, original_task: str) -> str:
        """将执行结果翻译成人类友好的自然语言总结"""
        
        # 截断过长的输出（节省token）
        result_preview = execution_result[-3000:] if len(execution_result) > 3000 else execution_result
        
        prompt = f"""请将以下命令/脚本的执行结果翻译成简洁明了的中文总结。

【原始任务】
{original_task}

【执行输出】
```
{result_preview}
```

请按以下格式输出总结：

---
📋 **任务执行报告**

**状态**: ✅成功 / ⚠️部分完成 / ❌失败

**完成内容**:
(具体完成了什么，包含数据：处理了多少文件、耗时等)

**关键发现**:
(如果有值得注意的信息)

**建议**:
(如有后续操作建议则列出，否则省略)
---

注意：
- 用简洁的中文描述
- 包含具体的数字和数据
- 如果出错了，分析可能的原因
"""
        
        messages = [{"role": "user", "content": prompt}]
        return self._call_api(messages)
    
    def debug_and_fix(self, error_output: str, original_code: str, task: str) -> str:
        """当执行出错时，让LLM分析错误并修复代码"""
        
        prompt = f"""以下代码执行时出现了错误，请分析错误原因并修复代码。

【任务目标】
{task}

【原始代码】
```python
{original_code[:2000]}
```

【错误输出】
```
{error_output[-2000:] if len(error_output) > 2000 else error_output}
```

请：
1. 分析错误原因（简述）
2. 输出修复后的完整代码（不要省略任何部分）
3. 只输出修复后的Python代码，不需要解释
"""
        
        messages = [{"role": "user", "content": prompt}]
        raw_response = self._call_api(messages)
        
        # 清理markdown标记
        code = re.sub(r'^```python\s*', '', raw_response.strip())
        code = re.sub(r'^```\s*', '', code.strip())
        code = re.sub(r'\s*```\s*$', '', code.strip())
        
        return code.strip()
    
    def _call_api(self, messages: List[Dict]) -> str:
        """调用LLM API（自动选择requests或urllib）"""
        
        url = f"{self.base_url}/chat/completions"
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 8192
        }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        if self._use_requests:
            return self._call_with_requests(url, data, headers)
        else:
            return self._call_with_urllib(url, data, headers)
    
    def _call_with_requests(self, url: str, data: dict, headers: dict) -> str:
        """使用requests库发送请求"""
        try:
            response = self._http.post(
                url,
                json=data,
                headers=headers,
                timeout=self.timeout
            )
            result = response.json()
            
            if 'error' in result:
                return f"API错误: {result['error'].get('message', str(result['error']))}"
            
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            
            return f"未知响应格式: {json.dumps(result, ensure_ascii=False)[:500]}"
            
        except Exception as e:
            return f"请求失败: {str(e)}"
    
    def _call_with_urllib(self, url: str, data: dict, headers: dict) -> str:
        """使用urllib发送请求（无需第三方库）"""
        try:
            req_data = json.dumps(data).encode('utf-8')
            req = self._http.Request(
                url,
                data=req_data,
                headers=headers
            )
            
            with self._http.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode('utf-8'))
                
                if 'error' in result:
                    return f"API错误: {result['error'].get('message', str(result['error']))}"
                
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                
                return f"未知响应格式: {json.dumps(result, ensure_ascii=False)[:500]}"
                
        except Exception as e:
            return f"请求失败: {str(e)}"
    
    def _parse_response(self, raw_response: str) -> Dict[str, str]:
        """解析LLM的响应，提取JSON"""
        
        # 尝试提取JSON
        patterns = [
            r'\{[\s\S]*"type"[\s\S]*"content"[\s\S]*\}',  # 宽松匹配
            r'```json\s*(\{.*?\})\s*```',                   # markdown中的JSON
            r'(\{[^{}]*"type"[^{}]*"content"[^{}]*\})',      # 紧凑JSON
        ]
        
        for pattern in patterns:
            match = re.search(pattern, raw_response, re.DOTALL | re.IGNORECASE)
            if match:
                try:
                    json_str = match.group(1) if match.lastindex else match.group(0)
                    parsed = json.loads(json_str)
                    if 'type' in parsed and 'content' in parsed:
                        return parsed
                except json.JSONDecodeError:
                    continue
        
        # 如果无法解析为JSON，将整个响应作为command返回
        content = raw_response.strip()
        
        # 智能判断是否像是代码
        if any(keyword in content for keyword in ['def ', 'import ', 'class ', 'for ', 'while ', 'if __name__']):
            return {"type": "script", "content": content}
        
        return {"type": "command", "content": content}
    
    @staticmethod
    def _detect_os() -> str:
        """检测当前操作系统详细信息"""
        import platform
        system = platform.system()
        release = platform.release()
        machine = platform.machine()
        
        if system == 'Windows':
            version = platform.version()
            return f"Windows {version} ({machine})"
        elif system == 'Darwin':
            ver = platform.mac_ver()[0]
            return f"macOS {ver} ({machine})"
        else:
            dist = ""
            try:
                with open('/etc/os-release') as f:
                    for line in f:
                        if line.startswith('PRETTY_NAME='):
                            dist = line.split('=')[1].strip('"')
                            break
            except:
                pass
            return f"{dist or 'Linux'} ({system} {release}, {machine})"


# ============================================================
# 第二部分：通用命令执行器（手脚）
# ============================================================

class UniversalExecutor:
    """
    通用命令执行器 - Agent的"手脚"
    
    能力范围：
    - 执行任意shell命令（跨平台：Win/Linux/Mac）
    - 执行Python脚本（动态生成的代码）
    - 安全机制：危险命令检测与确认
    - 执行历史记录
    - 错误捕获与返回
    """
    
    # 高危命令模式（正则表达式列表）
    HIGH_DANGER_PATTERNS = [
        r'rm\s+(-rf|-r\s+f|-f)\s+[~/]?(\.\*|/|\*)',
        r'rm\s+-rf?\s+[/~]',
        r'del\s+/[SFQ]\s+[a-zA-Z]:\\',
        r'del\s+/[SFQ]\s+(/s\s+)?C:\\',
        r'format\s+[a-zA-Z]:\s*/[qx]',
        r'shutdown\s+(/s|-h)',
        r'reboot\s*(-f)?\s*$',
        r':\(\)\s*\{\s*:\s*\|\s*:\s*&\s*;\s*:\s*\}',  # Fork炸弹
        r'>\s*\/dev\/sd[a-z]\d?',
        r'mkfs(\.[a-z]+)?\s+\/dev',
        r'dd\s+if=.*of=\/dev\/',
        r'chmod\s+(-R\s+)?777',
        r'chown\s+-R.*\/(etc|usr|bin|var)',
        r'drop\s+(database|table)\s+',
        r'truncate\s+table',
        r'DROP\s+(DATABASE|TABLE)',
        r'git\s+push\s+--force.*master',
        r'git\s+reset\s+--hard.*HEAD~',
    ]
    
    # 中危命令模式
    MEDIUM_DANGER_PATTERNS = [
        r'\bpip\s+uninstall\b',
        r'\bnpm\s+uninstall\b',
        r'\bsudo\s+',
        r'net\s+stop\s+',           # Windows停止服务
        r'taskkill\s+(/F\s+)?/IM',  # 强制结束进程
        r'kill\s+-9\s+',            # Linux强制杀进程
        r'regedit',                 # Windows注册表编辑
        r'bcdedit',                 # Windows启动配置
        r'fdisk',                   # 磁盘分区
        r'cryptsetup',              # 加密设置
    ]
    
    def __init__(self, 
                 auto_approve_dangerous: bool = False,
                 command_timeout: int = 300,
                 script_timeout: int = 600):
        """
        Args:
            auto_approve_dangerous: 是否自动批准危险操作（生产环境应设为False）
            command_timeout: 命令执行超时时间（秒）
            script_timeout: 脚本执行超时时间（秒）
        """
        self.auto_approve = auto_approve_dangerous
        self.command_timeout = command_timeout
        self.script_timeout = script_timeout
        self.history: List[Dict] = []
        
    def execute(self, content: str, is_script: bool = False) -> Dict[str, Any]:
        """
        执行命令或脚本的主入口
        
        Args:
            content: 要执行的命令或脚本内容
            is_script: 是否为Python脚本
            
        Returns:
            {
                "success": bool,
                "output": str,
                "return_code": int,
                "duration": float,
                "command_or_script": str,
                "error": str (可选)
            }
        """
        
        start_time = time.time()
        
        # 安全检查
        danger_level = self._check_danger(content)
        
        if danger_level == 'high':
            if not self.auto_approve:
                print("\n" + "=" * 60)
                print("⚠️  【高危操作警告】")
                print("=" * 60)
                print(f"检测到以下操作被判定为高危：")
                print("-" * 60)
                print(content[:500])
                print("-" * 60)
                print("\n此操作可能导致不可逆的数据丢失！")
                
                confirm = input("\n是否继续执行？输入 'yes' 确认: ")
                if confirm.lower().strip() != 'yes':
                    self._record_history(content, False, "用户取消高危操作", time.time() - start_time)
                    return {
                        "success": False,
                        "output": "",
                        "error": "用户取消了高危操作的执行"
                    }
        
        elif danger_level == 'medium':
            if not self.auto_approve:
                print(f"\n⚠️  检测到中等风险操作，正在执行...")
        
        # 执行
        try:
            if is_script:
                result = self._execute_script(content)
            else:
                result = self._execute_command(content)
            
            duration = time.time() - start_time
            result["duration"] = round(duration, 2)
            result["command_or_script"] = content
            
            # 记录历史
            self._record_history(
                content, 
                result.get("success", False),
                result.get("output", ""),
                duration
            )
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            error_result = {
                "success": False,
                "output": "",
                "error": str(e),
                "duration": round(duration, 2),
                "command_or_script": content
            }
            self._record_history(content, False, str(e), duration)
            return error_result
    
    def _execute_command(self, command: str) -> Dict[str, Any]:
        """
        执行 Shell 命令 — 跨平台实现
        
        【跨平台策略详解】
        
        Windows (os.name == 'nt'):
          使用 subprocess.Popen + ['cmd.exe', '/c', command]
          - cmd.exe /c 是 Windows 下执行命令的标准方式
          - 不用 shell=True，避免命令注入风险
          - CREATE_NO_WINDOW 标志防止弹出黑色控制台窗口
          
        Linux / macOS:
          使用 subprocess.Popen + command, shell=True
          - Unix 系统的 shell（bash/zsh）原生支持管道、重定向、通配符
          - shell=True 让这些特性正常工作
          - Unix 环境下 shell=True 的安全性风险相对可控
        
        【实时输出机制】
          使用 readline() 逐行读取 stdout，而非等进程结束后一次性读取：
          - 用户能看到实时进度（如下载进度条、编译输出）
          - 长时间运行的任务不会看起来像"卡死"
          - bufsize=1 启用行缓冲，确保每行立即输出
        
        【超时处理】
          process.wait(timeout=self.command_timeout)
          超时后调用 process.kill() 强制终止子进程
        """
        
        print(f"\n{'=' * 60}")
        print(f"🔧  执行命令")
        print(f"{'=' * 60}")
        print(f"$ {command}")
        print(f"{'─' * 60}\n")
        
        sys.stdout.flush()
        
        try:
            # 根据操作系统选择执行方式
            if os.name == 'nt':  # Windows
                process = subprocess.Popen(
                    ['cmd.exe', '/c', command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
                )
            else:  # Linux/macOS
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
            
            # 实时输出
            output_lines = []
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    print(line, end='')
                    sys.stdout.flush()
                    output_lines.append(line)
            
            # 等待完成（带超时）
            try:
                returncode = process.wait(timeout=self.command_timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                returncode = -1
                output_lines.append("\n[错误] 命令执行超时！")
            
            output = ''.join(output_lines)
            
            print(f"\n{'─' * 60}")
            status = "✅ 成功" if returncode == 0 else f"⚠️  退出码: {returncode}"
            print(f"状态: {status} | 耗时: ...")
            print(f"{'=' * 60}\n")
            
            return {
                "success": returncode == 0,
                "return_code": returncode,
                "output": output
            }
            
        except FileNotFoundError as e:
            return {
                "success": False,
                "return_code": -1,
                "output": f"命令未找到: {e}"
            }
        except Exception as e:
            return {
                "success": False,
                "return_code": -1,
                "output": f"执行异常: {str(e)}"
            }
    
    def _execute_script(self, script_content: str) -> Dict[str, Any]:
        """
        执行 Python 脚本 — 将 LLM 生成的代码写入临时文件并运行
        
        【为什么要把代码写到文件再执行，而不是直接 exec()/eval()？】
          1. 安全性：exec() 可以访问调用者作用域的所有变量，风险高
          2. 隔离性：子进程的崩溃不会影响主 Agent 进程
          3. 调试方便：用户可以查看 _agent_task_*.py 文件来调试
          4. 完整支持：import、if __name__ == '__main__' 等都能正常工作
          
        【文件命名规则】
          _agent_task_{时间戳}.py — 例如 _agent_task_20260406024800.py
          前缀下划线表示临时文件，可通过 cleanup_temp_files() 批量清理
          
        【执行方式】
          使用 sys.executable（当前 Python 解释器）+ -u 参数（无缓冲输出）
          -u 确保 print() 立即刷新，实现实时输出效果
        """
        
        # 创建临时脚本文件
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        script_filename = f"_agent_task_{timestamp}.py"
        script_path = os.path.join(os.getcwd(), script_filename)
        
        # 写入脚本文件
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"\n{'=' * 60}")
        print(f"🐍  执行Python脚本")
        print(f"{'=' * 60}")
        print(f"📄 文件: {script_path}")
        print(f"📏 大小: {len(script_content)} 字符")
        print(f"{'─' * 60}\n")
        
        sys.stdout.flush()
        
        try:
            # 使用当前Python解释器执行
            process = subprocess.Popen(
                [sys.executable, '-u', script_path],  # -u 无缓冲输出
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=os.getcwd(),
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            # 实时输出
            output_lines = []
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    print(line, end='')
                    sys.stdout.flush()
                    output_lines.append(line)
            
            # 等待完成
            try:
                returncode = process.wait(timeout=self.script_timeout)
            except subprocess.TimeoutExpired:
                process.kill()
                returncode = -1
                output_lines.append("\n[错误] 脚本执行超时！")
            
            output = ''.join(output_lines)
            
            print(f"\n{'─' * 60}")
            status = "✅ 成功" if returncode == 0 else f"⚠️  退出码: {returncode}"
            print(f"状态: {status}")
            print(f"📍 脚本已保留: {script_path}")
            print(f"{'=' * 60}\n")
            
            return {
                "success": returncode == 0,
                "return_code": returncode,
                "output": output,
                "script_file": script_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "return_code": -1,
                "output": f"脚本执行异常: {str(e)}",
                "script_file": script_path
            }
    
    def _check_danger(self, command: str) -> str:
        """
        检查命令的危险等级
        
        Returns:
            'high' - 高危（必须确认）
            'medium' - 中危（警告）
            'low' - 低危（正常执行）
        """
        cmd_combined = command + ' '
        
        for pattern in self.HIGH_DANGER_PATTERNS:
            if re.search(pattern, cmd_combined, re.IGNORECASE):
                return 'high'
        
        for pattern in self.MEDIUM_DANGER_PATTERNS:
            if re.search(pattern, cmd_combined, re.IGNORECASE):
                return 'medium'
        
        return 'low'
    
    def _record_history(self, command: str, success: bool, output: str, duration: float):
        """记录执行历史"""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "command": command[:200] + "..." if len(command) > 200 else command,
            "success": success,
            "output_preview": output[:100].replace('\n', ' ') if output else "",
            "duration_seconds": round(duration, 2)
        })
        
        # 保持历史记录不超过1000条
        if len(self.history) > 1000:
            self.history = self.history[-1000:]
    
    def get_history(self, limit: int = 20) -> List[Dict]:
        """获取最近的执行历史"""
        return list(reversed(self.history[-limit:]))
    
    def clear_history(self):
        """清除历史记录"""
        self.history.clear()
    
    def cleanup_temp_files(self, pattern: str = "_agent_task_*.py"):
        """清理临时生成的脚本文件"""
        import glob
        files = glob.glob(os.path.join(os.getcwd(), pattern))
        removed = []
        for f in files:
            try:
                os.remove(f)
                removed.append(f)
            except:
                pass
        return removed


# ============================================================
# 第三部分：上下文管理器（记忆系统）
# ============================================================

class ContextManager:
    """
    上下文管理器 - Agent的"记忆系统"
    
    功能：
    - 维护运行环境信息
    - 记录任务执行历史
    - 存储学到的知识
    - 支持持久化保存和加载
    """
    
    def __init__(self, memory_file: str = "agent_memory.json"):
        self.memory_file = memory_file
        self.context = self._build_initial_context()
    
    def _build_initial_context(self) -> Dict:
        """构建初始上下文"""
        import platform
        
        context = {
            "session": {
                "start_time": datetime.now().isoformat(),
                "session_id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
            },
            "environment": {
                "os": platform.system(),
                "os_detail": platform.platform(),
                "python_version": sys.version.split()[0],
                "python_executable": sys.executable,
                "cwd": os.getcwd(),
                "home": os.path.expanduser('~'),
            },
            "config": {
                "dangerous_mode": False,
                "auto_cleanup": True,
            },
            "task_history": [],
            "learned_knowledge": [],
            "variables": {},  # 用户定义的变量
        }
        
        return context
    
    def update_cwd(self):
        """更新当前工作目录"""
        self.context["environment"]["cwd"] = os.getcwd()
    
    def add_task_record(self, task: str, result: Dict, summary: str = None):
        """添加任务执行记录"""
        record = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "success": result.get("success", False),
            "output_length": len(result.get("output", "")) if result.get("output") else 0,
            "duration": result.get("duration", 0),
            "summary": summary,
        }
        self.context["task_history"].append(record)
        
        # 保持最近100条
        if len(self.context["task_history"]) > 100:
            self.context["task_history"] = self.context["task_history"][-100:]
    
    def set_variable(self, key: str, value: Any):
        """设置变量"""
        self.context["variables"][key] = value
    
    def get_variable(self, key: str, default=None):
        """获取变量"""
        return self.context["variables"].get(key, default)
    
    def add_knowledge(self, knowledge: str):
        """添加学到的知识"""
        entry = {
            "time": datetime.now().isoformat(),
            "content": knowledge,
        }
        self.context["learned_knowledge"].append(entry)
        
        # 保持最近50条知识
        if len(self.context["learned_knowledge"]) > 50:
            self.context["learned_knowledge"] = self.context["learned_knowledge"][-50:]
    
    def get_context_string(self, max_length: int = 4000) -> str:
        """
        获取供LLM使用的上下文字符串
        
        自动截断过长的内容以节省token
        """
        ctx = dict(self.context)
        
        # 截断过长的历史
        if len(ctx.get("task_history", [])) > 10:
            ctx["task_history"] = ctx["task_history"][-10:]
        
        # 截断过长的知识
        if len(ctx.get("learned_knowledge", [])) > 10:
            ctx["learned_knowledge"] = ctx["learned_knowledge"][-10:]
        
        text = json.dumps(ctx, indent=2, ensure_ascii=False, default=str)
        
        if len(text) > max_length:
            text = text[:max_length] + "\n... (上下文已截断)"
        
        return text
    
    def save(self, filepath: str = None):
        """保存记忆到文件"""
        path = filepath or self.memory_file
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.context, f, indent=2, ensure_ascii=False, default=str)
    
    def load(self, filepath: str = None) -> bool:
        """从文件加载记忆"""
        path = filepath or self.memory_file
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    
                # 合并加载的内容（保留新的环境信息）
                old_env = self.context.get("environment", {})
                self.context = loaded
                self.context["environment"] = old_env  # 使用最新的环境信息
                
                return True
            except Exception as e:
                print(f"⚠️  加载记忆失败: {e}")
                return False
        return False
    
    def get_stats(self) -> Dict:
        """获取会话统计信息"""
        total_tasks = len(self.context.get("task_history", []))
        success_tasks = sum(1 for t in self.context.get("task_history", []) if t.get("success"))
        
        return {
            "total_tasks": total_tasks,
            "success_tasks": success_tasks,
            "success_rate": f"{(success_tasks/total_tasks*100):.1f}%" if total_tasks > 0 else "N/A",
            "knowledge_count": len(self.context.get("learned_knowledge", [])),
            "session_start": self.context.get("session", {}).get("start_time"),
            "memory_file": self.memory_file,
        }


# ============================================================
# 第四部分：主Agent类 — 组合大脑、手脚、记忆
# ============================================================

class UniversalAgent:
    """
    极简万能Agent - 完整实现
    
    将 LLM大脑 + 执行器手脚 + 记忆系统 组合成一个完整的智能代理
    
    特性：
    ✅ 全流程自动化：从理解任务到执行完成，无需人工干预
    ✅ 智能决策：自动判断应该生成命令还是脚本
    ✅ 自我修复：出错时自动分析原因并修复
    ✅ 安全机制：危险操作拦截与确认
    ✅ 跨平台：Windows / macOS / Linux 通用
    ✅ 记忆持久化：跨会话保留学习成果
    ✅ 交互模式：支持单次任务和持续对话
    
    使用方式：
        # 方式1：单次执行
        agent = UniversalAgent(api_key="your-key")
        agent.run("列出当前目录的所有文件")
        
        # 方式2：交互模式
        agent.chat()
        
        # 方式3：程序化调用
        agent = UniversalAgent(api_key="your-key", base_url="http://localhost:11434/v1")
        result = agent.run_and_get_result("分析这个CSV文件")
        print(result["summary"])
    """
    
    def __init__(self,
                 api_key: str = None,
                 model: str = "gpt-4o",
                 base_url: str = None,
                 dangerous_mode: bool = False,
                 memory_file: str = "universal_agent_memory.json",
                 auto_save: bool = True,
                 backend: str = "llm"):
        """
        初始化Agent
        
        Args:
            api_key: LLM API密钥（bridge模式不需要）
            model: 模型名称
            base_url: API端点（bridge模式不需要）
            dangerous_mode: 是否允许自动执行危险操作
            memory_file: 记忆文件路径
            auto_save: 是否自动保存记忆
            backend: 后端类型
                - "llm": 默认，使用LLMBrain通过HTTP调用外部API（独立运行模式）
                - "bridge": 使用AgentBridge接收外部Agent的输出（Skill/集成模式）
        
        self.backend = backend
        
        # ===== 初始化三大组件 =====
        
        # 🧠 大脑：根据后端类型选择接口
        if backend == "bridge":
            if api_key is None:
                api_key = "bridge"  # 占位符
            self.brain = AgentBridge(
                input_source=os.environ.get('UA_INPUT_SOURCE', 'env'),
                work_dir=os.getcwd()
            )
        else:
            if api_key is None:
                raise ValueError("llm 模式需要提供 api_key")
            self.brain = LLMBrain(
            api_key=api_key,
            model=model,
            base_url=base_url
        )
        
        # 🦶 手脚：命令执行器
        self.hands = UniversalExecutor(
            auto_approve_dangerous=dangerous_mode
        )
        
        # 🧠💾 记忆：上下文管理器
        self.memory = ContextManager(memory_file=memory_file)
        
        # 配置
        self.auto_save = auto_save
        self.dangerous_mode = dangerous_mode
        
        # 统计
        self.total_runs = 0
        self.successful_runs = 0
        
        # 尝试加载已有记忆
        self.memory.load()
        self.memory.update_cwd()
        
        # 打印启动信息
        self._print_banner()
    
    def _print_banner(self):
        """打印启动横幅"""
        
        env_info = self.memory.context.get("environment", {})
        stats = self.memory.get_stats()
        
        banner = f"""
╔══════════════════════════════════════════════════════════╗
║                                                            ║
║   🤖  极简万能 Agent (Minimal Universal Agent)              ║
║                                                            ║
║   ┌──────────────────────────────────────────────┐        ║
║   │                                              │        ║
║   │  🧠 Backend: {self.backend:<29}│        ║
║   │  🦶 Executor: {'Universal Command Executor':<23}│        ║
║   │  💾 Memory: {stats['memory_file']:<29}│        ║
║   │                                              │        ║
║   └──────────────────────────────────────────────┘        ║
║                                                            ║
║   📅  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<24}       ║
║   🖥️  系统: {env_info.get('os_detail', 'Unknown'):<27}     ║
║   🐍  Python: {env_info.get('python_version', '?'):<26}         ║
║   📁  目录: {env_info.get('cwd', '.'):<28}             ║
║   📊  历史: {stats['total_tasks']}个任务 ({stats['success_rate']} 成功率)<{"":>13}       ║
║                                                            ║
╚══════════════════════════════════════════════════════════╝
"""
        print(banner)
    
    def run(self, task: str, max_retries: int = 2) -> str:
        """
        【核心方法】执行单个任务 — Agent 的完整工作流
        
        这是整个脚本最关键的方法。它将"大脑"(brain)、
        "手脚"(hands)、"记忆"(memory) 三个组件串联起来，
        实现从自然语言输入到最终结果输出的全流程自动化。
        
        ┌─────────────────────────────────────────────────────────┐
        │                    run() 四阶段流程                      │
        ├─────────────────────────────────────────────────────────┤
        │                                                         │
        │  [1/4] 🧠 Think（思考）                                  │
        │    brain.think(task, context)                           │
        │    → LLM 理解任务 → 决定生成 command 还是 script         │
        │    → 返回 {"type": "command|script", "content": "..."}   │
        │           ↓                                             │
        │  [2/4] 🔨 Execute（执行）                                 │
        │    hands.execute(content, is_script)                    │
        │    → 先过 _check_danger() 安全检查                       │
        │    → 再调用 _execute_command() 或 _execute_script()      │
        │    → 返回 {"success": bool, "output": str, ...}          │
        │           ↓ (如果失败且重试次数未用尽)                     │
        │  [3/4] 🔧 Fix（修复）— 可选循环                            │
        │    brain.debug_and_fix(error_output, code, task)         │
        │    → LLM 分析错误原因 → 生成修复后的代码                  │
        │    → 重新 execute()                                      │
        │    → 最多循环 max_retries 次                              │
        │           ↓                                             │
        │  [4/4] 🎯 Summarize（总结）                               │
        │    brain.summarize(output, task)                         │
        │    → LLM 将技术输出翻译成人类友好的总结                    │
        │    → 返回给用户                                          │
        │                                                         │
        └─────────────────────────────────────────────────────────┘
        
        Args:
            task: 用户的自然语言任务描述（如"列出当前目录的文件"）
            max_retries: 最大重试次数（默认2次），仅对执行失败时生效
            
        Returns:
            任务执行的人类友好总结文本（由 LLM 生成）
        """
        
        self.total_runs += 1
        run_start = time.time()
        
        print(f"\n{'━' * 70}")
        print(f"📋  任务 #{self.total_runs}: {task}")
        print(f"{'━' * 70}")
        
        # ========== 第一步：LLM思考 ==========
        print(f"\n  🧠  [1/4] 思考中...")
        decision = self.brain.think(task, self.memory.get_context_string())
        
        exec_type = decision.get('type', 'command')
        content = decision.get('content', '')
        explanation = decision.get('explanation', '')
        
        print(f"  💡  决策: 生成 [{exec_type}] 类型")
        if explanation:
            print(f"  📝  理由: {explanation}")
        print(f"  📏  规模: {len(content)} 字符")
        
        # ========== 第二步：执行 ==========
        is_script = (exec_type == 'script')
        
        print(f"\n  🔨  [2/4] 执行中...")
        result = self.hands.execute(content, is_script=is_script)
        
        # ========== 第三步：错误处理与自我修复 ==========
        retry_count = 0
        while (not result.get("success") and 
               retry_count < max_retries and
               result.get("output")):
            
            retry_count += 1
            print(f"\n  🔧  [3/4] 第{retry_count}次尝试修复...")
            
            fixed_code = self.brain.debug_and_fix(
                error_output=result.get("output", ""),
                original_code=content,
                task=task
            )
            
            result = self.hands.execute(fixed_code, is_script=is_script)
        
        # 更新统计
        if result.get("success"):
            self.successful_runs += 1
        
        # ========== 第四步：LLM总结 ==========
        print(f"\n  🎯  [4/4] 生成总结...")
        summary = self.brain.summarize(
            execution_result=result.get("output", ""),
            original_task=task
        )
        
        # ========== 记录和保存 ==========
        duration = time.time() - run_start
        self.memory.add_task_record(task, result, summary)
        self.memory.update_cwd()
        
        if self.auto_save:
            self.memory.save()
        
        # ========== 展示最终结果 ==========
        print(f"\n{'━' * 70}")
        print(f"✅  任务完成！耗时: {duration:.1f}秒")
        print(f"{'━' * 70}")
        print(f"\n{summary}\n")
        
        return summary
    
    def run_and_get_result(self, task: str) -> Dict:
        """
        执行任务并返回完整的结果字典
        
        适用于程序化调用，可以获取原始输出等信息
        
        Returns:
            {
                "summary": str,          # 人类友好的总结
                "raw_output": str,       # 原始执行输出
                "success": bool,         # 是否成功
                "duration": float,       # 耗时
                "generated_code": str,   # 生成的代码/命令
            }
        """
        summary = self.run(task)
        
        return {
            "summary": summary,
            "raw_output": self.hands.history[-1]["output_preview"] if self.hands.history else "",
            "success": self.hands.history[-1]["success"] if self.hands.history else False,
            "generated_code": "",  # 可扩展记录
        }
    
    def chat(self, welcome_message: str = None):
        """
        进入交互式对话模式
        
        支持的特殊命令：
        - exit/quit/q: 退出
        - history: 查看执行历史
        - context: 显示当前上下文
        - stats: 显示统计信息
        - clear: 清除临时文件
        - help: 显示帮助
        """
        
        print(f"\n{'━' * 70}")
        print(f"💬  交互模式已启动")
        print(f"   输入任务描述，我将自动完成")
        print(f"   输入 'help' 查看可用命令")
        print(f"   输入 'exit' 退出")
        print(f"{'━' * 70}\n")
        
        if welcome_message:
            print(f"🤖  {welcome_message}\n")
        
        while True:
            try:
                user_input = input("👤  你: ").strip()
                
                # 空输入跳过
                if not user_input:
                    continue
                
                # 内置命令处理
                lower_input = user_input.lower()
                
                if lower_input in ['exit', 'quit', 'q', 'bye']:
                    self._print_goodbye()
                    break
                
                elif lower_input == 'help':
                    self._print_help()
                    continue
                
                elif lower_input == 'history':
                    self._show_history()
                    continue
                
                elif lower_input == 'context':
                    print(f"\n{self.memory.get_context_string(max_length=2000)}\n")
                    continue
                
                elif lower_input == 'stats':
                    self._show_stats()
                    continue
                
                elif lower_input == 'clear':
                    removed = self.hands.cleanup_temp_files()
                    print(f"\n🧹  已清理 {len(removed)} 个临时文件\n")
                    continue
                
                elif lower_input.startswith('var '):
                    # 设置变量
                    parts = user_input.split(' ', 2)
                    if len(parts) >= 3:
                        self.memory.set_variable(parts[1], parts[2])
                        print(f"\n✅  变量 {parts[1]} 已设置\n")
                    continue
                
                elif lower_input.startswith('remember '):
                    # 记录知识
                    knowledge = user_input[9:].strip()
                    self.memory.add_knowledge(knowledge)
                    print(f"\n📝  已记住: {knowledge}\n")
                    continue
                
                # 正常任务执行
                self.run(user_input)
                
            except KeyboardInterrupt:
                print(f"\n\n👋  再见！")
                break
            except EOFError:
                break
            except Exception as e:
                print(f"\n❌  发生错误: {e}\n")
                if self.dangerous_mode:
                    import traceback
                    traceback.print_exc()
    
    def batch_run(self, tasks: List[str]) -> List[str]:
        """
        批量执行多个任务
        
        Args:
            tasks: 任务列表
            
        Returns:
            总结列表
        """
        results = []
        for i, task in enumerate(tasks, 1):
            print(f"\n{'█' * 70}")
            print(f"批量任务 {i}/{len(tasks)}")
            print(f"{'█' * 70}")
            
            summary = self.run(task)
            results.append(summary)
        
        # 打印批量执行摘要
        print(f"\n{'═' * 70}")
        print(f"📊  批量执行完成: {len(tasks)} 个任务, "
              f"成功 {self.successful_runs}/{self.total_runs}")
        print(f"{'═' * 70}")
        
        return results
    
    # ==================== 辅助方法 ====================
    
    def _print_help(self):
        """显示帮助信息"""
        help_text = """
┌──────────────────────────────────────────────────────────┐
│                     📖  可用命令                           │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  正常用法：                                               │
│    直接输入你的任务描述（自然语言即可）                      │
│                                                          │
│  示例：                                                   │
│    "列出当前目录的文件"                                    │
│    "帮我写一个快速排序算法"                                 │
│    "把这个CSV文件转换成Excel"                              │
│    "分析一下sales.csv的销售趋势"                           │
│                                                          │
│  特殊命令：                                               │
│    help      - 显示此帮助信息                              │
│    history   - 查看执行历史                                │
│    context   - 查看当前上下文                              │
│    stats     - 查看统计信息                                │
│    clear     - 清理临时生成的脚本文件                       │
│    var X Y   - 设置变量 X 的值为 Y                         │
│    remember X - 让Agent记住一条信息                        │
│    exit      - 退出交互模式                                │
│                                                          │
└──────────────────────────────────────────────────────────┘
"""
        print(help_text)
    
    def _show_history(self):
        """显示执行历史"""
        history = self.hands.get_history(15)
        
        if not history:
            print("\n📭  暂无执行历史\n")
            return
        
        print(f"\n{'─' * 80}")
        print(f"📜  最近 {len(history)} 条执行记录")
        print(f"{'─' * 80}")
        
        for i, item in enumerate(history, 1):
            icon = "✅" if item['success'] else "❌"
            time_short = item['timestamp'].split('T')[1][:8]
            print(f"  {i:2}. {icon} [{time_short}] {item['duration']}s")
            print(f"     └─ {item['command'][:65]}")
        
        print(f"{'─' * 80}\n")
    
    def _show_stats(self):
        """显示统计信息"""
        stats = self.memory.get_stats()
        executor_history = self.hands.get_history(len(self.hands.history))
        
        print(f"\n{'═' * 50}")
        print(f"📊  Agent 统计信息")
        print(f"{'═' * 50}")
        print(f"""
  会话信息:
    ├─ 开始时间: {stats['session_start']}
    ├─ 总任务数: {stats['total_tasks']}
    ├─ 成功数量: {stats['success_tasks']}
    └─ 成功率:   {stats['success_rate']}
  
  本次运行:
    ├─ 执行次数: {self.total_runs}
    ├─ 成功次数: {self.successful_runs}
    └─ 记忆文件: {stats['memory_file']}
""")
        print(f"{'═' * 50}\n")
    
    def _print_goodbye(self):
        """打印告别信息"""
        
        final_stats = self.memory.get_stats()
        
        goodbye = f"""
{'═' * 60}
  👋  会话结束
{'═' * 60}
  📊  本次会话统计:
     • 执行任务: {self.total_runs} 次
     • 成功完成: {self.successful_runs} 次
     • 成功率:   {(self.successful_runs/self.total_runs*100):.1f}% (本次)
     
  💾  记忆已保存到: {final_stats['memory_file']}
     下次启动时会自动加载
  
  感谢使用极简万能 Agent！
{'═' * 60}
"""
        print(goodbye)


# ============================================================
# 第五部分：预设配置（快速开始模板）
# ============================================================

PRESETS = {
    # OpenAI
    "openai_gpt4o": {
        "api_key": "sk-your-openai-key-here",
        "model": "gpt-4o",
        "base_url": "https://api.openai.com/v1",
        "description": "OpenAI GPT-4o (最强综合能力)"
    },
    
    "openai_gpt4o_mini": {
        "api_key": "sk-your-openai-key-here",
        "model": "gpt-4o-mini",
        "base_url": "https://api.openai.com/v1",
        "description": "OpenAI GPT-4o-mini (性价比高)"
    },
    
    # DeepSeek
    "deepseek_chat": {
        "api_key": "sk-your-deepseek-key-here",
        "model": "deepseek-chat",
        "base_url": "https://api.deepseek.com",
        "description": "DeepSeek Chat (国产优秀模型)"
    },
    
    "deepseek_reasoner": {
        "api_key": "sk-your-deepseek-key-here",
        "model": "deepseek-reasoner",
        "base_url": "https://api.deepseek.com",
        "description": "DeepSeek Reasoner (深度推理)"
    },
    
    # 阿里云通义千问
    "qwen_max": {
        "api_key": "sk-your-dashscope-key-here",
        "model": "qwen-max",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "description": "通义千问 Max (阿里云)"
    },
    
    "qwen_turbo": {
        "api_key": "sk-your-dashscope-key-here",
        "model": "qwen-turbo",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "description": "通义千问 Turbo (速度快)"
    },
    
    # 智谱AI GLM
    "glm4": {
        "api_key": "sk-your-zhipu-key-here",
        "model": "glm-4-plus",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "description": "智谱GLM-4 Plus"
    },
    
    # 本地 Ollama
    "ollama_llama3": {
        "api_key": "ollama",
        "model": "llama3",
        "base_url": "http://localhost:11434/v1",
        "description": "本地 Ollama + Llama3 (免费无限用)"
    },
    
    "ollama_qwen2": {
        "api_key": "ollama",
        "model": "qwen2",
        "base_url": "http://localhost:11434/v1",
        "description": "本地 Ollama + Qwen2 (免费无限用)"
    },
}


# ============================================================
# 第六部分：启动入口
# ============================================================

def main():
    """主函数 - 启动Agent"""
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🤖  极简万能 Agent v1.0.0                                   ║
║                                                               ║
║   Minimal Universal Agent                                      ║
║   LLM (大脑) + Command Executor (手脚) = 万能                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
""")
    
    # ===== 配置方式选择 =====
    
    config_method = input("请选择配置方式:\n"
                          "  1. 手动输入 API Key 和 URL\n"
                          "  2. 使用预设配置 (OpenAI/DeepSeek/Qwen/Ollama)\n"
                          "  3. 从配置文件读取 (config.json)\n"
                          "  4. 使用环境变量\n"
                          "\n"
                          "选择 [1/2/3/4]: ").strip()
    
    api_key = ""
    model = "gpt-4o"
    base_url = None
    
    if config_method == '1':
        # 手动输入
        api_key = input("请输入 API Key: ").strip()
        model = input("模型名称 [默认 gpt-4o]: ").strip() or "gpt-4o"
        base_url_input = input("API URL [默认 https://api.openai.com/v1]: ").strip()
        base_url = base_url_input if base_url_input else None
        
    elif config_method == '2':
        # 预设配置
        print("\n可用的预设配置:")
        presets_list = list(PRESETS.keys())
        for i, name in enumerate(presets_list, 1):
            preset = PRESETS[name]
            print(f"  {i:2}. {name:<25} - {preset['description']}")
        
        choice = input(f"\n选择预设 [1-{len(presets_list)}]: ").strip()
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(presets_list):
                selected = PRESETS[presets_list[idx]]
                api_key = selected['api_key']
                model = selected['model']
                base_url = selected['base_url']
                print(f"\n已选择: {presets_list[idx]}")
            else:
                print("无效选择，使用默认配置")
                return
        except ValueError:
            print("无效输入")
            return
    
    elif config_method == '3':
        # 从文件读取
        config_file = input("配置文件路径 [默认 config.json]: ").strip() or os.path.join(SCRIPT_DIR, "config.json")
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            api_key = config.get('api_key', '')
            model = config.get('model', 'gpt-4o')
            base_url = config.get('base_url')
            print(f"\n已从 {config_file} 加载配置")
        except FileNotFoundError:
            print(f"配置文件 {config_file} 不存在")
            return
        except Exception as e:
            print(f"读取配置失败: {e}")
            return
    
    elif config_method == '4':
        # 环境变量
        api_key = os.environ.get('LLM_API_KEY', '')
        model = os.environ.get('LLM_MODEL', 'gpt-4o')
        base_url = os.environ.get('LLM_BASE_URL')
        
        if not api_key:
            print("❌ 未找到环境变量 LLM_API_KEY")
            return
        
        print(f"\n已从环境变量加载配置:")
        print(f"  Model: {model}")
        if base_url:
            print(f"  URL: {base_url}")
    
    else:
        print("无效选择")
        return
    
    # ===== 验证API Key =====
    
    if not api_key or api_key.endswith('-here'):
        print(f"\n⚠️  请先设置有效的 API Key！")
        print("  当前值:", api_key if len(api_key) < 20 else api_key[:10] + "...")
        confirm = input("\n是否继续测试？(y/n): ").strip().lower()
        if confirm != 'y':
            return
    
    # ===== 选择运行模式 =====
    
    mode = input("\n请选择运行模式:\n"
                 "  1. 交互模式 (推荐)\n"
                 "  2. 单次任务模式\n"
                 "  3. 危险模式 (跳过安全确认)\n"
                 "\n"
                 "选择 [1/2/3]: ").strip()
    
    dangerous_mode = (mode == '3')
    
    # ===== 创建并启动 Agent =====
    
    agent = UniversalAgent(
        api_key=api_key,
        model=model,
        base_url=base_url,
        dangerous_mode=dangerous_mode
    )
    
    if mode == '2':
        # 单次任务模式
        task = input("\n请输入任务: ").strip()
        if task:
            agent.run(task)
    
    else:
        # 交互模式（默认）
        welcome = (
            "你好！我是极简万能 Agent。\n"
            "你可以用自然语言告诉我你想做什么，我会自动完成。\n"
            "例如：'列出当前目录的文件'、'帮我写一个排序算法'"
        )
        agent.chat(welcome_message=welcome)


def create_config_template():
    """创建示例配置文件"""
    template = {
        "_comment": "这是极简万能 Agent 的配置文件模板",
        "api_key": "your-api-key-here",
        "model": "gpt-4o",
        "base_url": "https://api.openai.com/v1",
        "dangerous_mode": False,
        "auto_save_memory": True,
        "memory_file": "universal_agent_memory.json",
        "command_timeout": 300,
        "script_timeout": 600,
    }
    
    with open(os.path.join(SCRIPT_DIR, 'config.json'), 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=4, ensure_ascii=False)
    
    print("✅ 已创建配置文件模板: config.json")
    print("   请编辑填入你的 API Key")


def parse_args():
    """解析命令行参数"""
    args = {
        'backend': 'llm',       # llm 或 bridge
        'task': None,
        'dangerous': False,
        'create_config': False,
        'help': False,
        'version': False,
        'bridge_info': False,   # 输出 Bridge 协议信息
    }
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i].lower()
        
        if arg in ['--help', '-h', 'help']:
            args['help'] = True
        elif arg == '--create-config':
            args['create_config'] = True
        elif arg in ['--version', '-v']:
            args['version'] = True
        elif arg == '--backend':
            if i + 1 < len(sys.argv):
                i += 1
                args['backend'] = sys.argv[i].lower()
            else:
                print("错误: --backend 需要指定参数 (llm / bridge)")
                sys.exit(1)
        elif arg == '--run':
            if i + 1 < len(sys.argv):
                i += 1
                args['task'] = ' '.join(sys.argv[i:])  # 剩余所有参数作为任务
                break  # 后面都是任务内容了
            else:
                print("用法: python universal_agent.py --run \"你的任务\"")
                sys.exit(1)
        elif arg == '--dangerous':
            args['dangerous'] = True
        elif arg == '--bridge-info':
            args['bridge_info'] = True
        
        i += 1
    
    return args


def print_bridge_protocol():
    """输出 Bridge 协议说明（供外部 Agent 参考）"""
    protocol = """
╔═══════════════════════════════════════════════════════════════╗
║          🌉 Agent Bridge Protocol v1.0.0                     ║
║                                                               ║
║  任何有 LLM + 命令执行能力的 Agent 都可通过此协议驱动脚本      ║
╚═══════════════════════════════════════════════════════════════╝

📌 启动方式:
   python universal_agent.py --backend bridge --run "任务描述"

📡 通信机制（环境变量）:

   脚本需要外部 Agent 提供以下输入，通过环境变量传递：

   ┌─────────────────┬───────────────────┬────────────────────┐
   │ 环境变量名       │ 用途               │ 格式               │
   ├─────────────────┼───────────────────┼────────────────────┤
   │ UA_THINK         │ 任务决策结果       │ JSON:              │
   │                  │ (type+content)     │ {"type":"command",│
   │                  │                    │  "content":"ls",  │
   │                  │                    │  "explanation":""}│
   ├─────────────────┼───────────────────┼────────────────────┤
   │ UA_GENERATE_     │ 生成的Python脚本   │ 完整代码文本       │
   │ SCRIPT           │                   │                    │
   ├─────────────────┼───────────────────┼────────────────────┤
   │ UA_SUMMARIZE     │ 执行结果的总结     │ 自然语言总结文本   │
   ├─────────────────┼───────────────────┼────────────────────┤
   │ UA_DEBUG_AND_FIX │ 修复后的代码      │ 修复后的完整代码   │
   └─────────────────┴───────────────────┴────────────────────┘

🔄 执行流程:

   外部Agent                          脚本(universal_agent.py)
   ──────────                         ─────────────────────
   1. 接收用户任务 "列出文件"
         │
         ▼
   2. LLM决策 → set UA_THINK={"type":"command","content":"dir"}
         │                              │
         ▼                              ▼
   3. execute_command(                 ← 读取UA_THINK
      python ... --backend             ──► 决定执行类型
      bridge --run "...")                   
         │                              
         ▼                             
   4. 接收执行输出                      
         │                              
         ▼                             
   5. LLM总结 → set UA_SUMMARIZE="..."  │
         │                              ▼
         └────────────────────────────  ← 读取UA_SUMMARIZE
                                         返回最终结果给Agent

🛡️ 安全机制（Bridge模式同样生效）:

   ✅ 高危命令自动检测 (rm -rf, format, etc.)
   ✅ 中危命令警告提示
   ✅ 自动重试修复（最多2次）
   ✅ 记忆持久化

💡 使用示例（伪代码）:

   # 外部Agent的执行逻辑：
   
   task = "分析sales.csv"
   
   # Step 1: Agent用LLM生成决策
   decision = agent.llm.decide(task)  
   # → {"type": "script", "content": "import pandas..."}
   
   # Step 2: 设置环境变量并执行脚本
   env.UA_THINK = json.dumps(decision)
   result = shell("python universal_agent.py --backend bridge --run \"" + task + "\"")
   # 如果出错，会请求 UA_DEBUG_AND_FIX
   
   # Step 3: Agent用LLM总结
   summary = agent.llm.summarize(result.output, task)
   env.UA_SUMMARIZE = summary
   # （或通过程序化调用 bridge.set_response()）
   
   # Step 4: 返回给用户
   print(summary)

⚙️ 高级选项:

   --backend bridge          启用Bridge模式
   --dangerous              跳过安全确认（不推荐）
   UA_INPUT_SOURCE=file     改用临时文件通信（替代环境变量）

"""
    print(protocol)


# ============================================================
# 启动入口 — 命令行参数分发器
# ============================================================
# 本段代码是脚本的"总开关"，根据命令行参数将执行流分发到不同模式：
#
#   python universal_agent.py                     → main() → 交互式引导
#   python universal_agent.py --run "任务"        → LLM模式单次任务
#   python universal_agent.py --backend bridge    → Bridge模式
#   python universal_agent.py -h / --version      → 帮助/版本信息
#   python universal_agent.py --bridge-info       → 打印Bridge协议文档
#   python universal_agent.py --create-config     → 生成config.json模板
#
# 【设计思路】
#   不使用 argparse 等第三方库，手写 parse_args() 保持零依赖。
#   parse_args() 返回一个字典，__main__ 段用 if/elif 链进行分发。
# ============================================================

if __name__ == "__main__":
    
    args = parse_args()
    
    # ===== 帮助/版本/协议信息 =====
    if args['help']:
        main()
    elif args['version']:
        print("极简万能 Agent v1.0.0")
        print("Minimal Universal Agent")
        print("LLM + Command Executor = Universal AI Agent")
        print("\n支持三种运行模式：独立模式(llm) | 桥接模式(bridge) | Skill模拟(无需运行)")
    elif args['bridge_info']:
        print_bridge_protocol()
    elif args['create_config']:
        create_config_template()
    
    # ===== Bridge 模式的 --run =====
    elif args['backend'] == 'bridge' and args['task']:
        task = args['task']
        
        print(f"\n{'='*60}")
        print(f"🌉  Bridge Mode — 等待外部 Agent 驱动")
        print(f"{'='*60}")
        print(f"📋  Task: {task}")
        print(f"🧠  Backend: bridge (external Agent)")
        print(f"{'='*60}\n")
        
        try:
            agent = UniversalAgent(
                api_key="bridge",
                backend="bridge",
                dangerous_mode=args['dangerous']
            )
            
            # Bridge模式下 run() 内部会从环境变量读取各阶段输入
            result = agent.run(task)
            
            # 输出结构化结果供 Agent 解析
            output_json = {
                "status": "success",
                "summary": result,
                "backend": "bridge"
            }
            print(f"\n\n--- BRIDGE_OUTPUT ---")
            print(json.dumps(output_json, ensure_ascii=False, indent=2))
            print(f"--- END_BRIDGE_OUTPUT ---\n")
            
        except BridgeInputError as e:
            error_json = {
                "status": "error",
                "error_type": "BRIDGE_INPUT_MISSING",
                "message": str(e),
                "hint": "请确保外部 Agent 通过环境变量提供了所需的输入"
            }
            print(f"\n\n--- BRIDGE_OUTPUT ---")
            print(json.dumps(error_json, ensure_ascii=False, indent=2))
            print(f"--- END_BRIDGE_OUTPUT ---\n")
            sys.exit(2)
        except Exception as e:
            error_json = {
                "status": "error",
                "error_type": "EXECUTION_ERROR",
                "message": str(e)
            }
            print(f"\n\n--- BRIDGE_OUTPUT ---")
            print(json.dumps(error_json, ensure_ascii=False, indent=2))
            print(f"--- END_BRIDGE_OUTPUT ---\n")
            sys.exit(1)
    
    # ===== 标准 LLM 模式的 --run =====
    elif args['run']:
        task = args['task']
        
        api_key = os.environ.get('LLM_API_KEY', '')
        model = os.environ.get('LLM_MODEL', 'gpt-4o')
        base_url = os.environ.get('LLM_BASE_URL')
        
        if not api_key:
            print("❌ 请设置环境变量 LLM_API_KEY")
            sys.exit(1)
        
        agent = UniversalAgent(api_key, model, base_url, dangerous_mode=args['dangerous'])
        agent.run(task)
    
    else:
        # 默认：交互式启动
        main()


# ============================================================
# 文件结束
# ============================================================
#
# 📝 使用指南
#
# 三种运行模式：
#
# 模式1 - 独立运行（需API Key）:
#   python universal_agent.py
#   python universal_agent.py --run "任务描述"
#
# 模式2 - Bridge集成（需外部Agent提供LLM能力）:
#   python universal_agent.py --backend bridge --run "任务描述"
#   python universal_agent.py --bridge-info    # 查看完整协议说明
#
# 模式3 - Skill模拟（不需要运行此脚本）:
#   由加载Skill的Agent直接按照架构思路工作
#
# ============================================================
