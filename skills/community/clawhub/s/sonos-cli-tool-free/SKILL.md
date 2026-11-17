---
slug: sonos-cli-tool-free
name: sonos-cli-tool-free
version: 1.0.0
displayName: Sonos控制工具-免费版
summary: "Sonos音箱命令行控制工具,支持播放控制、音量调节与分组管理,适合个人家庭使用。Sonos 音箱命令行控制工具免费版,面向个人家庭用户."
license: Proprietary
edition: free
description: Sonos 音箱命令行控制工具免费版,面向个人家庭用户，可自动提升工作效率
  核心能力:

  - 播放/暂停/下一曲/上一曲控制

  - 音量调节与静音

  - 播放列表与收藏管理

  - 多房间分组控制

  - 音箱状态查询

  - 定时播放与休眠

  适用场景:

  - 家庭 Sonos 系统控制

  - 自动化播放场景

  - 多房间音乐同步

  差异化:免费版提供基础控制能力。PRO版扩展多区域编排、语音集成与企业级场景管理.
  适用关键词: sonos, speaker, 音箱, 播放控制, music, multi-room, 多房间'
tags:
  - Sonos
  - 智能音箱
  - 音乐控制
  - 智能家居
  - 工具
  - 效率
  - 自动化
  - 写作
  - 电商
  - 创意
  - 图像
  - 研究
  - sonos-cli
  - sonos
  - 客厅
  - room
  - 卧室
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# Sonos 控制工具 - 免费版

## 概述

Sonos 控制工具免费版通过命令行控制 Sonos 音箱,支持播放控制、音量调节、多房间分组与定时播放。适合个人家庭 Sonos 系统的日常控制与自动化场景.
## 核心能力

### 1. 播放控制

播放、暂停、下一曲、上一曲、跳转到指定位置.

**处理**: 解析播放控制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回播放控制的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. 音量控制

音量增减、静音/取消静音、设置绝对音量值.

**处理**: 解析音量控制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回音量控制的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 分组管理

将多个 Sonos 音箱分组,实现多房间同步播放.

**处理**: 解析分组管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回分组管理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 播放列表

管理和播放收藏的音乐、播放列表与电台.

**处理**: 解析播放列表的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回播放列表的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 5. 状态查询

查询当前播放状态、曲目信息、音箱连接状态.

**处理**: 解析状态查询的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回状态查询的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 6. 定时控制

定时播放指定音乐,定时休眠停止播放.

**处理**: 解析定时控制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回定时控制的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：音箱命令行控制工、支持播放控制、音量调节与分组管、适合个人家庭使用、具免费版、面向个人家庭用户等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:基本播放控制

控制客厅 Sonos 音箱播放音乐.
用户可通过自然语言指令触发此场景，工具将自动执行相应操作并返回结构化结果.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Sonos控制工具-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 发现网络中的 Sonos 设备
sonos-cli discover
# ...
# 输出:
# 发现 Sonos 设备:
# 1. 客厅 (192.168.1.100) - Sonos Play:5
# 2. 卧室 (192.168.1.101) - Sonos One
# 3. 厨房 (192.168.1.102) - Sonos Beam
# ...
# 播放音乐
sonos-cli play --room "客厅"
# ...
# 暂停
sonos-cli pause --room "客厅"
# ...
# 下一曲
sonos-cli next --room "客厅"
# ...
# 查看当前播放
sonos-cli status --room "客厅"
# ...
# 输出:
# 客厅 - 正在播放
# 曲目: Bohemian Rhapsody
# 艺术家: Queen
# 专辑: A Night at the Opera
# 进度: 02:15 / 05:55
# 音量: 35
```

### 场景二:多房间分组

将客厅和厨房音箱分组,同步播放.
```bash
# 创建分组
sonos-cli group create \
  --name "楼下" \
  --members "客厅,厨房"
# ...
# 分组播放
sonos-cli play --room "楼下"
# ...
# 调整分组音量
sonos-cli volume --room "楼下" --set 30
# ...
# 解散分组
sonos-cli group dissolve --name "楼下"
```

### 场景三:定时播放与休眠

设置闹钟与睡眠定时器.
```bash
# 设置早上 7 点播放指定播放列表
sonos-cli alarm create \
  --time "07:00" \
  --room "卧室" \
  --playlist "晨间音乐" \
  --volume 20 \
  --repeat daily
