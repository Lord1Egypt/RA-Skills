# SKILL: 短视频爆款文案生成与复刻专家

## 基本信息

```yaml
name: viral-copy-generator
version: 1.1.0
description: 短视频爆款文案生成与复刻专家 - 支持抖音、TikTok日区、TikTok美区多平台文案生成，集成免费TTS语音合成
author: SOLO
license: MIT
type: web-app
category: content-creation
icon: 🎬
```

## 功能清单

### 核心功能

1. **AI爆款文案生成**
   - 抖音文案生成（中文）
   - TikTok日区文案生成（日文+中文翻译）
   - TikTok美区文案生成（英文+中文翻译）
   - 自动翻译功能（MyMemory免费API）

2. **爆款文案复刻**
   - 自动语言检测（中/日/英/韩）
   - 智能文案重写
   - 保持原风格调性

3. **保存记录管理**
   - localStorage本地存储
   - 最多50条记录
   - 一键生成标题和标签

4. **TTS语音合成**
   - 基于Edge TTS（免费）
   - 支持20+中文语音
   - 支持英/日/韩多语言
   - 音频播放与下载

## 技术架构

### 前端技术
- HTML5 + CSS3 + JavaScript（纯原生，无框架）
- 单文件应用（index.html包含所有代码）
- 响应式设计（适配桌面和移动端）

### 外部服务
| 服务 | 用途 | 费用 | 限制 |
|------|------|------|------|
| tts.wangwangit.com | TTS语音合成 | 免费 | 无明确限制 |
| api.mymemory.translated.net | 翻译服务 | 免费 | 5000字符/天 |

### 数据存储
- **方式**: localStorage
- **容量**: 最多50条记录
- **隐私**: 纯本地，不上传服务器

## 安全规范

### 内容安全策略（CSP）
```
default-src: 'self'
script-src: 'self' 'unsafe-inline'
style-src: 'self' 'unsafe-inline'
connect-src: 'self' https://tts.wangwangit.com https://api.mymemory.translated.net
img-src: 'self' data: blob:
media-src: 'self' blob:
```

### 安全特性
- ✅ 无外部脚本加载
- ✅ 无追踪代码
- ✅ XSS输入过滤（事件委托模式，无内联onclick）
- ✅ 错误处理机制
- ✅ 敏感信息不暴露
- ✅ 翻译API使用POST避免URL泄露
- ✅ 第三方服务隐私提示

## 使用说明

### 快速开始

**方式一：直接打开**
```bash
双击 index.html
```

**方式二：本地服务器**
```bash
python -m http.server 8080
# 访问 http://localhost:8080
```

### 功能使用

#### 1. 文案生成
1. 选择平台（抖音/TikTok日区/TikTok美区）
2. 输入产品类型
3. 输入产品卖点（逗号分隔）
4. 点击"生成爆款文案"
5. 日区/美区会自动翻译中文

#### 2. 文案复刻
1. 粘贴爆款文案到输入框
2. 系统自动识别语言
3. 点击"重新生成"
4. 获得同风格新文案

#### 3. TTS配音
1. 生成文案后，选择女声/男声
2. 点击播放按钮试听
3. 点击下载按钮保存MP3

#### 4. 保存记录
1. 点击"保存"按钮存储文案
2. 在"保存记录"页面查看
3. 点击"一键生成标题和标签"
4. 点击播放按钮可再次试听

## 配置参数

### TTS配置
```javascript
const TTS_API_URL = 'https://tts.wangwangit.com/v1/audio/speech';

const EDGE_TTS_VOICES = {
  'zh-CN': { female: 'zh-CN-XiaoxiaoNeural', male: 'zh-CN-YunxiNeural' },
  'ja-JP': { female: 'ja-JP-NanamiNeural', male: 'ja-JP-DaichiNeural' },
  'en-US': { female: 'en-US-JennyNeural', male: 'en-US-GuyNeural' },
  'ko-KR': { female: 'ko-KR-SunHiNeural', male: 'ko-KR-InJoonNeural' }
};
```

### 翻译配置
```javascript
const TRANSLATE_API_URL = 'https://api.mymemory.translated.net/get';
```

