.PHONY: validate

validate:
	grep -q '^name: visual-dna$$' SKILL.md
	grep -q 'openclaw skills install visual-dna' README.md
	python3 -m json.tool examples/sample-design-dna.json >/dev/null
	python3 -c 'import json; from pathlib import Path; data=json.loads(Path("examples/sample-design-dna.json").read_text()); required={"meta","design_system","design_style","visual_effects"}; missing=sorted(required-set(data)); assert not missing, f"missing top-level keys: {missing}"; assert all(isinstance(data[k], dict) for k in required), "required top-level values must be objects"; print("VALIDATE_OK")'
