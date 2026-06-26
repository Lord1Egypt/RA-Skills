import React from 'react';
import { networkMapEdges, networkMapNodes } from '../data/placeholders';

function nodeById(id) {
  return networkMapNodes.find((node) => node.id === id);
}

// Decorative static node graph preview for the network map section.
export default function NetworkMapPreview() {
  return (
    <section className="rounded-2xl border border-zinc-200 bg-white p-5">
      <h2 className="text-lg font-semibold text-zinc-900">Network map (preview)</h2>

      <div className="mt-4 rounded-xl border border-[#ece7dd] bg-[#f6f1e7] p-3">
        <svg viewBox="0 0 460 240" className="h-[240px] w-full">
          {networkMapEdges.map(([sourceId, targetId]) => {
            const source = nodeById(sourceId);
            const target = nodeById(targetId);
            if (!source || !target) {
              return null;
            }

            return (
              <line
                key={`${sourceId}-${targetId}`}
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                stroke="#d5d0c7"
                strokeWidth="1.2"
              />
            );
          })}

          {networkMapNodes.map((node) => (
            <g key={node.id}>
              <circle cx={node.x} cy={node.y} r={node.r} fill={node.color} opacity={node.id === 'you' ? 1 : 0.9} />
              {node.label && (
                <text
                  x={node.x}
                  y={node.y + 26}
                  textAnchor="middle"
                  className="fill-zinc-700"
                  style={{ fontSize: '12px', fontWeight: 500 }}
                >
                  {node.label}
                </text>
              )}
            </g>
          ))}
        </svg>
      </div>
    </section>
  );
}
