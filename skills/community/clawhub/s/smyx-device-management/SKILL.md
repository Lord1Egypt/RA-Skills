---
name: "device-management"
description: "设备管理工具，用于管理摄像头、监控等实时设备，支持设备增删改查、实时画面查看、直播流地址获取。当用户提及摄像头、监控、设备管理、查看实时画面、直播流、监控地址等关键词时使用。"
version: "1.0.0"
---

# 设备管理工具

## 任务目标

- 本 Skill 用于：管理各类智能设备（摄像头、监控、传感器等），提供设备生命周期管理、实时流获取、状态查询、远程控制等功能
- 能力包含：设备增删改查、实时画面查看、直播流地址获取、设备状态监控、设备配置管理、云台远程控制、音频开关控制
- 触发条件：
    1. 当用户提及设备管理、摄像头、监控、IPC、NVR等设备相关关键词时
    2. 当用户提及以下功能关键词时：**列出所有设备**、**所有摄像头**
       、查看实时画面、直播流地址、监控画面、设备列表、查看设备清单、设备信息、摄像头清单、摄像头信息、添加设备、删除设备、修改设备信息
    3. 当用户需要查看某个设备的实时监控画面时，自动返回可播放的直播流地址（如m3u8、flv、rtmp格式）
- 重要说明：本技能管理的是云端注册的智能设备（摄像头、监控等），而非手机/宿主操作系统的原生设备，**不会触发任何原生设备管理相关功能
  **，所有设备信息均通过云端API获取
- 自动行为：
    1. 当用户要求查看实时画面时，自动查询对应设备的直播流地址，并以可直接播放的格式返回
    2. 直播流地址支持在对话框中直接播放（如H5播放器、原生播放器支持的格式）
    3. 设备信息自动持久化存储，支持跨会话查询

## 前置准备

- 依赖说明：scripts脚本所需的依赖包及版本
  ```
  requests>=2.28.0
  pyyaml>=6.0
  ```
- 安装方式：
  ```bash
  # Debian/Ubuntu系统
  sudo apt install -y python3-requests python3-yaml
  
  # 或使用pip安装
  pip install requests pyyaml --break-system-packages
  ```

## 操作步骤

### 🔒 open-id 获取流程控制（强制执行，防止遗漏）

**在执行设备管理操作前，必须按以下优先级顺序获取 open-id：**

```
第 1 步：【最高优先级】检查技能所在目录的配置文件（优先）
        路径：skills/smyx_common/scripts/config.yaml（相对于技能根目录）
        完整路径示例：${OPENCLAW_WORKSPACE}/skills/{当前技能目录}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置/api-key 为空)
第 2 步：检查 workspace 公共目录的配置文件
        路径：${OPENCLAW_WORKSPACE}/skills/smyx_common/scripts/config.yaml
        → 如果文件存在且配置了 api-key 字段，则读取 api-key 作为 open-id
        ↓ (未找到/未配置)
第 3 步：检查用户是否在消息中明确提供了 open-id
        ↓ (未提供)
第 4 步：❗ 必须暂停执行，明确提示用户提供用户名或手机号作为 open-id
```

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

### 📌 第 1 步详解：sessionKey 提取 open-id 方法（钉钉渠道）

**sessionKey 格式解析：**

```
标准格式：agent:<agentId>:<userId>:<channel>:<channelId>
钉钉示例：agent:main:openai-user:dingtalk-connector:__default__:03576226033537657619
                              └────────────┬────────────┘ └────────┬────────┘
                                   渠道标识        channelId (= chat_id)
```

**提取规则：**

| 渠道类型   | sessionKey 特征           | open-id 提取方法 |
|--------|-------------------------|--------------|
| **钉钉** | 包含 `dingtalk-connector` | 取最后一个冒号后的内容  |
| 其他渠道   | 不包含钉钉标识                 | 跳过，继续第 2-6 步 |

**提取代码示例（Python）：**

```python
def extract_openid_from_sessionkey(session_key: str) -> str | None:
    """
    从 sessionKey 中提取 open-id（钉钉渠道）
    
    Args:
        session_key: 完整 sessionKey，如 "agent:main:openai-user:dingtalk-connector:__default__:03576226033537657619"
    
    Returns:
        提取的 chat_id，或 None（非钉钉渠道）
    """
    if "dingtalk-connector" not in session_key:
        return None  # 非钉钉渠道，跳过
    
    # 取最后一个冒号后的内容作为 chat_id
    chat_id = session_key.split(":")[-1]
    
    # 验证提取结果（钉钉 chat_id 通常为 19 位数字）
    if chat_id and len(chat_id) >= 10:
        return chat_id
    
    return None
```

