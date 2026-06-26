#!/bin/bash

#========================================
# Sentinel 卫星影像下载器
# 基于 STAC API 下载哨兵系列卫星影像
#========================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/sentinel-download.py"

# 检查 Python 是否安装
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        echo "错误：未找到 Python，请先安装 Python 3"
        exit 1
    fi
}

# 检查依赖
check_dependencies() {
    echo "检查依赖..."
    $PYTHON_CMD -c "import requests" 2>/dev/null || {
        echo "安装 requests..."
        pip3 install requests || pip install requests
    }
    $PYTHON_CMD -c "import pystac_client" 2>/dev/null || {
        echo "安装 pystac_client..."
        pip3 install pystac-client || pip install pystac-client
    }
}

# 显示帮助
show_help() {
    echo "=========================================="
    echo "  Sentinel 哨兵卫星影像下载器"
    echo "  基于 STAC API"
    echo "=========================================="
    echo ""
    echo "用法：$0 [选项]"
    echo ""
    echo "必填参数:"
    echo "  --bbox <minLon minLat maxLon maxLat>  地理范围"
    echo "  --start-date <YYYY-MM-DD>             开始日期"
    echo "  --end-date <YYYY-MM-DD>               结束日期"
    echo ""
    echo "可选参数:"
    echo "  --mission <sentinel-1|2|5p>           卫星任务 (默认：sentinel-2)"
    echo "  --max-cloud-cover <0-100>             最大云量 (默认：100)"
    echo "  --stac-api <URL>                      STAC API 端点"
    echo "  --output-dir <目录>                   输出目录"
    echo "  --limit <数量>                        最大结果数 (默认：10)"
    echo "  --download                            下载影像"
    echo "  --output-format <table|json>          输出格式"
    echo "  --check-deps                          检查并安装依赖"
    echo "  -h, --help                            显示帮助"
    echo ""
    echo "示例:"
    echo "  # 搜索北京地区的 Sentinel-2 影像"
    echo "  $0 --bbox 116.0 39.0 117.0 40.0 --start-date 2024-01-01 --end-date 2024-12-31"
    echo ""
    echo "  # 搜索并限制云量小于 10%"
    echo "  $0 --bbox 116.0 39.0 117.0 40.0 --start-date 2024-01-01 --end-date 2024-12-31 --max-cloud-cover 10"
    echo ""
    echo "  # 搜索并下载"
    echo "  $0 --bbox 116.0 39.0 117.0 40.0 --start-date 2024-01-01 --end-date 2024-12-31 --download --output-dir ./data"
    echo ""
    echo "常用 STAC API 端点:"
    echo "  - AWS Earth Search: https://earth-search.aws.element84.com/v0"
    echo "  - Microsoft PC: https://planetarycomputer.microsoft.com/api/stac/v1"
    echo ""
}

# 主程序
main() {
    # 处理帮助
    if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
        show_help
        exit 0
    fi

    # 处理依赖检查
    if [[ "$1" == "--check-deps" ]]; then
        check_python
        check_dependencies
        echo "依赖检查完成"
        exit 0
    fi

    # 检查 Python
    check_python

    # 检查参数
    if [[ $# -eq 0 ]]; then
        echo "错误：缺少参数"
        show_help
        exit 1
    fi

    # 检查脚本是否存在
    if [[ ! -f "$PYTHON_SCRIPT" ]]; then
        echo "错误：未找到 Python 脚本：$PYTHON_SCRIPT"
        exit 1
    fi

    # 执行 Python 脚本
    $PYTHON_CMD "$PYTHON_SCRIPT" "$@"
}

main "$@"
