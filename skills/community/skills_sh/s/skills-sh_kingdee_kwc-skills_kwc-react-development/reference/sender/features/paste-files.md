# 粘贴文件

[返回目录](../index.md)

## 功能说明

监听 `sl-paste-file` 事件捕获用户粘贴的文件（如剪贴板中的图片）。`sl-paste` 事件在所有粘贴操作（包括文本）时触发。

## 示例代码（React）

```jsx
import React, { useState, useRef, useCallback } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import SlTag from '@kdcloudjs/shoelace/dist/react/tag/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);
  const [files, setFiles] = useState<File[]>([]);
  const [log, setLog] = useState('');

  const handlePasteFile = useCallback((e: CustomEvent) => {
    const pastedFiles = Array.from(e.detail.files as FileList);
    setFiles(prev => [...prev, ...pastedFiles]);
    setLog(`粘贴了 ${pastedFiles.length} 个文件: ${pastedFiles.map(f => f.name).join(', ')}`);
  }, []);

  const handleRemoveFile = useCallback((index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  }, []);

  const handleSubmit = useCallback((e: CustomEvent) => {
    console.log('提交:', e.detail.value, '文件:', files.map(f => f.name));
    setFiles([]);
    const sender = senderRef.current;
    if (sender) sender.value = '';
  }, [files]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
      <SlSender
        ref={senderRef}
        placeholder="尝试粘贴图片或文件 (Ctrl+V / Cmd+V)..."
        onSlPasteFile={handlePasteFile as any}
        onSlSubmit={handleSubmit as any}
      />
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
        {files.map((file, index) => (
          <SlTag
            key={index}
            size="small"
            removable
            onSlRemove={() => handleRemoveFile(index)}
          >
            {file.name} ({(file.size / 1024).toFixed(1)} KB)
          </SlTag>
        ))}
      </div>
      {log && <div style={{ fontSize: '0.8rem', color: 'var(--sl-color-neutral-500)' }}>{log}</div>}
    </div>
  );
};
```

---

## 注意事项

1. **sl-paste-file**：仅在粘贴内容包含文件时触发，`detail.files` 为 `FileList`
2. **sl-paste**：所有粘贴操作都会触发，`detail.event` 为原始 `ClipboardEvent`
3. **文件类型**：支持图片、文档等任意文件类型，需自行处理文件上传逻辑

[返回目录](../index.md)
