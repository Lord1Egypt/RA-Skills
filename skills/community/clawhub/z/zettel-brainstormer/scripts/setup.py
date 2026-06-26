#!/usr/bin/env python3
from config_manager import ConfigManager


def get_input(prompt, default):
    response = input(f"{prompt} [{default}]: ").strip()
    return response if response else default


def main():
    print("🧠 Zettel Brainstormer Setup 🧠")
    print("--------------------------------")

    defaults = ConfigManager.load_defaults()
    config = {}

    # Directories
    print("\n--- Directory Configuration ---")
    config["zettel_dir"] = get_input(
        "Zettelkasten Directory",
        defaults.get("zettel_dir", "~/Documents/Obsidian/Zettelkasten"),
    )
    config["output_dir"] = get_input(
        "Output/Inbox Directory",
        defaults.get("output_dir", "~/Documents/Obsidian/Inbox"),
    )

    # Models
    print("\n--- Model Tiers ---")
    models = defaults.get("models", {})
    agent_models = defaults.get("agent_models", {})
    config["models"] = {
        "fast": get_input(
            "Fast model (retrieval/extraction)",
            models.get("fast", "google/gemini-3-flash-preview"),
        ),
        "deep": get_input(
            "Deep model (synthesis/critic)",
            models.get("deep", "google/gemini-3-pro-preview"),
        ),
    }
    config["agent_models"] = {
        "default": get_input(
            "Default agent model tier (fast/deep)",
            agent_models.get("default", "fast"),
        ),
        "retriever": get_input(
            "Retriever model tier (fast/deep)",
            agent_models.get("retriever", "fast"),
        ),
        "preprocess": get_input(
            "Preprocess model tier (fast/deep)",
            agent_models.get("preprocess", "fast"),
        ),
        "drafter": get_input(
            "Drafter model tier (fast/deep)",
            agent_models.get("drafter", "deep"),
        ),
        "publisher": get_input(
            "Publisher model tier (fast/deep)",
            agent_models.get("publisher", "deep"),
        ),
    }

    # Wikilink extraction settings
    print("\n--- Retrieval Limits ---")
    retrieval = defaults.get("retrieval", {})
    config["retrieval"] = {}
    config["retrieval"]["link_depth"] = int(get_input(
        "Link depth (N levels deep to follow wikilinks)",
        str(retrieval.get("link_depth", 2)),
    ))
    config["retrieval"]["max_links"] = int(get_input(
        "Max links (M total linked notes to include)",
        str(retrieval.get("max_links", 10)),
    ))
    config["retrieval"]["semantic_max"] = int(get_input(
        "Max semantic notes from zettel-link cache",
        str(retrieval.get("semantic_max", 5)),
    ))

    # Save
    print("\nSaving configuration...")
    ConfigManager.save(config)
    print("Setup complete! You can now use the skill.")

if __name__ == "__main__":
    main()
