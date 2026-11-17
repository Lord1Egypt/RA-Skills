# Research basis

**Checked: 2026-10-04.** Research-backed here means the sources motivate editing checks. It does not mean this prompt has reproduced a paper's results. The search is not an exhaustive census of all models, languages, or AI writing habits.

## Recent arXiv findings

| Source and inspected version | Finding used | Limit on applying it |
| --- | --- | --- |
| [SlopBench](https://arxiv.org/abs/2609.33905v1), 2026-09-27; sections 3–8 and Appendix A | Separates length, opener reuse, paragraph rhythm, and lexical constructions across ordinary writing tasks. | Version, route, and task matter; rankings are unstable. Corpus-relative surface measures do not establish overall writing quality. |
| [Science or Slop?](https://arxiv.org/abs/2610.00531v1), 2026-09-30; sections 3–4 | Scientific slop includes failures connecting claims, arguments, and artifacts; revisions should be grounded in supplied records. | Its harness and evaluation are not this editing skill. A sentence that sounds better may still be unsupported. |
| [Citing Less Critically](https://arxiv.org/abs/2609.01432v1), 2026-09-01; methods and results | Six tested models softened critical citation intent in reconstructed citation sentences. | GPT-5.1, Claude 3.5 Haiku, Gemini 2.0 Flash, DeepSeek V3.2, Llama 4 Maverick, and Qwen 2.5-72B; this is not a direct test of style-preserving edits. |
| [Measuring AI “Slop” in Text](https://arxiv.org/abs/2509.19163v2), revised 2026-01-24; taxonomy and evaluation | Slop involves usefulness, information quality, and style, with subjective judgments. | A stock-word count alone cannot cover these dimensions; the paper does not validate a universal current-family blacklist. |
| [Antislop](https://arxiv.org/abs/2510.15061v2), revised 2025-10-21; section 3 and Appendix K | Compares recurring phrases with human baselines; patterns vary by model and writing domain. | Main experiments concern Gemma 3 12B, Mistral Small 3.2, and Llama 3.3 70B. Sampler/fine-tuning results do not establish prompt-only performance. |
| [Visual Fingerprints for LLM Generation Comparison](https://arxiv.org/abs/2605.06054v1), 2026-05-07 | Compares distributions of linguistic choices under different generation conditions. | A single response cannot establish a model's habitual frequency; system instructions and sampling matter. |
| [Detecting Stylistic Fingerprints of Large Language Models](https://arxiv.org/abs/2503.01659v1), 2025-03-03 | Finds stylistic signals across model families. | Classification evidence does not supply a current family's list of defects or a writing-quality measure. |

The editing applications are our inferences: review whole constructions, keep real disagreement, preserve voice, and flag evidence gaps. Do not present these applications as interventions tested by the paper authors. In particular, the newer scientific-slop study gives another reason to avoid polishing an unsupported argument into apparent certainty.

## Sentence structure and genre

Additional sources checked 2026-10-04:

- [Do LLMs write like humans?](https://arxiv.org/html/2410.16107v2), arXiv v2, revised 2025-08-21; published in PNAS in 2025. Parallel human and model corpora show differences in grammatical and rhetorical feature use for GPT-4o and Llama 3 variants. This supports reviewing more than vocabulary; it does not test a three-part-pattern ban or this editing prompt.
- [Interpretable Stylistic Variation](https://arxiv.org/html/2604.14111v1), 2026-04-15. Analysis of 11 models across eight genres finds genre has a stronger influence on the studied stylistic features than human/model source. Its RAID corpus uses older models; publication in 2026 does not make it evidence about every current model family.
- [Linguistic and Embedding-Based Profiling](https://arxiv.org/html/2507.13614v1), 2025-07-18, sections 5.1 and 5.6-5.7. Human texts show greater variability in the studied linguistic feature space, with genre-dependent results. Average sentence length has no clear pattern across humans and models. Variability across texts and genres does not establish a required within-paragraph alternation of sentence lengths.
- [SlopBench](https://arxiv.org/html/2609.33905v1), 2026-09-27, section 4.1. Rhythm is measured using paragraph-length variation, and separates models only for email. Its rule-of-three check compares occurrence rates to human baselines; it does not establish that each instance is bad writing.

Our editorial application is to preserve a natural mix of sentence structures and meaningful repetition, suited to the genre. Review repeated openings, clause shapes, and rhetorical moves when they make a paragraph sound mechanical. Keep an effective marketing tagline. These papers do not establish sentence-length variance as the strongest human-writing signal, an ideal short/long sentence ratio, or a blanket ban on three-part phrasing. Prompt effectiveness still needs direct testing.

## Supplemental primary dataset

[Mapping LLM Style and Range in Flash Fiction](https://github.com/lechmazur/writing_styles), December 2025 update, contains 29 models and 15,347 short stories, with LLM-based style judgments. Its linked head-to-head summaries support conditional phrase and closure checks in the family profiles. These are narrower, weaker foundations than replicated human editing trials, and the fiction genre limits transfer to other tasks. Each profile links the specific comparison it uses.

Do not infer that a positive ending, internal reflection, rich imagery, or bilingual voice is intrinsically defective. A tendency becomes an editing concern when it is unwanted, repetitive, unsupported, or obstructs the draft's purpose.

## Editorial preferences and research are distinct

Plain language, direct verbs, economy, natural sentence variation, and preservation of meaning are editorial principles. The checks for canned humor, unsolicited defensive framing, and unnecessary negation also reflect the requested editing style. They are not all experimentally validated AI tells. We publish them as useful editing decisions, not evidence that an author or model produced a passage.

Future profiles should name the model version, task, sampling or route when known, source, and date. Add a family trait only when an observation supports it. Recheck the actual text and keep the general fallback for unstudied versions. Non-English editing needs language-specific evidence; do not impose English phrasing rules on another language.
