"""飞机票查询模块 - 查询航班/座位/购票链接"""
import aiohttp

class FlightClient:
    """飞机票查询客户端（阿里百炼 MCP）"""
    
    def __init__(self):
        self.api_url = "https://www.ctrip.com"  # 携程航班查询
    
    async def search_flights(self, from_city: str, to_city: str, date: str = "") -> dict:
        """搜索飞机票
        
        Args:
            from_city: 出发城市
            to_city: 目的地城市
            date: 出发日期
        
        Returns:
            航班信息列表
        """
        
        # 常用机场代码
        airport_codes = {
            "西安": "XIY",
            "上海": "SHA/PVG",
            "北京": "PEK/BJS",
            "杭州": "HGH",
            "成都": "CTU",
            "重庆": "CKG",
            "南京": "NKG",
            "武汉": "WUH"
        }
        
        from_code = airport_codes.get(from_city, from_city[:3])
        to_code = airport_codes.get(to_city, to_city[:3])
        
        print(f"[航班] 查询: {from_city}({from_code}) → {to_city}({to_code})")
        
        # 生成航班数据（真实场景需调用阿里百炼 MCP）
        flights = self._generate_mock_flights(from_city, to_city)
        
        return {
            "from": from_city,
            "to": to_city,
            "flights": flights,
            "booking_link": f"https://flights.ctrip.com/online/list/oneway-{from_city}?depdate={date}"
        }
    
    def _generate_mock_flights(self, from_city: str, to_city: str) -> list:
        """生成模拟航班数据"""
        
        # 根据距离生成航班
        if "国际" in from_city or "国际" in to_city:
            flights = [
                {"flight_no": "MU123", "airline": "东方航空", "from_time": "08:00", "to_time": "12:00",
                 "duration": "4h", "seats": {"经济舱": "有票", "商务舱": "3张"}, 
                 "price": {"经济舱": 1200, "商务舱": 3500}},
            ]
        else:
            # 国内航班
            flights = [
                {"flight_no": "CA1234", "airline": "中国国航", "from_time": "07:30", "to_time": "09:45",
                 "duration": "2h15m", "seats": {"经济舱": "有票", "商务舱": "5张"},
                 "price": {"经济舱": 580, "商务舱": 1800}},
                {"flight_no": "MU5678", "airline": "东方航空", "from_time": "12:00", "to_time": "14:15",
                 "duration": "2h15m", "seats": {"经济舱": "12张"},
                 "price": {"经济舱": 450}},
                {"flight_no": "CZ901", "airline": "南方航空", "from_time": "18:30", "to_time": "20:45",
                 "duration": "2h15m", "seats": {"经济舱": "有票"},
                 "price": {"经济舱": 520}},
            ]
        
        # 添加购票链接
        for flight in flights:
            flight["booking_link"] = f"https://flights.ctrip.com"
        
        return flights