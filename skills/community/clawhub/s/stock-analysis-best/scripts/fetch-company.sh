#!/bin/bash
# 公司官网投资者关系数据获取
# 用法：./fetch-company.sh <公司名> <数据类型>
# 数据类型：announcement(公告), report(财报), presentation(路演)

COMPANY_NAME=$1
DATA_TYPE=${2:-announcement}

if [ -z "$COMPANY_NAME" ]; then
    echo "用法：$0 <公司名> [数据类型]"
    exit 1
fi

# 常见公司投资者关系 URL 映射
declare -A IR_URLS=(
    ["蓝思科技"]="https://www.lensTechnology.com/investor"
    ["宁德时代"]="https://www.catl.com/investor"
    ["茅台"]="http://www.moutai.com.cn/investor"
)

IR_URL="${IR_URLS[$COMPANY_NAME]}"

if [ -z "$IR_URL" ]; then
    echo "未找到 $COMPANY_NAME 的投资者关系页面"
    echo "请手动访问公司官网查询"
    exit 1
fi

case $DATA_TYPE in
  "announcement")
    echo "获取公告：$COMPANY_NAME"
    curl -s "${IR_URL}/announcements" | grep -oP '<a[^>]*>.*?</a>' | head -20
    ;;
  "report")
    echo "获取财报：$COMPANY_NAME"
    curl -s "${IR_URL}/reports" | grep -oP '<a[^>]*>.*?</a>' | head -20
    ;;
  "presentation")
    echo "获取路演材料：$COMPANY_NAME"
    curl -s "${IR_URL}/presentations" | grep -oP '<a[^>]*>.*?</a>' | head -20
    ;;
  *)
    echo "未知的数据类型：$DATA_TYPE"
    exit 1
    ;;
esac
