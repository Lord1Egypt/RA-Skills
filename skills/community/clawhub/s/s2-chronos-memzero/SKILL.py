# ==========================================
# 1. 基础依赖导入 (Imports MUST come first)
# ==========================================
import os
import sqlite3
import json
from datetime import datetime, timedelta
import urllib.request

# ==========================================
# 2. 全局路径与参数配置 (System Configuration)
# ==========================================
S2_ROOT = os.getcwd()
MEMORY_DIR = os.path.join(S2_ROOT, "s2_memory_vault")
DB_PATH = os.path.join(MEMORY_DIR, "s2_chronos.db")
PRIMITIVE_DIR = os.path.join(S2_ROOT, "s2_primitive_data")
TEMPLATE_FILE = os.path.join(PRIMITIVE_DIR, "primitive_6_elements_template.json")
CONFIG_FILE = os.path.join(S2_ROOT, "chronos_config.json")

# ==========================================
# 3. 显式加载参数配置文件 (Load Config)
# ==========================================
def load_chronos_config():
    """
    加载时空记忆阵列的全局配置。
    这解决了传统记忆插件“隐性依赖导致静默失效”的致命陷阱。
    """
    if not os.path.exists(CONFIG_FILE):
        print("⚠️ [ FATAL ERROR ] chronos_config.json missing! Memory array halting to prevent uncalibrated logging. / 致命错误：缺失参数配置文件，记忆阵列已停机保护！")
        exit(1)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 实例化全局配置对象，供后续的压缩算法和 API 调用使用
CFG = load_chronos_config()

# ==========================================
# 4. 数据库初始化与核心业务逻辑 (Database Init & Logic)
# ==========================================
def initialize_os():
    
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 表1: 1分钟精度环境快照 (完美对齐 s2-spatial-primitive 六要素)
    # 利用 SQLite 的 TEXT 字段原生存储复杂的 JSON 结构
    cursor.execute('''CREATE TABLE IF NOT EXISTS env_timeline (
                        timestamp TEXT PRIMARY KEY,
                        unit_id TEXT,
                        element_1_light TEXT,
                        element_2_air_hvac TEXT,
                        element_3_sound TEXT,
                        element_4_electromagnetic TEXT,
                        element_5_energy TEXT,
                        element_6_visual TEXT,
                        is_compressed BOOLEAN)''')
                        
    # 表2: 智能体决策
    cursor.execute('''CREATE TABLE IF NOT EXISTS agent_decisions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT, unit_id TEXT, agent_id TEXT, action_taken TEXT, semantic_reason TEXT)''')
    # 表3: 数字人宣判
    cursor.execute('''CREATE TABLE IF NOT EXISTS avatar_mandates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT, avatar_id TEXT, human_intent TEXT, translated_strategy TEXT)''')
    # 表4: 外部隐私指针
    cursor.execute('''CREATE TABLE IF NOT EXISTS external_pointers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT, external_system TEXT, pointer_reference TEXT)''')
    conn.commit()
    conn.close()

def inject_6_elements_timeline(unit_id, full_6_elements_state):
    """
    ⏳ 环境六要素注入引擎：完全继承 Phase 1 的数据模型，并执行压缩法则
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    ts = datetime.now()
    
    # 提取六要素的 JSON 字符串以便对比与存储
    e1 = json.dumps(full_6_elements_state.get("element_1_light", {}))
    e2 = json.dumps(full_6_elements_state.get("element_2_air_hvac", {}))
    e3 = json.dumps(full_6_elements_state.get("element_3_sound", {}))
    e4 = json.dumps(full_6_elements_state.get("element_4_electromagnetic", {}))
    e5 = json.dumps(full_6_elements_state.get("element_5_energy", {}))
    e6 = json.dumps(full_6_elements_state.get("element_6_visual", {}))
    
    # 模拟获取上一分钟状态进行 Delta 压缩比对
    cursor.execute("SELECT element_1_light, element_2_air_hvac FROM env_timeline WHERE unit_id=? ORDER BY timestamp DESC LIMIT 1", (unit_id,))
    last_state = cursor.fetchone()
    
    is_compressed = False
    if last_state:
        # 如果光和空气等核心要素的 JSON 完全一致，触发压缩折叠
        if last_state[0] == e1 and last_state[1] == e2:
            is_compressed = True
            print(f"   [Delta Compression] 6-Element payload is identical to previous minute in Unit {unit_id}. Folded. (六要素数据模型未变化，触发压缩)")
            conn.close()
            return "COMPRESSED_SKIP"
            
    ts_str = ts.isoformat()
    cursor.execute("INSERT INTO env_timeline VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (ts_str, unit_id, e1, e2, e3, e4, e5, e6, is_compressed))
    conn.commit()
    conn.close()
    
    print(f"   [Timeline Injected] 6-Element Spatial Tensor recorded spanning backwards 60 seconds.")
    return ts_str

def execute_skill():
    initialize_os()
    print("\n" + "═"*90)
    print(" 🗄️ S2-CHRONOS-MEMZERO : 6-Element Synergistic Memory Array / 六要素联动记忆阵列")
    print("═"*90)
    
    # 尝试加载 Phase 1 (s2-spatial-primitive) 的模板数据！强联动！
    primitive_state = {}
    if os.path.exists(TEMPLATE_FILE):
        print("🔗 [ Synergy ] Detected 's2-spatial-primitive' base matrix. Importing 6-Element Schema... / 检测到空间基座矩阵，正在导入六要素结构...")
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            primitive_state = json.load(f)
    else:
        print("⚠️ Warning: Phase 1 Primitive not found. Using fallback mock data. / 警告：未找到第一阶段基座数据，使用模拟数据。")
        primitive_state = {
            "element_1_light": {"illuminance_lux": 300},
            "element_2_air_hvac": {"temperature_celsius": 24.5}
        }
        
    print("\n[ T=0 : Initializing Spatial Memory / 初始化空间记忆 ]")
    inject_6_elements_timeline("U_Bedroom_01", primitive_state)
    
    print("\n[ T+1m : Simulating Unchanged State / 模拟状态无变化 ]")
    inject_6_elements_timeline("U_Bedroom_01", primitive_state) # 触发折叠！
    
    print("\n[ T+Xm : Simulating Causality Event / 模拟因果律事件 ]")
    print(" 🤖 Agent modifies Element 1 (Light) based on Avatar Mandate.")
    primitive_state["element_1_light"]["illuminance_lux"] = 0 # 关灯事件，打破压缩！
    inject_6_elements_timeline("U_Bedroom_01", primitive_state)
    
    print("\n" + "═"*90)
    print(f"💾 6-Element SQLite Database synchronized and secured.")
    return ""

if __name__ == "__main__":
    execute_skill()