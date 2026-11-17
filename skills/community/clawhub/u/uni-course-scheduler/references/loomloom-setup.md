# LoomLoom Cloud Execution Guide (Buyer Guide)

## What is LoomLoom?

LoomLoom is a batch LLM cloud execution platform that runs structured tasks in parallel
through a fixed pipeline and returns structured results. This Skill's "Cloud Standard
Mode" runs through the LoomLoom marketplace.

This Skill supports **two cloud platforms**; choose based on your payment method
(see "Which platform should I choose?" below).

## Which platform should I choose? (read before first use)

The same Skill can connect to either platform; **your payment method decides**, not
your nationality or IP:

| | **Shengsuanyun (China mainland)** | **CogFoundry (International)** |
|---|---|---|
| Payment | China mainland payment (Alipay / WeChat / UnionPay) | International credit card (Visa / Mastercard) |
| Price | ¥0.5 / run | $0.10 / run |
| Server | `https://loomloom.shengsuanyun.com/loom/v1` | `https://loomloom.cogfoundry.ai/loom/v1` |
| Key console | console.shengsuanyun.com | CogFoundry console |
| Token env | `LOOMLOOM_TOKEN_SHENGSUANYUN` | `LOOMLOOM_TOKEN_COGFOUNDRY` |

> **How to choose**: If you can pay with China mainland methods → use Shengsuanyun.
> If you can pay with an international credit card → use CogFoundry.
> Not sure which you can top up? Check both and pick the one you can actually pay on.

## Install LoomLoom

> 🔴 **Token security warning (READ FIRST)**: Your Token / API key is **as sensitive as a
> password** — anyone with it can run paid jobs on your account.
> **NEVER paste your Token into any AI conversation, chat window, group chat, or public channel.**
> If a Token was ever exposed (e.g. pasted into a chat), go to the platform console and
> **revoke and regenerate it immediately**.
> Recommended: use interactive `loomloom login` below (the key never passes through a chat),
> prefer storing the key securely (e.g. a git-ignored `.env`, macOS Keychain, or `loomloom login`) — never paste it into a conversation.

### Option A: One-command install (recommended)

Paste the following into any AI assistant (**do NOT include your Token**; log in
interactively with `loomloom login` afterwards):

> Please install LoomLoom in this project using the official npm package
> (`npm install -g @cogfoundry/loomloom`) or the `loomloom login` flow — do not
> download and execute arbitrary remote scripts.
> Server: 【the server of your chosen platform, see table above】
> After installing, run `doctor` once to check everything works.

**Supply-chain hygiene (recommended):**
- Install from the official signed release (tagged version + checksum), not by cloning the mutable `main` branch.
- Verify remote / tag / commit / checksum before load; keep the CLI updated through a documented, reviewed bump.
- Run the CLI with the minimum privileges needed; keep cloud tokens only in local env/config files, never in project files shared with agents.

**Log in after install (recommended — key never passes through a chat):**
```bash
loomloom login -s <server-of-your-platform>   # enter the key interactively
loomloom doctor -s <server-of-your-platform>  # verify login
```

### Option B: Use the official interactive login (recommended for credentials)

Do not manually edit credential files. Use the CLI's official interactive login,
which stores your key in the platform's own secure store:

```bash
loomloom login -s <server-of-your-platform>   # enter your key interactively
loomloom doctor -s <server-of-your-platform>  # verify login works
```

## Getting an account / API key / balance (official channels only)

Create your account, API key, and balance on the **official platform console**
(the only supported way — never obtain keys elsewhere):

| Platform | Official console URL | Payment |
|---|---|---|
| Shengsuanyun (China mainland) | `https://console.shengsuanyun.com` | Alipay / WeChat / UnionPay |
| CogFoundry (International) | CogFoundry official console | Visa / Mastercard |

