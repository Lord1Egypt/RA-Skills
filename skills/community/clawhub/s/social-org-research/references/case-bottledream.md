# Case Study: BottleDream Research Session

> A real-world demonstration of `social-org-research` in `depth: deep` mode.

## Background

- **Target:** BottleDream (Shanghai Bottle Dreamer Network Technology Co., Ltd.) — China's 5th B Corp, first media-type B Corp, a social innovation content platform.
- **Date:** September 2026
- **Depth:** `deep` (4 iterative sessions over 2 hours)
- **Triggering user questions:**
  1. "Help me deep-research BottleDream" (initial brief)
  2. "Output as PDF attachment" (format requirement)
  3. "Is the event execution done by themselves, or by a contracted team?" (deep dive 1)
  4. "Do volunteers / interns / co-creators get paid? What benefits?" (deep dive 2)
  5. "Save this as a reusable prompt for similar research" (final ask — became this skill)

---

## Dimensions Executed (deep mode — all 10)

| # | Dimension | Sources consulted | Key finding |
|---|-----------|-------------------|-------------|
| 1 | Company body | Aiqicha, Tianyancha, B Lab | Two legal entities: Guangzhou Kaige Bottle Network Tech (early) + Shanghai Bottle Dreamer Network Tech (Jan 2017, ¥1M reg capital, ¥9K paid-in, founder as legal rep). |
| 2 | Brand & history | 36Kr, iFeng, LinkedIn, WEF | Founded 2011-06-01; cofounder 衷声 as CEO since 2016; B Corp certified 2017-08-03 (5th in mainland China, 1st media-type). |
| 3 | Business model | 36Kr 2017, Impact Garden | Two revenue axes: media business + Bottleverse sponsorship; breakeven by 2017; NO equity funding disclosed. |
| 4 | Content & methodology | 36Kr CEO interview, China Development Brief, Yixi talk | "Appreciative Inquiry" + #For Good# framework; daily-life categorization instead of academic; ~1000 changemaker stories, 200M cumulative reach. |
| 5 | Activity system | 36Kr retrospective, Sina Finance 2019, NetEase 2025 | Bottleverse festival (2016-2025, 5 editions); 10 core team + 100 volunteers for 2017 second edition; 65 co-creators; 520 attendees + 11M livestream + 180M exposure. |
| 6 | People incentives | WonderCV 2026 intern posting, NetEase 2025 volunteer recruitment | 5 identity types with different incentive models; interns: subsidized (est. ¥150-200/day); volunteers: NO cash, only meal + T-shirt + immersive experience (housing/travel self-funded except 6 "guest angels"). |
| 7 | Co-creation network | Sina Finance 2019, NetEase 2025, Impact Garden | 5 categories: joint hosts (FAO/WWF/SK/小红村) + strategic (Unilever/JD/Robam/IKEA/SK) + content (200+ changemakers) + venue (West Bund Art Center / Anji Yucun) + platform (Weibo/Youku/NetEase). |
| 8 | Team & culture | LinkedIn, WonderCV, WEF | 5 core team members, mostly media/journalism backgrounds; "gentle CEO" culture; visible internal volunteer culture (BD staff volunteer at other NGO camps). |
| 9 | Funding & legal | Narada Foundation, LinkedIn, Aiqicha | ¥40K small grant from Narada Foundation 2016; ¥0 disclosed equity funding; registered capital likely under-states actual scale. |
| 10 | Information gaps | Cross-referenced | Annual revenue/profit, employee headcount, intern salary exact, volunteer count per edition, partner ROI — all "not publicly disclosed." |

---

## Output Artifacts

| Artifact | Size | Verification |
|----------|------|--------------|
| Markdown source | 40.6 KB | Single source of truth for the report |
| PDF deliverable | 2.35 MB, 18 pages A4 | VBC: 35 source links = 35 matched links = 42 /Link rectangles; all URIs HTTP(S); Chinese rendering OK |

---

## Three Iterative Deep-Dives

The user's research questions evolved from a single "tell me about BottleDream" into three follow-up probes — exactly the kind of iterative behavior this skill supports.

### Deep dive 1: Activity execution model

User question: "Is the event execution done by themselves, or by a contracted team?"

Execution: Pulled 36Kr long-form retrospective from CEO 衷声 (the canonical "how we built Bottleverse 2017" article), cross-referenced with Sina Finance 2019 third-edition recap, plus WonderCV 2026 intern posting for role definitions and Journal of Futures Studies 2021 academic paper citing BD as example.

Output: Added 9-section "Activity execution model" sub-chapter with role split table (BD core team / volunteers / co-creators / 3rd-party vendors), per-edition staffing data, 4 worked co-creation examples (Henong Organic, Robam, SK Group, Xiaohongshu Philanthropy).

### Deep dive 2: People incentives

User question: "Do volunteers / interns / co-creators get paid? What benefits? How do they attract volunteers?"

Execution: Pulled NetEase 2025-05-16 volunteer recruitment post (the canonical "what we offer volunteers" doc), WonderCV 2026 intern posting (the canonical "what we offer interns" doc), cross-referenced with industry salary benchmarks (Charity Box: ¥133-177/day, Enpai Foundation: ¥100-120/day), plus the Volunteer Service Regulations for legal framework.

Output: Added 8-section "People incentives" sub-chapter with 5-identity table, full volunteer benefits list (5 non-cash hooks), intern compensation structure (3 salary estimates), co-creator value exchange model, financial flow diagram (who pays whom), industry comparison table.

### Outcome: Skill meta-reflection

User question: "Save this as a reusable prompt for similar research."

Execution: The skill's own existence. The 10 dimensions and 8 Pitfalls were distilled directly from this session's evidence.

---

## Lessons Learned (encoded into the skill)

1. "Registered capital ≠ actual scale" — always cross-check LinkedIn + B Lab + office size.
2. "Co-creator ≠ sponsor" — clarify before designing the survey.
3. "Volunteers in China are statutorily unpaid" — separate the legal fact from the benefits discussion.
4. "5 non-cash hooks" framework for explaining how non-monetary organizations attract people.
5. "MD is single source of truth" + "VBC the links PDF" — output deliverable structure.
6. "Founder story ≠ org reality" — separate founder's narrative from team execution.

---

## Reproducing This Case

```
Research BottleDream, depth: deep
```

Replace "BottleDream" with any other social innovation organization. The skill will run all 10 dimensions and produce equivalent Markdown + PDF outputs.
