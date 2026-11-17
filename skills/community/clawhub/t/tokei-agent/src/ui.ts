// Interactive terminal UI for tokei-agent.
//
// This module is PRESENTATION ONLY and is deliberately inert unless a real
// human terminal is attached. stdout is the machine contract for this CLI —
// JSON for every command, and the JSON-RPC transport in `mcp` mode — so
// createTerm() returns undefined for pipes, redirects, CI, MCP and tests, and
// every call site degrades to today's byte-identical output.
//
// Zero runtime dependencies, in keeping with the rest of the package.

export interface TermHost {
  // RAW write — no trailing newline is added, unlike Io.stdout.
  write: (chunk: string) => void;
  isTTY: boolean;
  columns?: number;
  env: Record<string, string | undefined>;
  // process.platform, injected. src/ deliberately has no @types/node and never
  // touches `process` — the bin owns all environment access.
  platform?: string;
  // Registers a Ctrl+C handler and returns an unregister function. The bin
  // owns the signal wiring (and the re-raise); the UI only needs to restore
  // the cursor before the process goes away.
  onInterrupt?: (handler: () => void) => () => void;
}

// The canonical wordmark. All six rows are exactly 37 columns.
//
// DO NOT hand-edit. The fifth letter is "I" (`██╗/██║/██║/██║/██║/╚═╝`); the
// visually similar "L" (`.../███████╗/╚══════╝`) would spell TOKEL, which is
// how an earlier draft of this art was wrong. logoIsIntact() below is the
// regression guard.
export const LOGO: readonly string[] = [
  "████████╗ ██████╗ ██╗  ██╗███████╗██╗",
  "╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝██║",
  "   ██║   ██║   ██║█████╔╝ █████╗  ██║",
  "   ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║",
  "   ██║   ╚██████╔╝██║  ██╗███████╗██║",
  "   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝",
];

export const LOGO_WIDTH = 37;
export const LOGO_HEIGHT = 6;
const INDENT = "              "; // 14 spaces -> block sits at 51 columns
const BODY_INDENT = "        ";

/** Regression guard: the art must be 6x37 and end in "I", never "L". */
export function logoIsIntact(): boolean {
  return (
    LOGO.length === LOGO_HEIGHT &&
    LOGO.every((r) => [...r].length === LOGO_WIDTH) &&
    LOGO[4]!.endsWith("██║") &&
    LOGO[5]!.endsWith("╚═╝")
  );
}

type Rgb = readonly [number, number, number];

// Palindromic stop list: the first and last stops are identical, so a moving
// gradient wraps with no visible seam. Every stop is inside the
// blue/purple/magenta family, which is what keeps a *moving* gradient on-brand
// without per-frame tuning.
const STOPS: readonly Rgb[] = [
  [0x25, 0x63, 0xeb], // deep blue
  [0x22, 0xd3, 0xee], // cyan
  [0x7d, 0x78, 0xc6], // brand purple
  [0xe8, 0x79, 0xf9], // magenta
  [0x7d, 0x78, 0xc6], // brand purple
  [0x22, 0xd3, 0xee], // cyan
  [0x25, 0x63, 0xeb], // deep blue (== stop 0)
];

// Vertical weight dominates so the motion reads as downward. The horizontal
// weight is small but load-bearing: with WH = 0 the 6-row logo has only six
// sampling positions and renders as four flat bands instead of a gradient.
const WV = 0.5;
const WH = 0.3;

const PHASE_PER_FRAME = 0.0208; // ~2.4s per cycle at 50ms
const FRAME_MS = 50;
const MIN_BANNER_MS = 700;
const REST_MS = 150;

const GREEN: Rgb = [0x22, 0xc5, 0x5e];
const RED: Rgb = [0xef, 0x44, 0x44];
const PURPLE: Rgb = [0x7d, 0x78, 0xc6];

