# 📦 上传 ClawHub 文件清单

**技能名称**: video-processor  
**版本**: v2.1.0  
**日期**: 2026-03-24

---

## ✅ 必需文件（核心）

```
video-processor/
├── SKILL.md                          # ✅ 技能说明（必需）
├── README.md                         # ✅ 使用指南（必需）
├── CHANGELOG.md                      # ✅ 更新日志（必需）
├── clawhub.json                      # ✅ ClawHub 配置（必需）
├── subtitle_style_template.json      # ✅ 样式模板
│
├── scripts/
│   ├── video_processor.py            # ✅ 主处理器（必需）
│   └── subtitle_processor.py         # ✅ 后处理器（必需）
│
├── 快速开始.bat                       # ✅ 一键启动脚本
└── 后处理.bat                         # ✅ 后处理脚本
```

**核心文件数**: 8 个

---

## 📚 可选文件（文档）

```
video-processor/
├── 字幕后处理完整指南.md              # 📖 详细使用文档
├── 后处理使用指南.md                  # 📖 后处理文档
├── 模型对比测试.md                    # 📊 测试报告
├── 优化指南.md                        # 💡 优化建议
└── 功能清单.md                        # ✅ 功能验收清单
```

**文档文件数**: 5 个

---

## ❌ 不上传的文件

```
video-processor/
├── video.mp4                         # ❌ 测试视频（太大）
├── video - 副本.mp4                  # ❌ 测试视频副本
├── output/                           # ❌ 输出目录（运行时生成）
├── regenerated/                      # ❌ 再生目录（运行时生成）
├── *.pyc                            # ❌ Python 缓存
├── __pycache__/                     # ❌ Python 缓存目录
└── .git/                            # ❌ Git 目录
```

---

## 📋 上传步骤

### 1. 准备文件

```bash
# 清理测试文件
cd C:\Users\laimeng\.openclaw\workspace\skills\video-processor

# 删除测试视频
Remove-Item "video.mp4" -Force
Remove-Item "video - 副本.mp4" -Force

# 删除输出目录
Remove-Item "output" -Recurse -Force
Remove-Item "regenerated" -Recurse -Force
```

### 2. 验证文件结构

```bash
# 查看最终文件
Get-ChildItem -Recurse -File | Select-Object FullName
```

### 3. 打包

**方式 A: ZIP 压缩包**
```bash
# 压缩为 ZIP
Compress-Archive -Path * -DestinationPath "../video-processor-v2.1.0.zip"
```

**方式 B: Git 仓库**
```bash
# 提交到 Git
git add .
git commit -m "video-processor v2.1.0"
git tag v2.1.0
git push origin main --tags
```

### 4. 上传到 ClawHub

1. 访问 https://clawhub.com
2. 登录账号
3. 点击"发布技能"
4. 填写信息：
   - 名称：video-processor
   - 版本：2.1.0
   - 描述：自动处理短视频，语音识别转字幕
   - 分类：媒体处理
5. 上传文件（ZIP 或 Git 仓库 URL）
6. 提交审核

---

## 📊 文件大小估算

| 文件 | 大小 |
|------|------|
| SKILL.md | ~7 KB |
| README.md | ~9 KB |
| CHANGELOG.md | ~3 KB |
| clawhub.json | ~2 KB |
| subtitle_style_template.json | ~1 KB |
| scripts/video_processor.py | ~13 KB |
| scripts/subtitle_processor.py | ~10 KB |
| 快速开始.bat | ~1 KB |
| 后处理.bat | ~2 KB |
| 文档（5 个） | ~25 KB |
| **总计** | **~73 KB** |

---

## ✅ 上传前检查清单

- [ ] 已创建 `clawhub.json` 配置文件
- [ ] 已删除测试视频文件
- [ ] 已删除 output/ 和 regenerated/ 目录
- [ ] 已验证所有脚本可正常运行
- [ ] 已测试繁简转换功能
- [ ] 已测试后处理功能
- [ ] README.md 包含完整使用说明
- [ ] CHANGELOG.md 包含版本历史
- [ ] 所有文件使用 UTF-8 编码
- [ ] 没有硬编码的本地路径

---

## 🔧 clawhub.json 配置说明

```json
{
  "name": "video-processor",          // 技能标识
  "displayName": "短视频自动处理器",   // 显示名称
  "version": "2.1.0",                 // 版本号
  "description": "...",               // 简短描述
  "entry": "SKILL.md",                // 入口文件
  "main": "scripts/video_processor.py", // 主脚本
  "requirements": {                   // 依赖
    "python": ">=3.8",
    "packages": ["faster-whisper", "opencc-python-reimplemented"],
    "system": ["ffmpeg"]
  }
}
```

---

## 📝 发布说明模板

```markdown
## video-processor v2.1.0

### ✨ 核心功能
- 🎙️ 语音识别转文字（支持 5 种 Whisper 模型）
- 📝 自动生成 SRT 字幕（时间戳精确同步）
- 🎯 智能提炼视频标题
- 📺 字幕烧录到视频
- 🔄 支持修改文字稿后重新生成
- 🎨 自定义字幕样式配置
- 🌐 繁体自动转简体

### 🚀 快速开始
```bash
python scripts/video_processor.py -i "video.mp4" -m "medium"
```

### 📦 依赖
- Python 3.8+
- faster-whisper
- opencc-python-reimplemented
- FFmpeg

### 📖 详细文档
见 README.md 和 字幕后处理完整指南.md
```

---

## 🎯 最终文件结构（上传用）

```
video-processor/
├── SKILL.md                          ✅
├── README.md                         ✅
├── CHANGELOG.md                      ✅
├── clawhub.json                      ✅
├── subtitle_style_template.json      ✅
├── 快速开始.bat                       ✅
├── 后处理.bat                         ✅
│
├── scripts/
│   ├── video_processor.py            ✅
│   └── subtitle_processor.py         ✅
│
└── docs/ (可选)
    ├── 字幕后处理完整指南.md          ✅
    ├── 后处理使用指南.md              ✅
    ├── 模型对比测试.md                ✅
    ├── 优化指南.md                    ✅
    └── 功能清单.md                    ✅
```

**总计**: 8 个核心文件 + 5 个文档文件 = **13 个文件**

---

**准备就绪**: ✅  
**预估大小**: ~73 KB  
**上传时间**: < 1 分钟

---

**更新日期**: 2026-03-24 13:55
