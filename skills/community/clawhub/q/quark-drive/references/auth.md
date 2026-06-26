# 夸克网盘扫码登录流程

## 概述

扫码登录是夸克网盘推荐的登录方式，安全且便捷。

## 登录流程

```
1. 获取二维码 Token
   ↓
2. 生成二维码 URL
   ↓
3. 用户扫码
   ↓
4. 检查登录状态
   ↓
5. 获取 Service Ticket
   ↓
6. 使用 Ticket 获取 Cookie
   ↓
7. 保存 Cookie
```

## API 端点

### 1. 获取二维码 Token

**URL**: `https://uop.quark.cn/cas/ajax/getTokenForQrcodeLogin`

**参数**:
- `client_id`: 固定值 `532`
- `v`: 版本号 `1.2`
- `request_id`: 随机 UUID

**响应**:
```json
{
  "status": 2000000,
  "message": "ok",
  "data": {
    "members": {
      "token": "xxx"
    }
  }
}
```

### 2. 检查登录状态

**URL**: `https://uop.quark.cn/cas/ajax/getServiceTicketByQrcodeToken`

**参数**:
- `client_id`: 固定值 `532`
- `v`: 版本号 `1.2`
- `token`: 二维码 Token
- `request_id`: 随机 UUID

**响应**:
```json
{
  "status": 2000000,
  "message": "ok",
  "data": {
    "members": {
      "service_ticket": "xxx"
    }
  }
}
```

### 3. 获取用户信息（设置 Cookie）

**URL**: `https://pan.quark.cn/account/info`

**参数**:
- `st`: Service Ticket
- `lw`: 登录方式 `scan`

## Cookie 说明

登录成功后会获取以下关键 Cookie：

| Cookie | 说明 |
|--------|------|
| `__pus` | 主要认证 Cookie |
| `__kps` | 会话 Cookie |
| `__uid` | 用户 ID |

## 二维码 URL 格式

```
https://su.quark.cn/4_eMHBJ?token={token}&client_id=532&ssb=weblogin&uc_param_str=&uc_biz_str=S:custom|OPT:SAREA@0|OPT:IMMERSIVE@1|OPT:BACK_BTN_STYLE@0
```

## 超时处理

- 二维码有效期：约 5 分钟
- 建议轮询间隔：2 秒
- 超时后需重新获取二维码

## 错误处理

| 状态码 | 说明 |
|--------|------|
| 2000000 | 成功 |
| 50004001 | 等待扫码 |
| 50004002 | 二维码过期 |
| 50004003 | 登录失败 |
| 50004004 | 取消登录 |
