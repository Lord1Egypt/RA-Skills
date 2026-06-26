# 事件监听

[返回目录](../index.md)

## 功能说明

`SlSender` 支持多种事件：`sl-change`（值变化）、`sl-submit`（提交）、`sl-clear`（清空）、`sl-focus`（聚焦）、`sl-blur`（失焦）、`sl-speech-toggle`（语音切换）、`sl-paste`（粘贴）、`sl-paste-file`（粘贴文件）。

## 示例代码（React）

```jsx
import React, { useRef, useCallback } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);

  const handleChange = useCallback((e: CustomEvent) => {
    console.log('sl-change', { value: e.detail.value });
  }, []);

  const handleSubmit = useCallback((e: CustomEvent) => {
    console.log('sl-submit', { value: e.detail.value });
    const sender = senderRef.current;
    if (sender) {
      sender.loading = true;
      setTimeout(() => {
        sender.loading = false;
      }, 2000);
    }
  }, []);

  const handleClear = useCallback(() => {
    console.log('sl-clear');
  }, []);

  const handleFocus = useCallback(() => {
    console.log('sl-focus');
  }, []);

  const handleBlur = useCallback(() => {
    console.log('sl-blur');
  }, []);

  const handlePaste = useCallback(() => {
    console.log('sl-paste');
  }, []);

  const handlePasteFile = useCallback((e: CustomEvent) => {
    console.log('sl-paste-file', { count: e.detail.files.length });
  }, []);

  const handleSpeechToggle = useCallback(() => {
    console.log('sl-speech-toggle');
  }, []);

  return (
    <SlSender
      ref={senderRef}
      placeholder="尝试输入、提交、清空..."
      allowSpeech
      onSlChange={handleChange as any}
      onSlSubmit={handleSubmit as any}
      onSlClear={handleClear as any}
      onSlFocus={handleFocus as any}
      onSlBlur={handleBlur as any}
      onSlPaste={handlePaste as any}
      onSlPasteFile={handlePasteFile as any}
      onSlSpeechToggle={handleSpeechToggle as any}
    />
  );
};
```

---

## 注意事项

1. **事件映射**：所有 `sl-*` 事件在 React 中映射为 `onSl*`（PascalCase），如 `sl-paste-file` → `onSlPasteFile`
2. **类型断言**：事件处理函数需使用 `as any` 类型断言
3. **sl-change detail**：普通模式返回 `{ value }`，slot 模式返回 `{ value, slotConfig, skill? }`
4. **sl-submit detail**：与 `sl-change` 结构一致，包含提交时的完整值

[返回目录](../index.md)
