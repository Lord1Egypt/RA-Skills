# weDa-integration - 微搭 WeDa 集成技能

_版本：V1.0 | 创建时间：2026-03-08 | 状态：测试中_

---

## 📋 技能描述

集成腾讯云微搭 WeDa 低代码平台 API，实现微信小程序自动化创建、更新、发布。

**微搭 WeDa：** 腾讯官方低代码开发平台，与微信生态深度集成。

---

## 🔑 前置条件

### 1. 腾讯云账号
- 注册腾讯云账号：https://cloud.tencent.com/
- 完成实名认证（个人或企业）

### 2. 开通微搭 WeDa
- 访问微搭控制台：https://cloud.tencent.com/product/weda
- 开通微搭服务（有免费额度）

### 3. 获取 API 密钥
- 访问 CAM 控制台：https://console.cloud.tencent.com/cam
- 创建 API 密钥（SecretId + SecretKey）
- 保存密钥（只显示一次）

### 4. 微信小程序账号
- 注册微信小程序：https://mp.weixin.qq.com/
- 完成微信认证（300 元）
- 获取 AppID

---

## ⚙️ 配置方式

### 方式 1：环境变量（推荐）
```powershell
# 添加到系统环境变量
$env:WEDA_SECRET_ID = "你的 SecretId"
$env:WEDA_SECRET_KEY = "你的 SecretKey"
$env:WEDA_APP_ID = "你的小程序 AppID"
```

### 方式 2：配置文件
在 `workspace/.weda-config.json` 中配置：
```json
{
  "secretId": "你的 SecretId",
  "secretKey": "你的 SecretKey",
  "appId": "你的小程序 AppID",
  "region": "ap-guangzhou"
}
```

---

## 🎯 核心功能

### 1. 创建小程序应用
```powershell
# 调用示例
调用 weDa-integration 技能
动作：create-app
参数：
  - name: 应用名称
  - description: 应用描述
  - template: 模板 ID（可选）
```

### 2. 更新应用配置
```powershell
# 调用示例
调用 weDa-integration 技能
动作：update-app
参数：
  - appId: 应用 ID
  - config: 配置对象（JSON）
```

### 3. 发布小程序
```powershell
# 调用示例
调用 weDa-integration 技能
动作：deploy-app
参数：
  - appId: 应用 ID
  - version: 版本号
  - description: 版本描述
```

### 4. 获取应用列表
```powershell
# 调用示例
调用 weDa-integration 技能
动作：list-apps
```

### 5. 删除应用
```powershell
# 调用示例
调用 weDa-integration 技能
动作：delete-app
参数：
  - appId: 应用 ID
```

---

## 📚 API 参考

### 微搭 WeDa API 端点
```
基础 URL：https://weda.tencentcloudapi.com
接口版本：2021-09-22
签名方法：TC3-HMAC-SHA256
```

### 核心 API 接口

#### 1. CreateApp（创建应用）
```json
{
  "Action": "CreateApp",
  "Version": "2021-09-22",
  "Region": "ap-guangzhou",
  "Name": "应用名称",
  "Description": "应用描述",
  "TemplateId": "模板 ID（可选）"
}
```

#### 2. DescribeApps（查询应用列表）
```json
{
  "Action": "DescribeApps",
  "Version": "2021-09-22",
  "Limit": 10,
  "Offset": 0
}
```

#### 3. ReleaseApp（发布应用）
```json
{
  "Action": "ReleaseApp",
  "Version": "2021-09-22",
  "AppId": "应用 ID",
  "Version": "版本号",
  "Description": "版本描述"
}
```

---

## 🔧 使用示例

### 示例 1：创建万物卡片化小程序
```powershell
# 调用技能
调用 weDa-integration 技能
动作：create-app
参数：
  name: 万物卡片化
  description: 卡片化 UGC 平台
  template: card-platform-template
```

### 示例 2：查询应用状态
```powershell
# 调用技能
调用 weDa-integration 技能
动作：list-apps
```

### 示例 3：发布小程序
```powershell
# 调用技能
调用 weDa-integration 技能
动作：deploy-app
参数：
  appId: weda_xxx123
  version: 1.0.0
  description: MVP 版本上线
```

---

## ⚠️ 注意事项

### 安全提示
- **SecretKey 绝密**：不要提交到代码仓库
- **权限最小化**：CAM 策略只开通微搭相关权限
- **定期轮换**：建议每 90 天更换 API 密钥

### 限制说明
- **免费额度**：微搭有免费额度，超出后付费
- **发布审核**：小程序发布需微信官方审核（1-3 个工作日）
- **API 调用频率**：腾讯云 API 有调用频率限制

### 人工确认环节
- ✅ 可自动化：创建应用、更新配置、查询状态
- ⚠️ 需人工：微信认证（300 元支付）、发布审核提交

---

## 🐛 故障排查

### 问题 1：认证失败
```
错误：Signature failure
原因：SecretId 或 SecretKey 错误
解决：检查配置文件，重新获取密钥
```

### 问题 2：权限不足
```
错误：UnauthorizedOperation
原因：CAM 策略未开通微搭权限
解决：在 CAM 控制台添加 WeDa 全量访问权限
```

### 问题 3：应用已存在
```
错误：ResourceInUse
原因：应用名称重复
解决：更换应用名称或使用其他模板
```

---

## 📝 版本记录

| 版本号 | 修改时间 | 修改内容 | 修改人 |
|--------|----------|----------|--------|
| V1.0 | 2026-03-08 16:57 | 初始版本，创建技能框架 | 阿福 |

---

## 🔗 关联资源

- 微搭官方文档：https://cloud.tencent.com/document/product/1301
- API 文档：https://cloud.tencent.com/document/api/1301/52254
- SDK 下载：https://github.com/TencentCloud/tencentcloud-sdk-python

---

_本技能由阿福维护，用于万物卡片化项目微信小程序开发_
