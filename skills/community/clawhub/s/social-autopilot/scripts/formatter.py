"""Formats social media posts — human-sounding, raw, English only.

v4.0 — Sounds like a real UPSC aspirant sharing their journey.
No emoji spam. No perfect structure. Just real talk.
"""

import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

X_CHAR_LIMIT = 280
APP_PROMO = ""

# ─── Post Pools ───────────────────────────────────────────────────────────────
# Written like a real person — messy, opinionated, raw
# Vary structure so 3 posts in a row don't feel templated

INSIGHT_POSTS = [
    # Short ones
    "went through 30 years of UPSC papers. constitutional amendments showed up 28 times out of 30.\nif you're skipping this topic you're literally skipping marks",

    "polity + economy = 33% of the entire prelims paper. one third.\nhow are people still treating these as secondary subjects",

    "i did the math on negative marking. attempting 75 and getting 55 right beats attempting 90 and getting 58 right.\nhow many marks are you losing by guessing on unsure questions",

    "environment questions grew 7x from the 90s to now. 7 times.\nand people still prep it last. doesn't make sense to me",

    "3274 questions analyzed from 1995 to 2025. polity alone is 17.7%.\nthat's almost 1 in every 5 questions",

    # Medium ones
    "spent a week doing topic-wise PYQs instead of year-wise. completely changed how i see the paper.\n\nyou start noticing which concepts keep showing up in different forms. same idea, different angle every few years.\n\nhow are you doing your PYQ practice right now",

    "the pattern i noticed in environment questions is honestly wild. 2-3 per paper in the 90s.\nnow it's 15-20 regularly. entire new subject basically grew inside the exam.\n\nif you're treating environment as a small topic you're behind",

    "art and culture is 6.7% of the paper. the questions are mostly factual — which dance form, which state, which festival.\nstraightforward marks if you spend even a week on it.\n\nmost people skip it for harder topics and leave easy marks on the table",

    "science questions in UPSC have been declining for years. used to be 15+ per paper. now barely 5-8.\n\nall that bandwidth moved to environment and current affairs.\nstill studying all 5 units of science equally",

    "spent an hour just plotting which topics appear how often. vedic period — 12 times in 30 years. fundamental rights — 25+ times.\n\nthe exam has favorites. once you know the favorites everything becomes clearer",

    "current affairs is 10% of the paper but people spend 80% of their time on it.\n\nnewspaper daily for 2 hours but polity once a month. the numbers don't add up",

    "maps. just maps. rivers through which states, national parks, arrange north to south.\n\n3-5 marks just from map-based questions and most people never deliberately practice them. tried this last cycle and it helped",

    "here's what i got wrong for too long — treating all subjects equally.\n\npolity 17.7%, economy 15.9%, history 14.8% — these three alone are almost half the paper. prioritize accordingly",

    "solved 3274 questions topic-wise. the constitutional amendments pattern is almost embarrassing how clear it is.\n\n28 out of 30 years. UPSC is basically telling you what to study. are we listening",

    "the jump in difficulty from pre-2010 to post-2015 papers is real. old papers feel like GK quizzes.\n\nnewer ones need actual thinking and elimination. if you're only practicing old papers you might be underprepared",

    "took me too long to figure out that WTO and trade bodies appear almost every time there's a major global agreement.\n\nthe news is telling you what UPSC will ask next year. connecting those dots is a skill",

    "economy is 15.9% of the paper and the questions lately are very conceptual.\n\nnot just 'what is repo rate' but 'what happens to inflation when this changes.' mechanism-based. how deep is your economics understanding",
]

