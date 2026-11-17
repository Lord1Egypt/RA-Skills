---
name: social-org-research
description: 'Research a B Corp / social enterprise / NGO / youth culture brand. 10-dimension framework, depth: quick|deep switch, case study included.'
version: 0.1.0
author: 0xcjl
license: MIT
category: research
metadata:
  hermes:
    tags: [research, social-enterprise, b-corp, ngo, social-innovation, youth-culture, content-strategy, b-impact-assessment, sustainability, due-diligence]
    related_skills: [market-research, deep-research, md-pdf-report, kanban-use, anti-sycophancy]
---

# Social-Org Research · Research Prompt for B Corps, Social Enterprises, NGOs, and Youth Culture Brands

**One prompt, two depth modes** — toggle with `depth: quick | deep`.

- **quick**: ~30 minutes, ~3 A4 pages. Covers only the 4 ⚡ dimensions (company body, brand & history, business model, content & methodology).
- **deep**: ~3-4 hours, ~15-20 A4-page PDF. Covers all 10 dimensions with VBC-verified clickable-link PDF output.

**Why this skill differs from `market-research`**: targets organizations whose business mixes revenue with mission — sponsored content, donor relationships, volunteer labor, paid partnerships with global NGOs, government grants, and "co-creator" rather than "sponsor" brand relationships.

---

## When to Use

| Trigger / Scenario | Action |
|--------------------|--------|
| "Research BottleDream" / "look into that B Corp" / "social enterprise X" | Use this skill |
| "How does this NGO make money?" / "who actually runs their events?" / "are volunteers paid?" | Use this skill |
| "Youth culture brand Y's content + community model" | Use this skill |
| Standard commercial due diligence | Use `market-research` |
| Academic literature review | Use `academic-research` or `deep-research` |

---

## Core Framework: 10 Research Dimensions

Run **deep** for all 10. **quick** runs only the 4 ⚡ dimensions.

### ⚡ Dimension 1: Company Body
- Legal entities (full registered name, unified social credit code, founding date, registered capital / paid-in, registered address, legal representative)
- Organizational structure (affiliates, subsidiaries, parallel projects from same team)
- Team size (LinkedIn headcount / Crunchbase / B Lab scoring)
- Sources: Tianyancha / Aiqicha / Qixin / National Enterprise Credit Information Publicity System

### ⚡ Dimension 2: Brand & History
- Slogan / mission / vision
- Key timeline (founding / turning points / certifications / landmark partnerships)
- Founder story (one-paragraph trajectory + core DNA)
- B Corp / co-benefit / social enterprise certifications (if any, attach B Impact Assessment score)

### ⚡ Dimension 3: Business Model
- Revenue categories (media / content sponsorship / training / consulting / co-branded products / event sponsorship)
- Customer structure (brand partners / NGO partners / government / international orgs)
- Business model classification: B2B / B2C / B2B2C / co-creation / impact investment
- Financial status: disclosed funding / revenue / profit (rarely available — annotate)

