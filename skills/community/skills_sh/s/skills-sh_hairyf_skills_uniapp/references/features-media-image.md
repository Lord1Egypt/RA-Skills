---
name: features-media-image
description: uni-app 图片选择与预览 chooseImage、previewImage、getImageInfo、saveImageToPhotosAlbum
---

# 图片 API

## uni.chooseImage(OBJECT)

从相册选图或拍照。常用参数：`count`（最多张数，默认 9）、`sizeType`（['original','compressed']）、`sourceType`（['album','camera']）。success 返回 `tempFilePaths`（临时路径数组）、`tempFiles`（File 对象，含 path、size 等）。临时路径本次启动有效，持久化需调用 `uni.saveFile`。小程序需配置域名与隐私协议；H5 表现依赖浏览器。

## uni.previewImage(OBJECT)

预览图片。参数：`urls`（图片地址数组，必填）、`current`（当前显示 url 或索引）。可配合长按保存等，部分平台支持 indicator、loop、longPressActions。

## uni.getImageInfo(OBJECT)

获取图片宽高、路径等。参数：`src`（图片路径）。success 返回 width、height、path、orientation 等。不传 success/fail/complete 则返回 Promise。

## uni.saveImageToPhotosAlbum(OBJECT)

保存图片到系统相册。参数：`filePath`（图片临时路径）。需用户授权相册；失败时可引导用户打开设置。

## 其它

- **uni.compressImage**：压缩图片，可指定质量。
- 上传建议用 `uni.uploadFile`；如需选图+上传一体化可参考 uni-ui 的 uni-file-picker、uniCloud 存储。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/media/image
-->
