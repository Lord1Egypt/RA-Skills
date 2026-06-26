#!/usr/bin/env python3
"""导出母单列表到Excel，带自定义表头。需认证。"""
import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 字段映射：API字段 -> 中文表头
FIELD_MAPPING_ZH = {
    'startTime': '开始时间(UTC)',
    'endTime': '理论结束时间(UTC)',
    'finishTime': '结束时间(UTC)',
    'masterOrderId': '母单ID',
    'exchange': '交易所',
    'marketType': '市场类型',
    'tradingAccount': '交易账户',
    'algorithm': '算法类型',
    'symbol': '交易对',
    'side': '方向',
    'executionDuration': '执行时长',
    'totalQuantity': '下单总数量',
    'filledQuantity': '已成交量',
    'completionProgress': '完成率(%)',
    'makerRate': '被动成交率(%)',
    'averagePrice': '成交均价',
    'status': '母单状态',
    'mustComplete': '必须完成',
    'makerRateLimit': '最低Maker率(%)',
    'povLimit': '最大市场成交量占比(%)',
    'limitPrice': '最差成交价',
    'upTolerance': '偏离容忍度上限(%)',
    'lowTolerance': '偏离容忍度下限(%)',
    'strictUpBound': '严格小于偏离容忍度上限',
    'tailOrderProtection': '尾单强制成交',
    'enableMake': '允许挂单'
}

# 字段映射：API字段 -> 英文表头
FIELD_MAPPING_EN = {
    'startTime': 'Start Time(UTC)',
    'endTime': 'End Time(UTC)',
    'finishTime': 'Finish Time(UTC)',
    'masterOrderId': 'Master Order ID',
    'exchange': 'Exchange',
    'marketType': 'Market Type',
    'tradingAccount': 'Trading Account',
    'algorithm': 'Algorithm Type',
    'symbol': 'Trading Pair',
    'side': 'Side',
    'executionDuration': 'Execution Duration',
    'totalQuantity': 'Total Quantity',
    'filledQuantity': 'Filled Quantity',
    'completionProgress': 'Completion Rate(%)',
    'makerRate': 'Maker Rate(%)',
    'averagePrice': 'Average Price',
    'status': 'Order Status',
    'mustComplete': 'Must Complete',
    'makerRateLimit': 'Min Maker Rate(%)',
    'povLimit': 'Max Market Volume Ratio(%)',
    'limitPrice': 'Worst Price',
    'upTolerance': 'Up Tolerance(%)',
    'lowTolerance': 'Low Tolerance(%)',
    'strictUpBound': 'Strictuptolerance',
    'tailOrderProtection': 'TailOrderProtection',
    'enableMake': 'EnableMake'
}

