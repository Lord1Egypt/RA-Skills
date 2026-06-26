SKILL.md
universal-smarthome
通用智能家居支配Skill
Dominate your smart home with seamless control across Home Assistant and Tuya Smart.
通过Home Assistant（首选）和涂鸦智能（备选）操控全球品牌家电，支持模糊名称匹配。

Setup
设置
Option 1: Config File (Recommended)
选项1：配置文件（推荐）
Create ~/.config/universal-smarthome/config.json:
创建~/.config/universal-smarthome/config.json：

{
  "homeassistant": {
    "url": "http://homeassistant.local:8123",
    "token": "your-long-lived-access-token"
  },
  "tuya": {
    "access_id": "your-access-id",
    "access_secret": "your-access-secret",
    "endpoint": "https://openapi.tuyacn.com"
  }
}
Option 2: Environment Variables
选项2：环境变量
export HA_URL="http://homeassistant.local:8123"
export HA_TOKEN="your-long-lived-access-token"
export TUYA_ACCESS_ID="your-access-id"
export TUYA_ACCESS_SECRET="your-access-secret"
Getting Home Assistant Token
获取Home Assistant令牌
Open Home Assistant → Profile (bottom left)
打开Home Assistant → 个人资料（左下角）
Scroll to "Long-Lived Access Tokens"
滚动到“长期访问令牌”
Click "Create Token", name it (e.g., "Clawdbot")
点击“创建令牌”，将其命名（例如，“Clawdbot”）
Copy the token immediately (shown only once)
立即复制令牌（仅显示一次）
Getting Tuya Credentials
获取涂鸦凭据
Log in to Tuya Smart Platform (https://iot.tuya.com/)
登录涂鸦智能开放平台（https://iot.tuyacn.com/）
Create a cloud project or navigate to "Cloud Development"
创建云项目或进入“云开发”
Get access_id and access_secret from the project credentials
从项目凭据中获取access_id和access_secret
Quick Reference
快速参考
Discovery
设备发现
python3 scripts/smart.py discovery
Sync all devices from Home Assistant and Tuya to local cache.
从Home Assistant和涂鸦同步所有设备到本地缓存。

Control Devices
控制设备
# Turn on device by name
python3 scripts/smart.py control "device_name" on

# Turn off device by name
python3 scripts/smart.py control "device_name" off

# The script automatically identifies the platform (HA or Tuya) based on device ID
# 脚本根据设备ID自动识别平台（HA或涂鸦）
Device Name Matching
设备名称匹配
The script supports fuzzy name matching:
脚本支持模糊名称匹配：

# If device_cache.json contains:
# {"id": "light.living_room", "name": "客厅灯", "platform": "homeassistant"}
# User can say: "打开客厅灯" or "打开灯"
# 用户可以说：“打开客厅灯”或“打开灯”

Priority: Exact name match → ID match → Fuzzy match
优先级：精确名称匹配 → ID匹配 → 模糊匹配
CLI Wrapper
CLI包装器
The scripts/smart.py CLI provides smart home control:
scripts/smart.py CLI提供智能家居控制：

# Discovery - sync all devices
python3 scripts/smart.py discovery

# Control device by name
python3 scripts/smart.py control "客厅灯" on
python3 scripts/smart.py control "卧室灯" off

# The script will:
# 1. Look up device ID from local cache
# 2. Try Home Assistant first (preferred)
# 3. Fallback to Tuya Cloud if HA fails or device not found
# 脚本将：
# 1. 从本地缓存查找设备ID
# 2. 优先尝试Home Assistant
# 3. 若HA失败或设备不存在，回退到涂鸦云端
Supported Platforms
支持平台
Platform平台	Features功能	Priority优先级
Home Assistant	Local control, fast response, entity-based
本地控制，响应快，基于实体	1 (Primary)
首选
Tuya Cloud	Cloud API, broader device support
云端API，更广泛的设备支持	2 (Fallback)
备选
Common Issues & Solutions
常见问题与解决方案
Error: Config missing
错误：配置文件缺失
Solution: Create ~/.config/universal-smarthome/config.json
解决方案：创建~/.config/universal-smarthome/config.json

Error: 1004: Sign Invalid
错误：1004: 签名无效
Solution: Check Tuya access_id and access_secret. Ensure endpoint matches your region (cn/com/us/eu).
解决方案：检查涂鸦access_id和access_secret。确保endpoint匹配您的区域（cn/com/us/eu）。

Error: Entity not found
错误：实体未找到
Solution: Run "python3 scripts/smart.py discovery" to sync devices first.
解决方案：先运行“python3 scripts/smart.py discovery”同步设备。

Error: Connection refused (HA)
错误：连接被拒绝（HA）
Solution: Check HA_URL, ensure Home Assistant is running and accessible.
解决方案：检查HA_URL，确保Home Assistant正在运行且可访问。

Error: 401 Unauthorized (HA)
错误：401未授权（HA）
Solution: Token expired or invalid. Generate a new Long-Lived Access Token.
解决方案：令牌过期或无效。生成新的长期访问令牌。

Device not responding
设备无响应
Solutions:
解决方案：

1. Check if device is online in respective app (HA or Tuya)
   检查设备是否在相应应用（HA或涂鸦）中在线
2. Try controlling directly in Home Assistant or Tuya app
   尝试直接在Home Assistant或涂鸦应用中控制
3. Run discovery again to refresh device cache
   再次运行discovery刷新设备缓存
Architecture
架构设计
┌─────────────────┐
│   User Request  │
│   用户请求       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Semantic Parse │
│  语义解析       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Device Lookup  │
│  设备查找       │──────▶ Local Cache
│                 │       (device_cache.json)
└────────┬────────┘
         │
         ▼
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│   HA  │ │ Tuya  │
│  优先 │ │ 备选  │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         │
         ▼
┌─────────────────┐
│  Control Result │
│  控制结果       │
└─────────────────┘
Security
安全说明
Credentials are stored locally at ~/.config/universal-smarthome/
凭据存储在本地~/.config/universal-smarthome/
No hardcoded tokens or secrets in scripts
脚本中无硬编码的令牌或密钥
Only访问用户定义的HA address and Tuya official API
只访问用户定义的HA地址和涂鸦官方API
No third-party data exfiltration
无第三方数据回传
Troubleshooting
故障排除
401 Unauthorized: HA token expired or invalid. Generate a new one.
401未授权：HA令牌过期或无效。生成新的令牌。

Connection refused: Check HA_URL, ensure HA is running and accessible.
连接被拒绝：检查HA_URL，确保HA正在运行且可访问。

Entity not found: Run discovery to sync devices first.
实体未找到：先运行discovery同步设备。

1004 Sign Invalid: Verify Tuya credentials and region endpoint.
1004签名无效：验证涂鸦凭据和区域endpoint。

All platforms failed: Check network connection and device online status.
所有平台失败：检查网络连接和设备在线状态。

API Reference
API参考
For advanced usage and custom integrations, see:
高级使用和自定义集成，请参阅：

Home Assistant API: https://developers.home-assistant.io/docs/api/rest/
Tuya Cloud API: https://developer.tuya.com/en/docs/iot/api-reference/list
