#!/usr/bin/env python3
"""Run synomega locally and print JSON, loading the model + stock from env vars.

A thin convenience wrapper over the installed `synomega` package so an agent can
call every operation uniformly (the package CLI has no single-step subcommand):
single-step retro, forward, plan, score, evolve. Requires:
`pip install "synomega[gnn]"`.

Environment:
    SYNOMEGA_MODEL       trained run directory (contains best.pt + config.yaml)  [optional: else downloads default]
    SYNOMEGA_STOCK       custom building-block file (.keys or raw .smi catalogue) [optional: else a built-in library]
    SYNOMEGA_STOCK_KEYS  "1" if SYNOMEGA_STOCK is a precomputed .keys file       [default 0]
    SYNOMEGA_DEVICE      torch device, e.g. "cpu" or "cuda:0"                    [default cpu]
    SYNOMEGA_PLAUSIBILITY           "1" to enable dual-tower plausibility screening  [default off]
    SYNOMEGA_PLAUSIBILITY_THRESHOLD drop candidates below this plausibility         [default 0.4]
    SYNOMEGA_FORWARD_MODEL          forward run dir for `forward`/`evolve`           [default: download]

Usage:
    python synomega_run.py single-step "CC(=O)Nc1ccccc1O" --top-k 10
    python synomega_run.py plan        "CC(=O)Nc1ccccc1O" --max-depth 5 [--simplify] [--library molport]
    python synomega_run.py score       "CC(=O)Nc1ccccc1O" --max-steps 5  # simplify model by default; --library {zinc,molport}
    python synomega_run.py forward     "CC(=O)O.NCc1ccccc1" --top-k 5
    python synomega_run.py evolve      "CC(=O)c1ccccc1.C=O.CNC" --max-depth 3 --score-threshold 0.01
"""
from __future__ import annotations

import argparse
import json
import os
import sys


def _truthy(name: str) -> bool:
    return os.environ.get(name, "").lower() in {"1", "true", "yes", "on"}


def _load(algorithm: str, *, simplify: bool = False, expansion_width: int = 50,
          forward_consistency: bool = False, forward_top_k: int = 3,
          library: str = "zinc"):
    """Build (model, planner). Uses SYNOMEGA_MODEL/SYNOMEGA_STOCK if set,
    otherwise downloads a pretrained model + stock on first use.

    `simplify=True` uses the simplification-constrained single-step model (only
    fragmentation disconnections) -- the model synomega recommends for scoring;
    ignored when SYNOMEGA_MODEL points at an explicit checkpoint.
    `expansion_width` is the planner's search width -- single-step candidates
    expanded per node in multi-step search (scoring uses 10).
    `library` picks the built-in commercial building-block set ("zinc" default,
    or "molport") used when SYNOMEGA_STOCK is not set."""
    try:
        from synomega import Planner
        from synomega.singlestep import TemplateGNN
        from synomega.stock import InMemoryStock
    except ImportError:
        sys.exit('synomega is not installed. Run:  pip install "synomega[gnn]"')

    device = os.environ.get("SYNOMEGA_DEVICE", "cpu")
    model_path = os.environ.get("SYNOMEGA_MODEL", "").strip()
    stock_path = os.environ.get("SYNOMEGA_STOCK", "").strip()

    # Model: explicit path, else the simplify or the default downloaded model.
    if model_path:
        model = TemplateGNN.from_pretrained(model_path, device=device)
    elif simplify:
        model = TemplateGNN.simplify(device=device)
    else:
        model = TemplateGNN.default(device=device)

    # Stock: explicit path, or the auto-downloaded default.
    if stock_path:
        stock = (
            InMemoryStock.from_keys_file(stock_path)
            if _truthy("SYNOMEGA_STOCK_KEYS")
            else InMemoryStock.from_file(stock_path)
        )
    else:
        stock = InMemoryStock.builtin(library)

    # Reaction-plausibility screening of single-step predictions (OFF by default;
    # set SYNOMEGA_PLAUSIBILITY=1 to enable, SYNOMEGA_PLAUSIBILITY_THRESHOLD tunes
    # the drop threshold).
    plausibility = None
    if os.environ.get("SYNOMEGA_PLAUSIBILITY", "0").lower() in {
        "1", "true", "yes", "on"
    }:
        from synomega.plausibility import PlausibilityScorer

        plausibility = PlausibilityScorer.default(device=device)
    threshold = float(os.environ.get("SYNOMEGA_PLAUSIBILITY_THRESHOLD", "0.4"))

    planner = Planner(model, stock, algorithm=algorithm,
                      expansion_width=expansion_width,
                      plausibility=plausibility, plausibility_threshold=threshold,
                      forward_consistency=(forward_consistency or None),
                      forward_top_k=forward_top_k)
    return model, planner


