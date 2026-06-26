# 企业微信API接口文档

## 概述

本文档详细说明企业微信相关API接口的使用方法和注意事项。

## 1. 普通回调接口

### 1.1 回调验证
企业微信会发送GET请求进行回调验证：

**请求参数：**
- `msg_signature`: 消息体签名
- `timestamp`: 时间戳
- `nonce`: 随机数
- `echostr`: 加密字符串

**验证流程：**
1. 将token、timestamp、nonce三个参数进行字典序排序
2. 将三个参数字符串拼接成一个字符串进行sha1加密
3. 将加密后的字符串与msg_signature对比，验证成功则返回解密后的echostr

### 1.2 消息接收
企业微信会发送POST请求推送消息：

**消息格式：** XML
**加密方式：** AES-256-CBC

**消息类型：**
- `text`: 文本消息
- `image`: 图片消息
- `voice`: 语音消息
- `video`: 视频消息
- `file`: 文件消息
- `location`: 位置消息
- `event`: 事件消息

### 1.3 事件类型
- `change_contact`: 通讯录变更
- `batch_job_result`: 异步任务完成
- `enter_agent`: 进入应用
- `subscribe`: 关注
- `unsubscribe`: 取消关注

## 2. 会话内容存档接口

### 2.1 数据格式
会话存档数据使用RSA公钥加密，需要私钥解密。

**消息结构：**
```json
{
  "msgid": "消息ID",
  "action": "send/receive/revoke",
  "from": "发送方",
  "tolist": ["接收方列表"],
  "roomid": "群聊ID",
  "msgtime": 时间戳,
  "msgtype": "消息类型",
  "content": "加密内容"
}
```

### 2.2 消息类型
- `text`: 文本消息
- `image`: 图片
- `voice`: 语音
- `video`: 视频
- `file`: 文件
- `emotion`: 表情
- `location`: 位置
- `chatrecord`: 聊天记录
- `mixed`: 混合消息

### 2.3 加解密流程
1. 企业微信使用RSA公钥加密消息内容
2. 服务端使用RSA私钥解密
3. 返回success表示接收成功

## 3. 访问令牌管理

### 3.1 获取Access Token
```
GET https://qyapi.weixin.qq.com/cgi-bin/gettoken
参数: corpid, corpsecret
```

### 3.2 Token有效期
- 有效时间：7200秒（2小时）
- 建议缓存并定时刷新

## 4. 消息发送接口

### 4.1 发送应用消息
```
POST https://qyapi.weixin.qq.com/cgi-bin/message/send
参数: access_token
```

**消息体示例：**
```json
{
  "touser": "UserID",
  "toparty": "PartyID",
  "totag": "TagID",
  "msgtype": "text",
  "agentid": 1000002,
  "text": {
    "content": "消息内容"
  },
  "safe": 0
}
```

## 5. 用户管理接口

### 5.1 获取用户信息
```
GET https://qyapi.weixin.qq.com/cgi-bin/user/get
参数: access_token, userid
```

### 5.2 获取部门成员
```
GET https://qyapi.weixin.qq.com/cgi-bin/user/simplelist
参数: access_token, department_id
```

## 6. 媒体文件接口

### 6.1 上传临时素材
```
POST https://qyapi.weixin.qq.com/cgi-bin/media/upload
参数: access_token, type
```

### 6.2 获取临时素材
```
GET https://qyapi.weixin.qq.com/cgi-bin/media/get
参数: access_token, media_id
```

## 7. 错误码说明

### 7.1 常见错误码
- `-1`: 系统繁忙
- `0`: 请求成功
- `40001`: 获取access_token时Secret错误
- `40014`: 不合法的access_token
- `42001`: access_token已过期
- `40058`: 不合法的回调URL
- `60020`: 会话存档已关闭

### 7.2 错误处理建议
1. 检查access_token是否过期
2. 检查IP白名单配置
3. 检查回调URL配置
4. 检查消息格式是否正确

## 8. 频率限制

### 8.1 API调用限制
- 获取access_token: 2000次/小时
- 发送消息: 600次/分钟
- 上传素材: 1000次/天

### 8.2 回调频率限制
- 普通回调: 2000次/分钟
- 会话存档: 1000次/分钟

## 9. 安全要求

### 9.1 数据加密
- 回调消息必须加密传输
- 会话存档必须使用RSA加密
- 敏感信息需要额外加密

### 9.2 访问控制
- 配置IP白名单
- 使用HTTPS传输
- 定期更换Token和密钥

### 9.3 合规要求
- 存储用户数据需获得授权
- 保留操作日志
- 定期清理过期数据

## 10. 最佳实践

### 10.1 错误重试机制
- 网络错误自动重试3次
- Token过期自动刷新
- 消息去重处理

### 10.2 性能优化
- 缓存access_token
- 批量处理消息
- 异步处理耗时操作

### 10.3 监控告警
- 监控API调用成功率
- 监控消息处理延迟
- 设置异常告警阈值

## 11. 调试工具

### 11.1 在线调试
- 企业微信调试工具
- Postman接口测试
- curl命令行测试

### 11.2 日志记录
- 记录所有API请求
- 记录错误详情
- 记录处理时间

## 12. 更新日志

### 2024-03-05
- 初始版本发布
- 包含普通回调和会话存档接口
- 添加错误码说明
- 添加安全要求说明