### ⚡ Dimension 4: Content Production & Methodology
- Content formats (text / video / documentary / podcast / live events / curatorial)
- Core methodology (e.g., "Appreciative Inquiry" + #For Good# framework — case study patterns)
- Narrative emphasis (what categorization is used to organize topics; what rhetoric attracts target audience)
- Cumulative reach / user base / distribution metrics

### Dimension 5: Activity System
- Activity types (flagship IP / recurring events / cross-sector collaborations / co-creation competitions)
- Per-edition scale (date / venue / attendees / co-creator count / distribution)
- **Execution model** — internal team / volunteers / co-creators / 3rd-party vendors role split
- Per-edition execution flow (theme design → outreach → co-creation → on-site → retrospective)

### Dimension 6: People Incentives & Benefits
Examine **5 identity types** separately:

| Identity | What to find |
|----------|--------------|
| Full-time employees | Salary range, social insurance, employee benefits (B Corp dimensions) |
| Interns | Stipend, certificate, conversion opportunity |
| **Activity volunteers** | Cash? Meals? Housing/travel self-funded? Merch? Experience? Certificate? |
| **CAMPer / changemaker / co-creator** | Bring your own plan, or pay booth fee? What exposure & rights do they get? |
| Competition participants | Prize? Mentorship? Overseas exchange? |

### Dimension 7: Co-creation Network
- **Joint hosts** (international NGO / government / large foundation / major IP)
- **Strategic co-creators** (brands bringing core products / channels to solve the theme)
- **Content co-creators** (individual changemakers / small orgs bringing their own exhibits)
- **Venues / residencies** (physical space + government backing)
- **Platform partners** (traffic distribution / joint hashtag initiatives)

### Dimension 8: Team & Culture
- Founding team backgrounds (education / career / media-journalism ratio)
- Cultural keywords (slogan / tone / visual aesthetic)
- Advisors / industry backing (Forbes / Davos / industry awards)
- Internal volunteer culture (e.g., staff also volunteer at other NGO camps)

### Dimension 9: Funding & Legal
- Funding history (VC / impact investment / patient capital)
- Foundation grants (Narada / Leping / Ford / UN)
- Government programs (cultural development special funds / entrepreneurship subsidies)
- Registered vs paid-in capital
- Tax incentive eligibility (charitable donation pre-tax deduction / non-profit tax exemption)

### Dimension 10: Information Gaps (honestly annotated)
- What data is officially undisclosed
- What data is inferred (e.g., "estimated salary range" must be flagged)
- What data is single-point snapshot (e.g., registered capital from one filing ≠ current scale)

---

## Reusable User Prompt Template

Copy-paste this to Helen and fill in `[target]` and `depth`:

```
Research [target company / brand name], depth: [quick | deep]

Please cover the following dimensions (deep = all 10; quick = first 4 ⚡):
1. Company body (registered capital / team size)
2. Brand & history
3. Business model (revenue / customers / model)
4. Content production & methodology
5. Activity system (types / scale / execution model / role split)
6. People incentives & benefits (full-time / interns / volunteers / CAMPer / participants)
7. Co-creation network (joint hosts / strategic / content / venue / platform)
8. Team & culture
9. Funding & legal
10. Information gaps (honestly annotated)

Output requirements:
- Markdown + PDF, both deliverables
- PDF must use weasyprint + pikepdf two-stage (md-pdf-report skill's scripts/md2pdf_with_links.py)
- Every claim attached to [source](url) link
- VBC four steps: ① pdfinfo pages OK ② pikepdf /Annots ≥ MD link count × 0.5 ③ re-open PDF check all URIs HTTP(S) ④ pdftotext sample page Chinese rendering OK
- Standalone empty lines / tables / hierarchical headings
- "Unverified" and "Inferred" must be explicitly labeled
```

---

## Information Source Priority (highest to lowest credibility)

| Tier | Sources | Use case |
|------|---------|----------|
| ★★★★★ | B Lab certification page / National Enterprise Credit Information Publicity System / Official website | Company body, certifications |
| ★★★★☆ | LinkedIn company page / Crunchbase / 36Kr / Yixi / iFeng Philanthropy | Team, history, partnerships |
| ★★★★☆ | Founder / executive public talks (video / podcast / WeChat OA) | Culture, tone |
| ★★★☆☆ | Mainstream financial media (Jiemian / The Paper / Sina reposts) | Historical events, distribution |
| ★★★☆☆ | Recruiting platforms (WonderCV / Shixiseng / Miaoruzhi / Lagou) | Intern benefits, role details |
| ★★★☆☆ | Academic literature (Journal of Futures Studies / CNKI) | Third-party observation |
| ★★☆☆☆ | Tianyancha / Aiqicha | Registered capital (note: ≠ actual scale) |
| ★★☆☆☆ | Digitaling / BrandStar / SocialBeta | Creative industry observation |
| ★☆☆☆☆ | Zhihu / Xiaohongshu / Jike | Intern reviews, industry sentiment (watch for UGC bias) |
| ★☆☆☆☆ | Mass-media secondary reposts | Cross-verification only |

---

## Key Pitfalls (real lessons from the field)

### 1. Registered capital ≠ actual scale
- A ¥1M registered / ¥9K paid-in company can still be a 50-person operation
- **Always cross-check** LinkedIn headcount + B Lab score + office size

### 2. "Non-profit / public-interest" label ≠ not making money
- B Corp / social enterprise / co-benefit = company that solves social problems with commercial means
- Asking "how do they make money?" is the **right** question, not an insult

### 3. Volunteers in China are statutorily unpaid
- Volunteer Service Regulations (志愿服务条例) mandates "voluntary, unpaid, public-spirited, organized"
- Cannot charge fees under the name of volunteer service
- **But** can provide: meals / T-shirts / merch / experience / certificates / training / priority access
- Analyze via **"5 non-cash hooks"**: identity marker / scarce experience / skill building / network access / résumé credit

### 4. "Co-creator" vs "sponsor" are two different relationships
- Co-creator: brings plan + resources + product to solve the issue (e.g., JD brings products to match the theme)
- Sponsor: pays for naming rights (traditional event sponsorship)
- The moat for top social-org players is the former, not the latter

### 5. "X people impacted" claims are vague
- "Inspired 150,000+ Chinese young people" (B Lab)
- "200,000+ subscribers" (WeChat OA)
- "Cumulative reach 200M" (LinkedIn)
- **Always tag with date + source** — these are point-in-time snapshots, not cumulative

### 6. Founder story ≠ organization reality
- Founder's personal narrative is brand asset, not operating reality
- Distinguish founder's story from the team's day-to-day execution

### 7. "Impacted X people" / "co-created with Y orgs" is marketing speak
- Third-party observation (academic / media) is more credible than self-report
- Cross-reference with peer-reviewed or independent coverage

### 8. Social-org players are "content companies," not "event companies"
- Core KPI is content reach, not ticket revenue
- Events are a content vehicle, not the end goal
- When asking "what does this organization live on," ask about content capability, not event revenue

---

## Skill Coordination

| Coordinate with | When |
|-----------------|------|
| `md-pdf-report` | To generate the PDF deliverable (must use two-stage weasyprint + pikepdf) |
| `market-research` | If the target is a commercial company, not a social enterprise |
| `deep-research` | If you need maximum depth (academic literature review / multi-language sources) |
| `kanban-use` | If you want to delegate research tasks to sub-agents in parallel |
| `anti-sycophancy` | Strip any "amazing organization" or "so inspiring" framing — objective facts only |

---

## Maintenance Notes

- After each real research project, append newly-discovered Pitfalls to the section above
- When new high-quality information sources appear (e.g., new industry databases), add to the priority table
- When a dimension is unsearchable for a particular org (e.g., "no funding ever"), document it in the "Information gaps" handling template
