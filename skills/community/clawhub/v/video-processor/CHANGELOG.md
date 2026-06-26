# 更新日志

## v2.1 (2026-03-24) - 模型优化与精度提升

### ✨ 新增功能

1. **多模型支持** - 支持 tiny/base/small/medium/large 五种模型
2. **精确时间戳同步** - 字幕时间戳与人声精确匹配
3. **模型对比测试** - 新增详细测试报告

### 🔧 优化改进

1. **简化识别参数** - 移除过度处理，保留原始时间戳
2. **VAD 优化** - 合理过滤静音，避免过度合并
3. **字幕生成优化** - 直接使用识别时间戳，不做人为修改

### 📊 模型测试结果

**测试视频**：2 分 35 秒 AI 设备介绍

| 模型 | 大小 | 段数 | 处理时间 | 准确度 | 推荐度 |
|------|------|------|----------|--------|--------|
| tiny | 75MB | 5 段 | ~30 秒 | ⭐⭐ | ❌ |
| base | 142MB | 56 段 | ~45 秒 | ⭐⭐⭐ | ⭐⭐⭐ |
| small | 244MB | 90 段 | ~90 秒 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| medium | 769MB | 47 段 | ~3 分钟 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### 🏆 推荐配置

```bash
# 最佳精度（强烈推荐）
python scripts/video_processor.py -i "video.mp4" -m "medium"

# 平衡速度与精度
python scripts/video_processor.py -i "video.mp4" -m "small"

# 快速处理
python scripts/video_processor.py -i "video.mp4" -m "base"
```

### 📈 准确度提升示例

**开场白识别对比**：
- tiny: "這裡是湖聯網直光波浪會的現場" ❌
- base: "这里是互联网职光博兰会的现场" ⚠️
- small: "这里是互联网直光博览会的现场" ✅
- medium: "这里是互联网直观博览会的现场" ✅

**关键术语识别**：
- "博览会"：medium/small ✅ | base/tiny ❌
- "外骨骼机器人"：medium/small ✅ | base/tiny ❌
- "仿生手"：medium/small ✅ | base/tiny ❌

---

## v2.0 (2026-03-24) - 重大更新

### ✨ 新增功能

1. **真实语音识别支持**
   - 支持 OpenAI Whisper 引擎
   - 支持 faster-whisper 引擎（推荐，速度更快）
   - 自动检测并选择可用的引擎
   - 无 Whisper 时自动降级为模拟模式

2. **同步字幕生成**
   - 字幕时间戳基于实际语音识别结果
   - 每段字幕时间与语音片段精确对应
   - 标准 SRT 格式（HH:MM:SS,mmm）

3. **改进的音频提取**
   - 16kHz 采样率（Whisper 要求）
   - 单声道 WAV 格式
   - 显示音频文件大小

4. **增强的错误处理**
   - 更详细的错误信息
   - 优雅降级（无 Whisper 时使用模拟模式）
   - 路径转义修复（Windows 兼容）

### 🔧 修复问题

1. **SRT 时间戳格式** - 从错误的逗号分隔修复为标准格式
2. **字幕烧录路径** - 修复 Windows 路径转义问题
3. **文字稿内容** - 从硬编码改为实际语音识别生成

### 📋 使用说明

```bash
# 基础使用（模拟模式）
python scripts/video_processor.py -i "video.mp4" -o "./output"

# 使用 Whisper 识别（需要安装）
python scripts/video_processor.py -i "video.mp4" -o "./output" -m "base"

# 使用更小模型（更快）
python scripts/video_processor.py -i "video.mp4" -o "./output" -m "tiny"
```

### 📦 依赖安装

```bash
# 必需
# FFmpeg - 视频处理

# 可选（用于真实语音识别）
pip install faster-whisper  # 推荐
# 或
pip install openai-whisper
```

---

## v1.0 (2026-03-23) - 初始版本

- 基础视频处理框架
- 模拟语音识别
- SRT 字幕生成
- 标题提炼
- 视频字幕烧录
