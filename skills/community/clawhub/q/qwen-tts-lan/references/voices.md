# 千问 TTS 音色列表

## 系统音色（无需定制，直接使用）

### 中文音色

| 音色名 | 性别 | 风格 | 适用场景 |
|--------|------|------|---------|
| `Cherry` | 女 | 活泼甜美 | 客服、互动、教学 |
| `Huogeng` | 女 | 温柔知性 | 有声书、情感内容 |
| `Shanbin` | 男 | 沉稳磁性 | 新闻、导航、讲解 |
| `Eason` | 男 | 年轻活力 | 品牌广告、短视频 |
| `Yunyang` | 男 | 成熟专业 | 知识讲解、纪录片 |
| `Junhou` | 男 | 亲切温和 | 儿童内容、故事 |
| `Nini` | 女 | 清新自然 | 教育、互动 |
| `Yexun` | 男 | 大气厚重 | 纪录片、史诗 |
| `Zhuoma` | 女 | 藏族女声 | 民族特色内容 |
| `Mingyue` | 女 | 古典优雅 | 古风、有声书 |

### 英文音色

| 音色名 | 性别 | 风格 | 适用场景 |
|--------|------|------|---------|
| `Emma` | 女 | 轻快自然 | 品牌、广告、互动 |
| `Ashley` | 女 | 专业知性 | 企业介绍、教学 |
| `Laura` | 女 | 温暖友好 | 有声书、故事 |
| `Clara` | 女 | 清晰标准 | 客服、导航 |
| `Alice` | 女 | 活泼可爱 | 儿童内容 |
| `Jennifer` | 女 | 自然流畅 | 长文本朗读 |
| `Arnold` | 男 | 专业稳重 | 企业、新闻 |
| `Daniel` | 男 | 磁性低沉 | 纪录片、故事 |
| `Eric` | 男 | 年轻活力 | 短视频、社交 |
| `Ryan` | 男 | 阳光开朗 | 品牌、运动 |
| `William` | 男 | 英式古典 | 高端品牌、历史 |

### 粤语音色

| 音色名 | 性别 | 适用场景 |
|--------|------|---------|
| `Yixing` | 女 | 粤语对话、教育 |
| `Jiamu` | 男 | 粤语新闻、讲解 |

### 中文方言

| 音色名 | 方言 | 地区 |
|--------|------|------|
| `Zhiyu` | 四川话 | 四川 |
| `Yixuan` | 东北话 | 东北 |
| `Qiao` | 台湾话 | 台湾 |

## 声音定制音色

### 声音设计（Voice Design）- qwen3-tts-vd

通过文本描述创建全新音色，适合品牌定制：

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3-tts-vd",
    "input": {
      "text": "欢迎来到我们的品牌世界",
      "voice": "young_female_excited_brand_ambassador"
    }
  }'
```

### 声音复刻（Voice Clone）- qwen3-tts-vc

基于音频样本复刻真人音色：

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3-tts-vc",
    "input": {
      "text": "要复刻的文本内容"
    },
    "parameters": {
      "voice_id": "your-voice-id"
    }
  }'
```

## 指令控制（Instruct）

仅 `qwen3-tts-instruct-flash` 支持，用自然语言控制情感和风格：

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen3-tts-instruct-flash",
    "input": {
      "text": "今天真的好开心啊！",
      "voice": "Cherry",
      "language_type": "Chinese",
      "instructions": "语速较快，带有明显的上扬语调，表达兴奋和喜悦"
    },
    "parameters": {
      "optimize_instructions": true
    }
  }'
```

常用指令示例：
- "语速较慢，低沉有力，适合新闻播报"
- "带有明显的上扬语调，表达兴奋"
- "温柔亲切，像朋友聊天"
- "庄重正式，适合企业介绍"
