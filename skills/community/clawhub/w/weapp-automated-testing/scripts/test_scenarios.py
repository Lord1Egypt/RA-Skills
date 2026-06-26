#!/usr/bin/env python3
"""
WeChat Mini Program test scenario examples.
Provides pre-defined scripts for common test scenarios.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weapp_automation import AutomationConfig, WeappTestRunner
from typing import Dict, Any, List
import json


class TestScenarios:
    """Pre-defined test scenarios."""

    def __init__(self, project_path: str, cli_path: str = "", ws_endpoint: str = "ws://localhost:9420"):
        self.config = AutomationConfig(
            project_path=project_path,
            cli_path=cli_path,
            ws_endpoint=ws_endpoint
        )

    def smoke_test(self) -> Dict[str, Any]:
        """
        Smoke test - verify basic mini program functionality.

        Test steps:
        1. Launch and navigate to home page
        2. Take screenshot of home page
        3. Check basic elements
        """
        runner = WeappTestRunner(self.config)

        result = (runner
            .navigate("pages/index/index")
            .wait(2)
            .screenshot("smoke_test_home.png")
            .get_results())

        return {
            "scenario": "smoke_test",
            "results": result,
            "summary": runner.get_summary()
        }

    def navigation_flow_test(self, pages: List[str]) -> Dict[str, Any]:
        """
        Navigation flow test.

        Args:
            pages: List of page paths to navigate through sequentially

        Test steps:
        1. Navigate to each page in order
        2. Take screenshot of each page
        3. Verify page loads successfully
        """
        runner = WeappTestRunner(self.config)

        for i, page in enumerate(pages):
            runner.navigate(page).wait(1).screenshot(f"nav_flow_{i}_{page.replace('/', '_')}.png")

        return {
            "scenario": "navigation_flow_test",
            "pages": pages,
            "results": runner.get_results(),
            "summary": runner.get_summary()
        }

    def form_submission_test(self, form_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Form submission test.

        Args:
            form_data: Form fields and values, e.g. {"input[name='username']": "testuser"}

        Test steps:
        1. Navigate to form page
        2. Fill out form
        3. Submit form
        4. Verify submission result
        """
        runner = WeappTestRunner(self.config)

        runner.navigate("pages/form/form").wait(1)

        # Fill out form
        for selector, value in form_data.items():
            runner.input(selector, value).wait(0.5)

        # Screenshot the filled form
        runner.screenshot("form_filled.png")

        # Click submit button
        runner.click("button[type='submit']").wait(2)

        # Screenshot submission result
        runner.screenshot("form_submitted.png")

        return {
            "scenario": "form_submission_test",
            "form_data": form_data,
            "results": runner.get_results(),
            "summary": runner.get_summary()
        }

    def ui_regression_test(self, pages: List[str], baseline_dir: str = "./baseline") -> Dict[str, Any]:
        """
        UI regression test.

        Args:
            pages: List of pages to test
            baseline_dir: Baseline screenshot directory

        Test steps:
        1. Take screenshot of each page
        2. Compare with baseline (if exists)
        3. Generate comparison report
        """
        from pathlib import Path

        runner = WeappTestRunner(self.config)

        # Create baseline directory
        Path(baseline_dir).mkdir(parents=True, exist_ok=True)

        screenshots = []
        for page in pages:
            filename = f"ui_{page.replace('/', '_')}.png"
            runner.navigate(page).wait(1).screenshot(filename)
            screenshots.append({
                "page": page,
                "filename": filename,
                "path": os.path.join(self.config.screenshot_dir, filename)
            })

        return {
            "scenario": "ui_regression_test",
            "pages": pages,
            "screenshots": screenshots,
            "baseline_dir": baseline_dir,
            "results": runner.get_results(),
            "summary": runner.get_summary()
        }

    def scroll_performance_test(self, page: str, scroll_element: str, scrolls: int = 5) -> Dict[str, Any]:
        """
        Scroll performance test.

        Args:
            page: Test page
            scroll_element: Scrollable element selector
            scrolls: Number of scrolls

        Test steps:
        1. Navigate to page
        2. Scroll multiple times
        3. Take screenshot after each scroll
        """
        runner = WeappTestRunner(self.config)

        runner.navigate(page).wait(1)

        for i in range(scrolls):
            runner.scroll(scroll_element, "down", 500).wait(0.5)
            runner.screenshot(f"scroll_{i}.png")

        return {
            "scenario": "scroll_performance_test",
            "page": page,
            "scrolls": scrolls,
            "results": runner.get_results(),
            "summary": runner.get_summary()
        }

    def user_journey_test(self, steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        User journey test.

        Args:
            steps: List of test steps, each containing action and parameters

        Example steps:
        [
            {"action": "navigate", "page": "pages/index/index"},
            {"action": "click", "selector": ".product-item"},
            {"action": "click", "selector": ".add-to-cart"},
            {"action": "navigate", "page": "pages/cart/cart"},
            {"action": "screenshot", "filename": "cart.png"}
        ]
        """
        runner = WeappTestRunner(self.config)

        for step in steps:
            action = step.get("action")

            if action == "navigate":
                runner.navigate(step.get("page", "pages/index/index"))
            elif action == "click":
                runner.click(step.get("selector"))
            elif action == "input":
                runner.input(step.get("selector"), step.get("text", ""))
            elif action == "scroll":
                runner.scroll(step.get("selector"), step.get("direction", "down"), step.get("distance", 300))
            elif action == "screenshot":
                runner.screenshot(step.get("filename"))
            elif action == "wait":
                runner.wait(step.get("seconds", 1))

        return {
            "scenario": "user_journey_test",
            "steps": steps,
            "results": runner.get_results(),
            "summary": runner.get_summary()
        }


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="WeChat Mini Program test scenarios")
    parser.add_argument("--project", "-p", required=True, help="Mini program project path")
    parser.add_argument("--cli-path", help="CLI path")
    parser.add_argument("--scenario", "-s", required=True,
                        choices=["smoke", "navigation", "form", "ui", "scroll", "journey"],
                        help="Test scenario")
    parser.add_argument("--pages", help="Page list, comma-separated (for navigation/ui scenarios)")
    parser.add_argument("--output", "-o", help="Output result file path")

    args = parser.parse_args()

    scenarios = TestScenarios(args.project, args.cli_path)

    if args.scenario == "smoke":
        result = scenarios.smoke_test()
    elif args.scenario == "navigation":
        if not args.pages:
            print("Error: navigation scenario requires --pages argument")
            sys.exit(1)
        pages = args.pages.split(",")
        result = scenarios.navigation_flow_test(pages)
    elif args.scenario == "form":
        # Example form data
        form_data = {
            "input[name='username']": "testuser",
            "input[name='email']": "test@example.com"
        }
        result = scenarios.form_submission_test(form_data)
    elif args.scenario == "ui":
        if not args.pages:
            print("Error: ui scenario requires --pages argument")
            sys.exit(1)
        pages = args.pages.split(",")
        result = scenarios.ui_regression_test(pages)
    elif args.scenario == "scroll":
        result = scenarios.scroll_performance_test("pages/list/list", ".scroll-view", 5)
    elif args.scenario == "journey":
        # Example user journey
        steps = [
            {"action": "navigate", "page": "pages/index/index"},
            {"action": "wait", "seconds": 2},
            {"action": "screenshot", "filename": "journey_start.png"}
        ]
        result = scenarios.user_journey_test(steps)
    else:
        print(f"Unknown scenario: {args.scenario}")
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
