"""
run_brief.py — PullStar 1-on-1 pipeline runner for OpenClaw.

Usage:
    python run_brief.py --login jsmith
    python run_brief.py --login jsmith --days 14 --pr-insights
    python run_brief.py --login jsmith --api-mode rest --max-results 20

Runs the deterministic pipeline (ingest -> score -> prepare) and then
instructs the agent to perform the LLM inference step and finalize.

Agent flow:
    Step 1  run_brief.py         -- ingest + score + prepare (this script)
    Step 2  agent (LLM call)     -- reads llm_input_{login}.json, calls LLM
    Step 3  agent_finalize_1on1  -- merges LLM output into final artifact
"""

import argparse
import subprocess
import sys
from pathlib import Path

# All scripts are co-located under skills/scripts/
_SCRIPTS_DIR = Path(__file__).resolve().parent / "scripts"


def _run(cmd: list[str]) -> None:
    """Run a subprocess, inheriting stdout/stderr. Exit on failure."""
    result = subprocess.run(cmd)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the PullStar deterministic pipeline and prepare agent LLM input."
    )
    parser.add_argument("--login",        required=True, help="Engineer GitHub login")
    parser.add_argument("--days",         type=int, default=5,
                        help="Lookback window in days (default: 5)")
    parser.add_argument("--output-dir",   default=None,
                        help="Directory for all artifacts "
                             "(default: .pullstar/ next to this script)")
    parser.add_argument("--pr-insights",  action="store_true", default=False,
                        help="Enable PR review/comment context in LLM prompt")
    parser.add_argument("--max-results",  type=int, default=20, metavar="N",
                        help="Max search results to iterate in ingest (default: 20)")
    parser.add_argument("--github-token", default=None, metavar="TOKEN",
                        help="[Override/debug only] GitHub PAT. Never logged.")
    parser.add_argument("--api-mode",     choices=["graphql", "rest"], default="graphql",
                        help="GitHub API mode: graphql (default) or rest")
    args = parser.parse_args()

    login = args.login.strip()

    # Resolve output_dir to an absolute path anchored to the script's own
    # directory so artifacts land in the same place regardless of launch CWD.
    output_dir = Path(
        args.output_dir if args.output_dir else Path(__file__).resolve().parent / ".pullstar"
    ).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    py = sys.executable

    # ------------------------------------------------------------------
    # Step 1 -- Ingest
    # ------------------------------------------------------------------
    ingest_cmd = [
        py, str(_SCRIPTS_DIR / "ingest.py"),
        "--login",       login,
        "--days",        str(args.days),
        "--output-dir",  str(output_dir),
        "--max-results", str(args.max_results),
        "--api-mode",    args.api_mode,
    ]
    if args.pr_insights:
        ingest_cmd.append("--pr_insights")
    if args.github_token:
        ingest_cmd += ["--github-token", args.github_token]

    _run(ingest_cmd)

    # ------------------------------------------------------------------
    # Step 2 -- Score
    # ------------------------------------------------------------------
    _run([
        py, str(_SCRIPTS_DIR / "score.py"),
        "--login",      login,
        "--input-dir",  str(output_dir),
        "--output-dir", str(output_dir),
    ])

    # ------------------------------------------------------------------
    # Step 3 -- Prepare LLM input artifact
    # ------------------------------------------------------------------
    prepare_mode = "pr_insights" if args.pr_insights else "default"
    _run([
        py, str(_SCRIPTS_DIR / "agent_prepare_1on1.py"),
        "--login",     login,
        "--input-dir", str(output_dir),
        "--mode",      prepare_mode,
    ])

    # ------------------------------------------------------------------
    # Agent instruction block
    # ------------------------------------------------------------------
    llm_input_path  = output_dir / f"llm_input_{login}.json"
    llm_output_path = output_dir / f"llm_output_{login}.json"
    finalize_cmd    = f'python "{_SCRIPTS_DIR / "agent_finalize_1on1.py"}" --login {login}'

    print(f"""
PIPELINE COMPLETE -- AGENT ACTION REQUIRED

  1. Read:   {llm_input_path}
  2. Extract the "system" and "user" fields
  3. Call your LLM with those as the system prompt and user message
  4. Write the response to:

       {llm_output_path}

     Required JSON schema:
       {{
         "version":        "1.0",
         "engineer_login": "{login}",
         "brief":          "<markdown brief here>"
       }}

  5. Run:    {finalize_cmd}
""")


if __name__ == "__main__":
    main()
