"""
city-game 本地预览服务
用法: python3 scripts/serve.py <html文件路径>

启动一个轻量 HTTP 服务，自动打开浏览器访问生成的 H5 页面。
服务会在前台运行，Ctrl+C 或关闭终端即可停止。

端口策略:
  - 优先使用固定端口 8080。
  - 启动前通过 PID 文件找到上一次本脚本的进程，并在终止前验证进程身份
    （确认命令行中包含 serve.py），防止误杀 PID 被复用后的其他程序。
  - 若旧进程身份验证失败，跳过终止，改为随机申请一个系统空闲端口（不抢占任何端口）。
"""

import sys, os, signal, socket, subprocess, time, webbrowser, threading
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from urllib.parse import quote

PID_FILE = os.path.join(os.path.expanduser("~"), ".city-game-serve.pid")
DEFAULT_PORT = 8080

# 用于身份验证的特征串，必须出现在目标进程的命令行中
PROCESS_IDENTITY = "serve.py"

# 全局标志，用于防止重复打开浏览器
_browser_opened = False


def is_our_process(pid):
    """
    通过 ps 命令检查指定 PID 的进程命令行是否包含 PROCESS_IDENTITY，
    防止 PID 被系统复用后误杀其他程序。
    """
    try:
        result = subprocess.run(
            ["ps", "-p", str(pid), "-o", "command="],
            capture_output=True, text=True, timeout=3
        )
        return PROCESS_IDENTITY in result.stdout
    except Exception:
        return False


def kill_previous_server():
    """
    安全终止上一次本脚本启动的进程：
    1. 读取 PID 文件（存储 pid:port）。
    2. 验证该 PID 的进程身份（命令行含 serve.py）。
    3. 验证通过才发送 SIGTERM；验证失败则放弃（不做任何操作）。
    返回旧进程使用的端口（供复用），验证失败或无旧进程返回 None。
    """
    if not os.path.exists(PID_FILE):
        return None

    old_port = None
    try:
        with open(PID_FILE) as f:
            parts = f.read().strip().split(":")
        old_pid = int(parts[0])
        old_port = int(parts[1]) if len(parts) > 1 else DEFAULT_PORT

        if not is_our_process(old_pid):
            # PID 已被系统分配给其他程序，绝对不能杀
            print(
                f"⚠️  PID {old_pid} 已不是本服务进程（可能已被其他程序复用），跳过终止。",
                flush=True
            )
            old_port = None  # 端口归属不明，放弃复用
        else:
            os.kill(old_pid, signal.SIGTERM)
            time.sleep(0.5)  # 等待端口释放
            print(f"🔄 已停止旧服务 (PID: {old_pid}, 端口: {old_port})", flush=True)

    except (ProcessLookupError, ValueError):
        pass  # 进程已自然退出，端口也已释放，可直接复用
    except PermissionError:
        print(f"⚠️  无权限终止旧服务 (PID 文件: {PID_FILE})，请手动关闭", flush=True)
        old_port = None
    finally:
        try:
            os.remove(PID_FILE)
        except OSError:
            pass

    return old_port


def try_bind_port(port):
    """尝试绑定指定端口，成功返回 True，失败返回 False（被其他程序占用）。"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("", port))
            return True
    except OSError:
        return False


def get_random_free_port():
    """让系统分配一个随机空闲端口（不指定任何端口，完全由 OS 决定）。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def resolve_port(preferred):
    """
    端口解析策略（不抢占、不顺延其他端口）：
    1. 优先尝试旧进程的端口（刚杀掉并等待释放）。
    2. 若不可用，尝试默认端口 8080。
    3. 若 8080 也被其他程序占用，让 OS 随机分配空闲端口（兜底，不抢占任何固定端口）。
    """
    if preferred and try_bind_port(preferred):
        return preferred
    if preferred != DEFAULT_PORT and try_bind_port(DEFAULT_PORT):
        return DEFAULT_PORT
    port = get_random_free_port()
    print(
        f"⚠️  8080 端口被其他程序占用，使用系统分配的临时端口 {port}（不影响其他项目）",
        flush=True
    )
    return port


def save_pid_port(pid, port):
    """将当前进程 PID 和端口写入 PID 文件，供下次启动时精确、安全地清理。"""
    try:
        with open(PID_FILE, "w") as f:
            f.write(f"{pid}:{port}")
    except OSError:
        pass


def remove_pid_file():
    """退出时删除 PID 文件，保持环境整洁。"""
    try:
        os.remove(PID_FILE)
    except OSError:
        pass


def open_browser_once(url):
    """
    安全地打开浏览器，确保只打开一个标签页。
    使用全局标志防止重复调用。
    """
    global _browser_opened
    if _browser_opened:
        return
    _browser_opened = True
    # new=1 表示在新标签页中打开，而不是新窗口
    webbrowser.open(url, new=1)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/serve.py <html文件路径>")
        sys.exit(1)

    # 安全检查：解析并验证文件路径，防止目录遍历攻击
    html_path = os.path.abspath(sys.argv[1])

    # 安全检查 1: 确保文件位于项目 outputs 目录内
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    allowed_dir = os.path.join(project_root, "outputs")

    # 路径规范化并检查是否在允许的目录内
    html_path = os.path.normpath(html_path)
    if not html_path.startswith(os.path.normpath(allowed_dir) + os.sep):
        print("错误：只能提供 outputs 目录内的 HTML 文件")
        print(f"允许目录：{allowed_dir}")
        print(f"请求文件：{html_path}")
        sys.exit(1)

    if not os.path.exists(html_path):
        print(f"文件不存在：{html_path}")
        sys.exit(1)

    # Step 1: 安全终止上一个本脚本进程（含身份验证），获取其端口供复用
    old_port = kill_previous_server()

    serve_dir = os.path.dirname(html_path)
    filename = os.path.basename(html_path)

    # Step 2: 解析最终端口（复用旧端口 → 8080 → OS 随机，全程不抢占其他端口）
    port = resolve_port(old_port if old_port else DEFAULT_PORT)
    url = f"http://localhost:{port}/{quote(filename)}"

    os.chdir(serve_dir)
    handler = SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None  # 静默日志

    server = TCPServer(("127.0.0.1", port), handler)

    # Step 3: 保存本次 PID + 端口，供下次精确、安全地清理
    save_pid_port(os.getpid(), port)

    # Step 4: 延迟 0.5 秒后自动打开浏览器（使用防重复函数）
    threading.Timer(0.5, lambda: open_browser_once(url)).start()

    print(f"🎮 游戏已启动: {url}", flush=True)
    print(f"📁 文件路径: {html_path}", flush=True)
    print(f"⏹️  按 Ctrl+C 停止服务", flush=True)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        remove_pid_file()
        print("\n服务已停止", flush=True)


if __name__ == "__main__":
    main()