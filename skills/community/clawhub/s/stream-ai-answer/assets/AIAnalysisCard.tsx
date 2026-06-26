// AIAnalysisCard.tsx — 流式AI分析卡片组件模板
// 复制到目标项目的 components/common/ 目录，按需调整
// 依赖：React 18 + TypeScript + TailwindCSS

import React, { useState, useEffect } from 'react';

// ── Types ──────────────────────────────────────────────────────────

export interface Step {
  key: string;
  label: string;
  status: 'pending' | 'active' | 'done' | 'error';
}

export interface Source {
  label: string;
  url?: string;
}

interface AIAnalysisCardProps {
  /** 初始化的步骤列表 */
  steps: Step[];
  /** 实时流式生成的文本（实时追加） */
  streamedText: string;
  /** 外部传入的静态来源（streamedText解析前使用） */
  sources?: Source[];
  /** 免责声明文本 */
  disclaimer?: string;
  /** 模型名称标签 */
  modelName?: string;
  /** 是否已完成流式生成 */
  isDone?: boolean;
}

// ── 来源解析 ───────────────────────────────────────────────────────

function parseSources(text: string): { body: string; sources: Source[] } {
  const pattern = /📚 参考来源：\n([\s\S]*?)(?=\n⚠️|$)/;
  const match = text.match(pattern);
  if (!match) return { body: text, sources: [] };
  return {
    body: text.replace(match[0], '').replace(/⚠️[\s\S]*$/, '').trim(),
    sources: match[1].split('\n').filter(l => l.trim()).map(line => {
      const urlMatch = line.match(/(https?:\/\/[^\s）]+)/);
      return {
        label: line.replace(/https?:\/\/[^\s）]+/, '').trim(),
        url: urlMatch?.[1],
      };
    }),
  };
}

// ── 步骤状态图标 ──────────────────────────────────────────────────

const STATUS_ICON = {
  pending: '○',
  active:  '⏳',
  done:    '✅',
  error:   '❌',
};

// ── 组件 ───────────────────────────────────────────────────────────

export default function AIAnalysisCard({
  steps: initialSteps,
  streamedText,
  sources: staticSources = [],
  disclaimer = '⚠️ 本回答仅供科普参考，不作为诊断依据，请以医生诊断为准。如有不适请及时就医。',
  modelName = 'MiniMax',
  isDone = false,
}: AIAnalysisCardProps) {
  const { body, sources: parsedSources } = parseSources(streamedText);
  const allSources = parsedSources.length > 0 ? parsedSources : staticSources;
  const [completedSteps, setCompletedSteps] = useState(0);

  // 流式进行时：超时自动推进步骤
  useEffect(() => {
    if (isDone || !streamedText) return;
    const timers: ReturnType<typeof setTimeout>[] = [];
    initialSteps.forEach((_, i) => {
      if (i > completedSteps) {
        timers.push(setTimeout(() => setCompletedSteps(i), 400 + i * 600));
      }
    });
    return () => timers.forEach(clearTimeout);
  }, [streamedText, isDone, completedSteps, initialSteps]);

  const finalSteps = initialSteps.map((s, i) => ({
    ...s,
    status: i < completedSteps ? 'done' : i === completedSteps ? 'active' : 'pending',
  }));

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 bg-gradient-to-r from-primary/5 to-primary/10 border-b border-gray-100 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-base">🤖</span>
          <span className="text-sm font-semibold text-primary">AI 智能回答</span>
        </div>
        {isDone ? (
          <span className="text-xs text-green-600 flex items-center gap-1">
            <span className="w-1.5 h-1.5 bg-green-500 rounded-full" />
            完成
          </span>
        ) : (
          <span className="text-xs text-blue-500 flex items-center gap-1">
            <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-pulse" />
            实时生成
          </span>
        )}
      </div>

      {/* Steps 流水线 */}
      <div className="px-4 py-3 space-y-2 border-b border-gray-100">
        {finalSteps.map((step, i) => (
          <div key={step.key} className="flex items-center gap-2">
            <span className="text-sm w-5 text-center">
              {STATUS_ICON[step.status]}
            </span>
            <span
              className={`text-sm ${
                step.status === 'done'   ? 'text-green-600 font-medium' :
                step.status === 'active' ? 'text-blue-600 font-medium' :
                step.status === 'error'  ? 'text-red-500' :
                'text-gray-400'
              }`}
            >
              {step.label}
              {step.status === 'active' && (
                <span className="ml-1 inline-block w-1.5 h-3 bg-blue-400 rounded animate-pulse" />
              )}
            </span>
          </div>
        ))}
      </div>

      {/* Body：流式文本 */}
      {body && (
        <div className="px-4 py-4 text-sm text-gray-700 leading-relaxed whitespace-pre-line">
          {body}
        </div>
      )}

      {/* 来源区块 */}
      {allSources.length > 0 && (
        <div className="px-4 py-3 bg-green-50 border-t border-green-100">
          <p className="text-xs font-semibold text-green-700 mb-2">📚 参考来源</p>
          <ul className="space-y-1">
            {allSources.map((s, i) => (
              <li key={i} className="text-xs text-green-700 flex items-start gap-1">
                <span className="shrink-0">{i + 1}.</span>
                {s.url ? (
                  <a
                    href={s.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline hover:text-green-900 break-all"
                  >
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

      {/* 免责声明 */}
      <div className="px-4 py-2.5 bg-amber-50 border-t border-amber-100">
        <p className="text-xs text-amber-700 leading-relaxed">{disclaimer}</p>
      </div>

      {/* Footer：模型标签 */}
      <div className="px-4 py-2 bg-gray-50 border-t border-gray-100">
        <p className="text-xs text-gray-400">⭐ {modelName}</p>
      </div>
    </div>
  );
}
