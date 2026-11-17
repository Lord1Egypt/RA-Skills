.ONESHELL:
SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c
.PHONY: validate examples

validate:
	python3 -m unittest discover -s tests
	scratch=$$(mktemp -d /tmp/visual-architecture-validate.XXXXXX)
	trap 'rm -rf "$$scratch"' EXIT
	grep -q '^name: visual-architecture$$' SKILL.md
	grep -q 'openclaw skills install visual-architecture' README.md
	@for schema in schemas/*.schema.json; do \
		python3 -m json.tool "$$schema" >/dev/null; \
	done
	@for spec in $$(find examples -maxdepth 1 -name '*.json' ! -name '*.receipt.json' | sort); do \
		python3 -m json.tool "$$spec" >/dev/null; \
		python3 scripts/render_architecture.py validate "$$spec" --json >/dev/null; \
	done
	@for spec in $$(find examples -maxdepth 1 -name '*.json' ! -name '*.receipt.json' | sort); do \
		name=$$(basename "$$spec" .json); \
		python3 scripts/render_architecture.py deliver "$$spec" "$$scratch/$$name.svg" --receipt "$$scratch/$$name.svg.receipt.json" >/dev/null; \
		cmp -s "examples/$$name.svg" "$$scratch/$$name.svg"; \
	done
	python3 scripts/render_architecture.py compare examples/pr-delta-before.json examples/pr-delta-head.json $$scratch/pr-delta-generated.html --spec $$scratch/pr-delta-generated.json --json >/dev/null
	python3 scripts/render_architecture.py gallery $$scratch/gallery.html >/dev/null
	python3 scripts/render_architecture.py layout examples/visual-architecture-auto.json $$scratch/layout.json --mode architecture --theme showcase >/dev/null
	python3 scripts/render_architecture.py extract-repo . --output $$scratch/extracted-repo.json --title "Validation Repo Evidence Map" >/dev/null
	if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then \
		python3 scripts/render_architecture.py extract-pr --base HEAD --head HEAD --output $$scratch/extracted-pr.json >/dev/null; \
	else echo "Git extraction integration check skipped outside a checkout"; fi
	python3 scripts/render_architecture.py bundle examples/visual-architecture-auto.json $$scratch/bundle --min-quality good >/dev/null
	python3 -m json.tool examples/showcase-artifact-engine.html.receipt.json >/dev/null
	@echo VALIDATE_OK

examples:
	@for spec in $$(find examples -maxdepth 1 -name '*.json' ! -name '*.receipt.json' | sort); do \
		name=$$(basename "$$spec" .json); \
		python3 scripts/render_architecture.py deliver "$$spec" "examples/$$name.svg" --receipt "examples/$$name.svg.receipt.json" >/dev/null; \
		python3 scripts/render_architecture.py deliver "$$spec" "examples/$$name.html" --receipt "examples/$$name.html.receipt.json" >/dev/null; \
		python3 scripts/render_architecture.py share-card "$$spec" "examples/$$name.share-card.svg" >/dev/null; \
	done
	python3 scripts/render_architecture.py compare examples/pr-delta-before.json examples/pr-delta-head.json examples/pr-delta-generated.html --spec examples/pr-delta-generated.json --receipt examples/pr-delta-generated.html.receipt.json >/dev/null
	python3 scripts/render_architecture.py share-card examples/pr-delta-generated.json examples/pr-delta-generated.share-card.svg >/dev/null
	python3 scripts/render_architecture.py gallery docs/gallery.html >/dev/null
	python3 scripts/render_architecture.py gallery index.html >/dev/null
