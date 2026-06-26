---
name: features-request
description: uni-app 网络请求 uni.request、上传下载、超时与中断
---

# 网络请求

小程序端使用前需在对应平台配置**域名白名单**。

## uni.request(OBJECT)

| 常用参数 | 类型 | 默认 | 说明 |
|----------|------|------|------|
| url | String | 必填 | 接口地址 |
| data | Object/String/ArrayBuffer | - | 请求体，GET 会转 query string，POST 按 header content-type 序列化 |
| header | Object | - | 请求头，不能设 Referer |
| method | String | GET | 需大写，各平台支持范围见文档（如 PUT/DELETE 部分小程序不支持） |
| timeout | Number | 60000 | 超时 ms |
| dataType | String | json | 为 json 时对返回数据做 JSON.parse |
| success / fail / complete | Function | - | 回调 |

- 返回：若不传 success/fail/complete，则返回 **Promise**；若传入则返回 **requestTask**，可调用 `requestTask.abort()` 中断请求。
- 超时时间也可在 manifest 的 `networkTimeout.request` 中统一配置。

## 上传与下载

- `uni.uploadFile`：上传文件，需传 `url`、`filePath`、`name`（文件 key）。
- `uni.downloadFile`：下载文件到本地临时路径。

二者同样支持 success/fail/complete，不传则返回 Promise；可配置 manifest 的 uploadFile/downloadFile 超时。

## 示例

```javascript
// 回调
uni.request({
  url: 'https://example.com/api',
  data: { id: 1 },
  success: (res) => console.log(res.data),
  fail: (err) => console.error(err)
});

// Promise（Vue3）
const res = await uni.request({ url: 'https://example.com/api' });

// 中断
const task = uni.request({ url: '...', complete: () => {} });
task.abort();
```

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/request/request
- https://uniapp.dcloud.net.cn/api/request/network-file
-->
