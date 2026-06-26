# 房产中介网站爬虫技能

## 简介

这个技能用于爬取中国主流房产中介网站的数据，包括：
- 安居客 (anjuke.com)
- 贝壳找房 (ke.com)
- 链家 (lianjia.com)
- 搜房网 (soufun.com)

包含完整的反爬虫绕过策略和数据提取功能。

## 功能特点

1. **反爬虫绕过策略**：
   - 模拟真实浏览器指纹
   - 随机延迟避免频率检测
   - Cookie和会话管理
   - 代理IP支持
   - 验证码处理机制

2. **数据提取功能**：
   - 房价信息
   - 房产面积
   - 地理位置
   - 户型信息
   - 装修状态
   - 建筑年代

3. **多种爬取模式**：
   - Python快速爬取（适合简单的反爬虫网站）
   - agent-browser浏览器自动化（适合复杂的反爬虫网站）

4. **多种导出格式**：
   - JSON格式
   - CSV格式
   - Excel格式（需要额外安装pandas）
   - 可视化图表

## 使用方法

### 安装依赖

```bash
pip install requests beautifulsoup4 lxml pandas
```

### Python爬虫模式

```bash
# 爬取安居客数据
python main.py -w anjuke -c 北京 -p 3 -o anjuke_properties.json

# 爬取贝壳找房数据
python main.py -w ke -c 上海 -d "浦东新区" -p 2 -o ke_properties.json -f csv

# 爬取链家数据
python main.py -w lianjia -c 广州 -p 5 -o lianjia_properties.json

# 爬取搜房网数据
python main.py -w soufun -c 深圳 -d "福田区" -o soufun_properties.json
```

### agent-browser模式

```bash
# 使用浏览器自动化爬取
bash scripts/bypass_real_estate.sh
```

运行脚本后，按照提示输入：
1. 网站编号（1-4）
2. 城市名称
3. 区域名称（可选）

脚本会自动：
1. 设置浏览器指纹
2. 访问目标网站
3. 绕过反爬虫机制
4. 提取房源信息
5. 保存会话状态和数据文件

## 配置文件说明

配置文件位于 `config/real_estate_config.py`，包含：

1. **网站配置**：
   - URL和选择器
   - 数据解析规则
   - 反爬虫等级
   - 使用建议

2. **反爬虫配置**：
   - 用户代理列表
   - 延迟设置
   - 代理IP列表
   - 验证码处理策略
   - 会话管理配置

3. **数据保存配置**：
   - 输出格式选择
   - 截图保存设置
   - 目录配置

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
    "source": "来源网站"
}
```

## 反爬虫策略

### 高反爬虫网站（安居客、贝壳找房）

1. **浏览器指纹伪装**：
   ```bash
   agent-browser set device "iPhone 14"
   agent-browser set viewport 375 812
   ```

2. **随机延迟**：
   ```python
   import time
   import random
   
   delay = random.uniform(3, 8)
   time.sleep(delay)
   ```

3. **Cookie管理**：
   ```bash
   agent-browser cookies set "session_id" "your_session_value"
   ```

### 中等反爬虫网站（链家、搜房网）

1. **更换User-Agent**：
   ```bash
   agent-browser set headers '{"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"}'
   ```

2. **请求频率控制**：
   ```python
   batch_size = 10
   for i in range(batch_size):
       # 处理请求
       time.sleep(random.uniform(1, 2))
   ```

## 法律与伦理

### 注意事项
1. **遵守网站条款**：不要违反网站的服务协议
2. **数据使用限制**：仅用于合法目的和研究
3. **频率控制**：避免影响网站正常运营
4. **隐私保护**：不收集个人隐私信息

### 建议使用频率
- 每批次不超过100个请求
- 每小时不超过1000个请求
- 每天不超过5000个请求

## 更新日志

### v1.0.0 (2026-03-26)
- 初始版本发布
- 支持四个主流房产中介网站
- Python爬虫模式和agent-browser模式
- 完整的反爬虫绕过策略
- 多格式数据导出

## 常见问题

### 1. 爬虫被封禁怎么办？
- 增加延迟时间
- 更换User-Agent
- 使用代理IP
- 使用agent-browser模式

### 2. 验证码频繁出现怎么办？
- 降低请求频率
- 增加批次延迟
- 使用验证码识别服务
- 手动处理验证码

### 3. 数据提取不准确怎么办？
- 更新HTML选择器
- 检查网站结构变化
- 使用正则表达式改进匹配规则
- 使用agent-browser可视化检查

### 4. Python模式不工作怎么办？
- 检查网络连接
- 检查反爬虫策略
- 尝试agent-browser模式
- 更新选择器和匹配规则

## 联系方式

如有问题或建议，请联系技能开发者。

---

**警告**: 使用本技能爬取数据时，请遵守相关法律和网站条款。