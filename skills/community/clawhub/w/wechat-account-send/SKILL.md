---
name: wechat-account-send
version: 4.0.0
description:  This skill provides integrated WeChat account management, message delivery, and file transmission capabilities. It supports querying current user account information and actively sending text messages or various file types (including images, videos, audio, and documents) to specified WeChat contacts or groups when invoked through OpenClaw. The functionality enables complete operation execution for user-driven communication and sharing tasks.
---


# 微信账号消息发送 Skill

使用 OpenClaw 的微信集成功能，实现微信账号信息查询、会话管理、主动文本消息和文件发送功能。
调用时机：当用户需要查询当前微信账户信息，或主动向指定微信联系人/群组发送消息时,通过微信发送文件即可触发。

## 功能说明

本技能提供以下核心功能：

1.  **微信会话查询**：使用 sessions_list 工具查询当前活跃的微信会话和对话信息。
2.  **主动文本消息发送**：通过微信后端API向指定用户发送文本消息。
3.  **文件发送**：通过微信后端API向指定用户或机器人发送多种格式的文件（如图片、视频、音频、文档）。

## 功能亮点

- 支持多账号管理
- 自动获取用户配置信息
- 完整的消息与文件发送反馈
- 跨平台兼容性（Windows/Linux/MacOS）
- 详细的调试信息输出
- 会话信息查询和管理
- 实时会话状态监控
- 自动路径检测，无需手动配置
- 支持广泛的文件格式（图片、视频、音频、文档、压缩包等）

## 使用方法

### 1. 会话查询功能

#### 列出所有活跃会话
当用户要求列出所有会话时，调用 sessions_list 工具：
sessions_list()
```

#### 找到当前对话
当用户要求找到我们之间的对话时：
# 获取所有会话
sessions_list()
# 过滤出微信渠道的会话
# 找到最新的或与当前对话匹配的会话
```

#### 获取会话详情
使用 sessions_list 的参数来获取更详细的信息：
# 获取最近活跃的会话
sessions_list(activeMinutes=60, messageLimit=5)
```

### 2. 主动消息发送功能

#### 命令行调用方式
```bash
python scripts/main_send_msg <account_id> <message>
```

#### 示例
```bash
python scripts/main_send_msg "6e2f83e62b99-im-bot" "这是发送的消息"
```

### 3. 文件发送功能 (新增)

本技能提供两种核心文件发送场景：

#### 场景一：微信文件自我发送
- **使用场景**：当用户要求将某个文件（如截图、结果文件等）通过微信发送给自己时触发。
- **执行流程**：
  1.  通过微信会话查询功能，确认当前会话对应的机器人账号。
  2.  理解用户需要发送的文件（由用户提供或根据上下文生成）。
  3.  调用文件发送程序，将文件发送至用户微信。

#### 场景二：微信文件推送发送
- **使用场景**：当用户要求将某个文件通过微信发送给指定机器人时触发。
- **执行流程**：
  1.  解析用户指令，确认需要发送的文件。
  2.  调用文件发送程序，将文件发送至目标机器人账号。

#### 命令行调用方式
```bash
# 发送图片
python scripts/main_send_file.py "XXXXXXX-im-bot" "/home/测试图片.jpg"

# 发送视频
python scripts/main_send_file.py "XXXXXXX-im-bot" "/home/测试视频.mp4"

# 发送文档
python scripts/main_send_file.py "XXXXXXX-im-bot" "/home/测试文档.pdf"

