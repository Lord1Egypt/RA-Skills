---
name: qweather-china
description: "基于中国气象局数据的完整天气服务，通过和风天气API提供实时天气、天气预报、生活指数、空气质量等全方位天气信息。专为中国用户优化，数据更准确，功能更全面。"
version: "1.2.2"
homepage: https://dev.qweather.com/
author: uni-huang
license: MIT-0
metadata:
  openclaw:
    emoji: "🇨🇳"
    requires:
      bins: ["python3", "curl"]
      env:
        required:
          - QWEATHER_API_HOST
          - QWEATHER_PROJECT_ID
          - QWEATHER_CREDENTIALS_ID
          - QWEATHER_PRIVATE_KEY_PATH
        optional:
          - QWEATHER_DEFAULT_LOCATION
          - QWEATHER_CACHE_DIR
    permissions:
      filesystem:
        read:
          - ~/.config/qweather/config.json
          - ~/.config/qweather/private.pem
          - ~/.cache/qweather/
        write:
          - ~/.cache/qweather/
      network:
        endpoints:
          - "*.qweatherapi.com"
---

# QWeather China Skill

基于中国气象局数据的完整天气服务Skill，提供准确、本地化的天气信息。

## 目标
给用户提供可靠的实时天气与预报（不依赖通用 web_search）。
自动处理地点输入（城市名/经纬度/locationId）。
支持"今天/明天/后天/未来N天"等表达。

## 触发条件
用户提到：天气、气温、下雨、降温、风、湿度、预报、今天/明天/后天、未来几天。
一旦判定是天气问题，优先本 skill。

## 功能特点

### ✅ 核心功能
1. **实时天气** - 当前温度、体感温度、湿度、风速、降水等
2. **天气预报** - 3天/7天详细预报，包含白天夜间天气
3. **生活指数** - 穿衣、洗车、运动、紫外线等生活建议
4. **空气质量** - 实时AQI、污染物浓度
5. **天气预警** - 官方天气预警信息

### ✅ 数据优势
- **数据源**: 中国气象局官方数据
- **准确性**: 针对中国气候特点优化
- **本地化**: 中文天气描述，符合中国用户习惯
- **完整性**: 日出日落、月相、能见度等全方位信息

### ✅ 用户体验
- **智能建议**: 基于天气的穿衣、出行建议
- **多城市支持**: 支持全国主要城市
- **缓存优化**: 减少API调用，提高响应速度
- **错误处理**: 完善的错误处理和降级机制
- **智能地点处理**: 自动识别城市名、经纬度、locationId
- **自然语言理解**: 支持"今天/明天/后天/未来N天"等表达

## 工作流

### 1. 获取地点
- 若用户提供地点：调用 `qweather_location_lookup({location})`
- 若未提供地点：
  - 若 env 存在 `QWEATHER_DEFAULT_LOCATION`：使用默认地点，并明确说明"按默认地点查询"
  - 否则追问用户城市/地点

### 2. 判断查询类型
- **"现在/当前/实时"**：调用 `weather_now({location})`
- **"今天/明天/后天/未来N天"**：调用 `weather_forecast({location, days})`
  - 建议 days 映射：
    - 今天：days=1
    - 明天：days=2（输出前2天，重点标明第2天）
    - 后天：days=3（重点标明第3天）
    - "未来几天"：默认 days=3；用户说 N 天则用 N（上限 15）

### 3. 输出格式
- **地点**：解析后的 name
- **实时**：天气现象、气温/体感、湿度、风向风力、观测时间
- **预报**：每天最高/最低、白天/夜间天气、降水（如有）、风力

## 约束
- **不要使用 web_search 代替天气数据源**。
- **API 失败时**：返回明确错误，并提示检查环境变量：
  - `QWEATHER_API_HOST` - API 主机地址
  - `QWEATHER_PROJECT_ID` - 项目ID (sub)
  - `QWEATHER_CREDENTIALS_ID` - 凭据ID (kid)
  - `QWEATHER_PRIVATE_KEY_PATH` - 私钥文件路径（建议使用 `~/.config/qweather/private.pem`）
