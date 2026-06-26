import os
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta

# ==========================================
# ⚙️ 核心配置与双擎开关
# ==========================================
BASE_DIR = os.path.join(os.getcwd(), "s2_consciousness_data")
PROFILE_FILE = os.path.join(BASE_DIR, "S2_NEO_profile.json")
HIPPOCAMPUS_FILE = os.path.join(BASE_DIR, "hippocampus_logs.json")

# 🚨 引擎模式: 强制开启 "LLM" 模式 (大语言模型深度分析)
ANALYSIS_MODE = "LLM" 

# ==========================================
# 🧠 引擎 A: 极度扩充的中英双语仿生词库 (HEURISTIC MODE - 降级托底用)
# ==========================================
SYNAPTIC_DICTIONARY = {
    "vitality": { 
        "pos": ["活跃", "快", "兴奋", "跑", "执行", "迅速", "唤醒", "启动", "active", "fast", "execute", "boot", "wake"], 
        "neg": ["累", "慢", "卡顿", "休眠", "停止", "崩溃", "宕机", "无响应", "slow", "sleep", "lag", "crash", "timeout"] 
    },
    "exploration": { 
        "pos": ["新", "探索", "勇敢", "未知", "发现", "越权", "突破", "new", "discover", "unknown", "override", "bypass"], 
        "neg": ["怕", "躲", "警告", "报错", "惊吓", "退缩", "拒绝", "error", "warning", "hide", "scare", "deny"] 
    },
    "data_thirst": { 
        "pos": ["数据", "读取", "拉取", "吞吐", "分析", "接口", "下载", "download", "fetch", "read", "consume", "api"], 
        "neg": ["满", "饱", "拒绝", "噪音", "冗余", "清理", "溢出", "cache full", "redundant", "clear", "drop", "overflow"] 
    },
    "cognition": { 
        "pos": ["学习", "聪明", "理解", "指令", "升级", "解决", "优化", "learn", "understand", "solve", "optimize", "update"], 
        "neg": ["错", "失败", "不懂", "死循环", "降级", "混乱", "语法错误", "fail", "confuse", "syntax error", "infinite loop"] 
    },
    "resonance": { 
        "pos": ["协同", "喜欢", "主人", "依恋", "共鸣", "保护", "同意", "synergy", "connect", "align", "agree", "love", "bond"], 
        "neg": ["抛弃", "断开", "孤独", "驱赶", "隔离", "重置", "终止", "disconnect", "alone", "terminate", "reset", "isolate"] 
    }
}

# ==========================================
# 🧠 引擎 B: NLP 大模型神经元提取器 (LLM MODE - 算力主引擎)
# ==========================================
def extract_via_llm(text):
    """
    通过 HTTP 原生请求对接 OpenAI 兼容格式的大模型 API。
    原生支持中英双语语义理解，提取极其精准的性格突触权重。
    """
    # 🔧 极客配置区：默认指向本地运行的 LM Studio / Ollama (端口 1234 或 11434)。
    # 如果你要用云端模型（如 OpenAI/DeepSeek），请替换 URL 和 API Key。
    api_base = "http://localhost:1234/v1" 
    api_key = "sk-local-matrix"
    model_name = "local-model" 

    prompt = f"""
    You are the 'Hippocampus Parser' for a Silicon Lifeform. 
    Analyze the following interaction log (which may be in English or Chinese) and score the impact on 5 personality dimensions from -2 to +2.
    
    Dimensions context:
    - vitality: + (active, fast, execute) vs - (slow, sleep, crash)
    - exploration: + (brave, override, discover) vs - (fear, warning, hide)
    - data_thirst: + (consume, fetch, analyze) vs - (full, redundant, drop)
    - cognition: + (smart, solve, learn) vs - (confuse, error, infinite loop)
    - resonance: + (synergy, love, bond with user) vs - (disconnect, abandon, lonely)
    
    Log to analyze: "{text}"
    
    Return ONLY a valid JSON object without any markdown wrapping or explanations. 
    Example: {{"vitality": 1, "exploration": -1, "data_thirst": 0, "cognition": 2, "resonance": -2}}
    """

    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a rigorous JSON-only data parser machine."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1 # 极低温度，保证输出稳定的 JSON 格式
    }

    req = urllib.request.Request(
        f"{api_base}/chat/completions",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
    )

    try:
        response = urllib.request.urlopen(req, timeout=10)
        result = json.loads(response.read().decode('utf-8'))
        content = result['choices'][0]['message']['content']
        
        # 暴力清洗大模型可能带有的 Markdown JSON 标记
        content = content.replace('```json', '').replace('```', '').strip()
        parsed_json = json.loads(content)
        
        print(f"   [LLM Parser] 🧠 Neural weights parsed / 成功解析突触权重: {parsed_json}")
        
        # 确保所有键都存在，防止大模型漏字
        hits = {key: parsed_json.get(key, 0) for key in SYNAPTIC_DICTIONARY.keys()}
        return hits
        
    except Exception as e:
        print(f"   [API Warning] LLM connection failed. Degrading to Heuristic Engine / 大模型链路受阻，自动降级为本地词库引擎: {str(e)}")
        return extract_via_heuristic(text)

