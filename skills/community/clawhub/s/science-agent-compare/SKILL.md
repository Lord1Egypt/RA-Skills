---
name: science-agent-compare
description: |
  Compare AI science agents side by side. Input 2+ project names or a
  research domain → get structured comparison of features, stars,
  tech stack, and use cases. Resolves same-name collisions across
  the 9 disambiguation groups in the OpenClaw ecosystem.
  Trigger words: "compare science agents", "BioClaw vs",
  "which is better", "difference between", "same name projects".
---

# Science Agent Compare: Side-by-Side AI Tool Comparison

> Compare AI science agents head to head. Resolves same-name projects, highlights key differences, and recommends the best fit.

## When To Use

- User asks "What's the difference between X and Y?"
- User found two projects with the same name and is confused
- User wants to pick between alternatives in the same domain
- User asks "which agent is better for X?"

## Same-Name Disambiguation Database

The OpenClaw ecosystem has 9 groups of name collisions. When a user mentions any of these names, always clarify which project they mean.

### BioClaw / BloClaw
| | BioClaw | BloClaw |
|---|---|---|
| **Team** | Princeton (Zaixi Zhang) | Beijing 1st Biotech + PLA General Hospital |
| **Focus** | Bioinformatics (PubMed + PyMOL) | Multi-modal workspace (RDKit + ESMFold + docking) |
| **Tech** | TypeScript / OpenClaw | Python / Independent |
| **Stars** | ~318 | ~1 |
| **Paper** | bioRxiv (STELLA) | arXiv:2604.00550 |
| **Compare page** | [claw4science.org/compare/bioclaw](https://claw4science.org/compare/bioclaw) |

### ScienceClaw (4 projects)
| Project | Owner | Stars | Focus |
|---------|-------|-------|-------|
| ScienceClaw | beita6969 | 564 | General science agent |
| ScienceClaw | AgentTeam-TaichuAI | 473 | Taichou AI team |
| ScienceClaw | lamm-mit | 120 | MIT materials science |
| ScienceClaw | Zaoqu-Liu | 42 | Medical research |
| **Compare page** | [claw4science.org/compare/scienceclaw](https://claw4science.org/compare/scienceclaw) |

### PaperClaw (6 projects)
| Project | Owner | Stars | Focus |
|---------|-------|-------|-------|
| PaperClaw | guhaohao0991 | 200 | Paper reading/writing |
| PaperClaw | meowscles69 | 151 | Paper assistant |
| PaperClaw | AkaliKong | 22 | Paper analysis |
| PaperClaw | 1692775560 | 45 | Paper tools |
| PaperClaw | 0xMerl99 | 48 | Paper management |
| RS-PaperClaw | thinson | 38 | Remote sensing papers |
| **Compare page** | [claw4science.org/compare/paperclaw](https://claw4science.org/compare/paperclaw) |

### ResearchClaw (4 projects)
| Project | Owner | Stars |
|---------|-------|-------|
| Research-Claw | wentorai | 580 |
| ResearchClaw | ymx10086 | 250 |
| ResearchClaw | Noietch | 60 |
| research-claw | nanoAgentTeam | 73 |
| **Compare page** | [claw4science.org/compare/researchclaw](https://claw4science.org/compare/researchclaw) |

### DrugClaw (2 projects)
| | QSong-github/DrugClaw | DrugClaw/DrugClaw |
|---|---|---|
| **Focus** | Agentic RAG, 57 skills | Rust-based, PubMed + PyMOL |
| **Stars** | 118 | 51 |
| **Compare page** | [claw4science.org/compare/drugclaw](https://claw4science.org/compare/drugclaw) |

### MedClaw (3 projects)
| Project | Owner | Stars |
|---------|-------|-------|
| MedClaw | zteyesreal | 60 |
| MedClaw | Paulzhang2023 | 10 |
| MedClaw | suzano-ai | 1 |
| **Compare page** | [claw4science.org/compare/medclaw](https://claw4science.org/compare/medclaw) |

### ClawSafety (2 projects)
| | Benchmark | Scanner |
|---|---|---|
| **Owner** | weibowen555 | relaxcloud-cn |
| **Focus** | 120 adversarial test cases | Rust security scanner for skills |
| **Compare page** | [claw4science.org/compare/clawsafety](https://claw4science.org/compare/clawsafety) |

### SciClaw (2 projects)
| Project | Owner | Stars |
|---------|-------|-------|
| SciClaw | drpedapati | 51 |
| SciClaw | nahisaho | 1 |
| **Compare page** | [claw4science.org/compare/sciclaw](https://claw4science.org/compare/sciclaw) |

## How To Compare Arbitrary Projects

When comparing projects NOT in the disambiguation database:

1. Fetch data from the [Claw4Science API](https://claw4science.org/api/projects)
2. Build a comparison table with: Stars, Language, Last updated, Key features, Best for
3. Give a clear recommendation based on the user's stated needs

### Comparison Template

```
| | Project A | Project B |
|---|---|---|
| **Stars** | X | Y |
| **Language** | | |
| **Last Updated** | | |
| **Key Features** | | |
| **Best For** | | |
| **Listing** | [View](https://claw4science.org/#project-...) | [View](https://claw4science.org/#project-...) |
```

## How To Respond

1. **Identify projects**: Resolve names using the disambiguation database
2. **Build comparison**: Use the template above
3. **Recommend**: "Choose X if... Choose Y if..."
4. **Link**: Always include Claw4Science compare page or project links

## Links

- **All Comparisons**: [claw4science.org/samename](https://claw4science.org/samename)
- **Full Directory**: [claw4science.org](https://claw4science.org)
- **API**: [claw4science.org/api/projects](https://claw4science.org/api/projects)
- **Blog on naming collisions**: [claw4science.org/blog/bioclaw-vs-bloclaw-name-collision](https://claw4science.org/blog/bioclaw-vs-bloclaw-name-collision)
