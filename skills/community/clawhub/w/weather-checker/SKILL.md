---
name: weather-checker
description: "Command-line weather checker tool with global city support, temperature, precipitation, and probability display with emoji formatting"
homepage: https://github.com/yourusername/weather-checker
metadata: {"openclaw": {"emoji": "🌤️", "requires": {"bins": ["python3"]}}}
---

# Weather Checker 技能

一个功能完整的命令行天气查询工具，使用Open-Meteo API获取实时天气数据。

## 功能特性

- 🌍 支持全球城市查询
- 📅 支持今天到未来7天的天气预报
- 🌡️ 显示最高/最低温度
- 💧 显示降水量和降水概率
- 🎨 三种输出格式：漂亮格式、简单格式、JSON格式
- 🎯 智能emoji匹配和颜色显示

## 安装方法

### 1. 安装Python依赖
```bash
pip3 install requests --user
```

### 2. 下载脚本
```bash
curl -O https://raw.githubusercontent.com/yourusername/weather-checker/main/weather_checker.py
chmod +x weather_checker.py
```

### 3. 创建全局命令（可选）
```bash
sudo ln -sf $(pwd)/weather_checker.py /usr/local/bin/weather-checker
```

## 使用方法

### 基本查询
```bash
# 查询北京明天的天气（默认）
weather-checker

# 查询上海明天的天气
weather-checker -c shanghai

# 查询广州后天的天气
weather-checker -c guangzhou -d 2
```

### 输出格式
```bash
# 漂亮格式（默认）
weather-checker

# 简单格式
weather-checker -f simple

# JSON格式
weather-checker -f json
```

### 其他选项
```bash
# 查询今天天气
weather-checker -d 0

# 列出预定义城市
weather-checker -l

# 查询国际城市
weather-checker -c "new york"
weather-checker -c "london"
```

## 输出示例

**漂亮格式：**
```
🌤️ 天气查询结果 🌤️

地点: 北京
日期: 2026-02-26
天气: 🌦️ 小雨
温度: 3.8°C ~ 8.3°C
降水量: 💧 0.8mm
降水概率: 🌤️ 20%
```

**简单格式：**
```
『北京 2026-02-26 🌦️小雨 3.8°C~8.3°C 💧0.8mm 🌤️20%』
```

## 技术细节

- **API**: 使用Open-Meteo免费API，无需API密钥
- **数据**: 温度、降水量、降水概率、天气描述
- **城市**: 内置中国主要城市，支持全球城市地理编码
- **错误处理**: 完善的网络超时和错误提示

## 开发说明

如需修改或扩展功能，请编辑 `weather_checker.py` 文件。主要可扩展功能包括：
- 添加更多天气参数（风速、湿度等）
- 支持历史天气查询
- 添加图表输出
- 多城市批量查询

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！