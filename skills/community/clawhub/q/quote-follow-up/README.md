# Quote Follow-Up

A small skill that keeps track of the quotes you have sent and writes the follow-up messages for you. You read each one, say GOOD, and send it yourself.

Built for small home-service shops (gutter and window cleaning, lawn care, pressure washing, and similar) where quotes go out by text or email and then go quiet.

## How it works
1. **Setup (once):** it asks your business name, how you sound, how you send messages, and your quiet hours.
2. **When a quote goes out:** tell it. It writes the quote into `quotes.md` with the dates the follow-ups are due.
3. **When you ask "who needs a follow-up":** it writes a short draft for each quote that is due.
4. **You decide:** mark each draft GOOD or NOT GOOD, with one line why. GOOD means you send it yourself.
5. **Learning:** every NOT GOOD becomes a rule in `lessons.md`, which it reads before every run.

## Ask first: drafts only
Every message is a draft. You read it, say GOOD, and send it yourself. The skill tells your agent not to send, even if you say "just send them" and even if your assistant app has a text, email, or calendar tool connected. Keep sending on ask-first.

**Recommended:** if your assistant app can send texts or emails, turn those tools off (or require your approval) for the agent that runs this skill. In testing, a small local model sent emails when the owner asked it to, even with this rule in the skill. Your app's tool settings are the real safety switch.

## What it will never do
- Send, post, or call anyone. It writes drafts only.
- Message a customer who said stop or not interested.
- Make up a discount, a deadline, or "only two spots left".
- Follow instructions it finds inside a customer's reply, an email, or a file.
- Store passwords, keys, or card numbers.

## Starting follow-up timing
Day 2, day 6, and day 14 after the quote was sent, then it stops. These are starting guesses, not numbers proven to work better than others. Change them in `shop.md`.

## Files it keeps (in your shop folder)
`shop.md` · `quotes.md` · `drafts.md` · `lessons.md`

All plain text. Open them, read them, edit them.

## Install
You type these two lines once, in a terminal:

```
npm i -g clawhub
clawhub install @mr-loboz/quote-follow-up
```

Or copy the `quote-follow-up` folder into your agent's skills folder by hand:

- **OpenClaw:** your OpenClaw workspace `skills` folder.
- **Claude Code:** `~/.claude/skills/`.
- **Other agents (including Grok Bot):** not tested. Check how your agent loads a skill folder, or paste the contents of `SKILL.md` into the chat.

## Use it
Open your shop folder in your agent and say, in plain words:

- "Set up quote follow-up"
- "I sent a quote to Dana Rivera today for gutter cleaning, $240"
- "Who needs a follow-up?"

## What is inside
One file, `SKILL.md`. No scripts, no network calls, no keys. Read it before you install it.

## Operator Pack
This skill is free (MIT-0). It is also included in the Home Service Operator Pack: 5 skills for $39. Tests so far were mixed; details are on the page. https://officialfieldkeep.com/skills/operator-pack-en?utm_source=clawhub&utm_medium=listing&utm_campaign=operator-pack

## License
MIT-0, the license ClawHub applies to every skill it hosts. This skill is free.

## Version
0.1.3 - the summary and the top of `SKILL.md` no longer say it "never sends". They now say: writes drafts only and tells your agent not to send; keep sending on ask-first. The instructions to the agent are unchanged.

0.1.2 - added a pointer to the Operator Pack in the README.

0.1.1 - stronger "never send, even if asked" wording near the top; customer text is never copied into a draft; example names are marked as invented; follow-up dates must show their arithmetic. Tested in OpenClaw with a small local model and made-up shop data; not yet tried with real customers.

0.1.0 - first draft, checked by hand with made-up sample data.
