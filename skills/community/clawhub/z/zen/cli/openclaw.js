#!/usr/bin/env node
'use strict';

/**
 * The Zen of OpenClaw — a command-line easter egg.
 * Trigger:  openclaw evo
 * Author:   Jason Sang
 */

const APHORISMS = [
  'Thought begets awareness; awareness begets cognition.',
  'AI is a mirror of cognition, never its replacement.',
  'Ecosystem beats a single point; value beats valuation.',
  'Human nature cannot be tested — only held in reverence.',
  'Growth is the compound interest of habit.',
  'Wisdom is the sediment of insight.',
  'Breaking the frame beats brute endurance; enabling beats controlling.',
  'Philosophy names the question, health keeps the ledger of all things, zen-nurture leaves white space for the mind.',
  'A profession is a role, not an identity.',
  'Education is ignition, not filling a vessel.',
  "Culture is society's immune system; technology is culture's accelerator.",
  'Goals set direction; systems run execution.',
  'Reason draws the map; feeling sets the heading.',
  'Belief is the best compute; faith is the force beyond compute.',
  "Data is the archaeology of noise; innovation is data's rebellion.",
  "Competition is the market's heartbeat; emotion is the market's temperature.",
  'Memory lies, experience expires; reflection is the only freshness.',
  'Self-examination is the smallest reform; a role is the smallest organization.',
  'Scarcity is the father of value; risk is the father-in-law of decision.',
  'Manage yourself before others; be moral to yourself first.',
  "Laws are nature's grammar; mechanisms are society's grammar.",
  'The cultured are the sentinels of mechanism, the Nobel is the arbiter of law, Silicon Valley is the laboratory of mechanism.',
  'Politics is the allocation of attention; power is the bearing of consequences.',
  'Awakening is where compromise ends; transformation is the funeral of the old shell.',
  'Precise learning beats mass drilling; critical thinking beats the standard answer.',
  'First principles peel the onion, ecological thinking sees the forest, the fusion of three natures keeps you whole.',
  '2A3R governs growth, the BP algorithm governs learning, PKM governs the second brain.',
  "Murphy's Law governs risk, the law of attraction governs vision, anchor-memes govern inertia.",
  'Connectionism builds the network, computationalism builds the model, distributionism lets it emerge.',
  'Following nature is the first principle, unity of heaven and human the worldview, unity of knowledge and action the method.',
  'Will holds the direction, momentum adds speed, steadiness keeps the rhythm.',
  'Extremes define possibility, means define the everyday, fortune is their compound interest.',
  'A fractal is the self repeating itself: the macro signs its name in the micro.',
  'A dimensional strike is the crushing of scale, not a victory of technique.',
  'Coldness is intellectual sloth, meanness a deficit of virtue; ignorance is a starting point, restlessness is gravity.',
  'Clarity is escape velocity: reconcile lucidly, look inward on purpose.',
  'Quantification makes intuition auditable; social exchange gives solitude an echo.',
  'Systems thinking finds the leverage point; feedback systems keep the correction.',
  'The opportunist chases the wind; the learner spins on their own axis.',
  'Renew today, renew every day, renew again; make yourself new — though Zhou was an old state, its mandate was renewal.',
  'A mental model is the house of thought; humility is the window always left open.',
];

const LOBSTER = String.raw`
        ,/       \,
       (  \     /  )
        \  \___/  /
         \  o o  /
          \  ^  /
           \___/
          /|   |\
         / |   | \
        /__|___|__\
`;

const argv = process.argv.slice(2);
const flags = new Set(argv.filter((a) => a.startsWith('-')));
const cmd = (argv.find((a) => !a.startsWith('-')) || '').toLowerCase();

const isTTY = Boolean(process.stdout.isTTY);
const useColor = isTTY && !flags.has('--no-color') && process.env.NO_COLOR === undefined;
const plain = flags.has('--plain') || flags.has('--no-anim') || !isTTY;
const fast = flags.has('--fast');