HOT_TAKE_POSTS = [
    "hot take: most coaching notes are a liability not an asset.\n\nyou spend more time organizing and reading them than actually thinking. the understanding doesn't transfer.\n\nwhat's your experience with notes",

    "NCERTs alone will not clear UPSC prelims in 2025. i said it.\n\nthey're the foundation yes. but the paper moved. post-2015 questions need conceptual depth NCERTs don't give.\n\ntell me i'm wrong",

    "the '14 hours a day study' flex is mostly performative.\n\n6 focused hours consistently beats 12 scattered hours every time. i've tested this on myself.\n\nwhat's your honest daily average",

    "unpopular opinion: CSAT is where a lot of people quietly fail.\n\neveryone's focused on GS. CSAT is 'qualifying only' so it gets 2 days of prep. then exam day hits.\n\nhow much time are you actually giving it",

    "self study candidates make it to the top 100 every year. every year.\n\nbut the industry has convinced everyone they need a 1.5 lakh course to crack UPSC.\n\nwhat actually differentiates toppers isn't the coaching. it's the consistency",

    "revision is more important than covering new topics. genuinely.\n\nmost people fail not because they don't know things but because they can't recall under pressure.\n\nhow many times have you revised your polity notes",

    "monthly current affairs compilations are more useful than daily newspaper reading for UPSC.\n\nfight me. the daily news is 90% noise for prelims. the monthly filter keeps what matters.\n\nhow long is your daily newspaper routine",

    "everyone talks about toppers' booklists. nobody talks about toppers' elimination strategies.\n\nknowing which option to kill first is a real skill and it's what separates 55 marks from 75 marks.\n\nhave you ever practiced just elimination",

    "taking fewer attempts with higher accuracy is objectively better than attempting everything.\n\ngot this wrong in my first prep phase. was attempting 95+ questions every mock. score was worse than when i attempted 70 carefully.\n\nwhat's your attempt strategy",

    "answer writing is tested in mains but the thinking it builds helps prelims too.\n\nbeing able to explain WHY an option is wrong is different from just marking the right one.\n\nhow often are you writing out your reasoning",

    "the syllabus is not the guide. PYQs are the guide.\n\nthe official syllabus is vague. the actual questions tell you exactly how deep each topic goes. start there.\n\nwhen did you first start solving PYQs",

    "geography gets underrated because people find it boring. but 12.5% of the paper is geography.\n\nand most of it is Indian geography — rivers, regions, soils, agriculture. not even world geo.\n\nhow's your Indian geography",
]

QUESTION_POSTS = [
    "what's the one topic that you keep postponing and you know it's going to cost you marks",

    "if you had to cut your prep down to just 3 subjects for the next 30 days, which ones would you pick and why",

    "what changed most in your prep after you started solving PYQs seriously",

    "be honest — how many days in a row can you maintain a real 6-hour study routine without breaking",

    "which UPSC subject do you think is the most underrated and why",

    "what's the worst advice you received about UPSC prep that you actually followed for a while",

    "if you could ask a real UPSC topper one question right now, what would it be",

    "what's one thing you wish you'd started doing in your very first month of prep that you only figured out later",

    "polity or economy — which one do you find easier to retain and why",

    "what does your revision schedule actually look like? be specific — not the ideal one, the real one",

    "how do you decide when you've studied a topic 'enough' before moving to the next one",

    "what's your strategy for current affairs? newspaper, app, monthly compilation, something else — what works for you",

    "if the exam is in 3 months and you haven't touched environment yet, what do you do",

    "do you think the way you're studying right now would be enough to clear prelims? honest answer",
]

