# 同程特价机票查询技能 v1.1.0 发布说明

## 概述

同程特价机票查询技能是一个专为 EasyClaw/OpenClaw 设计的智能机票查询与价格监控工具。该技能允许用户通过自然语言查询机票价格，创建价格监控订阅，并在价格下降时接收飞书推送通知。

## 版本信息

- **版本号**: 1.1.0
- **发布日期**: 2026-03-12
- **兼容性**: EasyClaw 2026.3.8+, OpenClaw 技能框架 v1
- **技能ID**: `tongcheng-cheap-flights`

## 新特性

### ✈️ 核心功能
- **自然语言查询**: 支持中文自然语言输入，如"帮我查一下3月16日北京到上海的机票"
- **实时价格获取**: 通过同程旅行官方数据源获取实时航班价格
- **多城市支持**: 支持国内主要城市与机场代码自动映射
- **智能日期解析**: 自动解析"今天"、"明天"、"下周"等相对日期

### 📊 价格监控系统
- **订阅管理**: 创建、查看、删除价格监控订阅
- **定时监控**: 自动定时查询价格波动（默认6小时/次）
- **降价推送**: 价格下降≥5元时自动发送飞书通知
- **价格历史**: 记录价格变化趋势，提供购买建议

### 🔧 技术特性
- **三重查询模式**: API查询 + 浏览器自动化（备用） + 模拟数据（开发）
- **健壮的错误处理**: 网络异常自动重试，数据解析容错
- **详细日志系统**: 完整的操作日志便于调试
- **配置化管理**: 通过JSON配置文件自定义监控参数

## 安装指南

### 快速安装（推荐）
```bash
# 进入技能目录
cd tongcheng-cheap-flights

# 运行一键安装脚本
python3 install.py
```

### 手动安装
1. **安装Python依赖**
   ```bash
   pip install requests dateparser
   ```

2. **注册技能到EasyClaw**
   ```bash
   python3 scripts/easyclaw_register_skill.py .
   ```

3. **配置飞书推送**（可选）
   - 在飞书群聊中添加机器人，获取Webhook地址
   - 编辑 `~/.easyclaw/skills/tongcheng-cheap-flights/config.json`
   - 设置 `feishu_webhook` 字段

## 使用方法

### 在EasyClaw会话中
技能会自动识别以下类型的查询：

#### 1. 机票价格查询
```
"帮我查一下北京到上海的机票"
"3月16日成都到广州的航班价格"
"明天深圳到北京的机票"
"查询上海到重庆最便宜的航班"
```

#### 2. 价格监控订阅
```
"监控北京到上海机票价格"
"订阅成都到广州的航班CA1611"
"设置广州到深圳的价格提醒"
```

#### 3. 订阅管理
```
"查看我的机票订阅"
"删除北京到上海的监控"
"更新监控频率为12小时"
```

### 直接API调用
```python
from easyclaw_query import query_tongcheng_prices

# 自然语言查询
result = query_tongcheng_prices("帮我查一下北京到上海的机票")
print(result)

# 获取价格监控
from scripts.monitor_prices import check_all_subscriptions
check_all_subscriptions()
```

## 文件结构

```
tongcheng-cheap-flights/
├── _meta.json                    # OpenClaw技能元数据
├── .easyclaw-metadata.json      # EasyClaw技能元数据
├── SKILL.md                     # 技能详细说明文档
├── RELEASE.md                   # 本发布说明
├── README.md                    # 用户手册
├── install.py                   # 一键安装脚本
├── package.sh                   # 打包脚本
├── easyclaw_query.py            # EasyClaw封装查询接口
├── scripts/                     # 核心脚本目录
│   ├── natural_language_parser.py  # 自然语言解析器
│   ├── tongcheng_api.py            # 核心API查询类
│   ├── easyclaw_register_skill.py  # 技能注册脚本
│   ├── create_subscription.py      # 创建订阅脚本
│   ├── monitor_prices.py           # 定时监控脚本
│   └── send_notification.py        # 发送通知脚本
├── assets/                      # 资源文件
│   ├── config_template.json     # 配置文件模板
│   └── example_response.json    # API响应示例
├── references/                  # 参考文档
│   ├── api_documentation.md     # API参数说明
│   ├── city_airport_codes.md    # 城市与机场代码映射
│   └── natural_language_examples.md # 自然语言示例
└── logs/                        # 日志目录
```

