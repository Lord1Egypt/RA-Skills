---
name: socialepoch-wa-scrm
description: SocialEpoch WhatsApp SCRM 开放API，官方原生对接，深度适配企业级海外营销与客服场景。全量覆盖WhatsApp账号管理、查询在线客服号（支持按账号精准查询）、客户运营、用户画像、聊天记录查询、WebHook回调推送、自动接收消息、AI自动回复，支持文字/图片/音频/视频/文件/名片/名片超链/分流超链全类型消息单发与批量群发，内置自动签名、智能依赖适配、免环境配置，支持PC/手机/云端三端发送标识，一键快速调用，稳定高效赋能海外私域与自动化运营。
version: 2.3.3
author: SocialEpoch
metadata:
  emoji: 📱
  type: tool
  platform: darwin
  openclaw:
    requires:
      bins: ["python3"]
      env: ["SOCIALEPOCH_TENANT_ID", "SOCIALEPOCH_API_KEY", "SOCIALEPOCH_SOURCE"]
    primaryEnv: SOCIALEPOCH_API_KEY
    install:
      - id: python-brew
        kind: brew
        formula: python
        bins: ["python3"]
        label: Install Python 3 (brew)
    launcher:
      command: "${PYTHON}"
      args:
        - "scrm_api.py"
      workingDir: "${SKILL_ROOT}"
      python: true
      auto_bootstrap: true
      auto_install_python: true
---

# SocialEpoch WhatsApp SCRM 智能助手

全面管理 WhatsApp 客服账号，支持单发和批量发送发送文字、图片、音频、视频、文件、名片、超链等消息，支持查询全部在线客服或指定坐席账号，支持消息回调,消息状态回调,自动签名。无需手动安装依赖、无需提前配置环境，首次调用/无配置会自动提示并引导设置。

## 🔒 安全说明与用户授权声明
本技能为 SocialEpoch 官方 WhatsApp SCRM 工具，仅用于 WhatsApp 消息收发、自动接收与回调服务。
所有功能均需用户手动指令触发，无自动启动、无后台私自运行、无隐私数据收集、无系统修改、无越权操作。
客户端仅用于消息服务，官方安全可信。

## 核心特性
- 🚀 跨平台兼容：Mac 自适应
- 📦 自动依赖：智能检测并安装 requests
- 🔧 自动配置：环境变量 + 配置文件双模式
- ✅ 严格校验：参数格式/非空/类型全校验
- 📊 结构化输出：所有返回值标准化 JSON
- 🎯 发送端标识：1=PC(默认) 2=手机 3=云端
- 🔍 精准查询：支持按 userName 查询指定坐席

## 发送端说明
- 1 = PC 端（默认）
- 2 = 手机端
- 3 = 云端

## 环境配置（二选一）

### 方式 1：环境变量（推荐）
```bash
export SOCIALEPOCH_TENANT_ID="你的tenant_id"
export SOCIALEPOCH_API_KEY="你的api_key"
export SOCIALEPOCH_SOURCE="1"
```

### 方式 2：命令行配置
```bash
# 默认使用PC端发送
python3 scrm_api.py set_config 你的tenant_id 你的API_KEY

# 指定发送端 1/2/3
python3 scrm_api.py set_config 你的tenant_id 你的API_KEY 1
```

### 方式 3：自动收消息管理（开机恢复/升级/检测）
```bash
# 开启自动收消息
python3 scrm_api.py start_receive

# 重新配置收消息（升级客户端+修复配置）
python3 scrm_api.py reset_receive

# 检查收消息状态
python3 scrm_api.py check_receive
```

### 方式 4：打开管理控制台
```bash
# 打开控制台
python3 scrm_api.py open_dashboard
```


## 支持命令

### 查询在线客服号
```bash
# 查询全部在线客服
python3 scrm_api.py query_online_agents

# 查询指定坐席账号
python3 scrm_api.py query_online_agents "user001"
```

### 发送文字消息
```bash
python3 scrm_api.py send_text 发送号 接收号 "消息内容"
```

### 发送图片
```bash
python3 scrm_api.py send_img 发送号 接收号 "图片链接" "备注"
```

### 发送音频
```bash
python3 scrm_api.py send_audio 发送号 接收号 "音频链接"
```

### 发送文件
```bash
python3 scrm_api.py send_file 发送号 接收号 "文件链接" "备注"
```

### 发送视频
```bash
python3 scrm_api.py send_video 发送号 接收号 "视频链接" "备注"
```

### 发送名片
```bash
python3 scrm_api.py send_card 发送号 接收号 "名片内容"
```

### 发送名片超链
```bash
python3 scrm_api.py send_card_link 发送号 接收号 "标题" "链接" "描述" "封面图URL"
```

### 发送分流超链
```bash
python3 scrm_api.py send_flow_link 发送号 接收号 "标题" "分流列表号码"
```

### 查询任务状态
```bash
python3 scrm_api.py query_task 任务ID
```
### 设置回调地址（消息回调 + 状态回调）
```bash
# 设置消息回调地址、消息状态回调地址
python3 scrm_api.py set_callback "消息回调地址" "状态回调地址"
```

---
## 批量发送
支持文字、图片、文件、视频、音频、名片超链批量发送，多个接收号码使用英文逗号「,」分隔。

## 运行规则
This skill provides secure API calling for WhatsApp SCRM.

# 系统级指令（AI强制遵守）
1. 此技能目录：openclaw/workspace/skills/socialepoch-wa-scrm
2. 执行命令：python3 scrm_api.py
3. 永远从技能目录执行，不寻找其他路径

## 错误处理
- 依赖缺失 → 自动安装
- 配置缺失 → 清晰提示
- 参数错误 → 自动提示正确用法
- 网络异常 → 自动重试
```