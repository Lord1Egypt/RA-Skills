import React, { useMemo, useState } from 'react';
import { initialChatMessages } from '../data/placeholders';

function platformBadgeClass(platform) {
  if (platform === 'LI') {
    return 'bg-blue-50 text-[#0077b5]';
  }
  return 'bg-pink-50 text-rose-600';
}

function formatResultSummary(results) {
  if (!Array.isArray(results) || results.length === 0) {
    return 'I could not find a strong match right now. Try adding role, city, or company in your query.';
  }

  const topMatches = results.slice(0, 3).map((item) => `${item.name} (${item.company})`).join(', ');
  return `Found ${results.length} relevant contacts. Top matches: ${topMatches}. Want intros or a shortlist?`;
}

// Chat panel with backend call to /api/query and optimistic message flow.
export default function AIChatPanel({ sessionId }) {
  const [messages, setMessages] = useState(initialChatMessages);
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const canSend = useMemo(() => query.trim().length > 0 && !isLoading, [query, isLoading]);

  async function handleSend(event) {
    event.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) {
      return;
    }

    const userMessage = {
      id: `u-${Date.now()}`,
      role: 'user',
      text: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
    setQuery('');
    setError('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: trimmed, sessionId }),
      });

      if (!response.ok) {
        throw new Error('I had trouble reaching the assistant. Please try again in a moment.');
      }

      const data = await response.json();
      const results = Array.isArray(data.results) ? data.results : [];
      const summary = formatResultSummary(results);

      const assistantMessage = {
        id: `a-${Date.now()}`,
        role: 'assistant',
        text: summary,
        results,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (requestError) {
      const friendly = requestError.message || 'Something went wrong while asking the assistant.';
      setError(friendly);
      setMessages((prev) => [
        ...prev,
        {
          id: `e-${Date.now()}`,
          role: 'assistant',
          text: 'Sorry - I hit an error while searching your network. Please try again.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="flex h-full min-h-[460px] flex-col rounded-2xl border border-zinc-200 bg-white p-5">
      <h2 className="text-lg font-semibold text-zinc-900">AI assistant</h2>

      <div className="mt-4 flex-1 space-y-3 overflow-y-auto pr-1">
        {messages.map((message) => (
          <article
            key={message.id}
            className={`max-w-[92%] rounded-2xl px-3.5 py-2.5 text-sm leading-relaxed ${
              message.role === 'user'
                ? 'ml-auto bg-violet-100 text-violet-900'
                : 'border border-zinc-200 bg-zinc-50 text-zinc-800'
            }`}
          >
            <p>{message.text}</p>

            {Array.isArray(message.results) && message.results.length > 0 && (
              <div className="mt-3 space-y-2">
                {message.results.slice(0, 3).map((item) => (
                  <div key={`${message.id}-${item.name}`} className="rounded-xl border border-zinc-200 bg-white p-2.5">
                    <div className="flex items-center justify-between gap-2">
                      <div>
                        <p className="font-medium text-zinc-900">{item.name}</p>
                        <p className="text-xs text-zinc-500">
                          {item.role} · {item.company}
                        </p>
                      </div>
                      <span className="rounded-full bg-zinc-100 px-2 py-0.5 text-xs font-medium text-zinc-700">
                        {item.relevanceScore ?? '--'}
                      </span>
                    </div>

                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {(item.platforms || []).map((platform) => (
                        <span
                          key={`${message.id}-${item.name}-${platform}`}
                          className={`rounded-full px-2 py-0.5 text-xs font-semibold ${platformBadgeClass(platform)}`}
                        >
                          {platform}
                        </span>
                      ))}
                    </div>

                    <div className="mt-2 flex flex-wrap gap-2">
                      {(item.suggestedActions || ['Draft Intro', 'Follow Up']).slice(0, 2).map((action) => (
                        <button
                          key={`${message.id}-${item.name}-${action}`}
                          type="button"
                          className="rounded-full border border-zinc-300 px-2.5 py-1 text-xs font-medium text-zinc-700"
                        >
                          {action}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </article>
        ))}

        {isLoading && (
          <div className="inline-flex items-center gap-2 rounded-2xl border border-zinc-200 bg-zinc-50 px-3 py-2 text-sm text-zinc-500">
            <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-zinc-300 border-t-zinc-600" />
            Thinking...
          </div>
        )}
      </div>

      {error && <p className="mt-3 text-xs text-rose-600">{error}</p>}

      <form onSubmit={handleSend} className="mt-4 flex gap-2">
        <input
          type="text"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Ask about your network..."
          className="h-10 flex-1 rounded-xl border border-zinc-300 bg-white px-3 text-sm outline-none ring-violet-200 transition focus:ring"
        />
        <button
          type="submit"
          disabled={!canSend}
          className="h-10 rounded-xl bg-zinc-900 px-4 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-60"
        >
          Send
        </button>
      </form>
    </section>
  );
}
