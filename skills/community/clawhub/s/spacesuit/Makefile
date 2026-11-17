# Spacesuit — OpenClaw Workspace Framework
# Usage: make [target]

SPACESUIT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SCRIPTS_DIR := $(SPACESUIT_DIR)scripts
VERSION_FILE := $(SPACESUIT_DIR)VERSION
VERSION := $(shell cat $(VERSION_FILE))

# Default workspace is two levels up (skills/spacesuit/ → workspace root)
WORKSPACE ?= $(abspath $(SPACESUIT_DIR)/../..)

TESTS_DIR := $(SPACESUIT_DIR)tests

.DEFAULT_GOAL := help
.PHONY: help init upgrade diff version test release

help: ## Show this help
	@echo "Spacesuit v$(VERSION) — OpenClaw Workspace Framework"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Workspace: $(WORKSPACE)"

init: ## First-time install (creates workspace files from templates)
	@$(SCRIPTS_DIR)/install.sh "$(WORKSPACE)"

upgrade: ## Upgrade framework sections (preserves your customizations)
	@$(SCRIPTS_DIR)/upgrade.sh "$(WORKSPACE)"

upgrade-dry: ## Show what upgrade would change (no modifications)
	@$(SCRIPTS_DIR)/upgrade.sh --dry-run "$(WORKSPACE)"

diff: ## Show differences between installed and latest base
	@$(SCRIPTS_DIR)/diff.sh "$(WORKSPACE)"

test: ## Run test suite
	@bash $(TESTS_DIR)/run_tests.sh

version: ## Show installed and available versions
	@echo "Available: v$(VERSION)"
	@if [ -f "$(WORKSPACE)/.spacesuit-version" ]; then \
		echo "Installed: v$$(cat $(WORKSPACE)/.spacesuit-version)"; \
	else \
		echo "Installed: (not installed)"; \
	fi

release: ## Check release metadata only (usage: make release V=0.4.0)
ifndef V
	@echo "Usage: make release V=<version>"
	@echo "  e.g., make release V=0.4.0"
	@$(SCRIPTS_DIR)/release.sh --current
else
	@$(SCRIPTS_DIR)/release.sh $(V)
endif
