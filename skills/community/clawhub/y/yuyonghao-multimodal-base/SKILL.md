# Multimodal Base Skill

**version**: 0.1.0

OpenClaw 多模态基础 - 图像理解 + 语音识别 + 语音合成

## 功能特性

- **图像理解**: GPT-4V API 图像描述、OCR 文字提取、图表分析
- **语音识别**: Whisper 语音转文字（支持本地/API 模式）
- **语音合成**: Edge TTS 文字转语音（8 种音色）
- **统一管道**: 多模态输入输出统一处理

## 安装

```bash
cd skills/multimodal-base
npm install

# 安装 Edge TTS（需要 Python）
pip install edge-tts

# 可选：安装 FFmpeg（音频处理）
# Windows: winget install FFmpeg
```

## 快速开始

```javascript
import { MultimodalPipeline } from './src/multimodal-pipeline.js';

// 创建管道
const pipeline = new MultimodalPipeline({
  image: {
    openaiApiKey: 'your-api-key'
  },
  speech: {
    mode: 'api', // 'local' 或 'api'
    openaiApiKey: 'your-api-key'
  },
  tts: {
    outputDir: './output'
  }
});

// 处理图像
const imageResult = await pipeline.processInput({
  type: 'image',
  path: './photo.jpg'
});
console.log(imageResult.content.image.description);

// 处理语音
const audioResult = await pipeline.processInput({
  type: 'audio',
  path: './recording.wav'
});
console.log(audioResult.content.audio.transcript);

// 生成语音输出
const output = await pipeline.generateOutput(
  '这是合成的语音',
  { speak: true, voice: 'zh-CN-XiaoxiaoNeural' }
);
console.log(output.content.audio.path);
```

## API 参考

### MultimodalPipeline

#### processInput(input)
处理多模态输入

```javascript
// 文本输入
await pipeline.processInput({
  type: 'text',
  content: '你好'
});

// 图像输入
await pipeline.processInput({
  type: 'image',
  path: './image.jpg',
  prompt: '描述这张图片'
});

// 语音输入
await pipeline.processInput({
  type: 'audio',
  path: './audio.wav'
});

// 多模态输入
await pipeline.processInput({
  type: 'multimodal',
  text: '请分析',
  image: './chart.png'
});
```

#### generateOutput(text, options)
生成输出（支持语音）

```javascript
await pipeline.generateOutput('你好', {
  speak: true,
  voice: 'zh-CN-XiaoxiaoNeural',
  rate: 1.0,
  pitch: 0
});
```

### ImageProcessor

#### understand(imagePath, prompt)
理解图像内容

```javascript
import ImageProcessor from './src/image-processor.js';

const processor = new ImageProcessor({ openaiApiKey: 'key' });
const result = await processor.understand('./photo.jpg', '描述内容');
// { description: '...', tokens: 123 }
```

#### ocr(imagePath)
OCR 文字提取

```javascript
const result = await processor.ocr('./document.png');
// { text: '...', confidence: 95 }
```

### SpeechRecognizer

#### recognize(audioPath)
语音识别

```javascript
import SpeechRecognizer from './src/speech-recognizer.js';

const recognizer = new SpeechRecognizer({
  mode: 'api',
  openaiApiKey: 'key'
});

const result = await recognizer.recognize('./audio.wav');
// { text: '...', confidence: 0.95 }
```

### SpeechSynthesizer

#### synthesize(text, options)
语音合成

```javascript
import SpeechSynthesizer from './src/speech-synthesizer.js';

const tts = new SpeechSynthesizer();
const result = await tts.synthesize('你好', {
  voice: 'zh-CN-XiaoxiaoNeural',
  rate: 1.2
});
// { audioPath: './output/tts_xxx.mp3', duration: 1.5 }
```

#### getVoices()
获取可用音色

```javascript
const voices = tts.getVoices();
// [{ id: 'zh-CN-XiaoxiaoNeural', name: '晓晓', ... }]
```

## 配置选项

### 完整配置

```javascript
const pipeline = new MultimodalPipeline({
  // 图像处理
  image: {
    openaiApiKey: process.env.OPENAI_API_KEY,
    model: 'gpt-4o',
    baseURL: 'https://api.openai.com/v1'
  },
  
  // 语音识别
  speech: {
    mode: 'api', // 'local' 或 'api'
    modelPath: './models/ggml-base.bin',
    openaiApiKey: process.env.OPENAI_API_KEY,
    language: 'zh'
  },
  
  // 语音合成
  tts: {
    outputDir: './output',
    defaultVoice: 'zh-CN-XiaoxiaoNeural'
  },
  
  // 历史记录
  maxHistory: 100
});
```

## 音色列表

| ID | 名称 | 性别 | 语言 |
|----|------|------|------|
| zh-CN-XiaoxiaoNeural | 晓晓 | 女 | 中文 |
| zh-CN-XiaoyiNeural | 晓伊 | 女 | 中文 |
| zh-CN-YunjianNeural | 云健 | 男 | 中文 |
| zh-CN-YunxiNeural | 云希 | 男 | 中文 |
| en-US-AriaNeural | Aria | 女 | 英文 |
| en-US-GuyNeural | Guy | 男 | 英文 |
| ja-JP-NanamiNeural | 七海 | 女 | 日文 |
| ko-KR-SunHiNeural | 善熙 | 女 | 韩文 |

## 注意事项

1. **API Key**: 图像理解和语音识别需要 OpenAI API Key
2. **Edge TTS**: 需要 Python 环境和 `edge-tts` 包
3. **音频格式**: 支持 WAV、MP3、M4A 等常见格式
4. **图像大小**: 最大 20MB
5. **音频大小**: 最大 25MB（OpenAI 限制）

## License

MIT
