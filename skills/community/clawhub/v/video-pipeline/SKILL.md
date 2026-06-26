# video-pipeline

## 描述
一句话输入自然语言，自动生成5-6分钟行业AI短视频（竖屏1080x1920）。

## 触发词
- 生成视频
- 做视频
- 短视频
- 行业视频

## 前置依赖
- Node.js (>=16.x)
- Python 3 (>=3.8)
- FFmpeg
- Remotion（通过 npm 安装）
- Edge-TTS（通过 pip 安装）
- DashScope API（需要配置 API 密钥）

## 使用方法
运行主入口脚本 `pipeline.py`，支持自然语言输入和传统模式：

### 自然语言模式（推荐）
```bash
python pipeline.py "帮我做一个零售业AI智能推荐的短视频"

python pipeline.py "医疗AI如何改变诊断？做一个3分钟科普视频" --size 1920x1080 --duration 3

python pipeline.py "介绍AI在教育行业的应用" --size 1920x1080
```

### 传统模式
```bash
python pipeline.py --lesson 1 --action all
python pipeline.py --lesson 1 --action gen_html
python pipeline.py --lesson 1 --action render --size 1080x1920
```

### 参数说明
- `--duration`: 目标视频时长（分钟），默认5分钟
- `--size`: 视频尺寸，默认1080x1920（竖屏），支持1920x1080（横屏）等

## 配置项
在 `credentials/dashscope.json` 中配置 DashScope API 密钥：
```json
{
  "api_key": "your-dashscope-api-key-here",
  "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1"
}
```

## 8步视频生成流程
1. **环境检测** — 检查 Node.js、Python、FFmpeg、Remotion、Edge-TTS
2. **缓存清理** — 清理旧文件
3. **大纲生成** — AI 生成课程大纲（封面/钩子/内容页/总结/行动指南）
4. **逐字稿生成** — 根据大纲生成详细配音文本
5. **HTML 课件生成** — 从配音文本生成 HTML 课件及 insights.json
6. **TSX 组件生成** — 根据 insights.json 生成 React 组件
7. **TTS 音频生成** — 将配音文本转换为 MP3
8. **Composition 生成 + 渲染** — 生成 Remotion Composition 并渲染最终视频

## 许可协议
MIT License

Copyright (c) 2026 郡城智能科技 (JunCheng AI Technology)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
