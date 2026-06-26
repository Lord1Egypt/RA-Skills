# 功能开关

[返回目录](../index.md)

## 功能说明

`SlSenderSwitch` 是一个切换按钮组件，用于在 Sender 中启用/禁用功能（如深度思考、搜索等）。支持默认内容、选中/未选中内容、禁用、加载、受控模式。

## 示例代码（React）

```jsx
import React, { useState, useCallback } from 'react';
import SlSenderSwitch from '@kdcloudjs/shoelace/dist/react/sender-switch/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const [controlled, setControlled] = useState(false);

  const handleToggle = useCallback(() => {
    setControlled(prev => !prev);
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      {/* 默认用法 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        默认:
        <SlSenderSwitch>
          <SlIcon slot="icon" name="search" />
          深度搜索
        </SlSenderSwitch>
      </div>

      {/* 自定义选中/未选中内容 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        自定义内容:
        <SlSenderSwitch>
          <SlIcon slot="icon" name="search" />
          <span slot="checked">深度搜索: 开</span>
          <span slot="unchecked">深度搜索: 关</span>
        </SlSenderSwitch>
      </div>

      {/* 禁用 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        禁用:
        <SlSenderSwitch disabled>
          <SlIcon slot="icon" name="search" />
          深度搜索
        </SlSenderSwitch>
      </div>

      {/* 加载中 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        加载中:
        <SlSenderSwitch loading>
          <SlIcon slot="icon" name="search" />
          深度搜索
        </SlSenderSwitch>
      </div>

      {/* 受控模式 */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        受控模式:
        <SlSenderSwitch checked={controlled}>
          <SlIcon slot="icon" name="search" />
          深度搜索
        </SlSenderSwitch>
        <SlButton size="small" onClick={handleToggle}>切换</SlButton>
      </div>
    </div>
  );
};
```

---

## 注意事项

1. **导入路径**：`import SlSenderSwitch from '@kdcloudjs/shoelace/dist/react/sender-switch/index.js';`
2. **事件**：`sl-change` → `onSlChange`，读取 `el.checked` 获取新状态
3. **defaultChecked**：仅在首次渲染时生效，后续需通过 `checked` 属性控制
4. **Slots**：`icon`（图标）、`checked`（选中内容）、`unchecked`（未选中内容）、默认 slot（始终显示）

[返回目录](../index.md)
