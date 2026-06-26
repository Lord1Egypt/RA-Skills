"""API data fetcher module with browser-based fallback."""

import asyncio
import json
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx
from playwright.async_api import async_playwright, Page, Response

from .config import Settings
from .models import WeeklyReportData, WeeklyReportItem
from .login import LoginResult
from .date_utils import format_date_for_api

# Data cache file path
DATA_CACHE_FILE = Path(".data_cache")


class ReportFetcher:
    """Fetches weekly report data from the API with browser-based fallback."""

    def __init__(self, settings: Settings, login_result: LoginResult):
        self.settings = settings
        self.token = login_result.token
        self.cookies = login_result.cookies
        self.api_url = f"{settings.system.base_url}/wwwapi/Worksheet/GetFilterRows"

    def _build_request_body(
        self,
        page_index: int = 1,
        page_size: int = 50,
        date_filter: Optional[Dict[str, Any]] = None,
        team_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = {
            "worksheetId": self.settings.api.worksheet_id,
            "pageSize": page_size,
            "pageIndex": page_index,
            "status": 1,
            "appId": self.settings.api.app_id,
            "viewId": self.settings.api.view_id,
            "filterControls": [],
            "fastFilters": [],
            "searchControls": [],
            "kw": "",
            "rowId": "",
            "rowIdIndex": 0,
            "sortControls": [],
            "getType": 1,
        }

        if date_filter:
            body["filterControls"].append(date_filter)

        if team_filter:
            body["filterControls"].append({
                "controlId": "班组",
                "value": team_filter,
                "filterType": "2",
                "spliceType": "1",
            })

        return body

    def _build_headers(self) -> Dict[str, str]:
        return {
            "authorization": self.token,
            "content-type": "application/json",
            "accept": "application/json",
        }

    async def fetch_page(
        self,
        page_index: int = 1,
        page_size: int = 50,
        date_filter: Optional[Dict[str, Any]] = None,
        team_filter: Optional[str] = None,
    ) -> Dict[str, Any]:
        body = self._build_request_body(page_index, page_size, date_filter, team_filter)
        headers = self._build_headers()

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                self.api_url,
                json=body,
                headers=headers,
                cookies=self.cookies,
            )
            response.raise_for_status()
            return response.json()

    async def fetch_with_browser(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        team: Optional[str] = None,
        headless: bool = False,
        timeout: int = 60,
        verbose: bool = True,
    ) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """Fetch data using browser automation with API interception."""
        if verbose:
            print("[Fetcher] Starting browser for data fetching...")

        captured_data: List[Dict[str, Any]] = []
        api_url_found: Optional[str] = None
        data_event = asyncio.Event()

        async def on_response(response: Response) -> None:
            nonlocal api_url_found, captured_data

            url = response.url
            if any(keyword in url for keyword in ["GetFilterRows", "GetWorksheetRows", "worksheet", "rowdata"]):
                try:
                    if response.status == 200:
                        json_data = await response.json()
                        if verbose:
                            print(f"[Fetcher] Intercepted response from: {url}")

                        rows = None
                        if isinstance(json_data, dict):
                            outer_data = json_data.get("data", {})
                            if isinstance(outer_data, dict):
                                inner_data = outer_data.get("data", [])
                                if isinstance(inner_data, list):
                                    rows = inner_data
                                else:
                                    rows = outer_data.get("rows", None)

                            if rows is None:
                                rows = outer_data.get("rows", None) if isinstance(outer_data, dict) else None

                            if rows is None:
                                rows = json_data.get("rows", None)

                        if rows:
                            captured_data.extend(rows if isinstance(rows, list) else [rows])
                            api_url_found = str(url)
                            if verbose:
                                print(f"[Fetcher] Captured {len(rows)} items from API")
                            data_event.set()
                except Exception as e:
                    if verbose:
                        print(f"[Fetcher] Could not parse response: {e}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context()

            if self.cookies:
                cookie_list = []
                for name, value in self.cookies.items():
                    cookie_list.append({
                        "name": name,
                        "value": value,
                        "domain": "120.210.237.117",
                        "path": "/",
                    })
                if cookie_list:
                    await context.add_cookies(cookie_list)
                    if verbose:
                        print(f"[Fetcher] Restored {len(cookie_list)} cookies")

            page = await context.new_page()
            page.on("response", on_response)

            try:
                worksheet_url = f"{self.settings.system.base_url}/worksheet/{self.settings.api.worksheet_id}"
                if verbose:
                    print(f"[Fetcher] Navigating to worksheet page...")
                    print(f"[Fetcher] URL: {worksheet_url}")

                await page.goto(worksheet_url, wait_until="networkidle", timeout=timeout * 1000)

                if verbose:
                    print("[Fetcher] Waiting for data to load...")

                try:
                    await asyncio.wait_for(data_event.wait(), timeout=30)
                except asyncio.TimeoutError:
                    if verbose:
                        print("[Fetcher] API interception timeout, trying DOM extraction...")
                    dom_data = await self._extract_from_dom(page)
                    if dom_data:
                        captured_data = dom_data
                        if verbose:
                            print(f"[Fetcher] Extracted {len(dom_data)} items from DOM")

                await browser.close()

            except Exception as e:
                await browser.close()
                raise

        return captured_data, api_url_found

    async def _extract_from_dom(self, page: Page) -> List[Dict[str, Any]]:
        """Extract data directly from page DOM as fallback."""
        print("[Fetcher] Attempting DOM extraction...")

        try:
            await page.wait_for_selector("table, .worksheet-table, .data-table, [role='grid']", timeout=10000)
            await page.wait_for_timeout(2000)

            data = []
            rows = await page.locator("tbody tr, [role='row']").all()

            if not rows:
                rows = await page.locator(".worksheetRow, .data-row, [class*='row']").all()

            print(f"[Fetcher] Found {len(rows)} rows in table")

            for i, row in enumerate(rows):
                try:
                    cells = await row.locator("td, [role='gridcell'], .cell").all_inner_texts()

                    if cells:
                        item = {
                            "rowid": f"dom_{i}",
                            "raw_data": cells,
                        }
                        data.append(item)
                except Exception as e:
                    print(f"[Fetcher] Could not extract row {i}: {e}")

            return data

        except Exception as e:
            print(f"[Fetcher] DOM extraction failed: {e}")
            return []

    async def fetch_all(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        team: Optional[str] = None,
        page_size: int = 50,
        use_browser: bool = True,
        verbose: bool = True,
    ) -> WeeklyReportData:
        """Fetch all report data with pagination."""
        if verbose:
            print("[Fetcher] Fetching report data...")

        if team is None:
            team = self.settings.defaults.team

        all_items: List[WeeklyReportItem] = []

        if use_browser:
            try:
                if verbose:
                    print("[Fetcher] Method 1: Browser-based data fetching")
                rows, api_url = await self.fetch_with_browser(
                    start_date=start_date,
                    end_date=end_date,
                    team=team,
                    headless=self.settings.login.headless,
                    verbose=verbose,
                )

                if rows:
                    if verbose:
                        print(f"[Fetcher] Browser fetch succeeded, found {len(rows)} items")

                    for row in rows:
                        try:
                            item = WeeklyReportItem(**row)
                            all_items.append(item)
                        except Exception:
                            all_items.append(WeeklyReportItem(
                                rowid=row.get("rowid", row.get("rowid", f"item_{len(all_items)}"))
                            ))

                    self._save_data_cache(rows)

                    return WeeklyReportData(items=all_items, total_count=len(all_items))

            except Exception as e:
                if verbose:
                    print(f"[Fetcher] Browser fetch failed: {e}")
                    print("[Fetcher] Falling back to direct API...")

        if verbose:
            print("[Fetcher] Method 2: Direct API fetching")

        date_filter = None
        if start_date and end_date:
            date_filter = {
                "controlId": "日期",
                "value": [
                    format_date_for_api(start_date),
                    format_date_for_api(end_date),
                ],
                "filterType": "18",
                "spliceType": "1",
                "dataType": "6",
            }

        page_index = 1
        total_count = 0

        while True:
            if verbose:
                print(f"[Fetcher] Fetching page {page_index}...")

            try:
                response = await self.fetch_page(
                    page_index=page_index,
                    page_size=page_size,
                    date_filter=date_filter,
                    team_filter=team,
                )
            except httpx.HTTPStatusError as e:
                print(f"[Fetcher] API request failed: {e}")
                raise

            data = response.get("data", {})
            rows = data.get("rows", [])
            total_count = data.get("total", 0) or len(rows)

            for row in rows:
                try:
                    item = WeeklyReportItem(**row)
                    all_items.append(item)
                except Exception as e:
                    print(f"[Fetcher] Warning: Could not parse row: {e}")
                    all_items.append(WeeklyReportItem(rowid=row.get("rowid", "unknown")))

            if verbose:
                print(f"[Fetcher] Retrieved {len(rows)} items (total: {total_count})")

            if len(all_items) >= total_count or len(rows) < page_size:
                break

            page_index += 1

        if verbose:
            print(f"[Fetcher] Fetched {len(all_items)} total items")

        return WeeklyReportData(items=all_items, total_count=total_count)

    def _save_data_cache(self, data: List[Dict[str, Any]]) -> None:
        """Save fetched data to cache file."""
        try:
            DATA_CACHE_FILE.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"[Fetcher] Could not save data cache: {e}")


async def fetch_reports(
    settings: Settings,
    login_result: LoginResult,
    start_date: date,
    end_date: date,
    team: Optional[str] = None,
    verbose: bool = True,
) -> WeeklyReportData:
    """Convenience function to fetch reports."""
    fetcher = ReportFetcher(settings, login_result)
    return await fetcher.fetch_all(
        start_date=start_date,
        end_date=end_date,
        team=team,
        verbose=verbose,
    )
