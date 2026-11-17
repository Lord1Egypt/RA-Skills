// components/chat.tsx
'use client';

import { useChat } from '@ai-sdk/react';
import { useState } from 'react';

/** A minimal chat: useChat posts to /api/chat and streams the reply in. */
export function Chat() {
  const { messages, sendMessage, status } = useChat();
  const [input, setInput] = useState('');

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        if (!input.trim()) return;
        void sendMessage({ text: input });
        setInput('');
      }}
    >
      {messages.map((message) => (
        <p key={message.id}>
          <strong>{message.role === 'user' ? 'You' : 'Model'}:</strong>{' '}
          {message.parts.map((part) => (part.type === 'text' ? part.text : '')).join('')}
        </p>
      ))}
      <input value={input} onChange={(event) => setInput(event.target.value)} disabled={status !== 'ready'} />
    </form>
  );
}
