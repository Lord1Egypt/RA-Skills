---
name: features-file
description: uni-app 文件 saveFile、getSavedFileList、removeSavedFile、openDocument、getFileSystemManager
---

# 文件 API

## 本地文件存储（临时 → 持久）

- **uni.saveFile(OBJECT)**：将临时路径文件保存到本地，success 返回 savedFilePath。调用成功后原 tempFilePath 不可用。H5、快手等部分平台不支持。
- **uni.getSavedFileList(OBJECT)**：获取已保存文件列表，success 返回 fileList（含 filePath、createTime、size 等）。微信已停维该接口，建议用 FileSystemManager。
- **uni.getSavedFileInfo(OBJECT)**：查询某已保存文件信息。
- **uni.removeSavedFile(OBJECT)**：删除已保存文件，需传 filePath。
- **uni.getFileInfo(OBJECT)**：获取文件信息（size 等）。

## 打开文档

- **uni.openDocument(OBJECT)**：打开本地文件，可指定 filePath、fileType 等，用于预览文档。各端支持格式见官方文档。

## 文件系统管理器

- **uni.getFileSystemManager()**：获取文件管理器实例，可进行更底层操作（读目录、读文件、写文件等）。小程序端替代 wx.saveFile 等能力时常用。详见官方「getFileSystemManager」文档。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/file/file
- https://uniapp.dcloud.net.cn/api/file/getFileSystemManager
-->
