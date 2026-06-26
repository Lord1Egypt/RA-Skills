#!/usr/bin/env python3
"""Debug/report helpers for station identity resolution."""

from __future__ import annotations

from rds_observation import RdsEvidence
from station_identity import StationIdentityResult, get_candidate_metadata


def build_rds_debug_info(
    freq_mhz: float,
    timeout_sec: int,
    evidence: RdsEvidence,
    result: StationIdentityResult,
) -> dict:
    best_ps = result.best_ps_candidate
    best_partial = result.best_partial_ps_candidate
    return {
        'frequencyMHz': freq_mhz,
        'timeoutSec': timeout_sec,
        'chosenName': result.station_name,
        'chosenSource': result.source,
        'accepted': result.accepted,
        'confidence': result.confidence,
        'rejectionReason': result.rejection_reason,
        'bestPsCandidate': best_ps.name if best_ps is not None else None,
        'bestPsCount': best_ps.count if best_ps is not None else 0,
        'bestPsScore': best_ps.score if best_ps is not None else None,
        'bestPsShapeClass': best_ps.shape_class if best_ps is not None else None,
        'bestPsAccepted': best_ps.accepted if best_ps is not None else False,
        'bestPsRejectionReason': best_ps.rejection_reason if best_ps is not None else None,
        'bestPartialPsCandidate': best_partial.name if best_partial is not None else None,
        'bestPartialPsCount': best_partial.count if best_partial is not None else 0,
        'bestPartialPsScore': best_partial.score if best_partial is not None else None,
        'bestPartialPsShapeClass': best_partial.shape_class if best_partial is not None else None,
        'bestPartialPsAccepted': best_partial.accepted if best_partial is not None else False,
        'bestPartialPsRejectionReason': best_partial.rejection_reason if best_partial is not None else None,
        'psCounts': evidence.ps_counts,
        'partialPsCounts': evidence.partial_ps_counts,
        'piCounts': evidence.pi_counts,
        'rawPsCounts': evidence.raw_ps_counts,
        'rawPartialPsCounts': evidence.raw_partial_ps_counts,
        'psScores': {name: get_candidate_metadata(evidence, name).score for name in evidence.ps_counts},
        'partialPsScores': {name: get_candidate_metadata(evidence, name).score for name in evidence.partial_ps_counts},
        'totalObjects': evidence.total_objects,
        'validObjects': evidence.valid_objects,
        'sniffDurationSec': evidence.sniff_duration_sec,
        'rtlFmStderrFirstLine': evidence.rtl_fm_stderr_first_line,
    }
