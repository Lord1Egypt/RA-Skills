# 📦 免费文字转语音与克隆 - 上传资料包

## 📁 文件结构

```
free-tts-voice-cloning/
├── SKILL.md                # 技能主文档（OpenClaw 官网展示）
├── _meta.json              # 技能元数据
├── package.json            # npm 包配置
├── voice_cloning_demo.py   # 交互式演示脚本
├── install_dependencies.sh # 一键安装脚本
└── README.md               # 本说明文件
```

---

## 🚀 上传到 OpenClaw 技能商店

### 方法一：通过 Dashboard 上传

1. **打开 OpenClaw 控制面板**
   ```bash
   openclaw dashboard
   ```
   或直接访问：http://127.0.0.1:18789/

2. **进入技能管理页面**
   - 点击左侧菜单 "Skills"
   - 点击 "Upload Skill" 或 "发布技能" 按钮

3. **上传文件**
   - 将整个文件夹打包为 ZIP 文件
   - 上传 ZIP 文件
   - 或分别上传：`SKILL.md`、`_meta.json`、`package.json`

---

## 📋 技能信息

| 项目 | 内容 |
|------|------|
| **技能名称** | 免费文字转语音与克隆 |
| **英文名称** | Free TTS & Voice Cloning |
| **技能标识** | `free-tts-voice-cloning` |
| **版本** | 1.0.0 |
| **价格** | 🆓 完全免费 |
| **分类** | audio, tts, voice-cloning, free |
| **关键词** | 免费语音合成, 免费声音克隆, 文字转语音 |
| **支持平台** | macOS (Apple Silicon) |
| **依赖** | Python 3.10, mlx-audio, ffmpeg |

---

## ✨ 核心功能

### 为什么选择我们？
| 功能 | 说明 |
|------|------|
| 🆓 **完全免费** | 无任何费用，无 API 调用限制 |
| 🎭 **声音克隆** | 10-30秒参考音频，克隆任意声音 |
| 🎵 **文字转语音** | 12+ 内置声音模板 |
| ⚡ **本地运行** | Apple Silicon 优化，速度快 |
| 🔒 **隐私保护** | 所有处理本地完成 |
| 🌍 **多语言支持** | 中、英、日、韩 |
| 📝 **翻译配音** | 可配合翻译工具实现多语言配音 |

### 适用场景
- 🎧 有声书制作
- 🎮 AI 角色语音生成
- 📱 语音助手开发
- 🎬 视频配音和旁白
- 📚 学习资料音频化
- 🔊 无障碍应用
- 🌐 翻译内容配音

---

## 📝 上传前检查清单

- [x] `SKILL.md` 完整文档（中英双语，突出免费特性）
- [x] `_meta.json` 元数据正确配置
- [x] `package.json` 包含必要信息
- [x] `voice_cloning_demo.py` 测试可用
- [x] `install_dependencies.sh` 可执行
- [x] 法律声明和免责条款已添加
- [x] 故障排除部分覆盖常见问题
- [x] 突出"免费"关键词便于搜索

---

## 🎯 发布后验证

```bash
# 安装并测试技能
openclaw skills install free-tts-voice-cloning

# 运行演示
cd ~/.openclaw/skills/free-tts-voice-cloning
python3.10 voice_cloning_demo.py
```

---

## 📊 搜索优化

已配置高搜索量关键词：
```yaml
keywords: [免费语音合成, 免费声音克隆, 文字转语音, 免费TTS]
```

---

## 📄 许可证

MIT 许可证 - 完全免费，可自由使用和修改。

---

**准备就绪！** 🎉 你的「免费文字转语音与克隆技能包已准备好发布到 OpenClaw 技能商店。
