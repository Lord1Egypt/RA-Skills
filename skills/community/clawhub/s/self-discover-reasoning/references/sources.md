# SELF-DISCOVER Reasoning — Academic Sources

## Core Paper

### SELF-DISCOVER: Large Language Models Self-Compose Reasoning Structures
- **Authors:** Zhou, Agarwal, Hé, Zoph, Xiong, Keutzer, Dean
- **Year:** 2024 (NeurIPS)
- **URL:** https://arxiv.org/abs/2402.03660
- **Key finding:** >20% improvement over CoT-Self-Consistency on challenging reasoning benchmarks (BigBench-Hard, MATH, AQuA), while using 10-40x fewer inference computations. Models self-compose reasoning structures from atomic building blocks.
- **What we use:** Core SELECT → ADAPT → IMPLEMENT pipeline, seed reasoning modules, structure composition.

## Foundational Techniques

### Tree of Thoughts: Deliberate Problem Solving with Large Language Models
- **Authors:** Yao, Li, Liu, Wu, Ammanabrolu, Smith, Yang, Liu
- **Year:** 2023 (NeurIPS)
- **URL:** https://arxiv.org/abs/2305.10601
- **Key finding:** Exploring multiple reasoning paths in a tree structure dramatically improves planning and search tasks.
- **What we use:** The idea of structured exploration of reasoning space — SELF-DISCOVER operationalizes this as composable modules.

### Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning
- **Authors:** Wang, Xu, Moon, Wu, Liu
- **Year:** 2023 (ACL)
- **URL:** https://arxiv.org/abs/2305.04091
- **Key finding:** Decomposing reasoning into explicit planning and execution phases improves over zero-shot CoT.
- **What we use:** The planning-first paradigm that SELF-DISCOVER builds upon.

### Large Language Models as Analogical Reasoners
- **Authors:** Yasunaga, Chen, Wang, Li, Percy, Liang
- **Year:** 2024 (ICLR)
- **URL:** https://arxiv.org/abs/2310.01714
- **Key finding:** Self-generating analogical examples improves reasoning without external demonstrations.
- **What we use:** The concept of leveraging prior reasoning patterns — related to how SELF-DISCOVER reuses module templates.

### Self-Refine: Iterative Refinement with Self-Feedback
- **Authors:** Madaan, Tandon, Gupta, Hallinan, Gao, Wiegreffe, Alon, Dziri, Prabhumoye, Yang, Gupta, Majumder, Hermann, Welleck, Yazdanbakhsh, Clark
- **Year:** 2023
- **URL:** https://arxiv.org/abs/2303.17651
- **Key finding:** ~20% improvement from iterative self-refinement.
- **What we use:** Complementary technique — SELF-DISCOVER structures the reasoning path; Self-Refine polishes the output.

### Reflexion: Language Agents with Verbal Reinforcement Learning
- **Authors:** Shinn, Labash, Narasimhan
- **Year:** 2023 (NeurIPS)
- **URL:** https://arxiv.org/abs/2303.11366
- **What we use:** Cross-session learning — discovered reasoning structures can be cached and reused.

## Cognitive Science Background

### Components of Thinking
- **Source:** Resnick (1987), "Education and Learning to Think"
- **What we use:** The seed modules (decomposition, pattern recognition, abstraction) are grounded in cognitive science research on problem-solving strategies.

### Polya's Problem-Solving Heuristics
- **Source:** Polya (1945), "How to Solve It"
- **What we use:** Understand the problem → Devise a plan → Carry out the plan → Look back. Directly maps to SELECT → ADAPT → IMPLEMENT → EVALUATE.

## Related Techniques

### Chain-of-Thought Prompting Elicits Reasoning
- **Authors:** Wei et al.
- **Year:** 2022 (NeurIPS)
- **URL:** https://arxiv.org/abs/2201.11903

### Self-Consistency Improves Chain of Thought Reasoning
- **Authors:** Wang et al.
- **Year:** 2022 (ICLR)
- **URL:** https://arxiv.org/abs/2203.11171

### Least-to-Most Prompting Enables Complex Reasoning
- **Authors:** Zhou et al.
- **Year:** 2022 (ICLR)
- **URL:** https://arxiv.org/abs/2205.10625

### Take a Step Back: Evoking Reasoning via Abstraction
- **Authors:** Zheng et al.
- **Year:** 2024 (Google DeepMind)
- **URL:** https://arxiv.org/abs/2310.06117

## Practical References

### Andrew Ng — Agentic Design Patterns
- **Year:** 2024
- **Key insight:** Planning and tool use are core agentic patterns. SELF-DISCOVER embodies the Planning pattern.

### Learn Prompting — Advanced Techniques
- **URL:** https://learnprompting.org/docs/advanced/
- **Covers:** CoT, ToT, Self-Refine, and structured reasoning approaches
