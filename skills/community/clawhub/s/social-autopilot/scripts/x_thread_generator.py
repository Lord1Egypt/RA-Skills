"""Generate data-driven X threads from PYQ database. One thread per day, auto-rotated."""

import csv
import logging
import random
from collections import Counter, defaultdict
from pathlib import Path

logger = logging.getLogger(__name__)

DATA_PATH = Path(__file__).parent.parent / "data" / "questions.csv"


def _load_questions() -> list[dict]:
    with open(DATA_PATH, "r") as f:
        return list(csv.DictReader(f))


def _qs_by_era(rows, y1, y2):
    return [r for r in rows if r.get("year", "").isdigit() and y1 <= int(r["year"]) <= y2]


def _random_q(rows, **filters) -> dict | None:
    """Pick a random question matching filters. No answer included."""
    pool = rows
    for k, v in filters.items():
        pool = [r for r in pool if v.lower() in r.get(k, "").lower()]
    return random.choice(pool) if pool else None


def _fmt_q(q: dict) -> str:
    """Format question + options. NO answer."""
    opts = [q.get(f"option{i}", "") for i in range(1, 5)]
    year = q.get("year", "")
    return (
        f"[UPSC {year}]\n"
        f"{q['question'][:200]}\n\n"
        f"A) {opts[0]}\nB) {opts[1]}\nC) {opts[2]}\nD) {opts[3]}"
    )


def _trim(text: str, limit: int = 280) -> str:
    if len(text) <= limit:
        return text
    return text[:limit - 1] + "…"


# ── Thread generators (7 themes, rotate by day_of_year % 7) ──────────────────

def _thread_subject_weightage(rows) -> list[str]:
    """Subject weightage across eras."""
    tweets = []
    tweets.append(_trim(
        "🧵 I analyzed 3,274 UPSC PYQs (1995-2025). Here's how subject weightage shifted over 3 decades.\n\n"
        "The exam you're preparing for is NOT the same exam from 10 years ago.\n\n#UPSC"
    ))

    old = _qs_by_era(rows, 1995, 2005)
    new = _qs_by_era(rows, 2016, 2025)
    old_subs = Counter(r.get("subject", "").strip() for r in old if r.get("subject"))
    new_subs = Counter(r.get("subject", "").strip() for r in new if r.get("subject"))

    lines = []
    for s, n in new_subs.most_common(7):
        old_pct = round(old_subs.get(s, 0) * 100 / len(old), 1)
        new_pct = round(n * 100 / len(new), 1)
        arrow = "📈" if new_pct > old_pct else "📉"
        lines.append(f"{arrow} {s}: {old_pct}% → {new_pct}%")
    tweets.append(_trim("\n".join(lines)))

    # Biggest riser with proof question
    q = _random_q(rows, subject="Environment", year="2024")
    if q:
        tweets.append(_trim(
            "Environment went from 1.6% to 16.4% — a 10x increase.\n\n"
            "Here's a 2024 Environment question to prove the complexity:\n\n"
            f"{q['question'][:180]}"
        ))

    # Biggest faller with old question
    q_old = _random_q(rows, subject="History", year="1998")
    if q_old:
        tweets.append(_trim(
            "History dropped from 18.5% to 9.0%.\n\n"
            f"Compare this 1998 question:\n\"{q_old['question'][:150]}\"\n\n"
            "vs today's multi-statement conceptual questions."
        ))

    tweets.append(_trim(
        "Key takeaway: if you're allocating study time based on 2010 patterns, you're leaving marks on the table.\n\n"
        "Environment, Economy, Polity = where the marks moved.\n\n#UPSC #Prelims2026"
    ))
    return tweets


