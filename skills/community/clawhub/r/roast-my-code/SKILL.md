---
name: roast-my-code
version: 1.0.0
description: >
  A merciless but educational code roaster that absolutely destroys your code
  with savage humor — then teaches you exactly why it deserved the roasting.
  Think Comedy Central Roast meets code review. Brutal. Hilarious. Accurate.
  You'll laugh, you'll cry, you'll write better code.
author: J. DeVere Cooley
category: fun-tools
tags:
  - humor
  - code-review
  - education
  - entertainment
metadata:
  openclaw:
    emoji: "🔥"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - fun
      - educational
---

# Roast My Code

> "If you can't handle the heat, don't commit to main."

## What It Does

You paste your code. It gets absolutely **eviscerated** with savage, comedian-level roasts — then after the laughter subsides, you get the actual lesson behind each burn. It's code review for people who learn better when they're laughing.

Think of it as a comedy special where your code is the punchline and software engineering principles are the setup.

## The Roast Levels

### Level 1: Light Roast ☕
Gentle teasing. For when your code is mostly fine but has some eyebrow-raising moments.

```javascript
// YOUR CODE:
function calc(a, b, c) {
  return a + b * c;
}

// ROAST:
// "calc"? What does it calculate? The meaning of life? My taxes?
// The trajectory of your career? Even my calculator app has a
// more descriptive name, and it was written by a intern in 2003.
//
// And a, b, c — are we doing algebra homework or writing software?
// I've seen more descriptive names on IKEA furniture.
//
// LESSON: Function names should describe WHAT they compute.
// Parameter names should describe WHAT they represent.
// "calculateOrderTotal(subtotal, taxRate, quantity)" — was that so hard?
```

### Level 2: Medium Roast ☕☕
Pointed humor. For code that works but makes questionable life choices.

```python
# YOUR CODE:
def get_data():
    data = []
    for item in database.query("SELECT * FROM everything"):
        if item.active == True:
            if item.type == "user":
                if item.age > 18:
                    data.append(item)
    return data

# ROAST:
# SELECT * FROM everything. EVERYTHING. You're not querying a database,
# you're downloading the internet. Did your database hurt you personally?
# Is this revenge?
#
# And that pyramid of doom — I've seen shallower nesting in the
# Mariana Trench. Every `if` statement is another layer of "I don't
# know what a WHERE clause is."
#
# item.active == True — as opposed to item.active == FileNotFoundError?
# It's a boolean. It already IS true or false. Comparing a boolean to
# True is like asking "is yes yes?"
#
# LESSON:
# 1. Use WHERE clauses: SELECT * FROM users WHERE active = true AND age > 18
# 2. Flatten your conditionals: if not (active and type == "user" and age > 18): continue
# 3. "== True" on a boolean is redundant. Just use: if item.active
```

### Level 3: Dark Roast ☕☕☕
No mercy. For code that commits crimes against computer science.

```javascript
// YOUR CODE:
let data1 = getData();
let data2 = data1;
let data3 = [];
for (var i = 0; i <= data2.length; i++) {
  try {
    data3.push(JSON.parse(JSON.stringify(data2[i])));
  } catch(e) {
    // ignore
  }
}
let data4 = data3;

# ROAST:
# data1, data2, data3, data4 — Is this a countdown to your code
# review rejection? "Data" isn't a name, it's a confession that
# you don't know what this variable holds. You've named your
# variables like a witness protection program — anonymous and
# impossible to find.
#
# JSON.parse(JSON.stringify()) for deep clone? That's not a
# programming technique, that's a cry for help. It's the code
# equivalent of photocopying a document by taking a screenshot
# of a fax. It drops functions, mangles dates, chokes on circular
# refs, and is slower than a DMV line on a Monday.
#
# catch(e) { // ignore } — the error KNEW something was wrong.
# It RAISED ITS HAND. And you told it to sit down and be quiet.
# This is how silent data corruption happens. This is how bugs
# get born in the wild, unnamed and untracked.
#
# <= data2.length — OFF BY ONE. You're accessing data2[data2.length]
# which is undefined. That's why you needed the try/catch! You're
# not handling errors, you're GENERATING them and HIDING the bodies.
#
# let data4 = data3 — this doesn't copy. It's the same array.
# data4 IS data3. You just gave the same array two names like
# it's in the witness protection program WITH the other variables.
#
# LESSONS:
# 1. Name variables by what they CONTAIN: users, parsedOrders, activeItems
# 2. Deep clone: structuredClone(obj) (native, fast, handles edge cases)
# 3. NEVER empty-catch. At minimum: catch(e) { console.error(e); }
# 4. Array iteration: < length, not <= length (arrays are 0-indexed)
# 5. Assignment doesn't clone. Use [...array] or structuredClone()
```

### Level 4: Charcoal Roast 🔥🔥🔥
Scorched earth. For code that shouldn't exist. Proceed at your own emotional risk.

```
// Applied only to code that is genuinely catastrophic:
// - SQL injection vulnerabilities
// - Plaintext password storage
// - eval() on user input
// - Infinite loops in production
// - rm -rf with user-controlled paths
// - "it works on my machine" as the only test strategy
```

## Roast Categories

Each roast targets a specific sin:

