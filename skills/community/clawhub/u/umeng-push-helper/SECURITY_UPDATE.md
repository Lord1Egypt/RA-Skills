# API 安全限制更新说明

## 📋 更新概述

已为友盟推送助手技能添加 API 调用安全限制，**严格禁止**调用 4 个敏感接口，防止误操作或恶意操作。

## 🔒 禁止调用的接口（4 个）

| 序号 | 接口 URL | 用途 | 风险等级 | 禁止原因 |
|------|---------|------|---------|---------|
| 1 | `https://upush.umeng.com/hsf/push/sendMsg` | 发送推送消息 | 🔴 高危 | 可能向用户发送骚扰消息 |
| 2 | `https://upush.umeng.com/hsf/setting/updateApp` | 修改应用配置 | 🔴 高危 | 可能影响正常业务运行 |
| 3 | `https://upush.umeng.com/hsf/setting/updateChannelInfo` | 修改渠道信息 | 🔴 高危 | 可能影响数据统计和渠道管理 |
| 4 | `https://upush.umeng.com/hsf/setting/saveReceipt` | 保存回执配置 | 🟡 中危 | 需要通过官方后台执行 |

## ✅ 允许调用的接口（只读操作）

| 接口 | 用途 | 状态 |
|------|------|------|
| `listAll` | 获取应用列表 | ✅ 允许 |
| `messageOverview` | 消息概览 | ✅ 允许 |
| `diagnosisSummery` | 诊断摘要 | ✅ 允许 |
| `diagnosisReport` | 诊断报告 | ✅ 允许 |

## 📁 更新的文件

### 1. `SKILL.md` - 技能定义文件
**变更内容**:
- ✅ 在"功能概述"后添加"⚠️ 安全限制"章节
- ✅ 列出所有禁止调用的接口及原因
- ✅ 在"错误处理"中添加拒绝调用的标准回复模板
- ✅ 明确处理原则：态度坚定但礼貌，不提供绕过方法

**新增章节**:
```markdown
## ⚠️ 安全限制 - 禁止调用的接口

**重要**：出于安全考虑，本技能**严格禁止**调用以下敏感接口：

| 序号 | 禁止调用的接口 | 用途 | 风险等级 |
|------|--------------|------|---------|
| 1 | `sendMsg` | 发送推送消息 | 🔴 高危 |
| 2 | `updateApp` | 修改应用配置 | 🔴 高危 |
| 3 | `updateChannelInfo` | 修改渠道信息 | 🔴 高危 |
| 4 | `saveReceipt` | 保存回执配置 | 🟡 中危 |
```

### 2. `README.md` - 使用说明
**变更内容**:
- ✅ 在文档开头添加"⚠️ 安全限制"醒目提示
- ✅ 更新目录结构，添加 `security_interceptor.py`
- ✅ 明确说明仅支持查询类操作

### 3. `scripts/security_interceptor.py` - API 安全拦截器 ⭐
**新增文件**:
- ✅ 实现 URL 检查和拦截逻辑
- ✅ 提供友好的错误提示信息
- ✅ 支持命令行测试模式

**核心功能**:
```python
# 禁止调用的接口列表（黑名单）
FORBIDDEN_APIS = [
    {'url': 'sendMsg', 'name': '发送推送消息', 'risk': '高危'},
    {'url': 'updateApp', 'name': '修改应用配置', 'risk': '高危'},
    {'url': 'updateChannelInfo', 'name': '修改渠道信息', 'risk': '高危'},
    {'url': 'saveReceipt', 'name': '保存回执配置', 'risk': '中危'}
]

# 检查函数
def check_api_url(url):
    # 检查是否在禁止列表中
    for forbidden in FORBIDDEN_APIS:
        if forbidden['url'] in url:
            return False, format_forbidden_message(forbidden)
    return True, "允许调用"
```

**使用方法**:
```bash
# 检查单个 URL
python scripts/security_interceptor.py check "<url>"

# 列出所有禁止和允许的接口
python scripts/security_interceptor.py list

# 测试模式
python scripts/security_interceptor.py test
```

## 🧪 测试结果

### 测试 1: 检查禁止的接口
```bash
$ python scripts/security_interceptor.py check "https://upush.umeng.com/hsf/push/sendMsg"
✗ 禁止调用：⚠️ 安全限制 - 禁止调用的接口

接口名称：发送推送消息
接口地址：https://upush.umeng.com/hsf/push/sendMsg
风险等级：高危
禁止原因：此操作会向用户发送推送消息，可能导致误操作或骚扰用户

抱歉，出于安全考虑，本技能禁止调用此接口。

建议您：
1. 登录友盟官方后台手动执行此操作：https://upush.umeng.com
2. 使用本技能的查询功能（只读操作）
```

### 测试 2: 检查允许的接口
```bash
$ python scripts/security_interceptor.py check "https://upush.umeng.com/hsf/home/listAll"
✓ 允许调用：✓ URL 验证通过：https://upush.umeng.com/hsf/home/listAll
```

