# 语音输入

[返回目录](../index.md)

## 功能说明

通过 `allowSpeech` 启用语音输入功能。支持两种模式：布尔模式（使用浏览器内置语音识别）和受控模式（接入第三方语音服务）。

## 示例代码（React）— 内置语音

```jsx
import React, { useState, useRef, useCallback } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);
  const [status, setStatus] = useState('空闲');

  const handleSpeechToggle = useCallback(() => {
    const sender = senderRef.current;
    if (sender) {
      setStatus(sender.speechRecording ? '录音中...' : '空闲');
    }
  }, []);

  const handleSubmit = useCallback((e: CustomEvent) => {
    console.log('提交:', e.detail.value);
    const sender = senderRef.current;
    if (sender) {
      sender.loading = true;
      setTimeout(() => {
        sender.value = '';
        sender.loading = false;
      }, 3000);
    }
  }, []);

  return (
    <div>
      <SlSender
        ref={senderRef}
        placeholder="点击麦克风按钮开始语音输入..."
        allowSpeech
        onSlSpeechToggle={handleSpeechToggle as any}
        onSlSubmit={handleSubmit as any}
      />
      <div style={{ marginTop: '0.5rem', fontSize: '0.875rem' }}>
        状态: {status}
      </div>
    </div>
  );
};
```

## 示例代码（React）— 自定义语音服务

```jsx
import React, { useState, useRef, useCallback } from 'react';
import SlSender from '@kdcloudjs/shoelace/dist/react/sender/index.js';
import type SlSenderElement from '@kdcloudjs/shoelace/dist/components/sender/sender.js';

export default () => {
  const senderRef = useRef<SlSenderElement>(null);
  const [recording, setRecording] = useState(false);

  // 受控语音配置
  const allowSpeech = {
    recording,
    onRecordingChange: (nextRecording: boolean) => {
      setRecording(nextRecording);
      if (nextRecording) {
        // 模拟第三方语音服务
        setTimeout(() => {
          const sender = senderRef.current;
          if (sender) {
            sender.value = sender.value + '来自自定义语音服务的文本 ';
          }
          setRecording(false);
        }, 2000);
      }
    }
  };

  return (
    <div>
      <SlSender
        ref={senderRef}
        placeholder="点击麦克风使用自定义语音..."
        allowSpeech={allowSpeech}
      />
      <div style={{ marginTop: '0.5rem', fontSize: '0.875rem' }}>
        录音: {recording ? '开启' : '关闭'}
      </div>
    </div>
  );
};
```

---

## 注意事项

1. **布尔模式**：`allowSpeech={true}` 或 `allowSpeech` 使用浏览器内置 `SpeechRecognition` API
2. **受控模式**：传入 `{ recording, onRecordingChange }` 对象，禁用内置语音，由外部控制录音状态
3. **浏览器兼容**：内置语音依赖 `webkitSpeechRecognition`，部分浏览器不支持
4. **权限**：首次使用需要用户授权麦克风权限

[返回目录](../index.md)
