"""SportsWeb portal automation — fetch invoice PDFs for header-only documents.

Some Sports Inc documents are scanned rather than EDI, so the SportsLink API
returns their header money but no `lines` (`has_lines: false`). The PDF in the
SportsWeb Invoice Center is the only place that line detail exists, and there is
no API for it — so this module drives the portal with Playwright, as
`drivethru-adidas-click` drives adidas Click.

## The flow

    https://www.sportsinc.us/          click DEALER LOGIN  (403 if you goto its href)
      → sportsweb.us.auth0.com/u/login  Auth0 Universal Login
      → swv3.sportsinc.com/home         the home screen — the search box lives HERE
      → type the PO, click Search       → swv2h.sportsinc.com/Member/InvoiceCenter/…
      → tick the row(s) → Downloads → "PDF File"

Three of those steps are counter-intuitive and each one was learned the hard way:

* **The login redirect cannot be navigated to.** `swv3.sportsinc.com/login-redirect`
  returns 403 on a direct hit; it only works as a click-through from the public
  site. (A direct hit does eventually bounce to the login form on its own, but
  slowly — not something to build on.)
* **Home and the Invoice Center are different hosts.** Login lands on `swv3`,
  which is the only page with a search box; searching crosses to `swv2h`. A
  session check pointed at `swv2h` therefore always fails and sends every run
  through a full login it did not need.
* **The Invoice Center cannot be navigated to either** — its `?search=` URL
  appears in the address bar and is the search button's href, but a direct hit
  404s.

The download is equally session-bound. The file arrives from
`InvoicePDF.aspx?v=<sort>&x=<dir>&t=<cache-buster>` — note there is **no document
identifier in it**. Which documents come back is held in server-side session
state from the ticked checkboxes, so the URL cannot be fetched on its own and
there is no shortcut around driving the page.

## Waiting

Nothing here waits on `networkidle`. The home screen is a Vue app that holds
connections open, so that state may never arrive, and a long wait for an event
that will never come is indistinguishable from a hang. Every wait is for a
concrete element, and every step is recorded in `driver.trace` with elapsed
milliseconds so a slow run says where it is instead of looking frozen.

## Selector strategy

Auth0's CSS classes are per-build hashes (`c72825458`) and are never used; its
ids are. WebForms ids look generated but are
`<framework prefix>_<authored control name>`, so controls are matched on the
stable **suffix** (`table[id$='grdInvoices']`, `input[id$='_chkItem']`).

A row is matched on its SI Doc No. cell, never on its index — downloading the
wrong invoice is the one failure reconciliation cannot catch.
"""

from __future__ import annotations

import logging
import os
import re
import shutil
import subprocess
import sys
import time
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover — typing only
    from playwright.sync_api import Locator, Page

logger = logging.getLogger(__name__)

# The Invoice Center host. Note this is NOT where the home screen lives — the
# post-login landing page is on swv3 (see PORTAL_HOME_URL), and the search on
# that page navigates across to here.
DEFAULT_BASE_URL = "https://swv2h.sportsinc.com/"

# Where login lands, and the only page carrying the search box. Confirmed from a
# live run: `landing_url: https://swv3.sportsinc.com/home`.
PORTAL_HOME_URL = "https://swv3.sportsinc.com/home"

# The login journey starts on the public site and goes through its DEALER LOGIN
# button. Navigating to the redirect URL directly returns **403** — it only
# works as a click-through from the public page. (A direct hit does eventually
# reach the login form, but only after the 403 page bounces on its own, which
# is slow and not something to depend on.)
PUBLIC_SITE_URL = "https://www.sportsinc.us/"
LOGIN_ENTRY_URL = "https://swv3.sportsinc.com/login-redirect"  # the button's href; do NOT goto
AUTH0_HOST = "sportsweb.us.auth0.com"

# The Wix button. Its classes are generated (`twJknM`, `ZhVEJq`) so the href is
# the durable hook. It carries target="_blank", which is stripped before the
# click so the flow stays in one page.
_DEALER_LOGIN_LINK = "a[href*='login-redirect']"

# The Invoice Center's own URL. Navigating to it directly 404s — the page is
# only reachable by submitting the home screen's search box, so this is
# documentation and a sanity check, not a destination.
INVOICE_CENTER_PATH = "Member/InvoiceCenter/Default.aspx"

# Home screen search box (a Vue component) — the only way in.
_HOME_SEARCH_INPUT = ".search-bar input[placeholder='Search for Invoice']"
_HOME_SEARCH_BUTTON = ".search-bar .search-button a"

# WebForms ids are generated, but their *suffixes* are the developer-authored
# control names and are stable across renders; the `ctl00$ContentPlaceHolder1$`
# prefix is the framework's. Matching on the suffix survives a page restructure
# that would move the prefix.
_GRID = "table[id$='grdInvoices']"
_ROW_CHECKBOX = "input[id$='_chkItem']"
_DOWNLOADS_LINK = "a[id$='lbDisplayDownload']"
_DOWNLOAD_DIALOG = "#downloadOptions"
_ARCHIVED_TAB = "#histInv"
_ACTIVE_TAB = "#activeInv"

# The in-grid search, which lives on both tabs. Unlike the home screen's search
# box this one is column-scoped: the dropdown must be set *before* submitting,
# or the search runs against nothing.
_SEARCH_COLUMN_SELECT = "select[id$='ddlSearchBy']"
_SEARCH_INPUT = "input[id$='tbSearch']"
_SEARCH_BUTTON = "input[id$='btnSearchInvoices']"
_INVOICE_VIEW_STATE = "input[id$='hdnInvoiceView']"

# Paging. The portal reports its own position in hidden fields — `hdnPageIndex`
# is 0-based, `hdnMaxPage` is a count — which beats inferring it from the links,
# since the whole pager is `display: none` when there is only one page.
_PAGE_INDEX_STATE = "input[id$='hdnPageIndex']"
_MAX_PAGE_STATE = "input[id$='hdnMaxPage']"
_PAGE_FIRST = "a[id$='lbFirstPage']"
_PAGE_PREV = "a[id$='lbPrevPage']"
_PAGE_NEXT = "a[id$='lbNextPage']"

# A guard against a pager that accepts clicks without moving.
_MAX_PAGE_HOPS = 60

# The dropdown's option values, which are the portal's own column names.
SEARCH_COLUMNS = {
    "po": "DealerPONum",
    "si_doc": "ASWDocNum",
    "supplier_doc": "SupplierDocNum",
    "supplier": "SupplierName",
    "si_doc_date": "ASWDocDate",
    "archived_date": "HistoricalDate",
    "due_date": "DueDate",
    "discount_date": "DiscountDate",
    "total": "DocTotal",
}

