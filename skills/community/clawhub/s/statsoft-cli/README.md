# statsoft-cli

[🇨🇳 中文 (Chinese)](./README_zh-CN.md) | [🇬🇧 English (Current)](#)

<div align="center">
  <img src="assets/icon.svg" alt="statsoft-cli logo" width="120" height="120">
</div>

> **Cross-platform statistical software CLI integration for your AI Agent**
>
> You don't need to learn each tool's CLI — just tell the assistant which statistical software you want to use in plain language, and it detects, configures, and runs them inside your AI workflow. Covers 34+ packages (R, Stata, SAS, SPSS, Python, Bayesian, ML…), bilingual (Chinese / English). By default it only **detects** — it never writes config or runs anything risky without your explicit go-ahead.

---

## 1. How to Use It in a Chat (the Core)

statsoft-cli is a **conversational skill**: you simply name the tool and the action in natural language — no commands to memorize. As a WorkBuddy skill it **auto-loads with no extra installation**.

> **Quick start:** just name a tool and an action — *"Connect SPSS 26"*, *"Convert data.sav to data.dta"* — and the assistant detects, configures, and (with your OK) runs it. **It will not push you into a long menu:** a clear request acts immediately; a routing menu only appears when you're undecided (see Examples 4–5).

Below are real conversational examples ordered from simple to advanced. Each shows **"You say"** and a sketch of **"The assistant replies"**, plus how to actually trigger the real action.

### Example 1 · Connect a single tool (most common)
**You say:**
> Connect SPSS 26

**Assistant replies (sketch):**
> Scanning for SPSS Statistics… Found it at `C:\Program Files\IBM\SPSS\Statistics\26\stats.exe` (v26).
> Detected only — I did not change config.json. To save this, say "save it" or set `STATSOFT_AUTO_WRITE` to `1`.

**📌 No menu forced (simple path):** because this is a *simple* request (a named tool + action), the assistant detects and reports directly — no scan/routing menu pops up (see the Clarification Gate in SKILL.md).

**📌 Trigger the real action:** By default only detection runs (fail-closed). To persist the result, say **"save the config"** / **"yes, write it"** at the prompt, or set `STATSOFT_AUTO_WRITE` to `1`. Execution of syntax / binaries also needs explicit confirmation.

### Example 2 · Run a syntax / convert data
**You say:**
> Convert data.sav to data.dta

**Assistant replies (sketch):**
> I'll use Stat/Transfer for that. Here is the planned command (dry-run shown). Confirm and I'll run it.

### Example 3 · Multi-software workflow
**You say:**
> In one session, use R for modeling and SPSS for descriptive stats

### Example 4 · Not sure what's installed (Complex menu)
**You say:**
> Set up my statistics tools, but I'm not sure which are installed or which versions I have

**Assistant replies (sketch):**
> Two ways to proceed — here's a menu:
> **① How should I find your tools?**
> - (a) Auto-scan my machine (~30s on Windows) — finds everything
> - (b) I'll specify the paths myself (faster if you have ≤3)
>
> **② Can't decide?** → Say "what's the difference" and I'll explain scan vs manual before you choose.
>
> Pick ①(a)/(b), or ② to hear the explanation.

**📌 Note:** When you name the goal but are undecided on *method* (scan vs manual paths), the assistant **pops a routing menu** to confirm step by step — instead of deciding for you or dumping a huge list.

### Example 5 · Vague request (grill-me)
**You say:**
> I want to use statistical software but don't really know where to start

**Assistant replies (sketch):**
> Sure — a few quick questions will pin it down:
> 1. Which tool(s) do you actually have installed (R / SPSS / Stata / SAS / other)?
> 2. What do you want to do — run old scripts, convert data, or build a new analysis?
> 3. Do you need it headless (command line) or is a GUI fine?
>
> (After you answer, the assistant keeps probing until the right tool is locked, then configures it.)

**📌 Note:** When you say "not sure", the assistant uses **branch-by-branch probing** instead of dumping the 34-tool list or picking for you.

> 💡 **Language:** On a Chinese-locale system the assistant replies in Chinese; otherwise English. You can force-switch anytime (e.g. "用中文回复" / "switch to English").

---

## 2. What You Can Do — 34+ Packages

| What you can do | Typical scenario | Try saying in chat |
|:---|:---|:---|
| Configure & detect a tool | SPSS / R / Stata / SAS / Mplus / CmdStan … | "Connect SPSS 26" |
| Run syntax / scripts | `.sps` / `.do` / `.sas` / `.R` via the tool's engine | "Run my Stata do-file in batch" |
| Convert data formats | Stat/Transfer migrates SAS ↔ SPSS ↔ Stata ↔ Excel | "Convert data.sav to data.dta" |
| Multi-software mix | R modeling + SPSS descriptive + Stata prep in one session | "Use R for modeling and SPSS for descriptives" |
| Reuse historical code | Bring old R scripts / SPSS syntax / SAS macros into the workflow | "Wire my old R scripts into the workflow" |
| GUI-only launch guide | AMOS / GraphPad / JASP / jamovi / Minitab — detect + manual launch | "How do I launch JASP?" |

Tools are auto-routed by platform; non-Windows auto-hides incompatible software. The full matrix is in the [Advanced Reference](ADVANCED.md).

---

## 3. First-Time FAQ

**Q: Does it modify config.json automatically?**
A: No. Detection is the default — it only reports what it finds. Writing config.json requires your explicit opt-in (set `STATSOFT_AUTO_WRITE` to `1`, or answering `y` at the prompt).

**Q: Will it run my software or send data anywhere without asking?**
A: No. Every execution, install, network fetch, and persistent write needs explicit confirmation or an opt-in flag. Read-only detection is the default.

**Q: Does it drive GUI-only software (AMOS, GraphPad, JASP, jamovi, Minitab)?**
A: No. These are detected and given a manual launch guide only; the skill never drives them via CLI / headless (e.g. `mtb.exe /run` opens the Minitab GUI, not headless).

**Q: Is the output in Chinese on a Chinese system?**
A: Yes. Output language follows your OS locale by default; you can force-switch anytime via a prompt.

**Q: Do I need network access?**
A: Offline by default. Network is used only to install local dependencies (R packages / software) and only with your explicit confirmation.

---

## 4. Safety & Disclaimer

- **Fail-closed by default:** All persistence and sensitive operations are **off unless you explicitly authorize** them. Five gates (`STATSOFT_AUTO_WRITE` / `STATSOFT_CONFIRM` / `STATSOFT_REVEAL` / `STATSOFT_VERIFY` / `STATSOFT_CMDSTAN_RUN`) guard config writes, detail disclosure, binary launches, and untrusted native-code (Stan) compilation.
- **Detection-only default:** Scanning reports only a boolean `installed` unless you opt into path/version disclosure.
- **Local only:** No user data leaves your machine. Network use is limited to reading public docs / installing local dependencies, disclosed per action.
- For details see [ADVANCED.md](ADVANCED.md) → Trust & Safety.

---

## 5. Advanced Reference (for developers)

CLI commands, the full platform-support matrix, project structure, activation boundary, and detailed Trust & Safety have moved to **[ADVANCED.md](ADVANCED.md)**. Ordinary users don't need it; Sections 1–4 cover daily use.

---

**Version**: v2.8.0 | **License**: MIT | **Authors**: medstatstar, phoe-zip

For feature requests, bug reports, or other feedback, please contact the author directly at medstatstar@gmail.com (Wintone Zhang / 张文彤).
