#!/usr/bin/env node

/**
 * task-progress-stream
 *
 * Stream long-running task progress into OpenClaw chat UI by:
 *  - running a command and parsing stdout/stderr, OR
 *  - tailing an existing log file
 *
 * It periodically injects compact progress summaries into a chat session via:
 *   openclaw gateway call chat.inject
 *
 * Usage:
 *   node task_progress_stream.js run \
 *     --session main \
 *     --label train \
 *     --cwd /path/to/project \
 *     --cmd "python src/train.py --config configs/train.yaml" \
 *     --interval-sec 20
 *
 *   node task_progress_stream.js tail \
 *     --session main \
 *     --label train \
 *     --file /path/to/train.log \
 *     --interval-sec 20
 */

const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith("--")) {
        args[key] = true;
      } else {
        args[key] = next;
        i++;
      }
    } else {
      args._.push(a);
    }
  }
  return args;
}

function nowIso() {
  return new Date().toISOString();
}

function safeNum(v) {
  if (v == null) return null;
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

class ProgressState {
  constructor(label) {
    this.label = label || "task";
    this.state = "idle";
    this.startedAt = null;
    this.endedAt = null;
    this.returnCode = null;
    this.pid = null;

    this.epoch = null;
    this.maxEpoch = null;
    this.step = null;
    this.maxStep = null;
    this.loss = null;
    this.lr = null;
    this.valMetric = null;
    this.bestMetric = null;
    this.eta = null;
    this.speed = null;

    this.lastLine = "";
    this.lastUpdate = null;
    this.lastInjectedText = "";
    this.linesSeen = 0;
    this.recentLines = [];
  }

  pushLine(line) {
    this.linesSeen += 1;
    this.lastLine = line;
    this.lastUpdate = nowIso();
    this.recentLines.push(line);
    if (this.recentLines.length > 50) this.recentLines.shift();
    this._parseLine(line);
  }

  _parseLine(line) {
    const rules = [
      { re: /\bEpoch\s*[:=\[]?\s*(\d+)\s*\/\s*(\d+)/i, kind: "epochPair" },
      { re: /\bepoch\s*[:=\[]?\s*(\d+)\s*\/\s*(\d+)/i, kind: "epochPair" },
      { re: /\bStep\s*[:=\[]?\s*(\d+)\s*\/\s*(\d+)/i, kind: "stepPair" },
      { re: /\bstep\s*[:=\[]?\s*(\d+)\s*\/\s*(\d+)/i, kind: "stepPair" },
      { re: /\bloss\b\s*[:=]\s*([0-9eE.+-]+)/i, kind: "loss" },
      { re: /\bloss\b\s+([0-9eE.+-]+)/i, kind: "loss" },
      { re: /\blr\b\s*[:=]\s*([0-9eE.+-]+)/i, kind: "lr" },
      { re: /\b(?:val[_\s-]?(?:score|metric|acc|accuracy|f1|auc))\b\s*[:=]\s*([0-9eE.+-]+)/i, kind: "valMetric" },
      { re: /\b(?:acc|accuracy|f1|auc)\b\s*[:=]\s*([0-9eE.+-]+)/i, kind: "valMetric" },
      { re: /\bbest(?:[_\s-]?(?:score|metric|acc|accuracy|f1|auc))?\b\s*[:=]\s*([0-9eE.+-]+)/i, kind: "bestMetric" },
      { re: /\bETA\b\s*[:=]?\s*([0-9dhms: ]+)/i, kind: "eta" },
      { re: /\b(?:speed|it\/s|samples\/s|img\/s)\b\s*[:=]?\s*([0-9eE.+/\- ]+)/i, kind: "speed" },
    ];

    for (const r of rules) {
      const m = line.match(r.re);
      if (!m) continue;

      switch (r.kind) {
        case "epochPair":
          this.epoch = safeNum(m[1]);
          this.maxEpoch = safeNum(m[2]);
          break;
        case "stepPair":
          this.step = safeNum(m[1]);
          this.maxStep = safeNum(m[2]);
          break;
        case "loss":
          this.loss = safeNum(m[1]);
          break;
        case "lr":
          this.lr = safeNum(m[1]);
          break;
        case "valMetric":
          this.valMetric = safeNum(m[1]);
          break;
        case "bestMetric":
          this.bestMetric = safeNum(m[1]);
          break;
        case "eta":
          this.eta = String(m[1]).trim();
          break;
        case "speed":
          this.speed = String(m[1]).trim();
          break;
      }
    }
  }

  progressPercent() {
    if (this.step != null && this.maxStep) {
      return Math.max(0, Math.min(100, Math.round((this.step / this.maxStep) * 100)));
    }
    if (this.epoch != null && this.maxEpoch) {
      return Math.max(0, Math.min(100, Math.round((this.epoch / this.maxEpoch) * 100)));
    }
    return null;
  }

  summaryText() {
    const pct = this.progressPercent();
    const rows = [];
    rows.push(`**${this.label} 进度更新**`);
    rows.push(`- 状态: ${this.state}`);
    if (pct != null) rows.push(`- 进度: ${pct}%`);
    if (this.epoch != null || this.maxEpoch != null) rows.push(`- Epoch: ${this.epoch ?? "-"} / ${this.maxEpoch ?? "-"}`);
    if (this.step != null || this.maxStep != null) rows.push(`- Step: ${this.step ?? "-"} / ${this.maxStep ?? "-"}`);
    if (this.loss != null) rows.push(`- Loss: ${this.loss}`);
    if (this.lr != null) rows.push(`- LR: ${this.lr}`);
    if (this.valMetric != null) rows.push(`- Val Metric: ${this.valMetric}`);
    if (this.bestMetric != null) rows.push(`- Best Metric: ${this.bestMetric}`);
    if (this.speed != null) rows.push(`- Speed: ${this.speed}`);
    if (this.eta != null) rows.push(`- ETA: ${this.eta}`);
    if (this.lastLine) rows.push(`- 最新日志: \`${truncate(this.lastLine, 160)}\``);
    return rows.join("\n");
  }

  finalText() {
    const rows = [];
    rows.push(`**${this.label} 已结束**`);
    rows.push(`- 状态: ${this.state}`);
    rows.push(`- 返回码: ${this.returnCode}`);
    if (this.epoch != null || this.maxEpoch != null) rows.push(`- Epoch: ${this.epoch ?? "-"} / ${this.maxEpoch ?? "-"}`);
    if (this.step != null || this.maxStep != null) rows.push(`- Step: ${this.step ?? "-"} / ${this.maxStep ?? "-"}`);
    if (this.loss != null) rows.push(`- Loss: ${this.loss}`);
    if (this.valMetric != null) rows.push(`- Val Metric: ${this.valMetric}`);
    if (this.bestMetric != null) rows.push(`- Best Metric: ${this.bestMetric}`);
    if (this.lastLine) rows.push(`- 最后一行日志: \`${truncate(this.lastLine, 200)}\``);
    return rows.join("\n");
  }
}

function truncate(s, n) {
  if (!s) return s;
  return s.length <= n ? s : s.slice(0, n - 3) + "...";
}

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function writeJson(file, obj) {
  fs.writeFileSync(file, JSON.stringify(obj, null, 2), "utf-8");
}

function writeText(file, text) {
  fs.writeFileSync(file, text, "utf-8");
}

function statusFiles(baseDir, label) {
  const safe = label.replace(/[^\w.-]+/g, "_");
  return {
    json: path.join(baseDir, `${safe}.status.json`),
    md: path.join(baseDir, `${safe}.status.md`),
    log: path.join(baseDir, `${safe}.stream.log`),
  };
}

function renderStatusMarkdown(state) {
  const lines = [];
  lines.push(`# ${state.label} 状态`);
  lines.push("");
  lines.push(`- 状态: **${state.state}**`);
  lines.push(`- 开始时间: \`${state.startedAt}\``);
  lines.push(`- 结束时间: \`${state.endedAt}\``);
  lines.push(`- PID: \`${state.pid}\``);
  lines.push(`- 返回码: \`${state.returnCode}\``);
  lines.push("");
  lines.push("## 指标");
  lines.push("");
  lines.push(`- Epoch: \`${state.epoch}\` / \`${state.maxEpoch}\``);
  lines.push(`- Step: \`${state.step}\` / \`${state.maxStep}\``);
  lines.push(`- Loss: \`${state.loss}\``);
  lines.push(`- LR: \`${state.lr}\``);
  lines.push(`- Val Metric: \`${state.valMetric}\``);
  lines.push(`- Best Metric: \`${state.bestMetric}\``);
  lines.push(`- ETA: \`${state.eta}\``);
  lines.push(`- Speed: \`${state.speed}\``);
  lines.push("");
  lines.push("## 最新日志");
  lines.push("");
  lines.push("```text");
  for (const l of state.recentLines.slice(-20)) lines.push(l);
  lines.push("```");
  lines.push("");
  return lines.join("\n");
}

function spawnOpenClawInject(session, message) {
  return new Promise((resolve) => {
    const payload = JSON.stringify({ sessionKey: session, message });
    const child = spawn(
      "openclaw",
      ["gateway", "call", "chat.inject", payload],
      {
        stdio: ["ignore", "pipe", "pipe"],
      }
    );

    let out = "";
    let err = "";

    child.stdout.on("data", (d) => (out += d.toString()));
    child.stderr.on("data", (d) => (err += d.toString()));

    child.on("close", (code) => {
      resolve({ code, out, err });
    });

    child.on("error", (e) => {
      resolve({ code: -1, out: "", err: String(e) });
    });
  });
}

async function periodicInject(state, session, intervalSec) {
  const text = state.summaryText();
  if (text !== state.lastInjectedText) {
    state.lastInjectedText = text;
    await spawnOpenClawInject(session, text);
  }
  await sleep(intervalSec * 1000);
}

async function runMode(args) {
  const session = args["session"] || "main";
  const label = args["label"] || "task";
  const cwd = args["cwd"] || process.cwd();
  const cmd = args["cmd"];
  const intervalSec = Number(args["interval-sec"] || 20);
  const outDir = args["out-dir"] || path.join(cwd, "runs", "task-progress-stream");

  if (!cmd) {
    console.error("missing --cmd");
    process.exit(2);
  }

  ensureDir(outDir);
  const files = statusFiles(outDir, label);
  const state = new ProgressState(label);
  state.state = "starting";
  state.startedAt = nowIso();

  const logStream = fs.createWriteStream(files.log, { flags: "a" });

  const child = spawn("/bin/bash", ["-lc", cmd], {
    cwd,
    stdio: ["ignore", "pipe", "pipe"],
    detached: true,
  });

  state.pid = child.pid;
  state.state = "running";

  function flushState() {
    writeJson(files.json, state);
    writeText(files.md, renderStatusMarkdown(state));
  }

  function onLine(line) {
    state.pushLine(line);
    logStream.write(line + "\n");
    flushState();
  }

  function wire(stream) {
    let buf = "";
    stream.on("data", (d) => {
      buf += d.toString();
      const parts = buf.split(/\r?\n/);
      buf = parts.pop() || "";
      for (const p of parts) onLine(p);
    });
    stream.on("end", () => {
      if (buf) onLine(buf);
    });
  }

  wire(child.stdout);
  wire(child.stderr);

  let finished = false;

  child.on("close", async (code) => {
    finished = true;
    state.returnCode = code;
    state.endedAt = nowIso();
    state.state = code === 0 ? "finished" : "failed";
    flushState();
    await spawnOpenClawInject(session, state.finalText());
    logStream.end();
  });

  process.on("SIGINT", () => {
    try {
      process.kill(-child.pid, "SIGTERM");
    } catch {}
    process.exit(130);
  });

  process.on("SIGTERM", () => {
    try {
      process.kill(-child.pid, "SIGTERM");
    } catch {}
    process.exit(143);
  });

  while (!finished) {
    flushState();
    await periodicInject(state, session, intervalSec);
  }
}

async function tailMode(args) {
  const session = args["session"] || "main";
  const label = args["label"] || "task";
  const file = args["file"];
  const intervalSec = Number(args["interval-sec"] || 20);
  const outDir = args["out-dir"] || path.join(process.cwd(), "runs", "task-progress-stream");

  if (!file) {
    console.error("missing --file");
    process.exit(2);
  }

  ensureDir(outDir);
  const files = statusFiles(outDir, label);
  const state = new ProgressState(label);
  state.state = "tailing";
  state.startedAt = nowIso();

  let position = 0;
  if (fs.existsSync(file)) {
    position = fs.statSync(file).size;
  }

  function flushState() {
    writeJson(files.json, state);
    writeText(files.md, renderStatusMarkdown(state));
  }

  while (true) {
    try {
      if (fs.existsSync(file)) {
        const stat = fs.statSync(file);
        if (stat.size < position) {
          position = 0;
        }
        if (stat.size > position) {
          const fd = fs.openSync(file, "r");
          const len = stat.size - position;
          const buf = Buffer.alloc(len);
          fs.readSync(fd, buf, 0, len, position);
          fs.closeSync(fd);
          position = stat.size;

          const text = buf.toString("utf-8");
          for (const line of text.split(/\r?\n/)) {
            if (line.trim()) state.pushLine(line);
          }
          flushState();
        }
      }

      await periodicInject(state, session, intervalSec);
    } catch (e) {
      state.pushLine(`[tail-error] ${String(e)}`);
      flushState();
      await sleep(intervalSec * 1000);
    }
  }
}

async function main() {
  const args = parseArgs(process.argv);
  const mode = args._[0];

  if (!mode || !["run", "tail"].includes(mode)) {
    console.log(`
task-progress-stream

Usage:

  node task_progress_stream.js run \\
    --session main \\
    --label train \\
    --cwd /path/to/project \\
    --cmd "python src/train.py --config configs/train.yaml" \\
    --interval-sec 20

  node task_progress_stream.js tail \\
    --session main \\
    --label train \\
    --file /path/to/train.log \\
    --interval-sec 20
`);
    process.exit(1);
  }

  if (mode === "run") {
    await runMode(args);
  } else if (mode === "tail") {
    await tailMode(args);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
