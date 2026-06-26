---
name: features-upload-download
description: uni-app 上传与下载 uploadFile、downloadFile、formData、多文件
---

# 上传与下载

小程序端使用前需配置**域名白名单**。超时可在 manifest 的 networkTimeout 中配置 uploadFile、downloadFile。

## uni.uploadFile(OBJECT)

将本地文件上传到服务器。POST，content-type 为 multipart/form-data。

- **url**（必填）：服务器地址。
- **filePath**（与 files 二选一）：本地文件路径，如 chooseImage 返回的 tempFilePaths[0]。
- **name**（必填）：文件对应的 key，服务端通过该 key 取二进制。
- **formData**：额外表单字段。
- **header**：请求头，不能设 Referer。
- **timeout**：超时 ms。

**多文件**：App 支持 **files** 数组（每项含 name、uri），一次上传多文件；微信等仅支持单文件，需循环调用 uploadFile。success 返回 data、statusCode。

## uni.downloadFile(OBJECT)

下载文件到本地临时路径。

- **url**（必填）：文件地址。
- **header**：请求头。

success 返回 **tempFilePath**。临时路径本次启动有效，持久化需调用 uni.saveFile。不传 success/fail/complete 则返回 Promise。

## 示例

```javascript
// 上传
uni.uploadFile({
  url: 'https://example.com/upload',
  filePath: tempFilePath,
  name: 'file',
  formData: { user: 'test' },
  success: (res) => console.log(res.data)
});

// 下载
const res = await uni.downloadFile({ url: 'https://example.com/file.pdf' });
```

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/request/network-file
-->
