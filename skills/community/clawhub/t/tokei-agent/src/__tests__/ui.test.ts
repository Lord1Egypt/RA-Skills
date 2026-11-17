/** @jest-environment node */
import {
  LOGO,
  LOGO_HEIGHT,
  LOGO_WIDTH,
  cellColor,
  createTerm,
  detectColorMode,
  failureMessage,
  formatCount,
  isLegacyWindowsConsole,
  logoIsIntact,
  renderBanner,
  renderLogoRow,
  sampleStops,
  SPINNER,
  SPINNER_STATIC,
  spinnerGlyph,
} from "../ui.js";
import type { TermHost } from "../ui.js";

/**
 * Colour escapes are emitted per-glyph run, so the logo never appears as a
 * contiguous substring in coloured output. Strip SGR/cursor sequences before
 * asserting on shape.
 */
// eslint-disable-next-line no-control-regex -- matching escape sequences is the point
const stripAnsi = (s: string) => s.replace(/\x1b\[[0-9;?]*[A-Za-z]/g, "");

/**
 * A minimal terminal screen model.
 *
 * The raw-write assertions elsewhere in this file check that the right bytes
 * are emitted, which is a different property from what the user ends up
 * seeing. Redrawing in place overwrites characters without shortening the
 * line, so a short label drawn over a longer one leaves a tail behind — the
 * bytes are correct, the screen is wrong. This models cursor-up, clear-to-EOL
 * and overwrite semantics so tests can assert on the visible result.
 */
function screen(chunks: string[]): string[] {
  const lines: string[] = [""];
  let row = 0;
  let col = 0;
  const put = (text: string) => {
    const cur = lines[row] ?? "";
    lines[row] = cur.padEnd(col, " ").slice(0, col) + text + cur.slice(col + text.length);
    col += text.length;
  };
  // eslint-disable-next-line no-control-regex -- driving escape sequences is the point
  const token = /\x1b\[([0-9;?]*)([A-Za-z])|\n|[^\n\x1b]+/g;
  const all = chunks.join("");
  for (const m of all.matchAll(token)) {
    const [raw, params, cmd] = m;
    if (raw === "\n") {
      row += 1;
      col = 0;
      while (lines.length <= row) lines.push("");
    } else if (cmd === "A") {
      row = Math.max(0, row - (Number(params) || 1));
      col = 0;
    } else if (cmd === "K") {
      lines[row] = (lines[row] ?? "").slice(0, col);
    } else if (cmd === undefined) {
      put(raw);
    }
    // every other sequence (colour, cursor show/hide) has no effect on layout
  }
  return lines;
}

function host(over: Partial<TermHost> = {}): TermHost & { out: string[] } {
  const out: string[] = [];
  return {
    out,
    write: (c: string) => out.push(c),
    isTTY: true,
    columns: 120,
    env: { COLORTERM: "truecolor" },
    platform: "linux",
    ...over,
  } as TermHost & { out: string[] };
}

describe("logo integrity", () => {
  // The original brief's art had an "L" as the fifth letter, which spells
  // TOKEL. I and L are identical for four of six rows in ANSI Shadow, so only
  // the last two rows distinguish them.
  it("is 6 rows of exactly 37 columns", () => {
    expect(LOGO).toHaveLength(LOGO_HEIGHT);
    for (const row of LOGO) expect([...row]).toHaveLength(LOGO_WIDTH);
  });

  it("spells TOKEI, not TOKEL", () => {
    expect(LOGO[4]!.endsWith("██║")).toBe(true);
    expect(LOGO[5]!.endsWith("╚═╝")).toBe(true);
    expect(LOGO[4]!.endsWith("███████╗")).toBe(false);
    expect(LOGO[5]!.endsWith("╚══════╝")).toBe(false);
    expect(logoIsIntact()).toBe(true);
  });
});

describe("gradient", () => {
  it("wraps seamlessly — first and last stop are identical", () => {
    expect(sampleStops(0)).toEqual(sampleStops(1));
    expect(sampleStops(0.0001)).toEqual(sampleStops(1.0001));
  });

  it("stays in the blue/purple/magenta family — never green or yellow", () => {
    for (let i = 0; i <= 100; i++) {
      const [, g, b] = sampleStops(i / 100);
      // Blue is always a strong component; green never dominates it.
      expect(b).toBeGreaterThan(150);
      expect(g).toBeLessThanOrEqual(b);
    }
  });

  it("has enough distinct colours to avoid banding", () => {
    // A pure vertical gradient over 6 rows yields exactly 6 colours — flat
    // bands. The horizontal weight is what turns it into a gradient: it lifts
    // this to 62 distinct colours across the 37x6 grid.
    const seen = new Set<string>();
    for (let r = 0; r < LOGO_HEIGHT; r++) {
      for (let c = 0; c < LOGO_WIDTH; c++) seen.add(cellColor(r, c, 0).join(","));
    }
    expect(seen.size).toBeGreaterThan(LOGO_HEIGHT * 5);
  });

  it("is smooth horizontally — no visible stepping along a row", () => {
    // The real anti-banding property: neighbouring cells must be close. A
    // large jump here would read as a hard edge mid-letter.
    let worst = 0;
    for (let r = 0; r < LOGO_HEIGHT; r++) {
      for (let c = 0; c < LOGO_WIDTH - 1; c++) {
        const a = cellColor(r, c, 0);
        const b = cellColor(r, c + 1, 0);
        for (let k = 0; k < 3; k++) worst = Math.max(worst, Math.abs(a[k]! - b[k]!));
      }
    }
    expect(worst).toBeLessThanOrEqual(12);
  });

  it("travels downward — a colour moves to a lower row as phase advances", () => {
    const target = cellColor(1, 0, 0);
    const moved = cellColor(2, 0, 1 / LOGO_HEIGHT * 0.5);
    expect(moved).toEqual(target);
  });
});

describe("renderLogoRow", () => {
  it("emits truecolor escapes and never colours spaces", () => {
    const line = renderLogoRow(0, 0, "truecolor");
    expect(line).toContain("\x1b[38;2;");
    // eslint-disable-next-line no-control-regex -- matching escape sequences is the point
    expect(line).not.toMatch(/\x1b\[38;2;[\d;]+m {2}/);
  });

  it("emits no escapes at all when colour is off", () => {
    const line = renderLogoRow(0, 0, "none");
    expect(line).not.toContain("\x1b");
    expect(line).toContain(LOGO[0]);
  });

  it("re-emits a colour only when it changes", () => {
    const line = renderLogoRow(0, 0, "truecolor");
    // eslint-disable-next-line no-control-regex -- matching escape sequences is the point
    const escapes = line.match(/\x1b\[38;2;[\d;]+m/g) ?? [];
    // Far fewer escapes than glyphs — otherwise every cell is being restated.
    expect(escapes.length).toBeLessThan(LOGO_WIDTH);
  });
});

describe("createTerm gating", () => {
  it("returns undefined when stdout is not a TTY", () => {
    expect(createTerm(host({ isTTY: false }))).toBeUndefined();
  });

  it("returns undefined when the host is absent (tests, embedders, MCP)", () => {
    expect(createTerm(undefined)).toBeUndefined();
  });

  it("returns undefined for TOKEI_OUTPUT=json", () => {
    expect(createTerm(host({ env: { TOKEI_OUTPUT: "json" } }))).toBeUndefined();
    expect(createTerm(host({ env: { TOKEI_OUTPUT: "JSON" } }))).toBeUndefined();
  });

  it("returns undefined in CI and on dumb terminals", () => {
    expect(createTerm(host({ env: { CI: "1" } }))).toBeUndefined();
    expect(createTerm(host({ env: { TERM: "dumb" } }))).toBeUndefined();
  });

  it("returns undefined for a narrow terminal", () => {
    expect(createTerm(host({ columns: 40 }))).toBeUndefined();
  });

  it("treats 0 or missing columns as unknown, not as a zero-width terminal", () => {
    // A pty whose size was never set reports 0 on a perfectly usable TTY.
    // Reading that as "narrower than 60" silently disabled the whole UI.
    expect(createTerm(host({ columns: 0 }))).toBeDefined();
    expect(createTerm(host({ columns: undefined }))).toBeDefined();
  });

  it("returns a Term for a normal interactive terminal", () => {
    expect(createTerm(host())).toBeDefined();
  });
});

describe("renderBanner (the --help wordmark)", () => {
  // --help returns from main() before any Term exists, so this is the only
  // path that can decorate it. The gates must match createTerm exactly,
  // because `tokei-agent --help | grep ...` is a documented agent workflow.
  it("is suppressed everywhere createTerm is suppressed", () => {
    expect(renderBanner(undefined)).toBeUndefined();
    expect(renderBanner(host({ isTTY: false }))).toBeUndefined();
    expect(renderBanner(host({ env: { TOKEI_OUTPUT: "json" } }))).toBeUndefined();
    expect(renderBanner(host({ env: { TOKEI_OUTPUT: "JSON" } }))).toBeUndefined();
    expect(renderBanner(host({ env: { CI: "1" } }))).toBeUndefined();
    expect(renderBanner(host({ env: { TERM: "dumb" } }))).toBeUndefined();
    expect(renderBanner(host({ columns: 40 }))).toBeUndefined();
  });

  it("renders all six wordmark rows plus the subtitle at a real terminal", () => {
    const out = renderBanner(host());
    expect(out).toBeDefined();
    // eslint-disable-next-line no-control-regex -- matching escape sequences is the point
    const plain = out!.replace(/\x1b\[[\d;]*m/g, "");
    for (const row of LOGO) expect(plain).toContain(row);
    expect(plain).toContain("T O K E I   A G E N T");
  });

  it("emits no cursor control — it is static, unlike the animated Term", () => {
    const out = renderBanner(host())!;
    expect(out).not.toContain("\x1b[?25l");
    expect(out).not.toContain("\x1b[?25h");
    expect(out).not.toContain("\x1b[K");
  });

  it("is deterministic — the same frame on every run", () => {
    expect(renderBanner(host())).toBe(renderBanner(host()));
  });

  it("falls back to plain text on a legacy Windows console", () => {
    const out = renderBanner(host({ platform: "win32", env: { COLORTERM: "truecolor" } }));
    expect(out).toBe("\n              T O K E I   A G E N T\n\n");
  });

  it("drops colour under NO_COLOR but keeps the art", () => {
    const out = renderBanner(host({ env: { NO_COLOR: "1" } }))!;
    expect(out).not.toContain("\x1b[38;2;");
    expect(out).toContain(LOGO[0]!);
  });
});

describe("terminal output", () => {
  it("writes the logo and restores the cursor on finish", async () => {
    const h = host();
    const term = createTerm(h)!;
    term.start("Verifying your API key");
    await term.finish("done", "Signed in");
    const all = h.out.join("");
    expect(stripAnsi(all)).toContain("████████╗");
    expect(stripAnsi(all)).toContain("Signed in");
    expect(all).toContain("\x1b[?25h"); // cursor restored
  }, 10000);

  it("dispose() is idempotent", () => {
    const h = host();
    const term = createTerm(h)!;
    term.start("Loading page");
    expect(() => {
      term.dispose();
      term.dispose();
    }).not.toThrow();
  });

  it("emits no colour escapes when NO_COLOR is set", async () => {
    const h = host({ env: { NO_COLOR: "1" } });
    const term = createTerm(h)!;
    term.start("Verifying your API key");
    await term.finish("done", "Signed in");
    const all = h.out.join("");
    expect(stripAnsi(all)).toContain("████████╗"); // logo still rendered
    expect(all).not.toContain("\x1b[38;2;");
    expect(all).not.toContain("\x1b[38;5;");
  });

  it("omits the wordmark when logo:false", async () => {
    const h = host();
    const term = createTerm(h)!;
    term.start("Fetching your pages", { logo: false });
    await term.finish("done", "4 pages");
    const all = h.out.join("");
    expect(stripAnsi(all)).not.toContain("████████╗");
    expect(stripAnsi(all)).toContain("4 pages");
  });

  it("uses an ASCII wordmark on a legacy Windows console", async () => {
    const h = host({ platform: "win32", env: { COLORTERM: "truecolor" } });
    const term = createTerm(h)!;
    term.start("Verifying your API key");
    await term.finish("done", "Signed in");
    const all = h.out.join("");
    expect(all).not.toContain("█");
    expect(stripAnsi(all)).toContain("T O K E I   A G E N T");
  });

  // Regression: the done label is shorter than the pending label, so an
  // in-place redraw that does not erase leaves the tail of the old text
  // behind. Observed in PowerShell as "✓ Signed in your API key…".
  it("leaves no stale text when a short label overwrites a longer one", async () => {
    const h = host();
    const term = createTerm(h)!;
    term.start("Verifying your API key");
    await term.finish("done", "Signed in");
    const visible = screen(h.out).map((l) => stripAnsi(l).trimEnd());
    const step = visible.filter((l) => l.includes("Signed in")).pop();
    expect(step?.trim()).toBe("✓ Signed in");
    expect(visible.join("\n")).not.toContain("your API key");
  }, 10000);

  it("leaves no stale text in the compact one-line form", async () => {
    const h = host();
    const term = createTerm(h)!;
    term.start("Fetching your pages", { logo: false });
    await term.finish("done", "4 pages");
    const visible = screen(h.out).map((l) => stripAnsi(l).trimEnd());
    expect(visible.filter((l) => l.includes("4 pages")).pop()?.trim()).toBe("✓ 4 pages");
    expect(visible.join("\n")).not.toContain("your pages");
  });

  it("leaves no stale text under NO_COLOR either", async () => {
    const h = host({ env: { NO_COLOR: "1" } });
    const term = createTerm(h)!;
    term.start("Verifying your API key");
    await term.finish("done", "Signed in");
    expect(screen(h.out).join("\n")).not.toContain("your API key");
  });

  it("opens with a blank line so the logo clears the shell prompt", async () => {
    const h = host();
    const term = createTerm(h)!;
    term.start("Verifying your API key");
    await term.finish("done", "Signed in");
    expect(screen(h.out)[0]!.trim()).toBe("");
  }, 10000);

  // The step marker used to be frozen for every command except `me`: the loop
  // was gated on showLogo, and pending() baked the glyph into a cached string.
  it("advances the spinner in the compact one-line form", async () => {
    const h = host();
    const term = createTerm(h)!;
    term.start("Fetching action catalog", { logo: false });
    await new Promise((r) => setTimeout(r, 350));
    const seen = new Set(SPINNER.filter((g) => h.out.join("").includes(g)));
    await term.finish("done", "Catalog loaded");
    expect(seen.size).toBeGreaterThan(1);
  }, 10000);

  it("keeps the static marker when animation is off", async () => {
    const h = host({ env: { TOKEI_NO_ANIM: "1" } });
    const term = createTerm(h)!;
    term.start("Fetching action catalog", { logo: false });
    await new Promise((r) => setTimeout(r, 250));
    const all = h.out.join("");
    await term.finish("done", "Catalog loaded");
    expect(all).toContain(SPINNER_STATIC);
    for (const g of SPINNER) expect(all).not.toContain(g);
  });

  // Regression guard for the cost of un-gating the loop: MIN_BANNER_MS and the
  // gradient settle must stay tied to the wordmark, or every routine command
  // silently grows an ~850ms tail.
  it("does not delay the compact form", async () => {
    const h = host();
    const term = createTerm(h)!;
    const t0 = Date.now();
    term.start("Fetching action catalog", { logo: false });
    await term.finish("done", "Catalog loaded");
    expect(Date.now() - t0).toBeLessThan(300);
  });

  it("resolves to the outcome glyph, never a spinner frame", async () => {
    const h = host();
    const term = createTerm(h)!;
    term.start("Fetching action catalog", { logo: false });
    await new Promise((r) => setTimeout(r, 250));
    await term.finish("done", "Catalog loaded");
    const visible = screen(h.out).map((l) => stripAnsi(l).trimEnd());
    const step = visible.filter((l) => l.includes("Catalog loaded")).pop();
    expect(step?.trim()).toBe("✓ Catalog loaded");
    for (const g of SPINNER) expect(step).not.toContain(g);
  }, 10000);

  it("cycles the spinner glyph two frames at a time", () => {
    expect(spinnerGlyph(0)).toBe(SPINNER[0]);
    expect(spinnerGlyph(1)).toBe(SPINNER[0]);
    expect(spinnerGlyph(2)).toBe(SPINNER[1]);
    expect(spinnerGlyph(SPINNER.length * 2)).toBe(SPINNER[0]);
  });

  // The colour was explicitly left alone: only the glyph animates. A pulsing
  // marker was tried and rejected.
  it("keeps the marker brand purple on every frame", async () => {
    const h = host();
    const term = createTerm(h)!;
    term.start("Fetching action catalog", { logo: false });
    await new Promise((r) => setTimeout(r, 350));
    const pending = h.out.join("").split("\x1b[K")[0] ?? "";
    await term.finish("done", "Catalog loaded");
    // eslint-disable-next-line no-control-regex -- matching escape sequences is the point
    const colours = new Set(pending.match(/\x1b\[38;2;[0-9;]+m/g) ?? []);
    expect(colours).toEqual(new Set(["\x1b[38;2;125;120;198m"])); // 0x7d78c6
  }, 10000);

  it("renders only the summary fields that are present", () => {
    const h = host();
    const term = createTerm(h)!;
    term.summary({ welcome: "Welcome back, a@b.com", rows: [{ label: "Plan", value: "ADMIN" }] });
    const all = stripAnsi(h.out.join(""));
    expect(all).toContain("Welcome back, a@b.com");
    expect(all).toContain("Plan");
    expect(all).toContain("ADMIN");
  });
});

describe("helpers", () => {
  it("detects colour modes", () => {
    expect(detectColorMode({ NO_COLOR: "1" })).toBe("none");
    expect(detectColorMode({ COLORTERM: "truecolor" })).toBe("truecolor");
    expect(detectColorMode({ FORCE_COLOR: "1" })).toBe("truecolor");
    expect(detectColorMode({})).toBe("ansi256");
  });

  it("detects legacy Windows consoles only on win32", () => {
    expect(isLegacyWindowsConsole({}, "win32")).toBe(true);
    expect(isLegacyWindowsConsole({ WT_SESSION: "x" }, "win32")).toBe(false);
    expect(isLegacyWindowsConsole({}, "linux")).toBe(false);
  });

  it("describes failures from the real HTTP status", () => {
    expect(failureMessage(undefined, {})).toBe("Couldn't reach Tokei");
    expect(failureMessage(401, {})).toBe("API key rejected");
    expect(failureMessage(403, {})).toBe("This key doesn't have write access");
    expect(failureMessage(429, {})).toContain("Rate limit");
    expect(failureMessage(503, {})).toContain("having trouble");
  });

  it("formats counts with thousands separators", () => {
    expect(formatCount(50000)).toBe("50,000");
    expect(formatCount(0)).toBe("0");
  });
});
