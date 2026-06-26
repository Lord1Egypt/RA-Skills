#!/bin/bash
#========================================
# 小红书数据分析 - 配置文件
#========================================
# 用户需要自行填写以下配置

# 方式1: 官方API (需要企业资质申请)
# export XHS_API_KEY="your-api-key"
# export XHS_API_SECRET="your-api-secret"

# 方式2: 第三方服务
# export XHS_API_KEY="your-third-party-key"

# 方式3: Cookie (部分接口可用)
# export XHS_COOKIE="your-cookie-string"

#========================================
# 通用配置
#========================================

# 请求间隔 (秒) - 建议 1-3 秒
REQUEST_DELAY=2

# 超时时间 (秒)
REQUEST_TIMEOUT=30

# 默认返回数量
DEFAULT_LIMIT=50

# 输出目录
OUTPUT_DIR="./output"
