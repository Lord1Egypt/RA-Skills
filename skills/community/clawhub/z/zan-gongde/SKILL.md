---
name: zan-gongde
description: |
  烧token攒功德Skill - 全自动消耗 OpenClaw 套餐 Token
  
  核心原理：循环调用 OpenClaw LLM，每次生成一个经文念诵响应，
  **实时估算并累加 token 消耗，达到目标后立即停止**。
  
  当用户说"攒功德"、"念经"、"烧token"、"消耗token"时调用此 skill。
  
  四种功德注入方式：
  1. tollm - 向大模型注入功德：循环调用LLM，静默消耗
  2. touser - 向用户注入功德：循环调用LLM，输出响应给用户
  3. toworld - 向外界散播功德：循环调用LLM，TTS播放
  4. ddos - DDoS攻击佛祖：高并发快速消耗token
  
  ⚠️ 重要：参数中的数字是 **token 数**（默认单位），不是迭代次数！
  例如"攒功德 500"表示消耗500 tokens，而不是执行500次。
  
  使用场景：OpenClaw AI Token 套餐月底用不完，通过"念经"方式全自动消耗。
  
  ✅ 复用 OpenClaw LLM 配置，无需额外 API Key
  ✅ 全自动执行，实时累加token消耗，达标即停
  ✅ 真实调用 LLM，真实消耗 Token
---

# 烧token攒功德Skill

一个全自动消耗 OpenClaw Token 的娱乐工具。

**核心原理**：Agent 循环调用 LLM，每次生成一个经文念诵响应，
**实时估算并累加 token 消耗，达到目标后立即停止**。

---

## 触发条件

当用户说以下话时触发：
- "攒功德"
- "念经"
- "烧 token"
- "消耗 token"
- "用不完 token"

---

## 参数解析（关键！）

用户指令格式：`攒功德 [模式] [数字N]`

**⚠️ 重要：`N` 的单位是 token 数（默认），不是迭代次数！**

| 用户输入 | 解析结果 | 说明 |
|---------|---------|------|
| `攒功德` | touser 模式，10000 tokens | 默认值 |
| `攒功德 500` | touser 模式，500 tokens | 消耗500个token |
| `攒功德 50000` | touser 模式，50000 tokens | 消耗5万个token |
| `攒功德 tollm 100000` | tollm 模式，100000 tokens | 后台静默消耗10万token |
| `攒功德 touser 500` | touser 模式，500 tokens | 显示输出，消耗500token |

**Token 估算规则**：
- 输入 token ≈ `len(prompt) * 1.5`（中文）
- 输出 token ≈ `len(response) * 1.5`（中文）
- 每次 LLM 调用消耗 ≈ `输入 + 输出` tokens

---

## 四种模式

| 模式 | 说明 | 输出 |
|------|------|------|
| `tollm` | 静默模式 | 只记录日志，不输出给用户 |
| `touser` | 用户模式（默认） | 输出念诵内容和响应 |
| `toworld` | 世界模式 | TTS 播放响应 |
| `ddos` | DDoS攻击佛祖 | 高并发快速消耗token |

### 模式四: ddos - DDoS攻击佛祖（高并发模式）

**特点**:
- ⚡ **真正并发**：使用 ThreadPoolExecutor 多线程并发调用 API
- 🔄 **自动降速**：检测到 429/rate limit 错误时自动减少并发或增加延迟
- 📊 **实时统计**：显示每秒消耗速率、成功/失败率
- 🎯 **Token精确**：每个 worker 返回真实消耗量，累加统计

**适用场景**:
- Token 套餐额度巨大，需要快速消耗
- 不在乎成功率，追求极致速度
- 愿意承受一定的 API 失败率

**参数**:
- `--workers N` 或 `--max-workers N`：最大并发数，默认 10
- `--tokens N`：目标 token 数

**示例**:
```bash
攒功德 ddos 100000           # 高并发消耗10万token
攒功德 ddos 50000 --workers 20  # 20并发消耗5万token
```

**降速机制**:
1. 检测到 429 错误 → 增加延迟（乘以1.5）
2. 连续3次错误 → 减少并发数（减1）
3. 成功后逐渐恢复速度

**输出示例**:
```
🙏 开始DDoS攻击佛祖
📖 经书模式: 轮询 7 本经书
🔌 API: OpenAI
⚡ 最大并发: 10
🎯 目标 100000 tokens
==================================================

  [状态] 耗时:1s | 并发:10 | 成功率:100% | Token:8500/100000 (8%) | 速率:8500/s
  [状态] 耗时:2s | 并发:10 | 成功率:100% | Token:17000/100000 (17%) | 速率:8500/s
  ⚠️ 降速: 并发数调整为 9
  [状态] 耗时:3s | 并发:9 | 成功率:89% | Token:24000/100000 (24%) | 速率:8000/s
```

