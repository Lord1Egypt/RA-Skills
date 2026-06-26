export function Panel({
  title,
  caption,
  children,
  className = "",
}: {
  title?: string;
  caption?: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <section
      className={`rounded-2xl border border-border bg-panel/60 p-5 backdrop-blur-sm transition hover:bg-panel ${className}`}
    >
      {(title || caption) && (
        <header className="mb-4 flex items-baseline justify-between">
          {title && (
            <h2 className="text-sm font-medium uppercase tracking-[0.16em] text-muted">
              {title}
            </h2>
          )}
          {caption && <span className="text-xs text-dim">{caption}</span>}
        </header>
      )}
      {children}
    </section>
  );
}
