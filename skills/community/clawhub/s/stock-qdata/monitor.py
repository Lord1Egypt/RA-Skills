import re
import time
import json
import os
import threading
import subprocess
from datetime import datetime, timedelta
from collections import deque
import sys
import webbrowser

# 尝试导入 psutil，用于检查进程
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("警告: psutil 模块未安装，将使用命令行检查进程")

# 全局变量，将在前端模式下初始化
app = None
socketio = None

# 导入 agent 模块（直接调用）
import agent

# 日志正则（匹配 my_log 的输出格式）
LOG_PATTERN = re.compile(
    r'\[SKILL: QMT-ASTOCK-DATA\] \[(?P<event>\w+)\]：\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+ (?P<message>.*)'
)

# 提取总数、已处理数的正则（从 "批次完成：123/456 (27%) - 本批：..." 中提取）
BATCH_COMPLETE_PATTERN = re.compile(
    r'批次完成：(\d+)/(\d+) \(\d+%\) - 本批：(.*)'
)

# 提取 total 的正则（从 "共需处理 456 个项目" 中提取）
TOTAL_PATTERN = re.compile(r'共需处理 (\d+) 个项目')

# 错误/警告信息中的股票代码提取（简单示例）
ERROR_STOCK_PATTERN = re.compile(r'[：:](\d{6}\.[A-Z]+)')

# -------------------- 配置 --------------------
config = agent.config
SPEED_WINDOW = 10

# -------------------- 全局状态 --------------------
state = {
    'status': 'idle',               # idle, running, paused, completed, error
    'progress': 0,
    'processed': 0,
    'total': 0,
    'current_stock': '',
    'elapsed_time_str': '00:00',
    'start_time_str': '',
    'success_count': 0,
    'error_count': 0,
    'download_speed': 0.0,
    'data_path': config.get('base_path', ''),
    'estimated_remaining_str': '--',
    'estimated_completion': '--',
    'last_update_str': '',
    'errors': [],
    'warnings': [],
}

state_lock = threading.Lock()
start_time = None
last_update_time = None
processed_history = deque(maxlen=SPEED_WINDOW)
current_batch = ""

# 定期广播控制
stop_event = threading.Event()

# 任务控制变量
download_thread = None
download_thread_lock = threading.Lock()
is_paused = False

# 空闲超时控制
last_activity_time = time.time()
idle_timeout_seconds = 300  # 5分钟
shutdown_event = threading.Event()

def update_activity_time():
    """更新最后活动时间戳"""
    global last_activity_time
    last_activity_time = time.time()

def check_idle_and_shutdown():
    """检查空闲条件，如果满足则关闭服务器"""
    global last_activity_time, shutdown_event
    
    # 如果已经触发了关闭事件，直接返回
    if shutdown_event.is_set():
        return
    
    current_time = time.time()
    idle_duration = current_time - last_activity_time
    
    # 获取当前状态
    with state_lock:
        current_status = state['status']
    
    # 获取活跃的Socket.IO客户端数量（仅在前端模式）
    active_clients = 0
    if socketio is not None:
        try:
            active_clients = len(socketio.server.manager.rooms.get('/', {}))
        except Exception:
            active_clients = 0
    
    # 检查下载线程是否在运行
    with download_thread_lock:
        download_active = download_thread is not None and download_thread.is_alive()
    
    # 空闲条件：
    # 1. 空闲时间超过阈值
    # 2. 系统状态为idle（没有运行中的下载任务）
    # 3. 没有活跃的Socket.IO客户端（网页已关闭）
    # 4. 没有下载线程在运行（双重检查）
    if (idle_duration >= idle_timeout_seconds and 
        current_status == 'idle' and 
        active_clients == 0 and
        not download_active):
        
        print(f"⚠️  服务器空闲超过 {idle_timeout_seconds} 秒，正在关闭...")
        print(f"   最后活动时间: {datetime.fromtimestamp(last_activity_time).strftime('%H:%M:%S')}")
        print(f"   当前状态: {current_status}")
        print(f"   活跃客户端: {active_clients}")
        print(f"   下载线程活跃: {download_active}")
        
        # 设置关闭事件，停止定期广播线程
        shutdown_event.set()
        stop_event.set()
        
        # 等待一小段时间让其他线程清理
        time.sleep(1)
        
        # 强制退出进程
        print("🛑 关闭 Flask 服务器进程")
        os._exit(0)

