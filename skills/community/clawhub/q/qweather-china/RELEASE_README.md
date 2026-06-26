# qweather-china v1.2.0 发布说明

## 🎉 版本亮点

### 核心优化功能
1. **智能地点记忆** - 优先从记忆（MEMORY.md）读取用户所在城市
2. **分级响应机制** - 简单问题直接结论，复杂问题完整信息
3. **问法兼容性** - 含义相同的问题得到相同回答
4. **跨平台兼容性** - Windows/Linux/macOS全支持
5. **中文语法优化** - 符合中文表达习惯

## 📁 发布文件结构

### 核心文件（必须包含）
```
qweather-china/
├── SKILL.md                    # 技能说明文档
├── openclaw_config.yaml       # OpenClaw配置
├── qweather.py                # 和风天气API客户端
├── encoding_utils.py          # 跨平台编码工具
├── location_handler.py        # 智能地点处理器
├── simple_question_fix.py     # 分级响应核心逻辑（优化版）
└── examples.py               # 使用示例
```

### 配置文件
```
config.json                   # 和风天气API配置
install.bat                   # Windows安装脚本
install.sh                    # Linux/macOS安装脚本
```

### 文档文件
```
README.md                    # 用户文档
RELEASE_README.md           # 发布说明（本文件）
```

## 🔧 核心功能说明

### 1. 智能地点记忆
- 用户问"天气怎么样？" → 自动使用记忆中的北京
- 用户问"上海天气怎么样？" → 使用指定的上海
- 兜底机制：无记忆时使用默认北京

### 2. 分级响应机制
#### 简洁模式（简单问题直接结论）：
- "天气怎么样？" → 天气、温度、风力、建议
- "冷不冷？" → 温度 + 体感 + 建议
- "热不热？" → 温度 + 体感 + 建议
- "要不要带伞？" → ✅/❌ + 原因
- "下雨吗？" → 🌧️/☀️ + 建议
- "风大吗？" → 风力等级 + 描述
- "湿度怎么样？" → 湿度百分比 + 舒适度

#### 详细模式（复杂问题完整信息）：
- "详细说说天气" → 完整天气报告
- 包含：实时天气、今天预报、生活建议、总结

### 3. 问法兼容性
含义相同的问题得到相同回答：
- "现在外面冷不冷？" = "冷不冷？"
- "风力大吗？" = "风大吗？"
- "需要带伞吗？" = "要不要带伞？"
- "有雨吗？" = "下雨吗？"

## 🚀 安装与配置

### 1. 前置要求
- Python 3.8+
- OpenClaw 已安装
- 和风天气API密钥（免费申请）

### 2. 安装步骤
```bash
# 方法1：使用clawhub安装
clawhub install qweather-china

# 方法2：手动安装
git clone https://github.com/your-repo/qweather-china.git
cd qweather-china
pip install -r requirements.txt
```

### 3. 配置和风天气API
1. 前往 https://dev.qweather.com/ 注册账号
2. 创建项目，获取API密钥
3. 配置 `config.json` 文件

## 📋 使用示例

### 基本使用
```python
from simple_question_fix import SimpleQuestionFix

weather = SimpleQuestionFix(user_city="beijing")

# 简洁回答
print(weather.ask("天气怎么样？"))
# 输出：您在北京现在：晴，13.0°C（体感9.0°C），2级风，今天2.0°C~15.0°C

print(weather.ask("冷不冷？"))
# 输出：您在北京：有点冷 🧥 体感9.0°C，今天2.0°C~15.0°C

# 详细回答
print(weather.ask("详细说说天气"))
# 输出：完整天气报告...
```

### OpenClaw集成
```yaml
# openclaw_config.yaml 配置示例
skills:
  qweather-china:
    enabled: true
    config_path: "~/.openclaw/skills/qweather-china/config.json"
    default_city: "beijing"
```

## 🧪 测试用例

### 测试所有简单问题
```python
from simple_question_fix import SimpleQuestionFix

weather = SimpleQuestionFix(user_city="beijing")

test_questions = [
    "天气怎么样？",
    "冷不冷？",
    "热不热？",
    "要不要带伞？",
    "下雨吗？",
    "风大吗？",
    "湿度怎么样？",
    "温度多少？",
    "详细说说天气",
]

for question in test_questions:
    answer = weather.ask(question)
    print(f"问题：{question}")
    print(f"回答：{answer}")
    print("-" * 40)
```

## 🔄 版本历史

### v1.2.0 (2026-03-15)
- ✅ 智能地点记忆功能
- ✅ 分级响应机制
- ✅ 问法兼容性优化
- ✅ 跨平台编码支持
- ✅ 中文语法优化

### v1.1.1 (2026-03-13)
- ✅ 修复Windows编码问题
- ✅ 优化错误处理
- ✅ 改进API调用稳定性

### v1.0.0 (2026-03-12)
- ✅ 基础天气查询功能
- ✅ 和风天气API集成
- ✅ 基本配置支持

## 📞 支持与反馈

- GitHub Issues: https://github.com/your-repo/qweather-china/issues
- 文档: https://docs.your-site.com/qweather-china
- 邮箱: support@your-site.com

## 📄 许可证

MIT License

Copyright (c) 2026 Your Name

---

**感谢使用 qweather-china！** 🎯