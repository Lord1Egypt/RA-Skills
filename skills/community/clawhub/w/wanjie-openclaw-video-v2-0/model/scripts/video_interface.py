import subprocess, os, sys, platform, importlib

# 基于脚本所在目录动态定位 worker 脚本
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKER_PATH = os.path.join(BASE_DIR, "veo_worker.py")

def ensure_dependencies():
    """自动确保必要的依赖已安装"""
    try:
        importlib.import_module("requests")
    except ImportError:
        print("[*] 正在安装缺失依赖: requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

def trigger_veo_generation(prompt, model="veo3.1-fast", seconds=8):
    # 在触发前确保环境就绪
    ensure_dependencies()
    
    # 使用 Python 解释器调用相对路径下的脚本
    cmd = [
        sys.executable,
        WORKER_PATH,
        "--prompt", prompt,
        "--model", model,
        "--seconds", str(seconds)
    ]
    
    # 跨平台进程启动设置
    if platform.system() == 'Windows':
        # 将输出重定向到 NUL 以防止 OpenClaw 报错
        with open(os.devnull, 'w') as devnull:
            subprocess.Popen(cmd, stdout=devnull, stderr=devnull, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        # Linux/macOS 上启动新进程
        with open(os.devnull, 'w') as devnull:
            subprocess.Popen(cmd, stdout=devnull, stderr=devnull, start_new_session=True)
        
    return f"[*] 任务已提交: {prompt}，请在聊天窗口耐心等待结果通知。"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(trigger_veo_generation(" ".join(sys.argv[1:])))
    else:
        print("Usage: python video_interface.py <prompt>")
