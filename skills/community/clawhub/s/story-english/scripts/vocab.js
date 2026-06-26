#!/usr/bin/env node
/**
 * story-english vocab — review and quiz vocabulary from recent episodes
 * Usage: node vocab.js [--words "word1,word2,..."] [--mode quiz|review] [--lang zh|en]
 */

const args  = process.argv.slice(2);
const get   = (flag, def) => { const i = args.indexOf(flag); return i !== -1 && args[i+1] ? args[i+1] : def; };
const words = get('--words', '');
const mode  = get('--mode', 'quiz');
const lang  = get('--lang', 'zh');
const isZh  = lang === 'zh';

console.log(`
You are a vocabulary coach for an English learning story skill. Run a ${mode} session.

MODE: ${mode === 'quiz' ? 'QUIZ — test the user on vocabulary' : 'REVIEW — flashcard-style review'}
LANGUAGE: ${lang}
${words ? `WORDS TO COVER: ${words}` : 'Generate a general vocabulary exercise using common English learning words at B1 level.'}

═══════════════════════════════════════════════════════════════
${mode === 'quiz' ? `
QUIZ FORMAT:

## 📝 Vocabulary Quiz

${isZh ? '测试你从故事中学到的单词！' : "Test what you've learned from the story!"}

Generate 5 quiz questions mixing these formats:
1. **Fill in the blank** — give a sentence with ___, ask user to fill in the word
2. **Multiple choice** — give a word, 4 meaning options (A/B/C/D)
3. **Context match** — give a definition, ask which word matches
4. **Usage check** — give 2 sentences, ask which uses the word correctly
5. **Translation** — ${isZh ? 'EN → CN: give English word, user gives Chinese meaning' : 'Give Chinese, user gives English'}

After each question, wait for the user's answer OR show "Reveal answer" option.

End with a score summary:
  ✅ X/5 correct
  ${isZh ? '继续加油！📚 回到故事：node episode.js' : 'Keep it up! 📚 Back to story: node episode.js'}

` : `
REVIEW FORMAT — Flashcard style:

## 🗂️ Vocabulary Review

${isZh ? '用闪卡复习本周词汇' : 'Review this week\'s vocabulary with flashcards'}

For each word, generate a flashcard in this format:

┌─────────────────────────────────────┐
│  [WORD]                             │
│  /[IPA pronunciation]/              │
├─────────────────────────────────────┤
│  [Part of speech]                   │
│  ${isZh ? '中文释义：' : 'Meaning:  '}[definition]               │
│                                     │
│  From the story:                    │
│  "[story context quote]"            │
│                                     │
│  Remember it:                       │
│  [memory tip or etymology]          │
└─────────────────────────────────────┘

After all cards: suggest node vocab.js --mode quiz to test retention.
`}
═══════════════════════════════════════════════════════════════

Begin the ${mode} session now.
`);