// In-flight spinner. Every frame is a *circle* — the glyph only rotates its
// fill, so the step marker never stops reading as the same purple dot it is
// when static. (A braille/line spinner would change the mark's identity
// mid-command.) The colour does NOT animate: the marker stays brand PURPLE
// throughout, exactly as it was before. The static fallback stays "◉", so
// NO_COLOR, TOKEI_NO_ANIM and legacy consoles render what they always did.
export const SPINNER: readonly string[] = ["◐", "◓", "◑", "◒"];
export const SPINNER_STATIC = "◉";

// Two 50ms frames per glyph -> 100ms each, 400ms per revolution. At one frame
// per glyph it reads as a flicker rather than a rotation.
const SPINNER_FRAME_DIV = 2;

/** Spinner glyph for an animation frame. */
export function spinnerGlyph(frame: number): string {
  return SPINNER[Math.floor(frame / SPINNER_FRAME_DIV) % SPINNER.length]!;
}

/** Sample the palindromic ramp at t (wraps). */
export function sampleStops(t: number): Rgb {
  const w = ((t % 1) + 1) % 1;
  const segments = STOPS.length - 1;
  const scaled = w * segments;
  const i = Math.min(Math.floor(scaled), segments - 1);
  const f = scaled - i;
  const a = STOPS[i]!;
  const b = STOPS[i + 1]!;
  return [
    Math.round(a[0] + (b[0] - a[0]) * f),
    Math.round(a[1] + (b[1] - a[1]) * f),
    Math.round(a[2] + (b[2] - a[2]) * f),
  ];
}

/** Colour of one logo cell at a given animation phase. */
export function cellColor(row: number, col: number, phase: number): Rgb {
  const t = (row / LOGO_HEIGHT) * WV + (col / (LOGO_WIDTH - 1)) * WH - phase;
  return sampleStops(t);
}

type ColorMode = "truecolor" | "ansi256" | "none";

export function detectColorMode(env: Record<string, string | undefined>): ColorMode {
  if (env.NO_COLOR !== undefined && env.NO_COLOR !== "") return "none";
  if (env.FORCE_COLOR !== undefined && env.FORCE_COLOR !== "" && env.FORCE_COLOR !== "0") {
    return "truecolor";
  }
  const ct = (env.COLORTERM ?? "").toLowerCase();
  if (ct.includes("truecolor") || ct.includes("24bit")) return "truecolor";
  return "ansi256";
}

/** Legacy Windows console (conhost + code page 437/850) mangles box drawing. */
export function isLegacyWindowsConsole(
  env: Record<string, string | undefined>,
  platform: string | undefined,
): boolean {
  if (platform !== "win32") return false;
  return !env.WT_SESSION && !env.TERM_PROGRAM && !env.ConEmuANSI;
}

function fg(c: Rgb, mode: ColorMode): string {
  if (mode === "none") return "";
  if (mode === "truecolor") return `\x1b[38;2;${c[0]};${c[1]};${c[2]}m`;
  // 6x6x6 cube
  const q = (v: number) => Math.round((v / 255) * 5);
  return `\x1b[38;5;${16 + 36 * q(c[0]) + 6 * q(c[1]) + q(c[2])}m`;
}

const RESET = "\x1b[0m";
const DIM = "\x1b[2m";
const BOLD = "\x1b[1m";
const HIDE_CURSOR = "\x1b[?25l";
const SHOW_CURSOR = "\x1b[?25h";
// Erase from the cursor to end of line. Redrawing in place rewrites each line
// but does not shorten it, so without this a short label leaves the tail of a
// longer previous one on screen ("✓ Signed in" over "◉ Verifying your API key…"
// rendered as "✓ Signed in your API key…"). Cursor control, not colour, so it
// is still emitted under NO_COLOR — that mode redraws once in finish().
const CLEAR_EOL = "\x1b[K";

/**
 * Render one logo row, emitting a colour escape only when the colour actually
 * changes from the previous cell. Spaces are never coloured.
 */
export function renderLogoRow(row: number, phase: number, mode: ColorMode): string {
  const chars = [...LOGO[row]!];
  if (mode === "none") return INDENT + chars.join("");
  let out = INDENT;
  let last = "";
  for (let col = 0; col < chars.length; col++) {
    const ch = chars[col]!;
    if (ch === " ") {
      if (last !== "") {
        out += RESET;
        last = "";
      }
      out += ch;
      continue;
    }
    const code = fg(cellColor(row, col, phase), mode);
    if (code !== last) {
      out += code;
      last = code;
    }
    out += ch;
  }
  if (last !== "") out += RESET;
  return out;
}

