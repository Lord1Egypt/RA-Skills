# 流式前端实现参考

## AIAnalysisCard.tsx（完整组件模板）

```typescript
import React, { useState, useEffect, useRef } from 'react';

export interface Step {
  key: string;
  label: string;
  icon: string;
  status: 'pending' | 'active' | 'done' | 'error';
}

export interface Source {
  label: string;
  url?: string;
}

interface AIAnalysisCardProps {
  steps: Step[];
  streamedText: string;
  sources: Source[];
  disclaimer?: string;
  modelName?: string;
}

const STATUS_ICON = {
  pending:  '○',
  active:   '⏳',
  done:     '✅',
  error:    '❌',
};

const STEP_ICONS: Record<string, string> = {
  understand: '🔍',
  retrieve:   '🗄️',
  analyze:    '🩺',
  generate:   '⚡',
};

function parseSources(text: string): { body: string; sources: Source[] } {
  const match = text.match(/📚 参考来源：\n([\s\S]*?)(?=\n⚠️|$)/);
  if (!match) return { body: text, sources: [] };
  return {
    body: text.replace(match[0], '').replace(/⚠️.*$/, '').trim(),
    sources: match[1].split('\n').filter(l => l.trim()).map(line => {
      const urlMatch = line.match(/\(([^)]+)\)/) || line.match(/(https?:\/\/[^\s]+)/);
      return {
        label: line.replace(/\(https?:\/\/[^\s]+\)/, '').trim(),
        url: urlMatch?.[1],
      };
    }),
  };
}

export default function AIAnalysisCard({
  steps: initialSteps,
  streamedText,
  sources: staticSources = [],
  disclaimer,
  modelName = 'MiniMax',
}: AIAnalysisCardProps) {
  const { body, sources: parsedSources } = parseSources(streamedText);
  const allSources = parsedSources.length > 0 ? parsedSources : staticSources;
  const [activeStep, setActiveStep] = useState(0);

  // 超时自动推进步骤
  useEffect(() => {
    if (!streamedText) return;
    const timers: ReturnType<typeof setTimeout>[] = [];
    initialSteps.forEach((_, i) => {
      if (i > activeStep) {
        const delay = Math.min(800 + i * 600, 3000);
        timers.push(setTimeout(() => setActiveStep(i), delay));
      }
    });
    return () => timers.forEach(clearTimeout);
  }, [streamedText, activeStep, initialSteps.length]);

  const steps = initialSteps.map((s, i) => ({
    ...s,
    status: i < activeStep ? 'done' : i === activeStep ? 'active' : 'pending',
  }));

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 bg-gradient-to-r from-primary/5 to-primary/10 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-base">🤖</span>
          <span className="text-sm font-semibold text-primary">AI 智能回答</span>
        </div>
        {streamedText ? (
          <span className="text-xs text-green-600 flex items-center gap-1">
            <span className="w-1.5 h-1.5 bg-green-500 rounded-full" />完成
          </span>
        ) : (
          <span className="text-xs text-blue-500 flex items-center gap-1">
            <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" />实时生成
          </span>
        )}
      </div>

      {/* Steps */}
      <div className="px-4 py-3 space-y-2 border-b border-gray-100">
        {steps.map((step, i) => (
          <div key={step.key} className="flex items-center gap-2">
            <span className={`text-sm ${step.status === 'active' ? 'animate-spin-slow' : ''}`}>
              {step.status === 'done' ? '✅' : step.status === 'active' ? '⏳' : step.status === 'error' ? '❌' : '○'}
            </span>
            <span className={`text-sm ${
              step.status === 'done' ? 'text-green-600 font-medium' :
              step.status === 'active' ? 'text-blue-600 font-medium' :
              step.status === 'error' ? 'text-red-500' :
              'text-gray-400'
            }`}>
              {step.label}
              {step.status === 'active' && <span className="ml-1 animate-pulse">...</span>}
            </span>
          </div>
        ))}
      </div>

      {/* Body */}
      {body && (
        <div className="px-4 py-4 text-sm text-gray-700 leading-relaxed whitespace-pre-line">
          {body}
        </div>
      )}

      {/* Sources */}
      {allSources.length > 0 && (
        <div className="px-4 py-3 bg-green-50 border-t border-green-100">
          <p className="text-xs font-semibold text-green-700 mb-2">📚 参考来源</p>
          <ul className="space-y-1">
            {allSources.map((s, i) => (
              <li key={i} className="text-xs text-green-700 flex items-start gap-1">
                <span className="shrink-0">{i + 1}.</span>
                {s.url ? (
                  <a href={s.url} target="_blank" rel="noopener noreferrer"
                     className="underline hover:text-green-900 break-all">
                    {s.label.replace(/^\d+\.\s*/, '')}
                  </a>
                ) : (
                  <span>{s.label.replace(/^\d+\.\s*/, '')}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Disclaimer */}
      {disclaimer && (
        <div className="px-4 py-2.5 bg-amber-50 border-t border-amber-100">
          <p className="text-xs text-amber-700 leading-relaxed">{disclaimer}</p>
        </div>
      )}

      {/* Footer model tag */}
      <div className="px-4 py-2 bg-gray-50 border-t border-gray-100">
        <p className="text-xs text-gray-400">⭐ {modelName}</p>
      </div>
    </div>
  );
}
```

## 流式fetch封装

```typescript
export async function streamAI(
  apiUrl: string,
  apiKey: string,
  model: string,
  messages: { role: string; content: string }[],
  onToken: (delta: string) => void,
  onDone: () => void,
  onError: (err: string) => void,
) {
  try {
    const res = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${apiKey}` },
      body: JSON.stringify({ model, messages, stream: true, temperature: 0.3, max_tokens: 600 }),
    });

    if (!res.body) throw new Error('No streaming support');
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) { onDone(); break; }
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop() || '';
      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        const data = line.slice(6);
        if (data === '[DONE]') { onDone(); return; }
        try {
          const json = JSON.parse(data);
          const delta = json.choices?.[0]?.delta?.content;
          if (delta) onToken(delta);
        } catch { /* ignore parse errors */ }
      }
    }
  } catch (err) {
    onError(String(err));
  }
}
```

## 步骤自动推进 Hook

```typescript
import { useState, useEffect } from 'react';

export function useStepAdvance(count: number, isLoading: boolean) {
  const [completed, setCompleted] = useState(0);

  useEffect(() => {
    if (!isLoading) return;
    const timers: ReturnType<typeof setTimeout>[] = [];
    for (let i = 1; i < count; i++) {
      timers.push(setTimeout(() => setCompleted(i), 400 + i * 500));
    }
    return () => timers.forEach(clearTimeout);
  }, [isLoading, count]);

  return completed;
}
```
