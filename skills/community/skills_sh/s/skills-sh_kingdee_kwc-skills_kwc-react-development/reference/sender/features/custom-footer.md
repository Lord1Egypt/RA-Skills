# 自定义尾部

[返回目录](../index.md)

## 功能说明

通过 `footer` 属性或 `footer` 插槽在输入区域下方添加工具栏。支持 TemplateResult、函数模式（可访问组件渲染器）。常用于放置功能开关、附件按钮、发送按钮等。

## 示例代码（React）

```jsx
import React, { useRef, useCallback, useEffect, useState } from 'react';
import { html } from 'lit';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);
  const [loading, setLoading] = useState(false);

  const updateFooter = useCallback(() => {
    const sender = senderRef.current;
    if (!sender) return;

    // 隐藏默认后缀按钮
    sender.suffixContent = false;

    sender.footer = (defaultFooter, { components }) => {
      return html`
        <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; padding: 0 0.25rem;">
          <div style="display: flex; align-items: center; gap: 0.25rem;">
            <sl-icon-button name="paperclip" label="附件"></sl-icon-button>
            <sl-icon-button name="search" label="搜索"></sl-icon-button>
          </div>
          <div style="display: flex; align-items: center; gap: 0.25rem;">
            ${loading
              ? components.LoadingButton({ title: '点击取消' })
              : components.SendButton({})}
          </div>
        </div>
      `;
    };
  }, [loading]);

  useEffect(() => {
    updateFooter();
  }, [updateFooter]);

  const handleSubmit = useCallback((e: CustomEvent) => {
    console.log('提交:', e.detail.value);
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      const sender = senderRef.current;
      if (sender) sender.value = '';
    }, 2000);
  }, []);

  return (
    <SlSender
      ref={senderRef}
      placeholder="按 Enter 发送消息"
      onSlSubmit={handleSubmit as any}
    />
  );
};
```

---

## 注意事项

1. **footer 函数签名**：`(defaultFooter, { components }) => BaseNode`，与 `suffixContent` 函数签名一致
2. **配合 suffixContent**：使用 footer 工具栏时通常需要设置 `suffixContent = false` 隐藏默认操作按钮
3. **footer 插槽**：也可通过 `<div slot="footer">` 在 HTML 中直接放置尾部内容
4. **Lit html 模板**：函数模式返回值需使用 `html` 模板字面量（从 `lit` 导入）

[返回目录](../index.md)
