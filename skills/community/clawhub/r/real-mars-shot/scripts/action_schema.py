#!/usr/bin/env python3
"""Print the action schema the agent maps natural language onto."""

from __future__ import annotations

import json

SCHEMA = {
    "actions": [
        {"type": "meta", "fields": ["language", "tts", "director", "program"], "spends_time": False},
        {"type": "status", "spends_time": False},
        {"type": "compute", "topics": ["rocket", "dose", "consumables", "windows", "people", "comms", "mission"], "spends_time": False},
        {"type": "wait", "fields": ["months"]},
        {"type": "research", "fields": ["tech_id"]},
        {"type": "facility", "fields": ["facility"], "facilities": ["analog_habitat", "vacuum_lab", "biosphere_module", "training_center", "pad", "superheavy_pad", "genome_archive", "plant_lab"]},
        {"type": "analog", "fields": ["days", "confirm_reckless"]},
        {"type": "lobby"},
        {"type": "diplomacy", "fields": ["faction"]},
        {"type": "govern", "fields": ["style"], "styles": ["open", "suppress"]},
        {"type": "train", "fields": ["cohort"]},
        {"type": "biology", "fields": ["organism", "site", "confirm_reckless"], "sites": ["earth_lab", "earth_simulant", "earth_open", "moon", "mars"]},
        {"type": "independence", "fields": ["site", "confirm_reckless"]},
        {"type": "mission", "fields": ["profile", "destination", "crew", "payload_t", "confirm_reckless"]},
        {"type": "epoch", "fields": ["site", "path", "scale"], "sites": ["moon", "mars", "freespace"], "paths": ["human", "biology", "machine"], "scales": ["decade", "century", "millennium"]},
    ],
    "rule": "Impossible actions do not advance time. Reckless actions return needs_confirmation and do not mutate until confirm_reckless is true.",
}


def main() -> None:
    print(json.dumps(SCHEMA, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
