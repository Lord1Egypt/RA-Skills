---
summary: "用手機 Chrome 登入的 credentials，免費調用 DeepSeek/Kimi/Qwen/GLM 等 AI 模型"
read_when:
  - 想免費使用各種 AI 模型
  - 需要在 Termux 環境使用 AI
  - 已經有手機 Chrome 登入的 AI 帳號
title: "termux-zero-token"
tags:
  - ai
  - chrome
  - deepseek
  - kimi
  - qwen
  - glm
  - free
  - termux
author: "安卓"
author_link: "telegram:@owner"
version: "1.0.0"
min_openclaw_version: "2026.3.0"
license: MIT
repo_url: "https://github.com/openclaw/termux-zero-token"
issues_url: "https://github.com/openclaw/termux-zero-token/issues"
---

# termux-zero-token

在 Android Termux 上使用手機 Chrome 瀏覽器登入的 credentials，免費調用各種 AI 模型。

## 🎯 功能特色

- 🤖 **多 AI 提供商**：DeepSeek、Kimi、Qwen、GLM
- 📱 **手機 Chrome**：使用已登入的瀏覽器 session
- 🔐 **無需 API Key**：直接使用瀏覽器 cookies
- ⚡ **完全免費**：用自己的帳號調用 AI

## 📱 支持的 AI

| 提供商 | 狀態 | 模型 | 費用 |
|--------|------|------|------|
| DeepSeek | ✅ | deepseek-chat, deepseek-reasoner | 免費 |
| Kimi | ✅ | moonshot-v1-8k/32k/128K | 免費 |
| Qwen | ✅ | qwen-turbo/plus/max | 免費 |
| GLM | ✅ | glm-4-flash/plus | 免費 |

## 🚀 快速開始

### 前置條件

1. **電腦安裝 ADB**
```bash
# macOS
brew install adb

# Linux
sudo apt install adb
```

2. **手機開啟開發者選項**
- 設定 → 關於手機 → 連續點擊版本號 7 次
- 開發者選項 → 啟用 USB 偵錯

3. **電腦連接手機**
```bash
adb devices
adb forward tcp:9222 tcp:9222
```

### 使用流程

```bash
# 1. 確保手機 Chrome 已登入 AI 網站
#    DeepSeek: https://chat.deepseek.com
#    Kimi: https://kimi.moonshot.cn
#    Qwen: https://qwen.chat
#    GLM: https://chatglm.cn

# 2. 連接手機 Chrome（需要 ADB port forward）
#    系統會自動連接 localhost:9222

# 3. 提取 credentials
#    運行 import 命令（CLI 開發中）

# 4. 使用 AI
#    直接調用相應的 provider
```

## 🔧 技術原理

```
┌──────────────────────────────────────────────────────┐
│                    系統架構                          │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐      adb forward      ┌─────────┐ │
│  │  手機 Chrome │ ◄──────────────────► │ Termux  │ │
│  │ (已登入AI)  │    tcp:9222           │ (本AI)  │ │
│  └─────────────┘                       └────┬────┘ │
│                                             │       │
│                                             ▼       │
│  ┌──────────────────────────────────────────────┐   │
│  │           Credentials 提取                   │   │
│  │  - CDP 連接手機 Chrome                       │   │
│  │  - 捕獲 cookies/session                     │   │
│  │  - 存儲到 ~/.openclaw/zero-token/           │   │
│  └──────────────────────────────────────────────┘   │
│                                             │       │
│                                             ▼       │
│  ┌──────────────────────────────────────────────┐   │
│  │           AI Provider 調用                   │   │
│  │  - 使用 cookies 調用 Web API                 │   │
│  │  - 模擬瀏覽器會話                            │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## 💰 商業模式

這個技能可以這樣賺錢：

1. **技術服務**：幫用戶配置，收取服務費 $5-10
2. **訂閱制**：$3/月，無限使用所有 AI
3. **企業部署**：幫企業建立內部 AI 系統

## ⚠️ 限制與風險

1. **Cookies 會過期** - 需要定期更新
2. **違反 AI 服務條款** - 僅供個人學習使用
3. **無法保證永久可用** - AI 公司可能會變更 API

## 📞 支援

- 問題反饋：GitHub Issues
- 商務合作：直接聯繫老闆

---

**版權聲明**：本 Skill 基於 openclaw-zero-token 開發，僅供學習和研究使用。