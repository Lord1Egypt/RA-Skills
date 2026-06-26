export function StatCard({
  value,
  label,
  delta,
  hint,
}: {
  value: string;
  label: string;
  delta?: { value: string; positive: boolean } | null;
  hint?: string;
}) {
  return (
    <div className="group relative overflow-hidden rounded-2xl border border-border bg-panel/60 p-6 backdrop-blur-sm transition hover:bg-panel">
      <div className="text-[11px] font-medium uppercase tracking-[0.18em] text-muted">
        {label}
      </div>
      <div className="mt-2 animate-count_up font-sans text-[44px] font-semibold leading-none tracking-tight text-ink">
        {value}
      </div>
      <div className="mt-3 flex items-center gap-2 text-xs">
        {delta && (
          <span
            className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 font-medium ${
              delta.positive
                ? "bg-success/10 text-success"
                : "bg-danger/10 text-danger"
            }`}
          >
            <span aria-hidden>{delta.positive ? "▲" : "▼"}</span>
            {delta.value}
          </span>
        )}
        {hint && <span className="text-dim">{hint}</span>}
      </div>
      <div
        aria-hidden
        className="pointer-events-none absolute -right-12 -top-12 h-32 w-32 rounded-full bg-accent/10 blur-2xl transition group-hover:bg-accent/20"
      />
    </div>
  );
}
