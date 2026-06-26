---
name: Real Estate Crawler
description: 综合房产中介网站爬虫技能，支持安居客、贝壳找房、链家、搜房网的数据抓取，包含反爬虫绕过策略和数据提取功能。
read_when:
  - 需要爬取房产中介网站数据
  - 需要绕过网站反爬虫机制
  - 需要提取房产信息（价格、面积、位置、户型等）
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["python3","agent-browser"]}}}
allowed-tools: Bash(agent-browser:*)
---

# 房产中介网站爬虫技能

## 简介

这个技能整合了安居客和贝壳找房的爬虫经验，专门用于爬取中国主流房产中介网站的数据：

1. **安居客 (anjuke.com)** - ✅ 已验证可绕过
2. **贝壳找房 (ke.com)** - ✅ 已验证可绕过
3. **链家 (lianjia.com)** - ⚠️ 部分页面需要验证码
4. **搜房网 (soufun.com)** - 待验证

包含完整的反爬虫绕过策略和数据提取功能。

## 核心功能

### 1. 反爬虫绕过策略
- 浏览器指纹伪装（桌面/移动设备）
- 随机延迟和人类行为模拟
- Cookie和会话管理
- 代理IP支持（可选）
- 验证码处理机制

### 2. 数据提取功能
- 房价信息（总价、单价）
- 房产面积
- 地理位置
- 户型信息
- 装修状态
- 建筑年代
- 房屋图片（可选）

### 3. 爬取模式
- **Python快速爬取模式** - 适用于简单反爬虫网站
- **agent-browser浏览器模式** - 适用于复杂反爬虫网站
- **混合模式** - 结合两种方法获取完整数据

### 4. 导出格式
- JSON格式
- CSV格式
- Excel格式（需要 pandas）
- HTML报告
- 可视化图表

## 快速开始

### 安装依赖
```bash
# 安装Python依赖
pip install requests beautifulsoup4 lxml pandas

# 安装agent-browser（已安装）
npm install -g agent-browser
agent-browser install
```

### 基本使用

#### 爬取安居客数据
```bash
# Python模式
python3 scripts/anjuke_crawler.py

# agent-browser模式
bash scripts/bypass_anjuke.sh
```

#### 爬取贝壳找房数据
```bash
# agent-browser模式（已验证有效）
bash scripts/bypass_ke.sh
```

#### 爬取链家数据
```bash
# 需要验证码处理的链家爬虫
bash scripts/bypass_lianjia.sh
```

## 主要脚本

### 1. `anjuke_crawler.py`
- Python脚本爬取安居客数据
- 使用requests库
- 包含反爬虫机制

### 2. `bypass_anjuke.sh`
- Shell脚本使用agent-browser
- 模拟真实浏览器行为
- 绕过安居客反爬虫

### 3. `bypass_ke.sh`
- Shell脚本爬取贝壳找房
- 使用移动设备UA
- 已验证可绕过验证码

### 4. `bypass_lianjia.sh`
- Shell脚本爬取链家
- 包含验证码处理策略
- 可能需要人工干预

### 5. `real_estate_crawler.py`
- 通用房产爬虫程序
- 支持四个网站
- 可配置反爬虫参数

## 配置文件

### `config/real_estate_config.py`
```python
CONFIG = {
    "anjuke": {
        "name": "安居客",
        "url": "https://www.anjuke.com",
        "anti_crawler_level": "高",
        "anti_crawler_tips": "安居客有较强的反爬虫机制，需要模拟人类行为、使用随机延迟、设置cookie"
    },
    "ke": {
        "name": "贝壳找房",
        "url": "https://www.ke.com",
        "anti_crawler_level": "较高",
        "anti_crawler_tips": "贝壳找房对爬虫有较强的检测，建议使用代理IP、会话管理、模拟移动设备"
    },
    "lianjia": {
        "name": "链家",
        "url": "https://www.lianjia.com",
        "anti_crawler_level": "高",
        "anti_crawler_tips": "链家有很强的验证码机制，建议：1) 使用真实Cookie（先手动完成一次验证）；2) 设置Referer和来源页；3) 使用代理IP；4) 限制访问频率"
    },
    "soufun": {
        "name": "搜房网",
        "url": "https://www.soufun.com",
        "anti_crawler_level": "中",
        "anti_crawler_tips": "搜房网反爬虫机制相对温和，但仍需注意频率控制"
    }
}
```

## 已验证的绕过策略

### 贝壳找房（已验证成功）
```bash
# 设置移动设备UA
agent-browser set device "iPhone 14"
agent-browser set viewport 375 812
agent-browser set headers '{
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
}'

# 访问页面
agent-browser open "https://bj.ke.com/ershoufang"
agent-browser wait 5000
```

