#!/usr/bin/env python3
from __future__ import annotations
import json, sys
from pathlib import Path

def L(v):
    if v is None: return []
    return v if isinstance(v, list) else [v]
def n(v): return str(v or '').strip().lower().replace(' ','_').replace('-','_')
def first(v):
    xs=L(v); return xs[0] if xs else None

def score(a):
    consequence=n(first(a.get('consequence', a.get('Q4'))))
    data=n(first(a.get('data_importance', a.get('Q5'))))
    sources={n(x) for x in L(a.get('sources', a.get('Q6')))}
    unknowns=n(first(a.get('unknowns', a.get('Q7'))))
    revisions=n(first(a.get('revisions', a.get('Q8'))))
    review=n(first(a.get('review', a.get('Q9'))))
    expertise=n(first(a.get('expertise', a.get('Q10'))))
    runtime='codex'
    current={n(x) for x in L(a.get('current_system', a.get('Q1')))}
    architecture={n(x) for x in L(a.get('architecture_concerns', a.get('Q_architecture')))}
    workflow={n(x) for x in L(a.get('workflow_concerns', a.get('Q_workflow')))}
    requested_count=n(first(a.get('agent_count_preference', a.get('Q_count'))))

    risk=0; dep=0; itr=0; rev=0; arch=0; flow=0
    if consequence in {'important_decisions','important_decision','major_decisions','legal','compliance','safety','health','finance','education','reputation','d','e','critical'}: risk+=3
    elif consequence in {'business','money','c'}: risk+=2
    elif consequence: risk+=1
    if data in {'very_important','critical','d','e'}: dep+=3
    elif data in {'important','c'}: dep+=2
    elif data: dep+=1
    if sources & {'official','official_sources','internal','internal_docs','third_party','realtime','realtime_api','conflicting','conflicting_sources','unknown','c','d','e','f','h','i'}: dep+=2
    if sources & {'conflicting','conflicting_sources','h'}: risk+=1
    if unknowns in {'often_missing','usually_discovered_while_working','emergent','c','d'}: itr+=2
    if revisions in {'many','multiple','new_information_changes_output','repeated_changes','c','d'}: itr+=2
    if review in {'independent_acceptance','acceptance_with_blocking_power','blocking','d','e'}: rev+=3
    elif review in {'fact_logic','c'}: rev+=2
    elif review: rev+=1
    if architecture & {'supervision','routing','handoff','shared_state','review_authority','skill_ownership','context_boundaries','credentials','workspace','isolation'}: arch+=2
    if workflow & {'branch','conditional','loop','retry','rerun','fan_out','fan_in','gate','human_wait','checkpoint','resume','terminal'}: flow+=2

    risk_level='critical' if risk>=4 else 'high' if risk>=3 else 'medium' if risk>=2 else 'low'
    data_dependency='critical' if dep>=5 else 'high' if dep>=3 else 'medium' if dep>=2 else 'low'
    iteration_need='high' if itr>=3 else 'medium' if itr>=1 else 'low'
    review_need='independent_acceptance' if rev>=3 else 'fact_logic' if rev>=2 else 'light' if rev else 'none'
    skill_sprawl=bool(current & {'many_skills','existing_agents','mixed_assets','b','c','d'})
    expertise_breadth='broad' if expertise in {'many','unknown','c','d'} else 'medium' if expertise in {'two_three','two_or_three','b'} else 'narrow'
    architecture_complexity='high' if arch>=2 or skill_sprawl else 'medium' if expertise_breadth!='narrow' else 'low'
    workflow_complexity='high' if flow>=2 or iteration_need=='high' else 'medium' if iteration_need=='medium' else 'low'

    # 1.9.2 default: compact serious teams should fit 5-6 top-level agents.
    count='5-6'
    count_rationale='default_for_nontrivial_team'
    if risk_level=='low' and data_dependency=='low' and iteration_need=='low' and review_need in {'none','light'} and expertise_breadth=='narrow' and not skill_sprawl:
        count='2-4'
        count_rationale='low_risk_consolidation_allowed'
    if (risk_level in {'critical'} and data_dependency in {'high','critical'} and review_need=='independent_acceptance') or requested_count in {'more_than_6','7_8','8_12'}:
        count='7-8'
        count_rationale='requires_strong_split_rationale'
    if requested_count in {'more_than_8','8_plus','more'}:
        count='>8'
        count_rationale='discouraged_requires_explicit_hard_isolation_and_consolidation_plan'

    must=[]
    if risk_level in {'high','critical'} or data_dependency in {'high','critical'}: must.append('Data Collector and Evidence Verifier must be separated, or justify a consolidated Source/Evidence role plus independent acceptance gate within 5-6 agents')
    if risk_level in {'high','critical'} or review_need=='independent_acceptance': must.append('Producer/Executor != Independent Acceptance Reviewer')
    if iteration_need=='high' or workflow_complexity=='high' or skill_sprawl: must.append('Orchestrator owns state, queues, versions, and rerun/resume policy')
    must.append('Agent Architecture Map != Workflow Orchestration Map')

    return {
        'risk_level':risk_level,
        'data_dependency':data_dependency,
        'iteration_need':iteration_need,
        'review_need':review_need,
        'expertise_breadth':expertise_breadth,
        'skill_sprawl':'high' if skill_sprawl else 'low',
        'architecture_complexity':architecture_complexity,
        'workflow_complexity':workflow_complexity,
        'recommended_agent_count':count,
        'agent_count_rationale':count_rationale,
        'must_separate':must,
        'architecture_map_required': architecture_complexity!='low' or risk_level!='low' or skill_sprawl,
        'workflow_orchestration_map_required': workflow_complexity!='low' or iteration_need!='low',
        'runtime_target':runtime,
        'runtime_adapter_recommended':True,
        'baseline_vs_team_evaluation_recommended':bool(current and not (current <= {'new_system'}))
    }

def main():
    if len(sys.argv)!=2:
        print('Usage: score_questionnaire.py answers.json', file=sys.stderr); return 2
    print(json.dumps(score(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))), ensure_ascii=False, indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
