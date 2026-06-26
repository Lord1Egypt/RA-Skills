#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

DEFAULT_GOALS = ["Build trust", "Grow audience", "Drive conversion", "Document the journey"]
DEFAULT_PLATFORMS = ["Xiaohongshu", "Shorts", "YouTube", "TikTok"]


def load_json(path):
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        return None
    return json.loads(p.read_text())


def synthesize_state(payload):
    creator = payload.get("creator", {})
    memory = payload.get("memory", {})
    problem = payload.get("problem") or creator.get("current_problem") or "Content direction is not yet clear enough."

    identity_bits = []
    if creator.get("name"):
        identity_bits.append(creator["name"])
    if creator.get("role"):
        identity_bits.append(creator["role"])
    if creator.get("company"):
        identity_bits.append(f"building {creator['company']}")

    platforms = creator.get("platforms") or memory.get("platforms") or []
    content_pattern = creator.get("content_pattern") or memory.get("content_pattern") or "Posting exists, but operating logic is still forming."

    return {
        "identity": ", ".join(identity_bits) if identity_bits else "Creator identity not fully specified",
        "platforms": platforms,
        "content_pattern": content_pattern,
        "current_problem": problem,
    }


def choose_goal(payload, state):
    goal = payload.get("goal")
    if goal:
        return goal

    problem = state.get("current_problem", "").lower()
    if "trust" in problem or "positioning" in problem:
        return "Build trust"
    if "conversion" in problem or "customer" in problem:
        return "Drive conversion"
    if "consistency" in problem or "system" in problem:
        return "Document the journey"
    return "Build trust"


def choose_platform(payload, state):
    platform = payload.get("platform")
    if platform:
        return platform
    platforms = state.get("platforms") or []
    if platforms:
        return platforms[0]
    return "Xiaohongshu"


def choose_materials(payload):
    materials = payload.get("materials") or []
    if not materials:
        return {
            "use": [],
            "ignore": [],
            "best_material": None,
        }

    ranked = sorted(materials, key=lambda x: x.get("strength", 0), reverse=True)
    use = ranked[:2]
    ignore = ranked[2:]
    return {
        "use": use,
        "ignore": ignore,
        "best_material": use[0] if use else None,
    }


def build_direction(payload, state, goal, platform, material_info):
    best = material_info.get("best_material")
    if best:
        best_title = best.get("title", "best material")
        why = best.get("why", "It contains the strongest combination of signal, emotion, and narrative tension.")
        direction = f"Turn {best_title} into the next piece of content."
    else:
        best_title = "the strongest current founder/operator idea"
        why = "There is not enough concrete source material yet, so the next move should start from the clearest thesis or proof point."
        direction = "Build one clear thesis-driven content piece from the strongest current idea."

    return {
        "operating_goal": goal,
        "best_content_direction": direction,
        "why_now": why,
        "platform": platform,
        "best_material_title": best_title,
    }


def generate_drafts(payload, state, direction, goal, platform, material_info):
    best = material_info.get("best_material") or {}
    source_name = best.get("title", "current strongest material")
    creator_tone = payload.get("tone") or "natural, sharp, high-signal"

    option_a = {
        "angle": f"Use {source_name} as a trust-building founder/operator insight piece",
        "hook": "Most people are solving the surface problem, not the real one.",
        "structure": [
            "state the false frame",
            "show the real tension",
            "connect it to the creator's thesis",
            "close with a concrete takeaway",
        ],
        "platform_fit": platform,
        "packaging": "thesis-driven, creator voice, high signal",
        "why_this_works": "Best when the goal is trust and positioning, not just short-term clicks.",
    }

    option_b = {
        "angle": f"Package {source_name} as a tighter growth-oriented social cut",
        "hook": "Here is the mistake most people make in this category.",
        "structure": [
            "start with a sharp contrast",
            "compress to one core lesson",
            "show proof or consequence",
            "end with one sticky line",
        ],
        "platform_fit": platform,
        "packaging": "faster, clearer, more contrast-heavy",
        "why_this_works": "Best when the same core idea needs stronger first-screen retention.",
    }

    drafts = [option_a, option_b]

    return {
        "tone_bias": creator_tone,
        "drafts": drafts,
    }


def build_next_action(payload, goal, platform, material_info):
    best = material_info.get("best_material")
    if best:
        return {
            "action": "execute",
            "reason": "The goal is clear and there is strong enough source material to produce a real draft now.",
            "handoff": {
                "goal": goal,
                "source_material": [m.get("title") for m in material_info.get("use", [])],
                "platform": platform,
                "duration": payload.get("duration") or "<30s",
                "style_or_prompt": payload.get("style_or_prompt") or "natural, sharp, compress for first-screen clarity",
                "must_preserve": payload.get("must_preserve") or ["creator tone", "real-world specificity", "one strong point of view"],
            },
        }

    return {
        "action": "collect_better_material",
        "reason": "The creator goal is understood, but there is not enough strong source material to justify execution yet.",
        "handoff": None,
    }


def run(payload):
    state = synthesize_state(payload)
    goal = choose_goal(payload, state)
    platform = choose_platform(payload, state)
    material_info = choose_materials(payload)
    direction = build_direction(payload, state, goal, platform, material_info)
    drafts = generate_drafts(payload, state, direction, goal, platform, material_info)
    next_action = build_next_action(payload, goal, platform, material_info)

    return {
        "current_state": state,
        "operating_goal": direction["operating_goal"],
        "best_content_direction": {
            "what_to_make_now": direction["best_content_direction"],
            "why_this_is_the_best_move": direction["why_now"],
        },
        "recommended_source_material": {
            "use": material_info.get("use", []),
            "ignore_for_now": material_info.get("ignore", []),
        },
        "draft_packages": drafts["drafts"],
        "next_action": next_action,
    }


def main():
    parser = argparse.ArgumentParser(description="Video Content Operator MVP")
    parser.add_argument("--input", help="Path to JSON input payload")
    args = parser.parse_args()

    payload = load_json(args.input) if args.input else json.load(__import__("sys").stdin)
    result = run(payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