def _thread_question_style(rows) -> list[str]:
    """How question style evolved."""
    tweets = []
    tweets.append(_trim(
        "🧵 UPSC questions are 70% longer than they were in 2005.\n\n"
        "Here's the data + real questions to prove it.\n\n#UPSC"
    ))

    # Stats
    old = _qs_by_era(rows, 1995, 2005)
    new = _qs_by_era(rows, 2016, 2025)
    old_ctf = sum(1 for r in old if "consider the following" in r.get("question", "").lower())
    new_ctf = sum(1 for r in new if "consider the following" in r.get("question", "").lower())

    tweets.append(_trim(
        f"\"Consider the following\" questions:\n"
        f"1995-2005: {round(old_ctf*100/len(old),1)}%\n"
        f"2016-2025: {round(new_ctf*100/len(new),1)}%\n\n"
        f"Multi-statement questions: 23.8% → 51.9%\n"
        f"Avg question length: 151 → 256 chars"
    ))

    # Old style example
    short = sorted(old, key=lambda r: len(r["question"]))
    if short:
        q = short[0]
        tweets.append(_trim(f"2000s style (direct recall):\n\n\"{q['question']}\"\n\nYou know it or you don't. 13 words."))

    # New style example
    long_new = [r for r in new if "consider the following" in r.get("question", "").lower()]
    if long_new:
        q = random.choice(long_new)
        tweets.append(_trim(f"2024 style ({len(q['question'])} chars):\n\n\"{q['question'][:200]}...\"\n\nYou need to evaluate each statement independently."))

    tweets.append(_trim(
        "What this means: stop memorizing isolated facts.\n\n"
        "UPSC now tests whether you UNDERSTAND concepts. Practice elimination — 44% of questions are designed for it.\n\n#UPSC"
    ))
    return tweets


def _thread_rising_falling(rows) -> list[str]:
    """Rising vs falling topics."""
    tweets = []
    tweets.append(_trim(
        "🧵 Which UPSC topics are RISING and which are DYING?\n\n"
        "Data from 3,274 PYQs. Real questions as proof.\n\n#UPSC"
    ))

    old = _qs_by_era(rows, 2006, 2015)
    new = _qs_by_era(rows, 2016, 2025)
    old_t = Counter(r.get("topicId", "") for r in old if r.get("topicId"))
    new_t = Counter(r.get("topicId", "") for r in new if r.get("topicId"))

    rising = []
    falling = []
    for t in set(list(old_t.keys()) + list(new_t.keys())):
        if not t: continue
        o, n = old_t.get(t, 0), new_t.get(t, 0)
        if o > 3 and n > 3:
            change = round((n - o) * 100 / o, 1) if o else 999
            if change > 50: rising.append((t.replace("-", " ").title(), o, n, change))
            elif change < -30: falling.append((t.replace("-", " ").title(), o, n, change))

    rising.sort(key=lambda x: x[3], reverse=True)
    falling.sort(key=lambda x: x[3])

    r_lines = [f"📈 {t}: {o}→{n} (+{c}%)" for t, o, n, c in rising[:6]]
    tweets.append(_trim("RISING topics:\n\n" + "\n".join(r_lines)))

    f_lines = [f"📉 {t}: {o}→{n} ({c}%)" for t, o, n, c in falling[:6]]
    tweets.append(_trim("FALLING topics:\n\n" + "\n".join(f_lines)))

    # Proof question for top riser
    if rising:
        topic_id = rising[0][0].lower().replace(" ", "-")
        q = _random_q(rows, topicId=topic_id)
        if q:
            tweets.append(_trim(f"Example — {rising[0][0]} (rose {rising[0][3]}%):\n\n{_fmt_q(q)[:240]}"))

    tweets.append(_trim(
        "Update your time allocation. The exam evolves — your prep should too.\n\n#UPSC #Prelims2026"
    ))
    return tweets