MYTH_BUST_POSTS = [
    "myth: you need to read every major newspaper daily.\n\nlooked at 30 years of papers. editorials from specific outlets don't show up as questions. analysis + PIB + monthly CA compilation is enough.\n\nhow many hours a week are you spending on newspapers",

    "myth: prelims is about how much you know.\n\nit's actually about what you choose NOT to attempt. with negative marking at -0.67, wrong answers are expensive.\n\nhave you calculated your ideal attempt count",

    "myth: art and culture is too vast to cover for 6% marks.\n\nit's not vast if you go topic-wise. dance forms, folk traditions, classical music basics — 10-12 days is actually enough for the high-frequency parts.\n\nhow much time have you given it",

    "myth: environment is a new addition so there's not much PYQ data.\n\nlooked at the data. environment appeared in every single paper since 2000. and the volume tripled post-2012.\n\nalmost 12% of the paper now",

    "myth: science is still a major subject in UPSC.\n\nit used to be. 15+ questions in the 90s. now it's down to 5-8 and declining.\n\nthe marks moved to environment and current affairs. update your time allocation",

    "myth: self study is only for repeaters, first attempt needs coaching.\n\nevery year toppers with no coaching make it. the exam doesn't know or care where your notes came from.\n\nwhat it cares about is whether you understand the concepts",

    "myth: the more topics you cover, the better your score.\n\npicking 3 subjects and going deep beats knowing 8 subjects shallowly.\n\npolity, economy, history alone = 48% of the paper. depth over breadth",

    "myth: current affairs is unpredictable so you can't prepare for it specifically.\n\nthere are recurring themes — international organizations, government schemes, environment summits, economic indicators.\n\nthese repeat. it's not random",

    "myth: you should finish reading before attempting questions.\n\ni tried both. starting questions on day one forced me to understand what actually matters in each topic.\n\nthe syllabus never really finishes. questions teach you what counts",

    "myth: high daily study hours = success.\n\nthree years of UPSC prep data suggests otherwise. consistency beats volume. 5 solid hours every day for a year is more than 12 hours for a month then burnout.\n\nwhat's sustainable for you",

    "myth: constitutional amendments are a separate optional topic.\n\n28 out of 30 years. not 'sometimes' or 'often.' twenty-eight times in thirty years.\n\nif this isn't in your serious prep pile we need to talk",

    "myth: mains syllabus is separate from prelims preparation.\n\nconcepts overlap massively. polity analysis for mains sharpens prelims MCQ reasoning too.\n\nintegrated prep is more efficient. are you treating them as completely separate",
]

STRUGGLE_POSTS = [
    "the day i realized i'd been studying wrong for 6 months was genuinely rough.\n\nnot wrong as in wrong information. wrong as in zero retention. reading without testing.\n\nhad to restart a lot of things. it felt like going backward but it was actually the turning point",

    "some days the whole thing feels pointless.\n\nyou read 4 hours, sit down with questions, get 40% right. what even is the point.\n\nbut those days are also weirdly the ones that build something. i can't explain it but it's true",

    "mock test day is genuinely stressful even when it's just practice.\n\nthat feeling before you look at your score. like you know it might hurt.\n\nanyone else do this or just me",

    "three months into prep and i still hadn't touched environment. kept pushing it.\n\nthen saw the statistics. 12% of the paper. growing every year.\n\nstarted the next day. regretted delaying for so long",

    "comparison is the worst part of this journey honestly.\n\nsomeone in your group finishes the polity NCERT in one day. you took a week. feels bad even though you know everyone learns differently.\n\nhow do you deal with it",

    "i gave up on CSAT for almost a month. thought it was just qualifying, not a real threat.\n\nfailed a mock. 66 marks when i needed 67.\n\nnever skipped CSAT practice again after that",

    "there's a specific kind of tired that UPSC prep creates.\n\nnot physical tired. mentally drained from holding so much information and never feeling like it's enough.\n\nhow do you rest from that kind of tired",

    "the gap between knowing something and being able to recall it under exam pressure is huge.\n\nlearned this the hard way. knew the material. blanked on exam day.\n\nrevision fixed this more than reading ever did",

    "asked myself honestly last week — if i got the result today, would i be proud of how i prepped.\n\nthe answer was no.\n\ndidn't feel great to admit but something shifted after that",

    "people in your life don't always understand why this takes so long.\n\nexplaining why you can't just 'finish studying' is exhausting.\n\nbut this path has a very specific kind of person walking it and you're one of them",

    "there's a version of you six months ago who would be genuinely impressed by where you are now.\n\neven on the days it doesn't feel like progress.\n\nespecially on those days",

    "failing a mock isn't failing the exam. i repeated this to myself so many times it started to feel true.\n\nthen it became true.\n\nhow are you handling your mock scores right now",
]

QUIZ_HOOKS = [
    "got this wrong on my first try honestly",
    "this one's trickier than it looks",
    "took me way too long to figure this out",
    "most people guess C on this. they're wrong",
    "if you get this right without googling i'm impressed",
    "this tripped me up during practice",
    "seemed easy until i read option B carefully",
    "the answer surprised me ngl",
    "classic UPSC elimination question — looks simple until you think about it",
    "spent like 3 minutes on this. should've taken 30 seconds",
    "this is the kind of question that breaks a good score if you guess wrong",
]

