# Feishu Calendar Skill

飞书日历智能助手 - 支持用户身份的日程管理和会议室预约

## 触发条件

当用户提到以下关键词时使用此技能：
- 日程、会议、预约、日历
- 会议室、房间
- 查看日程、修改会议、取消会议
- 邀请某人开会

## 功能

- 📅 **日程 CRUD**：创建、查询、修改、删除日程
- 🏢 **会议室管理**：查询、预约、取消会议室
- 👤 **用户身份**：以用户身份操作，显示为本人发起
- 🧠 **智能解析**：从自然语言中提取字段

## 指令解析

### 时间解析
- 相对时间：今天、明天、后天、下周X、本周X
- 绝对时间：X月X日、X号
- 具体时刻：早上9点、下午3点、14:30

### 人员解析
- 邀请+人名
- @人名
- 和+人名+开会

### 时长解析
- 默认1小时
- X小时、X分钟、Xh

## API 调用规范

### 用户授权流程
1. 检查是否已有 user_access_token
2. 如果没有或已过期，生成授权链接
3. 用户授权后保存 code 换取的 token

### 日程操作
1. 使用 user_access_token 获取用户主日历
2. 创建/查询/修改/删除事件
3. 添加/移除参会者
4. 关联会议室预约

### 会议室操作
1. 使用 tenant_access_token 查询会议室列表
2. 使用 user_access_token 进行预约

## 存储位置

- 用户 Token: `/root/.openclaw/credentials/feishu-user-token.json`
- 辅助脚本: `/root/.openclaw/workspace/skills/feishu-calendar/feishu-calendar.sh`

## 临时方案（用户授权未完成时）

在用户授权完成前，使用「日历助手」身份预约时，**必须在会议描述/备注中添加预约人信息**：

```
预约人：{用户姓名}
预约时间：{当前日期}
通过小咔拉咪助手预约
```

这样可以明确标识实际预约人。

## 用户授权配置

### 飞书开放平台配置

1. **配置回调地址**
   - 安全设置 → 重定向 URL
   - 添加：`https://your-domain.com/feishu/oauth/callback`

2. **申请用户身份权限**
   - 权限管理 → 找到以下权限
   - 确保申请了**用户身份（user）**权限：
     - `calendar:calendar` → 用户身份
     - `calendar:calendar.event` → 用户身份
     - `calendar:room` → 用户身份
     - `contact:user.base:readonly` → 用户身份

3. **发布应用**

### 授权流程

1. 生成授权链接（包含 scope 参数）
2. 用户点击授权
3. 获取回调的 code
4. 用 code 换取 user_access_token
5. 保存 token 到 `/root/.openclaw/credentials/feishu-user-token.json`

### 注意事项

- 飞书权限分为两种：**租户权限（tenant）** 和 **用户权限（user）**
- 租户权限：机器人身份操作
- 用户权限：用户身份操作
- 日历预约需要用户权限才能以用户身份操作
