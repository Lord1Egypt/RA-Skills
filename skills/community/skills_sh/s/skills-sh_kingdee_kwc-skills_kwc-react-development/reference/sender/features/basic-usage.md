# 基础用法

[返回目录](../index.md)

## 功能说明

演示 `SlSender` 的最小可用配置：`value`、`placeholder`、`onSlSubmit`，以及 `loading`、`disabled`、`readOnly` 状态。

## 示例代码（React）

```jsx
import React, { useState, useCallback, useRef } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);
  const [value, setValue] = useState('Hello, this is Shoelace!');

  const handleChange = useCallback((e: CustomEvent) => {
    setValue((e.target as SlSenderElement).value);
  }, []);

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

  const handleCancel = useCallback(() => {
    const sender = senderRef.current;
    if (sender) {
      sender.loading = false;
    }
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <SlSender
        ref={senderRef}
        value={value}
        placeholder="请输入消息..."
        onSlChange={handleChange as any}
        onSlSubmit={handleSubmit as any}
        onSlCancel={handleCancel as any}
      />
      <SlSender value="加载中状态" loading readOnly />
      <SlSender value="禁用状态" disabled allowSpeech />
    </div>
  );
};
```

---

## 注意事项

1. **value 受控**：通过 `onSlChange` 监听值变化并更新 state，实现受控模式
2. **loading 状态**：设置 `loading` 后发送按钮变为取消按钮，点击触发 `sl-cancel` 事件
3. **disabled vs readOnly**：`disabled` 完全禁用交互，`readOnly` 仅阻止编辑但保持内容可见
4. **事件类型断言**：事件处理函数需使用 `as any` 类型断言，通过 `e.target as SlSenderElement` 获取组件实例
