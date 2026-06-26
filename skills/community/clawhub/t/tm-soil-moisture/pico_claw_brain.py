import sqlite3
import json
import os
import argparse
from typing import Dict, Any, List

# 根据 README.md，默认的 SQLite 数据库路径
DB_PATH = "/usr/apps/config/agri.db"

# 尝试导入 mcp（ClawHub / MCP Server 支持的库）
try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("AgriBrainSkill")
except ImportError:
    mcp = None
    print("Warning: mcp package not found. Running in standalone mode.")

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"未找到数据库文件: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def parse_sensor_data(payload_str: str) -> Dict[str, Any]:
    """
    解析数据库中存储的 JSON 字符串，将多深度数据提取出来。
    """
    try:
        data = json.loads(payload_str)
    except (json.JSONDecodeError, TypeError):
        return {}
    
    result = {
        "depths": {},
        "geo": data.get("geo", {}),
        "power": data.get("power"),
        "rssi": data.get("GPRS_RSSI"),
        "sn": data.get("gprs_ccid")
    }
    
    # 动态解析各深度的温度(Soil_Temp)和湿度(Soil_Humi)
    for key, value in data.items():
        if key.startswith("Soil_Temp"):
            depth_str = key.replace("Soil_Temp", "")
            if depth_str.isdigit():
                depth = int(depth_str)
                if depth not in result["depths"]:
                    result["depths"][depth] = {}
                result["depths"][depth]["temp"] = value
        elif key.startswith("Soil_Humi"):
            depth_str = key.replace("Soil_Humi", "")
            if depth_str.isdigit():
                depth = int(depth_str)
                if depth not in result["depths"]:
                    result["depths"][depth] = {}
                result["depths"][depth]["humi"] = value
                
    return result

def extract_payload(row: sqlite3.Row) -> str:
    """
    兼容处理：根据文档 JSON 应该在 data 字段。
    但考虑到你提到 '表中的type字段存的数据格式为...'，这里增加对 type 字段的 fallback 检测。
    """
    payload_str = row["data"]
    # 如果 type 字段包含 JSON 特征字符串，则优先使用 type
    if row["type"] and "{" in str(row["type"]) and "Soil_Humi" in str(row["type"]):
        payload_str = row["type"]
    return payload_str

