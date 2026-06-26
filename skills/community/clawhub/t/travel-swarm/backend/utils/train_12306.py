"""12306火车票模块 - 查询班次/车次/座位/购票链接"""
import aiohttp
import os

class Train12306Client:
    """12306火车票查询客户端"""
    
    def __init__(self):
        self.base_url = "https://www.12306.cn/index/"
    
    async def search_trains(self, from_city: str, to_city: str, date: str = "") -> dict:
        """搜索火车票
        
        Args:
            from_city: 出发城市（如"西安"）
            to_city: 目的地城市（如"上海"）
            date: 出发日期
        
        Returns:
            车次信息列表
        """
        
        # 常用城市代码映射
        city_codes = {
            "西安": "XAY",
            "上海": "SHH",
            "北京": "BJP",
            "杭州": "HZH",
            "成都": "CDW",
            "重庆": "CQW",
            "南京": "NJH",
            "苏州": "SZH",
            "武汉": "WHN",
            "长沙": "CSQ"
        }
        
        from_code = city_codes.get(from_city, from_city[:2])
        to_code = city_codes.get(to_city, to_city[:2])
        
        print(f"[12306] 查询: {from_city}({from_code}) → {to_city}({to_code})")
        
        # 模拟车次数据（真实场景需调用MCP）
        # 常见车次类型：G(高铁)、D(动车)、C(城际)、Z(直达)、T(特快)、K(快速)
        trains = self._generate_mock_trains(from_city, to_city)
        
        return {
            "from": from_city,
            "to": to_city,
            "trains": trains,
            "booking_link": f"https://www.12306.cn/index/index.html"
        }
    
    def _generate_mock_trains(self, from_city: str, to_city: str) -> list:
        """生成模拟车次数据（真实场景需调用12306 MCP）"""
        
        # 根据距离生成车次
        if from_city in ["西安", "成都", "重庆"] and "上海" in from_city or "北京" in from_city:
            # 长途：高铁为主
            trains = [
                {"train_no": "G1234", "type": "高铁", "from_time": "08:00", "to_time": "13:30", "duration": "5h30m", 
                 "seats": {"一等座": "有票", "二等座": "有票", "商务座": "5张"}, "price": {"一等座": 900, "二等座": 550}},
                {"train_no": "D5678", "type": "动车", "from_time": "10:15", "to_time": "18:45", "duration": "8h30m",
                 "seats": {"一等座": "有票", "二等座": "12张"}, "price": {"一等座": 600, "二等座": 380}},
            ]
        else:
            # 短途：城际/高铁
            trains = [
                {"train_no": "G890", "type": "高铁", "from_time": "07:30", "to_time": "09:15", "duration": "1h45m",
                 "seats": {"一等座": "有票", "二等座": "有票"}, "price": {"一等座": 120, "二等座": 75}},
                {"train_no": "C201", "type": "城际", "from_time": "08:00", "to_time": "09:30", "duration": "1h30m",
                 "seats": {"二等座": "有票"}, "price": {"二等座": 50}},
            ]
        
        # 添加购票链接
        for train in trains:
            train["booking_link"] = f"https://www.12306.cn/index/index.html"
        
        return trains
    
    def get_booking_link(self, train_no: str) -> str:
        """获取购票链接"""
        return f"https://www.12306.cn/index/index.html"