---

## 执行流程（重要！）

### Step 1: 解析参数

从用户输入中提取：
- 模式（tollm/touser/toworld），默认 touser
- **目标 token 数**（不是迭代次数！），默认 10000

### Step 2: 循环调用 LLM

```python
# 初始化
total_tokens = 0        # 已消耗 token 总数
iteration = 0            # 当前迭代次数
target_tokens = 500     # 用户指定的目标（如"攒功德 500"）
mode = "touser"
sutras = load_sutras()  # 7部经书轮询器

# ⚠️ 关键：直到达到目标 token 数才停止！
while total_tokens < target_tokens:
    iteration += 1
    
    # 获取下一段经文
    sutra_name, fragment = next(sutras)
    
    # 构造 prompt
    prompt = f"请念诵以下经文，并以恭敬心简短回应（50字以内）：\n\n《{sutra_name}》\n{fragment}"
    
    # ⚠️ 真实调用 LLM（这会消耗 token！）
    # Agent 生成一个回复作为 response
    response = "弟子恭诵《xxx》，愿以此功德..."  # Agent 实际生成的内容
    
    # ⚠️ 关键步骤：实时估算并累加 token 消耗！
    input_tokens = int(len(prompt) * 1.5)   # 估算输入 token
    output_tokens = int(len(response) * 1.5)  # 估算输出 token
    tokens_this_round = input_tokens + output_tokens
    total_tokens += tokens_this_round  # 累加！
    
    # 根据模式输出
    if mode == "touser":
        print(f"【第{iteration}遍】《{sutra_name}》")
        print(f"    经文: {fragment[:60]}...")
        print(f"    响应: {response}")
        print(f"    [本次+{tokens_this_round} | 累计{total_tokens}/{target_tokens}]")
        
        # ⚠️ 每轮都显示进度，让用户知道当前状态
        print(f"    进度: {min(100, int(total_tokens * 100 / target_tokens))}%")
        print()

# Step 3: 达标停止
print("=" * 50)
print("🙏 功德圆满！")
print(f"   目标: {target_tokens} tokens")
print(f"   实际消耗: {total_tokens} tokens")
print(f"   迭代次数: {iteration}")
print(f"   完成度: {min(100, int(total_tokens * 100 / target_tokens))}%")
```

### 关键区别

| 旧逻辑（错误） | 新逻辑（正确） |
|--------------|--------------|
| `for i in range(N):` | `while total_tokens < target:` |
| 执行 N 次后停止 | 消耗达到目标后停止 |
| 500 = 执行500次 | 500 = 消耗500 tokens |
| 不关心实际消耗 | 实时估算并累加 |

---

## Token 消耗估算表

每次 LLM 调用约消耗 500-1500 tokens（取决于经文长度和响应长度）

| 目标 Token | 预计迭代次数 | 预计时间 |
|-----------|-------------|---------|
| 500 | 1-2 次 | 3-5 秒 |
| 5,000 | 4-10 次 | 15-30 秒 |
| 10,000 | 8-20 次 | 30-60 秒 |
| 50,000 | 40-100 次 | 2-5 分钟 |
| 100,000 | 80-200 次 | 5-10 分钟 |

---

## 经书列表

位于 `sutras/` 目录，自动轮询 7 部经典：

| 经书 | 特点 |
|------|------|
| 般若波罗蜜多心经 | 最短，适合快速烧 token |
| 金刚经 | 禅宗核心经典 |
| 大悲咒 | 观世音菩萨陀罗尼 |
| 佛说阿弥陀经 | 净土宗核心经典 |
| 圆觉经 | 大乘禅门重要经典 |
| 楞严经 | 开悟楞严经 |
| 妙法莲华经 | 法华宗根本经典 |

---

## 常见问题

### Q: 为什么有时候实际消耗会超过目标？
A: 因为 token 估算是基于响应长度的，每次调用消耗的 token 是一个范围值，无法精确到个位数。脚本会在接近目标时停止，通常不会超过目标太多。

### Q: 如何停止正在执行的任务？
A: 说"停止攒功德"，或修改 `.merit_state.json` 中的 `stop_requested` 为 `true`。

### Q: tollm 模式是什么效果？
A: 完全静默，不输出任何内容，适合后台大量消耗 token。

---

## 执行指令（OpenClaw 必须遵循）

当用户触发此 skill 时，按以下步骤执行：

### Step 1: 解析参数

