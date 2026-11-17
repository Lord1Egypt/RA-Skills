---
name: scale-readiness-checker
description: "Turn your app into a plan that can grow from 5 users to 5,000 users, in plain words. Upload your app idea or your app code, answer a few questions, and get a full scale readiness check, with a database index list, a caching plan, a load test plan, and a hosting plan, for any AI agent. Structured scale plan with database indexing, caching, load testing, and hosting, ready to brief Claude, Cursor, or any AI builder, or a human developer."
---

# Scale Readiness Checker

## Headline

Turn Your App Into a Plan That Can Grow From 5 Users to 5,000 Users, in Plain Words

## Hook

Upload your app. Answer a few questions. Get the full plan to grow it without it slowing down or crashing.

## Pain, in plain words

Most apps work fine with 5 users, then slow down or crash when more people join. The database has to search every row, the same data is fetched again and again, and no one tested what happens with 1,000 users at once. The fix is not a bigger server first. The fix is a plan: index the data, cache what is used often, test the load, and host it where it can grow.

## What you get

A scale readiness check, then a scale plan, made for your app only. The check finds what will break first. The plan gives you draft fixes to review, never a live change by itself.

## Who this is for

Founders with no code, who want to know if their app can grow, and what to fix first, in plain words. Small business owners with an app or a web app that is getting more users. Freelancers and builders who need a clear scale plan to hand to a developer, with indexing, caching, load testing, and hosting in it.

## Why this saves money

Fixing scale early is cheaper than fixing a crash later. A clear plan stops the builder from guessing, rebuilding the database, or buying a bigger server you do not need yet.

## Technical, for coders

Structured scale plan with database index list, caching plan with keys and expiry, load test plan with user levels and breaking point, and hosting plan with scaling notes, ready to brief Claude, Cursor, or any AI builder, or a human developer. No guarantee of a user number, and no claim that a plan alone makes an app scale. The plan is a draft for owner review, not a live change.

## Purpose

Check if an app is ready to grow from a few users to many users, then make a scale plan for it. The skill checks first, then plans. It does not change code, change the database, run a live load test on real users, or deploy anything by itself.

## How to use it

Step 1: ask the user these questions, one at a time, in plain words.
Step 2: check the app against the 4 scale checks below.
Step 3: write the scale plan, labelled DRAFT, NOT LIVE, with draft fixes for the gaps found.
Step 4: run the missing checks at the end, and list what is complete, missing, or not confirmed.

Ask these questions first, one at a time:
1. What does your app do, in plain words?
2. Who uses it now, and how many users do you have today?
3. How many users do you want it to handle, and by when?
4. What does a user do most often in the app, in order?
5. Where is your data stored now, for example Supabase, Firebase, a database, or other?
6. Where is your app hosted now, for example Netlify, Vercel, or other?
7. What is slow now, if anything, and when does it feel slow?
8. What must NOT break, even when many users join at once?
9. Do you have real user numbers, or are the user numbers a target only?
10. Who will do the fixes, an AI builder, a human developer, or you with help?

If the user does not know an answer, mark it Not confirmed, and use the most common answer for their app type, and say so. Do not invent an answer.

## The 4 scale checks

Check all 4, in order. For each check, record evidence: the file, the table, the query, the setting, or the user answer where you saw it. No evidence means no Pass.

### 1. Database indexing
- The most used queries have an index, like a book index, so the database finds rows fast instead of reading every row.
- List the top 5 queries by use, in plain words, and say for each one if it has an index or not.
- Fail if a top query has no index, or if the same query is slow with more rows.
- Draft fix: an index list, with table name, column name, and why that index helps, for owner review. Do not create an index by yourself.

### 2. Caching
- Data that is used often, and changes rarely, is cached, so it is not fetched from the database every time.
- List what is cached now, what should be cached, and for how long, in plain words.
- Fail if the same data is fetched on every page load, with no cache, or if cached data is never cleared when it changes.
- Draft fix: a caching plan, with cache key, what it holds, how long it lives, and when it clears, for owner review. Name the cache tool only if the user already uses one, for example Redis, or say Suggested, not confirmed. Do not set up caching by yourself.