- **默认地点**：使用 `QWEATHER_DEFAULT_LOCATION` 设置默认查询地点
- **安全注意**：私钥文件应存放在独立目录（如 `~/.config/qweather/`），并设置 600 权限

## 跨平台兼容性

### ✅ 完全支持的操作系统
- **Windows** (7/8/10/11, Server 2012+)
- **Linux** (Ubuntu, Debian, CentOS, Fedora, etc.)
- **macOS** (10.15+)

### ✅ 编码自动处理
- **Windows控制台**：自动处理GBK编码，将Unicode表情转换为文本描述
- **Linux/macOS终端**：原生支持UTF-8，完整显示Unicode字符
- **智能检测**：运行时自动检测系统编码并适配

### ✅ 新增工具模块
- **encoding_utils.py**：编码处理核心模块
- **safe_print()函数**：替代标准print，自动处理编码
- **系统检测**：自动识别平台和编码设置

### ✅ 向后兼容
- 完全兼容v1.1.0的所有功能
- 现有配置无需修改
- API接口保持不变

## 配置要求

### 必需配置
1. **和风天气API认证**（通过环境变量或 config.json 配置）
   - `QWEATHER_API_HOST`: API 主机地址（如 `p54up4xhmm.re.qweatherapi.com`）
   - `QWEATHER_PROJECT_ID`: 项目ID (sub)
   - `QWEATHER_CREDENTIALS_ID`: 凭据ID (kid)
   - `QWEATHER_PRIVATE_KEY_PATH`: 私钥文件路径（如 `~/.config/qweather/private.pem`）

2. **私钥文件准备**
   ```bash
   # 创建配置目录
   mkdir -p ~/.config/qweather
   
   # 将和风天气私钥复制到独立位置
   cp /path/to/your/qweather-private.pem ~/.config/qweather/private.pem
   chmod 600 ~/.config/qweather/private.pem
   ```

3. **Python依赖**（安装时自动处理）
   - `pyjwt>=2.0.0`
   - `cryptography>=3.0`
   - `requests>=2.25`

### 可选配置
- `QWEATHER_DEFAULT_LOCATION`: 默认查询城市
- `QWEATHER_CACHE_DIR`: 缓存目录（默认 `~/.cache/qweather`）

## 使用方法

### 基本查询
```bash
# 查询北京实时天气
python qweather.py now --city beijing

# 查询3天预报
python qweather.py forecast --city beijing --days 3

# 查询生活指数
python qweather.py indices --city beijing

# 查询空气质量
python qweather.py air --city shanghai

# 完整天气报告
python qweather.py full --city guangzhou
```

### OpenClaw集成
在OpenClaw中直接使用自然语言查询：

```
用户: 北京天气怎么样？
助手: 🌤️ 北京当前天气...

用户: 上海未来3天预报
助手: 📅 上海未来3天预报...

用户: 广州生活指数
助手: 📊 广州今日生活指数...

用户: 杭州空气质量
助手: 🌫️ 杭州空气质量...

用户: 深圳需要带伞吗？
助手: 🌂 深圳建议带雨伞...

用户: 成都穿什么？
助手: 👕 成都穿衣建议...
```

### 支持的自然语言查询
1. `[城市]天气` - 查询实时天气
2. `[城市]温度` - 查询当前温度  
3. `[城市]今天/明天/后天天气` - 查询特定日期
4. `[城市]预报` - 查询3天预报
5. `[城市]未来N天预报` - 查询N天预报
6. `[城市]生活指数` - 查询生活指数
7. `[城市]空气质量` - 查询空气质量
8. `[城市]需要带伞吗` - 雨伞建议
9. `[城市]穿什么` - 穿衣建议
10. `天气帮助` - 显示帮助信息

### 支持的城市
- **北京** (beijing)
- **上海** (shanghai) 
- **广州** (guangzhou)
- **深圳** (shenzhen)
- **杭州** (hangzhou)
- **成都** (chengdu)
- **武汉** (wuhan)
- **南京** (nanjing)
- **西安** (xian)
- **重庆** (chongqing)

