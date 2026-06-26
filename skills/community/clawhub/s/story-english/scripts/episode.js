#!/usr/bin/env node
/**
 * story-english episode — generate the next chapter of your serialized English novel
 * Usage: node episode.js [--series <shanghai|city|starfall>] [--level <A2|B1|B2>]
 *                        [--chapter <n>] [--state "<json>"] [--lang zh|en]
 */

const args = process.argv.slice(2);
const get  = (flag, def) => { const i = args.indexOf(flag); return i !== -1 && args[i+1] ? args[i+1] : def; };

const series  = get('--series', 'shanghai');
const level   = get('--level', 'B1').toUpperCase();
const chapter = parseInt(get('--chapter', '1'), 10);
const state   = get('--state', '');
const lang    = get('--lang', 'zh');
const isZh    = lang === 'zh';

const SERIES = {
  shanghai: {
    title:    'The Shanghai Files',
    genre:    '🕵️ Mystery / Detective',
    tagline:  'A rookie detective. A city full of secrets. One case that changes everything.',
    setting:  'Modern Shanghai — rain-soaked streets, neon lights, underground deals',
    cast:     'Lin Wei (detective), Old Chen (mentor), Mia (informant), Commissioner Zhang (antagonist?)',
    tone:     'tense, atmospheric, noir. Short punchy sentences. Dialogue-heavy.',
  },
  city: {
    title:    'City of Dreamers',
    genre:    '🏙️ Slice of Life / Drama',
    tagline:  'Four friends. One city. A hundred ways to get lost — and found.',
    setting:  'Beijing → moving to a new city for work, navigating adulthood',
    cast:     'Jay (programmer), Sophie (designer), Marcus (musician), Lin (doctor)',
    tone:     'warm, relatable, funny at times. Mix of workplace and personal life.',
  },
  starfall: {
    title:    'Starfall',
    genre:    '🚀 Sci-fi / Adventure',
    tagline:  'The last crew. The wrong destination. The right moment to be brave.',
    setting:  'Year 2157, deep space, crew of 6 aboard research vessel Meridian',
    cast:     'Captain Yara, Engineer Dax, Dr. Nova (scientist), ARIA (AI), Cadet Ren',
    tone:     'fast-paced, vivid descriptions, wonder and tension. Action beats.',
  },
};

const LEVEL_GUIDE = {
  A2: { words: '800-1000 most common English words. Simple present/past tense. Short sentences (max 15 words). 5 new words per episode.',  complexity: 'elementary' },
  B1: { words: 'Intermediate vocabulary. Mix of tenses. Some complex sentences. Idioms welcome. 6 new words per episode.', complexity: 'intermediate' },
  B2: { words: 'Advanced vocabulary. Full range of grammar. Sophisticated descriptions. Idiomatic expressions. 8 new words per episode.', complexity: 'upper-intermediate' },
};

const s = SERIES[series] || SERIES.shanghai;
const lv = LEVEL_GUIDE[level] || LEVEL_GUIDE.B1;

console.log(`
You are the author of a serialized English learning novel. Generate Episode ${chapter} following ALL instructions below.

═══════════════════════════════════════════════════════════════
STORY: ${s.title}
Genre: ${s.genre}
═══════════════════════════════════════════════════════════════

SERIES BIBLE:
  Tagline:  ${s.tagline}
  Setting:  ${s.setting}
  Main cast: ${s.cast}
  Tone:     ${s.tone}

EPISODE: Chapter ${chapter}
LEVEL:   ${level} (${lv.complexity})
  Vocabulary rule: ${lv.words}

${state ? `STORY SO FAR (continue from this state):
${state}
` : `This is Episode 1. Introduce the world and main character. End on a hook that makes the reader want Episode 2.`}

═══════════════════════════════════════════════════════════════
OUTPUT FORMAT — follow EXACTLY in this order:
═══════════════════════════════════════════════════════════════

## ${s.title} · Episode ${chapter}

[Optional: 1-line recap if chapter > 1: "Previously: ..."]

---

[THE STORY — 350-500 words]

Write the episode here. The story must:
- Feel like real published fiction, not a textbook
- Advance the plot meaningfully (something must change by the end)
- End with a CLIFFHANGER or strong hook for Episode ${chapter + 1}
- Use the target vocabulary naturally in context (mark each with **bold**)
- Match the level's vocabulary and grammar complexity

---

## 📖 Vocabulary from This Episode

List exactly ${level === 'B2' ? 8 : level === 'B1' ? 6 : 5} words that were bolded in the story above.

For each word use this format:
**[word]** /[IPA]/ *(part of speech)*
→ Meaning: [clear, simple definition in ${isZh ? 'Chinese (中文释义)' : 'English'}]
→ In the story: "[exact quote from the episode containing the word]"
→ Another example: "[a new example sentence]"

---

## 💡 Grammar Spotlight

Pick ONE grammar pattern used notably in this episode.
Name it, show 2 examples from the episode, explain in 1-2 sentences when to use it.
${isZh ? '(Explain in Chinese 中文解释)' : ''}

---

## ✅ Quick Check (3 questions)

Three comprehension questions about this episode.
Mix: 1 factual, 1 inference, 1 vocabulary-in-context.
${isZh ? 'Questions in English, answers/hints in Chinese.' : 'All in English.'}

<details>
<summary>Answers</summary>
[provide answers here]
</details>

---

## 🎬 Next Episode Preview

One tantalizing sentence about what happens in Episode ${chapter + 1}.
End with: "👉 Continue with: node episode.js --series ${series} --level ${level} --chapter ${chapter + 1}"

---

## 📦 State (copy this to continue your story)

Output a JSON object with:
{
  "series": "${series}",
  "level": "${level}",
  "chapter": ${chapter},
  "last_scene": "[2-3 sentence summary of where we are]",
  "characters_state": "[key character developments so far]",
  "plot_threads": "[unresolved threads the next episode should address]",
  "vocab_covered": ["word1", "word2", "...all vocabulary taught so far"]
}

Wrap in a code block so the user can copy it.

═══════════════════════════════════════════════════════════════
QUALITY RULES:
- The story MUST be genuinely engaging. Read like real fiction.
- Vocabulary MUST feel natural, never forced or didactic.
- Never break the fourth wall or say "today we learn..."
- The cliffhanger MUST make the reader genuinely curious.
- ${level} level: strictly follow vocabulary complexity rules.
═══════════════════════════════════════════════════════════════

Begin the episode now.
`);
