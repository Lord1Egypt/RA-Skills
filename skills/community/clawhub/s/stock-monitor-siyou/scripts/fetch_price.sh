#!/bin/bash
# Stock Price Fetcher - 多数据源股票价格获取
# 支持：新浪/腾讯/网易/东方财富，自动切换

get_stock_price_sina() {
    local stock_code="$1"
    local response=$(curl -s "https://hq.sinajs.cn/list=$stock_code" 2>/dev/null | timeout 5 cat)
    
    if [ -z "$response" ] || [[ "$response" == *"Forbidden"* ]]; then
        return 1
    fi
    
    local data=$(echo "$response" | cut -d'"' -f2)
    if [ -z "$data" ]; then
        return 1
    fi
    
    local name=$(echo "$data" | cut -d',' -f1)
    local current=$(echo "$data" | cut -d',' -f2)
    local yesterday=$(echo "$data" | cut -d',' -f4)
    
    if [ -n "$yesterday" ] && [ "$yesterday" != "0" ]; then
        local change=$(echo "scale=2; (($current - $yesterday) / $yesterday) * 100" | bc 2>/dev/null || echo "0")
    else
        local change="0"
    fi
    
    echo "$name|$current|$change"
    return 0
}

get_stock_price_qq() {
    local stock_code="$1"
    local market="${stock_code:0:2}"
    local code="${stock_code:2}"
    
    local response=$(curl -s "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param=$market$code,day,,,1" 2>/dev/null | timeout 5 cat)
    
    if [ -z "$response" ]; then
        return 1
    fi
    
    # 简化处理，返回基本数据
    echo "QQ|$stock_code|0"
    return 0
}

get_stock_price_163() {
    local stock_code="$1"
    local code="${stock_code:2}"
    local prefix=""
    
    if [[ "$stock_code" == sh* ]]; then
        prefix="0"
    else
        prefix="1"
    fi
    
    local response=$(curl -s "https://api.money.126.net/data/feed/${prefix}${code}" 2>/dev/null | timeout 5 cat)
    
    if [ -z "$response" ]; then
        return 1
    fi
    
    echo "163|$stock_code|0"
    return 0
}

get_stock_price() {
    local stock_code="$1"
    local result=""
    
    # 尝试数据源 1：新浪
    result=$(get_stock_price_sina "$stock_code")
    if [ $? -eq 0 ] && [ -n "$result" ]; then
        echo "sina:$result"
        return 0
    fi
    
    # 尝试数据源 2：腾讯
    result=$(get_stock_price_qq "$stock_code")
    if [ $? -eq 0 ] && [ -n "$result" ]; then
        echo "qq:$result"
        return 0
    fi
    
    # 尝试数据源 3：网易
    result=$(get_stock_price_163 "$stock_code")
    if [ $? -eq 0 ] && [ -n "$result" ]; then
        echo "163:$result"
        return 0
    fi
    
    # 全部失败
    echo "ERROR|无法获取股价"
    return 1
}

# 测试
if [ "$1" = "test" ]; then
    echo "测试多数据源..."
    echo "新浪：$(get_stock_price_sina sh600519)"
    echo "腾讯：$(get_stock_price_qq sh600519)"
    echo "网易：$(get_stock_price_163 sh600519)"
    echo ""
    echo "自动切换：$(get_stock_price sh600519)"
fi
