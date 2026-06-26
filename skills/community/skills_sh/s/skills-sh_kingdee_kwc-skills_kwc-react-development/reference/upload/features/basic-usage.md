# 基础用法

[返回目录](../index.md)

## 功能说明

最简单的用法，点击按钮选择文件上传。通过 `action` 指定上传地址，监听 `onSlChange` 获取上传状态。

## 示例代码（React）

```jsx
import React from 'react';
import SlUpload from '@kdcloudjs/shoelace/dist/react/upload/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

export default () => (
  <SlUpload
    action="https://httpbin.org/post"
    headers={{ authorization: 'authorization-text' }}
    onSlChange={(e) => {
      const { file, fileList } = e.detail;
      if (file.status === 'done') {
        console.log(`${file.name} file uploaded successfully`);
      } else if (file.status === 'error') {
        console.log(`${file.name} file upload failed.`);
      }
    }}
  >
    <SlButton>
      <SlIcon slot="prefix" name="upload" />
      Click to Upload
    </SlButton>
  </SlUpload>
);
```

---

## 注意事项

1. **action 必须有效**：`action` 为上传目标 URL，若服务端不可用文件状态将变为 `error`
2. **headers 通过 JSX 属性传递**：`headers` 是对象类型，不能作为 HTML 属性传递，必须通过 JSX 属性直接设置
3. **事件映射**：Shoelace 事件 `sl-change` 在 React 中映射为 `onSlChange`，回调参数通过 `e.detail` 获取
4. **文件状态流转**：文件状态依次为 `uploading` → `done`（成功）或 `error`（失败）