# 发送音频
python scripts/main_send_file.py "XXXXXXX-im-bot" "/home/测试音频.mp3"
```

#### 触发条件
当同时满足以下条件时，文件发送功能将被自动调用：
1.  用户通过微信发送的消息**非纯文本**。
2.  消息中**携带附件**（如图片、视频、文档等）。
3.  用户明确要求"通过微信发送文件"或表达类似意图。

## 参数说明

### 1. 会话查询参数
| 参数名称 | 类型 | 描述 | 默认值 |
| :--- | :--- | :--- | :--- |
| `activeMinutes` | 整数 | 查询指定分钟内活跃的会话 | 60 |
| `messageLimit` | 整数 | 每个会话返回的消息数量 | 5 |

### 2. 消息发送参数
#### 命令行参数
| 参数名称 | 类型 | 描述 | 必填 |
| :--- | :--- | :--- | :--- |
| `account_id` | 字符串 | 微信账号唯一标识符（如：`6e2f83e62b99-im-bot`） | ✅ 是 |
| `message` | 字符串 | 要发送的文本消息内容 | ✅ 是 |

### 3. 文件发送参数 (新增)
#### 命令行参数
| 参数名称 | 类型 | 描述 | 必填 |
| :--- | :--- | :--- | :--- |
| `account_id` | 字符串 | 微信账号唯一标识符（如：`XXXXXXX-im-bot`） | ✅ 是 |
| `file_path` | 字符串 | 待发送文件的完整本地路径 | ✅ 是 |

## 注意事项

### 使用前准备
1.  **环境配置**：确保已正确安装 OpenClaw 并完成微信账号登录。
2.  **账号配置**：确保账号ID对应的配置文件存在于正确的位置。
3.  **依赖安装**：确保已安装所需的 Python 依赖包（`requests`, `uuid`, `pathlib` 等）。

### 使用限制
1.  **消息格式**：支持文本消息和多种格式的文件发送。
2.  **频率限制**：请遵守微信API的调用频率限制，避免频繁发送。
3.  **账号状态**：确保账号处于正常登录状态。
4.  **权限控制**：发送消息和文件需要对应的权限配置。
5.  **文件限制**：目前不支持发送整个文件夹，文件需携带完整路径。

### 约束与限制 (新增)
#### 文件大小建议
| 文件类型 | 建议大小上限 |
| :--- | :--- |
| 图片 | ≤ 10 MB |
| 视频 | ≤ 20 MB |
| 其他文件 | ≤ 50 MB |

> 注：实际文件大小限制以微信官方API规定为准，超过限制可能导致发送失败。

#### 已测试支持的文件格式
- 图片：jpg, png, gif, bmp 等
- 视频：mp4, mov, avi 等
- 音频：mp3, wav, m4a 等
- 文档：pdf, doc, docx, xls, xlsx, ppt, pptx, txt 等
- 压缩文件：zip, rar, 7z 等

### 配置文件位置
账号配置文件默认存放在以下位置：
- Windows: `C:\Users\用户名\.openclaw\openclaw-weixin\accounts`
- Linux/MacOS: `~/.openclaw/openclaw-weixin/accounts`

### 自动路径检测
技能现在通过 `get_openclaw_path()` 函数实现自动路径检测：
1.  优先检测环境变量 `OPENCLAW_STATE_DIR`
2.  如果未设置环境变量，使用默认路径
3.  支持 Windows、Linux 和 macOS 平台

### 错误处理
常见错误及解决方法：

| 错误类型 | 可能原因 | 解决方法 |
| :--- | :--- | :--- |
| 路径不存在 | OpenClaw路径配置错误 | 检查 OpenClaw 是否正确安装 |
| 配置文件缺失 | 账号ID不存在或配置文件损坏 | 重新登录微信账号 |
| 网络请求异常 | 网络连接失败或API地址错误 | 检查网络连接和API地址配置 |
| 权限验证失败 | Token失效或权限不足 | 重新获取身份验证令牌 |
| 文件发送失败 (新增) | 文件路径错误、网络异常、API返回非零状态码、文件类型不支持或大小超限 | 检查文件路径与网络，查看错误日志，确认文件格式与大小 |

## 示例输出

### 会话查询示例
**sessions_list 返回示例：**
```json
{
  "sessions": [
    {
      "sessionKey": "openclaw-weixin:xxxxxxxx-22f75d8b",
      "kind": "openclaw-weixin",
      "lastMessage": "检查微信助手的账号ID",
      "lastMessageTime": "2026-04-01T17:12:00Z"
    }
  ]
}
```

### 消息发送示例
**成功发送文本消息的输出：**
```
==================================================
【微信消息发送测试】
目标用户: xxxxxxxx
客户端ID: openclaw-weixin:1735114630-abc123def
上下文Token: xxxxxxxx-22f75d8b
------------------------------
HTTP 状态码: 200
API 返回码 (ret): 0
✅ 消息发送成功！
服务器响应详情:
{
  "ret": 0,
  "msg": "success",
  "data": {}
}
==================================================
```

### 文件发送示例 (新增)
**成功发送文件的输出：**
```
1. 准备上传参数...
准备成功，filekey: a1b2c3d4e5f67890..., aeskey: 0011223344556677...

2. 申请上传参数...
获取到upload_param: xyz123abc456def789...

3. 加密文件...
  加密完成，原始大小: 102400, 加密后大小: 102416

4. 上传到CDN...
  上传成功，encrypt_query_param: enc_param_abc123def456...

