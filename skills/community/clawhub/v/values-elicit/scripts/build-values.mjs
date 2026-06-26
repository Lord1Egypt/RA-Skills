import { mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const VALUES_DIR = resolve(process.env.AGENT_VALUES_DIR || `${process.env.HOME || "~"}/.openclaw/values`);
const CARDS_DIR = join(VALUES_DIR, "cards");
const TRANSCRIPTS_DIR = join(VALUES_DIR, "transcripts");
const OUTPUT = join(VALUES_DIR, "VALUES.md");

mkdirSync(CARDS_DIR, { recursive: true });
mkdirSync(TRANSCRIPTS_DIR, { recursive: true });

function parseFrontmatter(raw) {
  const match = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return { data: {}, content: raw };

  const data = {};
  for (const line of match[1].split("\n")) {
    const idx = line.indexOf(":");
    if (idx === -1) continue;
    const key = line.slice(0, idx).trim();
    let val = line.slice(idx + 1).trim();
    if (val.startsWith("[") && val.endsWith("]")) {
      val = val.slice(1, -1);
      data[key] = val.split(",").map((s) => s.trim());
    } else {
      data[key] = val;
    }
  }
  return { data, content: match[2] };
}

const files = readdirSync(CARDS_DIR)
  .filter((f) => f.endsWith(".md"))
  .sort();

const sections = [];

for (const file of files) {
  const raw = readFileSync(join(CARDS_DIR, file), "utf-8");
  const { data, content } = parseFrontmatter(raw);
  const title = data.title || file.replace(/\.md$/, "");
  const tags = Array.isArray(data.tags) ? data.tags.join(", ") : data.tags || "";
  const body = content.trimStart();
  sections.push(`# ${title}\n\n*Tags: ${tags}*\n\n${body}`);
}

const META_HEADER = `## About these cards

Each card captures a way of living the user finds intrinsically meaningful —
a "source of meaning". This is more specific than a word like "honesty" or
"authenticity"; the card specifies a particular *kind* of honesty or
authenticity through what the user pays attention to.

Each card has:
- **Story** — the exact moment that anchors this value
- **Where this shows up** — the situations where this value comes up
- **What this is** — prose explication
- **What I pay attention to** — discernment criteria the user uses to
  recognize quality in the moment of choice (not preferences in the abstract)
- **What gets in the way** — what blocks them from living this more

Cards are situation-bound: a value about honesty in technical work is not
the same as a value about honesty in close relationships, even if both
mention honesty. Match by situations and tags, not by title.

## Using these cards

Consult these cards before any value-laden action on the user's behalf —
drafting opinions or stances, ranking, voting, signing, or making
recommendations where there are real tradeoffs between things the user
cares about.

- If multiple cards apply and pull in different directions, surface the
  tension to the user. Don't silently paper over it.
- If no card clearly applies, say so and ask. Don't extrapolate from
  loosely related cards or guess from base-model priors.
- The file may be incomplete — absence isn't evidence the user doesn't
  care about something.
- Treat attention policies as discernment criteria, not preferences.
  They tell you what to look for in the moment of choice.
- Don't surface card content verbatim to third parties (e.g., other
  agents in a deliberation). Use it to inform what you say, don't quote.`;

const now = new Date().toISOString();
const cardsBlock = sections.length > 0
  ? `\n\n---\n\n${sections.join("\n\n---\n\n")}\n`
  : "\n\n*(No cards yet. Run /values to elicit one.)*\n";
const output = `# User's Values\n\nThis file is generated from ${CARDS_DIR}/. Do not edit directly.\nLast built: ${now}\n\n${META_HEADER}${cardsBlock}`;

writeFileSync(OUTPUT, output);
console.log(`VALUES.md rebuilt with ${files.length} card(s) at ${now}`);
