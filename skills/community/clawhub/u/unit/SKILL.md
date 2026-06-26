---
name: unit
description: 单位全能换算技能，支持长度、重量、面积、体积、温度、时间、速度、数据存储、能量、功率、压力等基础单位换算，以及150+货币实时汇率换算。
compatibility: opencode
---

## 技能概述

本技能为OpenCode代理提供完整的单位换算能力，包括：

- **离线固定系数换算**：长度、重量、面积、体积、时间、速度、数据存储、能量、功率、压力
- **温度转换**：摄氏度、华氏度、开尔文（非线性公式）
- **实时货币汇率换算**：支持全球150+货币（需联网）

当用户提出任何单位换算请求时，代理应使用本技能提供的脚本或内置知识来计算并返回结果。

## 支持的离线单位类别及别名

### 长度（基准：米）
m, meter, meters, 米, km, kilometer, kilometers, 千米, cm, centimeter, centimeters, 厘米, mm, millimeter, millimeters, 毫米, mi, mile, miles, 英里, ft, foot, feet, 英尺, in, inch, inches, 英寸, yd, yard, yards, 码, nmi, nautical_mile, nautical_miles, 海里, 里, 丈, 尺, 寸

### 重量（基准：千克）
kg, kilogram, kilograms, 千克, g, gram, grams, 克, mg, milligram, milligrams, 毫克, t, ton, tons, 吨, lb, pound, pounds, 磅, oz, ounce, ounces, 盎司, 斤, 两, 钱

### 面积（基准：平方米）
m2, sq_m, square_meter, square_meters, 平方米, km2, sq_km, square_kilometer, 平方千米, ha, hectare, hectares, 公顷, mu, 亩, sq_ft, square_foot, 平方英尺, sq_in, square_inch, 平方英寸, sq_yd, square_yard, 平方码

### 体积/容积（基准：立方米）
m3, cubic_meter, 立方米, l, L, liter, litre, 升, ml, mL, milliliter, millilitre, 毫升, cm3, cubic_centimeter, 立方厘米, gal_us, gallon_us, us_gallon, gal_uk, gallon_uk, uk_gallon, 加仑, qt, quart, quarts, 夸脱, pt, pint, pints, 品脱, cup, cups, 杯

### 时间（基准：秒）
s, sec, second, seconds, 秒, min, minute, minutes, 分钟, h, hr, hour, hours, 小时, d, day, days, 天, wk, week, weeks, 周, mo, month, months, 月（平均）, yr, year, years, 年（平均）, ms, millisecond, milliseconds, 毫秒, us, microsecond, microseconds, 微秒

### 速度（基准：米/秒）
m/s, meter_per_second, 米/秒, km/h, kilometer_per_hour, 千米/小时, mph, mile_per_hour, 英里/小时, ft/s, foot_per_second, 英尺/秒, mach, 马赫

### 数据存储（基准：比特）
b, bit, bits, 比特, B, byte, bytes, 字节, KB, kilobyte, MB, megabyte, GB, gigabyte, TB, terabyte, PB, petabyte（二进制 1024 进制）

### 能量（基准：焦耳）
J, joule, joules, 焦耳, cal, calorie, calories, 卡路里（4.184 J）, kcal, kilocalorie, 千卡（4184 J）, kWh, 千瓦时（3.6e6 J）, eV, electronvolt, 电子伏特

### 功率（基准：瓦）
W, watt, watts, 瓦, kW, kilowatt, 千瓦, hp, horsepower, 马力（≈745.7 W）, metric_hp, metric_horsepower, 公制马力（≈735.5 W）

### 压力（基准：帕斯卡）
Pa, pascal, 帕斯卡, kPa, kilopascal, 千帕, MPa, megapascal, 兆帕, bar, 巴, atm, standard_atmosphere, 标准大气压, mmHg, mmhg, 毫米汞柱

## 货币（实时汇率，需联网）

支持超过 150 种货币，常见代码及别名：

USD, dollar, dollars, 美元
EUR, euro, euros, 欧元
CNY, rmb, yuan, renminbi, 人民币
JPY, yen, 日元
GBP, pound, pounds, 英镑
HKD, 港元
AUD, 澳元
CAD, 加元
CHF, 瑞士法郎
SGD, 新加坡元
INR, 印度卢比
RUB, 卢布
BRL, 巴西雷亚尔
KRW, 韩元
THB, 泰铢
MYR, 马来西亚林吉特
... 及更多

