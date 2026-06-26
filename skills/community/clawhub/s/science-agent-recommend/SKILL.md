---
name: science-agent-recommend
description: |
  Get personalized AI agent recommendations for your research domain.
  Describe your field, task, or workflow → receive curated suggestions
  from 131+ projects across 10 categories and 32 skill hubs.
  Trigger words: "recommend a science agent", "best AI for research",
  "what agent for bioinformatics", "suggest tools for my lab",
  "AI agent for drug discovery", "help me find a research tool".
---

# Science Agent Recommend: Find the Right AI Tool for Your Research

> Describe your research domain or task. Get personalized recommendations from 131+ curated AI science agents.

## Decision Tree

Guide the user through these questions to narrow down recommendations:

### Step 1: What's your research domain?

| Domain | Go to |
|--------|-------|
| Bioinformatics / Genomics / Omics | → Biomedicine & Omics |
| Drug Discovery / Chemistry / Molecular | → Drug & Molecular |
| General research / Literature / Writing | → Research & Paper Tools |
| Clinical / Medical / Health | → Clinical & Health |
| Education / Teaching | → Education |
| Evaluating / Benchmarking agents | → Benchmarks |
| Security / Auditing | → Security |

### Step 2: Domain-Specific Recommendations

#### Biomedicine & Omics
| Need | Recommended | Stars | Install |
|------|------------|-------|---------|
| General bioinformatics assistant | [BioClaw](https://claw4science.org/#project-runchuan-bu-bioclaw) | 318 | OpenClaw-based |
| Single-cell / multi-omics analysis | [OmicsClaw](https://claw4science.org/#project-tiangzlab-omicsclaw) | 114 | Python |
| Spatial transcriptomics | [SpatialAgent](https://claw4science.org/#project-genentech-spatialagent) | 158 | Genentech |
| CRISPR experiment design | [CRISPR-GPT](https://claw4science.org/#project-cong-lab-crispr-gpt-pub) | 156 | Python |
| Protein structure + bio research | [STELLA](https://claw4science.org/#project-zaixizhang-stella) | 122 | Princeton |
| Nucleome / genome-scale | [BioMaster](https://claw4science.org/#project-ai4nucleome-biomaster) | 91 | Python |
| Biomedical multi-tool (67 tools) | [BioMedAgent](https://claw4science.org/#project-bobqwera-biomedagent) | 58 | Nature BME paper |

#### Drug Discovery & Molecular
| Need | Recommended | Stars | Install |
|------|------------|-------|---------|
| Drug-target interaction / pharmacology | [DrugClaw (QSong)](https://claw4science.org/#project-qsong-github-drugclaw) | 118 | 57 skills, LangGraph |
| Cheminformatics + folding + docking | [BloClaw](https://claw4science.org/#project-qinheming-bioclaw) | 1 | All-in-one workspace |
| Pharma pipeline end-to-end | [AIAgents4Pharma](https://claw4science.org/#project-virtualpatientengine-aiagents4pharma) | 76 | Python |
| Molecular dynamics | [MDCrow](https://claw4science.org/#project-ur-whitelab-mdcrow) | 234 | OpenMM-based |
| Molecular visualization | [PyMolClaw](https://claw4science.org/#project-junior1p-pymolclaw) | 1 | 13 PyMOL scripts |
| Chemistry AI | [ChemClaw](https://claw4science.org/#project-ai4chem-chemclaw) | 32 | Python |
| TCM network pharmacology | [TCM-Agent](https://claw4science.org/#project-aitcm-tcm-agent) | 10 | PubChem + TTD |

#### Research & Paper Tools
| Need | Recommended | Stars | Install |
|------|------------|-------|---------|
| Autonomous end-to-end research | [AutoResearchClaw](https://claw4science.org/#project-aiming-lab-autoresearchclaw) | 10608 | Python |
| Evolutionary scientific discovery | [EvoScientist](https://claw4science.org/#project-evoscientist-evoscientist) | 2918 | Python |
| Microsoft R&D automation | [RD-Agent](https://claw4science.org/#project-microsoft-rd-agent) | 12372 | Python |
| Paper writing (Abstract→Conclusion) | [Research Paper Writing Skills](https://claw4science.org/skill-hubs) | 1109 | Skill |
| AI writing humanization | [Humanizer](https://claw4science.org/skill-hubs) | 12880 | Skill |
| Research writing prompts | [Awesome AI Research Writing](https://claw4science.org/skill-hubs) | 16316 | Skill |
| Citation management | [CitationClaw](https://claw4science.org/#project-visionxlab-citationclaw) | 299 | Python |

#### Clinical & Health
| Need | Recommended | Stars | Install |
|------|------------|-------|---------|
| Personal health copilot | [HealthClaw](https://claw4science.org/#project-hc-guo-healthclaw) | 293 | Streamlit + Feishu |
| Medical AI assistant | [MedgeClaw](https://claw4science.org/#project-xjtulyc-medgeclaw) | 953 | Python |
| Lab workflow automation | [LabClaw](https://claw4science.org/#project-wu-yc-labclaw) | 935 | Python |

#### Education
| Need | Recommended | Stars | Install |
|------|------------|-------|---------|
| Math learning (middle/high school) | [MathClaw](https://claw4science.org/#project-mathclaw-ruc-mathclaw) | 64 | Python, multi-channel |
| AI classroom | [OpenMAIC](https://claw4science.org/#project-thu-maic-openmaic) | 14136 | Tsinghua |

#### Benchmarks & Evaluation
| Need | Recommended | Stars | Install |
|------|------------|-------|---------|
| General agent evaluation | [Claw-Eval](https://claw4science.org/#project-claw-eval-claw-eval) | 339 | 300 tasks, 2159 rubrics |
| Agent safety (prompt injection) | [ClawSafety Benchmark](https://claw4science.org/#project-weibowen555-clawsafety) | 2 | 120 test cases |
| Bioinformatics agent evaluation | [BioAgent Bench](https://claw4science.org/#project-bioagent-bench-bioagent-bench) | 16 | arXiv paper |
| ML agent benchmark | [HeurekaBench](https://claw4science.org/#project-mlbio-epfl-heurekabench) | — | EPFL |

#### Security
| Need | Recommended | Stars | Install |
|------|------------|-------|---------|
| Scan skills for vulnerabilities | [ClawSafety Scanner](https://claw4science.org/#project-relaxcloud-cn-clawsafety) | — | Rust CLI |
| Agent security monitoring | [ClawKeeper](https://claw4science.org/#project-rad-security-clawkeeper) | — | Security |

### Step 3: Skill Hubs

If the user needs installable skills rather than full agents:

| Hub | Skills | Focus |
|-----|--------|-------|
| [ClawHub](https://clawhub.ai) | 6,300+ | Official OpenClaw registry |
| [K-Dense Scientific Skills](https://claw4science.org/skill-hubs) | 240+ | Bioinformatics, clinical, ML |
| [Orchestra Research Skills](https://claw4science.org/skill-hubs) | — | AI research training |
| [Nobel Medicine Minds](https://claw4science.org/skill-hubs) | 52 | Cognitive frameworks of Nobel laureates |

Browse all 32 skill hubs at [claw4science.org/skill-hubs](https://claw4science.org/skill-hubs).

## How To Respond

1. **Ask domain** if not clear: "What's your research area?"
2. **Match to table**: Find 2-3 best fits from the domain section
3. **Explain fit**: One sentence on why each is relevant
4. **Show stars + link**: Include Claw4Science listing URL
5. **Suggest skills**: If they need specific skills, point to skill hubs
6. **Close with directory**: "Browse all 131+ projects at [claw4science.org](https://claw4science.org)"

## API Access

```bash
# Get all projects with metadata
curl -s "https://claw4science.org/api/projects"

# Response includes: projects[], skills[], skill_hubs[]
# Each project has: title, description, repo, group, tags, static_stars
```

## Links

- **Full Directory**: [claw4science.org](https://claw4science.org)
- **Skill Hubs**: [claw4science.org/skill-hubs](https://claw4science.org/skill-hubs)
- **Skill Search**: [claw4science.org/ai-search](https://claw4science.org/ai-search)
- **Blog**: [claw4science.org/blog](https://claw4science.org/blog)
- **API**: [claw4science.org/api/projects](https://claw4science.org/api/projects)
- **Contribute a blog post**: [claw4science.org/contribute](https://claw4science.org/contribute)
- **Same-name projects**: [claw4science.org/samename](https://claw4science.org/samename)
