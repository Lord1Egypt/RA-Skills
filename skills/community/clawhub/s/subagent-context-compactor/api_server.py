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
