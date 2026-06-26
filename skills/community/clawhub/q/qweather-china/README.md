# QWeather China Skill for OpenClaw

基于中国气象局数据的完整天气服务技能，专为OpenClaw优化。

## 🎯 功能特点

### 🌤️ 完整天气服务
- **实时天气**: 温度、湿度、风力、降水等
- **天气预报**: 3天/7天详细预报
- **生活指数**: 穿衣、洗车、运动、紫外线等
- **空气质量**: 实时AQI、污染物数据
- **天气预警**: 官方预警信息

### 🇨🇳 中国本地化
- **数据源**: 中国气象局官方数据
- **准确性**: 针对中国气候特点优化
- **中文支持**: 完整中文天气描述
- **城市覆盖**: 全国主要城市

### 🚀 高性能
- **智能缓存**: 减少API调用
- **错误恢复**: 自动降级和重试
- **快速响应**: 优化请求处理

## 📦 安装

### 自动安装
```bash
# Windows
install.bat

# Linux/Mac
chmod +x install.sh
./install.sh
```

### 手动安装
1. 复制本目录到OpenClaw技能目录
2. 安装Python依赖：
   ```bash
   pip install pyjwt cryptography requests
   ```
3. 配置私钥文件：
   ```bash
   # 创建配置目录
   mkdir -p ~/.config/qweather
   
   # 复制私钥到独立位置（推荐）
   cp /path/to/your/qweather-private.pem ~/.config/qweather/private.pem
   chmod 600 ~/.config/qweather/private.pem
   ```
4. 测试安装：
   ```bash
   python qweather.py now --city beijing
   ```

## 🔧 配置

### 环境变量配置（推荐）
在OpenClaw环境或系统环境中配置：

```bash
# 必需配置
export QWEATHER_API_HOST="p54up4xhmm.re.qweatherapi.com"
export QWEATHER_PROJECT_ID="4FKRV2BREH"
export QWEATHER_CREDENTIALS_ID="CGWFM979C7"
export QWEATHER_PRIVATE_KEY_PATH="~/.config/qweather/private.pem"

# 可选配置
export QWEATHER_DEFAULT_LOCATION="beijing"
export QWEATHER_CACHE_DIR="~/.cache/qweather"
```

### config.json 配置
也可以通过 `config.json` 配置：

```json
{
  "qweather": {
    "enabled": true,
    "api_host": "p54up4xhmm.re.qweatherapi.com",
    "jwt": {
      "kid": "CGWFM979C7",
      "sub": "4FKRV2BREH",
      "private_key_path": "~/.config/qweather/private.pem"
    },
    "cache": {
      "enabled": true,
      "directory": "~/.cache/qweather"
    }
  }
}
```

**注意**：私钥文件应存放在独立目录（如 `~/.config/qweather/`），不要与其他应用共享。

## 📖 使用方法

### 在OpenClaw中直接使用
```
用户: 北京天气怎么样？
助手: 🌤️ 北京当前天气...
```

### 命令行使用
```bash
# 实时天气
python qweather.py now --city beijing

# 3天预报
python qweather.py forecast --city shanghai --days 3

# 生活指数
python qweather.py indices --city guangzhou

# 空气质量
python qweather.py air --city hangzhou

# 完整报告
python qweather.py full --city chengdu
```

### 支持的查询格式
1. `[城市]天气` - 实时天气
2. `[城市]温度` - 当前温度
3. `[城市]今天/明天/后天天气` - 特定日期
4. `[城市]预报` - 3天预报
5. `[城市]未来N天预报` - N天预报
6. `[城市]生活指数` - 生活指数
7. `[城市]空气质量` - 空气质量
8. `[城市]需要带伞吗` - 雨伞建议
9. `[城市]穿什么` - 穿衣建议

### 支持的城市
- 北京 (beijing)
- 上海 (shanghai)
- 广州 (guangzhou)
- 深圳 (shenzhen)
- 杭州 (hangzhou)
- 成都 (chengdu)
- 武汉 (wuhan)
- 南京 (nanjing)
- 西安 (xian)
- 重庆 (chongqing)

或直接使用城市代码：`101010100` (北京)

## 🛠️ 开发

### 项目结构
```
qweather-china/
├── qweather.py          # 核心天气服务
├── openclaw_integration.py # OpenClaw集成
├── examples.py          # 使用示例
├── SKILL.md            # 技能文档
├── README.md           # 本文件
├── config.json         # 配置文件
├── openclaw_config.yaml # OpenClaw配置
├── install.bat         # Windows安装脚本
└── install.sh          # Linux安装脚本
```

### 扩展功能
1. **添加新城市**: 在`config.json`的`cities`部分添加
2. **自定义模板**: 修改`openclaw_config.yaml`的`templates`部分
3. **添加新命令**: 在`openclaw_integration.py`中添加处理函数

### 测试
```bash
# 运行示例
python examples.py

# 测试集成
python openclaw_integration.py

# 单元测试
python -m pytest tests/ -v
```

## 🔍 故障排除

### 常见问题
1. **API连接失败**
   - 检查私钥文件是否存在
   - 验证JWT认证信息
   - 检查网络连接

2. **城市找不到**
   - 确认城市名称正确
   - 检查城市代码映射

3. **响应缓慢**
   - 检查缓存设置
   - 确认网络状况

### 日志查看
```bash
# 查看缓存目录
ls "C:\Users\uni_h\.openclaw\cache\qweather"

# 调试模式
python qweather.py now --city beijing --debug
```

## 📊 数据源

### 和风天气API
- **官方文档**: https://dev.qweather.com/docs/
- **数据源**: 中国气象局
- **更新频率**: 实时更新
- **免费额度**: 1000次/天

### 数据准确性
- 温度误差: ±1°C
- 降水预报: 85%准确率
- 空气质量: 实时监测站数据

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议：

1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

基于和风天气API服务条款，仅供个人和非商业使用。

## 📞 支持

- **问题反馈**: GitHub Issues
- **文档**: [SKILL.md](SKILL.md)
- **示例**: [examples.py](examples.py)
- **和风天气支持**: https://dev.qweather.com/support

## 🎉 更新日志

### v1.0.0 (2026-03-13)
- 初始版本发布
- 完整天气服务集成
- OpenClaw优化支持
- 智能缓存和错误处理

---

**数据来源**: 中国气象局 · 和风天气  
**技能维护**: OpenClaw Team  
**最后更新**: 2026年3月13日