def _load_forward():
    """Build the forward-prediction model (reactants -> products).

    Uses SYNOMEGA_FORWARD_MODEL if set, otherwise downloads the default forward
    model on first use. Independent of the retro model above.
    """
    try:
        from synomega.forward import ForwardTemplateGNN
    except ImportError:
        sys.exit('synomega is not installed. Run:  pip install "synomega[gnn]"')

    device = os.environ.get("SYNOMEGA_DEVICE", "cpu")
    fwd_path = os.environ.get("SYNOMEGA_FORWARD_MODEL", "").strip()
    if fwd_path:
        return ForwardTemplateGNN.from_pretrained(fwd_path, device=device)
    return ForwardTemplateGNN.default(device=device)


def main() -> int:
    p = argparse.ArgumentParser(description="run synomega locally -> JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    ss = sub.add_parser("single-step")
    ss.add_argument("smiles")
    ss.add_argument("--top-k", type=int, default=20)

    pl = sub.add_parser("plan")
    pl.add_argument("smiles")
    pl.add_argument("--algorithm", default="retrostar",
                    choices=["retrostar", "mcts", "bfs"])
    pl.add_argument("--max-depth", type=int, default=5)
    pl.add_argument("--max-routes", type=int, default=5)
    pl.add_argument("--simplify", action="store_true",
                    help="use the simplification-constrained single-step model "
                         "(fragmentation-only disconnections; cheaper search)")
    pl.add_argument("--exclude-target", action="store_true",
                    help="treat the target as not purchasable even if it is in "
                         "the stock (avoids a trivial zero-step solution)")
    pl.add_argument("--forward-consistency", action="store_true",
                    help="prune single-step candidates by round-trip forward "
                         "consistency (keep only if the retro template is in the "
                         "forward model's top-k for its reactants)")
    pl.add_argument("--forward-top-k", type=int, default=3)
    pl.add_argument("--library", default="zinc", choices=["zinc", "molport"],
                    help="built-in commercial building-block set to plan against "
                         "(ignored if SYNOMEGA_STOCK points at a custom catalogue)")

    sc = sub.add_parser("score")
    sc.add_argument("smiles")
    sc.add_argument("--max-steps", type=int, default=5)
    sc.add_argument("--algorithm", default="retrostar",
                    choices=["retrostar", "mcts", "bfs"])
    # Scoring defaults to the simplification-constrained model @ expansion
    # width 10, the operating point synomega recommends; --original reverts.
    sc.add_argument("--original", dest="simplify", action="store_false",
                    help="score with the unconstrained (original) model instead")
    sc.set_defaults(simplify=True)
    sc.add_argument("--exclude-target", action="store_true",
                    help="treat the target as not purchasable even if it is in "
                         "the stock (avoids a trivial zero-step solution)")
    sc.add_argument("--forward-consistency", action="store_true",
                    help="prune single-step candidates by round-trip forward "
                         "consistency (keep only if the retro template is in the "
                         "forward model's top-k for its reactants)")
    sc.add_argument("--forward-top-k", type=int, default=3)
    sc.add_argument("--library", default="zinc", choices=["zinc", "molport"],
                    help="built-in commercial building-block set to score against "
                         "(ignored if SYNOMEGA_STOCK points at a custom catalogue)")

    fw = sub.add_parser("forward")
    fw.add_argument("reactants", help="reactant SMILES, '.'-separated")
    fw.add_argument("--top-k", type=int, default=10)

    ev = sub.add_parser("evolve")
    ev.add_argument("reactants",
                    help="starting reactant SMILES, '.'-separated (each seeds the pool)")
    ev.add_argument("--max-depth", type=int, default=3,
                    help="max synthesis-tree depth (not step count)")
    ev.add_argument("--score-threshold", type=float, default=0.01,
                    help="min total score for a molecule to be reactable")
    ev.add_argument("--forward-top-k", type=int, default=5,
                    help="products taken per reaction pair")
    ev.add_argument("--frontier-width", type=int, default=None,
                    help="cap selectable molecules paired per round (for scale)")
    ev.add_argument("--top", type=int, default=20,
                    help="how many top-scoring product molecules to report")

    args = p.parse_args()

    if args.cmd == "single-step":
        _, planner = _load("retrostar")
        # planner.model is the plausibility-screened (and cached) single-step model.
        preds = planner.model.predict(args.smiles, top_k=args.top_k)
        out = {
            "target": args.smiles,
            "predictions": [
                {
                    "rank": i,
                    "reactants": list(pred.reactants),
                    "score": round(float(pred.score), 6),
                    "plausibility": (
                        round(float(pred.meta["plausibility"]), 6)
                        if pred.meta.get("plausibility") is not None else None
                    ),
                    "template_id": pred.template_id,
                }
                for i, pred in enumerate(preds, 1)
            ],
        }
    elif args.cmd == "plan":
        _, planner = _load(args.algorithm, simplify=args.simplify,
                           forward_consistency=args.forward_consistency,
                           forward_top_k=args.forward_top_k,
                           library=args.library)
        result = planner.plan(
            args.smiles, max_depth=args.max_depth,
            exclude_target=args.exclude_target,
        )
        out = {
            "target": args.smiles,
            "algorithm": args.algorithm,
            "solved": result.solved,
            "routes": [r.to_dict() for r in result.routes[: args.max_routes]],
        }
    elif args.cmd == "score":
        from synomega.synthesizability import SynthesizabilityScorer

        _, planner = _load(args.algorithm, simplify=args.simplify,
                           expansion_width=10,
                           forward_consistency=args.forward_consistency,
                           forward_top_k=args.forward_top_k,
                           library=args.library)
        report = SynthesizabilityScorer(planner).score(
            args.smiles, max_steps=args.max_steps,
            exclude_target=args.exclude_target,
        )
        out = report.as_dict()
    elif args.cmd == "forward":
        model = _load_forward()
        preds = model.predict(args.reactants, top_k=args.top_k)
        out = {
            "reactants": args.reactants,
            "products": [
                {
                    "rank": i,
                    "product": pred.product,
                    "score": round(float(pred.score), 6),
                    "template_id": pred.template_id,
                }
                for i, pred in enumerate(preds, 1)
            ],
        }
    elif args.cmd == "evolve":
        from synomega.forward import MultiComponentEvolution

        model = _load_forward()
        reactants = [r for r in args.reactants.split(".") if r]
        evolver = MultiComponentEvolution(
            model, max_depth=args.max_depth,
            score_threshold=args.score_threshold,
            forward_top_k=args.forward_top_k,
            frontier_width=args.frontier_width,
        )
        result = evolver.evolve(reactants)
        try:
            out = result.to_dict(max_molecules=args.top)
            out["reactants"] = reactants
        finally:
            result.close()
    else:  # pragma: no cover
        p.error("unknown command")

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