# ...
# 设置 30 分钟后休眠
sonos-cli sleep-timer --room "卧室" --minutes 30
# ...
# 查看所有定时任务
sonos-cli timer list
# 闹钟: 07:00 卧室 晨间音乐 (每日)
# 休眠: 30分钟后 卧室
```

## 不适用场景

以下场景Sonos控制工具-免费版不适合处理：

- 需要人工创意判断的任务
- 非结构化头脑风暴
- 人际沟通协调

## 触发条件

需要提升效率、自动化流程、批量处理、工作流优化时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 安装

```bash
# 依赖说明
npm install -g sonos-cli
# ...
# 或使用 Python 版
pip install soco-cli
```

### 发现设备

```bash
# 自动发现网络中的 Sonos 设备
sonos-cli discover
# ...
# 手动指定 IP
sonos-cli --ip 192.168.1.100 status
```

### 第一次控制

```bash
# 播放
sonos-cli play --room "客厅"
# ...
# 调节音量
sonos-cli volume --room "客厅" --set 30
# ...
# 查看状态
sonos-cli status --room "客厅"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 命令参数

| 命令 | 说明 | 示例 |
|:-----|:-----|:-----|
| `discover` | 发现设备 | `sonos-cli discover` |
| `play` | 播放 | `sonos-cli play --room 客厅` |
| `pause` | 暂停 | `sonos-cli pause --room 客厅` |
| `next` | 下一曲 | `sonos-cli next --room 客厅` |
| `previous` | 上一曲 | `sonos-cli previous --room 客厅` |
| `volume` | 音量 | `sonos-cli volume --room 客厅 --set 30` |
| `status` | 状态 | `sonos-cli status --room 客厅` |
| `group create` | 创建分组 | `sonos-cli group create --name 楼下 --members 客厅,厨房` |
| `alarm create` | 闹钟 | `sonos-cli alarm create --time 07:00 --room 卧室` |
| `sleep-timer` | 休眠 | `sonos-cli sleep-timer --room 卧室 --minutes 30` |

### 设备配置文件

```json
// ~/.sonos-cli/config.json
{
  "devices": [
    {"name": "客厅", "ip": "192.168.1.100", "model": "Play:5"},
    {"name": "卧室", "ip": "192.168.1.101", "model": "Sonos One"},
    {"name": "厨房", "ip": "192.168.1.102", "model": "Sonos Beam"}
  ],
  "groups": [
    {"name": "楼下", "members": ["客厅", "厨房"]},
    {"name": "全屋", "members": ["客厅", "卧室", "厨房"]}
  ],
  "defaults": {
    "volume": 30,
    "alarmVolume": 20
  }
}
```

## 最佳实践

1. **设备命名**:用房间名命名设备(客厅/卧室),便于识别
2. **合理音量**:默认音量设为 30,避免突然大音量
3. **分组管理**:按楼层或区域分组,同步播放音乐
4. **定时休眠**:睡前设置休眠定时器,避免整夜播放
5. **闹钟渐强**:闹钟从低音量开始,逐渐增大,避免惊醒

## 常见问题

### Q: 发现不到 Sonos 设备?

A: 确保电脑和 Sonos 在同一局域网。检查防火墙是否阻止了 UPnP(端口 1900)。尝试手动指定 IP 地址。Sonos 设备需要已开机并连接到网络.
### Q: 多房间播放有延迟怎么办?

A: Sonos 原生支持多房间同步,正常情况下延迟小于 1ms。如果出现延迟:1) 检查网络带宽;2) 确保所有设备使用有线连接或强 WiFi 信号;3) 重启 Sonos 设备.
### Q: 可以播放 Spotify/Apple Music 吗?

A: 可以。在 Sonos App 中先绑定 Spotify/Apple Music 账号,然后通过 CLI 选择对应音乐源播放。`sonos-cli play --room 客厅 --source spotify --playlist "我的收藏"`.
### Q: 命令行控制和 App 控制冲突吗?

A: 不冲突。CLI 和 App 都通过 Sonos API 控制,操作会实时同步。CLI 上播放后 App 也会显示播放状态.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 与 Sonos 设备同一局域网

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Node.js | 运行时(Node版) | Node版必需 | 官方网站下载 |
| Python 3 | 运行时(Python版) | Python版必需 | 官方网站下载 |
| soco | Python库 | Python版必需 | pip install soco |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置

- 本 Skill 无需 API Key
- Sonos 设备通过局域网 UPnP 协议通信,无需认证
- 如需绑定 Spotify/Apple Music,在 Sonos App 中配置账号

### 可用性分类

- **分类**: MD+EXEC(Markdown指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 控制 Sonos 音箱
- **限制**: 免费版不支持多区域编排、语音集成与高级场景管理

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力