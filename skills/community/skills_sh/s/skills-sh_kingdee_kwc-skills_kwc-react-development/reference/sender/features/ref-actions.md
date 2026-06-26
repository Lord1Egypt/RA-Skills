# 实例方法

[返回目录](../index.md)

## 功能说明

通过 `useRef` 获取 `SlSender` 实例后，可调用 `focus`、`blur`、`clear`、`insert`、`getValue` 等方法控制输入行为。

## 示例代码（React）

```jsx
import React, { useRef, useCallback } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);

  const handleInsert = useCallback(() => {
    senderRef.current?.insert([{ type: 'text', value: '插入的文本' }], 'cursor');
  }, []);

  const handleInsertEnd = useCallback(() => {
    senderRef.current?.insert([{ type: 'text', value: '末尾文本' }], 'end');
  }, []);

  const handleInsertStart = useCallback(() => {
    senderRef.current?.insert([{ type: 'text', value: '开头文本' }], 'start');
  }, []);

  const handleFocusStart = useCallback(() => {
    senderRef.current?.focus({ cursor: 'start' });
  }, []);

  const handleFocusEnd = useCallback(() => {
    senderRef.current?.focus({ cursor: 'end' });
  }, []);

  const handleFocusAll = useCallback(() => {
    senderRef.current?.focus({ cursor: 'all' });
  }, []);

  const handleBlur = useCallback(() => {
    senderRef.current?.blur();
  }, []);

  return (
    <div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginBottom: '1rem' }}>
        <SlButton size="small" onClick={handleInsert}>插入文本</SlButton>
        <SlButton size="small" onClick={handleInsertEnd}>插入到末尾</SlButton>
        <SlButton size="small" onClick={handleInsertStart}>插入到开头</SlButton>
        <SlButton size="small" onClick={handleFocusStart}>聚焦到开头</SlButton>
        <SlButton size="small" onClick={handleFocusEnd}>聚焦到末尾</SlButton>
        <SlButton size="small" onClick={handleFocusAll}>全选</SlButton>
        <SlButton size="small" onClick={handleBlur}>失焦</SlButton>
      </div>
      <SlSender
        ref={senderRef}
        value="你好，欢迎使用 Shoelace！"
        placeholder="输入消息..."
      />
    </div>
  );
};
```

---

## 注意事项

1. **Ref 类型**：使用 `useRef<SlSenderElement>(null)` 声明，类型从 `@kdcloudjs/shoelace/dist/components/sender/sender.js` 导入
2. **focus 选项**：`cursor` 支持 `'start'`、`'end'`、`'all'`、`'slot'`（聚焦第一个 slot input）
3. **insert 位置**：`'cursor'`（当前光标）、`'start'`（开头）、`'end'`（末尾）
4. **getValue 返回值**：`{ value: string, slotConfig: SlotConfigType[], skill?: SkillType }`
5. **clear 方法**：清空所有输入内容（包括 slot 模式下的结构化内容）

[返回目录](../index.md)
