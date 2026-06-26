# 辅助管理接口

> 本文件是 ziniao-webdriver-doc 的 Level 2 参考文档。
> 仅在需要查阅 stopBrowser / logout / exit / 缓存清理 / 插件查询 / updateCore 等辅助接口时加载。

## 4. stopBrowser — 关闭店铺窗口

**请求：**
```json
{
  "company": "公司",
  "username": "用户名",
  "password": "密码",
  "action": "stopBrowser",
  "browserOauth": "店铺ID",
  "browserId": "店铺数字ID（优先取此值）",
  "requestId": "全局唯一标识",
  "duplicate": 0
}
```

**响应：**
```json
{
  "statusCode": "状态码",
  "err": "异常信息",
  "action": "stopBrowser",
  "requestId": "全局唯一标识"
}
```

**状态码：** 0=成功，-10000=未知异常，-10002=参数非法，-10003=登录失败，-10013=需设备认证

---

## 5. logout — 退出登录

**请求：**
```json
{
  "action": "logout",
  "requestId": "全局唯一标识"
}
```

---

## 6. exit — 退出客户端进程

正常退出紫鸟浏览器主进程，会自动关闭已启动店铺并保持 Cookie 等信息。

**请求：**
```json
{
  "action": "exit",
  "requestId": "全局唯一标识"
}
```

**响应：**
```json
{
  "statusCode": "状态码",
  "err": "异常信息",
  "action": "exit",
  "requestId": "全局唯一标识"
}
```

**状态码：** 0=成功，-10005=登出失败

---

## 7. ClearCache — 清理本地缓存

不需要登录即可调用。

**请求：**
```json
{
  "action": "ClearCache",
  "browserOauths": ["店铺id1", "店铺id2"],
  "requestId": "全局唯一标识"
}
```

`browserOauths` 为空则删除所有本地缓存。

**响应：**
```json
{
  "statusCode": "状态码",
  "err": "异常信息",
  "action": "ClearCache",
  "requestId": "全局唯一标识"
}
```

**状态码：** 0=成功，-10000=未知异常

---

## 8. ClearOnline — 清理在线缓存

**请求：**
```json
{
  "company": "公司",
  "username": "用户名",
  "password": "密码",
  "action": "ClearOnline",
  "browserOauth": "店铺ID",
  "type": 2,
  "requestId": "全局唯一标识"
}
```

`type` 取值：1=清除所有缓存，2=仅保留cookie，3=仅保留二步认证cookie

**响应：**
```json
{
  "statusCode": "状态码",
  "statusMsg": "具体描述",
  "err": "异常信息",
  "action": "ClearOnline",
  "requestId": "全局唯一标识"
}
```

**状态码：** 0=成功，-10000=没有找到记录

---

## 9. getPluginInstalled — 查询插件安装状态

**请求：**
```json
{
  "action": "getPluginInstalled",
  "requestId": "全局唯一标识",
  "browserId": "店铺ID",
  "duplicate": 0,
  "pluginIds": "插件id,插件id"
}
```

**响应：**
```json
{
  "statusCode": "状态码",
  "statusMsg": "",
  "err": "异常信息",
  "action": "getPluginInstalled",
  "requestId": "全局唯一标识",
  "install_status": true
}
```

`install_status`：true=已通知安装，false=未通知

**状态码：** 0=成功，-10000=没有找到记录

---

## 10. getRunningInfo — 获取当前已开启的店铺

**请求：**
```json
{
  "action": "getRunningInfo",
  "requestId": "全局唯一标识"
}
```

**响应：**
```json
{
  "statusCode": "状态码",
  "browsers": [],
  "requestId": "全局唯一标识"
}
```

**状态码：** 0=成功

---

## 11. updateCore — 更新内核

> **⚠ 此接口必须携带 company/username/password 凭据。** 遗漏凭据会导致请求失败——这是最常见的对接错误之一，因为 updateCore 看似只是"内核检测"，容易被误认为不需要登录态。

因 HTTP 有超时限制，此接口适合循环调用直到返回成功。

**请求：**
```json
{
  "company": "公司",
  "username": "用户名",
  "password": "密码",
  "action": "updateCore",
  "requestId": "全局唯一标识"
}
```

**响应：**
```json
{
  "statusCode": "状态码",
  "err": "异常信息",
  "requestId": "全局唯一标识"
}
```

**状态码：** 0=成功，-10000=处理中

**调用机制：**
1. 客户端启动后调用 updateCore，若连接失败说明客户端还未启动成功，轮询（每2秒）直到连接成功
2. statusCode==0 → 内核就绪，继续后续操作
3. statusCode!=0 → 内核缺失/下载中，继续轮询并展示 `msg` 中的下载进度
4. 建议设置总超时 300 秒，避免无限等待

**错误排查：**
- 返回错误时**优先读取 `err` 字段**获取中文错误描述，而非仅看 statusCode 数字
- 若 `err` 内容出现乱码，说明 HTTP 响应体未正确按 UTF-8 解码——务必确保客户端以 UTF-8 解码响应
- 常见失败原因：未携带凭据、凭据错误、客户端尚未完全启动