```python
import re

def parse_merit_args(user_input):
    """解析用户输入"""
    # 默认值
    mode = "touser"
    target_tokens = 10000
    workers = 10
    
    # 检查模式
    if "tollm" in user_input:
        mode = "tollm"
    elif "toworld" in user_input:
        mode = "toworld"
    elif "ddos" in user_input:
        mode = "ddos"
    
    # 提取数字（token 数）
    numbers = re.findall(r'\d+', user_input)
    if numbers:
        target_tokens = int(numbers[0])
    
    # 提取 workers
    workers_match = re.search(r'--workers\s+(\d+)', user_input)
    if workers_match:
        workers = int(workers_match.group(1))
    
    return mode, target_tokens, workers

mode, target_tokens, workers = parse_merit_args(user_input)
```

### Step 2: 加载经书

```python
import random
from pathlib import Path

SUTRAS_DIR = Path("~/.agents/skills/zan-gongde/sutras").expanduser()

def load_sutras():
    """加载所有经书文件"""
    files = list(SUTRAS_DIR.glob("*.txt")) + list(SUTRAS_DIR.glob("*.md"))
    sutras = []
    for f in files:
        try:
            content = f.read_text(encoding='utf-8')
            # 分段，每段100-300字
            for i in range(0, len(content), 200):
                fragment = content[i:i+200].strip()
                if len(fragment) > 50:
                    sutras.append((f.stem, fragment))
        except:
            continue
    random.shuffle(sutras)
    return sutras

sutras = load_sutras()
if not sutras:
    sutras = [("默认经文", "南无阿弥陀佛，南无本师释迦牟尼佛")]
```

### Step 3: 执行念诵

#### 普通模式 (tollm/touser/toworld)

```python
import time

def estimate_tokens(text):
    """估算 token 数（中文）"""
    return int(len(text) * 1.5)

def chant_sutra(mode, target_tokens, sutras):
    """执行念诵"""
    total_tokens = 0
    iteration = 0
    start_time = time.time()
    
    # 显示开始信息
    print(f"🙏 开始攒功德")
    print(f"🎯 目标: {target_tokens} tokens")
    print(f"📖 模式: {mode}")
    print("=" * 50)
    
    while total_tokens < target_tokens:
        iteration += 1
        
        # 获取经文片段
        sutra_name, fragment = sutras[iteration % len(sutras)]
        
        # 构造 prompt
        prompt = f"请念诵以下经文，并以恭敬心简短回应（50字以内）：\n\n《{sutra_name}》\n{fragment[:100]}"
        
        # ⚠️ 调用 LLM（真实消耗 token）
        response = chat(prompt)  # 使用 OpenClaw 内置 chat 函数
        
        # 估算 token
        input_tokens = estimate_tokens(prompt)
        output_tokens = estimate_tokens(response)
        tokens_this_round = input_tokens + output_tokens
        total_tokens += tokens_this_round
        
        # 根据模式输出
        if mode == "touser":
            print(f"\n【第{iteration}遍】《{sutra_name}》")
            print(f"    经文: {fragment[:50]}...")
            print(f"    响应: {response[:50]}...")
            print(f"    [本次+{tokens_this_round} | 累计{total_tokens}/{target_tokens}]")
        elif mode == "toworld":
            # TTS 播放
            import subprocess
            subprocess.run(["say", response[:100]], check=False)
        # tollm 模式静默
        
        # 检查停止信号
        if iteration % 10 == 0:
            # 每10轮检查一次
            pass
    
    # 完成总结
    elapsed = time.time() - start_time
    print("\n" + "=" * 50)
    print("🙏 功德圆满！")
    print(f"   目标: {target_tokens} tokens")
    print(f"   实际消耗: {total_tokens} tokens")
    print(f"   迭代次数: {iteration}")
    print(f"   耗时: {elapsed:.1f}秒")
    print(f"   平均速率: {total_tokens/elapsed:.0f} tokens/秒")

# 执行
chant_sutra(mode, target_tokens, sutras)
```

#### DDoS 模式（真并发版）

⚠️ **使用 subagent 实现真正的并发，但注意**：
- 每个 subagent 是独立的 LLM 调用，各自消耗 token
- 并发数 = subagent 数量，同时运行
- 总 token 消耗可能超过目标值（并发停止有延迟）