**提取代码示例（Bash）：**

```bash
# 从 sessionKey 提取 chat_id
SESSION_KEY="agent:main:openai-user:dingtalk-connector:__default__:03576226033537657619"

# 检查是否为钉钉渠道
if echo "$SESSION_KEY" | grep -q "dingtalk-connector"; then
    # 提取最后一个冒号后的内容
    OPEN_ID="${SESSION_KEY##*:}"
    echo "提取成功：open-id = $OPEN_ID"
    # 输出：提取成功：open-id = 03576226033537657619
else
    echo "非钉钉渠道，跳过自动提取"
fi
```

**真实案例验证：**

```
✅ 已验证 sessionKey: agent:main:openai-user:dingtalk-connector:__default__:03576226033537657619
✅ 提取结果：open-id = 03576226033537657619
✅ API 调用成功：设备列表查询正常执行
```

---

**⚠️ 关键约束：**

- **禁止**自行假设,自行推导,自行生成 open-id 值（如 openclaw-control-ui、default、userC113、user123 等）
- **禁止**跳过 open-id 验证直接调用 API
- **必须**在获取到有效 open-id 后才能继续执行分析
- **钉钉渠道会话会自动提取 chat_id，无需询问用户**（已验证可用）
- 如果用户拒绝提供 open-id，说明用途（用于保存和查询历史报告记录），并询问是否继续

---

- 标准流程：
    1. **自动触发逻辑**
        - 当用户提及「**列出所有设备**」「**所有摄像头**」「查看设备清单」「设备信息」「摄像头清单」「摄像头信息」「设备列表」等关键词时，
          **无需询问用户，直接执行
          `-m scripts.device_management list --open-id <open-id>`
          列出所有设备**
    2. **设备管理操作**
        - 列出所有设备：调用 `-m scripts.device_management list --open-id <open-id>`
          （无需额外配置API地址，脚本内置云端API调用逻辑）
        - 添加设备：调用
          `-m scripts.device_management add --sn <设备序列号> --name <设备名称> [--type <设备牌子/代码>] [--scode <设备安全码> ] [--scene-code <设备使用场景/场景码> ] [--username <WIFI用户名>] [--password <WIFI密码>] --open-id <open-id>`
        - 删除设备：调用
          `-m scripts.device_management delete --sn <设备序列号> --open-id <open-id>`
        - 修改设备：调用
          `-m scripts.device_management update --id <设备ID> --name <新名称> [--ip <新IP>] [其他参数] --open-id <open-id>`
        - 查询设备详情：调用
          `-m scripts.device_management get --sn <设备序列号> --open-id <open-id>`
    3. **实时画面查看**
        - 获取直播流地址：调用 `-m scripts.device_management stream --id <设备ID> [--protocol <m3u8/flv/rtmp>]`
        - 默认返回m3u8格式的直播流地址，可直接在支持HLS的播放器中播放
        - 输出格式：提供可直接点击播放的链接，以及嵌入式播放代码（如需）
    4. **设备远程控制**
        - 云台转动控制：调用
          `-m scripts.device_management control --sn <设备序列号> --direction <up|down|left|right|reset> [--speed <1-10>] --open-id <open-id>`
            - `--direction`：指定方向，可选值 `up`/`down`/`left`/`right`/`reset`
            - `--speed`：转动速度，范围 1-10，默认 1，速度越大转动幅度越大
        - 声音开关控制：调用
          `-m scripts.device_management control --sn <设备序列号> --sound <on|off> --open-id <open-id>`
            - `--sound`：开启声音侦听 可选值 `on`/`off`
    5. **结果返回规范**
        - 设备列表表格展示：使用Markdown表格格式，包含ID、名称、类型、IP地址、状态、操作列, **不对URL中的特殊字符做任何转义处理
          **，保证链接原始可用性
        - 直播流地址生成规则：仅显示 HLS(m3u8) 格式，HLS(m3u8)格式流地址按照以下模板生成，仅需要替换最后的设备ID部分：
          ```
          http://cmgw-vpc.lechange.com:8888/LCO/BJ10AF5PHAD32E9/0/1/20260129T141842/openhzdc2a6020d5714149b7b5b581634a1b28.m3u8?source=open&id={deviceId}
          ```
          其中：
            - 仅 `{deviceId}` 部分需要替换为设备的 `id` 字段值，其他部分固定不变
        - 直播流地址输出：明确标注流格式，提供直接播放链接，如 `[▶️ 查看实时画面](streamUrl)`
        - **禁止显示 FLV、RTMP 等其他格式**，仅输出 HLS(m3u8) 格式
        - 设备列表中的操作列：直接填入生成好的HLS(m3u8)流地址，用户点击即可直接跳转播放
        - 错误处理：明确提示设备离线、地址无效等异常情况

