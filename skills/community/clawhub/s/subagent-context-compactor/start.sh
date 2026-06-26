#!/bin/bash

# 上下文压缩代理启动脚本

echo "启动上下文压缩代理..."
echo "采用分层压缩策略，基于内存使用触发机制"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误：需要Python3环境"
    exit 1
fi

# 安装依赖
echo "检查依赖..."
pip3 install -r requirements.txt 2>/dev/null || echo "跳过依赖安装"

# 创建日志目录
mkdir -p logs

# 启动压缩代理
echo "启动压缩代理进程..."
python3 compactor.py > logs/compactor.log 2>&1 &

# 获取进程ID
PID=$!
echo $PID > compactor.pid
echo "压缩代理已启动，PID: $PID"

# 创建监控脚本
cat > monitor.sh << 'EOF'
#!/bin/bash
# 压缩代理监控脚本

PID_FILE="compactor.pid"
LOG_FILE="logs/compactor.log"

if [ ! -f "$PID_FILE" ]; then
    echo "错误：PID文件不存在"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null; then
    echo "压缩代理正在运行 (PID: $PID)"
    
    # 显示最近日志
    echo "最近日志："
    tail -10 "$LOG_FILE"
    
    # 显示统计信息
    echo -e "\n发送统计请求..."
    echo "GET_STATS" > stats_request.fifo 2>/dev/null || echo "使用API获取统计"
else
    echo "压缩代理未运行"
fi
EOF

chmod +x monitor.sh

# 创建API接口
cat > api_server.py << 'EOF'
#!/usr/bin/env python3
"""
压缩代理API服务器
"""

from flask import Flask, request, jsonify
import json
import os
from compactor import ContextCompactor

app = Flask(__name__)
compactor = ContextCompactor()

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    stats = compactor.get_stats()
    return jsonify(stats)

@app.route('/api/compact', methods=['POST'])
def compact():
    """执行压缩"""
    data = request.json
    messages = data.get('messages', [])
    token_usage = data.get('token_usage', 0.0)
    
    result = compactor.compact(messages, token_usage)
    return jsonify(result)

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    """配置管理"""
    if request.method == 'POST':
        new_config = request.json
        result = compactor.update_config(new_config)
        return jsonify(result)
    else:
        return jsonify(compactor.config)

@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "service": "context-compactor",
        "timestamp": os.popen('date').read().strip()
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8081, debug=False)
EOF

echo "API服务器已创建 (端口: 8081)"
echo ""
echo "使用方法："
echo "1. 查看状态：./monitor.sh"
echo "2. 停止代理：kill \$(cat compactor.pid)"
echo "3. API接口：http://127.0.0.1:8081/api/stats"
echo ""
echo "压缩代理已就绪！"