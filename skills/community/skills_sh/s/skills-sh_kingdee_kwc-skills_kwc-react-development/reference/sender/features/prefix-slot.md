# 前缀插槽

[返回目录](../index.md)

## 功能说明

通过 `prefix` 插槽或 `prefixContent` 属性在输入区域左侧添加操作按钮。常用于放置附件按钮、语音按钮等。

## 示例代码（React）

```jsx
import React, { useRef, useEffect } from 'react';
import { html } from 'lit';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import SlIconButton from '@kdcloudjs/shoelace/dist/react/icon-button/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);

  useEffect(() => {
    const sender = senderRef.current;
    if (sender) {
      sender.prefixContent = html`
        <sl-icon-button name="paperclip" label="附件"></sl-icon-button>
      `;
    }
  }, []);

  return (
    <SlSender
      ref={senderRef}
      placeholder="输入消息..."
      allowSpeech
    />
  );
};
```

---

## 注意事项

1. **prefixContent 属性**：支持 TemplateResult（Lit html 模板）、HTMLElement、函数模式
2. **prefix 插槽**：也可通过 `<SlIconButton slot="prefix">` 在 JSX 中直接放置
3. **与 suffixContent 配合**：前缀和后缀可同时使用，分别控制输入区域两侧的操作按钮

[返回目录](../index.md)
