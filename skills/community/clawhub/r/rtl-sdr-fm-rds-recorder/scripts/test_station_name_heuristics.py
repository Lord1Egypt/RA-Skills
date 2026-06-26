#!/usr/bin/env python3
"""Small local test harness for station-name selection heuristics."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from rds_observation import RdsEvidence
from station_identity import resolve_station_identity
from station_identity_debug import build_rds_debug_info


def main() -> None:
    test_cases = [
        {
            'name': 'prefer_clean_ps_over_time_like_partial',
            'psCounts': {'RMF FM': 3},
            'partialPsCounts': {'20_41': 8, 'RMF': 5},
            'expected': 'RMF FM',
        },
        {
            'name': 'prefer_partial_when_ps_missing_and_partial_is_repeated',
            'psCounts': {},
            'partialPsCounts': {'TROJKA': 4, 'POLSKIE': 2},
            'expected': 'TROJKA',
        },
        {
            'name': 'reject_pretty_but_weak_partial_candidate',
            'psCounts': {},
            'partialPsCounts': {'LOLLI': 1},
            'expected': 'UnknownStation',
        },
        {
            'name': 'reject_generic_or_time_like_noise',
            'psCounts': {'RADIO': 2},
            'partialPsCounts': {'16_41': 6},
            'expected': 'UnknownStation',
        },
        {
            'name': 'prefer_ps_over_partial_with_more_repetitions',
            'psCounts': {'JEDYNKA': 2},
            'partialPsCounts': {'POLSKIE': 7},
            'expected': 'JEDYNKA',
        },
        {
            'name': 'prefer_repeated_ps_over_numeric_garbage',
            'psCounts': {'TROJKA': 17, '19_27': 4, 'Radio': 5, 'Polskie': 8},
            'partialPsCounts': {'19_2': 4, 'TRO': 22, 'TROJK': 16},
            'expected': 'TROJKA',
        },
        {
            'name': 'prefer_longer_real_brand_when_ps_repetition_is_higher',
            'psCounts': {'RMF FM': 11, 'RMF': 3},
            'partialPsCounts': {'RMF': 20},
            'expected': 'RMF FM',
        },
        {
            'name': 'keep_plausible_station_name_with_spaces',
            'psCounts': {'R MARYJA': 3},
            'partialPsCounts': {},
            'expected': 'R MARYJA',
        },
        {
            'name': 'reject_numeric_fragment_even_when_repeated',
            'psCounts': {'1108': 5, 'WARSZAWA': 3, '96.5FM': 3},
            'partialPsCounts': {'110': 5, 'WARS': 5},
            'expected': 'WARSZAWA',
        },
        {
            'name': 'suppress_partial_when_full_ps_is_plausible_prefix',
            'psCounts': {'RMF FM': 1},
            'partialPsCounts': {'RMF F': 5},
            'expected': 'UnknownStation',
        },
        {
            'name': 'suppress_partial_when_full_ps_count_is_close',
            'psCounts': {'JEDYNKA': 1},
            'partialPsCounts': {'JEDYNK': 3},
            'expected': 'UnknownStation',
        },
        {
            'name': 'prefer_brand_over_network_label_in_ps',
            'psCounts': {'POLSKIE': 10, 'JEDYNKA': 3},
            'partialPsCounts': {},
            'expected': 'JEDYNKA',
        },
    ]

    results = []
    failures = []
    for case in test_cases:
        evidence = RdsEvidence(
            ps_counts=case['psCounts'],
            partial_ps_counts=case['partialPsCounts'],
        )
        result = resolve_station_identity(evidence)
        chosen = result.station_name
        debug = build_rds_debug_info(0.0, 0, evidence, result)
        passed = chosen == case['expected']
        result = {
            'name': case['name'],
            'expected': case['expected'],
            'chosen': chosen,
            'passed': passed,
            'debug': debug,
        }
        results.append(result)
        if not passed:
            failures.append(result)

    print(json.dumps(results, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(f"Heuristic tests failed: {len(failures)}")


if __name__ == '__main__':
    main()
