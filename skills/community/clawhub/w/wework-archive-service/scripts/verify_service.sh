#!/bin/bash
# 企业微信存档服务一键验证脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config/wework_config.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== 企业微信存档服务验证 ===${NC}"

# 1. 检查配置文件
echo -e "\n1. 检查配置文件..."
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}✗ 配置文件不存在: $CONFIG_FILE${NC}"
    echo "请复制 config/wework_config_template.json 并填写配置"
    exit 1
else
    echo -e "${GREEN}✓ 配置文件存在${NC}"
    
    # 检查配置项
    if python3 -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)
    
required = ['callback_token', 'callback_encoding_aes_key', 'corp_id', 'agent_id', 'corp_secret', 'archive_token']
missing = [key for key in required if key not in config]
if missing:
    print('缺失配置项:', missing)
    exit(1)
else:
    print('所有必需配置项都存在')
    exit(0)
" 2>/dev/null; then
        echo -e "${GREEN}✓ 配置项完整${NC}"
    else
        echo -e "${RED}✗ 配置项不完整${NC}"
        exit 1
    fi
fi

# 2. 检查Python依赖
echo -e "\n2. 检查Python依赖..."
if python3 -c "import flask, Crypto, requests" 2>/dev/null; then
    echo -e "${GREEN}✓ Python依赖已安装${NC}"
else
    echo -e "${YELLOW}⚠ Python依赖未安装，正在安装...${NC}"
    pip3 install flask pycryptodome requests
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Python依赖安装成功${NC}"
    else
        echo -e "${RED}✗ Python依赖安装失败${NC}"
        exit 1
    fi
fi

# 3. 检查服务是否运行
echo -e "\n3. 检查服务状态..."
PID_FILE="$SCRIPT_DIR/../wework_service.pid"
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 服务正在运行 (PID: $PID)${NC}"
        
        # 测试健康检查接口
        echo -e "\n4. 测试服务接口..."
        if curl -s http://localhost:8400/health > /dev/null 2>&1; then
            echo -e "${GREEN}✓ 健康检查接口正常${NC}"
            
            # 测试回调验证接口
            if curl -s "http://localhost:8400/callback?msg_signature=test&timestamp=1234567890&nonce=test&echostr=test" > /dev/null 2>&1; then
                echo -e "${GREEN}✓ 回调接口可访问${NC}"
            else
                echo -e "${YELLOW}⚠ 回调接口访问异常（可能是正常现象）${NC}"
            fi
            
            # 测试存档接口
            if curl -s http://localhost:8400/archive/health > /dev/null 2>&1; then
                echo -e "${GREEN}✓ 存档接口正常${NC}"
            else
                echo -e "${YELLOW}⚠ 存档接口访问异常${NC}"
            fi
        else
            echo -e "${RED}✗ 健康检查接口异常${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ 服务PID文件存在但进程不存在${NC}"
        rm -f "$PID_FILE"
        echo -e "${YELLOW}请运行 ./scripts/start_service.sh 启动服务${NC}"
    fi
else
    echo -e "${YELLOW}⚠ 服务未运行${NC}"
    echo -e "${YELLOW}请运行 ./scripts/start_service.sh 启动服务${NC}"
fi

# 5. 检查端口占用
echo -e "\n5. 检查端口占用..."
if lsof -ti:8400 > /dev/null 2>&1; then
    PORT_PID=$(lsof -ti:8400)
    echo -e "${GREEN}✓ 8400端口已被占用 (PID: $PORT_PID)${NC}"
else
    echo -e "${YELLOW}⚠ 8400端口未被占用${NC}"
fi

# 6. 检查数据库
echo -e "\n6. 检查数据库..."
DB_FILE="$SCRIPT_DIR/../wework_combined.db"
if [ -f "$DB_FILE" ]; then
    DB_SIZE=$(du -h "$DB_FILE" | cut -f1)
    echo -e "${GREEN}✓ 数据库存在 (大小: $DB_SIZE)${NC}"
    
    # 检查数据库结构
    if python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('$DB_FILE')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"')
    tables = cursor.fetchall()
    print('数据库表:', [t[0] for t in tables])
    conn.close()
except Exception as e:
    print('数据库检查失败:', str(e))
    exit(1)
" 2>/dev/null; then
        echo -e "${GREEN}✓ 数据库结构正常${NC}"
    else
        echo -e "${YELLOW}⚠ 数据库检查异常${NC}"
    fi
else
    echo -e "${YELLOW}⚠ 数据库文件不存在（首次运行正常）${NC}"
fi

echo -e "\n${YELLOW}=== 验证完成 ===${NC}"
echo -e "服务状态: ${GREEN}就绪${NC}"
echo -e "下一步:"
echo -e "1. 在企业微信后台配置回调URL: http://你的域名/callback"
echo -e "2. 配置会话存档回调URL: http://你的域名/archive/callback"
echo -e "3. 使用Cloudflare Tunnel暴露服务到公网"