def idle_check_loop():
    """空闲检查循环，每30秒运行一次"""
    while not shutdown_event.is_set():
        check_idle_and_shutdown()
        time.sleep(30)

# -------------------- 日志回调函数 --------------------
def log_callback(event, message):
    """agent 调用的日志回调，实时更新状态并推送前端"""
    global start_time, last_update_time, current_batch

    now = datetime.now()
    # 调试日志：记录所有回调事件
    print(f"[DEBUG] log_callback: event={event}, message={message}")
    
    with state_lock:
        state['last_update_str'] = now.strftime('%H:%M:%S')

    # 根据事件类型更新状态
    if event == 'INFO':
        with state_lock:
            # 提取总数
            total_match = re.search(r'共需处理 (\d+) 个项目', message)
            if total_match and state['total'] == 0:
                state['total'] = int(total_match.group(1))

            # 提取批次完成信息
            batch_match = re.search(r'批次完成：(\d+)/(\d+) \(\d+%\) - 本批：(.*)', message)
            if batch_match:
                processed = int(batch_match.group(1))
                total = int(batch_match.group(2))
                batch_name = batch_match.group(3)
                state['processed'] = processed
                state['total'] = total
                state['progress'] = int(processed * 100 / total) if total else 0
                state['success_count'] = processed
                state['error_count'] = total - processed
                current_batch = batch_name
                state['current_stock'] = batch_name

                # 记录速度历史
                processed_history.append((now.timestamp(), processed))

    elif event == 'WARNING':
        with state_lock:
            warning_entry = {
                'time': now.strftime('%H:%M:%S'),
                'message': message,
                'stock': extract_stock_code(message)
            }
            state['warnings'].append(warning_entry)
            if len(state['warnings']) > 20:
                state['warnings'].pop(0)

    elif event == 'ERROR':
        with state_lock:
            error_entry = {
                'time': now.strftime('%H:%M:%S'),
                'message': message,
                'stock': extract_stock_code(message)
            }
            state['errors'].append(error_entry)
            if len(state['errors']) > 20:
                state['errors'].pop(0)
        # 发送错误弹窗（仅在前端模式）
        if socketio is not None:
            try:
                socketio.emit('missing_file', {'message': f"错误: {message}"})
            except Exception:
                pass
        broadcast_state()
        return

    elif event == 'PROGRESS':
        # 提取进度百分比
        progress_match = re.search(r'股票数据下载进度：(\d+)%', message)
        if not progress_match and message.strip().isdigit():
            progress_match = re.match(r'(\d+)', message.strip())

        count_match = re.search(r'已处理：(\d+)/(\d+)', message)
        batch_match = re.search(r'本批次：(.+?)(?:\||$)', message)
        
        with state_lock:
            if progress_match:
                state['progress'] = int(progress_match.group(1))
            if count_match:
                state['processed'] = int(count_match.group(1))
                state['total'] = int(count_match.group(2))
            if batch_match:
                state['current_stock'] = batch_match.group(1).strip()

        update_time_metrics()
        broadcast_state()
        return

    elif event == 'MISSING_FILE':
        # 记录错误日志并发送到前端弹窗
        error_entry = {
            'time': now.strftime('%H:%M:%S'),
            'message': f"缺失文件: {message}",
            'stock': extract_stock_code(message)
        }
        with state_lock:
            state['errors'].append(error_entry)
            if len(state['errors']) > 20:
                state['errors'].pop(0)
            # 重置状态
            state['status'] = 'idle'
            state['progress'] = 0
            state['processed'] = 0
            state['total'] = 0
            state['current_stock'] = ''
            state['download_speed'] = 0.0
            state['estimated_remaining_str'] = '--'
            state['estimated_completion'] = '--'
            processed_history.clear()
        # 发送缺失文件事件到前端弹窗（仅在前端模式）
        if socketio is not None:
            try:
                socketio.emit('missing_file', {'message': message})
            except Exception as e:
                print(f"[WARNING] 发送missing_file事件失败: {e}")
        broadcast_state()
        return

    elif event == 'FINAL':
        # 任务完成，重置状态
        with state_lock:
            state['status'] = 'idle'
        # 停止速度计算
        update_time_metrics()
        broadcast_state()
        return

    # 更新时间指标并广播
    update_time_metrics()
    broadcast_state()