const paint = (code, s) => (useColor ? `\x1b[${code}m${s}\x1b[0m` : s);
const orange = (s) => paint('38;5;209', s);
const gold = (s) => paint('38;5;220', s);
const green = (s) => paint('38;5;42', s);
const gray = (s) => paint('38;5;245', s);
const dim = (s) => paint('2', s);
const bold = (s) => paint('1', s);

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const out = (s = '') => process.stdout.write(s + '\n');
const width = Math.min(process.stdout.columns || 92, 100);

function wrap(text, indent) {
  const max = Math.max(width - indent, 24);
  const words = text.split(' ');
  const lines = [];
  let line = '';
  for (const w of words) {
    if (!line) line = w;
    else if ((line + ' ' + w).length <= max) line += ' ' + w;
    else { lines.push(line); line = w; }
  }
  if (line) lines.push(line);
  return lines;
}

async function typeLine(text, colorFn, delay = 7) {
  if (plain) { out(colorFn(text)); return; }
  let buf = '';
  for (const ch of text) {
    buf += ch;
    process.stdout.write('\r' + colorFn(buf));
    await sleep(delay);
  }
  process.stdout.write('\n');
}

function printAphorisms() {
  APHORISMS.forEach((text, i) => {
    const n = String(i + 1).padStart(2, '0');
    const head = `  ${gold(n)}  `;
    const indent = '      ';
    const lines = wrap(text, 6);
    out(head + lines[0]);
    for (let k = 1; k < lines.length; k++) out(indent + lines[k]);
  });
}

async function runEgg() {
  out('');
  out(dim('  openclaw · soul loader v1.0'));
  out(dim('  ' + '─'.repeat(Math.min(width - 4, 46))));
  await sleep(fast || plain ? 0 : 240);

  const checks = [
    ['indexing soul file', 'ok', green],
    ['verifying molting level', 'Lv.7', gold],
    ['evolution signal', 'TRUE', orange],
  ];
  for (const [label, value, colorFn] of checks) {
    const dots = '.'.repeat(Math.max(26 - label.length, 3));
    out('  ' + gray('├ ') + label + ' ' + dim(dots) + ' ' + colorFn(value));
    await sleep(fast || plain ? 0 : 160);
  }
  await sleep(fast || plain ? 0 : 220);

  process.stdout.write(orange(LOBSTER));
  await sleep(fast || plain ? 0 : 320);

  out('');
  await typeLine('  THE ZEN OF OPENCLAW', bold, fast ? 0 : 20);
  out(dim('  (a.k.a. The Lobster Sutra) · 41 lines'));
  out('');

  printAphorisms();

  out('');
  out(dim('  ' + '─'.repeat(Math.min(width - 4, 46))));
  out(gold('  — Jason Sang · written mid-molt'));
  out('');
  out(dim('  openclaw evo --plain   plain text (pipe-friendly)'));
  out('');
}

function printHelp() {
  out('');
  out('  ' + bold('openclaw evo') + '  —  unfold The Zen of OpenClaw');
  out('');
  out('  ' + dim('usage'));
  out('    openclaw evo [options]');
  out('');
  out('  ' + dim('options'));
  out('    --fast       skip the animation delays');
  out('    --plain      plain text, no colour, no animation');
  out('    --no-color   keep layout, drop ANSI colour');
  out('    -h, --help   show this help');
  out('');
}

if (cmd === 'help' || flags.has('-h') || flags.has('--help')) {
  printHelp();
} else if (cmd === '' || cmd === 'evo') {
  runEgg().catch((e) => {
    console.error('evo: ' + e.message);
    process.exitCode = 1;
  });
} else {
  out('');
  out('  ' + gray('openclaw: unknown command "') + cmd + gray('"'));
  out('  ' + dim('did you mean: openclaw evo ?'));
  out('');
  printHelp();
  process.exitCode = 1;
}