/**
 * A STATIC wordmark block for `--help`, returned as a string instead of being
 * written by a Term.
 *
 * `--help` and `--version` return from main() before the Term is ever created
 * (there is no in-flight request to animate), so the interactive UI could not
 * reach them — yet `--help` is the first command most humans run. This renders
 * the same art, settled at the deterministic end-of-cycle phase the animation
 * eases to, with no cursor control and no timers.
 *
 * Gates are deliberately identical to createTerm(): undefined for pipes,
 * redirects, CI, `TERM=dumb`, `TOKEI_OUTPUT=json`, narrow terminals and
 * corrupted art. So `tokei-agent --help | ...` stays byte-identical for agents
 * and scripts that parse it.
 */
export function renderBanner(host: TermHost | undefined): string | undefined {
  if (!host || !host.isTTY) return undefined;
  const env = host.env;
  if ((env.TOKEI_OUTPUT ?? "").toLowerCase() === "json") return undefined;
  if (env.CI !== undefined && env.CI !== "") return undefined;
  if (env.TERM === "dumb") return undefined;
  if (effectiveColumns(host) < 60) return undefined;
  if (!logoIsIntact()) return undefined;

  const mode = detectColorMode(env);
  if (isLegacyWindowsConsole(env, host.platform)) {
    return `\n${INDENT}T O K E I   A G E N T\n\n`;
  }
  // Phase 1 == the whole-cycle value settle() eases to, so the static banner is
  // the same frame a finished `me` run leaves on screen.
  const lines: string[] = [""];
  for (let r = 0; r < LOGO_HEIGHT; r++) lines.push(renderLogoRow(r, 1, mode));
  lines.push("");
  const sub = `${INDENT}      T O K E I   A G E N T`;
  lines.push(mode === "none" ? sub : `${DIM}${sub}${RESET}`);
  lines.push("");
  return lines.join("\n") + "\n";
}

export interface SummaryRow {
  label: string;
  value: string;
}

export interface Step {
  done(message: string): void;
  fail(message: string): void;
}

export interface Term {
  /**
   * Print the opening block and start the gradient. `logo: false` prints only
   * the step line — the full wordmark is reserved for `me`, so that routine
   * commands like `pages:list` stay compact.
   */
  start(stepLabel: string, opts?: { logo?: boolean }): void;
  /** Update the in-flight step's label without ending the animation. */
  setStep(label: string): void;
  /** Stop animating, settle the gradient, and resolve the step line. */
  finish(outcome: "done" | "fail", message: string): Promise<void>;
  /** Print the account summary below the (now static) banner. */
  summary(opts: { welcome?: string; rows?: SummaryRow[]; closing?: string }): void;
  /** Restore the cursor. Safe to call repeatedly. */
  dispose(): void;
}

/**
 * Returns undefined — making every call site a no-op — unless a real
 * interactive terminal is attached and the user has not opted out. That is what
 * keeps stdout byte-identical for agents, pipes, CI, MCP and the test suite.
 */
export function createTerm(host: TermHost | undefined): Term | undefined {
  if (!host || !host.isTTY) return undefined;
  const env = host.env;
  if ((env.TOKEI_OUTPUT ?? "").toLowerCase() === "json") return undefined;
  if (env.CI !== undefined && env.CI !== "") return undefined;
  if (env.TERM === "dumb") return undefined;
  // 0 means "unknown" (some ptys and CI shims report it on a perfectly good
  // TTY), not "zero columns wide" — treat it like undefined.
  if (effectiveColumns(host) < 60) return undefined;
  if (!logoIsIntact()) return undefined;
  return new TermImpl(host);
}

/** Terminal width, defaulting when the host reports 0 or nothing. */
function effectiveColumns(host: TermHost): number {
  return host.columns !== undefined && host.columns > 0 ? host.columns : 80;
}

const sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

class TermImpl implements Term {
  private readonly host: TermHost;
  private readonly mode: ColorMode;
  private readonly legacy: boolean;
  private readonly animateCapable: boolean;
  private phase = 0;
  private frame = 0;
  private showLogo = true;
  private stepText = "";
  private stepOutcome: "pending" | "done" | "fail" = "pending";
  private stepMessage = "";
  private blockLines = 0;
  private startedAt = 0;
  private running = false;
  private disposed = false;
  private unhook?: () => void;

  /**
   * The loop runs whenever the terminal can animate — the compact one-line form
   * has the spinner to drive even with no wordmark on screen. It used to be
   * gated on `showLogo`, which is why the step marker was frozen for every
   * command except `me`.
   */
  private get animate(): boolean {
    return this.animateCapable;
  }

  constructor(host: TermHost) {
    this.host = host;
    this.mode = detectColorMode(host.env);
    this.legacy = isLegacyWindowsConsole(host.env, host.platform);
    // No colour means no gradient, so there is nothing to animate.
    this.animateCapable =
      this.mode !== "none" &&
      !this.legacy &&
      (host.env.TOKEI_NO_ANIM ?? "") === "" &&
      effectiveColumns(host) >= LOGO_WIDTH + INDENT.length;
  }

  start(stepLabel: string, opts?: { logo?: boolean }): void {
    this.showLogo = opts?.logo !== false;
    this.stepText = stepLabel;
    this.stepOutcome = "pending";
    this.startedAt = Date.now();
    if (this.animate) {
      this.host.write(HIDE_CURSOR);
      // A Ctrl+C mid-animation must never leave the cursor hidden in the
      // user's shell. The bin re-raises the signal after this runs.
      this.unhook = this.host.onInterrupt?.(() => {
        this.dispose();
        this.host.write("\n");
      });
    }
    this.host.write(this.block());
    if (this.animate) {
      this.running = true;
      void this.loop();
    }
  }

  setStep(label: string): void {
    this.stepText = label;
    this.stepOutcome = "pending";
    if (!this.animate) this.redraw();
  }

  /**
   * The step line, rendered fresh on every frame. This is deliberately NOT
   * cached into a string at start()/setStep() time — the spinner has to be able
   * to advance between redraws.
   */
  private stepLine(): string {
    if (this.stepOutcome === "pending") {
      const glyph = this.legacy ? "*" : this.animate ? spinnerGlyph(this.frame) : SPINNER_STATIC;
      const mark = this.mode === "none" ? glyph : `${fg(PURPLE, this.mode)}${glyph}${RESET}`;
      return `${mark} ${this.stepText}${this.legacy ? "..." : "…"}`;
    }
    const done = this.stepOutcome === "done";
    const glyph = this.legacy ? (done ? "[ok]" : "[!]") : done ? "✓" : "✗";
    const mark =
      this.mode === "none" ? glyph : `${fg(done ? GREEN : RED, this.mode)}${glyph}${RESET}`;
    return `${mark} ${this.stepMessage}`;
  }

  async finish(outcome: "done" | "fail", message: string): Promise<void> {
    // The minimum-on-screen hold and the gradient settle exist so the wordmark
    // is legible before it goes static. Both are gated on `showLogo`, NOT on
    // `animate` — otherwise enabling the spinner would silently add ~850ms to
    // every routine command.
    if (this.animate && this.showLogo) {
      const elapsed = Date.now() - this.startedAt;
      // Overlap, never pad: the request has already been running for `elapsed`.
      if (elapsed < MIN_BANNER_MS) await sleep(MIN_BANNER_MS - elapsed);
      await this.settle();
    }
    // Stop the loop before the final draw, so a queued frame cannot repaint the
    // spinner over the resolved ✓/✗.
    this.running = false;
    this.stepOutcome = outcome;
    this.stepMessage = message;
    this.redraw();
    this.dispose();
  }

