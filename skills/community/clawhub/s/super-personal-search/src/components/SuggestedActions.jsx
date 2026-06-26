import React from 'react';
import { suggestedActionItems } from '../data/placeholders';

// Action recommendations stacked in the right-side card.
export default function SuggestedActions() {
  return (
    <section className="rounded-2xl border border-zinc-200 bg-white p-5">
      <h2 className="text-lg font-semibold text-zinc-900">Suggested actions</h2>

      <div className="mt-4 space-y-3">
        {suggestedActionItems.map((action) => (
          <article
            key={action.id}
            className="flex items-center justify-between gap-3 rounded-xl border border-zinc-200 bg-zinc-50 px-3.5 py-3"
          >
            <div>
              <h3 className="text-sm font-semibold text-zinc-900">{action.title}</h3>
              <p className="mt-0.5 text-xs text-zinc-500">{action.description}</p>
            </div>

            <button
              type="button"
              className="shrink-0 rounded-lg border border-zinc-300 bg-white px-3 py-1.5 text-xs font-medium text-zinc-700"
            >
              {action.buttonLabel}
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}
