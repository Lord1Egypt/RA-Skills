---
name: Real Estate Spider
description: 专业爬取中国房产中介网站（安居客、搜房网、贝壳找房、链家）数据的通用爬虫技能，包含反爬虫策略和自动数据提取功能
read_when:
  - 需要爬取房产中介网站数据
  - 需要绕过网站反爬虫机制
  - 需要提取房产信息（价格、面积、位置、户型等）
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["python3","agent-browser"]}}}
allowed-tools: Bash(agent-browser:*)
---

# 房产中介网站爬虫技能

## 简介

本技能专门用于爬取中国主流房产中介网站数据，包括：
1. 安居客 (anjuke.com)
2. 搜房网 (soufun.com)
3. 贝壳找房 (ke.com)
4. 链家 (lianjia.com)

## 前置要求

- Python 3.x
- agent-browser 技能已安装
- requests 库 (可以通过 pip 安装)

## 安装依赖

```bash
# 安装 Python requests 库
pip install requests beautifulsoup4 lxml
```

## 主要功能

### 1. 反爬虫绕过策略
- 模拟真实浏览器指纹
- 随机延迟避免频率检测
- Cookie 和会话管理
- 代理 IP 支持（可选）
- 验证码处理机制

### 2. 数据提取功能
- 提取房价信息
- 提取房产面积
- 提取地理位置
- 提取户型信息
- 提取装修状态
- 提取建筑年代

### 3. 导出格式
- JSON 格式
- CSV 格式
- Excel 格式
- 可视化图表

## 使用方法

### 基本爬虫脚本

```bash
# 使用 Python 脚本爬取安居客数据
python3 ~/.openclaw/workspace/skills/real-estate-spider/scripts/anjuke_crawler.py

# 使用 Shell 脚本配合 agent-browser
bash ~/.openclaw/workspace/skills/real-estate-spider/scripts/bypass_anjuke.sh
```

### 配置网站选择

```python
# 配置文件示例
# ~/.openclaw/workspace/skills/real-estate-spider/config/real_estate_config.py

import json

CONFIG = {
    "anjuke": {
        "url": "https://www.anjuke.com",
        "data_selectors": {
            "price": ".property-price",
            "area": ".property-area",
            "location": ".property-location",
            "type": ".property-type"
        }
    },
    "ke": {
        "url": "https://ke.com",
        "data_selectors": {
            "price": ".price-text",
            "area": ".area-text",
            "location": ".location-text",
            "type": ".type-text"
        }
    },
    "lianjia": {
        "url": "https://www.lianjia.com",
        "data_selectors": {
            "price": ".total-price",
  4         "area": ".area-num",
            "location": ".location-text",
            "type": ".house-type"
        }
    },
    "soufun": {
        "url": "https://www.soufun.com",
        "data_selectors": {
            "price": ".price-num",
            "area": ".area-num",
            "location": ".location-text",
            "type": ".type-text"
        }
    }
}
```

### 通用爬虫模板

```python
# 通用爬虫脚本模板
import time
import random
import json
from dataclasses import dataclass

@dataclass
class PropertyData:
    title: str
    price: str
    area: str
    location: str
    house_type: str
    age: str
    orientation: str
    decoration: str

class RealEstateSpider:
    def __init__(self, website_name):
        self.website_name = website_name
        self.config = CONFIG[website_name]
        self.base_url = self.config["url"]
        self.selectors = self.config["data_selectors"]
        
    def crawl(self, city="北京", district=None):
        """爬取指定城市和区域的房产数据"""
        # 构建URL
        url = self.build_url(city, district)
        
        # 发送请求
        data = self.send_request(url)
        
        # 解析数据
        properties = self.parse_data(data)
        
        # 返回结果
        return properties
    
    def build_url(self, city, district):
        """构建目标URL"""
        if self.website_name == "anjuke":
            return f"{self.base_url}/fangyuan/{city}"
        elif self.website_name == "ke":
            return f"{self.base_url}/city/{city}"
        elif self.website_name == "lianjia":
            return f"{self.base_url}/ershoufang/{city}"
        elif self.website_name == "soufun":
            return f"{self.base_url}/esf/{city}"
        else:
            return self.base_url
    
    def send_request(self, url):
        """发送请求，处理反爬虫"""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # 随机延迟避免频率检测
        sleep_time = random.uniform(2, 5)
        time.sleep(sleep_time)
        
        # 发送请求（此处为简化示例，实际需要根据网站调整）
        import requests
        response = requests.get(url, headers=headers)
        return response.text
    
    def parse_data(self, html_data):
        """解析HTML数据"""
        # 这里需要根据具体网站的HTML结构实现解析逻辑
        properties = []
        
        # 示例解析逻辑
        import re
        pattern = r'"price":"([\d\.]+)",.*"avg_price":"([\d\.]+)",.*"area_num":"([\d\.]+)",.*"house_age":"([\d年]+)",.*"orient":"([^"]+)",.*"fitment_name":"([^"]+)",.*"title":"([^"]+)"'
        matches = re.findall(pattern, html_data)
        
        for match in matches:
            property = PropertyData(
                title=match[6],
                price=match[0],
                area=match[2],
                location="",  # 需要根据网站调整
                house_type="",  # 需要根据网站调整
                age=match[3],
                orientation=match[4],
                decoration=match[5]
            )
            properties.append(property)
            
        return properties
    
    def save_data(self, properties, format="json"):
        """保存数据"""
        if format == "json":
            with open(f'{self.website_name}_properties.json', 'w', encoding='utf-8') as f:
                json.dump([prop.__dict__ for prop in properties], f, ensure_ascii=False, indent=2)
        elif format == "csv":
            import csv
            with open(f'{self.website_name}_properties.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['title', 'price', 'area', 'location', 'house_type', 'age', 'orientation', 'decoration'])
                for prop in properties:
                    writer.writerow([prop.title, prop.price, prop.area, prop.location, prop.house_type, prop.age, prop.orientation, prop.decoration])

if __name__ == "__main__":
    # 示例：爬取安居客数据
    spider = RealEstateSpider("anjuke")
    properties = spider.crawl(city="南京")
    spider.save_data(properties, format="json")
```

