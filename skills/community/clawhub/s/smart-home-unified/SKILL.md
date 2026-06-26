# Smart Home Unified - 智能家居统一控制

## ⚠️ 重要说明

本技能已实现**真实 API 集成**，需要用户自行配置设备 API 密钥。

## 🔧 配置指南

### 1. 安装依赖

```bash
# 安装技能
clawhub install smart-home-unified

# 安装平台特定依赖（根据需要选择）
npm install -g miio        # 小米米家设备
npm install -g hap-nodejs  # Apple HomeKit 设备
```

### 2. 获取设备 Token

#### 小米米家设备
```bash
# 安装 miio 工具
npm install -g miio

# 提取设备 token
miio extract --token <token>

# 发现设备
miio discover
```

#### Apple HomeKit 设备
- 在 Apple Home App 中配对设备
- 获取配件 PIN 码（通常在设备底部或说明书上）

### 3. 配置凭证

在 `TOOLS.md` 中添加配置：

```markdown
### Smart Home - 智能家居配置

#### 小米米家
- xiaomi:
  - username: "你的小米账号"
  - password: "你的小米密码"
  - device_token: "设备 token（通过 miio extract 获取）"

#### Apple HomeKit
- homekit:
  - pin_code: "配件 PIN 码（8 位数字，格式：XXX-XX-XXX）"
  - username: "Apple ID（可选，用于 iCloud 同步）"
  - password: "Apple 密码（可选）"
```

## 🚀 使用示例

### 发现设备
```bash
smart-home discover --platform xiaomi
smart-home discover --platform homekit
```

### 控制设备
```bash
# 打开灯
smart-home control --device "客厅主灯" --action turnOn

# 调节亮度
smart-home control --device "卧室灯" --action setBrightness --level 80

# 设置空调温度
smart-home control --device "客厅空调" --action setTemperature --temp 26
```

### 查看状态
```bash
smart-home status --all
smart-home status --device "客厅主灯"
```

## ⚠️ 注意事项

1. **本地网络要求**：设备必须在同一局域网内
2. **Token 有效期**：小米设备 token 可能定期更换
3. **防火墙设置**：确保 UDP 端口 54321 开放（小米设备）
4. **HomeKit 配对**：需要先通过 Home App 配对设备

## 📞 技术支持

- 文档：https://github.com/your-repo/smart-home-unified
- 问题反馈：https://github.com/your-repo/smart-home-unified/issues
- 邮件：support@smarthomeunified.com

## 💰 定价

**$99-299/月** - 包含所有平台无限次使用

- 基础版 $99/月：支持 10 个设备
- 专业版 $199/月：支持 50 个设备 + 场景联动
- 企业版 $299/月：无限设备 + 定制集成

---

**⚠️ 安全提示**：本技能需要访问你的智能家居设备，请确保：
1. 只在可信环境中使用
2. 定期更换设备 token/密码
3. 不要分享配置文件
