#!/usr/bin/env python3
import json
import os
import sys
from copy import deepcopy
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / "config" / "models.json"
EXAMPLE_CONFIG = Path(__file__).parent.parent / "config" / "models.example.json"


class ConfigManager:
    @staticmethod
    def get_default_model():
        return (
            os.environ.get("DEFAULT_MODEL")
            or os.environ.get("MODEL")
            or "google/gemini-3-flash-preview"
        )

    @staticmethod
    def _base_defaults():
        default_model = ConfigManager.get_default_model()
        return {
            "zettel_dir": "~/Documents/Obsidian/Zettelkasten",
            "output_dir": "~/Documents/Obsidian/Inbox",
            "models": {
                "fast": default_model,
                "deep": default_model,
            },
            "agent_models": {
                "default": "fast",
                "retriever": "fast",
                "preprocess": "fast",
                "drafter": "deep",
                "publisher": "deep",
            },
            "retrieval": {
                "link_depth": 2,
                "max_links": 10,
                "semantic_max": 5,
            },
        }

    @staticmethod
    def _normalize_config(raw):
        defaults = ConfigManager._base_defaults()
        cfg = deepcopy(defaults)

        if not isinstance(raw, dict):
            return cfg

        cfg["zettel_dir"] = raw.get("zettel_dir", defaults["zettel_dir"])
        cfg["output_dir"] = raw.get("output_dir", defaults["output_dir"])

        if isinstance(raw.get("models"), dict):
            cfg["models"].update(raw["models"])

        if isinstance(raw.get("agent_models"), dict):
            cfg["agent_models"].update(raw["agent_models"])

        if isinstance(raw.get("retrieval"), dict):
            cfg["retrieval"].update(raw["retrieval"])

        return cfg

    @staticmethod
    def load_defaults():
        if EXAMPLE_CONFIG.exists():
            raw = json.loads(EXAMPLE_CONFIG.read_text(encoding="utf-8"))
            return ConfigManager._normalize_config(raw)
        return ConfigManager._base_defaults()

    @staticmethod
    def load():
        if not CONFIG_FILE.exists():
            return ConfigManager.load_defaults()
        try:
            raw = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return ConfigManager._normalize_config(raw)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in configuration file at {CONFIG_FILE}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def save(config):
        normalized = ConfigManager._normalize_config(config)
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(normalized, indent=2), encoding="utf-8")
        print(f"Configuration saved to {CONFIG_FILE}")

    @staticmethod
    def get_model_for_agent(config, agent_role):
        model_tier = config.get("agent_models", {}).get(
            agent_role, config.get("agent_models", {}).get("default", "fast")
        )
        return config.get("models", {}).get(model_tier, config.get("models", {}).get("fast"))