### 使用 agent-browser 进行浏览器自动化

```bash
# 使用 agent-browser 绕过JavaScript检测
agent-browser set viewport 1920 1080
agent-browser set headers '{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}'

# 访问房产网站
agent-browser open "https://www.anjuke.com"
agent-browser wait 3000
agent-browser snapshot -i

# 模拟人类浏览行为
agent-browser scroll down 300
agent-browser wait 1000
agent-browser click "link:二手房"
agent-browser wait 2000

# 获取页面数据
agent-browser snapshot -c --scope ".property-list"
agent-browser screenshot "anjuke_properties.png"
```

## 反爬虫策略

### 1. 浏览器指纹伪装
```bash
# 设置设备指纹
agent-browser set device "iPhone 14"
agent-browser set geo 39.9042 116.4074  # 北京地理位置
agent-browser set media dark
```

### 2. 会话管理
```bash
# 保存会话状态
agent-browser cookies set "session_id" "your_session_value"
agent-browser state save "real_estate_session.json"

# 恢复会话状态
agent-browser state load "real_estate_session.json"
```

### 3. 请求频率控制
```python
import time
import random

# 随机延迟
delay = random.uniform(3, 8)
time.sleep(delay)

# 批次处理，每批次后长时间休息
batch_size = 10
for i in range(batch_size):
    # 处理请求
    # 小延迟
    time.sleep(random.uniform(1, 2))
    
# 批次结束后大延迟
time.sleep(random.uniform(30, 60))
```

### 4. 代理IP轮换
```python
# 代理IP池示例
proxy_pool = [
    "http://proxy1.example.com:8080",
    "http://proxy2.example.com:8080",
    "http://proxy3.example.com:8080",
]

import requests

for url in urls_to_crawl:
    proxy = proxy_pool[i % len(proxy_pool)]
    response = requests.get(url, proxies={"http": proxy})
```

## 验证码处理

### 手动处理验证码
```bash
# 遇到验证码时暂停脚本，人工处理
echo "验证码出现，请手动处理！"
agent-browser screenshot "captcha.png"
agent-browser pause
# 手动处理后继续
agent-browser continue
```

### 验证码识别服务（可选）
```python
# 使用第三方验证码识别服务（需要API密钥）
import requests

def solve_captcha(image_path):
    # 上传验证码图片到识别服务
    response = requests.post(
        "https://captcha.service.com/api/solve",
        files={"image": open(image_path, "rb")}
    )
    return response.json()["solution"]
```

## 数据导出与分析

```python
# 数据分析示例
import json
import pandas as pd

# 加载数据
with open('anjuke_properties.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 转换为DataFrame
df = pd.DataFrame(data)

# 统计分析
avg_price = df['price'].mean()
avg_area = df['area'].mean()
price_range = df['price'].min(), df['price'].max()

print(f"平均价格: {avg_price}")
print(f"平均面积: {avg_area}")
print(f"价格范围: {price_range}")
```

## 常见问题与解决方案

### 1. 网站封锁
- **解决方案**: 使用代理IP轮换
- **解决方案**: 降低请求频率
- **解决方案**: 更换用户代理

### 2. 验证码频繁出现
- **解决方案**: 增加随机延迟
- **解决方案**: 模拟真实用户行为（滚动、点击）
- **解决方案**: 使用验证码识别服务

### 3. 数据提取失败
- **解决方案**: 更新HTML选择器
- **解决方案**: 检查网站结构变化
- **解决方案**: 使用备用解析方法

### 4. JavaScript渲染问题
- **解决方案**: 使用agent-browser等待页面完全加载
- **解决方案**: 等待网络空闲状态
- **解决方案**: 截图检查页面状态

## 法律与伦理注意事项

### 使用本技能时请遵守：
1. **网站条款**: 遵守房产网站的爬虫政策
2. **数据使用**: 仅用于合法目的
3. **频率控制**: 避免影响网站正常运营
4. **数据保护**: 保护用户隐私信息

### 建议使用频率：
- 每批次不超过100个请求
- 每小时不超过1000个请求
- 每天不超过5000个请求

## 持续改进

本技能会根据房产网站的反爬虫策略更新，持续改进爬取方法和数据提取逻辑。

### 更新日志：
- 2026-03-26: 创建技能，包含通用房产爬虫框架
- 后续更新: 将根据网站变化调整选择器和反爬虫策略