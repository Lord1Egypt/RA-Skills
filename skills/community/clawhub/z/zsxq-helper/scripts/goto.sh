#!/bin/bash
# 进入指定星球
# 使用方法: ./goto.sh <group_id>

GROUP_ID=${1:-51112818881544}

echo "正在进入星球..."
echo "星球URL: https://wx.zsxq.com/group/${GROUP_ID}"
echo ""
echo "如果未登录，请先执行 login.sh 进行登录"
