# 自定义头部

[返回目录](../index.md)

## 功能说明

通过 `header` 属性或 `header` 插槽在输入区域上方添加内容。支持 HTMLElement、TemplateResult、函数模式。配合 `SlSenderHeader` 子组件可实现可折叠的附件面板或引用面板。

## 示例代码（React）— 引用面板

```jsx
import React, { useState, useRef, useCallback, useEffect } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import SlSenderHeader from '@kdcloudjs/shoelace/dist/react/sender-header/index.js';
import SlSwitch from '@kdcloudjs/shoelace/dist/react/switch/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);
  const [hasRef, setHasRef] = useState(true);

  const updateHeader = useCallback((showRef: boolean) => {
    const sender = senderRef.current;
    if (!sender) return;

    if (!showRef) {
      sender.header = false;
      return;
    }

    const header = document.createElement('sl-sender-header');
    header.open = true;
    header.addEventListener('sl-open-change', (e) => {
      const open = (e as CustomEvent).detail.open;
      if (!open) {
        setHasRef(false);
        sender.header = false;
      }
    });

    const titleSlot = document.createElement('div');
    titleSlot.slot = 'title';
    titleSlot.style.cssText = 'display: flex; align-items: center; gap: 0.5rem;';
    titleSlot.innerHTML = '<sl-icon name="reply"></sl-icon><span style="color: var(--sl-color-neutral-500);">"请告诉我更多关于 Shoelace 组件的信息"</span>';
    header.appendChild(titleSlot);

    sender.header = header;
  }, []);

  useEffect(() => {
    updateHeader(hasRef);
  }, [hasRef, updateHeader]);

  const handleSubmit = useCallback((e: CustomEvent) => {
    console.log('提交:', e.detail.value);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      <SlSwitch checked={hasRef} onSlChange={() => setHasRef(!hasRef)}>
        带引用
      </SlSwitch>
      <SlSender
        ref={senderRef}
        placeholder="输入回复..."
        onSlSubmit={handleSubmit as any}
      />
    </div>
  );
};
```

---

## 注意事项

1. **header 属性类型**：支持 HTMLElement（如 `sl-sender-header`）、TemplateResult、函数 `(defaultHeader, { components }) => BaseNode`、`false`（隐藏）
2. **SlSenderHeader**：可折叠面板组件，通过 `open` 控制展开，`closable` 控制关闭按钮，`sl-open-change` 监听状态变化
3. **header 插槽**：也可通过 `<div slot="header">` 在 HTML 中直接放置头部内容
4. **DOM 操作**：在 React 中使用 `header` 属性传入 HTMLElement 时，需通过 `document.createElement` 创建

[返回目录](../index.md)