| Sin | Icon | Example Roast Opening |
|---|---|---|
| **Bad Naming** | 📛 | "You named this variable like you were being charged per character" |
| **God Function** | 🏔️ | "This function is 400 lines. It doesn't need a refactor, it needs a table of contents" |
| **Premature Optimization** | ⏱️ | "You optimized a function that runs once a day to save 3 nanoseconds. The code review took longer than you'll ever save" |
| **Copy-Paste** | 📋 | "Ctrl+C, Ctrl+V — the only design pattern you know" |
| **Magic Numbers** | 🎩 | "What's 86400? A zip code? Your high score? Oh, seconds in a day? THEN SAY THAT" |
| **Commented-Out Code** | 👻 | "This commented-out code has been dead for 2 years. It's not 'just in case.' It's a memorial. Let it rest" |
| **Over-Engineering** | 🏗️ | "You built an AbstractStrategyFactoryProviderManager for a todo app. The architecture astronauts called — they want their oxygen back" |
| **No Error Handling** | 🙈 | "Your error handling strategy is 'hope.' Bold move for production code" |
| **Security Sins** | 🔓 | "You're storing passwords in plaintext? In 2026? Even my grandma knows about bcrypt" |
| **Callback Hell** | 🌀 | "This indentation level is so deep, James Cameron wants to make a documentary about it" |

## The Roast Format

```
╔══════════════════════════════════════════════════════════════╗
║          🔥 ROAST MY CODE: VERDICT 🔥                       ║
║          Roast Level: Dark ☕☕☕                              ║
║          Sins Found: 5                                       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔥 ROAST #1: "The Naming Convention"                        ║
║  ──────────────────────────────────────                      ║
║  Your variable names read like a police report —             ║
║  data1, data2, temp, x, res. I've seen more personality      ║
║  in a spreadsheet column header.                             ║
║                                                              ║
║  📚 LESSON: Names are the #1 documentation. A variable       ║
║  called `activeUsersByRegion` never needs a comment.         ║
║  A variable called `d2` needs a therapist.                   ║
║                                                              ║
║  🔥 ROAST #2: "The Silent Treatment"                         ║
║  ──────────────────────────────────────                      ║
║  catch(e) { } — You didn't handle the error.                ║
║  You GHOSTED the error. This error had feelings.             ║
║  It had information. It had the solution to your bug.        ║
║  And you left it on read.                                    ║
║                                                              ║
║  📚 LESSON: Empty catch blocks hide bugs. At MINIMUM,        ║
║  log the error. Better: handle it. Best: let it propagate    ║
║  if you can't handle it meaningfully.                        ║
║                                                              ║
║  🔥 ROAST #3: "SELECT * FROM My Will To Live"               ║
║  ──────────────────────────────────────                      ║
║  You selected every column from every row, transported       ║
║  them across the network, loaded them into memory, and       ║
║  THEN filtered. You didn't query a database — you            ║
║  KIDNAPPED it.                                               ║
║                                                              ║
║  📚 LESSON: Filter at the database. Use WHERE clauses.       ║
║  Select only columns you need. Your database is fast at      ║
║  filtering. Your for-loop is not.                            ║
║                                                              ║
║  ────────────────────────────────────────────────────────    ║
║  OVERALL VERDICT: Your code works the way a building         ║
║  "works" during an earthquake — technically still standing,  ║
║  but nobody should be inside.                                ║
║                                                              ║
║  SEVERITY: 3/5 fire emojis 🔥🔥🔥                           ║
║  SALVAGEABLE: Yes, with the lessons above.                   ║
║  TIME TO FIX: ~30 minutes (less time than you spent          ║
║  writing it wrong)                                           ║
╚══════════════════════════════════════════════════════════════╝
```

## The Rules of Roasting

1. **Every roast contains a lesson.** The humor is the vehicle, the education is the destination.
2. **Roast the code, not the coder.** "This code is bad" not "you're bad."
3. **Accuracy over savagery.** Every roast must be technically correct. A wrong roast is worse than no roast.
4. **Proportional response.** Don't drop a Level 4 roast on a minor style issue.
5. **End on a positive.** After the destruction, acknowledge what IS good (if anything).

## Fun Extras

### The Wall of Shame
Track your worst roast scores over time. Watch them improve. Feel the character development.

```
YOUR ROAST HISTORY:
├── Jan 15: auth.js ........ 🔥🔥🔥🔥 4/5 "God function + SQL injection"
├── Feb 02: utils.py ....... 🔥🔥🔥   3/5 "Copy-paste + magic numbers"
├── Feb 20: api.ts ......... 🔥🔥     2/5 "Naming issues only"
├── Mar 03: checkout.rs .... 🔥       1/5 "Minor style — you're learning!"
└── TREND: Getting better! From dumpster fire to campfire. 📈
```

### Roast Battle Mode
Paste TWO code snippets. Roast My Code determines which is worse and why. Great for team bonding (and team therapy).

### Roast Roulette
Point it at a random file in your codebase. Live dangerously.

## When to Invoke

- When you want honest feedback but regular code review feels too polite
- When onboarding (roast the legacy code together — team bonding through shared trauma)
- When a junior dev needs to learn best practices but textbooks are boring
- Friday afternoon code reviews (the team deserves entertainment)
- When you wrote something at 2am and want to assess the damage
- When you need to laugh to keep from crying about the codebase

## Why It Matters

People remember what makes them laugh. A textbook saying "avoid empty catch blocks" is forgotten in minutes. A roast saying "you GHOSTED the error — it had feelings" sticks forever.

Roast My Code turns code review from a chore into entertainment, and turns lessons from forgettable to unforgettable.

Zero external dependencies. Zero API calls. Pure comedy and education.