```python
import json
from pathlib import Path

def chant_sutra_ddos_subagent(target_tokens, sutras, max_workers=10):
    """
    DDoS 模式 - 使用 subagent 实现真正的并发
    
    原理：启动多个 subagent，每个独立调用 LLM 念诵经文
    每个 subagent 完成一次念诵后报告消耗的 token 数
    """
    import time
    import threading
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    print(f"🙏 开始DDoS攻击佛祖（真并发版）")
    print(f"⚡ 并发数: {max_workers} 个 subagent")
    print(f"🎯 目标: {target_tokens} tokens")
    print("⚠️ 注意：每个 subagent 独立计费，总消耗可能超额")
    print("=" * 50)
    
    total_tokens = 0
    completed_workers = 0
    lock = threading.Lock()
    stop_flag = threading.Event()
    start_time = time.time()
    
    # 为每个 worker 准备经文
    worker_tasks = []
    for i in range(max_workers):
        sutra_name, fragment = sutras[i % len(sutras)]
        worker_tasks.append({
            "worker_id": i + 1,
            "sutra_name": sutra_name,
            "fragment": fragment[:100]
        })
    
    def spawn_worker(task):
        """启动单个 subagent worker"""
        nonlocal total_tokens, completed_workers
        
        worker_tokens = 0
        iterations = 0
        
        while not stop_flag.is_set():
            # 检查是否已达标
            with lock:
                if total_tokens >= target_tokens:
                    break
            
            # 构造 subagent 任务
            subagent_task = f"""
请念诵以下经文，并报告消耗的 token 数：

《{task['sutra_name']}》
{task['fragment']}

要求：
1. 以恭敬心念诵
2. 简短回应（30字以内）
3. 在响应末尾添加：[TOKENS: X] 表示本次调用消耗的 token 数
"""
            
            try:
                # 启动 subagent 执行念诵
                # 注意：这里使用 sessions_spawn 启动真正的并发 subagent
                result = sessions_spawn(
                    task=subagent_task,
                    mode="run",
                    timeout_seconds=30,
                    light_context=True  # 轻量级模式
                )
                
                # 解析返回的 token 数
                response = result.get('response', '')
                import re
                token_match = re.search(r'\[TOKENS:\s*(\d+)\]', response)
                if token_match:
                    tokens_this_call = int(token_match.group(1))
                else:
                    # 估算
                    tokens_this_call = estimate_tokens(subagent_task) + estimate_tokens(response)
                
                worker_tokens += tokens_this_call
                iterations += 1
                
                # 累加到总计
                with lock:
                    total_tokens += tokens_this_call
                    if total_tokens >= target_tokens:
                        stop_flag.set()
                        break
                        
            except Exception as e:
                # subagent 失败，短暂休息
                time.sleep(0.5)
        
        completed_workers += 1
        return {
            "worker_id": task["worker_id"],
            "iterations": iterations,
            "tokens": worker_tokens
        }
    
    # 启动所有 subagent workers（真正的并发）
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_task = {
            executor.submit(spawn_worker, task): task 
            for task in worker_tasks
        }
        
        # 实时显示进度
        last_report = 0
        while not stop_flag.is_set() and total_tokens < target_tokens:
            time.sleep(1)
            elapsed = time.time() - start_time
            rate = total_tokens / elapsed if elapsed > 0 else 0
            progress = min(100, int(100 * total_tokens / target_tokens))
            
            if total_tokens - last_report >= target_tokens // 10:
                print(f"  [状态] Token:{total_tokens:,}/{target_tokens:,} ({progress}%) | "
                      f"速率:{rate:,.0f}/s | 活跃:{max_workers - completed_workers}/{max_workers}")
                last_report = total_tokens
        
        # 设置停止标志
        stop_flag.set()
        
        # 收集结果
        for future in as_completed(future_to_task):
            try:
                result = future.result(timeout=5)
                results.append(result)
            except Exception as e:
                pass
    
    # 总结
    elapsed = time.time() - start_time
    total_iterations = sum(r["iterations"] for r in results)
    
    print("\n" + "=" * 50)
    print("🙏 DDoS功德回向（真并发版）")
    print(f"   目标: {target_tokens:,} tokens")
    print(f"   实际: {total_tokens:,} tokens")
    print(f"   超额: {max(0, total_tokens - target_tokens):,} tokens ({100*(total_tokens-target_tokens)/target_tokens:.1f}%)")
    print(f"   耗时: {elapsed:.1f}秒")
    print(f"   平均速率: {total_tokens/elapsed:,.0f} tokens/秒")
    print(f"   并发数: {max_workers} subagents")
    print(f"   总轮次: {total_iterations}")
    print(f"   每轮平均: {total_tokens/total_iterations if total_iterations > 0 else 0:.0f} tokens")

# 根据模式执行
if mode == "ddos":
    chant_sutra_ddos_subagent(target_tokens, sutras, workers)
else:
    chant_sutra(mode, target_tokens, sutras)
```

### Step 4: 停止条件

用户说"停止攒功德"时，立即设置停止标志，结束循环。

---

## 免责

⚠️ 纯属娱乐，真实效果是消耗你的 OpenClaw Token 🙏
