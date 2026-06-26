# 同程特价机票查询技能

## 简介

基于同程旅行（17u.cn）API的特价机票查询与价格监控技能。支持自然语言输入查询机票价格、创建价格监控订阅、降价推送（飞书）等功能。

## 功能特性

- ✈️ **自然语言查询**：支持“帮我查一下3.16日北京到成都的机票价格”等自然语句
- 📊 **实时价格查询**：通过API获取实时航班价格信息
- 🔔 **价格监控**：创建订阅任务，定时监控价格波动
- 📱 **降价推送**：支持飞书Webhook推送降价通知
- 📈 **价格分析**：自动分析价格趋势，提供购买建议
- 🔧 **多模式查询**：支持API查询和浏览器自动化（备用）

## 快速安装

### 方法一：使用安装脚本（推荐）

```bash
# 进入技能目录
cd tongcheng-cheap-flights

# 运行安装脚本
python3 install.py
```

### 方法二：手动安装

1. **安装Python依赖**
   ```bash
   pip install requests dateparser
   ```

2. **注册技能到EasyClaw**
   ```bash
   python3 scripts/easyclaw_register_skill.py .
   ```

## 使用方法

### 在EasyClaw会话中

```python
# 技能会自动识别以下查询语句：

# 1. 查询机票价格
"帮我查一下北京到上海的机票"
"3月16日成都到广州的航班价格"
"明天深圳到北京的机票"

# 2. 创建价格监控
"监控北京到上海机票价格"
"订阅成都到广州的航班CA1611"
"设置广州到深圳的价格提醒"

# 3. 管理订阅
"查看我的机票订阅"
"删除北京到上海的监控"
```

### 直接调用API

```python
from easyclaw_query import query_tongcheng_prices

# 查询机票价格
result = query_tongcheng_prices("帮我查一下北京到上海的机票")
print(result)

# 使用自然语言解析器
from scripts.natural_language_parser import NaturalLanguageParser
parser = NaturalLanguageParser()
params = parser.parse("3月16日北京到成都的机票")
print(params)
```

## 配置说明

### 1. 配置文件
技能安装后会在 `~/.easyclaw/skills/tongcheng-cheap-flights/` 目录生成配置文件：

```json
{
  "feishu_webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx",
  "monitor_interval_hours": 6,
  "price_drop_threshold": 5,
  "log_level": "INFO"
}
```

### 2. 飞书推送配置
1. 在飞书中创建群聊机器人，获取Webhook地址
2. 将Webhook地址填入配置文件的 `feishu_webhook` 字段
3. 重启EasyClaw生效

## 文件结构

```
tongcheng-cheap-flights/
├── SKILL.md                    # 技能详细说明文档
├── .easyclaw-metadata.json     # 技能元数据
├── install.py                  # 一键安装脚本
├── README.md                   # 本文件
├── easyclaw_query.py           # EasyClaw封装查询接口
├── scripts/
│   ├── natural_language_parser.py  # 自然语言解析器
│   ├── tongcheng_api.py            # 核心API查询类
│   ├── easyclaw_register_skill.py  # 技能注册脚本
│   ├── create_subscription.py      # 创建订阅脚本
│   ├── monitor_prices.py           # 定时监控脚本
│   └── send_notification.py        # 发送通知脚本
├── assets/
│   ├── config_template.json        # 配置文件模板
│   └── example_response.json       # API响应示例
├── references/
│   ├── api_documentation.md        # API参数说明
│   ├── city_airport_codes.md       # 城市与机场代码映射
│   └── natural_language_examples.md # 自然语言示例
└── logs/                           # 日志目录
```

## 技术实现

### 查询流程
1. **自然语言解析** → 提取出发城市、到达城市、日期、航班号
2. **API查询** → 使用 `wx.17u.cn/cheapflights/newcomparepriceV2/single` API
3. **数据提取** → 解析HTML中的 `window.__INITIAL_STATE__` JSON数据
4. **结果格式化** → 按价格排序，分析价格趋势，提供购买建议

### 监控流程
1. **订阅创建** → 保存查询参数到 `subscriptions.json`
2. **定时查询** → 使用EasyClaw cron任务定时执行
3. **降价判断** → 价格下降≥5元触发推送
4. **通知发送** → 通过飞书Webhook发送降价通知

## 常见问题

### Q: 查询不到数据怎么办？
A: 
1. 检查网络连接是否正常
2. 确认城市名称是否正确（支持中文城市名）
3. 尝试使用备用查询模式
4. 查看日志文件 `logs/tongcheng.log`

### Q: 飞书推送没收到？
A:
1. 检查配置文件中的webhook地址是否正确
2. 确认飞书机器人已添加到群聊
3. 检查日志文件中的推送记录

### Q: 如何修改监控频率？
A:
编辑配置文件中的 `monitor_interval_hours` 设置（单位：小时）

## 更新日志

### v1.1.0 (2026-03-12)
- ✅ 更新API查询参数格式（使用originList/destList/dateInfo）
- ✅ 完善自然语言解析器
- ✅ 添加价格分析和购买建议
- ✅ 支持飞书降价推送
- ✅ 创建一键安装脚本

### v1.0.0 (2026-03-12)
- ✅ 基础技能框架
- ✅ 自然语言解析功能
- ✅ API查询功能
- ✅ 价格监控订阅功能

## 许可证

本技能仅供个人学习和研究使用，请勿用于商业用途或对目标网站造成过大访问压力。