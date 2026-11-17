# Scale Readiness Checker

Turn Your App Into a Plan That Can Grow From 5 Users to 5,000 Users, in Plain Words

Upload your app. Answer a few questions. Get the full plan to grow it without it slowing down or crashing.

Most apps work fine with 5 users, then slow down or crash when more people join. The database has to search every row, the same data is fetched again and again, and no one tested what happens with 1,000 users at once. This skill checks first, then makes a scale plan for your app only, with draft fixes for owner review, never a live change by itself.

## What you get

- A scale readiness check on 4 points: database indexing, caching, load testing, and hosting that can grow
- A scale plan, labelled DRAFT, NOT LIVE: index list, caching plan, load test plan, and hosting plan
- A clear answer on what will break first, in plain words, with evidence
- A missing checks list at the end, so nothing is hidden

## Who this is for

Founders with no code, who want to know if their app can grow, and what to fix first, in plain words. Small business owners with an app that is getting more users. Freelancers and builders who need a clear scale plan to hand to a developer.

## Why this saves money

Fixing scale early is cheaper than fixing a crash later. A clear plan stops the builder from guessing, rebuilding the database, or buying a bigger server you do not need yet.

## Technical, for coders

Structured scale plan with database index list, caching plan with keys and expiry, load test plan with user levels and breaking point, and hosting plan with scaling notes, ready to brief Claude, Cursor, or any AI builder, or a human developer. No guarantee of a user number, and no claim that a plan alone makes an app scale. The plan is a draft for owner review, not a live change.

## The 4 checks

1. Database indexing, like a book index, so the database finds rows fast
2. Caching, so data used often is not fetched from the database every time
3. Load testing, with many fake users, to find where it breaks first
4. Hosting that can grow, without a full rebuild

It also gives separate notes: slow pages, heavy work that should run in the background, cost as users grow, and mobile use.

## How to use it

1. Install the skill in your AI agent (see below).
2. Give your agent your app idea, your app code, or your app link.
3. Answer, in plain words: what does it do, how many users today, how many users do you want, what do users do most, where is your data, where is it hosted?
4. Ask: "Check my app with scale-readiness-checker."
5. Read the plan. Approve the draft fixes first, before any index is made, any caching is set up, or any load test is run.

## What it will not do

- It will not change code, change the database, set up caching, run a load test on real users, move hosting, or deploy anything by itself.
- It will not invent a user number, a speed, a cost, a table, an index, or a test result.
- It will not claim your app can handle 5,000 users unless a load test proved it.
- A scale plan is not a promise of growth, users, or money.

## How to install it

Works with any AI agent that can read a SKILL.md file, including Claude, Copilot, Cursor, Gemini, ChatGPT, DeepSeek, Hermes, OpenClaw and other AI tools.

Copy the `SKILL.md` file into your skills folder, in a folder called `scale-readiness-checker`, then restart your agent. The skill file itself is just instructions. It collects no data and sends nothing anywhere.

## Files

- `SKILL.md` - the full skill: instructions, checklist, hard rules, and plan format.

## License

MIT - free to use and adapt. If you improve it, a credit is appreciated but not required.