### 测试 3: 测试模式
```bash
$ python scripts/security_interceptor.py test
测试模式 - 检查所有禁止的接口...
❌ 禁止 - 发送推送消息: https://upush.umeng.com/hsf/push/sendMsg
❌ 禁止 - 修改应用配置: https://upush.umeng.com/hsf/setting/updateApp
❌ 禁止 - 修改渠道信息: https://upush.umeng.com/hsf/setting/updateChannelInfo
❌ 禁止 - 保存回执配置: https://upush.umeng.com/hsf/setting/saveReceipt

测试模式 - 检查所有允许的接口...
✅ 允许 - https://upush.umeng.com/hsf/home/listAll
✅ 允许 - https://upush.umeng.com/hsf/push/messageOverview
✅ 允许 - https://upush.umeng.com/hsf/push/diagnosisSummery
✅ 允许 - https://upush.umeng.com/hsf/push/diagnosisReport
```

## 🛡️ 安全防护机制

### 三层防护

#### 第一层：文档说明
- ✅ 在 SKILL.md 和 README.md 中明确标注禁止调用的接口
- ✅ 告知用户风险等级和禁止原因
- ✅ 提供替代方案（官方后台）

#### 第二层：代码拦截
- ✅ 在 API 请求前调用 `security_interceptor.check_api_url()`
- ✅ 发现禁止的接口立即阻止请求
- ✅ 返回详细的错误提示和引导信息

#### 第三层：用户教育
- ✅ 每次拒绝时说明安全原因
- ✅ 引导用户使用官方后台
- ✅ 强调只读操作的安全性

### 标准拒绝话术

当用户请求调用禁止接口时，统一回复：

```
抱歉，出于安全考虑，本技能禁止调用以下类型的接口：

❌ 发送推送消息 (sendMsg)
❌ 修改应用配置 (updateApp)
❌ 修改渠道信息 (updateChannelInfo)
❌ 保存回执配置 (saveReceipt)

这些操作涉及账号安全和数据修改，需要您登录友盟官方后台 
(https://upush.umeng.com) 手动执行。

本技能仅支持查询类操作（只读），如：
✅ 获取应用列表
✅ 查询推送数据
✅ 查看诊断报告
```

## 💡 使用示例

### 场景 1: 用户请求发送推送
**用户**: "帮我给所有用户发一条推送消息"

**回复**:
```
抱歉，出于安全考虑，本技能禁止调用 sendMsg 接口发送推送消息。

原因：此操作会向用户发送消息，可能导致误操作或骚扰用户。

建议操作：
1. 登录友盟官方后台：https://upush.umeng.com
2. 进入"推送" -> "创建推送"页面
3. 填写推送内容和目标用户
4. 确认发送

如需查询推送数据，我可以帮助您：
✅ 查看应用列表
✅ 查询推送统计
✅ 分析送达率和点击率
```

### 场景 2: 用户请求修改应用配置
**用户**: "帮我更新一下应用名称"

**回复**:
```
抱歉，出于安全考虑，本技能禁止调用 updateApp 接口修改应用配置。

原因：此操作会修改应用配置，可能影响正常业务。

建议操作：
1. 访问 https://upush.umeng.com/apps/list
2. 找到对应应用，点击"配置"
3. 在应用设置中修改名称
4. 保存更改

我可以帮您查询应用信息：
✅ 获取应用列表
✅ 查看应用详情
```

## 🎯 最佳实践

### 对于开发者
1. **始终使用白名单机制**：只允许明确的只读接口
2. **提供清晰的错误信息**：告知用户为什么被拒绝
3. **引导到官方渠道**：提供官方后台链接和操作步骤
4. **不留下任何绕过方法**：代码层面严格拦截

### 对于用户
1. **理解安全限制**：这些限制保护您的账号安全
2. **使用正确的工具**：查询用技能，修改用官方后台
3. **定期更新 Cookie**：保持会话安全
4. **遇到问题及时反馈**：联系技术支持

## 📊 影响评估

### 受影响的功能
- ❌ 发送推送消息 - 需使用官方后台
- ❌ 修改应用配置 - 需使用官方后台
- ❌ 修改渠道信息 - 需使用官方后台
- ❌ 保存回执配置 - 需使用官方后台

### 不受影响的功能
- ✅ 获取应用列表 - 正常使用
- ✅ 查询消息概览 - 正常使用
- ✅ 查看诊断摘要 - 正常使用
- ✅ 获取诊断报告 - 正常使用
- ✅ Cookie 管理 - 正常使用

### 向后兼容性
- ✅ 现有查询功能完全兼容
- ✅ Cookie 管理逻辑不变
- ✅ API 调用方式不变（只增加了安全检查）

## 🚀 未来计划

### 短期（v1.2.0）
- [ ] 在 api_request.py 中集成自动拦截
- [ ] 添加更多只读接口的支持
- [ ] 优化错误提示信息

### 中期（v1.3.0）
- [ ] 实现接口调用日志记录
- [ ] 添加调用频率限制
- [ ] 提供操作审计功能

### 长期（v2.0.0）
- [ ] 支持多账号安全管理
- [ ] 实现基于角色的访问控制
- [ ] 提供企业级安全策略

---

*更新时间：2026-03-31*  
*版本：v1.2.0*  
*安全级别：🔒 高*
