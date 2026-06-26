# Xiaomi MiMo TTS Skill

小米 MiMo TTS 语音合成 OpenClaw Skill。

## ✨ 核心亮点：多语言智能版本支持

**自动分析文本，智能选择最合适的情感、方言、语速，多语言实现支持！**

### 🎯 智能版本支持

| 版本 | 文件 | 特点 | 推荐度 |
|------|------|------|--------|
| **统一入口** | `mimo-tts-smart.sh` | 自动选择最佳实现 | ★★★★★ |
| **NodeJS 版 (removed in this release)** | `mimo_tts_smart.js` | 功能最完善 | ★★★★★ |
| **Python 版 (removed in this release)** | `mimo_tts_smart.py` | 功能完整，备用方案 | ★★★★☆ |
| **Shell 版** | `mimo_tts_smart.sh` | 简化版，兼容性好 | ★★★☆☆ |

```bash
# 推荐：统一入口（自动选择最佳实现）
scripts/mimo-tts-smart.sh "今天太开心了，哈哈！" output.ogg

# 直接调用 NodeJS 版 (removed in this release)（功能最完整）
node scripts/mimo_tts_smart.js "今天太开心了，哈哈！" output.ogg
# 输出: 📊 检测结果: 情感: happy
#       🏷️ 风格: <style>开心</style>

# Python 版 (removed in this release)
python3 scripts/mimo_tts_smart.py "宝宝晚安，爱你哦～" output.ogg
# 输出: 📊 检测结果: 情感: gentle
#       🏷️ 风格: <style>温柔</style>

# Shell 简化版
scripts/mimo_tts_smart.sh "老铁，咋整啊？" output.ogg
# 输出: 🏷️ 检测到风格: 东北话
```

### 智能模式（说明与使用建议）

本项目提供“智能模式”（位于 scripts/mimo-tts-smart.sh 与 scripts/smart/ 下），它使用轻量的启发式与关键词检测来自动为文本选择合适的风格、方言与情感。该模式设计用于快速试验与交互式体验，而非对每种语境都保证高精度。

建议与行为：
- 默认不在自动化流水线中启用智能模式。将其视为可选的便捷工具，需由 agent 或用户显式调用。
- 若对输出准确性有较高要求，请在输入文本最前面使用 `<style>...</style>` 明确指定风格与方言。
- 智能模式适合快速原型、演示与人机协作场景；不适合替代人工细致调整或用于对准确性敏感的生产流程。

调用示例：

```bash
# 明确启用智能模式（显式调用）
./scripts/mimo-tts-smart.sh "宝宝晚安，爱你哦～" output.ogg

# 若要手动覆盖智能判断，仍可直接在文本前使用 style 标签
./scripts/mimo-tts.sh "<style>温柔</style>床前明月光..." out.ogg
```

## 安装

```bash
clawhub install xiaomi-mimo-tts
```

## 配置

推荐使用官方环境变量名（优先）：

```bash
export XIAOMI_API_KEY=your-api-key
```

为兼容历史配置，也支持旧名：

```bash
export MIMO_API_KEY=your-api-key  # 仍被接受，脚本会优先使用 XIAOMI_API_KEY
```

获取 API Key: https://platform.xiaomimimo.com/

## 使用

### 命令行

```bash
# 基本用法
~/.openclaw/skills/mimo-tts/scripts/mimo-tts.sh "你好世界"

# 指定输出文件
~/.openclaw/skills/mimo-tts/scripts/mimo-tts.sh "你好世界" output.ogg

# 使用 Python 脚本（更多功能）
pip install openai
python3 ~/.openclaw/skills/mimo-tts/scripts/mimo_tts.py "你好" \
  --voice default_zh --style "夹子音" --output output.wav
```

### 可用语音

- `mimo_default` - 默认
- `default_zh` - 中文女声
- `default_eh` - 英文女声

### 风格控制

```bash
# 夹子音
python3 scripts/mimo_tts.py "<style>夹子音</style>主人～我来啦！" --voice default_zh

# 悄悄话
python3 scripts/mimo_tts.py "<style>悄悄话</style>这是秘密" --voice default_zh

# 方言
python3 scripts/mimo_tts.py "<style>东北话</style>你瞅啥" --voice default_zh
```