def is_qmt_running():
    """真实检查 XtMiniQmt.exe 进程"""
    if PSUTIL_AVAILABLE:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] == 'XtMiniQmt.exe':
                return True
    else:
        # 使用 tasklist 命令
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq XtMiniQmt.exe'],
                                capture_output=True, text=True)
        if 'XtMiniQmt.exe' in result.stdout:
            return True
    return False

def start_qmt():
    """实际启动 XtMiniQmt.exe"""
    # 假设 QMT 安装路径在配置中或固定
    qmt_path = r"C:\Program Files\XtMiniQmt\XtMiniQmt.exe"  # 需根据实际路径配置
    try:
        subprocess.Popen([qmt_path], shell=True)
        print(f"[QMT] 已启动: {qmt_path}")
    except Exception as e:
        print(f"[ERROR] 启动 QMT 失败: {e}")
        sys.exit(1)

def start_qmt():
    """
    启动 XtMiniQmt.exe - 快速启动版本
    """
    # 读取配置
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except Exception as e:
        print(f"[QMT] 读取配置文件失败: {e}")
        raise
    
    qmt_path = config_data.get('qmt_path', '')
    if not qmt_path:
        raise ValueError("config.json 中缺少 qmt_path 字段")
    
    # 构建完整路径
    exe_path = os.path.join(qmt_path, 'XtMiniQmt.exe')
    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"未找到 XtMiniQmt.exe: {exe_path}")
    
    print(f"[QMT] 正在启动: {exe_path}")
    try:
        # 使用 subprocess 启动，不等待完成
        subprocess.Popen(
            [exe_path],
            cwd=qmt_path,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("[QMT] 启动命令已发送，等待2秒让进程初始化...")
        time.sleep(2)  # 等待进程启动
    except Exception as e:
        print(f"[QMT] 启动失败: {e}")
        raise

def extract_stock_code(text):
    match = re.search(r'[：:](\d{6}\.[A-Z]+)', text)
    return match.group(1) if match else None

def update_time_metrics():
    global start_time
    now = datetime.now()
    with state_lock:
        if start_time:
            elapsed = now - start_time
            state['elapsed_time_str'] = str(elapsed).split('.')[0]

            # 计算速度
            if len(processed_history) >= 2:
                oldest_time, oldest_processed = processed_history[0]
                newest_time, newest_processed = processed_history[-1]
                time_diff = newest_time - oldest_time
                if time_diff > 0:
                    speed = (newest_processed - oldest_processed) / time_diff
                    state['download_speed'] = round(speed, 2)

            # 估算剩余时间
            if state['download_speed'] > 0 and state['total'] > state['processed']:
                remaining = (state['total'] - state['processed']) / state['download_speed']
                state['estimated_remaining_str'] = str(timedelta(seconds=int(remaining)))
                finish_time = now + timedelta(seconds=remaining)
                state['estimated_completion'] = finish_time.strftime('%H:%M:%S')
            else:
                state['estimated_remaining_str'] = '--'
                state['estimated_completion'] = '--'

def broadcast_state():
    # 如果socketio未初始化（backend模式），直接返回
    if socketio is None:
        return
    
    with state_lock:
        # 创建状态的浅拷贝，避免在发送过程中状态被修改
        state_copy = state.copy()
        # 注意：errors 和 warnings 是列表，也需要拷贝
        state_copy['errors'] = state['errors'].copy()
        state_copy['warnings'] = state['warnings'].copy()
    # 调试日志
    print(f"[DEBUG] broadcast_state: status={state_copy['status']}, progress={state_copy['progress']}, processed={state_copy['processed']}/{state_copy['total']}")
    
    # 获取当前连接的客户端数量
    try:
        # 尝试获取活跃的Socket.IO客户端数量
        active_clients = len(socketio.server.manager.rooms.get('/', {}))
        print(f"[DEBUG] Active Socket.IO clients: {active_clients}")
    except Exception as e:
        print(f"[DEBUG] Could not get client count: {e}")
        active_clients = "unknown"
    
    # 发送状态更新，带回调检查是否成功
    def emit_callback(success):
        if success:
            print(f"[DEBUG] Socket.IO emit successful to {active_clients} client(s)")
        else:
            print(f"[WARNING] Socket.IO emit may have failed")
    
    try:
        # 确保在Flask应用上下文中执行emit
        socketio.emit('state_update', {'type': 'full', 'state': state_copy}, callback=emit_callback)
    except Exception as e:
        print(f"[ERROR] Socket.IO emit failed: {e}")
        # 尝试在应用上下文中重试
        try:
            with app.app_context():
                socketio.emit('state_update', {'type': 'full', 'state': state_copy})
                print(f"[DEBUG] Socket.IO emit retried with app context")
        except Exception as e2:
            print(f"[ERROR] Socket.IO emit with app context also failed: {e2}")
    return

# 测试端点：手动触发状态广播

# -------------------- 主程序入口 --------------------
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='股票数据下载监控服务器')
    parser.add_argument('--host', default='127.0.0.1', help='Web服务器主机地址（默认：127.0.0.1）')
    parser.add_argument('--port', type=int, default=5000, help='Web服务器端口（默认：5000）')
    parser.add_argument('--mode', choices=['frontend', 'backend'], default='frontend',
                        help='运行模式：frontend=启动Web监控，backend=直接执行下载并退出')
    # 下载参数（用于设置默认值）
    parser.add_argument('--period', type=str, default=None, 
                        help='数据周期（默认：从config.json读取）')
    parser.add_argument('--days', type=int, default=None,
                        help='回溯天数（默认：从config.json读取）')
    parser.add_argument('--batch_size', type=int, default=None,
                        help='每批处理数量（默认：从config.json读取）')
    args = parser.parse_args()
    
    # 检查并启动 QMT（所有模式都需要）
    # 确保 QMT 运行（所有模式）
    if not is_qmt_running():
        print("QMT 未运行，尝试启动...")
        start_qmt()
        # 等待几秒确保启动
        time.sleep(1)
    else:
        print("QMT 已在运行")

    # 如果提供了命令行参数，更新config.json
    config_changed = False
    if args.period is not None or args.days is not None or args.batch_size is not None:
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    current_config = json.load(f)
            else:
                current_config = {}
                
            if args.period is not None:
                current_config['download_period'] = args.period
                config_changed = True
            if args.days is not None:
                current_config['download_days'] = args.days
                config_changed = True
            if args.batch_size is not None:
                current_config['batch_size'] = args.batch_size
                config_changed = True
                
            if config_changed:
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(current_config, f, indent=2, ensure_ascii=False)
                print(f"✅ 配置文件已更新")
                # 重新加载配置到 agent 模块
                import importlib
                importlib.reload(agent)
        except Exception as e:
            print(f"⚠️  更新配置文件失败: {e}")

    if args.mode == 'backend':
        # 后端模式：直接执行下载，不启动 Web 服务器
        print("后端模式：开始下载任务...")
        agent.set_log_callback(lambda event, msg: print(f"[{event}] {msg}"))
        
        # 从config.json获取参数（可能已被命令行参数更新）
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                period = config_data.get('download_period', '1d')
                days = config_data.get('download_days', 500)
                batch_size = config_data.get('batch_size', 50)
                print(f"📊 使用参数: 周期={period}, 天数={days}, 批次大小={batch_size}")
                agent.download_all_data(period=period, days=days, batch_size=batch_size)
            else:
                print("⚠️  配置文件不存在，使用默认参数")
                agent.download_all_data()
        except Exception as e:
            print(f"⚠️  读取配置失败: {e}，使用默认参数")
            agent.download_all_data()
            
        print("下载任务结束，退出。")
        sys.exit(0)

    # ==================== 前端模式：启动Web服务器 ====================
    # 条件导入Web框架（仅在前端模式导入）
    print("前端模式：正在加载Web框架...")
    from flask import Flask, request, jsonify
    from flask_socketio import SocketIO
    
    # -------------------- Flask & SocketIO 初始化 --------------------
    import os
    static_folder_path = os.path.join(os.path.dirname(__file__), 'static')
    app = Flask(__name__, static_folder=static_folder_path, static_url_path='/static')
    app.config['SECRET_KEY'] = 'secret!'
    # 优化Socket.IO配置：禁用调试日志，减少启动开销
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",
        logger=False,           # 禁用Socket.IO日志
        engineio_logger=False,  # 禁用Engine.IO日志
        ping_timeout=60,
        ping_interval=25,
        max_http_buffer_size=1e8,
        async_mode='threading',
        allow_upgrades=True,
        transports=['websocket', 'polling'],
        http_compression=False
    )
    
    # -------------------- Web路由和事件处理 --------------------
    # 这些函数只有在frontend模式下才需要定义
    @app.route('/')
    def index():
        from flask import send_from_directory
        templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
        return send_from_directory(templates_dir, 'index.html')

    @app.route('/webfonts/<path:filename>')
    def serve_webfonts(filename):
        from flask import send_from_directory
        webfonts_dir = os.path.join(os.path.dirname(__file__), 'webfonts')
        return send_from_directory(webfonts_dir, filename)

    @app.route('/api/state')
    def get_state():
        with state_lock:
            return jsonify(state)

    @app.route('/api/config')
    def get_config():
        return jsonify({
            'batch_size': config.get('batch_size', 50),
            'download_period': config.get('download_period', '1d'),
            'download_days': config.get('download_days', 500),
            'host': config.get('host', '127.0.0.1'),
            'port': config.get('port', 5000),
            'base_path': config.get('base_path', 'c:\\data\\')
        })

    @app.route('/api/start', methods=['POST'])
    def start_download():
        global download_thread, start_time, is_paused, processed_history
        update_activity_time()

        with download_thread_lock:
            if download_thread and download_thread.is_alive():
                return jsonify({'error': '已有任务在运行中'}), 400

        data = request.get_json()
        period = data.get('period', '1d')
        days = data.get('days', 500)
        batch_size = data.get('batch_size', None)

        if days <= 0 or days > 9999:
            return jsonify({'error': '下载天数必须在1-9999之间'}), 400
        if batch_size and (batch_size <= 0 or batch_size > 1000):
            return jsonify({'error': '批次大小必须在1-1000之间'}), 400

        if batch_size is None:
            batch_size = config.get('batch_size', 50)

        # 保存配置到 config.json
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    current_config = json.load(f)
            else:
                current_config = {}
            current_config['download_period'] = period
            current_config['download_days'] = days
            current_config['batch_size'] = batch_size
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(current_config, f, indent=2, ensure_ascii=False)
            # 重新加载配置到 agent 模块
            import importlib
            importlib.reload(agent)
        except Exception as e:
            print(f"保存配置失败: {e}")

        # 重置全局变量
        with state_lock:
            start_time = datetime.now()
            state.update({
                'status': 'running',
                'progress': 0,
                'processed': 0,
                'total': 0,
                'current_stock': '',
                'elapsed_time_str': '00:00',
                'start_time_str': start_time.strftime('%H:%M:%S'),
                'success_count': 0,
                'error_count': 0,
                'download_speed': 0.0,
                'estimated_remaining_str': '--',
                'estimated_completion': '--',
                'last_update_str': start_time.strftime('%H:%M:%S'),
                'errors': [],
                'warnings': [],
            })
            processed_history.clear()
        is_paused = False
        broadcast_state()

        # 设置 agent 的回调
        agent.set_log_callback(log_callback)
        # 清除 agent 的控制标志
        agent.clear_stop()
        agent.clear_pause()

        # 启动下载线程
        def run_download():
            try:
                agent.download_all_data(period=period, days=days, batch_size=batch_size)
            except Exception as e:
                print(f"下载任务异常: {e}")
                with state_lock:
                    state['status'] = 'error'
                    broadcast_state()
            finally:
                # 任务结束，重置状态
                with state_lock:
                    state['status'] = 'idle'
                broadcast_state()
                with download_thread_lock:
                    global download_thread
                    download_thread = None

        download_thread = threading.Thread(target=run_download, daemon=True)
        download_thread.start()

        return jsonify({
            'message': f'下载任务已开始 (周期: {period}, 天数: {days}, 批次: {batch_size})',
            'period': period,
            'days': days,
            'batch_size': batch_size
        })

    @app.route('/api/pause', methods=['POST'])
    def pause_download():
        global is_paused
        update_activity_time()
        with download_thread_lock:
            if not download_thread or not download_thread.is_alive():
                return jsonify({'error': '没有运行中的任务可暂停'}), 400
            if is_paused:
                return jsonify({'error': '任务已暂停'}), 400

        agent.set_pause()
        is_paused = True
        with state_lock:
            state['status'] = 'paused'
            state['download_speed'] = 0.0
            state['estimated_remaining_str'] = '--'
            state['estimated_completion'] = '--'
        broadcast_state()
        return jsonify({'message': '下载任务已暂停'})

    @app.route('/api/resume', methods=['POST'])
    def resume_download():
        global is_paused
        update_activity_time()
        if not is_paused:
            return jsonify({'error': '任务未暂停'}), 400

        agent.clear_pause()
        is_paused = False
        with state_lock:
            state['status'] = 'running'
        broadcast_state()
        return jsonify({'message': '下载任务已恢复'})

    @app.route('/api/reset')
    def reset_state():
        global start_time, processed_history, current_batch
        update_activity_time()
        with state_lock:
            state.update({
                'status': 'idle',
                'progress': 0,
                'processed': 0,
                'total': 0,
                'current_stock': '',
                'elapsed_time_str': '00:00',
                'start_time_str': '',
                'success_count': 0,
                'error_count': 0,
                'download_speed': 0.0,
                'estimated_remaining_str': '--',
                'estimated_completion': '--',
                'last_update_str': '',
                'errors': [],
                'warnings': [],
            })
            start_time = None
            processed_history.clear()
            current_batch = ""
        return jsonify({'status': 'reset'})

    @app.route('/api/stop', methods=['POST'])
    def stop_download():
        global download_thread, start_time, is_paused, processed_history
        update_activity_time()

        with download_thread_lock:
            if not download_thread or not download_thread.is_alive():
                return jsonify({'error': '没有运行中的任务可停止'}), 400

        agent.set_stop()
        # 等待线程结束，最多3秒
        download_thread.join(timeout=3)
        if download_thread.is_alive():
            print("警告：停止线程超时，强制清理引用")
            # 仍然重置引用，避免阻塞新任务
            download_thread = None

        # 无论线程是否结束，重置状态
        is_paused = False
        with state_lock:
            state.update({
                'status': 'idle',
                'progress': 0,
                'processed': 0,
                'total': 0,
                'current_stock': '',
                'elapsed_time_str': '00:00',
                'start_time_str': '',
                'success_count': 0,
                'error_count': 0,
                'download_speed': 0.0,
                'estimated_remaining_str': '--',
                'estimated_completion': '--',
                'last_update_str': datetime.now().strftime('%H:%M:%S'),
            })
            processed_history.clear()
            start_time = None
        broadcast_state()
        return jsonify({'message': '下载任务已停止'})

    @socketio.on('connect')
    def handle_connect():
        update_activity_time()
        client_id = request.sid
        print(f'[DEBUG] Client connected: {client_id}')
        print(f'[DEBUG] Total connected clients: {len(socketio.server.manager.rooms.get("/", {}))}')
        with state_lock:
            socketio.emit('state_update', {'type': 'full', 'state': state})

    @socketio.on('disconnect')
    def handle_disconnect():
        client_id = request.sid
        print(f'[DEBUG] Client disconnected: {client_id}')
        print(f'[DEBUG] Remaining connected clients: {len(socketio.server.manager.rooms.get("/", {}))}')

    @socketio.on('test_ping')
    def handle_test_ping(data):
        update_activity_time()
        client_id = request.sid
        print(f'[DEBUG] Received test_ping from client {client_id}: {data}')
        # 回复 pong
        socketio.emit('test_pong', {
            'received': data,
            'timestamp': datetime.now().isoformat(),
            'server_time': datetime.now().strftime('%H:%M:%S')
        }, room=client_id)

    # 测试端点：手动触发状态广播
    @app.route('/api/test_broadcast')
    def test_broadcast():
        update_activity_time()
        print(f'[DEBUG] Manual broadcast triggered')
        broadcast_state()
        return jsonify({'message': 'Broadcast triggered', 'clients': len(socketio.server.manager.rooms.get("/", {}))})

    # -------------------- 前端模式启动流程 --------------------
    with state_lock:
        state['data_path'] = agent.BASE_PATH
    print(f"🚀 启动股票数据下载监控服务器")
    print(f"🌐 访问地址: http://{args.host}:{args.port}")
    print(f"📊 监控页面: http://{args.host}:{args.port}/")
    print(f"📈 数据路径: {agent.BASE_PATH}")
    print("="*60)
    print("💡 提示: 服务器已启动，等待前端控制命令...")
    print("="*60)

    # 自动打开浏览器（仅在非重载器子进程中打开，避免Flask调试模式打开两次）
    try:
        import webbrowser
        import os

        # 在启动服务器前启动一个线程延迟打开浏览器
        if not os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            def open_browser():
                time.sleep(2)
                webbrowser.open(f"http://{args.host}:{args.port}")
            threading.Thread(target=open_browser, daemon=True).start()
            print(f"🌐 已自动打开浏览器访问监控页面")
    except Exception as e:
        print(f"⚠️  无法自动打开浏览器: {e}")

    # 启动定期状态广播线程（每2秒广播一次，确保前端实时更新）
    def periodic_broadcast():
        if not stop_event.is_set():
            broadcast_state()
            threading.Timer(2.0, periodic_broadcast).start()
    
    periodic_broadcast()
    print("🔄 定期状态广播已启动（每2秒）")

    # 启动空闲检查线程（每30秒检查一次，5分钟无活动则关闭服务器）
    idle_check_thread = threading.Thread(target=idle_check_loop, daemon=True)
    idle_check_thread.start()
    print("⏱️  空闲检查线程已启动（5分钟超时）")

    # Socket.IO配置信息（已禁用日志）
    print(f"[CONFIG] Socket.IO 配置: ping_timeout=60, ping_interval=25, transports=['websocket', 'polling']")
    print(f"[CONFIG] 已禁用Socket.IO和Engine.IO日志以提升性能")
    
    # 启动Flask服务器
    print("[FLASK] 正在启动Flask服务器...")
    try:
        socketio.run(app, 
                     host=args.host, 
                     port=args.port, 
                     debug=False,
                     allow_unsafe_werkzeug=True,
                     log_output=False)  # 禁用Flask日志输出
    except Exception as e:
        print(f"[FLASK ERROR] Flask启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)