import os
import json
import subprocess
from flask import Flask, render_template_string, jsonify, send_from_directory, request

app = Flask(__name__)
WORKSPACE = os.path.expanduser("~/.openclaw/workspace/memory/wechat_skill")
STATUS_FILE = os.path.join(WORKSPACE, "dashboard_status.json")

monitor_process = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WeChat Auto-Reply Dashboard V2</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f4f5f7; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; color: #2c3e50; }
        
        /* Control Panel */
        .control-panel { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px; display: flex; flex-wrap: wrap; gap: 15px; align-items: center; }
        .control-group { display: flex; flex-direction: column; flex-grow: 1; }
        .control-group label { font-weight: bold; margin-bottom: 5px; font-size: 0.9em; }
        .control-group input { padding: 8px; border: 1px solid #ccc; border-radius: 5px; font-size: 1em; }
        .btn { padding: 10px 20px; border: none; border-radius: 5px; font-size: 1em; font-weight: bold; cursor: pointer; transition: 0.3s; color: white; }
        .btn-start { background-color: #2ecc71; }
        .btn-start:hover { background-color: #27ae60; }
        .btn-start:disabled { background-color: #95a5a6; cursor: not-allowed; }
        .btn-stop { background-color: #e74c3c; }
        .btn-stop:hover { background-color: #c0392b; }
        .btn-stop:disabled { background-color: #95a5a6; cursor: not-allowed; }
        .daemon-status { font-weight: bold; padding: 5px 10px; border-radius: 5px; }
        .daemon-running { background-color: #d5f5e3; color: #27ae60; }
        .daemon-stopped { background-color: #fadbd8; color: #c0392b; }

        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
        .card { background: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); position: relative; display: flex; flex-direction: column;}
        .status-indicator { position: absolute; top: 20px; right: 20px; width: 15px; height: 15px; border-radius: 50%; }
        .online { background-color: #2ecc71; box-shadow: 0 0 8px #2ecc71; }
        .error { background-color: #e74c3c; box-shadow: 0 0 8px #e74c3c; }
        .checking { background-color: #f39c12; box-shadow: 0 0 8px #f39c12; }
        
        .target-name { font-size: 1.3em; font-weight: bold; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;}
        .info { font-size: 0.9em; color: #666; margin-bottom: 5px; }
        .error-msg { color: #e74c3c; font-size: 0.85em; margin-top: 10px; background: #fadbd8; padding: 5px; border-radius: 5px;}
        
        .chat-preview { margin-top:15px; background: #f9f9f9; padding: 10px; border-radius: 8px; flex-grow: 1; min-height: 150px; max-height: 250px; overflow-y: auto; border: 1px solid #eee; }
        .chat-bubble { background: #e5e5ea; padding: 8px 12px; border-radius: 15px; display: inline-block; margin-bottom: 8px; max-width: 90%; font-size: 0.95em; line-height: 1.4; clear: both; float: left; }
        .chat-bubble.self { background: #007aff; color: white; float: right; }
        
        .img-preview { width: 100%; border-radius: 5px; margin-top: 15px; border: 1px solid #ddd; object-fit: cover; max-height: 150px;}
        
        .log-container { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 10px; margin-top: 30px; height: 250px; overflow-y: auto; font-family: monospace; font-size: 0.9em; }
        
        .btn-history { background: #3498db; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; font-size: 0.8em; }
        .btn-history:hover { background: #2980b9; }

        /* Modal Styles */
        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; overflow: auto; background-color: rgba(0,0,0,0.5); }
        .modal-content { background-color: #fff; margin: 5% auto; padding: 20px; border-radius: 10px; width: 80%; max-width: 800px; max-height: 80vh; display: flex; flex-direction: column;}
        .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
        .close:hover { color: black; }
        .modal-body { overflow-y: auto; flex-grow: 1; padding: 10px; background: #f9f9f9; border-radius: 8px; margin-top: 15px; }
    </style>
    <script>
        let isRunning = false;

        function checkDaemonStatus() {
            fetch('/api/daemon_status')
                .then(r => r.json())
                .then(data => {
                    isRunning = data.running;
                    document.getElementById('btn-start').disabled = isRunning;
                    document.getElementById('btn-stop').disabled = !isRunning;
                    const statusEl = document.getElementById('daemon-status-text');
                    if (isRunning) {
                        statusEl.className = 'daemon-status daemon-running';
                        statusEl.innerText = '🟢 监听中 (Running)';
                    } else {
                        statusEl.className = 'daemon-status daemon-stopped';
                        statusEl.innerText = '🔴 已停止 (Stopped)';
                    }
                });
        }

        function startDaemon() {
            const targets = document.getElementById('input-targets').value;
            const apikey = document.getElementById('input-apikey').value;
            fetch('/api/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ targets: targets, apikey: apikey })
            }).then(r => r.json()).then(data => { checkDaemonStatus(); fetchStatus(); });
        }

        function stopDaemon() {
            fetch('/api/stop', { method: 'POST' })
                .then(r => r.json()).then(data => { checkDaemonStatus(); });
        }

        function showHistory(target) {
            fetch(`/api/history/${target}`)
                .then(r => r.json())
                .then(data => {
                    const modal = document.getElementById('historyModal');
                    const title = document.getElementById('modal-title');
                    const body = document.getElementById('modal-body');
                    title.innerText = `📜 ${target} 的全部聊天记录 (Memory Bank)`;
                    body.innerHTML = '';
                    if (data.history && data.history.length > 0) {
                        data.history.forEach(msg => {
                            const isSelf = msg.startsWith('Self:');
                            const text = msg.replace(/^(Self:|Other:)\\s*/, '');
                            const cssClass = isSelf ? 'chat-bubble self' : 'chat-bubble';
                            body.innerHTML += `<div class="${cssClass}">${text}</div><div style="clear:both;"></div>`;
                        });
                    } else {
                        body.innerHTML = '<div style="text-align:center; color:#999; margin-top:20px;">暂无历史记录</div>';
                    }
                    modal.style.display = "block";
                    // scroll to bottom
                    body.scrollTop = body.scrollHeight;
                });
        }

        function closeModal() {
            document.getElementById('historyModal').style.display = "none";
        }

        window.onclick = function(event) {
            const modal = document.getElementById('historyModal');
            if (event.target == modal) { modal.style.display = "none"; }
        }

        function fetchStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const grid = document.getElementById('grid');
                    grid.innerHTML = '';
                    
                    if (data.targets) {
                        for (const [target, info] of Object.entries(data.targets)) {
                            if (target === 'System') continue; // Skip system internal card
                            
                            let statusClass = info.status === 'error' ? 'error' : (info.status === 'checking' ? 'checking' : 'online');
                            let errorHtml = info.last_error ? `<div class="error-msg">⚠️ ${info.last_error}</div>` : '';
                            
                            let chatHtml = '<div class="chat-preview">';
                            if (info.last_messages && info.last_messages.length > 0) {
                                info.last_messages.forEach(msg => {
                                    chatHtml += `<div class="chat-bubble">${msg.replace('Other:', '')}</div>`;
                                });
                            }
                            if (info.last_reply) {
                                chatHtml += `<div class="chat-bubble self">${info.last_reply}</div>`;
                            }
                            chatHtml += '<div style="clear:both;"></div></div>';

                            let imgHtml = info.image_path ? `<img src="/images/${info.image_path}?t=${new Date().getTime()}" class="img-preview" />` : '';

                            grid.innerHTML += `
                                <div class="card">
                                    <div class="status-indicator ${statusClass}"></div>
                                    <div class="target-name">
                                        <span>👤 ${target}</span>
                                        <button class="btn-history" onclick="showHistory('${target}')">全部记录</button>
                                    </div>
                                    <div class="info">🕒 Last Check: ${info.last_check_time || 'N/A'}</div>
                                    ${errorHtml}
                                    ${chatHtml}
                                    ${imgHtml}
                                </div>
                            `;
                        }
                    }
                    
                    const logs = document.getElementById('logs');
                    const isScrolledToBottom = logs.scrollHeight - logs.clientHeight <= logs.scrollTop + 1;
                    
                    logs.innerHTML = '';
                    if (data.global_logs) {
                        data.global_logs.slice().reverse().forEach(log => {
                            let color = log.includes('ERROR') ? '#e74c3c' : (log.includes('WARNING') ? '#f39c12' : '#ecf0f1');
                            logs.innerHTML += `<div style="color: ${color}; margin-bottom: 4px;">${log}</div>`;
                        });
                    }
                });
        }
        
        setInterval(() => {
            checkDaemonStatus();
            fetchStatus();
        }, 5000);
        
        window.onload = () => {
            checkDaemonStatus();
            fetchStatus();
        };
    </script>
</head>
<body>
    <div class="container">
        <h1>🤖 WeChat AI Dashboard V2</h1>
        
        <div class="control-panel">
            <div class="control-group" style="flex: 2;">
                <label for="input-targets">🎯 监听名单 (英文逗号分隔):</label>
                <input type="text" id="input-targets" value="">
            </div>
            <div class="control-group" style="flex: 2;">
                <label for="input-apikey">🔑 Gemini API Key:</label>
                <input type="password" id="input-apikey" placeholder="AIzaSy...">
            </div>
            <div class="control-group" style="flex: 1; align-items: center; flex-direction: row; gap: 15px; padding-top: 20px;">
                <button id="btn-start" class="btn btn-start" onclick="startDaemon()">▶️ 启动监听</button>
                <button id="btn-stop" class="btn btn-stop" onclick="stopDaemon()">⏹ 停止监听</button>
                <span id="daemon-status-text" class="daemon-status daemon-stopped">🔴 已停止 (Stopped)</span>
            </div>
        </div>

        <div class="grid" id="grid">
            <!-- Cards will be injected here -->
        </div>
        
        <div class="log-container" id="logs">
            <!-- Logs will be injected here -->
        </div>
    </div>

    <!-- History Modal -->
    <div id="historyModal" class="modal">
        <div class="modal-content">
            <div>
                <span class="close" onclick="closeModal()">&times;</span>
                <h2 id="modal-title" style="margin-top: 0;">聊天记录</h2>
            </div>
            <div class="modal-body" id="modal-body">
                <!-- Full history injected here -->
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                return jsonify(json.load(f))
        except:
            pass
    return jsonify({"targets": {}, "global_logs": ["No status file found yet."]})

@app.route('/api/daemon_status')
def get_daemon_status():
    global monitor_process
    # Double check via process list just in case
    check = subprocess.run("pgrep -f wechat-auto-reply/monitor_main.py", shell=True, capture_output=True)
    is_running = check.returncode == 0
    return jsonify({"running": is_running})

@app.route('/api/start', methods=['POST'])
def start_daemon():
    global monitor_process
    data = request.json
    targets = data.get('targets', '')
    apikey = data.get('apikey', '')
    persona = "回复要简短、干脆，不带句号，用词口语化，像哥们一样聊天，语气轻松。"
    
    # Kill any existing instances
    os.system("pkill -9 -f wechat-auto-reply/monitor_main.py")
    
    script_path = os.path.expanduser("~/.openclaw/workspace/skills/wechat-auto-reply/monitor_main.py")
    cmd = ["python3", script_path, "--targets", targets, "--persona", persona, "--interval", "60"]
    
    env = os.environ.copy()
    if apikey:
        env["GEMINI_API_KEY"] = apikey
    
    monitor_process = subprocess.Popen(cmd, env=env)
    return jsonify({"status": "started", "targets": targets})

@app.route('/api/stop', methods=['POST'])
def stop_daemon():
    global monitor_process
    os.system("pkill -9 -f wechat-auto-reply/monitor_main.py")
    if monitor_process:
        try:
            monitor_process.terminate()
        except:
            pass
        monitor_process = None
    return jsonify({"status": "stopped"})

@app.route('/api/history/<target>')
def get_history(target):
    json_file = os.path.join(WORKSPACE, f"last_parsed_{target.replace(' ', '_')}.json")
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return jsonify({"history": data.get("accumulated_history", [])})
        except:
            pass
    return jsonify({"history": []})

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(WORKSPACE, filename)

if __name__ == '__main__':
    print("🚀 Starting Web Dashboard V2 on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
