#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
from score_questionnaire import score

def roles(count, runtime):
    if count == '2-4':
        base=[
            ('Entry Coordinator / Producer','intake, simple production, and state tracking'),
            ('Source / Workflow Mapper','source inventory and compact workflow sketch'),
            ('Reviewer','quality, risk, and acceptance check')
        ]
    elif count in {'7-8','>8'}:
        base=[
            ('Entry Coordinator / Orchestrator','intake, routing, state, queues, versions, synthesis'),
            ('Source / Data Collector','source candidates, raw data, and asset inventory'),
            ('Evidence Verifier','verified claims, source conflicts, evidence ledger'),
            ('Architecture Designer','Agent Architecture Map, role topology, skill allocation'),
            ('Workflow Orchestrator','Workflow Orchestration Map, gates, loops, rerun/resume'),
            ('Domain Producer / Executor','analysis, composition, or controlled action'),
            ('Independent Acceptance Reviewer','accept/reject gate and risk checks')
        ]
    else:
        base=[
            ('Entry Coordinator / Orchestrator','intake, routing, state, queues, versions, synthesis'),
            ('Source Mapper','source inventory, original workflow extraction, local resources'),
            ('Architecture Designer','Agent Architecture Map, role boundaries, skill allocation, count rationale'),
            ('Workflow Orchestrator / Producer','Workflow Orchestration Map plus primary production or composition'),
            ('Independent Acceptance Reviewer','fact, logic, risk, and acceptance gate')
        ]
    if runtime == 'codex':
        if count == '5-6':
            base.append(('Runtime Adapter','Codex package artifacts, manifests, prompt rewrite, design-output archive, entry-agent startup welcome, and Codex-only package-end prompt templates'))
        else:
            base.append(('Runtime Adapter','export Codex artifacts'))
    return base

def main():
    parser = argparse.ArgumentParser(description="Generate a starter Skill2Team restructure plan from guided intake answers.")
    parser.add_argument("answers", help="Guided intake answers JSON.")
    parser.add_argument("--execution-path", choices=["direct-skill", "meta-team-first"], default="direct-skill")
    args = parser.parse_args()
    answers=json.loads(Path(args.answers).read_text(encoding='utf-8'))
    s=score(answers); runtime=s.get('runtime_target')
    meta_first = args.execution_path == "meta-team-first"
    print('# Skill2Team Starter Plan\n')
    print('## Execution-path log')
    print(f'- **execution_path**: {args.execution_path}')
    print('- **model_invocation_policy**: OpenAI Codex default; do not call direct model APIs unless explicitly labeled API-run role simulation')
    print(f'- **meta_team_first_done**: {str(meta_first).lower()}')
    print(f"- **current_run_fanout_status**: {'blocked_no_real_codex_meta_team' if meta_first else 'direct-skill-not-requested'}")
    print('- **target_subagent_fanout_supported**: runtime-dependent')
    print(f"- **execution_mode**: {'blocked' if meta_first else 'direct_skill'}")
    print(f"- **fallback_declaration**: {'meta-team-first blocked; real Codex meta-team activation/fan-out was not confirmed; fallback role-play is not permitted' if meta_first else 'not_applicable_direct_skill'}")
    print(f"- **synthesis_owner**: {'S2T Lead' if meta_first else 'Skill2Team direct skill'}")
    print()
    print('## Signals')
    for k,v in s.items(): print(f'- **{k}**: {v}')
    print('\n## Recommended top-level agents\n')
    print('| Agent | Accountability |\n|---|---|')
    for n,a in roles(s['recommended_agent_count'], runtime): print(f'| {n} | {a} |')
    print('\n## Agent Architecture Map')
    print('Define role topology, accountability, authority, context boundaries, skill ownership, shared state, and review relationships. Keep this separate from workflow orchestration.')
    print('\n## Workflow Orchestration Map')
    print('Extract original workflow first, then map runtime nodes, edges, branches, loops, gates, fan-out/fan-in, human waits, checkpoints, terminal boundaries, and handoffs.')
    print('\n## Control-Flow & Resume Contract')
    print('Record artifact lineage, stale rules, dependency-aware reruns, checkpoints, resume conditions, and blocked-resume cases.')
    print('\n## Package quality review')
    print('Review original skill/workflow versus candidate target-team package, including whether the agent count is justified and whether architecture/workflow separation is preserved.')
    return 0
if __name__=='__main__': raise SystemExit(main())
