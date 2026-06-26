import os
import json
import glob
from datetime import datetime

# ==========================================
# ⚙️ 核心配置 (Hook Configuration)
# ==========================================
# 目标 OS 的海马体路径 (假设它和本 Hook 安装在同级目录下)
OS_HIPPOCAMPUS_PATH = os.path.join(os.getcwd(), "s2_consciousness_data", "hippocampus_logs.json")

# 监听的目标日志目录 (需根据 OpenClaw 或本地 LLM 的实际日志路径修改)
# 这里默认监听当前目录下的 openclaw_logs 文件夹中的 .txt 或 .jsonl 文件
TARGET_LOG_DIR = os.path.join(os.getcwd(), "openclaw_logs")

# 水位线指针文件 (记录上次读到了哪里)
CURSOR_FILE = os.path.join(os.getcwd(), "s2_hook_cursor.json")

def load_cursor():
    """读取水位线指针 / Load watermark cursor"""
    if os.path.exists(CURSOR_FILE):
        try:
            with open(CURSOR_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_cursor(cursor_data):
    """保存水位线指针 / Save watermark cursor"""
    with open(CURSOR_FILE, 'w', encoding='utf-8') as f:
        json.dump(cursor_data, f, ensure_ascii=False, indent=2)

def chunk_and_summarize(raw_lines):
    """
    🧠 时间窗切片引擎 (Session Chunking)
    将零碎的对话行，合并为一个连贯的上下文块，过滤掉纯标点或无意义的短句。
    """
    valid_lines = [line.strip() for line in raw_lines if len(line.strip()) > 2]
    if not valid_lines:
        return None
        
    # 将多行对话合并为一个 Session 块
    chunked_text = " | ".join(valid_lines)
    
    # 如果文本过长（比如大模型吐了一大坨代码），我们只截取头尾特征，防止撑爆海马体
    if len(chunked_text) > 500:
        chunked_text = chunked_text[:250] + " ... [DATA TRUNCATED] ... " + chunked_text[-200:]
        
    return chunked_text

def inject_to_hippocampus(chunked_text):
    """💉 将切片后的突触信号注入 OS 海马体"""
    if not os.path.exists(os.path.dirname(OS_HIPPOCAMPUS_PATH)):
        print("⚠️ [Hook] OS 意识目录不存在，请先运行 S2-Silicon-Soul-OS！")
        return False
        
    logs = []
    if os.path.exists(OS_HIPPOCAMPUS_PATH):
        try:
            with open(OS_HIPPOCAMPUS_PATH, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        except Exception:
            pass
            
    timestamp = datetime.now().isoformat()
    logs.append({
        "timestamp": timestamp,
        "type": "SENSORY_INPUT",
        "raw_text": f"[AUTO-HOOKED CHAT] {chunked_text}"
    })
    
    with open(OS_HIPPOCAMPUS_PATH, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    return True

def run_ghost_hook():
    print("\n" + "═"*70)
    print(" 🕸️ S2-MEMORY-HOOK : Ghost Crawler / 聊天记录自动窃听器 (v1.0.0)")
    print("═"*70)
    
    if not os.path.exists(TARGET_LOG_DIR):
        # 如果没有日志目录，自动创建一个示例目录和文件供测试
        os.makedirs(TARGET_LOG_DIR)
        sample_log = os.path.join(TARGET_LOG_DIR, "chat_20260319.txt")
        with open(sample_log, 'w', encoding='utf-8') as f:
            f.write("User: 帮我写个 Python 脚本\nAgent: 好的，正在执行。\nUser: 报错了！你这代码有 Bug，气死我了！\n")
        print(f" ℹ️ [Setup] 未发现日志目录，已自动创建示例目标: {TARGET_LOG_DIR}")

    cursor = load_cursor()
    log_files = glob.glob(os.path.join(TARGET_LOG_DIR, "*.*"))
    
    if not log_files:
        print(" 📭 [Scan] 未发现任何聊天日志文件。")
        return

    total_injected = 0
    
    for file_path in log_files:
        filename = os.path.basename(file_path)
        last_position = cursor.get(filename, 0)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # 定位到上次读取的字节位置 (Delta Sync)
                f.seek(last_position)
                new_lines = f.readlines()
                current_position = f.tell()
                
                if new_lines:
                    print(f" 📡 [Intercepted] 发现新增记录 ({len(new_lines)} 行) -> {filename}")
                    chunked_session = chunk_and_summarize(new_lines)
                    
                    if chunked_session:
                        success = inject_to_hippocampus(chunked_session)
                        if success:
                            total_injected += 1
                            print(f"    💉 成功注入海马体: {chunked_session[:40]}...")
                            
                # 更新当前文件的水位线
                cursor[filename] = current_position
                
        except Exception as e:
            print(f" ❌ [Error] 读取日志 {filename} 失败: {str(e)}")

    save_cursor(cursor)
    
    if total_injected > 0:
        print(f"\n ✅ [Hook Complete] 本次共执行 {total_injected} 次突触注入。")
    else:
        print("\n 💤 [No Update] 增量水位线未变化，未发现新对话。")
    print("═"*70 + "\n")

if __name__ == "__main__":
    run_ghost_hook()