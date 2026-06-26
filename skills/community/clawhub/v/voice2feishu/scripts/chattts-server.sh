#!/bin/bash
# ChatTTS 服务器管理
# 用法: chattts-server.sh start|stop|status

set -e

CHATTTS_URL="${CHATTTS_URL:-http://localhost:8080}"
PID_FILE="/tmp/chattts-server.pid"
LOG_FILE="/tmp/chattts-server.log"
PORT="${CHATTTS_PORT:-8080}"

start_server() {
  # 检查是否已运行
  if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
      echo "✅ ChatTTS 服务已在运行 (PID: $PID)"
      return 0
    fi
    rm -f "$PID_FILE"
  fi
  
  echo "🚀 启动 ChatTTS 服务..."
  echo "   端口: $PORT"
  echo "   日志: $LOG_FILE"
  echo ""
  
  # 创建简单的 ChatTTS Flask 服务
  cat > /tmp/chattts_server.py << 'PYEOF'
#!/usr/bin/env python3
"""简单的 ChatTTS HTTP 服务"""

import os
import sys
import json
import tempfile
from flask import Flask, request, send_file
from flask_cors import CORS

try:
    import ChatTTS
    import torch
except ImportError:
    print("❌ 请先安装 ChatTTS: pip install ChatTTS torch")
    sys.exit(1)

app = Flask(__name__)
CORS(app)

# 初始化 ChatTTS
print("🔄 初始化 ChatTTS...")
chat = ChatTTS.Chat()
chat.load(compile=False)  # compile=True 在某些平台可能有问题
print("✅ ChatTTS 初始化完成")

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok'}

@app.route('/tts', methods=['POST'])
def tts():
    data = request.get_json()
    text = data.get('text', '')
    seed = data.get('seed', 500)
    
    if not text:
        return {'error': '缺少 text 参数'}, 400
    
    # 设置随机种子
    torch.manual_seed(seed)
    
    # 生成语音
    try:
        wavs = chat.infer([text], use_decoder=True)
        wav = wavs[0]
    except Exception as e:
        return {'error': f'生成失败: {str(e)}'}, 500
    
    # 保存为临时文件
    import torchaudio
    import numpy as np
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name
    
    # 转换并保存
    if isinstance(wav, np.ndarray):
        wav_tensor = torch.from_numpy(wav)
    else:
        wav_tensor = wav
    
    torchaudio.save(temp_path, wav_tensor.unsqueeze(0) if wav_tensor.dim() == 1 else wav_tensor, 24000)
    
    return send_file(temp_path, mimetype='audio/wav')

if __name__ == '__main__':
    port = int(os.environ.get('CHATTTS_PORT', 8080))
    print(f"🎧 ChatTTS 服务启动在端口 {port}")
    app.run(host='0.0.0.0', port=port)
PYEOF
  
  # 后台启动
  nohup python3 /tmp/chattts_server.py > "$LOG_FILE" 2>&1 &
  echo $! > "$PID_FILE"
  
  echo "⏳ 等待服务启动..."
  sleep 5
  
  # 检查是否成功
  if curl -s --connect-timeout 3 "$CHATTTS_URL/health" > /dev/null 2>&1; then
    PID=$(cat "$PID_FILE")
    echo "✅ ChatTTS 服务启动成功 (PID: $PID)"
    echo "   地址: $CHATTTS_URL"
  else
    echo "⚠️  服务可能启动较慢，请稍后检查状态"
    echo "   查看日志: tail -f $LOG_FILE"
  fi
}

stop_server() {
  if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
      echo "🛑 停止 ChatTTS 服务 (PID: $PID)..."
      kill "$PID"
      rm -f "$PID_FILE"
      echo "✅ 服务已停止"
    else
      echo "⚠️  服务未运行（PID 文件存在但进程不存在）"
      rm -f "$PID_FILE"
    fi
  else
    echo "⚠️  服务未运行（无 PID 文件）"
  fi
}

status_server() {
  if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
      echo "✅ ChatTTS 服务运行中 (PID: $PID)"
      echo "   地址: $CHATTTS_URL"
      
      # 检查健康状态
      if curl -s --connect-timeout 2 "$CHATTTS_URL/health" > /dev/null 2>&1; then
        echo "   状态: 健康"
      else
        echo "   状态: 无响应"
      fi
    else
      echo "⚠️  服务未运行（PID 文件存在但进程不存在）"
      rm -f "$PID_FILE"
    fi
  else
    echo "ℹ️  服务未运行"
  fi
}

# 主逻辑
case "${1:-}" in
  start)
    start_server
    ;;
  stop)
    stop_server
    ;;
  status)
    status_server
    ;;
  *)
    echo "用法: $0 {start|stop|status}"
    exit 1
    ;;
esac