# The download dialog's options. `pdf` is the one this skill needs: every
# selected document merged into a single PDF.
#
# `csv_items` ("CSV with Header and Item Detail") looks like it should make this
# whole path unnecessary, and does not: for a header-only document it comes back
# with no item detail, because it is fed by the same EDI line data the SportsLink
# API exposes. If the CSV had the lines, the API would have had them. The other
# formats are mapped so the dialog is faithfully catalogued and `capture-portal`
# can reach them — not because any of them help here.
DOWNLOAD_FORMATS = {
    "pdf": "a[id$='lbPDFPrint']",                    # one combined PDF
    "pdf_zip": "a[id$='btnDownloadPDF']",            # one PDF per doc, zipped
    "csv": "a[id$='btnDownloadCSV']",                # header detail only
    "csv_items": "a[id$='btnDownloadWithItemDetails']",  # empty for scanned docs
    "pdf_and_csv": "a[id$='btnDownloadBoth']",
}

# The results-table columns, by header text. `SI Doc No.` identifies a row.
ROW_COLUMNS = (
    "Supplier", "Supplier Doc No.", "PO No.", "SI Doc No.",
    "SI Doc Date", "Due Date", "Archived Date", "Discount Date", "Total",
)
_TABLE_ANCHOR_HEADER = "SI Doc"

# The page's frozen-header script clones the whole `<thead>` *into* cells, so a
# naive `td.textContent` returns every column heading followed by the value.
# Cell text is therefore read with a tree walker that skips anything inside a
# cloned header; this phrase is the tell that it leaked through anyway.
_CLONED_HEADER_TELL = "SI Doc No."

_CELL_TEXT_JS = """
element => {
  const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
  const parts = [];
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.parentElement && node.parentElement.closest('thead, th')) continue;
    const text = node.textContent.trim();
    if (text) parts.push(text);
  }
  return parts.join(' ');
}
"""

# Timeouts are deliberately short enough that a stall surfaces as an error with a
# step trace rather than looking like a freeze. `networkidle` is never waited on:
# the home screen is a Vue app that holds connections open, so it may never go
# idle, and a 45s wait for an event that will not come is indistinguishable from
# a hang. Every wait below is for a concrete element instead.
_DEFAULT_TIMEOUT_MS = int(os.environ.get("SPORTSINC_WEB_TIMEOUT_MS") or 25_000)
_DOWNLOAD_TIMEOUT_MS = int(os.environ.get("SPORTSINC_WEB_DOWNLOAD_TIMEOUT_MS") or 90_000)
_POPUP_GRACE_MS = 1_500

_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# Headless differs from headed in three ways that break portals, none of them
# about rendering:
#   1. The UA says "HeadlessChrome" — overridden above.
#   2. `navigator.webdriver` is true. The launch flag hides it; the init script
#      is the belt-and-braces for builds where the flag alone does not.
#   3. The default viewport is 1280×720, which is small enough for a responsive
#      layout to collapse its desktop navigation. The home screen's search box
#      is a Vue component, and a collapsed layout could hide it entirely — so
#      the viewport is pinned to a desktop size rather than left to the default.
_STEALTH_LAUNCH_ARGS = ["--disable-blink-features=AutomationControlled"]
_VIEWPORT = {"width": 1440, "height": 900}
_MASK_WEBDRIVER = "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"


class SportsWebError(RuntimeError):
    """Portal automation failed."""

    error_type = "api_error"


class SportsWebConfigError(SportsWebError):
    """Missing credentials, a bad login, or an unsupported login challenge."""

    error_type = "config_error"


class SportsWebTransportError(SportsWebError):
    """Browser launch or navigation failure."""

    error_type = "connection_error"


# ── configuration ────────────────────────────────────────────────────────────


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() in ("1", "true", "yes", "on")


def credentials(overrides: dict[str, Any] | None = None) -> dict[str, str]:
    """Resolve portal credentials from `SPORTSINC_WEB_*` env vars.

    The portal login is **separate** from `SPORTSINC_API_KEY` — the API key is
    issued per dealer by Sports Inc; this is a SportsWeb user (an email address,
    since Auth0 fronts it). Inline overrides win over the environment, matching
    how the adidas skill handles credentials.

    Raises `SportsWebConfigError` — the agent's cue to ask the user to configure
    them — rather than prompting for secrets in chat.
    """

    overrides = overrides or {}
    username = str(overrides.get("username") or os.environ.get("SPORTSINC_WEB_USERNAME") or "").strip()
    password = str(overrides.get("password") or os.environ.get("SPORTSINC_WEB_PASSWORD") or "").strip()
    base_url = str(
        overrides.get("base_url") or os.environ.get("SPORTSINC_WEB_BASE_URL") or DEFAULT_BASE_URL
    ).strip()
    home_url = str(
        overrides.get("home_url") or os.environ.get("SPORTSINC_WEB_HOME_URL") or PORTAL_HOME_URL
    ).strip()

    missing = [name for name, value in (("username", username), ("password", password)) if not value]
    if missing:
        raise SportsWebConfigError(
            "SportsWeb portal credentials are not configured (missing "
            + ", ".join(missing)
            + "). Set SPORTSINC_WEB_USERNAME / SPORTSINC_WEB_PASSWORD — the dealer's "
            "SportsWeb login, separate from SPORTSINC_API_KEY. Never ask for them in chat."
        )
    return {
        "username": username,
        "password": password,
        "base_url": base_url.rstrip("/") + "/",
        "home_url": home_url.rstrip("/"),
    }


def _storage_state_path() -> str | None:
    """Where to persist the logged-in session, if the operator wants one.

    Reusing a session avoids a full Auth0 round trip per run — and is the escape
    hatch if Auth0 ever adds a challenge that automation cannot answer: log in
    once by hand with this file set, and later runs ride the saved cookies.
    """

    return (os.environ.get("SPORTSINC_WEB_STATE_PATH") or "").strip() or None


def _headless() -> bool:
    override = os.environ.get("SPORTSINC_WEB_HEADLESS")
    return True if override is None else _truthy(override)


# ── browser plumbing ─────────────────────────────────────────────────────────


def _install_chromium() -> None:
    """Download Playwright's Chromium binary (one-time, ~150 MB)."""

    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)


