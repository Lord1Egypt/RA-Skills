# 房产中介网站爬虫技能发布说明

## 技能基本信息

- **名称**: Real Estate Crawler
- **版本**: 1.0.0
- **作者**: 韩元东
- **许可证**: MIT
- **依赖**: Python 3.x, agent-browser
- **类别**: 数据采集/房产中介

## 技能描述

综合房产中介网站爬虫技能，专门用于爬取中国主流房产中介网站数据：

### 已验证功能：
- ✅ **贝壳找房 (ke.com)** - 已验证可绕过验证码
- ✅ **安居客 (anjuke.com)** - 基于历史经验，已有完整爬虫脚本
- ⚠️ **链家 (lianjia.com)** - 包含验证码处理策略
- 🔄 **搜房网 (soufun.com)** - 待验证

### 核心特性：
1. **多种反爬虫策略**：
   - 浏览器指纹伪装（桌面/移动设备）
   - 随机延迟和人类行为模拟
   - Cookie和会话管理
   - 代理IP支持

2. **两种爬取模式**：
   - Python快速爬取模式
   - agent-browser浏览器自动化模式

3. **验证码处理**：
   - 人工验证策略
   - 会话状态保存
   - 备用访问路径

4. **数据提取功能**：
   - 房价信息（总价、单价）
   - 房产面积
   - 地理位置
   - 户型信息
   - 装修状态
   - 建筑年代

## 已验证技术亮点

### 贝壳找房验证码绕过（已验证成功）
通过以下策略成功绕过贝壳找房验证码：
```bash
# 使用移动设备UA和指纹
agent-browser set device "iPhone 14"
agent-browser set viewport 375 812
agent-browser set headers '{"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"}'

# 随机延迟和模拟人类行为
agent-browser wait 3000
agent-browser scroll down缅500
agent-browser wait 1000
```

### 实际测试结果
**贝壳找房**：
- ✅ 可以正常访问页面
- ✅ 可以获取房产信息
- ✅ 没有触发验证码
- ✅ 可提取价格、面积等数据

## 文件结构

```
real-estate-crawler/
├── SKILL.md              # 技能文档
├── README.md             # 使用指南
├── main.py               # 主程序入口
├── scripts/
│   ├── anjuke_crawler.py        # 安居客爬虫
│   ├── ke_crawler.py            # 贝壳找房爬虫
│   ├── bypass_ke.sh             # 贝壳找房脚本
│   ├── bypass_anjuke.sh         # 安居客脚本
│   ├── bypass_lianjia.sh        # 链家脚本
│   ├── real_estate_crawler.py   # 通用爬虫
│   └── batch_crawler.py         # 批量爬取
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

## 使用示例

### 爬取贝壳找房数据
```bash
bash scripts/bypass_ke.sh
```

### 爬取安居客数据
```bash
bash scripts/bypass_anjuke.sh
```

### 使用Python爬虫
```bash
python3 scripts/anjuke_crawler.py -c "北京" -p 3 -o data.json
python3 scripts/ke_crawler.py -c "上海" -p 2 -o ke_data.csv -f csv
```

## 风险评估声明

### 网络安全合规风险
1. **网站条款合规**：爬取数据可能违反网站服务条款
2. **数据使用限制**：仅建议用于合法目的和研究
3. **IP封禁风险**：高频访问可能导致IP被封
4. **法律合规**：使用者需遵守当地相关法律法规

### 技术风险
1. **验证码处理**：可能需要人工干预
2. **数据准确性**：网站结构变化可能导致提取失败
3. **反爬虫更新**：网站反爬虫机制可能随时更新

## 建议使用场景

1. **市场调研**：房产价格趋势分析
2. **数据研究**：房地产市场数据分析
3. **竞争分析**：房产中介平台比较
4. **学术研究**：房地产市场研究

## 更新计划

### v1.0.0 (当前版本)
- ✅ 整合安居客爬虫（基于历史经验）
- ✅ 整合贝壳找房爬虫（已验证可绕过）
- ✅ 添加链家爬虫（需要验证码处理）
- ✅ 完整的反爬虫策略文档
- ✅ 多种爬取模式支持
- ✅ 数据导出功能

### 未来版本计划
- 🔄 搜房网爬虫实现
- 🔄 更多的城市支持
- 🔄 验证码自动识别
- 🔄 数据可视化功能

## 法律声明

使用本技能时，使用者需：
1. 遵守目标网站的服务条款
2. 仅用于合法目的
3. 不收集个人隐私信息
4. 控制访问频率避免影响网站服务
5. 遵守当地法律法规

## 联系方式

如需技术支持或使用指导，请联系技能作者。

---

**版权声明**：本技能由开发者独立创建，包含实际测试验证的反爬虫策略和房产数据提取功能。