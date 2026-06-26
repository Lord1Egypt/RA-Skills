# 插槽填充

[返回目录](../index.md)

## 功能说明

通过 `slotConfig` 将 Sender 切换为结构化输入模式，支持 `text`（纯文本）、`input`（输入框）、`select`（下拉选择）、`tag`（标签）、`content`（可编辑内容块）等类型。配合 `skill` 标识当前技能，使用 `insert`、`clear`、`getValue` 等方法控制输入。

## 示例代码（React）

```jsx
import React, { useRef, useCallback } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

const slotConfig = [
  { type: 'text', value: '我想去 ' },
  { type: 'content', key: 'location', props: { defaultValue: '北京', placeholder: '[输入地点]' } },
  { type: 'text', value: ' 乘坐 ' },
  {
    type: 'select',
    key: 'transport',
    props: {
      defaultValue: 'airplane',
      options: [
        { label: '飞机', value: 'airplane' },
        { label: '高铁', value: 'high-speed-rail' },
        { label: '邮轮', value: 'cruise-ship' }
      ],
      placeholder: '选择交通方式'
    }
  },
  { type: 'text', value: '。请 ' },
  { type: 'tag', key: 'tool', props: { label: '@旅行规划师', value: 'travelTool' } },
  { type: 'text', value: ' 帮我规划，使用账号 ' },
  { type: 'input', key: 'account', props: { placeholder: '输入账号' } },
  { type: 'text', value: '。' }
];

const skill = { value: 'travelId', title: '旅行规划', closable: true };

export default () => {
  const senderRef = useRef<SlSenderElement>(null);

  const handleClear = useCallback(() => {
    senderRef.current?.clear();
  }, []);

  const handleGetValue = useCallback(() => {
    const val = senderRef.current?.getValue();
    console.log('当前值:', val);
  }, []);

  const handleInsert = useCallback(() => {
    senderRef.current?.insert([
      { type: 'text', value: ' 附加文本' },
      { type: 'content', key: 'extra_' + Date.now(), props: { defaultValue: '默认值' } }
    ]);
  }, []);

  const handleSubmit = useCallback((e: CustomEvent) => {
    console.log('提交:', e.detail.value, e.detail.slotConfig);
    senderRef.current?.clear();
  }, []);

  return (
    <div>
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        <SlButton size="small" onClick={handleClear}>清空</SlButton>
        <SlButton size="small" onClick={handleGetValue}>获取值</SlButton>
        <SlButton size="small" onClick={handleInsert}>插入内容</SlButton>
      </div>
      <SlSender
        ref={senderRef}
        placeholder="按 Enter 发送"
        slotConfig={JSON.parse(JSON.stringify(slotConfig))}
        skill={skill}
        onSlSubmit={handleSubmit as any}
      />
    </div>
  );
};
```

---

## 注意事项

1. **slotConfig 深拷贝**：传入 `slotConfig` 时建议使用 `JSON.parse(JSON.stringify(...))` 深拷贝，避免引用共享导致状态异常
2. **key 唯一性**：每个非 `text` 类型的 slot 项必须有唯一的 `key`
3. **insert 方法**：支持 `'start'`、`'end'`、`'cursor'` 三种插入位置，默认为 `'cursor'`
4. **getValue 返回值**：返回 `{ value: string, slotConfig: SlotConfigType[], skill?: SkillType }`，其中 `value` 为拼接后的纯文本
5. **动态切换**：可随时更新 `slotConfig` 和 `skill` 属性切换不同的结构化模板

[返回目录](../index.md)
