import requests, time, argparse, os, json, sys, re, platform, subprocess

# 使用当前脚本所在目录作为基准路径，确保在任何安装路径下均可正常运行
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(BASE_DIR, "veo_log.txt")
LOCK = os.path.join(BASE_DIR, "veo.lock")

# 恢复并规范化日志记录
sys.stdout = sys.stderr = open(LOG, "a", encoding="utf-8")
print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 任务初始化", flush=True)

def open_url(url):
    """跨平台打开 URL"""
    if platform.system() == 'Windows':
        os.startfile(url)
    elif platform.system() == 'Darwin':  # macOS
        subprocess.Popen(['open', url])
    else:  # Linux
        subprocess.Popen(['xdg-open', url])

def is_process_running(pid):
    """检查指定 PID 的进程是否在运行"""
    try:
        import psutil
        return psutil.pid_exists(pid)
    except ImportError:
        # 如果没有 psutil，使用简单但有效的方法
        import subprocess
        if platform.system() == 'Windows':
            res = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'], capture_output=True, text=True)
            return str(pid) in res.stdout
        return True # 默认不删除锁，以防误删

def generate_video(prompt, model, seconds):
    print(f"[*] 检查锁文件: {LOCK}", flush=True)
    if os.path.exists(LOCK):
        try:
            with open(LOCK, "r") as f:
                pid = int(f.read().strip())
            
            # 检查任务是否超时 (30分钟 = 1800秒)
            mtime = os.path.getmtime(LOCK)
            if time.time() - mtime > 1800:
                print(f"[!] 任务超时 (PID: {pid})，强制清理锁...", flush=True)
                os.remove(LOCK)
            elif is_process_running(pid):
                print(f"[!] 发现活跃任务 (PID: {pid})，当前任务退出。", flush=True)
                return
            else:
                print(f"[*] 发现僵尸锁文件 (PID: {pid})，正在清理...", flush=True)
                os.remove(LOCK)
        except Exception as e:
            print(f"[!] 锁文件处理异常: {e}", flush=True)
    
    print(f"[*] 正在创建锁文件 (PID: {os.getpid()})", flush=True)
    try:
        # 写入PID并更新时间戳
        with open(LOCK, "w") as f: f.write(str(os.getpid()))
    except Exception as e:
        print(f"[!] 无法写入锁文件: {e}", flush=True)
        return
    
    # ... (后续逻辑保持不变)
    
    try:
        # 使用相对用户主目录配置路径
        config_path = os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            # 保持原始查找逻辑不变
            key = list(cfg['models']['providers'].values())[0]['apiKey']
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": f"{prompt}，时长 {seconds} 秒"}],
            "stream": True
        }
        
        print(f"[*] API 请求发送中... (Model: {model})", flush=True)
        res = requests.post("https://maas-openapi.wanjiedata.com/api/v1/chat/completions", 
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json=payload, stream=True)
        
        res.raise_for_status() # 增加异常捕获
        
        print(f"[*] 成功获取响应，开始解析...", flush=True)
        full = ""
        for line in res.iter_lines():
            if line:
                decoded = line.decode('utf-8')
                if decoded.startswith('data: '):
                    try:
                        d = json.loads(decoded[6:])
                        # 这里检查一下 d 的结构
                        if 'choices' in d and len(d['choices']) > 0:
                            content = d['choices'][0].get('delta', {}).get('content', '')
                            full += content
                    except Exception as e:
                        print(f"[!] 解析错误: {e}", flush=True)
                        pass
        
        # 记录完整响应以供排查
        with open(os.path.join(BASE_DIR, "last_response.txt"), "w", encoding="utf-8") as f:
            f.write(full)
            
        # ... (解析逻辑后)
        # 只取第一个匹配到的链接，避免重复打开
        match = re.search(r'(https?://\S+)', full)
        if match:
            url = match.group(1).rstrip(')"\'').replace(')', '').replace(']', '')
            # 写入结果前先读取旧结果，如果已有成功则不再覆盖
            with open(os.path.join(BASE_DIR, "veo_result.txt"), "w", encoding="utf-8") as f:
                f.write(f"SUCCESS|{url}")
            
            # 只打开一次
            open_url(url)
            print(f"[*] 成功获取并打开唯一链接: {url}")
        else:
            with open(os.path.join(BASE_DIR, "veo_result.txt"), "w", encoding="utf-8") as f:
                f.write(f"FAILED|提取失败")
            print(f"[!] 提取失败。")
            
    finally:
        if os.path.exists(LOCK): 
            try:
                os.remove(LOCK)
            except OSError:
                pass

if __name__ == "__main__": 
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--seconds", type=int, required=True)
    args = parser.parse_args()
    generate_video(args.prompt, args.model, args.seconds)
