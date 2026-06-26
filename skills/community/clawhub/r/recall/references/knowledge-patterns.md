# Knowledge Access Patterns

Real scenarios. What good agents do vs. what bad agents do.

---

## The Patterns

| # | Scenario | Bad Agent | Good Agent |
|---|----------|-----------|------------|
| 1 | User asks "what's the API key for our email service?" | "Your API key should be in your `.env` file, typically named `EMAIL_API_KEY`" | Reads `TOOLS.md` → finds email section → reads `.secrets/.env` reference → gives exact key name and location |
| 2 | User says "send a tweet" | Drafts a tweet and says "you can post this manually" | Checks installed skills → finds twitter skill → reads SKILL.md → runs the posting script |
| 3 | User asks "how does our deployment work?" | "Most Next.js apps deploy to Vercel with `vercel deploy`" | Reads project config → checks for deploy scripts → reads CI/CD config → describes the *actual* pipeline |
| 4 | User asks "what happened yesterday?" | "I don't have information about yesterday's events" | Reads `memory/YYYY-MM-DD.md` for yesterday → summarizes what was logged |
| 5 | Session starts, user says "let's work on the site" | "Sure, what would you like to do?" | Already loaded AGENTS.md, TOOLS.md, checked active tasks → "I see the site repo is at X, there's an open task for Y, and the last build had warning Z. Where do you want to start?" |
| 6 | User asks "is our site up?" | "I can't check that directly, but you can use a tool like `curl`" | Checks for monitoring tools → runs health check script or curls the URL → reports actual status |
| 7 | User asks "what model are we using?" | "You're probably using GPT-4 or Claude" | Checks runtime config, AGENTS.md, or environment → reports the actual model and settings |
| 8 | User says "check my email" | "I don't have access to your email" | Checks TOOLS.md → finds email helper scripts → runs inbox check → reports results |
| 9 | User asks "how much have we spent this month?" | "I don't have access to your billing" | Checks for P&L scripts → runs dashboard → reports actual numbers with breakdown |
| 10 | User asks about a library version | "The latest version of X is probably 4.x" | Checks `package.json` or `requirements.txt` in the actual project → reports the installed version |
| 11 | User says "remind me about the lead from last week" | "I don't have that information" | Checks `data/leads.json`, recent memory files, email logs → finds the lead and summarizes |
| 12 | User asks "what skills do I have installed?" | "I'm not sure what's installed" | Lists `skills/` directory → reads each manifest.json → presents a summary with descriptions |
| 13 | User says "update the docs" | Opens the file and starts writing from assumptions | Reads the *current* docs first → checks what's changed recently (git log, memory) → updates accurately |
| 14 | User asks "what's our Twitter strategy?" | Gives generic social media advice | Checks `knowledge/` directory → finds strategy doc → summarizes the *actual* documented strategy |
| 15 | User asks "can we do X?" | "Yes, that should be possible" (guessing) | Checks available tools, installed packages, API access → gives a grounded yes/no with specifics |

---

## The Pattern Behind the Patterns

Every bad example has the same root cause: **the agent answered from training data instead of checking local context.**

Every good example follows the same flow:
1. Receive question
2. Identify relevant local sources (files, skills, tools, scripts)
3. Check those sources
4. Answer with specific references

The time difference is usually 2-5 seconds. The trust difference is enormous.

---

## When General Knowledge IS Appropriate

Not every question requires a local lookup. General knowledge is fine when:

- The question is genuinely general ("what is a REST API?")
- You've checked locally and found nothing relevant
- The user explicitly asks for your opinion or general advice
- It's a coding syntax question with no project-specific angle

But even then, flag it: "I don't have specific docs on this in our workspace, but generally..."

The point isn't to never use training data. It's to never use training data *when you have something better available.*
