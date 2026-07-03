#!/usr/bin/env python3
"""
Deeptechnic × SkillOpt 训练和评估脚本。

注册 deep_tech_dd benchmark 并运行 SkillOpt 训练循环。
"""
from __future__ import annotations

import argparse
import os
import sys

# Add skillopt scripts to path
_SCRIPTS_DIR = "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/scripts"
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from skillopt.model.common import default_model_for_backend, normalize_backend_name

# ── Register our benchmark adapter ─────────────────────────────────────
from skillopt.envs.deep_tech_dd.adapter import DeepTechDDAdapter
_ENV_REGISTRY = {"deep_tech_dd": DeepTechDDAdapter}

# ── Register other builtins ───────────────────────────────────────────
for modname, clsname in [
    ("skillopt.envs.searchqa.adapter", "SearchQAAdapter"),
    ("skillopt.envs.docvqa.adapter", "DocVQAAdapter"),
]:
    try:
        mod = __import__(modname, fromlist=[clsname])
        _ENV_REGISTRY[modname.split(".")[2]] = getattr(mod, clsname)
    except ImportError:
        pass


def find_config() -> str:
    """Find the deep_tech_dd config YAML."""
    # Check next to this script, then in user's project
    candidates = [
        os.path.join(os.path.dirname(__file__), "configs", "deep_tech_dd", "default.yaml"),
        os.path.expanduser("~/Documents/AI-Space/专家/skillopt-integration/configs/deep_tech_dd/default.yaml"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[-1]  # fallback, will be created


def main():
    parser = argparse.ArgumentParser(description="Deeptechnic × SkillOpt training")
    parser.add_argument("--mode", choices=["train", "eval"], default="train",
                        help="Run mode: train (default) or eval-only")
    parser.add_argument("--out_root", default="/Users/ackiles/Documents/AI-Space/专家/skillopt-integration/outputs",
                        help="Output root directory")
    parser.add_argument("--num_epochs", type=int, default=2,
                        help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=1,
                        help="Batch size (number of projects per rollout)")
    parser.add_argument("--learning_rate", type=int, default=4,
                        help="Max edits per step (learning rate)")
    parser.add_argument("--skill_init", default="",
                        help="Initial skill document path (default: current workflow rules)")

    args = parser.parse_args()
    
    config_path = find_config()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # Build config dict
    cfg = {
        "env": {
            "name": "deep_tech_dd",
            "split_mode": "split_dir",
            "split_dir": os.path.expanduser(
                "~/Documents/AI-Space/专家/skillopt-integration/data/deep_tech_dd"
            ),
            "skill_init": args.skill_init or os.path.expanduser(
                "~/Documents/AI-Space/专家/02-workflow-rules.md"
            ),
            "out_root": args.out_root,
        },
        "train": {
            "num_epochs": args.num_epochs,
            "batch_size": args.batch_size,
            "seed": 42,
        },
        "gradient": {
            "minibatch_size": 2,
            "analyst_workers": 1,
            "failure_only": False,
        },
        "optimizer": {
            "learning_rate": args.learning_rate,
            "lr_scheduler": "constant",
            "skill_update_mode": "patch",
            "use_slow_update": False,
            "use_meta_skill": False,
        },
        "evaluation": {
            "use_gate": True,
            "sel_env_num": 1,
            "test_env_num": 1,
            "eval_test": True,
        },
        "model": {
            "backend": "azure_openai",
            "optimizer": "deepseek-chat",
            "optimizer_backend": "openai_chat",
            "reasoning_effort": "low",
            "azure_openai_auth_mode": "openai_compatible",
        },
    }
    
    # Setup API keys from env
    deepseek_key = os.environ.get("LOBSTER_APIKEY_DEEPSEEK") or os.environ.get("DEEPSEEK_API_KEY", "")
    cfg["model"]["azure_openai_endpoint"] = os.environ.get(
        "DEEPSEEK_ENDPOINT", "https://api.deepseek.com/v1"
    )
    cfg["model"]["azure_openai_api_key"] = deepseek_key
    
    if args.mode == "eval":
        # Eval-only: score skill against test data
        from scripts.eval_only import main as eval_main
        sys.argv = ["eval_only",
            "--config", config_path,
            "--env", "deep_tech_dd",
        ]
        os.environ["DEEPTECH_DD_CFG"] = str(cfg)
        eval_main()
    else:
        # Full training
        from scripts.train import main as train_main
        
        # write config YAML
        import yaml
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(cfg, f, default_flow_style=False)
        print(f"Config written to: {config_path}")
        
        # Run training
        sys.argv = ["train",
            "--config", config_path,
        ]
        train_main()


if __name__ == "__main__":
    main()