### 情感标签

```bash
# 在文本中使用 () 标注情感
python3 scripts/mimo_tts.py "（紧张，深呼吸）呼……冷静，冷静"
```

## 测试

```bash
~/.openclaw/skills/mimo-tts/scripts/test.sh
```

## 📁 目录结构

```
scripts/
├── mimo-tts.sh           # 基础版本统一入口
├── mimo-tts-smart.sh     # 智能版本统一入口
├── base/                 # 基础版本实现
│   ├── mimo-tts.sh       # Shell 基础版
│   ├── mimo_tts.js       # NodeJS 基础版
│   └── mimo_tts.py       # Python 基础版
├── smart/                # 智能版本实现
│   ├── mimo_tts_smart.js    # NodeJS 智能版
│   ├── mimo_tts_smart.py    # Python 智能版
│   └── mimo_tts_smart.sh    # Shell 智能版
├── utils/                # 工具脚本
│   └── test.sh           # 测试脚本
└── examples/             # 示例脚本
    └── demo.sh           # 演示脚本
```

## 脚本版本

### 统一入口（推荐）
- `mimo-tts.sh` - 基础版本统一入口
- `mimo-tts-smart.sh` - **智能版本统一入口（推荐）**

### 基础版本
- `base/mimo-tts.sh` - Shell 脚本（基础）
- `base/mimo_tts.js (removed)` - Node.js 脚本
- `base/mimo_tts.py (removed)` - Python 脚本

### 智能版本
- `smart/mimo_tts_smart.js` - NodeJS 智能版，功能最完善
- `smart/mimo_tts_smart.py` - Python 智能版，功能完整
- `smart/mimo_tts_smart.sh` - Shell 智能版，简化版

## 依赖

- curl
- node (Node.js >= 18，内置 fetch)
- python3（可选）
- ffmpeg

## License

MIT

## 关于智能模式的说明（重要）

当前“智能”模式使用基于关键词的启发式规则来选择语气、方言和风格。这种方法简单、高效，但并不总能准确理解复杂语境或细微语义，可能会发生误判或选择不合适的风格。

建议：默认不要在自动化流程中开启智能模式。将智能模式作为可选功能，只有在需要快速试验或用户明确同意自动选择风格时才启用。要使用智能模式，请调用 `scripts/mimo-tts-smart.sh` 或在工具中显式设置启用标志。若对输出有高准确性要求，建议手动在文本前添加 `<style>...</style>` 明确指定风格与语气。


## 安装（npx / clawhub）

除了使用 clawhub 安装外，你也可以通过 npx 直接运行或安装：

- 直接用 npx 运行（无需全局安装）：

```bash
npx @openclaw/skill-runner run ~/.openclaw/skills/xiaomi-mimo-tts -- "<style>温柔</style>你好世界" output.ogg
```

- 建议方式：将技能作为本地依赖或通过 clawhub 管理，npx 适合临时运行或测试场景。


## 发布到 skills.sh / ClawHub

如果你想把该技能发布到 skills.sh（ClawHub 注册表），参考以下步骤：

1. 准备发布包（已在仓库根目录生成 `.skill` 打包文件）：
   - 文件名示例： `xiaomi-mimo-tts.skill`
2. 选择版本号：确保该版本号在 registry 中未被占用（见 `clawhub inspect xiaomi-mimo-tts`）。
3. 使用 `clawhub` CLI 发布：

```bash
clawhub publish ~/.openclaw/skills/xiaomi-mimo-tts --version 1.3.0 --name "Xiaomi MiMo TTS" --tags "tts,mimo,xiaomi" --changelog "短的发布说明"
```

4. 若发布失败提示版本已存在：
   - 选择新的语义化版本号（例如 1.3.1）或联系当前 skill 所有者来更新已有条目。
5. 注意事项与权限：
   - 发布需要在 ClawHub 上登录且拥有相应权限（owner 或有发布权限的账号）。
   - CI/自动化在运行真实发布前不要把 secrets 写入公开 workflow；优先在本地或受控环境执行。

6. 发布后（可选）：
   - 在 GitHub Release 中附加 `.skill` 包作为 artifact（已完成示例）。
   - 在 README 中加入安装示例（clawhub install 或 npx 运行示例）。