# ─── Legacy pool aliases (backward compat with html_video_generator) ──────────
SHOCKING_STAT_POSTS = INSIGHT_POSTS
MYTH_BUSTER_POSTS = MYTH_BUST_POSTS
THIS_OR_THAT_POSTS = HOT_TAKE_POSTS
MOTIVATION_POSTS = STRUGGLE_POSTS


def get_day_format() -> str:
    """Get today's content format based on day of week."""
    formats = [
        "insight",    # Monday
        "hot_take",   # Tuesday
        "question",   # Wednesday
        "myth_bust",  # Thursday
        "insight",    # Friday
        "quiz",       # Saturday
        "struggle",   # Sunday
    ]
    day = datetime.now().weekday()
    return formats[day]


def format_question_post(q: dict) -> str | None:
    """Format post for X/Twitter (280 char limit).

    Quiz days: use the actual question dict with human hook.
    Non-quiz days: pick from pre-written pool — never use the question dict.
    Zero hashtags. Max 1 emoji. Zero links.
    Always ends with question or open thought.
    """
    day_format = get_day_format()

    if day_format == "quiz":
        return _format_quiz_post(q)

    pool_map = {
        "insight": INSIGHT_POSTS,
        "hot_take": HOT_TAKE_POSTS,
        "question": QUESTION_POSTS,
        "myth_bust": MYTH_BUST_POSTS,
        "struggle": STRUGGLE_POSTS,
    }
    pool = pool_map.get(day_format, INSIGHT_POSTS)
    text = random.choice(pool)
    text = _add_x_hashtags(text, q)
    return trim_to_limit(text)


def _add_x_hashtags(text: str, q: dict) -> str:
    """Add 1-2 relevant hashtags to X post. Sometimes just #UPSC, sometimes +topic."""
    subject = q.get("subject", "").lower() if q else ""
    topic_tags = {
        "polity": "#Polity", "governance": "#Polity",
        "environment": "#Environment", "ecology": "#Environment",
        "geography": "#Geography",
        "economic": "#Economy", "economy": "#Economy",
        "history": "#History",
        "science": "#ScienceTech", "technology": "#ScienceTech",
        "art": "#ArtCulture", "culture": "#ArtCulture",
        "international": "#IR",
    }
    second_tag = None
    for key, val in topic_tags.items():
        if key in subject:
            second_tag = val
            break
    # Randomly use 1 or 2 hashtags
    if second_tag and random.random() > 0.4:
        tags = f"#UPSC {second_tag}"
    else:
        tags = "#UPSC"
    return f"{text}\n\n{tags}"


def _format_quiz_post(q: dict) -> str | None:
    """Format a quiz question for X with a casual human hook."""
    opts = q.get("options", [])
    if len(opts) < 4:
        opts = [
            q.get("option_a", ""),
            q.get("option_b", ""),
            q.get("option_c", ""),
            q.get("option_d", ""),
        ]
    year = q.get("year", "")
    hook = random.choice(QUIZ_HOOKS)

    year_str = f"upsc {year}" if year else "upsc pyq"
    subject = q.get("subject", "").lower()
    # Pick 2 hashtags based on subject
    tag2 = "#PYQ"
    for key, tag in [("polity","#Polity"),("environment","#Environment"),("geography","#Geography"),
                      ("economic","#Economy"),("history","#History"),("science","#ScienceTech")]:
        if key in subject:
            tag2 = tag
            break
    text = (
        f"{hook}\n\n"
        f"{q['question']}\n\n"
        f"a) {opts[0]}\n"
        f"b) {opts[1]}\n"
        f"c) {opts[2]}\n"
        f"d) {opts[3]}\n\n"
        f"— {year_str}\n\n"
        f"#UPSC {tag2}"
    )
    return trim_to_limit(text)


