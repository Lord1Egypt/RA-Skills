# 更新日志 - QQ Bot 语音识别 Skill

## v2.0.0 (2026-03-01) - Gateway 自动识别集成 🎉

### ✨ 新增功能

#### 1. Gateway 自动识别
- **自动判断附件类型** - 根据文件扩展名和 MIME 类型自动识别语音消息
- **自动识别流程** - 无需手动调用脚本，Gateway 自动处理
- **用户确认流程** - 识别后显示结果，请用户确认再执行
- **自动清理** - 处理完成后自动清理临时文件

**代码示例：**
```typescript
const ext = path.extname(localPath).toLowerCase();
const mimeType = att.content_type?.toLowerCase() || '';

if (ext === '.amr' || mimeType.includes('amr')) {
  // 自动识别流程
}
```

#### 2. txt 文件路径修复
- **问题**：Whisper 输出 `.amr.txt`，代码查找 `.wav.txt`
- **解决**：检查多个可能的路径
```typescript
const possibleTxtPaths = [
  localPath + ".txt",         // .amr.txt ✅
  wavPath + ".txt",           // .wav.txt
  downloadDir + "/" + path.basename(localPath) + ".txt"
];
```

#### 3. 系统优化
- **4GB swap 配置** - 防止 OOM 崩溃
- **磁盘清理** - 清理 7GB 空间
- **medium 模型默认** - 准确率 ~95%+

### 🔧 修复问题

| 问题 | 状态 | 解决方案 |
|------|------|----------|
| OOM 崩溃 | ✅ 已修复 | 添加 4GB swap |
| 识别结果为空 | ✅ 已修复 | txt 路径多路径检查 |
| 提示语错误 | ✅ 已修复 | 纯语音消息特殊处理 |
| 硬盘空间不足 | ✅ 已修复 | 清理 7GB 空间 |

### 📊 性能提升

**识别准确率：**
- v1.0: ~90% (base 模型)
- v2.0: ~95%+ (medium 模型) ⬆️

**处理流程：**
- v1.0: 手动调用脚本
- v2.0: 自动识别 + 用户确认 🚀

**系统稳定性：**
- v1.0: 可能 OOM 崩溃
- v2.0: 4GB swap 保护 ✅

### 📝 使用示例

**v1.0 方式（手动）：**
```bash
python3 scripts/process_qq_voice.py voice.amr
```

**v2.0 方式（自动）：**
```
用户发送语音 → Gateway 自动识别 → 显示结果 → 用户确认 → 执行
```

**识别效果：**
```
🎤 **语音消息识别结果**：今天天气如何

_请确认是否正确，我将按此执行_
```

### 📦 依赖更新

**新增依赖：**
- whisper (必需，之前是可选)
- swap 空间 (推荐，4GB)

**移除依赖：**
- 无

### 🔗 相关文件

**更新文件：**
- `SKILL.md` - 更新版本和更新日志
- `README.md` - 新增 Gateway 集成说明
- `scripts/process_qq_voice.py` - 默认模型改为 medium

**新增文件：**
- `CHANGELOG.md` - 本文件
- `examples/gateway-integration-v2.ts` - Gateway 集成示例

---

## v1.0.0 (2026-02-28) - 初始版本

### ✨ 功能
- ✅ QQ Silk V3 格式解码
- ✅ Whisper 中文识别
- ✅ 批量处理支持
- ✅ QQ Bot 集成示例

### 📦 依赖
- ffmpeg
- python3
- silk-v3-decoder
- openai-whisper (可选)

### 📝 文档
- SKILL.md
- README.md
- 示例代码

---

## 📈 版本对比

| 特性 | v1.0 | v2.0 |
|------|------|------|
| 自动识别 | ❌ | ✅ |
| 用户确认 | ❌ | ✅ |
| txt 路径修复 | ❌ | ✅ |
| 默认模型 | base | medium |
| 准确率 | ~90% | ~95%+ |
| OOM 保护 | ❌ | ✅ (4GB swap) |
| Gateway 集成 | 示例 | 内置 |

---

**维护者：** 卡妹 (CyberKamei) 🌸  
**最后更新：** 2026-03-01
