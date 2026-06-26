.PHONY: validate

validate:
	grep -q '^name: visual-architecture$$' SKILL.md
	grep -q 'openclaw skills install visual-architecture' README.md
	python3 -m json.tool examples/service-map.json >/dev/null
	rm -f /tmp/visual-architecture-service-map.svg
	python3 scripts/render_architecture.py examples/service-map.json /tmp/visual-architecture-service-map.svg
	cmp -s examples/service-map.svg /tmp/visual-architecture-service-map.svg
	@echo VALIDATE_OK