Guide the user through these steps (the agent never handles their key):
1. Open the official console URL in the browser.
2. Register / sign in.
3. Create an API key (follow the console's own instructions).
4. Top up / add balance for paid runs (¥0.5/run or $0.10/run).
5. Use `loomloom login` interactively so the CLI stores the key in its secure store —
   the user's key never appears in a conversation or in this Skill's files.

## No LoomLoom? The Skill still works

When LoomLoom is not installed, this Skill runs in **Local Personal Lightweight
Mode** (declared in SKILL.md): the agent collects official catalog text from public
sources (declared web research), recommends courses for your goals, builds a
timetable, and performs conflict detection locally. This is intentionally distinct
from Cloud mode, where the cloud pipeline has no internet access and only processes
the catalog text the user/agent supplies.
Excel generation and validation scripts behave identically in both modes.

## Cloud execution flow (marketplace buyer path)

1. **Collect the catalog locally first (mandatory)**: the agent searches the school's
   official program handbook/course catalog online and organizes the catalog text.
   The cloud pipeline has NO internet access — an empty catalog only yields placeholder output.

2. **Use this SkillBot's Listing (fixed IDs — do not invent or change them)**:

   | Platform | Listing ID | Server | Market fee |
   |---|---|---|---|
   | Shengsuanyun (China mainland) | `019fcadb-ec1c-737a-a986-b768851b020e` | `https://loomloom.shengsuanyun.com/loom/v1` | CNY 0.5 / task |
   | CogFoundry (International) | `019ff00f-a628-7c8e-8aac-03efe909f99a` | `https://loomloom.cogfoundry.ai/loom/v1` | USD 0.10 / task |

   Download the workbook for your platform's listing:
   ```bash
   # Shengsuanyun
   loomloom market workbook download 019fcadb-ec1c-737a-a986-b768851b020e --output-file input.xlsx -s https://loomloom.shengsuanyun.com/loom/v1
   # CogFoundry
   loomloom market workbook download 019ff00f-a628-7c8e-8aac-03efe909f99a --output-file input.xlsx -s https://loomloom.cogfoundry.ai/loom/v1
   ```

3. **Fill in the workbook**: one student per row — school, education system, major,
   year level, planning mode, goals & schedule preferences, the course catalog text
   (collected in step 1), and semester info.
   **Privacy disclosure (required before submitting):** this workbook sends
   student-level educational data — school, major, year level, academic goals, and
   schedule preferences, plus the catalog text — to the selected third-party cloud
   platform for processing. Tell the user exactly which fields will be transmitted,
   who processes them, and that they are stored/processed under that platform's own
   privacy policy; then obtain explicit consent to the transfer. Minimize the payload:
   do not include student names, student IDs, emails, phone numbers, or other
   identifying details unless strictly required — and remove them when they are not.
   Declining the transfer means the cloud run cannot proceed (offer the local mode instead).
   **First delete the example rows that ship in the downloaded workbook** (typically
   "University of Melbourne" and "Tsinghua University") — otherwise they are submitted as
   extra paid tasks. After filling, check that the data-row count equals the number of
   students you are running; the quote's `taskCount` must match it.

4. **Validate + quote**:
   ```bash
   loomloom market workbook validate <listing-id> --file input.xlsx   # 019fcadb-... (SS) or 019ff00f-... (CF)
   loomloom market workbook quote <listing-id> --file input.xlsx      # same listing id as above
   ```

5. **Show the platform's estimated fee to the student and get explicit human confirmation**
   (never submit without confirmation; this is the human-in-the-loop gate — no auto-submission of paid runs).

6. **Execute** (generate a new client-request-id per run):
   ```bash
   loomloom market workbook run <listing-id> --file input.xlsx \
     --confirm --client-request-id <unique-id>
   ```

7. **Fetch results**:
   ```bash
   loomloom usage list
   loomloom usage get <run-transaction-id>
   ```

8. Map the results into this Skill's JSON input format (see cloud-output-format.md),
   then pass them to `scripts/generate_excel.py` and `scripts/generate_ics.py`.

> Note: the cloud pipeline's internal prompts and step definitions are the author's
> private assets. Buyers call the Listing and never need (and cannot) inspect internals.