## 配置说明

### 主要配置项
```json
{
  "feishu_webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx",
  "monitor_interval_hours": 6,
  "price_drop_threshold": 5,
  "max_flights_display": 10,
  "log_level": "INFO",
  "query_mode": "api"  # api|browser|mock
}
```

### 飞书推送配置
1. 在飞书群聊中创建自定义机器人
2. 获取Webhook URL
3. 更新配置文件中的 `feishu_webhook` 字段
4. 重启EasyClaw服务

## 技术实现细节

### 数据源
- **主数据源**: `ly.com` 同程旅行主站航班查询页面
- **备用数据源**: `wx.17u.cn` API接口
- **数据格式**: HTML页面嵌入的JSON状态数据

### 查询流程
1. **自然语言解析** → 使用正则表达式和日期库提取查询参数
2. **城市代码映射** → 将中文城市名转换为机场三字码
3. **API请求** → 构造URL参数发送HTTP请求
4. **数据提取** → 从HTML中解析 `window.__INITIAL_STATE__` JSON
5. **结果处理** → 过滤、排序、分析价格趋势
6. **格式输出** → 生成易读的Markdown/文本结果

### 监控系统
- **订阅存储**: JSON文件存储订阅信息
- **定时任务**: 通过EasyClaw cron系统调度
- **价格比较**: 记录历史价格，检测降价幅度
- **通知发送**: 异步发送飞书Webhook请求

## 已知问题与限制

### 当前版本
1. **数据源稳定性**: `wx.17u.cn` API返回HTML而非纯JSON，需要额外解析
2. **城市覆盖**: 仅支持国内主要城市，部分小城市可能无法识别
3. **价格更新频率**: 同程数据更新频率约为15-30分钟
4. **浏览器模式**: 备用浏览器自动化模式依赖Playwright，需要额外安装

### 解决方案
- 已实现 `ly.com` 作为主数据源，提供更稳定的数据解析
- 持续更新城市机场代码数据库
- 添加重试机制和备用数据源
- 提供清晰的错误提示和日志

## 更新日志

### v1.1.0 (2026-03-12)
- ✅ 新增 `ly.com` 主数据源支持，提高查询稳定性
- ✅ 完善自然语言解析器，支持更多查询格式
- ✅ 添加价格趋势分析和购买建议功能
- ✅ 实现飞书Webhook降价推送
- ✅ 创建一键安装脚本和打包脚本
- ✅ 添加详细日志系统和错误处理
- ✅ 提供完整的API文档和示例

### v1.0.0 (2026-03-12)
- ✅ 基础技能框架搭建
- ✅ 自然语言解析功能实现
- ✅ `wx.17u.cn` API查询功能
- ✅ 价格监控订阅系统
- ✅ 基础配置文件管理

## 贡献指南

欢迎提交Issue和Pull Request来改进本技能：

1. **问题反馈**: 在GitHub仓库创建Issue，描述问题或建议
2. **功能开发**: Fork仓库，创建功能分支，提交Pull Request
3. **文档改进**: 帮助完善文档、添加使用示例
4. **测试反馈**: 测试技能功能并报告问题

## 许可证

本技能采用 MIT 许可证开源，仅供个人学习和研究使用。请遵守同程旅行网站的使用条款，不要过度频繁访问其服务。

## 支持与联系方式

- **技能作者**: 刀盾狗 (OpenClaw社区)
- **问题反馈**: 通过OpenClaw技能仓库Issue页面
- **更新通知**: 关注OpenClaw技能市场更新

---

**感谢使用同程特价机票查询技能！祝您旅途愉快！**