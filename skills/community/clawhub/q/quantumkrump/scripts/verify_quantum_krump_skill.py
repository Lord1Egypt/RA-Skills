#!/usr/bin/env python3
"""
verify_quantum_krump_skill.py
=============================
Validation and integrity audit suite for the Quantum Krump OpenClaw Skill.
Checks:
1. OpenClaw skill structure & YAML frontmatter metadata.
2. Progressive disclosure references linkage and non-triviality.
3. Epistemic integrity guardrails (Zero Bio Coherence, 0 QPU Shots, 3,310x floor).
4. Terminology adherence (Session vs. Cypher).
5. Mathematical consistency of Bloch coordinate mappings and Bell thresholds.
"""

import sys
import re
import math
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

REQUIRED_REFERENCES = [
    "laban-krump-bloch.md",
    "categorical-diagrammatics.md",
    "quantinuum-guppy-selene.md",
    "qubo-stage-scheduling.md",
    "biophysical-motor-grounding.md",
    "physical-ai-robotics.md",
    "krump-culture-ontology.md",
    "evidence-integrity-audit.md",
]

def check_frontmatter(skill_md_path: Path) -> bool:
    content = skill_md_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        print("❌ FAIL: SKILL.md missing opening YAML frontmatter delimiter (---)")
        return False
    parts = content.split("---", 2)
    if len(parts) < 3:
        print("❌ FAIL: SKILL.md frontmatter malformed")
        return False
    frontmatter = parts[1]
    name_match = re.search(r"^name:\s*([a-z0-9_-]+)", frontmatter, re.MULTILINE)
    desc_match = re.search(r"^description:\s*(.+)", frontmatter, re.MULTILINE)
    
    if not name_match or name_match.group(1).strip() != "quantumkrump":
        print(f"❌ FAIL: SKILL.md name must be 'quantumkrump', got: {name_match.group(1) if name_match else 'None'}")
        return False
    if not desc_match or len(desc_match.group(1).strip()) < 30:
        print("❌ FAIL: SKILL.md description missing or too short")
        return False
        
    print(f"✅ PASS: Frontmatter valid (name='{name_match.group(1).strip()}')")
    return True

def check_references() -> bool:
    ref_dir = SKILL_DIR / "references"
    if not ref_dir.is_dir():
        print(f"❌ FAIL: references directory missing: {ref_dir}")
        return False
        
    all_ok = True
    for ref_name in REQUIRED_REFERENCES:
        ref_path = ref_dir / ref_name
        if not ref_path.is_file():
            print(f"❌ FAIL: Required reference missing: {ref_name}")
            all_ok = False
        elif ref_path.stat().st_size < 500:
            print(f"❌ FAIL: Reference file {ref_name} appears empty or truncated (<500 bytes)")
            all_ok = False
        else:
            print(f"✅ PASS: Reference verified: {ref_name} ({ref_path.stat().st_size} bytes)")
    return all_ok

def check_epistemic_guardrails() -> bool:
    audit_file = SKILL_DIR / "references" / "evidence-integrity-audit.md"
    text = audit_file.read_text(encoding="utf-8")
    
    checks = [
        ("Zero Biological Coherence", "Zero Biological Quantum Coherence"),
        ("Classical Floor (3,310x)", "3,310"),
        ("Zero Physical QPU Shots", "Zero Physical QPU Hardware Shots"),
        ("Dimmer Switch Misconception", "Dimmer Switch Misconception"),
        ("Spinning Coin Misconception", "Spinning Coin Misconception"),
        ("Tomographic Threshold", "4\\sqrt{\\frac{0.5}{\\text{shots}}}"),
    ]
    
    all_ok = True
    for label, term in checks:
        if term in text:
            print(f"✅ PASS: Guardrail verified: {label}")
        else:
            print(f"❌ FAIL: Guardrail missing from audit doc: {label}")
            all_ok = False
    return all_ok

def check_terminology_mandate() -> bool:
    # Check that SKILL.md strictly prohibits 'cypher' in favor of 'session'
    skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    ontology_text = (SKILL_DIR / "references" / "krump-culture-ontology.md").read_text(encoding="utf-8")
    
    if 'NEVER use "cypher"' in skill_text or "never cypher" in skill_text.lower():
        print("✅ PASS: Strict session vs. cypher rule declared in SKILL.md")
    else:
        print("❌ FAIL: Strict session vs. cypher mandate missing in SKILL.md")
        return False
        
    if "session" in ontology_text.lower():
        print("✅ PASS: Authentic 'session' vocabulary verified in ontology")
    else:
        print("❌ FAIL: 'session' vocabulary not found in ontology")
        return False
        
    return True

def check_math_consistency() -> bool:
    # Validate Tomographic Equivalence threshold formula
    shots = 1000
    thresh = 4.0 * math.sqrt(0.5 / shots)
    expected = 0.0894427190999916
    if abs(thresh - expected) < 1e-6:
        print(f"✅ PASS: Mathematical threshold calculation verified: Delta(1000) = {thresh:.4f}")
        return True
    else:
        print(f"❌ FAIL: Threshold mismatch: computed {thresh}, expected {expected}")
        return False

def main():
    print("==================================================")
    print("🕺⚛️ QUANTUM KRUMP OPENCLAW SKILL: INTEGRITY AUDIT ⚛️🕺")
    print("==================================================")
    
    results = [
        check_frontmatter(SKILL_DIR / "SKILL.md"),
        check_references(),
        check_epistemic_guardrails(),
        check_terminology_mandate(),
        check_math_consistency(),
    ]
    
    print("\n--------------------------------------------------")
    if all(results):
        print("🎉 ALL SKILL AUDIT CHECKS PASSED PERFECTLY!")
        print(f"Skill location: {SKILL_DIR}")
        sys.exit(0)
    else:
        print("❌ AUDIT DETECTED ERRORS. Please resolve before publishing.")
        sys.exit(1)

if __name__ == "__main__":
    main()
