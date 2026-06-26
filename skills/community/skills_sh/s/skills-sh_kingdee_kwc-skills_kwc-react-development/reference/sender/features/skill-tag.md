# 技能标签

[返回目录](../index.md)

## 功能说明

通过 `skill` 属性为 Sender 添加技能标签，标识当前使用的 AI 技能或代理。支持显示标题、可关闭、关闭回调等配置。

## 示例代码（React）

```jsx
import React, { useState, useRef, useCallback } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

const skills = {
  search: { value: 'deepSearch', title: '深度搜索', closable: true },
  code: { value: 'aiCode', title: '代码助手', closable: true },
  writing: {
    value: 'writing',
    title: '写作助手',
    closable: {
      onClose: () => console.log('写作助手已关闭'),
      disabled: false
    }
  }
};

export default () => {
  const senderRef = useRef<SlSenderElement>(null);
  const [currentSkill, setCurrentSkill] = useState('search');

  const handleSwitch = useCallback((key: string) => {
    setCurrentSkill(key);
    const sender = senderRef.current;
    if (sender) {
      sender.skill = { ...skills[key] };
    }
  }, []);

  return (
    <div>
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
        {Object.entries(skills).map(([key, s]) => (
          <SlButton
            key={key}
            size="small"
            variant={currentSkill === key ? 'primary' : 'default'}
            onClick={() => handleSwitch(key)}
          >
            {s.title}
          </SlButton>
        ))}
      </div>
      <SlSender
        ref={senderRef}
        placeholder="输入消息..."
        skill={skills[currentSkill]}
      />
    </div>
  );
};
```

---

## 注意事项

1. **skill 对象**：`value` 为必填字段，用于标识技能；`title` 为显示文本
2. **closable 配置**：布尔值 `true` 显示关闭按钮；对象模式支持 `onClose` 回调和 `disabled` 禁用关闭
3. **动态切换**：直接更新 `skill` 属性即可切换技能标签
4. **与 slotConfig 配合**：通常 `skill` 和 `slotConfig` 一起使用，切换技能时同步更新结构化模板

[返回目录](../index.md)
