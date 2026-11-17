# OpenClaw Gateway Management
# Usage: make [target]
#
# Customize this Makefile for your gateway deployment.

TMUX_SESSION := openclaw-gateway
LOG_FILE := ~/.openclaw/logs/gateway.log
GATEWAY_BIN := $(CURDIR)/scripts/gateway-loop.sh
GATEWAY_DIRECT := openclaw gateway

.DEFAULT_GOAL := help
.PHONY: help lfg ensure start stop restart status logs attach clean

help: ## Show this help
	@echo "OpenClaw Gateway - tmux-based management"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Quick start: make lfg"

lfg: ## Start gateway and drop into cockpit
	@$(MAKE) ensure
	@$(MAKE) attach

ensure: ## Ensure gateway is running (idempotent, self-healing)
	@mkdir -p ~/.openclaw/logs
	@touch $(LOG_FILE)
	@if ! command -v tmux >/dev/null 2>&1; then \
		echo "❌ tmux not found. Please install tmux."; \
		exit 1; \
	fi
	@if ! command -v openclaw >/dev/null 2>&1; then \
		echo "❌ openclaw not found. Please install openclaw."; \
		exit 1; \
	fi
	@if ! tmux has-session -t $(TMUX_SESSION) 2>/dev/null; then \
		echo "Creating tmux session '$(TMUX_SESSION)'..."; \
		tmux new-session -d -s $(TMUX_SESSION) "$(GATEWAY_BIN); echo '[Gateway exited - shell ready]'; exec bash -l"; \
		sleep 2; \
		echo "✅ Gateway started."; \
	else \
		echo "✅ Gateway already running."; \
	fi

start: ensure ## Start gateway in tmux (alias for ensure)

stop: ## Stop gateway
	@if tmux has-session -t $(TMUX_SESSION) 2>/dev/null; then \
		echo "Stopping gateway..."; \
		tmux send-keys -t $(TMUX_SESSION) C-c; \
		sleep 1; \
		tmux kill-session -t $(TMUX_SESSION) 2>/dev/null || true; \
		echo "✅ Gateway stopped."; \
	else \
		echo "Gateway not running."; \
	fi

restart: stop start ## Restart gateway

status: ## Show gateway status
	@echo "=== tmux session ==="
	@tmux has-session -t $(TMUX_SESSION) 2>/dev/null && echo "✅ Running" || echo "❌ Not running"
	@echo ""
	@echo "=== Recent logs ==="
	@tail -5 $(LOG_FILE) 2>/dev/null || echo "No logs"

logs: ## Tail gateway logs
	@tail -f $(LOG_FILE)

attach: ## Attach to tmux session (Ctrl-B D to detach)
	@if ! tmux has-session -t $(TMUX_SESSION) 2>/dev/null; then \
		echo "Gateway not running. Use 'make lfg' to start."; \
	elif [ -n "$$TMUX" ]; then \
		tmux switch-client -t $(TMUX_SESSION); \
	else \
		tmux attach -t $(TMUX_SESSION); \
	fi

clean: ## Stop gateway and clean logs
	@$(MAKE) stop
	@echo "Cleaning logs..."
	@rm -f $(LOG_FILE)
	@echo "✅ Cleaned."
