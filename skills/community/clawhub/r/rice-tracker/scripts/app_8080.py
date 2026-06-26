#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""大米消耗采购提醒系统 - 使用 8080 端口"""
import sys
import os

# 修改端口为 8080
PORT = 8080
HOST = "0.0.0.0"

# 导入原 app
sys.path.insert(0, os.path.dirname(__file__))
from app import app, DATA_FILE, load_records, save_records, days_left, expected_date

if __name__ == "__main__":
    print(f"\n🍚 大米消耗提醒系统已启动 (端口 8080)")
    print(f"   本地访问：http://localhost:{PORT}")
    print(f"   手机访问：http://<本机IP>:{PORT}")
    print(f"   数据文件：{DATA_FILE}")
    print(f"   按 Ctrl+C 停止服务\n")
    app.run(host=HOST, port=PORT, debug=False)
