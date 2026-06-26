"""Browser login module using Playwright."""

import asyncio
import json
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright, Request

from .config import Settings

# Token cache file path
TOKEN_CACHE_FILE = Path(".token_cache")


class LoginResult:
    """Result of login operation."""

    def __init__(self, token: str, cookies: dict):
        self.token = token
        self.cookies = cookies

    def to_dict(self) -> dict:
        return {"token": self.token, "cookies": self.cookies}

    @classmethod
    def from_dict(cls, data: dict) -> "LoginResult":
        return cls(token=data["token"], cookies=data["cookies"])


async def capture_token_from_request(request: Request) -> Optional[str]:
    """Check if a request contains the authorization token."""
    auth = request.headers.get("authorization", "")
    if "md_pss_id" in auth.lower():
        return auth
    return None


async def login_with_browser(
    settings: Settings,
    headless: Optional[bool] = None,
    timeout: Optional[int] = None,
    verbose: bool = True,
) -> LoginResult:
    """
    Perform login using Playwright browser automation.

    Args:
        settings: Application settings.
        headless: Whether to run browser in headless mode.
        timeout: Login timeout in seconds.
        verbose: Print progress messages.

    Returns:
        LoginResult containing token and cookies.

    Raises:
        TimeoutError: If login times out.
        RuntimeError: If token capture fails.
    """
    headless = headless if headless is not None else settings.login.headless
    timeout = timeout or settings.login.timeout

    login_url = f"{settings.system.base_url}{settings.login.login_url}"

    if verbose:
        print(f"[Login] Starting browser for login...")
        print(f"[Login] URL: {login_url}")

    captured_token: Optional[str] = None
    token_event = asyncio.Event()

    async def on_request(request: Request) -> None:
        nonlocal captured_token
        token = await capture_token_from_request(request)
        if token:
            captured_token = token
            if verbose:
                print("[Login] Token captured from request!")
            token_event.set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless)
        context = await browser.new_context()
        page = await context.new_page()

        page.on("request", on_request)

        try:
            if verbose:
                print(f"[Login] Navigating to login page...")

            await page.goto(login_url, wait_until="networkidle")

            # Try to auto-fill credentials if available
            if settings.username and settings.password:
                if verbose:
                    print("[Login] Attempting to fill credentials...")
                try:
                    username_input = page.locator('input[type="text"], input[name="username"], input[name="account"]')
                    password_input = page.locator('input[type="password"]')

                    if await username_input.count() > 0:
                        await username_input.fill(settings.username)
                    if await password_input.count() > 0:
                        await password_input.fill(settings.password)

                    if verbose:
                        print("[Login] Credentials filled. Please click login button.")
                except Exception as e:
                    if verbose:
                        print(f"[Login] Could not auto-fill credentials: {e}")

            if headless:
                try:
                    login_button = page.locator('button[type="submit"], input[type="submit"], .login-btn, #loginBtn')
                    if await login_button.count() > 0:
                        await login_button.click()
                except Exception:
                    pass

            if verbose:
                print("[Login] Waiting for login to complete...")
                print("[Login] Please log in manually in the browser window if needed.")

            try:
                await asyncio.wait_for(token_event.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                raise TimeoutError(
                    f"Login timed out after {timeout} seconds. "
                    "Please try again and complete login within the timeout period."
                )

            cookies = {c["name"]: c["value"] for c in await context.cookies()}

            return LoginResult(token=captured_token, cookies=cookies)

        finally:
            await browser.close()


def save_token_cache(result: LoginResult, cache_file: Path = TOKEN_CACHE_FILE) -> None:
    """Save login result to cache file."""
    cache_file.write_text(json.dumps(result.to_dict()), encoding="utf-8")


def load_token_cache(cache_file: Path = TOKEN_CACHE_FILE) -> Optional[LoginResult]:
    """Load login result from cache file."""
    if not cache_file.exists():
        return None

    try:
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        return LoginResult.from_dict(data)
    except (json.JSONDecodeError, KeyError):
        return None


def clear_token_cache(cache_file: Path = TOKEN_CACHE_FILE) -> None:
    """Clear the token cache file."""
    if cache_file.exists():
        cache_file.unlink()


async def get_or_refresh_token(
    settings: Settings,
    force_login: bool = False,
    verbose: bool = True,
) -> LoginResult:
    """
    Get a valid token, using cache if available and valid.

    Args:
        settings: Application settings.
        force_login: If True, always perform fresh login.
        verbose: Print progress messages.

    Returns:
        LoginResult with valid token.
    """
    if not force_login:
        cached = load_token_cache()
        if cached:
            if verbose:
                print("[Login] Using cached token")
            return cached

    result = await login_with_browser(settings, verbose=verbose)
    save_token_cache(result)
    if verbose:
        print("[Login] Token cached")
    return result