### 链家（部分页面成功）
```bash
# 访问城市页面（无验证码）
agent-browser open "https://www.lianjia.com/city/"
agent-browser wait 4000

# 二手房页面可能需要验证码处理
agent-browser open "https://www.lianjia.com/ershoufang/bj/"
agent-browser wait 5000

# 如果出现验证码，需要人工干预
agent-browser pause
# 手动完成验证码
agent-browser continue
```

### 安居客（基于历史经验）
```bash
# 设置桌面浏览器UA
agent-browser set viewport 1920 1080
agent-browser set headers '{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}'

# 设置cookie模拟真实用户
agent-browser cookies set "ctid" "16"
agent-browser cookies set "twe" "2"
agent-browser cookies set "obtain_by" "3"
```

## 数据结构

房产数据包含以下字段：
```json
{
    "title": "房源标题",
    "price": "总价（万元）",
    "avg_price": "均价（元/㎡）",
    "area": "面积（㎡）",
    "location": "位置",
    "house_type": "户型",
    "age": "建筑年代",
    "orientation": "朝向",
    "decoration": "装修状态",
    "source": "来源网站",
    "url": "房源URL",
    "timestamp": "爬取时间"
}
```

## 使用示例

### 爬取贝壳找房北京二手房
```bash
# 使用agent-browser
bash scripts/bypass_ke.sh

# 或者使用Python脚本
python3 scripts/real_estate_crawler.py -w ke -c "北京" -p 1 -o ke_properties.json
```

### 爬取安居客南京房产数据
```bash
bash scripts/bypass_anjuke.sh
```

### 批量爬取多个城市
```python
python3 scripts/batch_crawler.py \
  --websites "anjuke,ke" \
  --cities "北京,上海,广州,深圳" \
  --pages 3 \
  --format "csv"
```

## 常见问题

### Q1: 遇到验证码怎么办？
- 使用agent-browser pause命令暂停脚本
- 手动完成验证码
- 使用agent-browser continue继续执行
- 保存会话状态（agent-browser state save）

### Q2: 爬虫被封禁怎么办？
- 更换代理IP
- 更换User-Agent
- 降低访问频率（增加延迟）
- 使用不同的设备指纹

### Q3: 数据提取不准确怎么办？
- 更新HTML选择器
- 使用正则表达式改进匹配规则
- 使用agent-browser查看实际页面结构
- 手动验证数据格式

### Q4: 如何提高爬取效率？
- 使用代理IP池
- 并行爬取多个城市
- 优化HTML解析算法
- 缓存已验证的会话

## 文件结构

```
real-estate-crawler/
├── SKILL.md              # 技能文档
├── README.md             # 使用指南
├── main.py               # 主程序入口
├── scripts/
│   ├── anjuke_crawler.py        # 安居客爬虫
│   ├── bypass_anjuke.sh         # 安居客反爬虫脚本
│   ├── bypass_ke.sh             # 贝壳找房脚本（已验证）
│   ├── bypass_lianjia.sh        # 链家脚本（需要验证码处理）
│   ├── bypass_soufun.sh         # 搜房网脚本
│   ├── real_estate_crawler.py   # 通用爬虫
│   └── batch_crawler.py        # 批量爬取脚本
├── config/
│   ├── real_estate_config.py    # 网站配置
│   ├── user_agents.txt          # User-Agent列表
│   └── proxy_list.txt           # 代理IP列表
├── docs/
│   ├── captcha_strategies.md    # 验证码绕过策略
│   ├── anti_crawler_guide.md    # 反爬虫指南
│   └── data_extraction.md       # 数据提取指南
└── output/
    ├── data/
    ├── screenshots/
    └── logs/
```

## 更新日志

### v1.0.0 (2026-03-26)
- ✅ 整合安居客爬虫（已验证）
- ✅ 整合贝壳找房爬虫（已验证可绕过）
- ✅ 添加链家爬虫（部分页面需要验证码）
- ✅ 完整的反爬虫策略文档
- ✅ 多种爬取模式支持
- ✅ 数据导出功能

## 法律与伦理

### 使用建议
1. **遵守网站条款**：不要违反网站的服务协议
2. **数据使用限制**：仅用于合法目的和研究
3. **频率控制**：避免影响网站正常运营
4. **隐私保护**：不收集个人隐私信息

### 建议频率
- 每批次不超过100个请求
- 每小时不超过1000个请求
- 每天不超过5000个请求

## 联系方式

如有问题或建议，请联系技能开发者。

---

**警告**: 使用本技能爬取数据时，请遵守相关法律和网站条款。