export function LiveDot({ label = "live" }: { label?: string }) {
  return (
    <span className="inline-flex items-center gap-2 text-xs font-medium uppercase tracking-[0.2em] text-success">
      <span className="relative inline-flex h-2 w-2">
        <span className="absolute inset-0 animate-pulse_dot rounded-full bg-success" />
        <span className="absolute inset-0 rounded-full bg-success" />
      </span>
      {label}
    </span>
  );
}
