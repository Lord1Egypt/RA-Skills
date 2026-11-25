"use client";
// Settings > Appearance. Shown only when the app has more than one pack.
// Picking a pack keeps the Light / Dark / Auto choice; every pack has both.
import { useEffect, useState } from "react";
import { applyPack, DEFAULT_PACK, getPack, MODE_KEY, PACK_KEY, PACKS, type ModeChoice } from "@/lib/theme-packs";

const MODES: { value: ModeChoice; label: string }[] = [
  { value: "light", label: "Light" },
  { value: "dark", label: "Dark" },
  { value: "system", label: "Auto" },
];

function read(): { pack: string; mode: ModeChoice } {
  try {
    const m = localStorage.getItem(MODE_KEY);
    return {
      pack: getPack(localStorage.getItem(PACK_KEY)).id,
      mode: m === "light" || m === "dark" || m === "system" ? m : "system",
    };
  } catch {
    return { pack: DEFAULT_PACK, mode: "system" };
  }
}

export default function ThemePackPicker() {
  const [state, setState] = useState<{ pack: string; mode: ModeChoice } | null>(null);
  useEffect(() => setState(read()), []);
  useEffect(() => {
    if (state?.mode !== "system") return;
    const mq = matchMedia("(prefers-color-scheme: dark)");
    const on = () => applyPack(state.pack, "system");
    mq.addEventListener("change", on);
    return () => mq.removeEventListener("change", on);
  }, [state]);

  function choose(next: { pack: string; mode: ModeChoice }) {
    try {
      localStorage.setItem(PACK_KEY, next.pack);
      localStorage.setItem(MODE_KEY, next.mode);
    } catch {
      // Not saved; still changes for this visit.
    }
    applyPack(next.pack, next.mode);
    window.dispatchEvent(new Event("themechange"));
    setState(next);
  }

  const cur = state ?? { pack: DEFAULT_PACK, mode: "system" as ModeChoice };
  return (
    <section aria-labelledby="appearance-h">
      <h2 id="appearance-h">Appearance</h2>
      {PACKS.length > 1 && (
        <div role="radiogroup" aria-label="Look" className="pack-grid">
          {PACKS.map((p) => (
            <button key={p.id} type="button" role="radio" aria-checked={cur.pack === p.id}
              onClick={() => choose({ ...cur, pack: p.id })} className="pack-card">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={p.preview} alt="" width={160} height={100} loading="lazy" />
              <span>{p.label}</span>
            </button>
          ))}
        </div>
      )}
      <div role="radiogroup" aria-label="Light or dark" className="mode-row">
        {MODES.map((m) => (
          <button key={m.value} type="button" role="radio" aria-checked={cur.mode === m.value}
            onClick={() => choose({ ...cur, mode: m.value })}>
            {m.label}
          </button>
        ))}
      </div>
    </section>
  );
}