或直接使用城市代码：`101010100` (北京)

## API端点

### 天气相关
- `/v7/weather/now` - 实时天气
- `/v7/weather/3d` - 3天预报
- `/v7/weather/7d` - 7天预报
- `/v7/weather/24h` - 24小时预报

### 生活指数
- `/v7/indices/1d` - 今日生活指数
- `/v7/indices/3d` - 3天生活指数

### 环境数据
- `/v7/air/now` - 实时空气质量
- `/v7/air/5d` - 5天空气质量预报

### 预警信息
- `/v7/warning/now` - 当前预警
- `/v7/warning/list` - 预警列表

## 城市代码

常用城市代码：
- 北京: `101010100`
- 上海: `101020100`
- 广州: `101280101`
- 深圳: `101280601`
- 杭州: `101210101`

完整城市代码参考：https://dev.qweather.com/docs/resource/city/

## 错误处理

### 常见错误
- `400`: 请求参数错误
- `401`: 认证失败
- `403`: 权限不足
- `404`: 城市不存在
- `429`: 请求频率超限
- `500`: 服务器错误

### 降级策略
1. 缓存上次成功的数据
2. 使用备用数据源（Open-Meteo）
3. 返回友好的错误提示

## 性能优化

### 缓存策略
- 实时数据: 10分钟缓存
- 预报数据: 1小时缓存
- 生活指数: 3小时缓存
- 空气质量: 30分钟缓存

### 请求优化
- 批量请求减少API调用
- 智能重试机制
- 连接池复用

## 更新日志

### v1.2.2 (2026-04-13)
- **🔒 安全合规更新**：
  - 在 skill.yaml 中完整声明所有必需环境变量及其用途
  - 在 skill.yaml 中详细声明文件系统权限和网络端点
  - 在 config.json 中将敏感值改为占位符格式 (YOUR_*)
  - 添加安全说明和风险评估
  - 添加安装前注意事项
- **📋 元数据修复**：解决 ClawHub 安全扫描中的元数据不匹配问题

### v1.2.1 (2026-04-13)
- **🔧 修复发布问题**：解决 ClawHub 发布中的文件路径问题

### v1.2.0 (2026-04-12)
- **🔒 安全修复**：私钥路径改为独立目录（`~/.config/qweather/`），不再读取 OpenClaw 代理私钥
- **✨ 环境变量支持**：新增 `QWEATHER_PROJECT_ID`, `QWEATHER_CREDENTIALS_ID` 等环境变量
- **📦 ClawHub 兼容**：新增 `skill.yaml` 文件，支持通过 ClawHub 安装
- **📝 配置简化**：支持 `~` 路径自动展开，跨平台配置更简单
- **🔧 权限修复**：明确声明文件系统权限，避免安全风险

### v1.1.1 (2026-03-15)
- **跨平台兼容性**：完全支持Windows、Linux、macOS系统
- **编码自动处理**：智能处理不同系统的编码问题
- **安全输出函数**：使用safe_print替代print，避免编码错误
- **表情符号兼容**：自动将Unicode表情转换为文本描述

### v1.1.0 (2026-03-15)
- **智能地点处理**：自动识别城市名、经纬度、locationId
- **自然语言理解**：支持"今天/明天/后天/未来N天"等表达
- **默认地点支持**：支持QWEATHER_DEFAULT_LOCATION环境变量
- **优化触发条件**：明确的天气相关关键词触发
- **改进错误处理**：API失败时返回明确错误提示
- **简洁工作流**：获取地点 → 判断查询类型 → 调用对应API

### v1.0.0 (2026-03-13)
- 初始版本发布
- 支持实时天气和3天预报
- 基础的生活指数查询
- JWT认证集成

## 贡献指南

1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

基于和风天气API服务条款，仅供个人和非商业使用。

## 技术支持

- 和风天气文档: https://dev.qweather.com/docs/
- 问题反馈: 通过GitHub Issues
- 紧急支持: 联系和风天气客服