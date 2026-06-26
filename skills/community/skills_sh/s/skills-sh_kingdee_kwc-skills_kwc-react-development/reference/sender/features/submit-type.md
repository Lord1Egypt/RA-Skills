# 提交模式

[返回目录](../index.md)

## 功能说明

通过 `submitType` 控制换行与提交的快捷键行为。默认 `'enter'` 模式下 Enter 提交、Shift+Enter 换行；`'shift-enter'` 模式下 Enter 换行、Shift+Enter 提交。

## 示例代码（React）

```jsx
import React, { useRef, useCallback } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);

  const handleSubmit = useCallback((e: CustomEvent) => {
    console.log('提交:', e.detail.value);
    const sender = senderRef.current;
    if (sender) {
      sender.loading = true;
      setTimeout(() => {
        sender.value = '';
        sender.loading = false;
      }, 3000);
    }
  }, []);

  return (
    <SlSender
      ref={senderRef}
      placeholder="按 Shift + Enter 发送消息"
      submitType="shift-enter"
      onSlSubmit={handleSubmit as any}
    />
  );
};
```

---

## 注意事项

1. **默认模式**：`submitType="enter"` 时 Enter 直接提交，Shift+Enter 换行
2. **反转模式**：`submitType="shift-enter"` 时 Enter 换行，Shift+Enter 提交
3. **多行输入**：需要多行输入场景建议使用 `shift-enter` 模式

[返回目录](../index.md)
