#!/usr/bin/env python3
"""
飞书 Bot 启动脚本（自动 patch SSL）
"""
import sys
import os

# 在导入 lark_oapi 之前 patch websockets
def patch_websockets_ssl():
    import ssl
    import websockets.legacy.client
    
    # 保存原始 connect 函数
    _original_connect = websockets.legacy.client.connect
    
    # 创建包装函数
    def connect_no_ssl_verify(uri, **kwargs):
        # 强制使用不验证证书的 SSL 上下文
        kwargs['ssl'] = ssl._create_unverified_context()
        return _original_connect(uri, **kwargs)
    
    # 替换
    websockets.legacy.client.connect = connect_no_ssl_verify
    print("✅ SSL 验证已禁用（解决本地代理证书问题）")

# 执行 patch
patch_websockets_ssl()

# 现在导入并运行 bot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bot_longconn import main

if __name__ == '__main__':
    main()