def _launch(playwright, headless: bool):
    """Launch Chromium, auto-installing the browser binary if it is missing.

    The Playwright *package* is a declared dependency, but its Chromium *binary*
    is a separate download pip does not fetch and OpenClaw has no install hook
    for, so the first run installs it once and retries.
    """

    try:
        return playwright.chromium.launch(headless=headless, args=_STEALTH_LAUNCH_ARGS)
    except Exception as exc:  # noqa: BLE001
        message = str(exc).lower()
        if not ("executable doesn't exist" in message or "playwright install" in message):
            raise SportsWebTransportError(
                f"Could not launch Chromium for Playwright: {exc}"
            ) from exc
        logger.info("Chromium binary missing — installing it once (~150 MB)…")
        try:
            _install_chromium()
        except Exception as install_exc:  # noqa: BLE001
            raise SportsWebConfigError(
                "Chromium is not installed and the automatic install failed. Run "
                f"`python -m playwright install chromium`. (error: {install_exc})"
            ) from install_exc
        try:
            return playwright.chromium.launch(headless=headless, args=_STEALTH_LAUNCH_ARGS)
        except Exception as retry_exc:  # noqa: BLE001
            raise SportsWebConfigError(
                "Could not launch Chromium even after installing it — check the "
                f"container has the required system libraries. (error: {retry_exc})"
            ) from retry_exc


def _stop_process(proc) -> None:
    if not proc or proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:  # noqa: BLE001
        proc.kill()


