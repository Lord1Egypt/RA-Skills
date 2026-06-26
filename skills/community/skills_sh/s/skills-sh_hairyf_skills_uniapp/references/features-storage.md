---
name: features-storage
description: uni-app 本地缓存 setStorage/getStorage/removeStorage
---

# 数据缓存

本地持久化存储，按 key 读写。**注意**：key 不要使用 `uni-`、`uni_`、`dcloud-`、`dcloud_` 前缀（系统保留）。

## 常用 API

| API | 说明 |
|-----|------|
| uni.setStorage / setStorageSync | 存：key + data，会覆盖同 key |
| uni.getStorage / getStorageSync | 取：key，返回 data |
| uni.removeStorage / removeStorageSync | 删指定 key |
| uni.clearStorage / clearStorageSync | 清空全部 |
| uni.getStorageInfo / getStorageInfoSync | 获取 key 列表、当前占用等 |

- 存储内容需为**可 JSON.stringify 的类型**（原生类型或可序列化对象）。
- 异步版接受 OBJECT，可带 success/fail/complete；不传则返回 Promise（规则同 request）。

## 示例

```javascript
// 异步
uni.setStorage({ key: 'user', data: { name: 'hairy' } });
const res = await uni.getStorage({ key: 'user' });

// 同步
uni.setStorageSync('token', 'xxx');
const token = uni.getStorageSync('token');
```

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/storage/storage
-->
