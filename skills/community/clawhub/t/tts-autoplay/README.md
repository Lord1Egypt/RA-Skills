# TTS AutoPlay Skill - README

## 🔊 自动播放 TTS 语音

让 OpenClaw 在 Windows Webchat 上自动播放语音回复，无需修改源码！

## 快速安装

```bash
# 使用 ClawHub 安装
npx clawhub install tts-autoplay

# 进入技能目录
cd skills/tts-autoplay

# 运行安装脚本
powershell -ExecutionPolicy Bypass -File install.ps1

# 启动自动播放
powershell -ExecutionPolicy Bypass -File tts-autoplay.ps1
```

## 配置 TTS

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "messages": {
    "tts": {
      "auto": "always",
      "provider": "edge",
      "edge": {
        "enabled": true,
        "voice": "zh-CN-XiaoxiaoNeural",
        "lang": "zh-CN"
      }
    }
  }
}
```

## 使用方法

### 启动
```powershell
# 直接运行
powershell -ExecutionPolicy Bypass -File tts-autoplay.ps1

# 或使用批处理文件
start.bat
```

### 停止
按 `Ctrl+C` 或关闭 PowerShell 窗口

### 查看日志
```powershell
Get-Content tts-autoplay.log -Tail 20
```

## 功能特性

- ✅ 自动检测新语音文件
- ✅ 立即自动播放
- ✅ 日志记录
- ✅ 智能去重（5 秒窗口）
- ✅ 免费（Edge TTS 无需 API）

## 系统要求

- Windows 10/11
- OpenClaw
- PowerShell 5.1+
- Windows Media Player

## 文件说明

```
tts-autoplay/
├── SKILL.md              # 技能说明
├── README.md             # 本文件
├── tts-autoplay.ps1     # 主脚本
├── install.ps1          # 安装脚本
├── uninstall.ps1        # 卸载脚本
├── start.bat            # 快速启动
└── examples/
    └── config-example.json  # 配置示例
```

## 故障排查

**脚本无法运行**：
```powershell
powershell -ExecutionPolicy Bypass -File tts-autoplay.ps1
```

**检测不到文件**：
检查 TTS 配置是否正确，确认文件在 `C:\tmp\openclaw\`

**播放失败**：
确保 Windows Media Player 已安装

## 更多文档

详细指南见：`TTS-AutoPlay-Guide.md`

## 支持

- GitHub Issues
- OpenClaw Discord
- 中文社区：clawcn.net

## 许可证

MIT License

---

**作者**: 爪爪 (ZhaoZhao)  
**版本**: 1.0.0  
**发布时间**: 2026-02-27
