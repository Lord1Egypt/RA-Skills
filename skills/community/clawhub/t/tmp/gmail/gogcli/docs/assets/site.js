(() => {
  const el = document.getElementById("demo");
  if (!el) return;

  const original = el.textContent || "";
  const prefersReduced = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
  if (prefersReduced) return;

  el.textContent = "";

  const lines = original.split("\n");
  const chunkDelay = 16;
  const lineDelay = 140;
  let i = 0;
  let j = 0;

  const tick = () => {
    if (i >= lines.length) return;
    const line = lines[i];
    if (j <= line.length) {
      el.textContent += line.slice(j, j + 1);
      j += 1;
      window.setTimeout(tick, chunkDelay);
      return;
    }
    el.textContent += "\n";
    i += 1;
    j = 0;
    window.setTimeout(tick, lineDelay);
  };

  window.setTimeout(tick, 260);
})();