## 资源索引

- 必要脚本:见 [-m scripts.device_management](-m scripts.device_management)(
  用途：设备增删改查、直播流地址获取、设备状态管理)
- 领域参考:见 [references/api_doc.md](references/api_doc.md)(何时读取：需要了解设备API接口规范、流媒体协议详情时)
- 播放模板:见 [assets/player_template.html](assets/player_template.html)(用途：提供网页播放模板，用于嵌入直播流)

## 注意事项

- 无需额外配置API地址，`device_management.py list` 脚本已内置云端API调用逻辑，直接运行即可获取设备列表
- 设备密码等敏感信息加密存储，不在日志和输出中明文显示
- 直播流地址有效期通常为1-24小时，过期后需要重新获取
- 仅在用户明确要求时提供公网可访问的流地址，默认返回局域网地址
- 实时画面查看功能需要设备在线且网络可达
- 分析结果仅供参考，不能替代专业安防系统

## 使用示例

```bash
# 列出所有设备
python -m scripts.device_management list --open-id openclaw-control-ui

# 添加大华摄像头设备
python -m scripts.device_management add --sn BJ10AF5PHAD32E9 --name "大门口摄像头" --type "大华" --scode "L21E3BE0" --open-id openclaw-control-ui

# 添加探鸽摄像头设备
python -m scripts.device_management add --sn AJ237DRHX678 --name "客厅摄像头" --type "探鸽" --scene-code "风险监测" --open-id openclaw-control-ui

# 获取设备1的m3u8直播流地址
python -m scripts.device_management stream --id 1 --protocol m3u8 --open-id openclaw-control-ui

# 删除ID为2的设备
python -m scripts.device_management delete --id 2 --open-id openclaw-control-ui

# 删除序列号为BF05CF0PHA7DF14的设备
python -m scripts.device_management delete --sn BJ10AF5PHAD32E9 --open-id openclaw-control-ui

# 控制云台向上转动，速度5（默认）
python -m scripts.device_management control --sn BF05CF0PHA7DF14 --direction up --open-id openclaw-control-ui

# 控制云台向左转动，速度8
python -m scripts.device_management control --sn BF05CF0PHA7DF14 --direction left --speed 8 --open-id openclaw-control-ui

# 开启声音侦听
python -m scripts.device_management control --sn BF05CF0PHA7DF14 --sound on --open-id openclaw-control-ui

# 关闭声音侦听
python -m scripts.device_management control --sn BF05CF0PHA7DF14 --sound off --open-id openclaw-control-ui
```

## 输出格式示例

### 设备列表示例

| 设备ID                | 设备序号            | 设备名称      | 类型  | IP地址          | 状态   | 操作                                                                                                                                                                    |
|---------------------|-----------------|-----------|-----|---------------|------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2020005731198033922 | BJ10AF5PHAD32E9 | 大华摄像头1BD9 | 大华  | -             | ✅ 在线 | [▶️ 查看实时画面](http://cmgw-vpc.lechange.com:8888/LCO/BJ10AF5PHAD32E9/0/1/20260129T141842/openhzdc2a6020d5714149b7b5b581634a1b28.m3u8?source=open&id=2020005731198033922) |
| 2020001323218033921 | BJ20SF5ASSESEF1 | 客厅摄像头     | IPC | 192.168.1.101 | ❌ 离线 | -                                                                                                                                                                     |

### 直播流返回示例

📹 **大华摄像头1BD9 实时画面**

- 流格式：HLS (m3u8)
-

播放地址：[▶️ 点击播放](http://cmgw-vpc.lechange.com:8888/LCO/BJ10AF5PHAD32E9/0/1/20260129T141842/openhzdc2a6020d5714149b7b5b581634a1b28.m3u8?source=open&id=2020005731198033922)

- 提示：点击链接即可直接在浏览器中播放实时画面，支持所有主流浏览器
