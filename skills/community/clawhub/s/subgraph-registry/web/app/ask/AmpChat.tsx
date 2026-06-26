"use client";

import { useEffect, useRef, useState } from "react";

interface TraceStep {
  sql?: string;
  rows?: number;
  error?: string;
}
interface Msg {
  role: "user" | "assistant" | "error";
  text: string;
  trace?: TraceStep[];
}

export function AmpChat({ suggestions }: { suggestions: string[] }) {
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [history, setHistory] = useState<Msg[]>([]);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history, busy]);

  async function ask(question: string) {
    if (!question.trim() || busy) return;
    setHistory((h) => [...h, { role: "user", text: question }]);
    setInput("");
    setBusy(true);
    try {
      const res = await fetch("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      if (!res.ok) {
        setHistory((h) => [...h, { role: "error", text: data.error || `HTTP ${res.status}` }]);
      } else {
        setHistory((h) => [
          ...h,
          { role: "assistant", text: data.answer, trace: data.trace },
        ]);
      }
    } catch (e) {
      setHistory((h) => [...h, { role: "error", text: String(e instanceof Error ? e.message : e) }]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Conversation */}
      <div className="min-h-[200px] space-y-3">
        {history.length === 0 && (
          <div className="rounded-lg border border-border bg-panelHover/40 px-4 py-6 text-center text-sm text-dim">
            Click a suggested question below, or type your own.
          </div>
        )}
        {history.map((m, i) => (
          <MessageBubble key={i} msg={m} />
        ))}
        {busy && <ThinkingIndicator />}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form
        className="flex gap-2"
        onSubmit={(e) => {
          e.preventDefault();
          ask(input);
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about x402 payments to The Graph…"
          className="flex-1 rounded-xl border border-border bg-panelHover/60 px-4 py-2.5 text-sm text-ink placeholder:text-dim focus:border-accent focus:outline-none"
          disabled={busy}
          autoFocus
        />
        <button
          type="submit"
          disabled={busy || !input.trim()}
          className="rounded-xl bg-accent px-4 py-2.5 text-sm font-medium text-white transition hover:bg-accentHover disabled:cursor-not-allowed disabled:opacity-50"
        >
          Ask
        </button>
      </form>

      {/* Suggested questions */}
      <div className="flex flex-wrap gap-2">
        {suggestions.map((s) => (
          <button
            key={s}
            type="button"
            disabled={busy}
            onClick={() => ask(s)}
            className="rounded-full border border-border bg-panelHover/40 px-3 py-1.5 text-left text-xs text-muted transition hover:border-accent/60 hover:bg-panelHover hover:text-ink disabled:cursor-not-allowed disabled:opacity-50"
          >
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}

function ThinkingIndicator() {
  // The full round-trip is typically 8-14s. Show staged messages so the wait
  // feels like progress rather than dead air. These thresholds match the
  // observed wall-clock split (LLM-write ~5s, SQL ~5s, LLM-summarize ~2s).
  const phases = [
    { at: 0, label: "Writing SQL" },
    { at: 5, label: "Running on DuckDB" },
    { at: 9, label: "Summarizing" },
  ];
  const [secs, setSecs] = useState(0);
  useEffect(() => {
    const start = Date.now();
    const id = setInterval(() => setSecs(Math.floor((Date.now() - start) / 1000)), 250);
    return () => clearInterval(id);
  }, []);
  const phase = [...phases].reverse().find((p) => secs >= p.at)!;
  return (
    <div className="flex items-center gap-2 text-sm text-dim">
      <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-accent" />
      <span>{phase.label}…</span>
      <span className="text-[11px] text-dim/60">{secs}s</span>
    </div>
  );
}

function MessageBubble({ msg }: { msg: Msg }) {
  if (msg.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-2xl rounded-br-md bg-accent/15 px-4 py-2.5 text-sm text-ink">
          {msg.text}
        </div>
      </div>
    );
  }
  if (msg.role === "error") {
    return (
      <div className="rounded-lg border border-danger/50 bg-danger/10 px-4 py-2.5 text-sm text-danger">
        {msg.text}
      </div>
    );
  }
  return (
    <div className="rounded-2xl rounded-bl-md bg-panelHover/60 px-4 py-3 text-sm leading-relaxed text-ink">
      <div className="whitespace-pre-wrap">{msg.text}</div>
      {msg.trace && msg.trace.length > 0 && (
        <details className="mt-3 group">
          <summary className="cursor-pointer text-[11px] uppercase tracking-wider text-dim hover:text-muted">
            SQL ({msg.trace.length} step{msg.trace.length > 1 ? "s" : ""})
          </summary>
          <div className="mt-2 space-y-2">
            {msg.trace.map((t, i) => (
              <div key={i} className="rounded-md border border-border bg-bg/50 p-2">
                <pre className="overflow-x-auto whitespace-pre-wrap font-mono text-[11px] text-muted">
                  {t.sql}
                </pre>
                <div className="mt-1 text-[10px] text-dim">
                  {t.error ? (
                    <span className="text-danger">error: {t.error}</span>
                  ) : (
                    <span>{t.rows} row{t.rows === 1 ? "" : "s"}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}