def _headed_needs_virtual_display() -> bool:
    """True only when a headed browser must fall back to Xvfb (Linux, no display)."""

    if not sys.platform.startswith("linux"):
        return False
    return not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def _start_virtual_display():
    """Start an Xvfb display for headed Chromium on a Linux host with no X server."""

    xvfb = shutil.which("Xvfb")
    if not xvfb:
        raise SportsWebConfigError(
            "Headed mode needs a virtual display, but the Xvfb binary is not installed. "
            "Install it (`apt-get install -y xvfb`) or leave SPORTSINC_WEB_HEADLESS unset "
            "to run headless."
        )
    read_fd, write_fd = os.pipe()
    try:
        proc = subprocess.Popen(
            [xvfb, "-displayfd", str(write_fd), "-screen", "0", "1440x900x24", "-nolisten", "tcp"],
            pass_fds=(write_fd,),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    finally:
        os.close(write_fd)
    with os.fdopen(read_fd) as handle:
        display_num = handle.readline().strip()
    if not display_num or proc.poll() is not None:
        _stop_process(proc)
        raise SportsWebConfigError("Could not start an Xvfb virtual display.")
    os.environ["DISPLAY"] = f":{display_num}"
    return proc


@contextmanager
def _browser_page(headless: bool):
    """Yield a ready `Page`, tearing down the browser (and Xvfb) afterwards."""

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover — runtime guard
        raise SportsWebConfigError(
            "playwright is required for the SportsWeb portal flow. Install it (see the "
            "skill's install deps) and it will fetch its Chromium binary on first use."
        ) from exc

    display_proc = None
    if not headless and _headed_needs_virtual_display():
        display_proc = _start_virtual_display()

    state_path = _storage_state_path()
    with sync_playwright() as playwright:
        browser = _launch(playwright, headless)
        context_args: dict[str, Any] = {
            "user_agent": _USER_AGENT,
            "accept_downloads": True,
            "viewport": _VIEWPORT,
            "locale": "en-US",
        }
        if state_path and os.path.isfile(state_path):
            context_args["storage_state"] = state_path
        context = browser.new_context(**context_args)
        context.set_default_timeout(_DEFAULT_TIMEOUT_MS)
        context.add_init_script(_MASK_WEBDRIVER)
        page = context.new_page()
        try:
            yield page
        finally:
            if state_path:
                try:
                    context.storage_state(path=state_path)
                except Exception:  # noqa: BLE001 — persisting the session is a nicety
                    logger.warning("Could not save the SportsWeb session to %s", state_path)
            context.close()
            browser.close()
            _stop_process(display_proc)


def _clean(value: str | None) -> str:
    return " ".join((value or "").split())


def looks_like_cloned_header(value: str | None) -> bool:
    """True when a cell's text still carries the cloned column headings.

    The Invoice Center's frozen-header script duplicates the entire `<thead>`
    inside individual cells, so a cell read naively comes back as
    `"Supplier Supplier Doc No. PO No. … Total P13554"`. Reading that as a PO
    number would silently select the wrong invoice, so every parsed cell is
    checked and a leak is raised rather than trimmed — trimming would guess.
    """

    return _CLONED_HEADER_TELL in (value or "")


# ── driver ───────────────────────────────────────────────────────────────────


class SportsWebDriver:
    """Drives the SportsWeb portal: log in, search the Invoice Center, download."""

    def __init__(self, page: "Page", base_url: str, home_url: str | None = None) -> None:
        self.page = page
        self.base_url = base_url.rstrip("/") + "/"
        self.home_url = (home_url or PORTAL_HOME_URL).rstrip("/")
        self.trace: list[dict[str, Any]] = []
        self._started = time.monotonic()

    def _step(self, name: str, **detail: Any) -> None:
        """Record a step with elapsed milliseconds.

        The trace is returned by `capture-portal` and attached to failures, so a
        slow or stuck run says *where* it is rather than looking like a freeze.
        """

        entry = {"step": name, "ms": int((time.monotonic() - self._started) * 1000)}
        entry.update(detail)
        self.trace.append(entry)
        logger.info("sportsweb: %s", entry)

    # -- auth -------------------------------------------------------------

    def login(self, creds: dict[str, str]) -> str:
        """Log in through Auth0 Universal Login. Returns the landing URL.

        Entry is the public site's DEALER LOGIN button, **not** the redirect URL
        it points at: navigating to that directly returns 403. Skipped entirely
        when a persisted session is still valid.
        """

        if self._restore_session():
            self._step("session-restored", url=self.page.url)
            return self.page.url

        self._open_login_form()
        self._step("login-form-visible", url=self.page.url)

        self.page.fill("input#username", creds["username"])
        self.page.fill("input#password", creds["password"])
        # The primary submit is `<button type=submit name=action value=default>`;
        # its classes are Auth0 build hashes and must not be used.
        self.page.click("button[type=submit][name=action]")
        self._step("credentials-submitted")

        # The definitive "we are in" signal is the home screen's search box —
        # not a load state, which a Vue app may never settle into.
        try:
            self.page.wait_for_selector(_HOME_SEARCH_INPUT, timeout=_DEFAULT_TIMEOUT_MS)
        except Exception as exc:  # noqa: BLE001
            if AUTH0_HOST in self.page.url:
                self._raise_login_failure()
            raise SportsWebTransportError(
                "Signed in, but the home screen's search box never appeared "
                f"(ended at {self.page.url}). Trace: {self.trace}"
            ) from exc

        self.home_url = self.page.url
        self._step("logged-in", url=self.page.url)
        return self.page.url

    def _open_login_form(self) -> None:
        """Public site → DEALER LOGIN → Auth0.

        The button carries `target="_blank"`, which is stripped so the flow stays
        in one page; if a popup opens anyway it is adopted.
        """

        try:
            self.page.goto(PUBLIC_SITE_URL, wait_until="domcontentloaded")
        except Exception as exc:  # noqa: BLE001
            raise SportsWebTransportError(
                f"Could not reach the public site ({PUBLIC_SITE_URL}): {exc}"
            ) from exc
        self._step("public-site-loaded")

        link = self.page.locator(_DEALER_LOGIN_LINK).first
        if not link.count():
            link = self.page.get_by_role("link", name=re.compile("dealer login", re.I)).first
        if not link.count():
            raise SportsWebError(
                f"The DEALER LOGIN button was not found on {PUBLIC_SITE_URL}. "
                "The public site may have been restyled."
            )
        try:
            link.evaluate("element => element.removeAttribute('target')")
        except Exception:  # noqa: BLE001 — popup handling below covers it
            pass

        context = self.page.context
        before = len(context.pages)
        link.click()
        self.page.wait_for_timeout(_POPUP_GRACE_MS)
        if len(context.pages) > before:
            self.page = context.pages[-1]
            self._step("adopted-login-popup")

        try:
            self.page.wait_for_selector("input#username", timeout=_DEFAULT_TIMEOUT_MS)
        except Exception as exc:  # noqa: BLE001
            raise SportsWebTransportError(
                "The Auth0 login form never appeared after clicking DEALER LOGIN "
                f"(ended at {self.page.url}). Trace: {self.trace}"
            ) from exc

    def _restore_session(self) -> bool:
        """Is a persisted session still good? Checks the *home* page (swv3).

        Checking the Invoice Center host instead would always fail — that host
        serves the grid, not the search box — and send every run through a full
        login it did not need.
        """

        if not _storage_state_path():
            return False
        try:
            self.page.goto(self.home_url, wait_until="domcontentloaded")
        except Exception:  # noqa: BLE001
            return False
        if AUTH0_HOST in self.page.url:
            return False
        try:
            self.page.wait_for_selector(_HOME_SEARCH_INPUT, timeout=8_000)
            return True
        except Exception:  # noqa: BLE001
            return False

    def _raise_login_failure(self) -> None:
        """Still on Auth0 after submitting — say precisely why."""

        url = self.page.url
        if "/mfa" in url or "/u/mfa" in url:
            raise SportsWebConfigError(
                "SportsWeb login hit a multi-factor challenge, which this skill cannot "
                "answer. Log in once by hand with SPORTSINC_WEB_STATE_PATH set to a file "
                "path — the session is saved there and reused on later runs."
            )
        message = ""
        for selector in ("#ulp-error-announcer", "[role=alert]", ".ulp-error-info:visible"):
            try:
                found = self.page.locator(selector).first
                if found.count() and found.is_visible():
                    message = _clean(found.text_content())
                    break
            except Exception:  # noqa: BLE001
                continue
        raise SportsWebConfigError(
            "SportsWeb login failed — check SPORTSINC_WEB_USERNAME / "
            "SPORTSINC_WEB_PASSWORD."
            + (f" Auth0 said: {message}" if message else f" (still at {url})")
        )

    # -- invoice center ---------------------------------------------------

    def open_invoice_center(self, search: str) -> str:
        """Search from the home screen and land on the Invoice Center results.

        The Invoice Center URL cannot be navigated to directly — it 404s — so
        the only way in is the home screen's search box. The search button *is*
        an anchor carrying the results URL, but it is built by the page's own
        script, so it gets clicked rather than read and re-navigated.
        """

        if not self.page.locator(_HOME_SEARCH_INPUT).count():
            try:
                self.page.goto(self.home_url, wait_until="domcontentloaded")
            except Exception as exc:  # noqa: BLE001
                raise SportsWebTransportError(
                    f"Could not open the SportsWeb home screen ({self.home_url}): {exc}"
                ) from exc

        if AUTH0_HOST in self.page.url:
            raise SportsWebConfigError(
                "The portal bounced back to the Auth0 login — the session did not carry "
                "over. If SPORTSINC_WEB_STATE_PATH is set, delete that file and retry."
            )

        try:
            self.page.wait_for_selector(_HOME_SEARCH_INPUT, timeout=_DEFAULT_TIMEOUT_MS)
            self.page.fill(_HOME_SEARCH_INPUT, str(search))
            self.page.click(_HOME_SEARCH_BUTTON)
        except Exception as exc:  # noqa: BLE001
            raise SportsWebTransportError(
                f"Could not run the home-screen search for {search!r} on {self.page.url}: "
                f"{exc}. Trace: {self.trace}"
            ) from exc
        self._step("search-submitted", search=str(search))

        # Wait for the grid itself — the search crosses hosts (swv3 → swv2h), so
        # a load-state wait would be watching the wrong page for part of it.
        try:
            self.page.wait_for_selector(_GRID, timeout=_DEFAULT_TIMEOUT_MS)
        except Exception as exc:  # noqa: BLE001
            raise SportsWebError(
                f"The Invoice Center results grid never appeared after searching {search!r} "
                f"(ended at {self.page.url}). Trace: {self.trace}"
            ) from exc
        self._step("grid-loaded", url=self.page.url)
        return self.page.url

    def _click_postback(self, locator: "Locator") -> None:
        """Click a control that submits the WebForms page, and wait for the reload.

        Every button here is a real form submit, so the click is a navigation.
        Waiting for it is what separates "the new results are on screen" from
        "the old results are still on screen and about to be replaced" — reading
        rows in that gap returns the *previous* search.
        """

        from playwright.sync_api import TimeoutError as PlaywrightTimeout

        try:
            with self.page.expect_navigation(
                wait_until="domcontentloaded", timeout=_DEFAULT_TIMEOUT_MS
            ):
                locator.click()
        except PlaywrightTimeout:
            # Some controls are handled client-side; give the DOM a moment and
            # let the caller's own wait decide whether it actually worked.
            self.page.wait_for_timeout(1_000)

    def search_in_grid(self, term: Any, column: str = "po") -> None:
        """Run the results page's own column-scoped search.

        The dropdown must be set before submitting — it defaults to
        `-- select search column --`, which matches nothing. `column` is a key of
        `SEARCH_COLUMNS` or one of the portal's raw column names.
        """

        value = SEARCH_COLUMNS.get(column, column)
        if value not in SEARCH_COLUMNS.values():
            raise SportsWebError(
                f"Unknown search column {column!r}. "
                f"Valid: {', '.join(sorted(SEARCH_COLUMNS))}."
            )
        try:
            self.page.select_option(_SEARCH_COLUMN_SELECT, value)
            self.page.fill(_SEARCH_INPUT, str(term))
            self._click_postback(self.page.locator(_SEARCH_BUTTON).first)
            self.page.wait_for_selector(_GRID, timeout=_DEFAULT_TIMEOUT_MS)
        except SportsWebError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise SportsWebError(
                f"The in-grid search for {term!r} by {value} failed: {exc}. "
                f"Trace: {self.trace}"
            ) from exc
        self._step("grid-search", term=str(term), column=value)

    def show_archived(self, search: Any = None, column: str = "po") -> None:
        """Switch to Archived Invoices and re-run the search there.

        Switching tabs **resets the result set** — the archived tab does not
        inherit the home screen's search. So a document is only found here by
        searching again with the results page's own column-scoped box, which is
        why this takes the search term rather than just clicking the tab.
        """

        tab = self.page.locator(_ARCHIVED_TAB)
        if not tab.count():
            raise SportsWebError("The 'Archived Invoices' tab was not found.")
        self._click_postback(tab.first)
        try:
            self.page.wait_for_selector(_GRID, timeout=_DEFAULT_TIMEOUT_MS)
        except Exception as exc:  # noqa: BLE001
            raise SportsWebError(f"The Archived tab did not load: {exc}") from exc

        # The portal tracks the active view itself; use it rather than trusting
        # the click landed.
        view = self._invoice_view()
        self._step("archived-tab-shown", invoice_view=view)
        if view and view.lower() not in ("historical", "archived"):
            raise SportsWebError(
                f"Clicking the Archived tab left the portal on the {view!r} view. "
                "Refusing to search the wrong tab."
            )

        if search is not None:
            self.search_in_grid(search, column)

    def _invoice_view(self) -> str | None:
        try:
            field = self.page.locator(_INVOICE_VIEW_STATE).first
            return field.input_value() if field.count() else None
        except Exception:  # noqa: BLE001
            return None

    def _results_table(self) -> "Locator | None":
        """The results grid. Prefers the control's own id suffix, falls back to
        header text."""

        grid = self.page.locator(_GRID)
        try:
            if grid.count():
                return grid.first
        except Exception:  # noqa: BLE001
            pass
        tables = self.page.locator("table")
        try:
            count = tables.count()
        except Exception:  # noqa: BLE001
            return None
        for index in range(count):
            table = tables.nth(index)
            try:
                headers = self._header_texts(table)
            except Exception:  # noqa: BLE001
                continue
            if any(_TABLE_ANCHOR_HEADER in header for header in headers):
                return table
        return None

    @staticmethod
    def _header_texts(table: "Locator") -> list[str]:
        """The real column headings.

        Scoped to the table's *direct* `thead` because the frozen-header script
        clones `<thead>` into body cells; an unscoped `th` lookup would return
        those clones too and shift every column index.
        """

        return [
            _clean(text)
            for text in table.locator(":scope > thead > tr > th").all_text_contents()
        ]

    def _header_index(self, table: "Locator") -> dict[str, int]:
        return {header: position for position, header in enumerate(self._header_texts(table)) if header}

    def _data_rows(self, table: "Locator") -> "Locator":
        return table.locator(":scope > tbody > tr.gridview-row, :scope > tbody > tr.gridview-alt-row")

    def _cell_text(self, cell: "Locator") -> str:
        """A cell's own text, ignoring any cloned header markup inside it."""

        try:
            return _clean(cell.evaluate(_CELL_TEXT_JS))
        except Exception:  # noqa: BLE001 — fall back to the naive read
            return _clean(cell.text_content())

    def read_rows(self) -> list[dict[str, Any]]:
        """Read the result rows as dicts keyed by column header.

        Each row carries `row_index` so it can be ticked later. Columns are
        addressed by header name, so a reordered grid still reads correctly.
        """

        table = self._results_table()
        if table is None:
            return []
        columns = self._header_index(table)
        rows = self._data_rows(table)
        out: list[dict[str, Any]] = []
        for index in range(rows.count()):
            row = rows.nth(index)
            cells = row.locator(":scope > td")
            values = [self._cell_text(cells.nth(position)) for position in range(cells.count())]
            if not values:
                continue
            entry: dict[str, Any] = {"row_index": index}
            for header, position in columns.items():
                if position < len(values):
                    entry[header] = values[position]
            leaked = [
                header for header, value in entry.items()
                if isinstance(value, str) and looks_like_cloned_header(value)
            ]
            if leaked:
                raise SportsWebError(
                    "The results grid could not be parsed: column "
                    f"{leaked[0]!r} came back carrying the table's own headings, which "
                    "means the frozen-header markup leaked into the cell text. Refusing "
                    "to match rows on it — a wrong row here downloads the wrong invoice."
                )
            if any(entry.get(key) for key in ("SI Doc No.", "PO No.")):
                out.append(entry)
        return out

    def _int_state(self, selector: str, default: int) -> int:
        try:
            field = self.page.locator(selector).first
            if not field.count():
                return default
            return int(str(field.input_value()).strip() or default)
        except Exception:  # noqa: BLE001
            return default

    def page_position(self) -> tuple[int, int]:
        """`(current 0-based page index, total pages)` from the portal's own state."""

        return (
            self._int_state(_PAGE_INDEX_STATE, 0),
            max(self._int_state(_MAX_PAGE_STATE, 1), 1),
        )

    def goto_page(self, target: int) -> None:
        """Walk the pager to `target` (0-based), verifying progress each hop.

        Clicks Next/Prev rather than the numbered links, which only ever show a
        five-page window. Progress is checked against `hdnPageIndex` after every
        hop so a pager that accepts clicks without moving fails loudly instead of
        spinning.
        """

        current, total = self.page_position()
        if not 0 <= target < total:
            raise SportsWebError(f"Page {target} is out of range (the grid has {total}).")

        hops = 0
        while current != target:
            hops += 1
            if hops > _MAX_PAGE_HOPS:
                raise SportsWebError(
                    f"Gave up paging to page {target}: stuck at {current} after "
                    f"{hops} hops."
                )
            selector = _PAGE_NEXT if target > current else _PAGE_PREV
            link = self.page.locator(selector).first
            if not link.count():
                raise SportsWebError(
                    f"The results grid has {total} pages but no pager link "
                    f"({selector}) to reach page {target}."
                )
            self._click_postback(link)
            self.page.wait_for_selector(_GRID, timeout=_DEFAULT_TIMEOUT_MS)
            moved, _ = self.page_position()
            if moved == current:
                raise SportsWebError(
                    f"Clicking the pager did not move off page {current} "
                    f"(target {target})."
                )
            current = moved
        self._step("paged-to", page=current)

    def read_all_rows(self) -> list[dict[str, Any]]:
        """Every row across every page, each tagged with the page it is on.

        `read_rows()` sees one page. A PO with more invoices than fit on a page
        would otherwise return a short set with no indication anything was
        missing — the caller cannot tell "this document is not here" from "this
        document is on page 3", and would report the first as if it were true.
        """

        start, total = self.page_position()
        if total <= 1:
            return [dict(row, page_index=start) for row in self.read_rows()]

        collected: list[dict[str, Any]] = []
        for index in range(total):
            self.goto_page(index)
            collected.extend(dict(row, page_index=index) for row in self.read_rows())
        self._step("read-all-pages", pages=total, rows=len(collected))
        return collected

    def select_rows(self, rows: list[dict[str, Any]]) -> int:
        """Tick each row's own checkbox. Returns how many were ticked.

        Targets the row checkbox by its `chkItem` id suffix rather than "the
        first checkbox in the row" — the cloned header markup inside each row
        carries a copy of the select-all `chkAll` box, which a positional lookup
        would find first.
        """

        table = self._results_table()
        if table is None:
            raise SportsWebError("The Invoice Center results grid was not found.")
        all_rows = self._data_rows(table)
        ticked = 0
        for row in rows:
            checkbox = all_rows.nth(row["row_index"]).locator(_ROW_CHECKBOX).first
            if not checkbox.count():
                raise SportsWebError(
                    f"No selection checkbox on the row for SI Doc {row.get('SI Doc No.')}."
                )
            try:
                # `force` skips Playwright's actionability wait. The cell also
                # holds the cloned header markup, which can sit over the real
                # checkbox — without `force` the click waits for it to become
                # hittable and stalls out. The event still fires normally, so
                # the page's own selection handlers run.
                checkbox.click(force=True)
                if not checkbox.is_checked():
                    checkbox.check(force=True)
                ticked += 1
            except Exception as exc:  # noqa: BLE001
                raise SportsWebError(
                    f"Could not select the row for SI Doc {row.get('SI Doc No.')}: {exc}. "
                    f"Trace: {self.trace}"
                ) from exc
        self._step("rows-selected", count=ticked)
        return ticked

    def download_selected(self, download_format: str = "pdf") -> tuple[bytes, str | None, str]:
        """Open the download dialog, pick a format, and capture the file.

        Two steps, not one: **Downloads** is a `__doPostBack` that opens an
        in-page dialog, and the actual download is a second link inside it.
        `pdf` merges every ticked document into a single file — the shape
        `invoice_pdf.prepare` segments.

        Returns `(bytes, url, mechanism)`; `mechanism` says whether the file
        arrived as a browser download or an inline response.
        """

        from playwright.sync_api import TimeoutError as PlaywrightTimeout

        option = DOWNLOAD_FORMATS.get(download_format)
        if option is None:
            raise SportsWebError(
                f"Unknown download format {download_format!r}. "
                f"Valid: {', '.join(sorted(DOWNLOAD_FORMATS))}."
            )

        trigger = self.page.locator(_DOWNLOADS_LINK)
        if not trigger.count():
            raise SportsWebError("The Invoice Center 'Downloads' control was not found.")
        trigger.first.click()
        self._step("downloads-clicked")

        # The dialog element is present in the DOM before it is opened, so wait
        # for it to become *visible* rather than merely to exist.
        try:
            self.page.wait_for_selector(f"{_DOWNLOAD_DIALOG}:visible", timeout=_DEFAULT_TIMEOUT_MS)
        except Exception as exc:  # noqa: BLE001
            raise SportsWebError(
                "The download options dialog did not open after clicking 'Downloads' — "
                "the portal may not have registered any selected rows. "
                f"Trace: {self.trace}"
            ) from exc
        self._step("download-dialog-open")

        chosen = self.page.locator(f"{_DOWNLOAD_DIALOG} {option}")
        if not chosen.count():
            raise SportsWebError(
                f"The {download_format!r} option was not in the download dialog."
            )

        responses: list[Any] = []

        def _watch(response: Any) -> None:
            try:
                content_type = (response.headers or {}).get("content-type", "").lower()
            except Exception:  # noqa: BLE001
                return
            if any(kind in content_type for kind in ("application/pdf", "octet-stream", "zip", "csv")):
                responses.append(response)

        self.page.on("response", _watch)
        try:
            with self.page.expect_download(timeout=_DOWNLOAD_TIMEOUT_MS) as download_info:
                chosen.first.click(force=True)
            download = download_info.value
            self._step("download-event", url=download.url)
            path = download.path()
            if not path:
                raise SportsWebError("The download completed but produced no file.")
            with open(path, "rb") as handle:
                data = handle.read()
            try:
                download.delete()  # we hold the bytes; don't leave a temp file behind
            except Exception:  # noqa: BLE001
                pass
            return data, download.url or None, "download"
        except PlaywrightTimeout:
            pass
        finally:
            try:
                self.page.remove_listener("response", _watch)
            except Exception:  # noqa: BLE001
                pass

        # No download event — did the file come back as an ordinary response?
        for response in reversed(responses):
            try:
                body = response.body()
            except Exception:  # noqa: BLE001
                continue
            if body:
                return body, response.url, "response"

        raise SportsWebError(
            f"Choosing '{download_format}' produced neither a download nor a file response "
            f"within {_DOWNLOAD_TIMEOUT_MS // 1000}s. Run `capture-portal` with "
            "probe_download to record what the click actually does."
        )

    def describe(self) -> dict[str, Any]:
        """Diagnostics for the capture harness: what is actually on this page."""

        table = self._results_table()
        described: dict[str, Any] = {
            "url": self.page.url,
            "title": self.page.title(),
            "results_grid_found": table is not None,
            "headers": self._header_index(table) if table is not None else {},
            "elements": {},
        }
        for label, selector in (
            ("home_search_input", _HOME_SEARCH_INPUT),
            ("home_search_button", _HOME_SEARCH_BUTTON),
            ("grid", _GRID),
            ("row_checkboxes", _ROW_CHECKBOX),
            ("downloads_link", _DOWNLOADS_LINK),
            ("download_dialog", _DOWNLOAD_DIALOG),
            ("active_tab", _ACTIVE_TAB),
            ("archived_tab", _ARCHIVED_TAB),
        ):
            try:
                described["elements"][label] = self.page.locator(selector).count()
            except Exception:  # noqa: BLE001
                described["elements"][label] = None
        # The portal tracks its own state in hidden fields; reading them is a
        # cheap cross-check that we are on the tab and page we think we are.
        described["state"] = {}
        for name in ("hdnInvoiceView", "hdnIsSearch", "hdnPageIndex", "hdnMaxPage"):
            try:
                field = self.page.locator(f"input[id$='{name}']").first
                described["state"][name] = field.input_value() if field.count() else None
            except Exception:  # noqa: BLE001
                described["state"][name] = None
        try:
            described["row_count"] = len(self.read_rows()) if table is not None else 0
        except SportsWebError as exc:
            described["row_count"] = None
            described["row_parse_error"] = str(exc)
        return described

    def save_page(self, html_path: str | None, screenshot_path: str | None) -> None:
        if html_path:
            try:
                with open(html_path, "w", encoding="utf-8") as handle:
                    handle.write(self.page.content())
            except Exception as exc:  # noqa: BLE001
                logger.warning("Could not save page HTML to %s: %s", html_path, exc)
        if screenshot_path:
            try:
                self.page.screenshot(path=screenshot_path, full_page=True)
            except Exception as exc:  # noqa: BLE001
                logger.warning("Could not save screenshot to %s: %s", screenshot_path, exc)


# ── entry points ─────────────────────────────────────────────────────────────


def _capture_failure(driver: "SportsWebDriver", label: str) -> dict[str, Any]:
    """Dump a screenshot and the page HTML when something goes wrong.

    A headless run has no window to look at, so a failure with no artefact is a
    failure you have to reproduce before you can diagnose. Writing them at the
    moment of the error means the first failing run is also the diagnostic one.
    """

    artefacts: dict[str, Any] = {"url": None, "screenshot": None, "html": None}
    try:
        from invoice_pdf import scratch_dir  # noqa: E402  (lazy, sibling module)

        directory = scratch_dir()
        safe = "".join(ch for ch in str(label) if ch.isalnum() or ch in "._-") or "portal"
        screenshot = str(directory / f"failure-{safe}.png")
        html = str(directory / f"failure-{safe}.html")
        artefacts["url"] = driver.page.url
        driver.save_page(html, screenshot)
        artefacts["screenshot"] = screenshot
        artefacts["html"] = html
    except Exception as exc:  # noqa: BLE001 — diagnostics must never mask the real error
        logger.warning("Could not capture failure artefacts: %s", exc)
    return artefacts


def _describe_failure(exc: Exception, driver: "SportsWebDriver", label: str) -> str:
    artefacts = _capture_failure(driver, label)
    parts = [str(exc)]
    if artefacts["url"]:
        parts.append(f"Ended at {artefacts['url']}.")
    if artefacts["screenshot"]:
        parts.append(
            f"Screenshot: {artefacts['screenshot']} — HTML: {artefacts['html']}."
        )
    parts.append(f"Steps completed: {driver.trace}")
    return " ".join(parts)


def _match_rows(
    rows: list[dict[str, Any]],
    si_doc_number: Any,
    supplier_doc_number: str | None,
) -> list[dict[str, Any]]:
    """Narrow a PO's rows to the requested document, if one was named."""

    if si_doc_number is None and not supplier_doc_number:
        return rows

    def _digits(value: Any) -> str:
        return "".join(character for character in str(value or "") if character.isdigit())

    wanted_si = _digits(si_doc_number) if si_doc_number is not None else None
    wanted_supplier = _digits(supplier_doc_number) if supplier_doc_number else None
    matched = [
        row for row in rows
        if (wanted_si and _digits(row.get("SI Doc No.")) == wanted_si)
        # The supplier's number is punctuated differently on either side
        # (SI3503366 vs SI-3503366), so compare on digits alone.
        or (wanted_supplier and _digits(row.get("Supplier Doc No.")) == wanted_supplier)
    ]
    return matched


def fetch_invoice_pdf(
    *,
    si_doc_number: Any = None,
    po_number: str | None = None,
    supplier_doc_number: str | None = None,
    credentials_override: dict[str, Any] | None = None,
    headless: bool | None = None,
) -> tuple[bytes, str | None, dict[str, Any]]:
    """Log in, find the document(s), and return `(pdf_bytes, source_url, meta)`.

    Searches by `po_number` when given (the portal's own search key), otherwise
    by the SI document number, then ticks the matching row(s) and downloads.
    Ticking one row yields that document; ticking several yields one combined
    PDF — `invoice_pdf.prepare` segments either shape.

    **Active first, then Archived, always.** No caller has to know which tab a
    document lives on; a miss on Active automatically re-runs the search on
    Archived. `meta["tab"]` reports where it was actually found, which is not
    cosmetic — see below.
    """

    creds = credentials(credentials_override)
    search = str(po_number or si_doc_number or "").strip()
    if not search:
        raise SportsWebConfigError("Pass a `po_number` or `si_doc_number` to search for.")

    use_headless = _headless() if headless is None else headless
    with _browser_page(use_headless) as page:
        driver = SportsWebDriver(page, creds["base_url"], creds["home_url"])
        try:
            return _fetch(
                driver, creds, search, si_doc_number, po_number, supplier_doc_number
            )
        except SportsWebError as exc:
            # Re-raise the same class, with a screenshot, the HTML and the step
            # trace attached — headless has no window to look at afterwards.
            raise type(exc)(_describe_failure(exc, driver, search)) from exc


def _fetch(
    driver: "SportsWebDriver",
    creds: dict[str, str],
    search: str,
    si_doc_number: Any,
    po_number: str | None,
    supplier_doc_number: str | None,
) -> tuple[bytes, str | None]:
    """The fetch itself. Split out so its caller can attach failure artefacts."""

    driver.login(creds)
    url = driver.open_invoice_center(search)

    rows = [dict(row, page_index=driver.page_position()[0]) for row in driver.read_rows()]
    wanted = _match_rows(rows, si_doc_number, supplier_doc_number)
    tab = "active"
    _, total_pages = driver.page_position()

    # A PO with more invoices than fit on a page is common, and page 1 alone
    # cannot tell "not here" from "on page 3". Two ways out, cheapest first:
    if not wanted and total_pages > 1:
        if si_doc_number is not None:
            # Narrowing beats paging: searching the grid by SI Doc No. collapses
            # the result to the single row we want, on page 1, in one postback —
            # no matter how many pages the PO spans.
            driver.search_in_grid(si_doc_number, "si_doc")
            rows = [dict(row, page_index=0) for row in driver.read_rows()]
            wanted = _match_rows(rows, si_doc_number, supplier_doc_number)
        if not wanted:
            # Whole-PO fetch, or the narrow found nothing: walk every page.
            rows = driver.read_all_rows()
            wanted = _match_rows(rows, si_doc_number, supplier_doc_number)
    elif total_pages > 1 and si_doc_number is None:
        # A PO-level fetch must cover every page even when page 1 had matches,
        # or it silently bills a subset of the PO.
        rows = driver.read_all_rows()
        wanted = _match_rows(rows, si_doc_number, supplier_doc_number)

    # A document that has already been marked historical lives on the Archived
    # tab, so a miss on Active is not necessarily a miss. This runs
    # automatically — a caller should never have to know which tab a document
    # is on, and often cannot. Switching tabs resets the results, so the search
    # is re-run there: by PO when that is what we searched with, otherwise by
    # SI doc number.
    if not wanted:
        column = "po" if po_number else "si_doc"
        driver.show_archived(search, column)
        archived = driver.read_all_rows()
        wanted = _match_rows(archived, si_doc_number, supplier_doc_number)
        if wanted:
            rows = archived
            tab = "archived"

    if not rows:
        raise SportsWebError(
            f"No Invoice Center rows matched {search!r} on either the Active or "
            "Archived tab. Check the search term is a PO number."
        )
    if not wanted:
        found = ", ".join(str(row.get("SI Doc No.")) for row in rows)
        raise SportsWebError(
            f"SI document {si_doc_number} was not among the rows for {search!r} "
            f"(found: {found})."
        )

    # Selection is per page — paging is a postback that re-renders the grid, so
    # ticks do not survive it. Rows spanning pages are therefore downloaded a
    # page at a time and the parts stitched back together, which leaves the rest
    # of the pipeline oblivious: `prepare()` segments the combined file exactly
    # as it does a single-page download.
    from invoice_pdf import merge_pdfs  # noqa: E402  (lazy, sibling module)

    by_page: dict[int, list[dict[str, Any]]] = {}
    for row in wanted:
        by_page.setdefault(row.get("page_index", 0), []).append(row)

    parts: list[bytes] = []
    source_url = None
    for page_index in sorted(by_page):
        if len(by_page) > 1 or page_index != driver.page_position()[0]:
            driver.goto_page(page_index)
        driver.select_rows(by_page[page_index])
        part, part_url, _mechanism = driver.download_selected("pdf")
        parts.append(part)
        source_url = source_url or part_url

    data = merge_pdfs(parts)
    return data, source_url or url, {
        "tab": tab,
        "pages_searched": total_pages,
        "download_parts": len(parts),
        "matched_rows": [
            {key: row.get(key) for key in ("SI Doc No.", "Supplier Doc No.", "PO No.", "Total")}
            for row in wanted
        ],
    }


def capture_portal(
    *,
    search: str | None = None,
    archived: bool = False,
    search_column: str = "po",
    probe_download: bool = False,
    download_format: str = "pdf",
    save_download_to: str | None = None,
    html_path: str | None = None,
    screenshot_path: str | None = None,
    credentials_override: dict[str, Any] | None = None,
    headless: bool | None = None,
) -> dict[str, Any]:
    """Diagnostic run: log in, search, and report what the portal actually does.

    Read-only unless `probe_download` is set, and even then it only downloads a
    PDF — nothing is modified either way. This exists so the remaining unknowns
    in `references/sportsweb_flow_notes.md` get answered by a real run instead of
    by guesswork.
    """

    creds = credentials(credentials_override)
    use_headless = _headless() if headless is None else headless
    result: dict[str, Any] = {
        "base_url": creds["base_url"],
        "home_url": creds["home_url"],
        "headless": use_headless,
        "viewport": _VIEWPORT,
    }

    with _browser_page(use_headless) as page:
        driver = SportsWebDriver(page, creds["base_url"], creds["home_url"])
        try:
            result["landing_url"] = driver.login(creds)
        except SportsWebError as exc:
            # A failed capture is the run that most needs artefacts — this is
            # the harness whose whole job is to explain what happened.
            result["logged_in"] = False
            result["error"] = _describe_failure(exc, driver, search or "portal")
            result["trace"] = driver.trace
            return result
        result["logged_in"] = True

        if search:
            result["search"] = search
            try:
                result["invoice_center_url"] = driver.open_invoice_center(search)
                if archived:
                    # Switching tabs resets the results, so the search has to be
                    # re-run there with the column-scoped box.
                    result["archived"] = True
                    result["search_column"] = search_column
                    driver.show_archived(search, search_column)
                    result["invoice_view"] = driver._invoice_view()
            except SportsWebError as exc:
                result["error"] = _describe_failure(exc, driver, search)
                result["trace"] = driver.trace
                return result

        result["page"] = driver.describe()
        try:
            result["rows"] = driver.read_rows() if search else []
        except SportsWebError as exc:
            result["rows"] = []
            result["row_parse_error"] = str(exc)
        driver.save_page(html_path, screenshot_path)
        result["html_path"] = html_path
        result["screenshot_path"] = screenshot_path

        if probe_download and result["rows"]:
            driver.select_rows(result["rows"][:1])
            try:
                data, source_url, mechanism = driver.download_selected(download_format)
                result["download"] = {
                    "ok": True,
                    "format": download_format,
                    "mechanism": mechanism,
                    "url": source_url,
                    "bytes": len(data),
                    "looks_like_pdf": data[:5] == b"%PDF-",
                    "head": data[:80].decode("utf-8", "replace") if data[:5] != b"%PDF-" else None,
                }
                if save_download_to:
                    with open(save_download_to, "wb") as handle:
                        handle.write(data)
                    result["download"]["saved_to"] = save_download_to
            except SportsWebError as exc:
                result["download"] = {"ok": False, "format": download_format, "error": str(exc)}

        # The step trace is the point of the harness: it says how long each step
        # took and exactly where a stalled run stopped.
        result["trace"] = driver.trace

    return result


__all__ = (
    "DEFAULT_BASE_URL",
    "DOWNLOAD_FORMATS",
    "INVOICE_CENTER_PATH",
    "LOGIN_ENTRY_URL",
    "PORTAL_HOME_URL",
    "PUBLIC_SITE_URL",
    "looks_like_cloned_header",
    "ROW_COLUMNS",
    "SportsWebConfigError",
    "SportsWebDriver",
    "SportsWebError",
    "SportsWebTransportError",
    "capture_portal",
    "credentials",
    "fetch_invoice_pdf",
)