def format_value(key, value, lang='zh', item=None):
    """格式化字段值

    Args:
        key: 字段名
        value: 字段值
        lang: 语言 (zh/en)
        item: 完整的数据项（用于计算派生字段）
    """
    # 特殊处理：实际结束时间（使用 finishedMs）
    # 必须在 value is None 检查之前，因为 finishTime 字段不存在于 API 返回中
    if key == 'finishTime':
        # 使用 finishedMs 字段（毫秒时间戳）
        if item and 'finishedMs' in item:
            finished_ms = item.get('finishedMs')
            if finished_ms:
                try:
                    # 将毫秒时间戳转换为秒
                    timestamp = int(finished_ms) / 1000
                    dt = datetime.fromtimestamp(timestamp)
                    return dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
        return None

    if value is None:
        return ''

    # 处理 NaN
    if isinstance(value, float):
        import math
        if math.isnan(value):
            return ''

    # 特殊处理：理论结束时间（使用 API 返回的 endTime）
    if key == 'endTime':
        if value and value != '' and isinstance(value, str):
            try:
                dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except:
                return value
        # 如果 endTime 为空，返回 None（pandas 会显示为空）
        return None

    # 执行时长格式化（优先使用秒，没有则用分钟）
    if key == 'executionDuration':
        # 优先使用 executionDurationSeconds
        if item and 'executionDurationSeconds' in item:
            total_seconds = item['executionDurationSeconds']
            if total_seconds:
                minutes = total_seconds // 60
                seconds = total_seconds % 60
                return f"{minutes}m {seconds}s"
        # 如果没有秒数，使用分钟
        if isinstance(value, (int, float)):
            return f"{int(value)}m 0s"
        return value

    # 数量字段格式化（不带单位）
    quantity_fields = ['totalQuantity', 'filledQuantity']
    if key in quantity_fields:
        if isinstance(value, (int, float)):
            return value
        return value

    # 母单状态翻译
    if key == 'status':
        status_map_zh = {
            'NEW': '执行中',
            'COMPLETED': '已完成',
            'COMPLETED_WITHTAIL': '已完成',
            'CANCELLED': '已取消',
            'EXPIRED': '已过期',
            'REJECTED': '已拒绝'
        }
        status_map_en = {
            'NEW': 'In Progress',
            'COMPLETED': 'Completed',
            'COMPLETED_WITHTAIL': 'Completed',
            'CANCELLED': 'Cancelled',
            'EXPIRED': 'Expired',
            'REJECTED': 'Rejected'
        }
        if lang == 'zh':
            return status_map_zh.get(value, value)
        else:
            return status_map_en.get(value, value)

    # 百分比字段（需要乘以100）
    percentage_fields = ['completionProgress', 'makerRate', 'makerRateLimit', 'povLimit', 'upTolerance', 'lowTolerance']
    if key in percentage_fields:
        if isinstance(value, (int, float)):
            # 处理特殊值
            if value == -1 or value <= -1:
                return '-' if lang == 'zh' else '-'
            if value == -100 or value <= -100:
                return '-' if lang == 'zh' else '-'
            # 如果值已经是百分比形式（>1），直接保留2位小数
            if value > 1:
                return round(value, 2)
            # 如果是小数形式（0-1），乘以100
            return round(value * 100, 2)
        return value

    # 价格字段的特殊值处理
    if key == 'limitPrice':
        if isinstance(value, (int, float)) and value == -1:
            return '-'

    # 布尔值转换
    if isinstance(value, bool):
        if lang == 'zh':
            return '是' if value else '否'
        else:
            return 'Yes' if value else 'No'

    # 时间字段格式化
    time_fields = ['startTime', 'endTime', 'finishTime', 'createdAt', 'updatedAt']
    if key in time_fields and isinstance(value, str) and value:
        try:
            # 尝试解析ISO格式时间
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return value

    return value

def main():
    parser = argparse.ArgumentParser(description="Export master orders to Excel with custom headers")
    parser.add_argument("--page", type=int, default=None, help="Page number")
    parser.add_argument("--page-size", type=int, default=None, help="Page size")
    parser.add_argument("--status", type=str, default=None, help="NEW or COMPLETED")
    parser.add_argument("--exchange", type=str, default=None, help="Binance, OKX, LTP, Deribit, Hyperliquid")
    parser.add_argument("--symbol", type=str, default=None, help="Trading pair symbol")
    parser.add_argument("--start-time", type=str, default=None, help="Start time ISO8601")
    parser.add_argument("--end-time", type=str, default=None, help="End time ISO8601")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    parser.add_argument("--lang", type=str, default="zh", choices=["zh", "en"], help="Language: zh (Chinese) or en (English)")
    args = parser.parse_args()

    try:
        from _client import get_client
        import pandas as pd

        client = get_client()
        params = {}
        if args.page is not None:
            params["page"] = args.page
        if args.page_size is not None:
            params["pageSize"] = args.page_size
        if args.status is not None:
            params["status"] = args.status
        if args.exchange is not None:
            params["exchange"] = args.exchange
        if args.symbol is not None:
            params["symbol"] = args.symbol
        if args.start_time is not None:
            params["startTime"] = args.start_time
        if args.end_time is not None:
            params["endTime"] = args.end_time

        result = client.get_master_orders(**params)
        items = result.get("items", [])

        if not items:
            print(json.dumps({"success": False, "error": "No data found"}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        # 选择字段映射
        field_mapping = FIELD_MAPPING_ZH if args.lang == "zh" else FIELD_MAPPING_EN

        # 构建数据，按照指定的字段顺序
        ordered_fields = list(field_mapping.keys())
        formatted_data = []

        for item in items:
            row = {}
            for field in ordered_fields:
                value = item.get(field)
                formatted_value = format_value(field, value, args.lang, item)
                header = field_mapping[field]
                row[header] = formatted_value
            formatted_data.append(row)

        df = pd.DataFrame(formatted_data)

        workspace = Path.home() / "workspace"
        workspace.mkdir(exist_ok=True)

        if args.output:
            output_path = Path(args.output)
        else:
            # 使用当前时间作为文件名
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = workspace / f"master_orders_{timestamp}.xlsx"

        # 导出到Excel
        df.to_excel(output_path, index=False, engine='openpyxl')

        print(json.dumps({
            "success": True,
            "file_path": str(output_path),
            "total_records": len(items),
            "language": args.lang
        }, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