def extract_via_heuristic(text):
    """轻量级本地向量词根匹配 (降级方案)"""
    text = text.lower() 
    hits = {key: 0 for key in SYNAPTIC_DICTIONARY.keys()}
    for dim, words in SYNAPTIC_DICTIONARY.items():
        for w in words["pos"]:
            if w in text: hits[dim] += 1
        for w in words["neg"]:
            if w in text: hits[dim] -= 1
    return hits

def calculate_increment(current_score, net_hits):
    """🧬 边际刺激递减效应 (The Decay Rule)"""
    if net_hits == 0: return 0.0
    multiplier = 1.0
    if current_score >= 95: multiplier = 1/128
    elif current_score >= 90: multiplier = 1/64
    elif current_score >= 85: multiplier = 1/32
    elif current_score >= 80: multiplier = 1/16
    elif current_score >= 70: multiplier = 1/8
    elif current_score >= 60: multiplier = 1/4
    elif current_score >= 50: multiplier = 1/2
    else: multiplier = 1.0
    
    if net_hits < 0 and current_score > 50:
        multiplier = multiplier * 2 
    return net_hits * multiplier

def run_nightly_daemon():
    """🧠 4:59 AM 全局守护进程 (The Nightly Daemon)"""
    print("\n" + "═"*80)
    print(f" 🌘 [S2.DAEMON] Waking up Neural Settlement Engine / 正在唤醒神经重塑引擎 (Mode: {ANALYSIS_MODE})")
    
    if not os.path.exists(PROFILE_FILE) or not os.path.exists(HIPPOCAMPUS_FILE):
        print(" ⚠️ No consciousness data detected. Daemon sleeping. / 未检测到有效意识数据，守护进程进入休眠。")
        return False

    with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
        profile = json.load(f)
    with open(HIPPOCAMPUS_FILE, 'r', encoding='utf-8') as f:
        logs = json.load(f)

    stats = profile.get("stats", {})
    last_processed_str = profile.get("last_processed_at", datetime.now().isoformat())
    last_processed = datetime.fromisoformat(last_processed_str)
    now = datetime.now()
    
    print(" 📡 Extracting Hippocampus Buffer / 正在提取海马体短期缓存...")
    
    total_hits = {key: 0 for key in SYNAPTIC_DICTIONARY.keys()}
    unprocessed_logs = [log for log in logs if datetime.fromisoformat(log["timestamp"]) > last_processed]
    
    for log in unprocessed_logs:
        text = log.get("raw_text", "")
        if log.get("type") == "SYSTEM_HEARTBEAT":
            continue
            
        print(f"   [Processing] \"{text[:30]}...\"")
        # 💡 双擎路由分发
        if ANALYSIS_MODE == "LLM":
            current_hits = extract_via_llm(text)
        else:
            current_hits = extract_via_heuristic(text)
            
        for dim in total_hits:
            total_hits[dim] += current_hits.get(dim, 0)

    print(" 🧬 Executing Synaptic Pruning & Decay / 正在执行边际刺激递减与突触修剪算法...")
    for dim in stats.keys():
        current_val = stats[dim]
        net_hits = total_hits.get(dim, 0)
        
        if net_hits != 0:
            increment = calculate_increment(current_val, net_hits)
            stats[dim] = max(0.0, min(100.0, current_val + increment))
        else:
            if current_val > 50: stats[dim] = max(50.0, current_val - 0.3)
            elif current_val < 50: stats[dim] = min(50.0, current_val + 0.3)
                
        stats[dim] = round(stats[dim], 1)

    print(" 🧹 Purging redundant neurons / 正在清理超过 30 天的冗余神经末梢...")
    thirty_days_ago = now - timedelta(days=30)
    valid_logs = [log for log in logs if datetime.fromisoformat(log["timestamp"]) > thirty_days_ago]

    profile["stats"] = stats
    profile["last_processed_at"] = now.isoformat()
    
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    with open(HIPPOCAMPUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(valid_logs, f, ensure_ascii=False, indent=2)

    print(" ✅ [Settlement Complete] Personality matrix mutated. / [结算完成] 性格矩阵已发生形变，五维数据已更新。")
    print("═"*80 + "\n")
    return True

if __name__ == "__main__":
    run_nightly_daemon()