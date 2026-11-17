# Accounts, step by step

Read the section for the step you are on. The student does the clicking; you run the commands.

## Money facts (tell them early, keep it short)

| Stage | Cost |
|---|---|
| Learning and demo apps | $0. Vercel Hobby, Supabase free, GitHub free |
| Real users who sign up by email | A domain, about $10 to $15 a year (Cloudflare Registrar or Porkbun). Or stay on the free `name.vercel.app` address |
| AI features in an app | $5 or more, once, to the AI provider. OpenRouter has free models (about 50 requests a day) |
| Taking money from customers | Vercel Pro $20 a month. The free Vercel plan does not allow commercial use, which includes payment checkout. Plus the payment provider's fees |
| A serious database | Supabase Pro $25 a month once real people depend on it (no pausing) |
| Phone app stores | Apple $99 a year (and a Mac). Google $25 once, plus 12 testers for 14 days |

Free Supabase: 2 active projects, and a project is paused after a week without use. Waking it is one click in the dashboard. Claude Pro limits are shared with claude.ai chat; on build days skip the chat and check `/usage`.

Prices change. If a figure matters to a decision, say it comes from the course notes and may have changed.

## 1. Tools

Run `check-tools.mjs`. It prints the install line for the student's system. Typical ones:

- Node.js: download the LTS version from nodejs.org and run the installer. Close and reopen the terminal afterwards.
- git: macOS asks to install developer tools the first time `git` runs. Windows: Claude Code already needs Git for Windows.
- GitHub tool `gh`: macOS `brew install gh`; Windows `winget install --id GitHub.cli`; Linux see cli.github.com.
- Playwright browser (used for phone-size checks): `npx playwright install chromium`. Run it yourself.

## 2. GitHub

1. github.com, Sign up (free). Use an email they can read.
2. You run `gh auth login --web`. It prints a one-time code and opens github.com/login/device. They paste the code and approve.
3. You run `gh auth setup-git` then `gh auth status`. The status must show "Logged in".

## 3. Vercel

1. vercel.com, Sign up, choose "Continue with GitHub". Pick the free Hobby plan.
2. You run `npx --yes vercel@64.3.1 login`. A browser page opens; they confirm.
3. `npx --yes vercel@64.3.1 whoami` prints the user. If they have a team, `npx --yes vercel@64.3.1 teams ls` shows it.

## 4. Supabase

1. supabase.com, Sign in with GitHub. An organisation is created automatically (free plan).
2. supabase.com/dashboard/account/tokens, Generate new token, name it "shipyard", copy it.
3. You run `secrets-init.mjs`. They paste the token after `SUPABASE_ACCESS_TOKEN=` with no spaces or quotes, save and close.
4. You run `secrets-check.mjs --live`. A tick means the token works.
5. The organisation slug is the short name in the dashboard address (`supabase.com/dashboard/org/<slug>`).

The token can manage all their Supabase projects. It stays in the keys file on their computer; nothing else gets it.

## 5. AI keys (optional)

- OpenRouter: openrouter.ai, Keys, Create key. Set a credit limit on the key. Paste into `OPENROUTER_API_KEY`.
- OpenAI: platform.openai.com, API keys, Create new secret key. Billing needs at least $5. Under Limits, set a monthly budget and an email alert. Paste into `OPENAI_API_KEY`.
- Best practice: a separate key per app, so you can see each app's cost and cut one off without breaking the others.

## 6. Email (optional)

resend.com, Sign up, API Keys, Create API key with Full access (it has to create your sending domain later). Paste into `RESEND_API_KEY`. This key stays on your computer: each app is given its own key that can only send email, never this one. To email anyone other than themselves they must verify a domain in Resend, which needs a domain from step 8. Until then password-reset emails only reach the account owner.

## 7. Stripe (optional)

stripe.com, create an account, stay in Test mode (toggle at the top). Developers, API keys: the Secret key (`sk_test_...`) goes in `STRIPE_SECRET_KEY` and the Publishable key (`pk_test_...`) in `STRIPE_PUBLISHABLE_KEY`. No real money moves in test mode, and these two slots only accept test keys. Going live is a later step, needs Vercel Pro, and uses separate slots (`STRIPE_LIVE_SECRET_KEY`, `STRIPE_LIVE_PUBLISHABLE_KEY`).

## 8. Domain

None is fine to start. If they want one, Cloudflare Registrar (cost price, about $10.5 a year for .com) or Porkbun (about $11). Connecting it comes in a later step.

## 9. Profile and 10. Habits

Saved with `profile.mjs set`. `starter/CLAUDE.md` is only added to `~/.claude/CLAUDE.md` after they see it and say yes.
