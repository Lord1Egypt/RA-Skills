#!/usr/bin/env python3
"""Station identity selection from aggregated RDS evidence.

`ps` and `partial_ps` are the only naming inputs.
`pi` may be retained in evidence/debug as an auxiliary station identifier,
but it is not used as a direct station-name source.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from rds_observation import CandidateMetadata, RdsEvidence

HIGH_CONFIDENCE_STATION_NAME_MAX_LEN = 8
MEDIUM_CONFIDENCE_STATION_NAME_MAX_LEN = 12
ALL_CAPS_STATION_NAME_MAX_LEN = 12
MIN_PS_COUNT_FOR_CONFIDENCE = 2  # Require at least two matching full-PS observations.
MIN_PARTIAL_PS_COUNT_FOR_CONFIDENCE = 3  # Partial PS is noisier; require stronger repetition.
MIN_STATION_SCORE_FOR_CONFIDENCE = 2  # Tuned for the current scoring rules; revisit if score weights or penalties change.
GENERIC_STATION_NAME_WORDS = {'RADIO', 'MUSIC', 'NEWS', 'STEREO', 'HITS'}
GENERIC_NETWORK_LABELS = {'POLSKIE'}


@dataclass
class StationIdentityCandidate:
    name: str
    source: Literal['ps', 'partial_ps']
    count: int
    score: int
    shape_class: str
    accepted: bool
    rejection_reason: str | None = None


@dataclass
class StationIdentityResult:
    station_name: str
    source: str
    accepted: bool
    confidence: float
    rejection_reason: str | None
    best_ps_candidate: StationIdentityCandidate | None
    best_partial_ps_candidate: StationIdentityCandidate | None


def score_station_name(name: str) -> int:
    score = 0
    if 3 <= len(name) <= HIGH_CONFIDENCE_STATION_NAME_MAX_LEN:
        score += 3
    elif len(name) <= MEDIUM_CONFIDENCE_STATION_NAME_MAX_LEN:
        score += 1
    else:
        score -= 2

    if re.fullmatch(r'[A-Z0-9][A-Z0-9 +&._/-]*', name) and len(name) <= ALL_CAPS_STATION_NAME_MAX_LEN:
        score += 2

    if ' ' in name and len(name) <= MEDIUM_CONFIDENCE_STATION_NAME_MAX_LEN:
        score += 1

    if any(ch.isdigit() for ch in name):
        score -= 2

    upper_words = {word for word in re.findall(r'[A-Za-z]+', name.upper())}
    if upper_words & GENERIC_STATION_NAME_WORDS:
        score -= 2

    if re.fullmatch(r'\d{1,2}[_:.-]\d{2}', name):
        score -= 6

    if re.search(r'[a-z]{4,}', name) and name != name.title():
        score -= 2

    return score


def classify_candidate_shape(name: str) -> str:
    if re.fullmatch(r'\d{1,2}[_:.-]\d{2}', name):
        return 'time_like'
    if re.fullmatch(r'\d{2,3}(?:[._]\d)? ?FM', name.upper()):
        return 'frequency_label'
    if re.fullmatch(r'\d{3,6}', name):
        return 'numeric_fragment'
    if re.search(r'(?i)\btel\b', name):
        return 'phone_like'
    if re.fullmatch(r'[A-Z][a-z]{3,}', name):
        return 'sentence_fragment'
    if re.search(r'[a-z]{4,}', name) and not re.search(r'[A-Z]{2,}', name):
        return 'sentence_fragment'
    upper_words = {word for word in re.findall(r'[A-Za-z]+', name.upper())}
    if name.upper() in GENERIC_NETWORK_LABELS:
        return 'generic_network_label'
    if upper_words & GENERIC_STATION_NAME_WORDS:
        return 'generic'
    if re.fullmatch(r'[A-Za-z0-9 +&._/-]+', name):
        return 'brand_like'
    return 'unknown_shape'


def compute_candidate_metadata(name: str) -> CandidateMetadata:
    score = score_station_name(name)
    shape_class = classify_candidate_shape(name)
    if shape_class == 'frequency_label':
        score -= 2
    if shape_class == 'generic_network_label':
        score -= 2
    return CandidateMetadata(score=score, shape_class=shape_class)


def get_candidate_metadata(evidence: RdsEvidence, name: str) -> CandidateMetadata:
    metadata = evidence.candidate_metadata.get(name)
    if metadata is None:
        metadata = compute_candidate_metadata(name)
        evidence.candidate_metadata[name] = metadata
    return metadata


def build_candidate(
    evidence: RdsEvidence,
    name: str,
    count: int,
    source: Literal['ps', 'partial_ps'],
) -> StationIdentityCandidate:
    metadata = get_candidate_metadata(evidence, name)
    return StationIdentityCandidate(
        name=name,
        source=source,
        count=count,
        score=metadata.score,
        shape_class=metadata.shape_class,
        accepted=False,
    )


def list_ranked_candidates(
    evidence: RdsEvidence,
    counts: dict[str, int],
    source: Literal['ps', 'partial_ps'],
) -> list[StationIdentityCandidate]:
    if not counts:
        return []
    candidates = [build_candidate(evidence, name, count, source) for name, count in counts.items()]
    candidates.sort(
        key=lambda candidate: (candidate.count, candidate.score, -len(candidate.name)),
        reverse=True,
    )
    return candidates


def select_best_candidate(
    evidence: RdsEvidence,
    counts: dict[str, int],
    source: Literal['ps', 'partial_ps'],
) -> StationIdentityCandidate | None:
    ranked = list_ranked_candidates(evidence, counts, source)
    return ranked[0] if ranked else None


def is_acceptable(
    candidate: StationIdentityCandidate | None,
    source: Literal['ps', 'partial_ps'],
    min_count: int,
    rejected_shapes: set[str],
    min_name_len: int = 0,
) -> tuple[bool, str | None]:
    source_label = source.replace('_', '-')
    if candidate is None:
        return False, f'missing-{source_label}-candidate'
    if candidate.count < min_count or candidate.score < MIN_STATION_SCORE_FOR_CONFIDENCE:
        return False, f'{source_label}-candidate-below-threshold'
    if candidate.shape_class in rejected_shapes:
        return False, f'{source_label}-candidate-{candidate.shape_class}'
    if len(candidate.name) < min_name_len:
        return False, f'{source_label}-candidate-too-short'
    return True, None


def is_acceptable_ps(candidate: StationIdentityCandidate | None) -> tuple[bool, str | None]:
    return is_acceptable(
        candidate,
        'ps',
        MIN_PS_COUNT_FOR_CONFIDENCE,
        {'time_like', 'phone_like', 'sentence_fragment', 'generic', 'numeric_fragment'},
    )


def is_acceptable_partial_ps(candidate: StationIdentityCandidate | None) -> tuple[bool, str | None]:
    return is_acceptable(
        candidate,
        'partial_ps',
        MIN_PARTIAL_PS_COUNT_FOR_CONFIDENCE,
        {'time_like', 'phone_like', 'sentence_fragment', 'generic', 'numeric_fragment', 'frequency_label', 'generic_network_label'},
        min_name_len=5,
    )


def find_best_acceptable_candidate(
    evidence: RdsEvidence,
    counts: dict[str, int],
    source: Literal['ps', 'partial_ps'],
) -> tuple[StationIdentityCandidate | None, StationIdentityCandidate | None, str | None]:
    ranked_candidates = list_ranked_candidates(evidence, counts, source)
    if not ranked_candidates:
        return None, None, f'missing-{source.replace("_", "-")}-candidate'

    best_candidate = ranked_candidates[0]
    acceptance_check = is_acceptable_ps if source == 'ps' else is_acceptable_partial_ps
    accepted_candidates: list[StationIdentityCandidate] = []
    last_reason = None
    for candidate in ranked_candidates:
        accepted, reason = acceptance_check(candidate)
        candidate.accepted = accepted
        candidate.rejection_reason = reason
        if accepted:
            accepted_candidates.append(candidate)
        else:
            last_reason = reason

    if not accepted_candidates:
        return best_candidate, None, last_reason

    chosen_candidate = accepted_candidates[0]
    if source == 'ps' and chosen_candidate.shape_class == 'generic_network_label':
        for candidate in accepted_candidates[1:]:
            if candidate.shape_class == 'brand_like' and candidate.score >= chosen_candidate.score:
                chosen_candidate = candidate
                break

    return best_candidate, chosen_candidate, None


def should_prefer_ps_over_partial(
    ps_candidate: StationIdentityCandidate | None,
    partial_candidate: StationIdentityCandidate | None,
) -> bool:
    if ps_candidate is None or partial_candidate is None:
        return False
    if ps_candidate.shape_class != 'brand_like':
        return False
    if partial_candidate.shape_class != 'brand_like':
        return False
    if ps_candidate.score < MIN_STATION_SCORE_FOR_CONFIDENCE:
        return False
    if (
        len(partial_candidate.name) < len(ps_candidate.name)
        and ps_candidate.name.startswith(partial_candidate.name)
        and (len(ps_candidate.name) - len(partial_candidate.name)) <= 2
    ):
        return True
    if ps_candidate.count >= max(1, partial_candidate.count - 2) and len(ps_candidate.name) > len(partial_candidate.name):
        return True
    return False


def resolve_station_identity(evidence: RdsEvidence) -> StationIdentityResult:
    best_ps_candidate, accepted_ps_candidate, ps_reason = find_best_acceptable_candidate(evidence, evidence.ps_counts, 'ps')
    best_partial_ps_candidate, accepted_partial_ps_candidate, partial_reason = find_best_acceptable_candidate(
        evidence,
        evidence.partial_ps_counts,
        'partial_ps',
    )

    if accepted_ps_candidate is not None:
        return StationIdentityResult(
            station_name=accepted_ps_candidate.name,
            source='ps',
            accepted=True,
            confidence=1.0 if accepted_ps_candidate is best_ps_candidate else 0.85,
            rejection_reason=None,
            best_ps_candidate=best_ps_candidate,
            best_partial_ps_candidate=best_partial_ps_candidate,
        )

    if should_prefer_ps_over_partial(best_ps_candidate, accepted_partial_ps_candidate):
        partial_reason = 'partial-ps-suppressed-by-plausible-full-ps'
    elif accepted_partial_ps_candidate is not None:
        return StationIdentityResult(
            station_name=accepted_partial_ps_candidate.name,
            source='partial_ps',
            accepted=True,
            confidence=0.7,
            rejection_reason=None,
            best_ps_candidate=best_ps_candidate,
            best_partial_ps_candidate=best_partial_ps_candidate,
        )

    rejection_reason = None
    if ps_reason not in {None, 'missing-ps-candidate'}:
        rejection_reason = ps_reason
    elif partial_reason not in {None, 'missing-partial-ps-candidate'}:
        rejection_reason = partial_reason

    return StationIdentityResult(
        station_name='UnknownStation',
        source='fallback-unknown',
        accepted=False,
        confidence=0.0,
        rejection_reason=rejection_reason,
        best_ps_candidate=best_ps_candidate,
        best_partial_ps_candidate=best_partial_ps_candidate,
    )
