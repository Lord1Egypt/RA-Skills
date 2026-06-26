# 天气简报生成器

一款自动化生成天气简报图片的工具，支持自定义城市、生成带有天气图表和 AI 温馨提示的图片。

## 功能特性

- 支持任意城市天气查询（英文城市名）
- 自动生成温度、降水、湿度、风速曲线图
- 毛玻璃特效背景
- AI 驱动的天气温馨提示
- 完整的天气数据展示（日出日落、月相、紫外线等）

## 文件说明

| 文件 | 说明 |
|------|------|
| main.py | 主程序入口，负责整体流程控制 |
| rain_weather.py | 天气图表绘制模块 |
| cutimage.py | 背景图片裁剪模块 |
| glass.py | 毛玻璃特效模块 |
| makeimage.py | AI 生成背景图模块 |
| AI.py | AI 温馨提示生成模块 |
| simhei.ttf | 黑体字体文件（确保中文显示） |
| config.json | API 配置文件（需自行配置） |

## 配置文件

首次运行前需要配置 `config.json`：

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

### 配置说明

- **zhipuAI.api_key**: 智谱AI的API密钥，用于生成天气背景图
- **zhipuAI.model**: 智谱AI生图模型，默认为 CogView-3-Flash
- **llm.api_key**: 大语言模型的API密钥，用于生成温馨提示
- **llm.base_url**: LLM API地址，根据你的提供商填写
- **llm.model**: LLM 模型名称

获取 API 密钥：
- 智谱AI：https://open.bigmodel.cn/
- LLM：支持任意 OpenAI 协议兼容的 API（如 OpenAI、OpenCode、DeepSeek 等）

## 使用方法

### 基本用法

运行默认城市（Nanjing）：
```bash
python main.py
```

### 指定城市

```bash
python main.py Beijing
python main.py Shanghai
python main.py Guangzhou
python main.py Shenzhen
```

支持全球任意城市，使用英文名称。

### 输出

程序运行后会生成 `output.png`，包含：
- AI 生成的天气背景图
- 温度与降水曲线
- 湿度曲线
- 风速曲线
- 日出日落、月相、紫外线指数等天气数据
- AI 生成的温馨提示

## 环境依赖

```bash
pip install requests pillow matplotlib scipy pandas openai zhipuai
```

## 输出示例

- example.png
- <img width="2510" height="8209" alt="example" src="https://github.com/user-attachments/assets/10bd9660-4859-44f4-afea-9a81c645620a" />

## openclaw支持

- 可以作为openclaw的skill工作

## 注意事项

- 天气数据来源：wttr.in
- 首次运行前必须配置 `config.json` 中的 API 密钥
- 运行会下载 AI 生成的背景图，可能需要较长时间
- 确保网络连接正常
- 字体文件 simhei.ttf 需要与脚本在同一目录
