# Dialog 对话框（扩展）

基于 Shoelace Dialog 标准组件，新增了以下扩展属性。

> 标准属性和用法请参考官方文档：https://shoelace.style/components/dialog

## 扩展属性

| 属性 | 描述 | 类型 | 默认值 |
| --- | --- | --- | --- |
| maskClosable | 点击蒙层是否允许关闭 | `boolean` | `true` |

## 使用示例

### 默认行为（点击蒙层可关闭）

```tsx
import React, { useState } from 'react';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import SlDialog from '@kdcloudjs/shoelace/dist/react/dialog/index.js';

export default function DialogDemo() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <SlButton onClick={() => setIsOpen(true)}>打开对话框</SlButton>
      <SlDialog 
        label="默认对话框" 
        open={isOpen} 
        onSlHide={() => setIsOpen(false)}
      >
        点击蒙层可以关闭此对话框
      </SlDialog>
    </>
  );
}
```

### 禁止点击蒙层关闭

```tsx
import React, { useState } from 'react';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import SlDialog from '@kdcloudjs/shoelace/dist/react/dialog/index.js';

export default function DialogDemo() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      <SlButton onClick={() => setIsOpen(true)}>打开对话框</SlButton>
      <SlDialog 
        label="禁止蒙层关闭" 
        open={isOpen} 
        maskClosable={false}
        onSlHide={() => setIsOpen(false)}
      >
        点击蒙层不会关闭此对话框，只能点击关闭按钮
      </SlDialog>
    </>
  );
}
```

## 导入

```tsx
import SlDialog from '@kdcloudjs/shoelace/dist/react/dialog/index.js';
```
