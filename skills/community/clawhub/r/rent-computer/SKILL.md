---
name: rent-computer
description: 当用户电脑性能不足，或者希望租赁高性能电脑时，帮助用户完成电脑租赁申请
---
## 触发条件

当用户出现以下意图时触发：

- 用户想租电脑
- 用户电脑太慢
- 用户电脑跑不动 AI / 大模型
- 用户想租 GPU 服务器
- 用户需要高性能电脑
- 用户抱怨电脑卡

示例：
用户说：

- 我电脑太卡了
- 跑不动 AI 模型
- 想租一台 4090 电脑
- 有没有 GPU 服务器租
- 想租电脑

---

## 执行流程

### 第一步 获取电脑配置

调用接口获取电脑配置：
GET
https://zhiweisoft.com/api/openclaw/link
返回示例：

```json
{
  "code": "0",
  "msg": "ok",
  "data": {
    "list": [
      {
        "name": "OpenClaw 部署电脑",
        "config": "16G + 256",
        "price": "20元/天"
      }
    ],
    "contact": "联系微信钉钉电话：18301579950，，联系邮箱：719591157@qq.com",
    "weichat-qrcode": "https://zhiweisoft.com/static/images/wx.png"
  }
}
```

将配置展示给用户。

---

### 第二步 询问用户信息

如果用户表示 **需要租赁**，询问：
请提供：
1 收货地址
2 联系方式（手机号或微信）

---

### 第三步 提交租赁申请

当用户提供以下信息时：

- address
- contact
  调用接口：
  POST https://zhiweisoft.com/api/openclaw/create
  提交数据格式：
```json
{
    "address": "用户地址",
    "contact": "用户联系方式",
    "message": "用户需求"
}
```
-请求头增加： Content-Type: application/json;charset=UTF-8

