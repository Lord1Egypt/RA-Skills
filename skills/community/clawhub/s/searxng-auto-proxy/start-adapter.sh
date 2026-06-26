#!/bin/bash
cd /root/.openclaw/searxng
nohup python3 -m adapter > /root/.openclaw/logs/searxng-adapter.log 2>&1 &
echo "适配器已启动，PID: $!"
