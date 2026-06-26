"""FlyAI MCP调用模块 - 真实航班/火车票价查询"""
import subprocess
import json
import os

class FlyAIClient:
    """FlyAI MCP客户端 - 真实票价查询"""
    
    def __init__(self):
        self.workspace = '/home/admin/.openclaw/workspace'
        self.cli_path = 'npx @fly-ai/flyai-cli'
    
    def search_flight(self, origin: str, destination: str, date: str) -> dict:
        """查询航班票价
        
        Args:
            origin: 出发城市（如"北京"）
            destination: 目的地城市（如"兰州"）
            date: 出发日期（如"2026-05-01"）
        
        Returns:
            航班列表（真实票价+预订链接）
        """
        cmd = f'{self.cli_path} search-flight --origin "{origin}" --destination "{destination}" --dep-date "{date}"'
        
        try:
            result = subprocess.run(
                cmd, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=self.workspace,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                if data.get("status") == 0:
                    print(f"[FlyAI] ✅ 航班查询成功: {origin}→{destination}")
                    return data.get("data", {})
            
            print(f"[FlyAI] ❌ 航班查询失败: {result.stderr}")
            return {"itemList": []}
            
        except Exception as e:
            print(f"[FlyAI] ❌ 异常: {str(e)}")
            return {"itemList": [], "error": str(e)}
    
    def search_train(self, origin: str, destination: str, date: str) -> dict:
        """查询火车票价
        
        Args:
            origin: 出发城市
            destination: 目的地城市
            date: 出发日期
        
        Returns:
            火车列表（真实票价+预订链接）
        """
        cmd = f'{self.cli_path} search-train --origin "{origin}" --destination "{destination}" --dep-date "{date}"'
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.workspace,
                timeout=30
            )
            
            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                if data.get("status") == 0:
                    print(f"[FlyAI] ✅ 火车查询成功: {origin}→{destination}")
                    return data.get("data", {})
            
            print(f"[FlyAI] ❌ 火车查询失败: {result.stderr}")
            return {"itemList": []}
            
        except Exception as e:
            print(f"[FlyAI] ❌ 异常: {str(e)}")
            return {"itemList": [], "error": str(e)}
    
    def format_flight_data(self, data: dict) -> list:
        """格式化航班数据为前端展示格式
        
        Returns:
            [{"flight_no": "HU7297", "airline": "海南航空", "price": 1050, "link": "..."}]
        """
        flights = []
        for item in data.get("itemList", []):
            journey = item.get("journeys", [{}])[0]
            segment = journey.get("segments", [{}])[0]
            
            flight = {
                "flight_no": segment.get("marketingTransportNo", ""),
                "airline": segment.get("marketingTransportName", ""),
                "from_time": segment.get("depDateTime", "").split()[-1] if segment.get("depDateTime") else "",
                "to_time": segment.get("arrDateTime", "").split()[-1] if segment.get("arrDateTime") else "",
                "from_station": segment.get("depStationName", ""),
                "to_station": segment.get("arrStationName", ""),
                "duration": journey.get("totalDuration", ""),
                "price": item.get("ticketPrice", ""),
                "jump_url": item.get("jumpUrl", ""),
                "type": journey.get("journeyType", "直达")
            }
            flights.append(flight)
        
        return flights
    
    def format_train_data(self, data: dict) -> list:
        """格式化火车数据为前端展示格式
        
        Returns:
            [{"train_no": "Z21", "type": "普快", "price": 189.5, "link": "..."}]
        """
        trains = []
        for item in data.get("itemList", []):
            journey = item.get("journeys", [{}])[0]
            segment = journey.get("segments", [{}])[0]
            
            train = {
                "train_no": segment.get("marketingTransportNo", ""),
                "type": segment.get("marketingTransportName", ""),
                "from_time": segment.get("depDateTime", "").split()[-1] if segment.get("depDateTime") else "",
                "to_time": segment.get("arrDateTime", "").split()[-1] if segment.get("arrDateTime") else "",
                "from_station": segment.get("depStationName", ""),
                "to_station": segment.get("arrStationName", ""),
                "seat": segment.get("seatClassName", ""),
                "duration": journey.get("totalDuration", ""),
                "price": item.get("price", ""),
                "jump_url": item.get("jumpUrl", ""),
                "journey_type": journey.get("journeyType", "直达")
            }
            trains.append(train)
        
        return trains


# 使用示例
if __name__ == "__main__":
    client = FlyAIClient()
    
    # 测试航班查询
    flights_data = client.search_flight("北京", "兰州", "2026-05-01")
    flights = client.format_flight_data(flights_data)
    print(f"航班数量: {len(flights)}")
    for f in flights[:3]:
        print(f"  {f['flight_no']} {f['airline']} ¥{f['price']}")
    
    # 测试火车查询
    trains_data = client.search_train("北京", "兰州", "2026-05-01")
    trains = client.format_train_data(trains_data)
    print(f"火车数量: {len(trains)}")
    for t in trains[:3]:
        print(f"  {t['train_no']} {t['type']} ¥{t['price']}")