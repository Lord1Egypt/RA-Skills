# 技能说明

## 项目概述

天气简报生成器 - 一键生成精美的天气简报图片，支持任意城市。

## 核心功能

### 1. 天气数据获取
- 数据来源：wttr.in (无需API密钥)
- 支持全球任意城市（英文名称）
- 获取内容：温度、降水、湿度、风速、日出日落、月相、紫外线指数等

### 2. 图表生成 (rain_weather.py)
- 温度曲线（平滑处理）
- 降水柱状图
- 湿度曲线
- 风速曲线
- 支持自适应尺寸、透明背景

### 3. 图像处理
- **毛玻璃特效** (glass.py)：圆角矩形 + 高斯模糊 + 边缘羽化
- **背景裁剪** (cutimage.py)：等比放大 + 左对齐裁剪
- **AI 生图** (makeimage.py)：智谱AI文生图API

### 4. AI 温馨提示 (AI.py)
- 基于天气数据生成贴心提醒
- 三条建议，每条不超过30字
- 使用任意 OpenAI 协议的 API

## 使用示例

```bash
# 默认南京
python main.py

# 指定城市
python main.py Beijing
python main.py Shanghai
python main.py Tokyo
```

## 文件结构

```
├── main.py           # 主程序入口
├── rain_weather.py   # 图表绘制
├── glass.py          # 毛玻璃特效
├── cutimage.py       # 图像裁剪
├── makeimage.py      # AI生图
├── AI.py             # 温馨提示生成
├── simhei.ttf        # 中文字体
├── config.json       # API配置文件（需自行配置）
├── README.md         # 项目说明
└── SKILL.md          # 本文件
```

## 配置文件 (config.json)

首次使用前需要配置 API 密钥：

```json
{
    "zhipuAI": {
        "api_key": "你的智谱AI API密钥",
        "model": "CogView-3-Flash"
    },
    "llm": {
        "api_key": "你的LLM API密钥",
        "base_url": "https://opencode.ai/zen/v1",
        "model": "minimax-m2.5-free"
    }
}
```

| 配置项 | 说明 |
|--------|------|
| zhipuAI.api_key | 智谱AI生图API密钥 |
| zhipuAI.model | 生图模型（默认CogView-3-Flash） |
| llm.api_key | LLM API密钥 |
| llm.base_url | LLM API地址 |
| llm.model | LLM 模型名称 |

## 依赖库

```
pip install requests pillow matplotlib scipy pandas openai zhipuai
```

## 依赖字体

simhei.ttf
- 若缺失需从github下载:https://github.com/ZYT64/WeatherReporter

## 输出

生成 `output.png`，包含完整的天气简报图片。