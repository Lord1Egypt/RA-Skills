# 🎬 短视频爆款文案生成与复刻专家

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Web-orange.svg)](https://)

一个功能完整的短视频文案生成工具，支持多平台爆款文案生成、智能复刻、免费TTS语音合成。

---

## ✨ 核心功能

### 📝 模块一：AI爆款文案生成
- **抖音文案**：生成符合抖音风格的中文爆款文案
- **TikTok日区**：生成日文爆款文案，自动翻译中文
- **TikTok美区**：生成英文爆款文案，自动翻译中文

### 🔄 模块二：爆款文案复刻
- 自动识别语言（中文/日文/英文/韩文）
- 智能生成同风格新文案
- 支持多语言输出

### 💾 模块三：保存记录
- 本地存储（localStorage）
- 一键生成标题和标签
- 最多保存50条记录

### 🎙️ 模块四：TTS语音合成
- **完全免费**：基于 Edge TTS
- **多语言支持**：中/英/日/韩
- **多音色选择**：20+ 中文语音
- **音频下载**：支持 MP3 格式

---

## 🚀 快速开始

### 方式一：直接打开
```bash
# 双击打开 index.html 即可使用
open index.html
```

### 方式二：本地服务器
```bash
# 使用 Python
python -m http.server 8080

# 使用 Node.js
npx serve .

# 访问 http://localhost:8080
```

### 方式三：作为 Skill 使用
将整个 `viral-copy-generator` 文件夹放入 AI 平台的 Skills 目录即可。

---

## 📁 文件结构

```
viral-copy-generator/
├── skill.json          # Skill 配置文件
├── index.html          # 主应用（单文件，包含所有功能）
├── README.md           # 使用文档
└── LICENSE             # MIT 许可证
```

---

## 🔧 技术架构

### 前端
- **纯原生技术**：HTML5 + CSS3 + JavaScript
- **无依赖**：无需 npm、无需打包
- **响应式**：适配桌面端和移动端

### API 服务
| 服务 | 用途 | 费用 |
|------|------|------|
| tts.wangwangit.com | TTS语音合成 | 免费 |
| api.mymemory.translated.net | 翻译服务 | 免费 |

### 数据存储
- **localStorage**：本地存储，无需后端
- **最大记录**：50条
- **隐私安全**：数据不上传服务器

---

## 🎨 支持的语音

### 中文语音（20+ 种）

**女声：**
| 语音 | 风格 |
|------|------|
| 晓晓 (Xiaoxiao) | 温柔 |
| 晓伊 (Xiaoyi) | 甜美 |
| 晓辰 (Xiaochen) | 知性 |
| 晓涵 (Xiaohan) | 优雅 |
| 晓梦 (Xiaomeng) | 梦幻 |
| 晓墨 (Xiaomo) | 文艺 |
| 晓秋 (Xiaoqiu) | 成熟 |

**男声：**
| 语音 | 风格 |
|------|------|
| 云希 (Yunxi) | 清朗 |
| 云扬 (Yunyang) | 阳光 |
| 云健 (Yunjian) | 稳重 |
| 云枫 (Yunfeng) | 磁性 |

### 其他语言
| 语言 | 女声 | 男声 |
|------|------|------|
| 英文 | Jenny | Guy |
| 日文 | 七海 | 大地 |
| 韩文 | 선희 | 인준 |

---

## 🔒 安全特性

### 内容安全策略（CSP）
```
default-src: 'self'
connect-src: 'self' https://tts.wangwangit.com https://api.mymemory.translated.net
```

### 隐私保护
- ✅ 无外部脚本加载
- ✅ 无追踪代码
- ✅ 数据仅存本地
- ✅ 无需用户注册

### 代码安全
- ✅ 输入内容 XSS 过滤
- ✅ API 调用错误处理
- ✅ 敏感信息不暴露

---

## 🌐 浏览器兼容性

| 浏览器 | 最低版本 |
|--------|----------|
| Chrome | 80+ |
| Firefox | 75+ |
| Safari | 13+ |
| Edge | 80+ |

---

## 📱 使用截图

### AI文案生成
输入产品类型和卖点，选择平台，一键生成爆款文案。

### 爆款复刻
粘贴任意爆款文案，自动识别语言并生成新文案。

### TTS配音
选择音色，点击播放或下载音频。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🙏 致谢

- [Edge TTS](https://tts.wangwangit.com/) - 免费语音合成服务
- [MyMemory](https://mymemory.translated.net/) - 免费翻译服务

---

## 📮 联系

如有问题或建议，请提交 Issue。