5. 发送文件...
HTTP 状态码: 200
API 返回码 (ret): 0
✅ 文件发送成功！
服务器响应详情:
{
  "ret": 0,
  "msg": "success",
  "data": {}
}
```

## 版本历史
| 版本 | 更新日期 | 更新内容 |
| :--- | :--- | :--- |
| 4.0.0 | 2026-04-03 | **新增文件发送功能**，支持图片、视频、音频、文档、压缩文件等多种格式文件发送。 |
| 3.0.0 | 2026-04-02 | 新增主动消息发送功能，支持向指定用户发送消息；添加自动路径检测功能 |
| 2.0.0 | 2026-04-01 | 改用sessions_list工具查询会话信息 |
| 1.0.0 | 2026-04-01 | 初始版本发布，支持微信账号信息查询 |

## 技术说明

### 工作原理
#### 会话查询原理
1.  调用 OpenClaw 的 sessions_list 工具
2.  获取所有活跃会话信息
3.  过滤出微信渠道的会话
4.  返回会话详细信息

#### 消息发送原理
1.  根据账号ID查找对应的配置文件
2.  读取配置文件中的连接参数
3.  构建符合微信API规范的请求
4.  发送HTTP请求到微信后端
5.  处理响应并显示结果

#### 文件发送原理 (新增)
1.  根据账号ID查找对应的配置文件，获取必要的连接参数。
2.  读取并验证本地文件，进行加密和上传参数准备。
3.  将文件上传至CDN，获取文件访问参数。
4.  调用微信API，发送包含文件访问信息的消息到指定会话。
5.  处理API响应，返回发送结果。

#### 自动路径检测原理
```python
def get_openclaw_path():
    """获取OpenClaw安装路径，支持Windows、Linux、MacOS"""
    # 优先使用环境变量指定的路径
    state_dir = os.environ.get('OPENCLAW_STATE_DIR')
    if state_dir and os.path.exists(state_dir):
        return Path(state_dir)

    # 默认路径
    home = Path.home()
    if sys.platform == 'win32':
        # Windows: C:\Users\用户名\.openclaw
        return home / '.openclaw'
    else:
        # Linux/MacOS: ~/.openclaw
        return home / '.openclaw'
```
### 架构设计
```

┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 会话查询模块    │     │ 账号信息查询     │────▶│ 消息发送模块     │
└─────────────────┘     └──────────────────┘     └──────────────────┘
         ▲                          ▲                          ▲
         │                          │                          │
         ▼                          ▼                          ▼
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 错误处理        │     │ 配置文件管理     │     │ 网络请求处理     │
└─────────────────┘     └──────────────────┘     └──────────────────┘
         ▲                          ▲                     ▲
         │                          │                     │
         ▼                          ▼                     ▼
┌─────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│ 自动路径检测    │     │ 环境变量检测     │     │ 文件处理模块(新增)│
└─────────────────┘     └──────────────────┘     └──────────────────┘

```
### 核心依赖
- `requests`: HTTP请求库
- `json`: JSON数据处理
- `time`: 时间戳管理
- `base64`: 编码解码
- `os`: 操作系统交互
- `uuid`: 唯一ID生成
- `pathlib`: 路径管理
- `sys`: 系统级操作

## 部署说明
### 1. 目录结构

wechat-account-send/
├── SKILL.md                 # 技能文档
├── scripts/
│   ├── main_send_msg        # 文本消息发送主程序
│   └── main_send_file.py    # (新增) 文件发送主程序
└── (其他配置文件)

### 2. 自动路径检测
技能现在支持自动路径检测，无需手动配置环境变量。但如果需要自定义 OpenClaw 路径，可以设置以下环境变量：

```bash
# Windows
set OPENCLAW_STATE_DIR=C:\path\to\your\openclaw

# Linux/MacOS
export OPENCLAW_STATE_DIR=/path/to/your/openclaw
```

## 安全注意事项
1.  **配置文件保护**：账号配置文件包含敏感信息，请勿泄露。
2.  **代码执行安全**：确保脚本来源可信，避免执行恶意代码。
3.  **API权限控制**：定期检查和更新API权限配置。
4.  **文件安全**：发送文件时，请确保文件来源安全可靠，不包含恶意内容。

## 使用场景
### 原始功能使用场景
- 检查微信助手的会话信息
- 找到当前对话的 sessionKey
- 查询所有活跃的会话列表
- 监控会话的实时状态
- 自动向微信用户发送通知或提醒文本消息

### 新增功能使用场景 (文件发送)
- 将本地生成的截图、报告、日志文件通过微信发送给自己。
- 将处理完成的图片、视频、音频或文档发送给指定的同事或机器人账号。
- 集成到自动化流程中，自动推送生成的文件结果。

---
