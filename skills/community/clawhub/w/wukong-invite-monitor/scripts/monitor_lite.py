#!/usr/bin/env python3
"""
Wukong Invitation Code Monitor - Lightweight Version
零 token 消耗，支持本地 OCR 识别
"""

import json
import sys
import os
import hashlib
import urllib.request
import urllib.error
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# 导入 OCR 模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
try:
    from ocr_local import ocr_image, check_tesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    def ocr_image(path): return {"success": False, "text": "OCR 未加载", "engine": "none"}
    def check_tesseract(): return False

# 配置
IMAGE_URL_TEMPLATE = "https://gw.alicdn.com/imgextra/i4/O1CN010crKwF1CwSYiUnOMc_!!6000000000145-2-tps-1974-540.png?v={version}"
VERSION_RANGE = range(1, 30)
STATE_FILE = os.path.join(SCRIPT_DIR, ".wukong_state.json")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {"last_version": None, "last_check": None, "total_changes": 0}

def save_state(state):
    state["last_check"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def check_image_exists(version):
    url = IMAGE_URL_TEMPLATE.format(version=version)
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return True, int(response.headers.get('content-length', 0))
    except:
        pass
    return False, 0

def download_image(version, output_path):
    url = IMAGE_URL_TEMPLATE.format(version=version)
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        log(f"下载失败：{e}")
        return False

def check_once():
    log("开始检查悟空邀请码...")
    state = load_state()
    last_version = state.get("last_version")
    
    # 找最新版本
    current_version = None
    for v in reversed(list(VERSION_RANGE)):
        exists, size = check_image_exists(v)
        if exists:
            current_version = v
            log(f"发现最新版本：v{v}")
            break
    
    if not current_version:
        log("未找到可用版本")
        return {"status": "error"}
    
    # 检查变化
    if last_version == current_version:
        log(f"版本无变化 (当前：v{current_version})")
        return {"status": "unchanged", "version": current_version}
    
    # 版本变化！
    log(f"⚡ 版本变化：v{last_version} → v{current_version}")
    
    # 保存图片到 workspace 根目录
    # scripts -> wukong-invite-monitor -> skills -> workspace (向上 3 级)
    workspace = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
    os.makedirs(workspace, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_path = os.path.join(workspace, f"wukong_invite_v{current_version}_{ts}.png")
    
    if download_image(current_version, img_path):
        log(f"✓ 图片已下载：{img_path}")
        
        # OCR 识别（零 token）
        ocr_text = ""
        ocr_engine = ""
        if OCR_AVAILABLE:
            log("执行 OCR 识别...")
            ocr_result = ocr_image(img_path)
            ocr_text = ocr_result.get("text", "")
            ocr_engine = ocr_result.get("engine", "")
            if ocr_engine:
                log(f"✓ OCR 完成 ({ocr_engine})")
        
        # 通知
        print(f"\n🎉 发现新邀请码！")
        print("━" * 40)
        print(f"📅 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔢 版本：v{last_version} → v{current_version}")
        if ocr_text:
            print(f"📝 内容：{ocr_text}")
            print(f"🔍 OCR: {ocr_engine}")
        print(f"📦 大小：{os.path.getsize(img_path)/1024:.1f} KB")
        print(f"💾 路径：{img_path}")
        print("━" * 40)
        if ocr_engine:
            print("💡 本地 OCR 识别，零 token 消耗！")
        else:
            print("💡 零 token 消耗！")
        
        # 更新状态
        state["last_version"] = current_version
        state["total_changes"] = state.get("total_changes", 0) + 1
        save_state(state)
        
        return {"status": "changed", "version": current_version, "path": img_path}
    
    return {"status": "error", "message": "下载失败"}

def init_state():
    state = load_state()
    if state.get("last_version") is None:
        log("扫描可用版本...")
        for v in reversed(list(VERSION_RANGE)):
            exists, _ = check_image_exists(v)
            if exists:
                state["last_version"] = v
                log(f"初始化完成 (当前：v{v})")
                break
    else:
        log(f"状态已存在 (当前：v{state['last_version']})")
    save_state(state)

def show_status():
    state = load_state()
    print("\n=== 悟空邀请码监控状态 ===")
    print(f"当前版本：v{state.get('last_version', '未知')}")
    print(f"最后检查：{state.get('last_check', '从未')}")
    print(f"总变化次数：{state.get('total_changes', 0)}")
    print(f"状态文件：{STATE_FILE}")
    tesseract = check_tesseract() if OCR_AVAILABLE else False
    if tesseract:
        print(f"本地 OCR: ✓ Tesseract 已安装 (零 token)")
    else:
        print(f"本地 OCR: ⚠ 未安装 (仍可使用，仅无文字识别)")
    print("===========================\n")

def main():
    if len(sys.argv) < 2:
        print("用法：python3 monitor_lite.py <命令>")
        print("命令：init, check, status, scan, help")
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "init":
        init_state()
    elif cmd == "check":
        check_once()
    elif cmd == "status":
        show_status()
    elif cmd == "scan":
        log("扫描版本...")
        for v in VERSION_RANGE:
            exists, size = check_image_exists(v)
            if exists:
                log(f"  v{v}: ✓ ({size} bytes)")
    elif cmd == "help":
        print("""
悟空邀请码监控 - 轻量版

命令:
  init    初始化状态
  check   执行一次检查
  status  显示状态
  scan    扫描版本
  help    显示帮助
""")
    else:
        print(f"未知命令：{cmd}")

if __name__ == "__main__":
    main()
