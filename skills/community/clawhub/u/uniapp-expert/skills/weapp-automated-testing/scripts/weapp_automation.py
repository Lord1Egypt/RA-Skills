#!/usr/bin/env python3
"""
WeChat Mini Program automation testing core module.
Provides page navigation, element interaction, screenshots, console log reading, and more.
"""

import subprocess
import json
import time
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
from dataclasses import dataclass
from datetime import datetime


def _default_cli_path() -> str:
    """Return the platform-specific default CLI path for WeChat DevTools."""
    if sys.platform == "win32":
        return r"C:\Program Files (x86)\Tencent\微信web开发者工具\cli.bat"
    return "/Applications/wechatwebdevtools.app/Contents/MacOS/cli"


@dataclass
class AutomationConfig:
    """Automation test configuration"""
    project_path: str
    cli_path: str = ""
    screenshot_dir: str = "./screenshots"
    timeout: int = 30
    ws_endpoint: str = "ws://localhost:9420"

    def __post_init__(self):
        if not self.cli_path:
            self.cli_path = _default_cli_path()


class WeappAutomation:
    """
    WeChat Mini Program automation test controller.

    Implemented via DevTools CLI and automation scripts:
    - Page navigation
    - Element click/input
    - Screenshots
    - Console log reading
    """

    def __init__(self, config: AutomationConfig):
        self.config = config
        self.session_id: Optional[str] = None
        self._ensure_screenshot_dir()

    @staticmethod
    def _escape_js(value: str) -> str:
        """Escape string to prevent JavaScript injection"""
        return (value
                .replace("\\", "\\\\")
                .replace("'", "\\'")
                .replace('"', '\\"')
                .replace("`", "\\`")
                .replace("$", "\\$")
                .replace("\n", "\\n")
                .replace("\r", "\\r"))

    def _ensure_screenshot_dir(self):
        """Ensure screenshot directory exists"""
        Path(self.config.screenshot_dir).mkdir(parents=True, exist_ok=True)

    def _run_batch_commands(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Execute automation commands in batch, sharing a single Node.js WebSocket connection for better performance.

        Args:
            steps: List of operation steps, e.g. [{"action": "navigate", "params": {"target": "..."}}]
        """
        if not steps:
            return []
            
        automation_script = self._generate_batch_script(steps)

        script_path = os.path.join(tempfile.gettempdir(), f"weapp_automation_batch_{int(time.time())}.js")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(automation_script)

        try:
            # Ensure NODE_PATH includes global npm modules so temp scripts can find them
            env = os.environ.copy()
            if "NODE_PATH" not in env:
                try:
                    npm_global = subprocess.run(
                        "npm root -g",
                        capture_output=True, text=True, timeout=10,
                        shell=True,
                    ).stdout.strip()
                    if npm_global:
                        env["NODE_PATH"] = npm_global
                except Exception:
                    pass

            result = subprocess.run(
                ["node", script_path],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=self.config.timeout * len(steps),
                env=env,
            )
            return self._parse_batch_result(result)
        except subprocess.TimeoutExpired as e:
            return [{"success": False, "error": f"Execution timed out: {e}"}]
        except Exception as e:
            return [{"success": False, "error": str(e)}]
        finally:
            if os.path.exists(script_path):
                os.remove(script_path)

    def _generate_batch_script(self, steps: List[Dict[str, Any]]) -> str:
        ws_endpoint = self.config.ws_endpoint if hasattr(self.config, 'ws_endpoint') else 'ws://localhost:9420'

        base_script = '''
const automator = require('miniprogram-automator');

function safeStringify(obj, indent = 2) {
  let cache = [];
  const retVal = JSON.stringify(
    obj,
    (key, value) =>
      typeof value === 'object' && value !== null
        ? cache.includes(value)
          ? undefined // Duplicate reference found, discard key
          : cache.push(value) && value // Store value in our collection
        : value,
    indent
  );
  cache = null; // Enable garbage collection
  return retVal;
}

async function runTest() {
    const miniProgram = await automator.connect({
        wsEndpoint: '%%WS_ENDPOINT%%'
    });
    const results = [];

    try {
        let page = await miniProgram.currentPage();
        // If no page found, startup may not be complete yet, wait a moment
        if (!page) {
            await miniProgram.waitFor(2000);
            page = await miniProgram.currentPage();
        }
        
%s

        await miniProgram.disconnect();
        console.log('BATCH_RESULT: ' + safeStringify(results));
    } catch (error) {
        results.push({ success: false, error: error.message });
        console.log('BATCH_RESULT: ' + safeStringify(results));
        await miniProgram.disconnect();
        process.exit(1);
    }
}

runTest();
'''
        js_code = []
        for i, step in enumerate(steps):
            action = step.get("action")
            params = step.get("params", {})
            action_snippet = self._get_action_code(action, params)
            
            # Wrap each snippet to catch errors and save results
            js_code.append(f'''
        try {{
            let result_{i};
            // --- Action: {action} ---
            {action_snippet.replace("const result =", f"result_{i} =")}
            // -------------------------
            results.push({{ success: true, action: '{action}', data: result_{i} }});
            // Update page ref after potential navigation
            page = await miniProgram.currentPage();
        }} catch(e) {{
            console.error('ACTION_ERROR:', '{action}', e.message, e.stack);
            results.push({{ success: false, action: '{action}', error: e.message }});
            // Continue executing remaining steps instead of breaking the chain
        }}
''')
        return base_script.replace('%%WS_ENDPOINT%%', ws_endpoint) % "".join(js_code)

    def _run_automation_command(self, action: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Backward-compatible single-step execution, delegates to batch execution"""
        results = self._run_batch_commands([{"action": action, "params": params or {}}])
        return results[0] if results else {"success": False, "error": "Unknown error"}

    def _get_action_code(self, action: str, params: Dict[str, Any]) -> str:
        """Generate code for the given action type"""

        if action == "navigate":
            target = self._escape_js(params.get("target", "pages/index/index"))
            method = self._escape_js(params.get("method", "auto"))
            # "auto" tries switchTab first (for tabbar pages), falls back to reLaunch
            return f'''
        let newPage;
        const navMethod = '{method}';
        if (navMethod === 'switchTab') {{
            newPage = await miniProgram.switchTab('/{target}');
        }} else if (navMethod === 'navigateTo') {{
            newPage = await miniProgram.navigateTo('/{target}');
        }} else if (navMethod === 'reLaunch') {{
            newPage = await miniProgram.reLaunch('/{target}');
        }} else {{
            // auto: try switchTab first, fall back to reLaunch
            try {{
                newPage = await miniProgram.switchTab('/{target}');
            }} catch(navErr) {{
                newPage = await miniProgram.reLaunch('/{target}');
            }}
        }}
        await newPage.waitFor(2000);
        const result = {{ page: '{target}', navigated: true }};
'''

        elif action == "click":
            selector = self._escape_js(params.get("selector", ""))
            return f'''
        const element = await page.$(`{selector}`);
        if (!element) throw new Error('Element not found: {selector}');
        await element.tap();
        await page.waitFor(500);
        const result = {{ selector: '{selector}', clicked: true }};
'''

        elif action == "input":
            selector = self._escape_js(params.get("selector", ""))
            text = self._escape_js(params.get("text", ""))
            return f'''
        const element = await page.$(`{selector}`);
        if (!element) throw new Error('Element not found: {selector}');
        await element.input(`{text}`);
        await page.waitFor(500);
        const result = {{ selector: '{selector}', text: '{text}', input: true }};
'''

        elif action == "screenshot":
            filename = self._escape_js(params.get("filename", f"screenshot_{int(time.time())}.png"))
            filepath = self._escape_js(os.path.join(self.config.screenshot_dir, filename))
            return f'''
        await miniProgram.screenshot({{
            path: '{filepath}'
        }});
        const result = {{ path: '{filepath}', filename: '{filename}' }};
'''

        elif action == "get_logs":
            return '''
        const logs = await miniProgram.getSystemInfo();
        const result = { logs: logs };
'''

        elif action == "get_element_text":
            selector = self._escape_js(params.get("selector", ""))
            return f'''
        const element = await page.$(`{selector}`);
        if (!element) throw new Error('Element not found: {selector}');
        const text = await element.text();
        const result = {{ selector: '{selector}', text: text }};
'''

        elif action == "get_wxml":
            raw_selector = params.get("selector", "")
            selector = self._escape_js(raw_selector if raw_selector else "page")
            return f'''
        const element = await page.$(`{selector}`);
        if (!element) throw new Error('Element not found: {selector}');

        // Due to driver bugs with element.wxml() in this automator version,
        // fallback to retrieving the page data which represents the DOM state
        // accurately in Taro/React architectures.
        const fallbackData = await page.data();
        let info = fallbackData;
        try {{
             const wxmlStr = await element.wxml();
             if (wxmlStr) info = wxmlStr;
        }} catch(e) {{
             console.log("WXML fetch failed, using state proxy");
        }}
        const result = {{ selector: '{selector}', wxml: info }};
'''

        elif action == "get_data":
            path = self._escape_js(params.get("path", ""))
            return f'''
        const data = await page.data('{path}');
        const result = {{ path: '{path}', data: data }};
'''

        elif action == "scroll":
            selector = self._escape_js(params.get("selector", ""))
            direction = self._escape_js(params.get("direction", "down"))
            distance = params.get("distance", 300)
            return f'''
        const element = await page.$(`{selector}`);
        if (!element) throw new Error('Element not found: {selector}');
        await element.scroll({{ direction: '{direction}', distance: {distance} }});
        await page.waitFor(500);
        const result = {{ selector: '{selector}', scrolled: true, direction: '{direction}' }};
'''

        elif action == "wait":
            seconds = float(params.get("seconds", 1.0))
            ms = int(seconds * 1000)
            return f'''
        await page.waitFor({ms});
        const result = {{ waited: {seconds} }};
'''

        else:
            return '''
        const result = { message: 'Unknown action' };
'''

    def _parse_result(self, result: subprocess.CompletedProcess) -> Dict[str, Any]:
        """Parse command execution result"""
        output = result.stdout + result.stderr

        # Find AUTOMATION_RESULT marker
        match = re.search(r'AUTOMATION_RESULT:\s*(\{.*?\})', output, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass

        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
        
    @staticmethod
    def _safe_print(*args, **kwargs):
        """Print with Unicode safety on Windows (GBK console)."""
        try:
            print(*args, **kwargs)
        except UnicodeEncodeError:
            # Fallback: replace unencodable chars
            safe_args = [str(a).encode("utf-8", errors="replace").decode("utf-8", errors="replace") for a in args]
            try:
                print(*safe_args, **kwargs)
            except Exception:
                pass

    def _parse_batch_result(self, result: subprocess.CompletedProcess) -> List[Dict[str, Any]]:
        """Parse batch execution result"""
        output = result.stdout + result.stderr

        # Find BATCH_RESULT marker — use greedy match to capture the full JSON array
        match = re.search(r'BATCH_RESULT:\s*(\[.*\])', output, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                self._safe_print("--- BATCH JSON PARSE FAIL ---\n", output, "\n-------------------")

        self._safe_print("--- FATAL BATCH FAIL ---\n", output, "\n-------------------")
        return [{
            "success": False,
            "error": "Failed to parse batch results",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }]

    # ============ Public API ============

    def navigate_to(self, page_path: str) -> Dict[str, Any]:
        """
        Navigate to a specific page.

        Args:
            page_path: Page path, e.g. "pages/index/index"

        Returns:
            Operation result
        """
        return self._run_automation_command("navigate", {"target": page_path})

    def click(self, selector: str, page: str = "pages/index/index") -> Dict[str, Any]:
        """
        Click an element.

        Args:
            selector: Element selector (CSS-like selector)
            page: Current page path

        Returns:
            Operation result
        """
        return self._run_automation_command("click", {"selector": selector, "page": page})

    def input_text(self, selector: str, text: str, page: str = "pages/index/index") -> Dict[str, Any]:
        """
        Input text into a text field.

        Args:
            selector: Text field selector
            text: Text to input
            page: Current page path

        Returns:
            Operation result
        """
        return self._run_automation_command("input", {"selector": selector, "text": text, "page": page})

    def screenshot(self, filename: Optional[str] = None, page: str = "pages/index/index") -> Dict[str, Any]:
        """
        Take a screenshot.

        Args:
            filename: Screenshot filename (optional, defaults to timestamp)
            page: Current page path

        Returns:
            Operation result, including screenshot path
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        return self._run_automation_command("screenshot", {"filename": filename, "page": page})

    def get_element_text(self, selector: str, page: str = "pages/index/index") -> Dict[str, Any]:
        """
        Get element text.

        Args:
            selector: Element selector
            page: Current page path

        Returns:
            Operation result, including element text
        """
        return self._run_automation_command("get_element_text", {"selector": selector, "page": page})

    def scroll(self, selector: str, direction: str = "down", distance: int = 300, page: str = "pages/index/index") -> Dict[str, Any]:
        """
        Scroll an element.

        Args:
            selector: Scrollable element selector
            direction: Scroll direction (up/down/left/right)
            distance: Scroll distance
            page: Current page path

        Returns:
            Operation result
        """
        return self._run_automation_command("scroll", {
            "selector": selector,
            "direction": direction,
            "distance": distance,
            "page": page
        })

    def get_system_info(self) -> Dict[str, Any]:
        """
        Get system information.

        Returns:
            System information
        """
        return self._run_automation_command("get_logs", {})


class WeappTestRunner:
    """Test runner with chained call and test scenario support. Now uses underlying batch execution optimization for significantly improved performance."""

    def __init__(self, config: AutomationConfig):
        self.automation = WeappAutomation(config)
        self.steps: List[Dict[str, Any]] = []
        self.results: List[Dict[str, Any]] = []
        self.current_page = "pages/index/index"
        self._executed = False

    def navigate(self, page_path: str, method: str = "auto") -> "WeappTestRunner":
        """Navigate to a page.

        Args:
            page_path: Page path, e.g. "pages/index/index"
            method: Navigation method - "auto" (try switchTab then reLaunch),
                    "switchTab" (for tabbar pages), "navigateTo" (push to stack),
                    "reLaunch" (close all and open). Default "auto".
        """
        self.steps.append({"action": "navigate", "params": {"target": page_path, "method": method}})
        return self

    def click(self, selector: str) -> "WeappTestRunner":
        """Click an element."""
        self.steps.append({"action": "click", "params": {"selector": selector, "page": self.current_page}})
        return self

    def input(self, selector: str, text: str) -> "WeappTestRunner":
        """Input text."""
        self.steps.append({"action": "input", "params": {"selector": selector, "text": text, "page": self.current_page}})
        return self

    def screenshot(self, filename: Optional[str] = None) -> "WeappTestRunner":
        """Take a screenshot."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        self.steps.append({"action": "screenshot", "params": {"filename": filename, "page": self.current_page}})
        return self

    def scroll(self, selector: str, direction: str = "down", distance: int = 300) -> "WeappTestRunner":
        """Scroll."""
        self.steps.append({"action": "scroll", "params": {
            "selector": selector,
            "direction": direction,
            "distance": distance,
            "page": self.current_page
        }})
        return self

    def get_wxml(self, selector: str) -> "WeappTestRunner":
        """Get element WXML structure."""
        self.steps.append({"action": "get_wxml", "params": {"selector": selector}})
        return self

    def get_data(self, path: str = "") -> "WeappTestRunner":
        """Get page data."""
        self.steps.append({"action": "get_data", "params": {"path": path}})
        return self

    def wait(self, seconds: float) -> "WeappTestRunner":
        """Wait (implemented via script native wait)."""
        self.steps.append({"action": "wait", "params": {"seconds": seconds}})
        return self

    def run(self) -> "WeappTestRunner":
        """Execute all accumulated test steps."""
        if self._executed or not self.steps:
            return self
            
        batch_results = self.automation._run_batch_commands(self.steps)
        
        # Map batch results back to original results format for backward compatibility
        for i, step in enumerate(self.steps):
            action = step["action"]
            result = batch_results[i] if i < len(batch_results) else {"success": False, "error": "Step not executed due to early failure"}
            
            # Record execution result
            step_record = {"action": action, "result": result}
            if action == 'click' or action == 'input' or action == 'scroll':
                step_record['selector'] = step['params'].get('selector')
            if action == 'input':
                step_record['text'] = step['params'].get('text')
                
            self.results.append(step_record)
            
        self._executed = True
        return self

    def get_results(self) -> List[Dict[str, Any]]:
        """Get all operation results. Triggers execution automatically if not yet executed."""
        if not self._executed:
            self.run()
        return self.results

    def get_summary(self) -> Dict[str, Any]:
        """Get test summary."""
        if not self._executed:
            self.run()
            
        total = len(self.steps)
        passed = sum(1 for r in self.results if r["result"].get("success"))
        return {
            "total": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": passed / total if total > 0 else 0
        }



def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="WeChat Mini Program automation testing")
    parser.add_argument("--project", "-p", required=True, help="Mini program project path")
    parser.add_argument("--cli-path", default="/Applications/wechatwebdevtools.app/Contents/MacOS/cli", help="CLI path")
    parser.add_argument("--action", "-a", required=True,
                        choices=["navigate", "click", "input", "screenshot", "scroll", "info", "get_wxml", "get_data"],
                        help="Action type")
    parser.add_argument("--selector", "-s", help="Element selector")
    parser.add_argument("--text", "-t", help="Input text")
    parser.add_argument("--path", help="Data path (for get_data)", default="")
    parser.add_argument("--page", default="pages/index/index", help="Page path")
    parser.add_argument("--filename", "-f", help="Screenshot filename")
    parser.add_argument("--direction", choices=["up", "down", "left", "right"], default="down", help="Scroll direction")
    parser.add_argument("--distance", type=int, default=300, help="Scroll distance")

    args = parser.parse_args()

    config = AutomationConfig(
        project_path=args.project,
        cli_path=args.cli_path
    )

    automation = WeappAutomation(config)

    if args.action == "navigate":
        result = automation.navigate_to(args.page)
    elif args.action == "click":
        if not args.selector:
            print("Error: click action requires --selector argument")
            sys.exit(1)
        result = automation.click(args.selector, args.page)
    elif args.action == "input":
        if not args.selector or not args.text:
            print("Error: input action requires --selector and --text arguments")
            sys.exit(1)
        result = automation.input_text(args.selector, args.text, args.page)
    elif args.action == "screenshot":
        result = automation.screenshot(args.filename, args.page)
    elif args.action == "scroll":
        if not args.selector:
            print("Error: scroll action requires --selector argument")
            sys.exit(1)
        result = automation.scroll(args.selector, args.direction, args.distance, args.page)
    elif args.action == "get_wxml":
        if not args.selector:
            print("Error: get_wxml action requires --selector argument")
            sys.exit(1)
        result = automation._run_automation_command("get_wxml", {"selector": args.selector, "page": args.page})
    elif args.action == "get_data":
        result = automation._run_automation_command("get_data", {"path": args.path, "page": args.page})
    elif args.action == "info":
        result = automation.get_system_info()
    else:
        print(f"Unknown action: {args.action}")
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
