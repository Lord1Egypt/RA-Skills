#!/usr/bin/env python3
"""
Sih.Ai 配置文件
"""

import os

# Sih.Ai API配置
SIH_API_KEY = os.getenv("SIH_API_KEY", "sk-w4YfLvoXwIEM0I3uNcOOOclfHkBDiR19Md9ixabWv1XMNPhn")
SIH_API_BASE_URL = "https://api.vwu.ai"

# 模型配置
DEFAULT_MODEL = "sihai-image-27"
DEFAULT_SIZE = "2048x2048"

# 超时配置
API_TIMEOUT = 60  # 秒

# 充值页面
TOPUP_URL = "https://sih.ai/topup"
