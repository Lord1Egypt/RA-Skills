# 自定义后缀

[返回目录](../index.md)

## 功能说明

通过 `suffixContent` 属性自定义操作按钮区域。支持 TemplateResult（Lit html 模板）、函数模式（可访问 `SendButton`、`ClearButton`、`LoadingButton`、`SpeechButton` 组件渲染器），或设为 `false` 隐藏默认操作按钮。

## 示例代码（React）— 函数模式（字符计数器）

```jsx
import React, { useState, useRef, useCallback } from 'react';
import { html } from 'lit';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

const MAX_LENGTH = 100;

export default () => {
  const senderRef = useRef<SlSenderElement>(null);
  const [value, setValue] = useState('');

  const updateSuffix = useCallback((currentValue: string) => {
    const sender = senderRef.current;
    if (!sender) return;
    const len = currentValue.length;
    const overLimit = len > MAX_LENGTH;

    sender.suffixContent = (defaultActions, { components }) => {
      const { SendButton } = components;
      return html`
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span style="font-size: 0.75rem; white-space: nowrap; color: ${overLimit ? 'var(--sl-color-danger-600)' : 'var(--sl-color-neutral-400)'};">
            ${len} / ${MAX_LENGTH}
          </span>
          ${SendButton({ disabled: overLimit || len === 0 })}
        </div>
      `;
    };
  }, []);

  const handleChange = useCallback((e: CustomEvent) => {
    const val = (e.target as SlSenderElement).value;
    setValue(val);
    updateSuffix(val);
  }, [updateSuffix]);

  const handleSubmit = useCallback((e: CustomEvent) => {
    console.log('提交:', e.detail.value);
  }, []);

  // 初始化后缀
  React.useEffect(() => {
    updateSuffix('');
  }, [updateSuffix]);

  return (
    <SlSender
      ref={senderRef}
      value={value}
      placeholder="输入消息（最多 100 字符）..."
      onSlChange={handleChange as any}
      onSlSubmit={handleSubmit as any}
    />
  );
};
```

## 示例代码（React）— 隐藏后缀

```jsx
import React, { useRef, useEffect } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);

  useEffect(() => {
    const sender = senderRef.current;
    if (sender) {
      sender.suffixContent = false;
    }
  }, []);

  return (
    <SlSender
      ref={senderRef}
      value="隐藏所有操作按钮"
      placeholder="无后缀按钮..."
    />
  );
};
```

---

## 注意事项

1. **函数签名**：`(defaultActions, { components }) => BaseNode`，其中 `components` 包含 `SendButton`、`ClearButton`、`LoadingButton`、`SpeechButton`
2. **组件渲染器参数**：每个渲染器接受 `{ disabled?, loading?, label?, title?, onClick? }` 等属性
3. **Lit html 模板**：函数模式返回值需使用 `html` 模板字面量（从 `lit` 导入）
4. **设为 false**：`suffixContent = false` 完全隐藏默认操作按钮区域
5. **动态更新**：值变化时需重新设置 `suffixContent` 以反映最新状态

[返回目录](../index.md)