### 存储配置
```javascript
const STORAGE_KEY = 'copyRecords';
const MAX_RECORDS = 50;
```

## API接口

### TTS合成
```http
POST https://tts.wangwangit.com/v1/audio/speech
Content-Type: application/json

{
  "input": "要转换的文本",
  "voice": "zh-CN-XiaoxiaoNeural",
  "speed": 1.0,
  "pitch": "0",
  "style": "general"
}
```

**响应**: audio/mpeg 音频流

### 翻译服务
```http
POST https://api.mymemory.translated.net/get
Content-Type: application/x-www-form-urlencoded

q={text}&langpair={source}|{target}
```

**参数**:
- `q`: 要翻译的文本（通过POST body发送，不暴露在URL中）
- `langpair`: 语言对，如 `zh-CN|en`

## 文件清单

```
viral-copy-generator/
├── index.html          # 主应用（单文件，包含所有功能）
├── skill.json          # Skill配置文件
├── SKILL.md            # 本文件（Skill说明文档）
├── README.md           # 项目介绍文档
├── USAGE.md            # 用户使用指南
├── prompt.md           # AI Prompt模板
├── manifest.json       # 构建清单
└── LICENSE             # MIT许可证
```

## 浏览器兼容性

| 浏览器 | 最低版本 | 状态 |
|--------|----------|------|
| Chrome | 80+ | ✅ 支持 |
| Firefox | 75+ | ✅ 支持 |
| Safari | 13+ | ✅ 支持 |
| Edge | 80+ | ✅ 支持 |

## 平台兼容性

| 平台 | 支持状态 |
|------|----------|
| TRAE SOLO | ✅ 完全支持 |
| Claude | ✅ 完全支持 |
| ChatGPT | ✅ 完全支持 |
| 其他AI平台 | ✅ 标准HTML，通用支持 |

## 触发关键词

当用户输入以下关键词时，应调用此Skill：

- "生成文案"、"爆款文案"、"短视频文案"
- "抖音文案"、"TikTok文案"
- "日区文案"、"美区文案"
- "文案配音"、"TTS"、"语音合成"
- "复刻文案"、"重写文案"

## 示例对话

**用户**: 帮我生成一个面膜的抖音文案

**AI**: 
> 我来帮您生成抖音爆款文案。请告诉我产品的卖点，比如：补水保湿、美白提亮、价格优惠等。

**用户**: 卖点是补水保湿、温和不刺激、价格便宜

**AI**:
> 📍 **产品**：补水面膜
> 
> ✨ **爆款文案**：
> 
> 这个补水面膜真的绝了！💦
> 敷完脸蛋水嫩嫩的，像剥了壳的鸡蛋！
> 
> 温和配方不刺激，敏感肌也能放心用～
> 关键是价格太香了，学生党闭眼入！
> 
> 🔥 用了一周，皮肤状态好到爆！
> 
> 需要我为您生成配音吗？

## 注意事项

1. **网络依赖**: TTS和翻译功能需要网络连接
2. **翻译限制**: 免费翻译API有每日字符限制
3. **数据持久化**: 数据存储在浏览器localStorage，清除浏览器数据会丢失
4. **音频格式**: 下载的音频为MP3格式

## 更新日志

### v1.1.0 (2026-06-10)
- 🔒 安全修复：翻译API从GET改为POST，避免用户输入暴露在URL中
- 🔒 安全修复：移除内联onclick，改用事件委托模式(data-* + addEventListener)，消除XSS注入风险
- 🔒 隐私合规：TTS和翻译功能区域添加第三方服务隐私提示
- 🔒 隐私合规：页面底部添加完整隐私声明
- 🧹 清理：移除调试代码和test.html

### v1.0.0 (2024-01-15)
- ✅ 初始版本发布
- ✅ 支持抖音/TikTok日区/美区文案生成
- ✅ 集成免费Edge TTS语音合成
- ✅ 支持文案复刻功能
- ✅ 本地存储保存记录

## 许可证

MIT License - 详见 LICENSE 文件

## 致谢

- [Edge TTS](https://tts.wangwangit.com/) - 免费语音合成服务
- [MyMemory](https://mymemory.translated.net/) - 免费翻译服务