### 3. Load testing
- The app has been tested with many fake users, to find where it breaks first, before real users find it.
- List the user levels tested, for example 50, 500, and 5,000 users at once, and the result for each level.
- Fail if no load test was done, or if the test only used 5 users, or if the breaking point is unknown.
- Draft fix: a load test plan, with user levels, what each test does, what to watch, and what counts as a pass, for owner review. Do not run a load test on real users, and do not run it on a live app unless the user says you may.

### 4. Hosting that can grow
- The hosting can grow when users grow, without a full rebuild.
- List the current hosting, and say if it scales on its own, or if it needs manual work to grow.
- Fail if the hosting is a single small server with no plan to grow, or if a traffic spike would stop the app.
- Draft fix: a hosting plan, with current hosting, what to change, and what stays the same, for owner review. Prefer simple hosting that scales on its own, for example Vercel or Netlify, over complex setups like Kubernetes or Azure, unless the user already uses a complex setup and wants to keep it. Do not move hosting by yourself.

## Extra checks

These are not part of the 4 checks above, but report them separately as Notes. Do not mix them into the 4 point score.
- Slow pages: list the slowest page, and what makes it slow, in plain words.
- Heavy work: list work that should run in the background, for example sending many emails, or making many files, instead of blocking the user.
- Cost: list what will cost more as users grow, for example database reads, or hosting, in plain words, with no invented price.
- Mobile: say if the app is used on a phone, and if the slow parts are worse on a phone.

## Hard rules

- Never mark Pass without evidence.
- Never invent a user number, a speed, a cost, a database table, an index, a cache key, or a test result.
- Never claim the app can handle 5,000 users, or any number, unless a load test proved it. Say clearly what was tested, and what was not tested.
- Never create an index, set up caching, run a load test on live users, move hosting, or deploy anything, without a separate approval from the owner.
- Suggested items must be marked Suggested, not confirmed.
- A scale plan is not a promise of growth, users, or money.
- Keep the plan in plain, short sentences. The owner may not be a technical reader.

## Scale plan format

Always finish with this format, in this order, labelled DRAFT, NOT LIVE, Owner approval needed:

### Scale plan: [app name]
### Users today: [number or Not confirmed] | Target users: [number or Not confirmed] | Main use: [plain words]

**Verdict: Ready to grow / Needs fixes first / Not ready to grow**

Use Ready to grow only if there is no Fail in the 4 checks. Otherwise use Needs fixes first, or Not ready to grow if a blocker was found.

**Results**

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Database indexing | Pass / Fail / Not confirmed | table, query, or file |
| 2 | Caching | Pass / Fail / Not confirmed | what is cached now |
| 3 | Load testing | Pass / Fail / Not confirmed | test level and result |
| 4 | Hosting that can grow | Pass / Fail / Not confirmed | hosting name |

**Draft fixes, in priority order**

1. Index list: [table, column, why it helps]
2. Caching plan: [cache key, what it holds, how long, when it clears]
3. Load test plan: [user levels, what to test, what counts as a pass]
4. Hosting plan: [current hosting, what to change, what stays the same]

Each draft fix must be marked DRAFT, NOT LIVE, Owner approval needed.

**What will break first**

- [The first thing that will break as users grow, in plain words, with evidence]

**Owner steps, needs the client**

- [For example: confirm the target user number]
- [For example: approve the index list before it is made]
- [For example: choose a time for the load test, not on live users]

**Notes**

- [Any note from the Extra checks section, or None.]

**What was not checked, and why**

- [For example: load test could not be run without owner approval.]

## Missing checks

After the plan, run these 6 checks, and list the result for each one:
1. Top 5 queries listed?
2. Index list made for the gaps?
3. Caching plan made, with keys and expiry?
4. Load test plan made, with user levels?
5. Hosting plan made?
6. Target user number confirmed by the owner, or marked Not confirmed?

List the results as Complete, Missing, or Not confirmed. Do not add a missing item without owner approval.