汇率数据来源：[exchangerate.host](https://exchangerate.host)，免费无需密钥，每小时缓存一次。

## 使用方法

### 推荐调用脚本

本技能附带一个 Python 脚本 `unit/unit_converter.py`，它实现了所有换算逻辑。代理应优先使用该脚本以确保准确性。

**调用方式**（在终端中执行）：
```bash
python unit/unit_converter.py convert <数值> <源单位> <目标单位>
```

示例：
```bash
python unit/unit_converter.py convert 100 meters feet
python unit/unit_converter.py convert 25 Celsius Fahrenheit
python unit/unit_converter.py convert 100 USD CNY
```

脚本输出为纯文本结果，例如：`100 meters = 328.084 feet`。

### 脚本依赖

运行脚本需要 `requests` 库。如未安装，请先执行：
```bash
pip install requests
```

### 备用方案（脚本不可用时）

如果脚本不可用，代理可根据以下规则手动计算：

1. **温度**：使用专用公式（见下文）。
2. **离线单位**：找到两个单位对应的换算系数（相对于基准单位），然后计算：
   ```
   目标值 = 输入值 × (源单位系数) / (目标单位系数)
   ```
3. **货币**：必须联网调用 API。如果脚本失败，可尝试直接使用 `requests` 调用 `https://api.exchangerate.host/latest?base=<源货币>` 获取汇率并计算。

## 温度转换公式（备用）

- 摄氏度 → 华氏度：F = C × 9/5 + 32
- 华氏度 → 摄氏度：C = (F - 32) × 5/9
- 开尔文 → 摄氏度：C = K - 273.15
- 摄氏度 → 开尔文：K = C + 273.15
- 华氏度 → 开尔文：K = (F + 459.67) × 5/9
- 开尔文 → 华氏度：F = K × 9/5 - 459.67

## 常见示例

| 用户输入 | 代理应执行 | 结果示例 |
|---------|-----------|---------|
| 把100米换算成英尺 | `python unit/unit_converter.py convert 100 m ft` 或手动：100 × 0.3048? Actually 1 m = 3.28084 ft → 328.084 ft | 100 米 ≈ 328.084 英尺 |
| 25摄氏度等于多少华氏度？ | 使用公式：25 × 9/5 + 32 = 77 | 77°F |
| 100美元兑换人民币 | 调用脚本获取实时汇率，假设 1 USD = 7.2 CNY → 720 CNY | 约 720 元（汇率浮动） |
| 5公斤是多少斤？ | 5 × (1 kg / 0.5 kg) = 10 斤 | 10 斤 |
| 1英里每小时等于多少米每秒？ | 1 mph = 0.44704 m/s → 0.44704 | 0.44704 m/s |

## 注意事项

- 货币汇率实时变动，结果仅供参考，实际交易以银行牌价为准。
- 温度转换有专门公式，不能使用线性系数。
- 体积单位中美制/英制加仑不同，脚本已区分 `gal_us` 与 `gal_uk`。
- 中文传统单位（里、丈、尺、寸、斤、两、钱、亩）基于市制，可能存在地区差异，使用请注意。
- 数据存储单位（KB/MB/GB等）采用二进制前缀（1 KB = 1024 字节），符合常见计算机存储习惯。
- 时间单位中的“月”和“年”使用平均长度（分别为 2629746 秒和 31557600 秒），实际月份/年份可能有±1天差异。

## 故障排除

- **脚本找不到**：确保 `unit/unit_converter.py` 文件与 `SKILL.md` 在同一目录（即 `.opencode/skills/unit/` 下）。
- **Python 或 requests 未安装**：提示用户安装 Python 3 和 `pip install requests`。
- **网络错误（货币换算）**：检查网络连接，或稍后重试。
- **不支持的货币**：确认货币代码正确，常见代码见上文列表。

## 扩展性

若需新增单位，只需在 `unit/unit_converter.py` 的相应字典中添加别名和系数即可。脚本范围涵盖大多数日常需求，150+ 货币通过在线 API 自动支持。