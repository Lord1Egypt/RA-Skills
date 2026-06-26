# 微信公众号发布技能 - 安装手册

**版本：** V2.0.1  
**最后更新：** 2026-04-04  
**技能名称：** wechat-publisher  

---

## 📋 安装前准备

### 系统要求

| 要求 | 说明 |
|------|------|
| **OpenClaw** | v1.0.0 或更高版本 |
| **Node.js** | v18.0.0 或更高版本 |
| **操作系统** | Windows / macOS / Linux |
| **网络** | 可访问微信 API 和 clawhub.com |

### 公众号要求

| 要求 | 说明 |
|------|------|
| **公众号类型** | 订阅号或服务号 |
| **AppID** | 公众号唯一标识 |
| **AppSecret** | 公众号密钥 |
| **IP 白名单** | 需配置服务器出口 IP |

---

## 🚀 快速安装

### 步骤 1：安装技能

```bash
openclaw skill install wechat-publisher
```

**安装过程：**
```
📦 Installing wechat-publisher@latest...
✅ Downloaded wechat-publisher-skill
✅ Installed to ~/.agents/skills/wechat-publisher
✅ Dependencies installed
🎉 Installation complete!
```

### 步骤 2：配置公众号

```bash
openclaw skill config wechat-publisher
```

**需要配置：**
```
? Enter your 公众号 AppID: wxebff9eadface1489
? Enter your 公众号 AppSecret: 44c10204ceb1bfb3f7ac096754976454
? Enter publish schedule (default: 06:00): 06:00
? Enter timezone (default: Asia/Shanghai): Asia/Shanghai
✅ Configuration saved!
```

### 步骤 3：设置发布时间

```bash
openclaw schedule wechat-publisher 06:00
```

**说明：**
- 默认每天 06:00 自动发布
- 可根据需要修改时间
- 时区默认东八区（Asia/Shanghai）

### 步骤 4：发布测试

```bash
openclaw skill run wechat-publisher --test
```

**测试结果：**
```
🚀 Starting test publish...
📝 Collecting news...
✅ Collected 32 news items
🎨 Generating HTML...
📤 Publishing to WeChat...
✅ Draft created: bEleejFU9wv67FJfDm4w_xxx
🎉 Test publish complete!
```

---

## 🔧 详细配置

### 配置项说明

| 配置项 | 说明 | 默认值 | 是否必填 |
|--------|------|--------|----------|
| `app_id` | 公众号 AppID | - | ✅ 是 |
| `app_secret` | 公众号 AppSecret | - | ✅ 是 |
| `schedule` | 发布时间 | `06:00` | ❌ 否 |
| `template` | 发布模板 | `block-v3` | ❌ 否 |
| `news_count` | 新闻条数 | `32` | ❌ 否 |
| `timezone` | 时区 | `Asia/Shanghai` | ❌ 否 |
| `qrcode_url` | 二维码 URL | 素材库 qrcode.jpg | ❌ 否 |

### 获取公众号配置

**1. 登录公众号后台**
```
https://mp.weixin.qq.com/
```

**2. 找到开发配置**
```
开发 → 基本配置 → 公众号开发信息
```

**3. 复制 AppID 和 AppSecret**
- AppID：如 `wxebff9eadface1489`
- AppSecret：如 `44c10204ceb1bfb3f7ac096754976454`

**注意：** AppSecret 是敏感信息，请妥善保管！

---

## ⚙️ 环境配置

### 1. IP 白名单配置

**微信公众号后台需要添加服务器 IP 到白名单：**

**步骤：**
1. 登录 https://mp.weixin.qq.com/
2. 设置 → 公众号设置 → 功能设置
3. 找到 IP 白名单
4. 添加当前出口 IP

**获取出口 IP：**
```bash
# Windows PowerShell
curl http://ip-api.com/json/

# macOS / Linux
curl -s http://ip-api.com/json/
```

**示例输出：**
```json
{
  "query": "123.45.67.89",
  "country": "China",
  "regionName": "Beijing"
}
```

**添加 IP：**
- 复制 `query` 字段的 IP 地址
- 添加到公众号 IP 白名单
- 保存配置

**注意：** 如未配置 IP 白名单，API 调用会返回 `40164 invalid ip` 错误。

### 2. 二维码图片上传

**上传到公众号素材库：**

**步骤：**
1. 登录公众号后台 → 素材管理 → 图片
2. 点击"上传"按钮
3. 选择公众号二维码图片
4. 命名为 `qrcode.jpg`
5. 保存到素材库

**图片要求：**
- 格式：JPG 或 PNG
- 尺寸：建议 200×200px 或更大
- 内容：清晰的公众号二维码
- 大小：不超过 2MB

**系统自动使用：**
- 技能会自动检测素材库中的 `qrcode.jpg`
- 发布时自动使用此图片
- 无需手动配置 URL

