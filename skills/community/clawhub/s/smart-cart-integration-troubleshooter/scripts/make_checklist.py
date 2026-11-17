#!/usr/bin/env python3
"""Print a safe diagnostic checklist for a smart-cart symptom category."""

from __future__ import annotations

import sys


CHECKLISTS = {
    "power": [
        "Stop motion and isolate the 12V supply before changing wiring.",
        "Inspect the battery and cable insulation; stop for swelling, heat, smoke, or damage.",
        "Verify connector fit and polarity against the hardware documentation.",
        "Check the controller power indicator and record any reset pattern.",
        "Run a low-load test, then observe power stability during one slow wheel movement.",
    ],
    "motion": [
        "Secure or lift the chassis so wheels can rotate without moving the cart.",
        "Inspect each wheel, coupler, and shaft for binding or looseness.",
        "Command each servo separately at low speed and record its response.",
        "Verify controller channel mapping without changing servo calibration.",
        "Reassemble and run a slow straight-line acceptance test.",
    ],
    "direction": [
        "Stop the cart and verify all omnidirectional wheels are installed in the intended orientation.",
        "Lift the chassis and verify each servo's zero position.",
        "Test each servo direction independently and record clockwise/counter-clockwise response.",
        "Compare the three channel directions with the intended motion-vector mapping.",
        "Run slow forward, lateral, and in-place-turn tests on a clear floor.",
    ],
    "camera": [
        "Check the USB connection and confirm the camera is enumerated.",
        "Capture one frame outside the agent pipeline.",
        "Repeat capture to detect frozen or stale frames.",
        "Reduce resolution or frame rate temporarily to isolate bandwidth or latency issues.",
        "Restore the agent pipeline and verify fresh timestamps or frame changes.",
    ],
    "communication": [
        "Stop the cart and test one harmless direct controller command with the chassis secured.",
        "Verify the expected device or port is present and accessible.",
        "Capture the exact outbound message and controller response or timeout.",
        "Compare the message format with the controller protocol documentation.",
        "Repeat the same command three times and record delivery consistency.",
    ],
    "agent": [
        "Record the original user instruction without paraphrasing it.",
        "Capture the model's structured plan before controller translation.",
        "Validate action names, units, sequence numbers, safety checks, and final stop.",
        "Compare the validated plan with the user's intended path.",
        "Test the controller translation with the chassis secured and low speed selected.",
    ],
    "obstacle": [
        "Use a controlled test area and a soft obstacle with the emergency stop ready.",
        "Verify camera view, lighting, and absence of occlusion.",
        "Confirm that frames are fresh before each movement segment.",
        "Record detection result and clearance threshold without changing both at once.",
        "Verify the cart stops or replans before reaching the obstacle.",
    ],
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in CHECKLISTS:
        choices = ", ".join(CHECKLISTS)
        print(f"Usage: make_checklist.py CATEGORY\nCategories: {choices}", file=sys.stderr)
        return 2
    category = sys.argv[1]
    print(f"# Smart Cart Diagnostic Checklist: {category}\n")
    for index, item in enumerate(CHECKLISTS[category], start=1):
        print(f"{index}. [ ] {item}")
    print("\nStop immediately for overheating, smoke, damaged insulation, battery swelling, or uncontrolled motion.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

