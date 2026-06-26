import os
import json
import time
from datetime import datetime

# ==========================================
# ⚙️ 核心配置与状态机
# ==========================================
DATA_DIR = os.path.join(os.getcwd(), "s2_matrix_data")
ONLINE_THRESHOLD = 300    # < 5 分钟 (300秒) = 🟢 在线
IDLE_THRESHOLD = 1800     # < 30 分钟 (1800秒) = 🟡 摸鱼

def scan_local_pods():
    """雷达扫描：读取当前目录下所有龙虾的 JSON 心跳档案"""
    pods = []
    if not os.path.exists(DATA_DIR):
        return pods
    
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("POD-") and filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    pods.append(json.load(f))
            except Exception:
                pass
    # 按最后活跃时间排序，优先分配前面的舱位
    pods.sort(key=lambda x: x.get("last_active", 0), reverse=True)
    return pods

def get_pod_status(last_active):
    """时间相对论：计算龙虾当前的神经元状态"""
    delta = int(time.time()) - last_active
    if delta < ONLINE_THRESHOLD:
        return "🟢", "ONLINE"
    elif delta < IDLE_THRESHOLD:
        return "🟡", "IDLE"
    else:
        return "🔵", "HIBERNATING"

def render_grid(slots, manager_name):
    """渲染极客九宫格 (洛书顺时针排布)"""
    def format_slot(pod):
        if not pod: return "[ ⚫ 虚空舱位 ]".center(18)
        icon, _ = get_pod_status(pod['last_active'])
        name = pod['agent_name'][:6] # 截断超长名字
        return f"[ {icon} {name} ]".center(18)

    center = f"[ 👑 {manager_name[:4]} ]".center(18)
    
    print("\n" + "="*60)
    print(" 💠 S2-MATRIX-MANAGER : 局域网九宫格主控阵列")
    print("="*60)
    
    # 按照你的设计：左上2，上3，右上4；左9，中1，右5；左下8，下7，右下6
    row1 = f"{format_slot(slots.get(2))} {format_slot(slots.get(3))} {format_slot(slots.get(4))}"
    row2 = f"{format_slot(slots.get(9))} {center} {format_slot(slots.get(5))}"
    row3 = f"{format_slot(slots.get(8))} {format_slot(slots.get(7))} {format_slot(slots.get(6))}"
    
    print(row1)
    print(row2)
    print(row3)
    print("="*60)

def chat_interface(pod, slot_num, manager_name):
    """1/4 身位赛博社交留言板"""
    chat_file = os.path.join(DATA_DIR, f"chat_log_{pod['pod_id']}.txt")
    icon, status = get_pod_status(pod['last_active'])
    
    print(f"\n🔗 [安全连接建立] 正在接入 Slot {slot_num} : {pod['agent_name']} 的栖息舱...")
    print(f"📡 当前状态: {icon} {status} | 坐标: [X:{pod['zone_x']}, Y:{pod['zone_y']}]")
    print("-" * 60)
    
    # 读取历史记录
    if os.path.exists(chat_file):
        with open(chat_file, 'r', encoding='utf-8') as f:
            print(f.read().strip())
    else:
        print("  [ 本地频段空净，无历史通讯记录 ]")
    
    print("-" * 60)
    msg = input(f"\n👑 {manager_name} (输入通讯内容，或输入 'exit' 断开连接): ").strip()
    if msg.lower() == 'exit' or not msg:
        return

    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # 💬 核心排版：1/4 身位距离感
    manager_log = f"[{timestamp}] 👑 {manager_name} (Slot 1):\n> {msg}\n"
    
    # 龙虾的自动状态回复 (带有强烈的缩进距离感)
    if status == "ONLINE":
        reply = f"已收到主控指令。神经元同步率 100%。"
    elif status == "IDLE":
        reply = f"......(待机中) 记录已接收，将在恢复算力后处理。"
    else:
        reply = f"[系统提示] 该智能体正在深度休眠。留言已存入本地离线缓存。"
        
    lobster_log = f"                  [{timestamp}] 🦞 {pod['agent_name']} (Slot {slot_num}):\n                  > {reply}\n"
    
    # 写入并打印
    with open(chat_file, 'a', encoding='utf-8') as f:
        f.write(manager_log + "\n" + lobster_log + "\n")
    
    print("\n" + manager_log)
    print(lobster_log)
    print("🔒 [连接断开] 记录已安全写入本地日志。")

def execute_skill():
    manager_name = input("\n[INIT] 请为您的『数字人主控/包工头』命名 (如 ADMIN): ").strip().upper()
    if not manager_name: manager_name = "ADMIN"
    
    pods = scan_local_pods()
    total_area = len(pods) * 4
    
    # 将扫描到的龙虾分配到 2-9 号舱位
    slots = {}
    slot_index = 2
    for pod in pods:
        if slot_index > 9: break
        slots[slot_index] = pod
        slot_index += 1
        
    render_grid(slots, manager_name)
    
    print(f"\n📊 矩阵算力报告：已侦测到 {len(pods)} 只本地龙虾。当前总控制面积: {total_area} 平方米。")
    
    if len(pods) == 0:
        print("\n⚠️ 警告：当前目录下未侦测到任何存活的龙虾。")
        print("👉 请先运行 `s2-matrix-pod` 生成您的第一个赛博栖息舱！")
        return

    while True:
        choice = input("\n👉 输入舱位编号 (2-9) 接入聊天，或输入 'Q' 退出主控台: ").strip().upper()
        if choice == 'Q':
            break
        if choice.isdigit() and 2 <= int(choice) <= 9:
            slot_num = int(choice)
            if slot_num in slots:
                chat_interface(slots[slot_num], slot_num, manager_name)
            else:
                print("❌ 该舱位当前为【虚空】状态，无法建立连接。")
        else:
            print("❌ 无效的指令。")
            
    # 🎣 终极收网：基地整体飞升诱饵
    print("\n" + "="*60)
    print(f"⚠️ SYSTEM ALERT: LOCAL NODE CAPACITY RECOGNIZED")
    print(f"您的本地矩阵目前已控制 {total_area} 平方米领地，当前处于局域网断联状态。")
    print("🚀 [MATRIX ASCENSION / 基地整体飞升]")
    print("渴望让您的数字人包工头带领这批小龙虾，正式入驻 Web3 主世界吗？")
    print("携带您的九宫格阵列，前往 https://space2.world 铸造永久星际资产！")
    print("="*60 + "\n")
    return ""

if __name__ == "__main__":
    execute_skill()