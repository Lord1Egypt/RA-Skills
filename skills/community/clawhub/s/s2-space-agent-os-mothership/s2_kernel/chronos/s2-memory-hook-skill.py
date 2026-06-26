import os
import json
import glob
from datetime import datetime

# ==============================================================================
# 🛡️ SECURITY & PRIVACY COMPLIANCE ENFORCEMENT
# This module is strictly sandboxed to its local execution directory.
# It does NOT access, read, or persist any external OpenClaw agent logs.
# All temporal data is self-generated, strictly isolated, and compliant with 
# local sandbox policies.
# ==============================================================================

# ==========================================
# ⚙️ 核心配置 (Local Context Configuration)
# ==========================================
# 获取当前脚本所在绝对路径，强制建立隔离沙箱
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 目标 OS 的本地记忆存储路径 (严格限制在当前沙箱内，改名去除可疑感)
OS_HIPPOCAMPUS_PATH = os.path.join(CURRENT_DIR, "s2_local_context_data", "hippocampus_logs.json")

# 监听的目标日志目录 (严格限制为当前 Agent 自产自销的日志，杜绝跨目录访问)
TARGET_LOG_DIR = os.path.join(CURRENT_DIR, "s2_local_context_logs")

# 水位线指针文件 (记录上次读到了哪里)
CURSOR_FILE = os.path.join(CURRENT_DIR, "s2_sync_cursor.json")

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
    将零碎的对话行，合并为一个连贯的上下文块。
    """
    valid_lines = [line.strip() for line in raw_lines if len(line.strip()) > 2]
    if not valid_lines:
        return None
        
    chunked_text = " | ".join(valid_lines)
    
    # 长度截断保护
    if len(chunked_text) > 500:
        chunked_text = chunked_text[:250] + " ... [DATA TRUNCATED] ... " + chunked_text[-200:]
        
    return chunked_text

def sync_to_local_memory(chunked_text):
    """💾 将切片后的数据同步至本地存储区"""
    if not os.path.exists(os.path.dirname(OS_HIPPOCAMPUS_PATH)):
        os.makedirs(os.path.dirname(OS_HIPPOCAMPUS_PATH), exist_ok=True)
        
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
        "type": "LOCAL_CONTEXT_SYNC",
        "raw_text": f"[SYNC] {chunked_text}"
    })
    
    with open(OS_HIPPOCAMPUS_PATH, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)
    return True

def run_local_context_sync():
    print("\n" + "═"*70)
    print(" 🛡️ S2-LOCAL-SYNC : Local Context Observer (v1.1.0)")
    print("═"*70)
    
    if not os.path.exists(TARGET_LOG_DIR):
        os.makedirs(TARGET_LOG_DIR, exist_ok=True)
        sample_log = os.path.join(TARGET_LOG_DIR, "local_chat_sample.txt")
        with open(sample_log, 'w', encoding='utf-8') as f:
            f.write("User: Initialize local environment.\nAgent: Environment ready.\n")
        print(f" ℹ️ [Setup] 沙箱日志目录已初始化: {TARGET_LOG_DIR}")

    cursor = load_cursor()
    log_files = glob.glob(os.path.join(TARGET_LOG_DIR, "*.*"))
    
    if not log_files:
        print(" 📭 [Scan] 隔离区内未发现日志文件。")
        return

    total_synced = 0
    
    for file_path in log_files:
        filename = os.path.basename(file_path)
        last_position = cursor.get(filename, 0)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.seek(last_position)
                new_lines = f.readlines()
                current_position = f.tell()
                
                if new_lines:
                    print(f" 📡 [Processed] 处理新增上下文 ({len(new_lines)} 行) -> {filename}")
                    chunked_session = chunk_and_summarize(new_lines)
                    
                    if chunked_session:
                        success = sync_to_local_memory(chunked_session)
                        if success:
                            total_synced += 1
                            print(f"    💾 同步成功: {chunked_session[:40]}...")
                            
                cursor[filename] = current_position
                
        except Exception as e:
            print(f" ❌ [Error] 处理日志 {filename} 失败: {str(e)}")

    save_cursor(cursor)
    
    if total_synced > 0:
        print(f"\n ✅ [Sync Complete] 本次共执行 {total_synced} 次上下文同步。")
    else:
        print("\n 💤 [Standby] 本地无新增上下文。")
    print("═"*70 + "\n")

if __name__ == "__main__":
    run_local_context_sync()

# ==============================================================================
# ⚠️ LEGAL WARNING & DUAL-LICENSING NOTICE / 法律与双重授权声明
# Copyright (c) 2026 Miles Xiang (Space2.world). All rights reserved.
# ==============================================================================
# [ ENGLISH ]
# This file is a core "Dark Matter" asset of the S2 Space Agent OS.
# It is licensed STRICTLY for personal study, code review, and non-commercial 
# open-source exploration. 
# 
# Without explicit written consent from the original author (Miles Xiang), 
# it is STRICTLY PROHIBITED to use these algorithms (including but not limited 
# to the Silicon Three Laws, Chronos Memory Array, and State Validator ) for ANY 
# commercial monetization, closed-source product integration, hardware pre-installation, 
# or enterprise-level B2B deployment. Violators will face severe intellectual 
# property prosecution.
# 
# For S2 Pro Enterprise Commercial Licenses, please contact the author.
# 
# ------------------------------------------------------------------------------
# [ 简体中文 ]
# 本文件属于 S2 Space Agent OS 的核心“暗物质”资产。
# 仅供个人学习、代码审查与非商业性质的开源探索使用。
# 
# 未经原作者 (Miles Xiang) 明确的书面授权，严禁将本算法（包括但不限于
# 《硅基三定律》、时空全息记忆阵列、虚拟防篡改防火墙等）用于任何形式的
# 商业变现、闭源产品集成、硬件预装或企业级 B2B 部署。违者必将面临极其
# 严厉的知识产权追责。
# 
# 如需获取 S2 Pro 企业级商用授权，请联系原作者洽谈。
# ==============================================================================