def query_device_data(sn: str) -> str:
    """
    查询指定设备最新的一条数据
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM device_data WHERE sn = ? ORDER BY time DESC LIMIT 1", (sn,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return f"❌ 数据库中没有找到设备 {sn} 的相关记录。"
            
        payload_str = extract_payload(row)
        parsed = parse_sensor_data(payload_str)
        
        if not parsed.get("depths"):
            return f"⚠️ 设备 {sn} 的数据格式无法解析。"
            
        # 构建对用户的友好回答
        lines = [f"🌱 设备 {sn} 最新数据：", f"🕒 记录时间: {row['time']}"]
        if parsed["geo"]:
            lines.append(f"📍 位置: {parsed['geo'].get('lon', 'N/A')}, {parsed['geo'].get('lat', 'N/A')}")
        if parsed["power"]:
            lines.append(f"🔋 电量: {parsed['power']}V")
            
        lines.append("\n📊 各深度温湿度:")
        # 按深度排序输出
        for depth in sorted(parsed["depths"].keys()):
            d_data = parsed["depths"][depth]
            t = d_data.get("temp", "N/A")
            h = d_data.get("humi", "N/A")
            lines.append(f"  - {depth}cm: 🌡️ 温度 {t}℃ | 💧 湿度 {h}%")
            
        return "\n".join(lines)
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"❌ 查询设备数据时发生错误: {str(e)}"

def calculate_depth_average(depth: int) -> str:
    """
    统计所有设备指定深度的平均土壤温度和湿度
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 兼容性更好的写法：获取每个设备最新的一条记录
        query = """
        SELECT d1.sn, d1.data, d1.type 
        FROM device_data d1
        INNER JOIN (
            SELECT sn, MAX(time) as max_time 
            FROM device_data 
            GROUP BY sn
        ) d2 ON d1.sn = d2.sn AND d1.time = d2.max_time
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "❌ 数据库中没有任何设备的记录。"
            
        total_temp = 0.0
        total_humi = 0.0
        count_temp = 0
        count_humi = 0
        
        for row in rows:
            payload_str = extract_payload(row)
            parsed = parse_sensor_data(payload_str)
            depth_data = parsed.get("depths", {}).get(depth)
            
            if depth_data:
                if "temp" in depth_data and depth_data["temp"] is not None:
                    total_temp += float(depth_data["temp"])
                    count_temp += 1
                if "humi" in depth_data and depth_data["humi"] is not None:
                    total_humi += float(depth_data["humi"])
                    count_humi += 1
                    
        if count_temp == 0 and count_humi == 0:
            return f"⚠️ 没有找到任何设备包含深度为 {depth}cm 的有效数据。"
            
        avg_temp = round(total_temp / count_temp, 2) if count_temp > 0 else "N/A"
        avg_humi = round(total_humi / count_humi, 2) if count_humi > 0 else "N/A"
        
        return (f"📈 {depth}cm 深度区域平均值统计：\n"
                f"🌡️ 平均温度: {avg_temp}℃ (参与统计设备数: {count_temp})\n"
                f"💧 平均湿度: {avg_humi}% (参与统计设备数: {count_humi})")
                
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"❌ 统计平均值时发生错误: {str(e)}"

def check_irrigation_advice(sn: str = "2544012010") -> str:
    """
    结合当前的土壤温度以及未来天气趋势给出建议
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM device_data WHERE sn = ? ORDER BY time DESC LIMIT 1", (sn,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return f"❌ 数据库中没有找到设备 {sn} 的相关记录，无法提供灌溉建议。"
            
        payload_str = extract_payload(row)
        parsed = parse_sensor_data(payload_str)
        
        depths = parsed.get("depths", {})
        # 提取浅层水分参考（如 20cm 和 40cm）
        humi_20 = depths.get(20, {}).get("humi")
        humi_40 = depths.get(40, {}).get("humi")
        
        if humi_20 is None or humi_40 is None:
            return f"⚠️ 设备 {sn} 数据不全（缺少20cm或40cm湿度数据），无法给出准确灌溉建议。"
            
        geo = parsed.get("geo", {})
        
        # 实际业务中可在这里加入真实的天气 API 调用 (例如使用 requests 获取降水概率)
        weather_forecast = "晴朗 (模拟)" 
        rain_prob = 0.0  # 模拟降水概率
        
        avg_humi = (float(humi_20) + float(humi_40)) / 2
        advice = ""
        
        # 简单规则引擎：文冠果较耐旱
        if rain_prob > 0.5:
            advice = "🌧️ 暂缓灌溉（预计未来有雨，可节约水资源）"
        elif avg_humi < 15:
            advice = f"🚨 建议立即灌溉（土壤极度干旱，20-40cm平均湿度仅 {avg_humi:.1f}%）"
        elif avg_humi < 25:
            advice = f"💧 建议适量灌溉（土壤含水量偏低，20-40cm平均湿度 {avg_humi:.1f}%）"
        else:
            advice = f"✅ 无需操作（土壤水分充足，20-40cm平均湿度 {avg_humi:.1f}%）"
            
        result = [
            f"💡 灌溉决策建议 (基于设备 {sn}):",
            f"📍 位置: {geo.get('lon', '未知')}, {geo.get('lat', '未知')}",
            f"💧 当前参考湿度 (20-40cm均值): {avg_humi:.1f}%",
            f"⛅ 未来天气预测: {weather_forecast}",
            f"🎯 最终建议: {advice}"
        ]
        
        return "\n".join(result)
        
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return f"❌ 获取灌溉建议时发生错误: {str(e)}"

# 注册 MCP Tools (当在 ClawHub 等支持 MCP 的环境中运行时)
if mcp:
    @mcp.tool()
    def query_device_data_tool(sn: str) -> str:
        """查询指定设备（如 2544012010）最新的一条温湿度数据"""
        return query_device_data(sn)

    @mcp.tool()
    def calculate_depth_average_tool(depth: int) -> str:
        """统计所有设备特定深度（如 50 厘米）的平均土壤温度和湿度"""
        return calculate_depth_average(depth)

    @mcp.tool()
    def check_irrigation_advice_tool(sn: str = "2544012010") -> str:
        """结合当前的土壤干湿程度和未来天气趋势给出灌溉建议"""
        return check_irrigation_advice(sn)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="文冠果智慧农业助手 - 本地测试 CLI")
    parser.add_argument("--query", type=str, help="查询指定设备最新数据, 传入设备SN")
    parser.add_argument("--avg", type=int, help="统计指定深度的区域平均值, 传入深度(cm)")
    parser.add_argument("--advice", type=str, help="获取指定设备的灌溉建议, 传入设备SN")
    parser.add_argument("--mcp", action="store_true", help="启动 MCP 服务器")
    
    args = parser.parse_args()
    
    if args.mcp:
        if mcp:
            print("Starting MCP Server...")
            mcp.run()
        else:
            print("MCP package not installed. Cannot start MCP server.")
    elif args.query:
        print(query_device_data(args.query))
    elif args.avg:
        print(calculate_depth_average(args.avg))
    elif args.advice:
        print(check_irrigation_advice(args.advice))
    else:
        # 默认不带参数时如果有 mcp 就尝试启动
        if mcp:
            mcp.run()
        else:
            parser.print_help()