  summary(opts: { welcome?: string; rows?: SummaryRow[]; closing?: string }): void {
    const w = this.host.write.bind(this.host);
    const dim = (s: string) => (this.mode === "none" ? s : `${DIM}${s}${RESET}`);
    const bold = (s: string) => (this.mode === "none" ? s : `${BOLD}${s}${RESET}`);
    if (opts.welcome) w(`\n${BODY_INDENT}${opts.welcome}\n`);
    if (opts.rows?.length) {
      w("\n");
      const width = Math.max(...opts.rows.map((r) => r.label.length)) + 4;
      for (const r of opts.rows) {
        w(`${BODY_INDENT}${dim(r.label.padEnd(width))}${bold(r.value)}\n`);
      }
    }
    if (opts.closing) w(`\n${BODY_INDENT}${dim(opts.closing)}\n`);
    w("\n");
  }

  dispose(): void {
    if (this.disposed) return;
    this.disposed = true;
    this.running = false;
    if (this.unhook) {
      this.unhook();
      this.unhook = undefined;
    }
    if (this.animate) this.host.write(SHOW_CURSOR);
  }

  // --- internals ---------------------------------------------------------

  /** The full redraw region: logo, subtitle, version, step. */
  private block(): string {
    const lines: string[] = [];
    if (!this.showLogo) {
      lines.push(`${BODY_INDENT}${this.stepLine()}`);
      return this.finalise(lines);
    }
    if (this.legacy) {
      lines.push("", `${INDENT}T O K E I   A G E N T`, "");
    } else {
      // Leading blank line so the wordmark does not butt against the prompt.
      lines.push("");
      for (let r = 0; r < LOGO_HEIGHT; r++) lines.push(renderLogoRow(r, this.phase, this.mode));
      lines.push("");
      const sub = `${INDENT}      T O K E I   A G E N T`;
      lines.push(this.mode === "none" ? sub : `${DIM}${sub}${RESET}`);
    }
    lines.push("");
    lines.push(`${BODY_INDENT}${this.stepLine()}`);
    return this.finalise(lines);
  }

  /**
   * Records the redraw height and clears each line's tail. blockLines is
   * derived from the array, so adding or removing a line self-corrects the
   * cursor-up arithmetic in redraw().
   */
  private finalise(lines: string[]): string {
    this.blockLines = lines.length;
    return lines.map((l) => l + CLEAR_EOL).join("\n") + "\n";
  }

  private redraw(): void {
    const n = this.blockLines;
    this.host.write(`\x1b[${n}A` + this.block());
  }

  private async loop(): Promise<void> {
    while (this.running && !this.disposed) {
      await sleep(FRAME_MS);
      if (!this.running || this.disposed) break;
      this.phase += PHASE_PER_FRAME;
      this.frame++;
      this.redraw();
    }
  }

  /**
   * Ease the phase to the next whole cycle so the final frame is deterministic
   * — otherwise the same command settles on a different-looking logo each run.
   */
  private async settle(): Promise<void> {
    const from = this.phase;
    const to = Math.ceil(this.phase || 1);
    const frames = Math.max(1, Math.round(REST_MS / FRAME_MS));
    for (let i = 1; i <= frames; i++) {
      await sleep(FRAME_MS);
      this.phase = from + (to - from) * (i / frames);
      this.frame++;
      this.redraw();
    }
    this.phase = 0;
    this.redraw();
  }
}

/** Human summary of a failed request, from the real HTTP status. */
export function failureMessage(status: number | undefined, payload: unknown): string {
  if (status === undefined) return "Couldn't reach Tokei";
  switch (status) {
    case 401:
      return "API key rejected";
    case 403:
      return "This key doesn't have write access";
    case 404:
      return "Not found";
    case 422:
      return "Tokei rejected the changes";
    case 429:
      return "Rate limit reached — try again shortly";
    default:
      break;
  }
  if (status >= 500) return "Tokei is having trouble — try again";
  const msg =
    payload !== null && typeof payload === "object"
      ? (payload as { error?: { message?: unknown } }).error?.message
      : undefined;
  return typeof msg === "string" && msg.length > 0 ? msg : "Request failed";
}

export function formatCount(n: number): string {
  return new Intl.NumberFormat("en-US").format(n);
}