---

## 💰 授权激活

### 试用版

- **次数：** 50 次免费使用
- **有效期：** 约 1 个月
- **功能：** 完整功能，无限制

**自动激活：**
```bash
# 安装后自动获得 50 次试用
openclaw skill install wechat-publisher
```

### 专业版

- **价格：** 8.8 元永久买断
- **次数：** 无限次使用
- **更新：** 免费享受所有更新

**购买流程：**
```bash
openclaw skill buy wechat-publisher
```

**支付方式：**
- 微信扫码支付
- 支付宝扫码支付

**获取激活码：**
- 微信：添加管理员微信 `lylovejava`（备注：技能购买）
- 邮箱：`support@wechat-publisher.ai`
- 公众号：关注"小蛋蛋助手"，发送订单号

**激活技能：**
```bash
openclaw skill activate wechat-publisher
# 输入激活码
```

---

## 📁 安装位置

### 默认安装路径

| 系统 | 路径 |
|------|------|
| **Windows** | `C:\Users\<用户名>\.agents\skills\wechat-publisher\` |
| **macOS** | `/Users/<用户名>/.agents/skills/wechat-publisher/` |
| **Linux** | `/home/<用户名>/.agents/skills/wechat-publisher/` |

### 文件结构

```
wechat-publisher/
├── SKILL.md              # 技能定义
├── skill.md              # 详细说明
├── changelog.md          # 更新日志
├── publish.py            # 发布脚本
├── docs/
│   ├── install-guide.md  # 安装手册（本文件）
│   ├── user-guide.md     # 用户手册
│   ├── templates.md      # 模板说明
│   └── block-layout.md   # 块布局规范
└── templates/
    └── block-v3.html     # 块布局 v3.0 模板
```

---

## 🔍 验证安装

### 检查技能状态

```bash
openclaw skill status wechat-publisher
```

**正常输出：**
```
Skill: wechat-publisher
Version: 2.0.1
Status: ✅ Active
Usage: 0/50 (Trial)
Next publish: 2026-04-05 06:00:00
```

### 查看配置

```bash
openclaw skill config wechat-publisher --show
```

**输出示例：**
```
app_id: wxebff9eadface1489
app_secret: 44c10204ceb1bfb3f7ac096754976454
schedule: 06:00
template: block-v3
news_count: 32
timezone: Asia/Shanghai
```

### 测试发布

```bash
openclaw skill run wechat-publisher --test
```

**测试成功标志：**
- ✅ 收集到 32 条新闻
- ✅ 生成 HTML 成功
- ✅ 创建草稿成功
- ✅ DraftID 不为空

---

## ⚠️ 常见问题

### 1. 安装失败

**错误：** `Skill not found`

**解决：**
```bash
# 检查 clawhub 连接
clawhub list

# 重新安装
openclaw skill install wechat-publisher --force
```

### 2. 配置失败

**错误：** `Invalid AppID or AppSecret`

**解决：**
1. 检查 AppID 和 AppSecret 是否正确
2. 确认公众号已认证
3. 确认 IP 白名单已配置

### 3. API 调用失败

**错误：** `40164 invalid ip`

**解决：**
1. 获取当前出口 IP
2. 添加到公众号 IP 白名单
3. 等待 5 分钟后重试

### 4. 二维码不显示

**原因：** 素材库无 qrcode.jpg

**解决：**
1. 登录公众号后台 → 素材管理 → 图片
2. 上传二维码图片，命名为 `qrcode.jpg`
3. 重新发布

### 5. 试用次数用完

**提示：** `Trial usage limit reached`

**解决：**
```bash
# 购买专业版
openclaw skill buy wechat-publisher

# 联系管理员获取激活码
# 微信：lylovejava
```

---

## 📞 技术支持

### 联系方式

| 方式 | 说明 |
|------|------|
| **微信** | `lylovejava`（备注：安装问题） |
| **邮箱** | `support@wechat-publisher.ai` |
| **GitHub** | https://github.com/403914291/issues |
| **公众号** | 关注"小蛋蛋助手"，发送问题 |

### 响应时间

- 工作日：24 小时内回复
- 周末：48 小时内回复
- 紧急问题：微信联系（优先处理）

### 在线文档

- **clawhub 页面：** https://clawhub.com/skill/wechat-publisher
- **GitHub 仓库：** https://github.com/403914291/wechat-publisher-skill

---

## 📝 更新历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| V2.0.1 | 2026-04-04 | 新增安装手册 |
| V2.0.0 | 2026-04-04 | 块布局 v3.0 固定版 |
| V1.1.8 | 2026-03-29 | 超链接增强版 |
| V1.0.0 | 2026-03-26 | 初始版本 |

---

_维护者：小蛋蛋 🦞_
_版本：V2.0.1_
_最后更新：2026-04-04 22:12_
