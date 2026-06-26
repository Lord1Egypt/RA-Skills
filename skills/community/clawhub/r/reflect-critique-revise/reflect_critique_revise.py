#!/usr/bin/env python3
"""
reflect_critique_revise.py
Executable implementation of the reflect-critique-revise skill.

Invoked by OpenClaw as: python3 reflect_critique_revise.py --task "..." --draft-file path.swift
"""
import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import aiohttp  # pip install aiohttp


CHECKLISTS = {
    "ios": """Review this Swift code for:
- Deprecated API usage (any API deprecated in iOS 17+)
- Missing @MainActor annotations on UI-touching code
- Improper Task / async handling (retention cycles, missing awaits)
- SwiftUI view hierarchy issues (missing @State, @Binding, @Observable)
- SwiftData/Core Data migration safety
- Force unwraps that could crash
- Missing availability checks for iOS 26+ APIs
- Incorrect concurrency patterns (Sendable violations)""",
    "web": """Review this code for:
- React rendering issues (missing keys, stale closures, effect dependencies)
- Accessibility violations (missing aria labels, keyboard navigation)
- XSS vulnerabilities (unescaped user input)
- Memory leaks (event listeners not cleaned up)
- Bundle size concerns (large imports, unused code)
- TypeScript type safety (any usage, missing types)
- Responsive / mobile breakpoint handling""",
    "python": """Review this code for:
- Resource leaks (unclosed files, connections, locks)
- Exception handling gaps (bare except, swallowed errors)
- Off-by-one errors in slices/ranges
- Mutable default arguments
- Race conditions in async/threading code
- SQL injection if building queries
- Unsafe pickle/eval/exec usage
- Missing input validation""",
    "trading": """Review this code for:
- Lookahead bias in backtesting (using future data)
- Survivorship bias in data selection
- Slippage/fees ignored in signal generation
- Position sizing without risk limits
- Division by zero in ratio calculations
- Missing market hours / holiday checks
- Currency/unit mixing
- Float comparison issues (use Decimal for money)""",
    "vc": """Review this analysis for:
- Unit confusion (ARR vs MRR, net vs gross)
- Missing risk factors (competition, moat erosion, key-person risk)
- Overly optimistic market sizing (TAM bloat)
- Unit economics fundamentals (CAC payback, LTV accuracy)
- Counterfactual reasoning (what if thesis is wrong)
- Selection bias in comparables
- Benchmark staleness""",
    "general": "Review this code for correctness, clarity, and potential bugs.",
}


CRITIQUE_PROMPT = """You are a senior {domain} engineer doing a thorough code review.
You have no investment in this code — your job is to find problems, not validate it.

Task the author was trying to solve:
{task}

Code to review:
```
{draft}
```

{checklist}

For each issue you find, output:
- SEVERITY: critical | major | minor
- LOCATION: line number or function name
- ISSUE: specific problem
- FIX: concrete correction

If you find no issues, say "NO ISSUES FOUND" explicitly.
Be direct. Do not hedge. Do not explain why the code is good."""


REVISE_PROMPT = """Original task:
{task}

Original code:
```
{draft}
```

Review findings:
{critique}

Produce a revised version that addresses every critical and major issue.
Minor issues: fix if clean, ignore if fix would compromise clarity.

Output ONLY the revised code. No explanation, no preamble."""


CONFIDENCE_PROMPT = """Task:
{task}

Final code:
```
{revised}
```

Rate your confidence in this code on a three-point scale:
- HIGH: you would ship this to production
- MEDIUM: works but has caveats you'd want reviewed
- LOW: has issues you can't fix without more context

Output exactly one of: HIGH, MEDIUM, LOW
Then one sentence explaining why."""


async def call_llm(prompt: str, system: str, temperature: float = 0.3,
                   max_tokens: int = 4096, endpoint: str = None) -> str:
    endpoint = endpoint or os.environ.get(
        "OPENCLAW_LLM_ENDPOINT", "http://localhost:8080/v1/chat/completions"
    )
    async with aiohttp.ClientSession() as session:
        async with session.post(
            endpoint,
            json={
                "model": "m27-jangtq-crack",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=aiohttp.ClientTimeout(total=600),
        ) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]


async def reflect_critique_revise(task: str, draft: str, domain: str = "general",
                                   num_passes: int = 2) -> dict:
    current = draft
    history = []

    for i in range(num_passes):
        critique = await call_llm(
            prompt=CRITIQUE_PROMPT.format(
                task=task, draft=current, domain=domain,
                checklist=CHECKLISTS.get(domain, CHECKLISTS["general"])
            ),
            system=f"You are a senior {domain} engineer code reviewer.",
            temperature=0.2,
            max_tokens=2000,
        )
        history.append({"pass": i + 1, "critique": critique})

        if "NO ISSUES FOUND" in critique:
            break

        current = await call_llm(
            prompt=REVISE_PROMPT.format(task=task, draft=current, critique=critique),
            system=f"You are a senior {domain} engineer revising code.",
            temperature=0.3,
            max_tokens=6000,
        )
        # Strip markdown fences if model added them
        current = current.strip()
        if current.startswith("```"):
            lines = current.split("\n")
            # Remove first fence line and find closing fence
            current = "\n".join(lines[1:])
            if "```" in current:
                current = current.rsplit("```", 1)[0].rstrip()

    confidence_raw = await call_llm(
        prompt=CONFIDENCE_PROMPT.format(task=task, revised=current),
        system="You are rating your own confidence.",
        temperature=0.1,
        max_tokens=200,
    )
    if "HIGH" in confidence_raw[:10].upper():
        confidence = "HIGH"
    elif "LOW" in confidence_raw[:10].upper():
        confidence = "LOW"
    else:
        confidence = "MEDIUM"

    return {
        "code": current,
        "critique_history": history,
        "confidence": confidence,
        "passes_used": len(history),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, help="Original task description")
    parser.add_argument("--draft-file", help="File containing code to review")
    parser.add_argument("--draft", help="Code string (alternative to --draft-file)")
    parser.add_argument("--domain", default="general",
                        choices=list(CHECKLISTS.keys()))
    parser.add_argument("--passes", type=int, default=2)
    parser.add_argument("--output", help="Path to write final code (default: stdout)")
    parser.add_argument("--json", action="store_true",
                        help="Output full result as JSON instead of just code")
    args = parser.parse_args()

    if args.draft_file:
        draft = Path(args.draft_file).read_text()
    elif args.draft:
        draft = args.draft
    else:
        draft = sys.stdin.read()

    result = asyncio.run(reflect_critique_revise(
        args.task, draft, args.domain, args.passes
    ))

    if args.json:
        output = json.dumps(result, indent=2)
    else:
        output = result["code"]

    if args.output:
        Path(args.output).write_text(output)
        print(f"→ Wrote {args.output} (confidence: {result['confidence']})",
              file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