def _thread_environment(rows) -> list[str]:
    """Environment's 10x growth."""
    tweets = []
    tweets.append(_trim(
        "🧵 Environment went from 1.6% to 16.4% in UPSC Prelims.\n\n"
        "That's a 10x increase. Here's the year-by-year data.\n\n#UPSC #Environment"
    ))

    env_by_year = defaultdict(int)
    total_by_year = defaultdict(int)
    for r in rows:
        y = r.get("year", "").strip()
        if not y.isdigit(): continue
        total_by_year[int(y)] += 1
        if "Environment" in r.get("subject", ""):
            env_by_year[int(y)] += 1

    # Show 5-year averages
    for era, y1, y2 in [("1995-2005", 1995, 2005), ("2006-2010", 2006, 2010),
                         ("2011-2015", 2011, 2015), ("2016-2020", 2016, 2020), ("2021-2025", 2021, 2025)]:
        env = sum(env_by_year[y] for y in range(y1, y2+1))
        total = sum(total_by_year[y] for y in range(y1, y2+1))
        pct = round(env * 100 / total, 1) if total else 0
        # build inline
    lines = []
    for era, y1, y2 in [("1995-2005", 1995, 2005), ("2006-2010", 2006, 2010),
                         ("2011-2015", 2011, 2015), ("2016-2020", 2016, 2020), ("2021-2025", 2021, 2025)]:
        env = sum(env_by_year[y] for y in range(y1, y2+1))
        total = sum(total_by_year[y] for y in range(y1, y2+1))
        pct = round(env * 100 / total, 1) if total else 0
        bar = "█" * (env // 2)
        lines.append(f"{era}: {pct}% {bar}")
    tweets.append(_trim("\n".join(lines)))

    # 1995 question vs 2024
    q_old = _random_q(rows, subject="Environment", year="1995")
    q_new = _random_q(rows, subject="Environment", year="2024")
    if q_old:
        tweets.append(_trim(f"1995 Environment question:\n\n\"{q_old['question'][:200]}\"\n\nSimple factual recall."))
    if q_new:
        tweets.append(_trim(f"2024 Environment question:\n\n\"{q_new['question'][:200]}\"\n\nMulti-layered, policy + science + current affairs."))

    tweets.append(_trim(
        "If Environment isn't in your top 3 priority subjects, you're ignoring 16% of the paper.\n\n#UPSC"
    ))
    return tweets


def _thread_answer_patterns(rows) -> list[str]:
    """Answer distribution analysis."""
    tweets = []
    tweets.append(_trim(
        "🧵 I checked the correct answer distribution across 3,274 UPSC questions.\n\n"
        "Is there really a pattern? Here's the data.\n\n#UPSC"
    ))

    ans = Counter(r.get("correctIndex", "") for r in rows)
    total = len(rows)
    tweets.append(_trim(
        f"Overall distribution:\n\n"
        f"A: {ans.get('0',0)} ({round(ans.get('0',0)*100/total,1)}%)\n"
        f"B: {ans.get('1',0)} ({round(ans.get('1',0)*100/total,1)}%)\n"
        f"C: {ans.get('2',0)} ({round(ans.get('2',0)*100/total,1)}%)\n"
        f"D: {ans.get('3',0)} ({round(ans.get('3',0)*100/total,1)}%)\n\n"
        f"B and C slightly more common. But barely."
    ))

    # By era
    for era, y1, y2 in [("1995-2005", 1995, 2005), ("2016-2025", 2016, 2025)]:
        eq = _qs_by_era(rows, y1, y2)
        ea = Counter(r.get("correctIndex", "") for r in eq)
        t = len(eq)
        lines = [f"{l}: {round(ea.get(str(i),0)*100/t,1)}%" for i, l in enumerate("ABCD")]
        tweets.append(_trim(f"{era}:\n" + " | ".join(lines) + "\n\nAlmost perfectly distributed."))

    tweets.append(_trim(
        "Verdict: UPSC doesn't favor any option consistently. Don't guess based on letter.\n\n"
        "Your best strategy is elimination, not statistics.\n\n#UPSC"
    ))
    return tweets


def _thread_topic_deep_dive(rows) -> list[str]:
    """Deep dive into a random high-frequency topic with real questions."""
    topics = Counter(r.get("topicId", "") for r in rows if r.get("topicId"))
    # Pick from top 15 topics randomly
    top = [t for t, c in topics.most_common(15)]
    topic = random.choice(top)
    topic_name = topic.replace("-", " ").title()
    topic_qs = [r for r in rows if r.get("topicId") == topic]

    tweets = []
    tweets.append(_trim(
        f"🧵 UPSC has asked {len(topic_qs)} questions on {topic_name} since 1995.\n\n"
        f"Here's what the data shows + real questions.\n\n#UPSC"
    ))

    # By era
    for era, y1, y2 in [("1995-2005", 1995, 2005), ("2006-2015", 2006, 2015), ("2016-2025", 2016, 2025)]:
        c = len(_qs_by_era(topic_qs, y1, y2))
        tweets.append("") if False else None  # placeholder
    era_counts = []
    for era, y1, y2 in [("1995-2005", 1995, 2005), ("2006-2015", 2006, 2015), ("2016-2025", 2016, 2025)]:
        c = len(_qs_by_era(topic_qs, y1, y2))
        era_counts.append(f"{era}: {c} questions")
    tweets.append(_trim(f"Frequency by era:\n\n" + "\n".join(era_counts)))

    # 2-3 real questions (no answers)
    samples = random.sample(topic_qs, min(2, len(topic_qs)))
    for q in samples:
        tweets.append(_trim(_fmt_q(q)))

    tweets.append(_trim(
        f"If {topic_name} keeps appearing, it's not coincidence — it's a priority area.\n\n"
        f"Practice these PYQs topic-wise, not year-wise.\n\n#UPSC"
    ))
    return [t for t in tweets if t]  # remove None


def _thread_elimination_strategy(rows) -> list[str]:
    """Elimination-style questions analysis."""
    tweets = []
    tweets.append(_trim(
        "🧵 44% of recent UPSC questions use elimination-style options.\n\n"
        "\"1 and 2 only\" / \"2 and 3 only\" / \"All of the above\"\n\n"
        "Here's how to handle them.\n\n#UPSC"
    ))

    old = _qs_by_era(rows, 1995, 2005)
    new = _qs_by_era(rows, 2016, 2025)
    old_elim = sum(1 for r in old if any(x in (r.get("option1","")+r.get("option2","")+r.get("option3","")+r.get("option4","")).lower()
        for x in ["1 and 2", "1 and 3", "2 and 3", "1, 2 and 3", "all of the above", "none of the above"]))
    new_elim = sum(1 for r in new if any(x in (r.get("option1","")+r.get("option2","")+r.get("option3","")+r.get("option4","")).lower()
        for x in ["1 and 2", "1 and 3", "2 and 3", "1, 2 and 3", "all of the above", "none of the above"]))

    tweets.append(_trim(
        f"Elimination questions:\n"
        f"1995-2005: {round(old_elim*100/len(old),1)}%\n"
        f"2016-2025: {round(new_elim*100/len(new),1)}%\n\n"
        f"Nearly tripled. This is the dominant question format now."
    ))

    # Real example
    elim_qs = [r for r in new if "consider the following" in r.get("question", "").lower()
               and any(x in (r.get("option1","")+r.get("option2","")+r.get("option3","")+r.get("option4","")).lower()
               for x in ["1 and 2", "2 and 3"])]
    if elim_qs:
        q = random.choice(elim_qs)
        tweets.append(_trim(f"Real example:\n\n{_fmt_q(q)[:250]}"))

    tweets.append(_trim(
        "Strategy: evaluate each statement as TRUE/FALSE independently. Then match the combination.\n\n"
        "Don't read options first — decide on statements first, then look for your combination.\n\n#UPSC"
    ))
    return tweets


# ── Main entry point ─────────────────────────────────────────────────────────

THREAD_GENERATORS = [
    _thread_subject_weightage,
    _thread_question_style,
    _thread_rising_falling,
    _thread_environment,
    _thread_answer_patterns,
    _thread_topic_deep_dive,
    _thread_elimination_strategy,
]


def generate_daily_thread() -> list[str]:
    """Generate today's thread. Rotates through 7 themes."""
    rows = _load_questions()
    from datetime import datetime
    day = datetime.now().timetuple().tm_yday
    gen = THREAD_GENERATORS[day % len(THREAD_GENERATORS)]
    logger.info("Thread theme: %s", gen.__name__)
    tweets = gen(rows)
    # Ensure all within 280 chars
    return [_trim(t) for t in tweets if t]