def format_answer_post(q_data: dict) -> str:
    """Casual answer reveal for X/Twitter."""
    letter = q_data.get("correct_answer", "")
    answer_text = q_data.get("correct_option_text", "")
    explanation = q_data.get("explanation", "")

    templates = [
        f"answer: {letter}) {answer_text}\n\n{explanation}",
        f"it's {letter}. {explanation}\n\ndon't feel bad if you got it wrong — most people do on first try",
        f"{letter}) {answer_text}\n\n{explanation}\n\nthis is exactly why pyq practice matters",
        f"correct answer is {letter}.\n\n{explanation}",
        f"answer was {letter}) {answer_text}.\n\n{explanation}\n\ndid you get it",
    ]
    text = random.choice(templates)
    return trim_to_limit(text) or f"answer: {letter}) {answer_text}"


def build_question_data(q: dict) -> dict:
    """Extract the data needed to post the answer later."""
    return {
        "question": q["question"],
        "correct_answer": q["correct_answer"],
        "correct_option_text": q["correct_option_text"],
        "explanation": q.get("explanation", ""),
    }


def format_ig_caption(q: dict) -> str:
    """Format an Instagram caption — longer, personal, 5-8 hashtags at the END only."""
    day_format = get_day_format()
    category = q.get("category", "General Studies")
    category_tag = category.replace(" ", "").replace("&", "And")

    if day_format == "quiz":
        opts = q.get("options", [])
        if len(opts) < 4:
            opts = [q.get("option_a", ""), q.get("option_b", ""), q.get("option_c", ""), q.get("option_d", "")]
        year = q.get("year", "")
        hook = random.choice(QUIZ_HOOKS)

        body = (
            f"{hook}\n\n"
            f"{q['question']}\n\n"
            f"a) {opts[0]}\n"
            f"b) {opts[1]}\n"
            f"c) {opts[2]}\n"
            f"d) {opts[3]}\n\n"
            f"comment your answer below — answer reveal in 24 hours\n\n"
            f"#UPSC #UPSCPreparation #IAS #PreviousYearQuestions #{category_tag} #UPSCPrelims #UPSC2026"
        )
        return body

    pool_map = {
        "insight": INSIGHT_POSTS,
        "hot_take": HOT_TAKE_POSTS,
        "question": QUESTION_POSTS,
        "myth_bust": MYTH_BUST_POSTS,
        "struggle": STRUGGLE_POSTS,
    }
    pool = pool_map.get(day_format, INSIGHT_POSTS)
    core = random.choice(pool)

    hashtags = {
        "insight": f"#UPSC #UPSCPreparation #IAS #UPSCPrelims #{category_tag} #CivilServices #IASPreparation",
        "hot_take": f"#UPSC #IAS #UPSCPreparation #UPSCTips #{category_tag} #CivilServices #UPSC2026",
        "question": f"#UPSC #IAS #UPSCPreparation #{category_tag} #UPSCAspirants #CivilServices #UPSC2026",
        "myth_bust": f"#UPSC #IAS #UPSCPreparation #UPSCMyths #{category_tag} #CivilServices #IASPreparation",
        "struggle": f"#UPSC #IAS #UPSCJourney #UPSCAspirants #CivilServices #IASMotivation #UPSC2026",
    }.get(day_format, f"#UPSC #IAS #UPSCPreparation #{category_tag} #CivilServices")

    return f"{core}\n\n{hashtags}"


def format_yt_title(q: dict) -> str:
    """Engaging YouTube title — lowercase, under 60 chars + #Shorts."""
    category = q.get("category", "upsc")
    year = q.get("year", "")

    day_format = get_day_format()

    if day_format == "quiz":
        templates = [
            f"upsc asked this in {year} — can you solve it? #Shorts",
            f"this {category.lower()} question tripped everyone #Shorts",
            f"upsc {year}: most people got this wrong #Shorts",
            f"can you crack this {category.lower()} pyq? #Shorts",
            f"upsc {year} — {category.lower()} question #Shorts",
        ]
    else:
        templates = [
            "UPSC asked this 28 times in 30 years #Shorts",
            "this data changed how i study for UPSC #Shorts",
            "the UPSC pattern nobody tells you about #Shorts",
            "polity is literally one third of the paper #Shorts",
            "environment grew 7x in UPSC — are you ready #Shorts",
            "negative marking math most aspirants get wrong #Shorts",
            "i analyzed 3274 UPSC questions — here's what i found #Shorts",
            "the most repeated UPSC topic in 30 years #Shorts",
        ]

    title = random.choice(templates)
    # Enforce ~67 char max (60 + " #Shorts")
    if len(title) > 67:
        title = title[:59] + " #Shorts"
    return title


