#!/usr/bin/env python3
"""
Weekly Report Generator - Main Entry Point

Generates weekly report documents by:
1. Logging into the report system
2. Fetching report data
3. Summarizing with AI
4. Generating Word document

Usage:
    python generate.py --week today
    python generate.py --week last --team "科创研发组"
    python generate.py --week 2026-03-07 --output report.docx
"""

import argparse
import asyncio
import json
import sys
from datetime import date
from pathlib import Path
from typing import Optional

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.config import Settings
from lib.models import DateRange, SummarizedReport
from lib.date_utils import parse_date_input
from lib.login import get_or_refresh_token
from lib.fetcher import fetch_reports
from lib.summarizer import summarize_reports
from lib.generator import generate_report_document


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate weekly report document",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--week", "-w",
        default="today",
        help="Week to generate report for: 'today', 'last', or date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--team", "-t",
        default=None,
        help="Team name (uses default from config if not specified)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output filename"
    )
    parser.add_argument(
        "--force-login", "-f",
        action="store_true",
        help="Force fresh login instead of using cached token"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to config file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args()


def output_json(data: dict):
    """Output result as JSON to stdout."""
    print(json.dumps(data, ensure_ascii=False))


async def generate_report(
    week: str,
    team: Optional[str],
    output: Optional[str],
    force_login: bool,
    headless: bool,
    config_path: Optional[str],
    verbose: bool,
) -> dict:
    """
    Generate weekly report.

    Returns:
        dict with success status and details
    """
    result = {
        "success": False,
        "output_file": None,
        "items_count": 0,
        "filtered_count": 0,
        "week_range": None,
        "error": None,
    }

    try:
        # Load settings
        settings = Settings.from_yaml(config_path)

        # Override headless if specified
        if headless:
            settings.login.headless = True

        # Parse week input
        try:
            start_date, end_date = parse_date_input(week)
        except ValueError as e:
            result["error"] = str(e)
            return result

        week_range = DateRange(start_date=start_date, end_date=end_date)
        result["week_range"] = str(week_range)

        team = team or settings.defaults.team

        if verbose:
            print(f"\n{'='*50}")
            print(f"Weekly Report Generator")
            print(f"{'='*50}")
            print(f"  Week: {week_range}")
            print(f"  Team: {team}")
            print()

        # Step 1: Login
        if verbose:
            print("[Step 1] Authentication...")

        try:
            login_result = await get_or_refresh_token(settings, force_login=force_login, verbose=verbose)
            if verbose:
                print("[Step 1] Authentication successful")
        except Exception as e:
            result["error"] = f"Authentication failed: {e}"
            return result

        # Step 2: Fetch data
        if verbose:
            print("\n[Step 2] Fetching report data...")

        try:
            data = await fetch_reports(
                settings=settings,
                login_result=login_result,
                start_date=start_date,
                end_date=end_date,
                team=team,
                verbose=verbose,
            )
            result["items_count"] = data.total_count
            if verbose:
                print(f"[Step 2] Fetched {data.total_count} report items")
        except Exception as e:
            result["error"] = f"Failed to fetch data: {e}"
            return result

        if data.is_empty():
            if verbose:
                print("[Step 2] No report data found for the specified criteria.")

            # Generate empty report
            summary = SummarizedReport(
                week_range=week_range,
                team_name=team,
                overview="本周暂无周报数据提交",
                completed_tasks=[],
                issues="",
                next_week_plan="",
                raw_items_count=0,
            )
        else:
            # Step 3: Summarize with AI
            if verbose:
                print("\n[Step 3] AI Summarization...")

            try:
                summary = await summarize_reports(
                    data=data,
                    settings=settings,
                    team_name=team,
                    week_range=week_range,
                    verbose=verbose,
                )
                result["filtered_count"] = summary.raw_items_count
            except Exception as e:
                result["error"] = f"Summarization failed: {e}"
                return result

        # Step 4: Generate document
        if verbose:
            print("\n[Step 4] Generating document...")

        try:
            output_path = generate_report_document(
                report=summary,
                settings=settings,
                output_filename=output,
                verbose=verbose,
            )
            result["output_file"] = str(output_path)
            result["success"] = True
            if verbose:
                print(f"\n{'='*50}")
                print(f"Report generated successfully!")
                print(f"Output: {output_path}")
                print(f"{'='*50}")
        except FileNotFoundError as e:
            result["error"] = f"Template file not found: {e}"
        except Exception as e:
            result["error"] = f"Document generation failed: {e}"

    except Exception as e:
        result["error"] = f"Unexpected error: {e}"

    return result


def main():
    """Main entry point."""
    args = parse_args()

    result = asyncio.run(generate_report(
        week=args.week,
        team=args.team,
        output=args.output,
        force_login=args.force_login,
        headless=args.headless,
        config_path=args.config,
        verbose=args.verbose,
    ))

    # Output JSON result
    output_json(result)

    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