def format_yt_description(q: dict) -> str:
    """Casual YouTube description — 2-3 lines + site link."""
    day_format = get_day_format()
    category = q.get("category", "general studies")
    year = q.get("year", "")

    if day_format == "quiz":
        descs = [
            f"went through 30 years of UPSC {category.lower()} questions and pulled out this gem from {year}.\n\ntest yourself before watching the answer — comment below.\n\nfree pyq practice: {BRAND_URL}",
            f"this {category.lower()} question from UPSC {year} is trickier than it looks.\n\ntry it first. answer is in the comments.\n\nfree pyq practice: {BRAND_URL}",
            f"UPSC {year} — {category.lower()} paper.\n\ngot this wrong on my first attempt. let's see if you do better.\n\nfree pyq practice: {BRAND_URL}",
        ]
    else:
        descs = [
            "analyzed 3274 UPSC questions from 1995 to 2025 and the patterns are wild.\n\nsharing what i found so you don't have to figure it out the hard way.\n\nfree pyq practice: {BRAND_URL}",
            "been prepping for UPSC for a while and these data points genuinely changed how i study.\n\nhope this helps someone avoid my mistakes.\n\nfree pyq practice: {BRAND_URL}",
            "the exam has patterns if you look at it across 30 years.\n\nmost people don't. you should.\n\nfree pyq practice: {BRAND_URL}",
        ]

    return random.choice(descs)


def trim_to_limit(text: str) -> str | None:
    """Trim text to X character limit."""
    if len(text) <= X_CHAR_LIMIT:
        return text
    # Remove hashtag lines first
    lines = text.split("\n")
    filtered = [l for l in lines if not l.strip().startswith("#")]
    text = "\n".join(filtered).strip()
    if len(text) <= X_CHAR_LIMIT:
        return text
    # Hard truncate with ellipsis
    return text[:X_CHAR_LIMIT - 1] + "…"


# ─── Legacy format functions (kept for backward compat — used by telegram_poster
#     and html_video_generator) ──────────────────────────────────────────────

def format_shocking_stat() -> str:
    """Insight-style post — personal UPSC data discovery."""
    return random.choice(INSIGHT_POSTS)


def format_myth_buster() -> str:
    """Myth-bust post — common UPSC myth destroyed with data."""
    return random.choice(MYTH_BUST_POSTS)


def format_this_or_that() -> str:
    """Hot take post — unpopular opinion that invites debate."""
    return random.choice(HOT_TAKE_POSTS)


def format_subject_breakdown() -> str:
    """Subject breakdown — insight about specific subject weightage."""
    breakdown_posts = [
        "here's what i found after going through 3274 questions\n\npolity: 17.7%\neconomy: 15.9%\nhistory: 14.8%\ngeography: 12.5%\nenvironment: 11.6%\n\ntop three alone = almost half the paper. are you allocating time accordingly",

        "polity + economy together = 33% of prelims.\n\none third of the entire paper. two subjects.\n\nhow much of your prep time is actually going to these two",

        "environment used to be 2-3 questions per paper in the 90s.\n\nnow it's 12-15 regularly. some years even more.\n\nbeing 'okay' at environment isn't enough anymore",

        "art and culture is 6.7% of the paper — about 5-7 questions.\n\nfactual, specific, and learnable in 10-12 days of focused prep.\n\nmost people skip it for 'harder' subjects. don't be that person",

        "current affairs looks huge but it's 10% of the paper.\n\npeople spend 40% of their time on it.\n\nsome rebalancing might help",
    ]
    return random.choice(breakdown_posts)


def format_motivation() -> str:
    """Struggle/motivation post — relatable aspirant emotional content."""
    return random.choice(STRUGGLE_POSTS)


def format_quick_quiz(q: dict) -> str | None:
    """Format quiz question for social media (legacy name kept for compat)."""
    return _format_quiz_post(q)
