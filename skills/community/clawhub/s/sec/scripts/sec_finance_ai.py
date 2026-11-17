"""
title: sec-finance-ai - AI-Powered SEC Filing Integration
description: Complete SEC Filing Data Suite - 23 tools for 10-K, 10-Q, 8-K, proxy statements, insider trading, and more. Real-time SEC filings, financial statements, company facts, ownership data. Works with OpenWebUI, OpenClaw, MCP clients (Claude, Cursor, VS Code, LangChain, Google ADK, Strands Agents), and any AI assistant with function calling.
author: lkcair
author_url: https://github.com/lkcair
funding_url: https://github.com/sponsors/lkcair
version: 2.0.4
license: MIT
requirements: pandas>=2.2.0,pydantic>=2.0.0,requests>=2.28.0,beautifulsoup4>=4.12.0,lxml>=4.9.0,python-dateutil>=2.8.0
repository: https://github.com/lkcair/sec-finance-ai

OPENWEBUI INSTALLATION:
1. Copy this entire file
2. Go to OpenWebUI > Workspace > Tools
3. Click "+" to create a new tool
4. Paste this code and click Save
5. Enable the tool on the model or in the chat
6. Start asking questions like "Get Apple's latest 10-K filing" or "Show Tesla's recent 8-K filings"

OTHER WAYS TO USE IT:
- MCP server (Claude, Cursor, VS Code, LangChain, Google ADK, Strands Agents): uvx sec-finance-ai@latest
- OpenClaw: openclaw skills install @lkcair/sec
- Python: from sec_finance_ai import Tools; tools = Tools()  (every tool is an async method)

FEATURES:
- 23 SEC tools over the official EDGAR APIs
- Any EDGAR form: 10-K, 10-Q, 8-K, 20-F, 6-K, DEF 14A, S-1, 424B4, 13D/13G, 3/4/5, 13F, N-PORT and more
- Read any filing in pages, search inside it, or get the link only (size checked before download, 25MB text limit)
- Full-text search across every EDGAR filing since 2001
- XBRL financial data: company facts, single concepts, and one metric across all companies
- Insider transactions (Form 4), 13D/13G holders, 13F institutional portfolios, recent IPOs
- Network access limited to https://*.sec.gov, streamed size caps, rate limiting
- Built-in self-test (28 checks)

CRITICAL: SEC USER-AGENT REQUIREMENT
The SEC requires all programmatic requests to include a User-Agent header that identifies
your company and provides a contact email. Failure to do so will result in a 403 Forbidden error.
Set the SEC_USER_AGENT environment variable (e.g., "MyCompany Name admin@example.com"),
or edit the "User-Agent" field of the `SEC_HEADERS` constant in this script.

EXAMPLE PROMPTS FOR AI:
- "Get Apple's latest 10-K filing"
- "Show me Tesla's recent 8-K filings"
- "What are the risk factors for Microsoft?"
- "Get insider trading activity for NVIDIA"
- "Show me Amazon's executive compensation"
- "Find recent 13F filings for Berkshire Hathaway"
- "Get the latest proxy statement for Google"
- "Show me recent SEC comment letters for Tesla"
- "What are the latest IPO filings?"
- "Get quarterly earnings filings for Apple"
- "Show me merger and acquisition filings"
- "Find beneficial ownership reports for GameStop"

TESTING:
AI can self-test by asking: "Run self-test on SEC tools"
This runs 28 checks across the 23 functions and reports results.
"""

from typing import Callable, Any, Optional, List, Dict, Union, Tuple
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timedelta, date
from dateutil import parser as dateutil_parser
from functools import wraps
import pandas as pd
import os
import requests
import logging
import re
import time
import inspect
import asyncio
import json
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import warnings

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
from urllib.parse import urljoin, quote, urlparse
import xml.etree.ElementTree as ET

# Direct SEC EDGAR API approach - no external library needed
# Using requests library to fetch .txt versions directly from SEC

# ============================================================
# CONFIGURATION & CONSTANTS
# ============================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SEC API Configuration
SEC_BASE_URL = "https://www.sec.gov"
SEC_API_BASE = "https://data.sec.gov"
SEC_EFTS_URL = "https://efts.sec.gov/LATEST/search-index"
SEC_EDGAR_BASE = "https://www.sec.gov/Archives/edgar/data"

# User agent required by SEC (must include company name and email)
# SEC blocks requests without proper User-Agent per their policy
# FORMAT: "Company Name email@address.com"
SEC_HEADERS = {
    "User-Agent": os.environ.get("SEC_USER_AGENT") or "SEC-AI-Research-Agent (admin@example.com)",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "*/*"
}

# Network safety limits (decoded bytes, so gzip bombs are capped too)
MAX_RESPONSE_BYTES = 50 * 1024 * 1024
MAX_FILING_BYTES = 25 * 1024 * 1024
TEXT_PAGE_CHARS = 50000
MAX_REDIRECTS = 5


class SecurityBlockedError(ValueError):
    """Raised when a request or redirect targets a host outside sec.gov"""


class ResponseTooLargeError(ValueError):
    """Raised when a response body exceeds the allowed byte limit"""

    def __init__(self, url: str, size: int, limit: int):
        super().__init__(f"Response from {url} exceeds {limit} bytes")
        self.url = url
        self.size = size
        self.limit = limit


def is_sec_url(url: str) -> bool:
    """True only for https URLs whose host is sec.gov or a subdomain of it"""
    try:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
    except ValueError:
        return False
    return parsed.scheme == "https" and (host == "sec.gov" or host.endswith(".sec.gov"))


class SecSession(requests.Session):
    """
    requests.Session restricted to sec.gov.

    Every request, and every redirect hop, is checked against is_sec_url before
    it is sent. Redirects are followed manually so an off-domain Location is
    never fetched. Bodies are streamed and capped at max_bytes regardless of
    the Content-Length the server reports.
    """

    def __init__(self):
        super().__init__()
        self.headers.update(SEC_HEADERS)
        self.max_redirects = MAX_REDIRECTS

    def request(self, method, url, max_bytes: int = MAX_RESPONSE_BYTES, **kwargs):
        kwargs.pop("allow_redirects", None)
        kwargs.pop("stream", None)
        for _ in range(MAX_REDIRECTS + 1):
            if not is_sec_url(url):
                raise SecurityBlockedError(f"Blocked non-SEC URL: {url}")
            response = super().request(method, url, allow_redirects=False, stream=True, **kwargs)
            if not response.is_redirect:
                self._read_capped(response, max_bytes)
                return response
            url = urljoin(response.url, response.headers["location"])
            response.close()
            if response.status_code == 303 or (response.status_code in (301, 302) and method.upper() == "POST"):
                method = "GET"
                kwargs.pop("data", None)
                kwargs.pop("json", None)
        raise requests.exceptions.TooManyRedirects(f"Exceeded {MAX_REDIRECTS} redirects")

    @staticmethod
    def _read_capped(response: requests.Response, max_bytes: int) -> None:
        declared = response.headers.get("content-length", "")
        if declared.isdigit() and int(declared) > max_bytes:
            response.close()
            raise ResponseTooLargeError(response.url, int(declared), max_bytes)
        body = bytearray()
        try:
            for chunk in response.iter_content(chunk_size=64 * 1024):
                body.extend(chunk)
                if len(body) > max_bytes:
                    raise ResponseTooLargeError(response.url, len(body), max_bytes)
        finally:
            response.close()
        response._content = bytes(body)
        response._content_consumed = True

# SEC Form Types
SEC_FORM_TYPES = {
    "10-K": "Annual Report",
    "20-F": "Annual Report (Foreign Issuer)",
    "10-Q": "Quarterly Report", 
    "8-K": "Current Report",
    "6-K": "Current Report (Foreign Issuer)",
    "DEF 14A": "Proxy Statement",
    "S-1": "Registration Statement",
    "S-3": "Registration Statement",
    "S-4": "Registration Statement",
    "10-K/A": "Annual Report Amendment",
    "20-F/A": "Annual Report Amendment (Foreign Issuer)",
    "10-Q/A": "Quarterly Report Amendment",
    "8-K/A": "Current Report Amendment",
    "6-K/A": "Current Report Amendment (Foreign Issuer)",
    "3": "Initial Statement of Beneficial Ownership",
    "3/A": "Initial Statement of Beneficial Ownership Amendment",
    "4": "Statement of Changes in Beneficial Ownership",
    "4/A": "Statement of Changes in Beneficial Ownership Amendment",
    "5": "Annual Statement of Changes in Beneficial Ownership",
    "5/A": "Annual Statement of Changes in Beneficial Ownership Amendment",
    "13D": "Schedule 13D",
    "13D/A": "Schedule 13D Amendment",
    "13G": "Schedule 13G",
    "13G/A": "Schedule 13G Amendment",
    "SC 13D": "Schedule 13D",
    "SC 13D/A": "Schedule 13D Amendment",
    "SC 13G": "Schedule 13G",
    "SC 13G/A": "Schedule 13G Amendment",
    "SCHEDULE 13D": "Schedule 13D",
    "SCHEDULE 13D/A": "Schedule 13D Amendment",
    "SCHEDULE 13G": "Schedule 13G",
    "SCHEDULE 13G/A": "Schedule 13G Amendment",
    "10-KT": "Annual Report (Transition Period)",
    "10-QT": "Quarterly Report (Transition Period)",
    "40-F": "Annual Report (Canadian Issuer)",
    "40-F/A": "Annual Report Amendment (Canadian Issuer)",
    "ARS": "Annual Report to Shareholders",
    "11-K": "Employee Benefit Plan Annual Report",
    "NT 10-K": "Notification of Late 10-K Filing",
    "NT 10-Q": "Notification of Late 10-Q Filing",
    "NT 20-F": "Notification of Late 20-F Filing",
    "DEF 14A/A": "Proxy Statement Amendment",
    "DEFA14A": "Additional Proxy Soliciting Materials",
    "DEFM14A": "Merger Proxy Statement",
    "PRE 14A": "Preliminary Proxy Statement",
    "DEF 14C": "Information Statement",
    "PRE 14C": "Preliminary Information Statement",
    "S-1/A": "Registration Statement Amendment",
    "S-3/A": "Registration Statement Amendment",
    "S-4/A": "Registration Statement Amendment",
    "S-8": "Employee Benefit Plan Registration",
    "S-11": "Real Estate Registration Statement",
    "F-1": "Registration Statement (Foreign Issuer)",
    "F-1/A": "Registration Statement Amendment (Foreign Issuer)",
    "F-3": "Registration Statement (Foreign Issuer)",
    "F-4": "Business Combination Registration (Foreign Issuer)",
    "DRS": "Draft Registration Statement",
    "424B1": "Prospectus",
    "424B2": "Prospectus",
    "424B3": "Prospectus",
    "424B4": "Final Prospectus (priced offering, typical for IPOs)",
    "424B5": "Prospectus Supplement",
    "425": "Business Combination Communication",
    "10-12B": "Registration of Securities (Exchange Listing)",
    "10-12G": "Registration of Securities",
    "8-A12B": "Registration of Securities on an Exchange",
    "15-12G": "Termination of Registration",
    "15-12B": "Termination of Registration",
    "25-NSE": "Notification of Removal from Listing",
    "SC TO-T": "Third-Party Tender Offer",
    "SC TO-I": "Issuer Tender Offer",
    "SC 14D9": "Tender Offer Solicitation/Recommendation",
    "SD": "Specialized Disclosure (Conflict Minerals)",
    "144": "Notice of Proposed Sale of Securities",
    "D": "Notice of Exempt Offering (Form D)",
    "D/A": "Notice of Exempt Offering Amendment",
    "1-A": "Regulation A Offering Statement",
    "C": "Regulation Crowdfunding Offering",
    "N-CSR": "Fund Annual/Semi-Annual Shareholder Report",
    "N-CEN": "Fund Annual Report",
    "NPORT-P": "Monthly Portfolio Investments Report",
    "485BPOS": "Fund Prospectus Post-Effective Amendment",
    "497": "Fund Prospectus",
    "13F-HR": "Institutional Investment Manager Holdings Report",
    "13F-HR/A": "Institutional Investment Manager Holdings Report Amendment",
    "13F-NT": "Institutional Investment Manager Notice",
    "N-PORT": "Monthly Portfolio Investments Report",
    "N-Q": "Quarterly Schedule of Portfolio Holdings",
    "ADV": "Investment Adviser Registration",
    "PF": "Private Fund Report"
}

# Filing frequency mappings
FILING_FREQUENCIES = {
    "annual": ["10-K", "20-F", "DEF 14A"],
    "quarterly": ["10-Q"],
    "current": ["8-K", "6-K"],
    "insider": ["3", "4", "5"],
    "ownership": ["13D", "13G", "SC 13D", "SC 13G"],
    "institutional": ["13F-HR"],
    "fund": ["N-PORT", "N-Q"],
    "registration": ["S-1", "S-3", "S-4"]
}

# API rate limiting (SEC allows 10 requests per second)
RATE_LIMIT_CALLS = 10
RATE_LIMIT_WINDOW = 1  # seconds

# Common CIK mappings for major companies (100+ most traded stocks)
COMMON_CIKS = {
    # MEGA CAP TECH
    "AAPL": "0000320193",
    "MSFT": "0000789019",
    "GOOGL": "0001652044",
    "GOOG": "0001652044",
    "AMZN": "0001018724",
    "TSLA": "0001318605",
    "META": "0001326801",
    "FB": "0001326801",
    "NVDA": "0001045810",

    # BERKSHIRE
    "BRK.A": "0001067983",
    "BRK.B": "0001067983",

    # FINANCIALS
    "JPM": "0000019617",
    "BAC": "0000070858",
    "WFC": "0000072971",
    "GS": "0000886982",
    "MS": "0000895421",
    "C": "0000831001",
    "AXP": "0000004962",
    "BLK": "0002012383",
    "SCHW": "0000316709",

    # HEALTH CARE
    "JNJ": "0000200406",
    "UNH": "0000731766",
    "PFE": "0000078003",
    "ABBV": "0001551152",
    "LLY": "0000059478",
    "MRK": "0000310158",
    "AMGN": "0000318154",
    "GILD": "0000882095",
    "BIIB": "0000875045",
    "TMO": "0000097745",
    "ABT": "0000001800",
    "CI": "0001739940",
    "AEP": "0000004904",

    # CONSUMER & RETAIL
    "WMT": "0000104169",
    "PG": "0000080424",
    "KO": "0000021344",
    "PEP": "0000077476",
    "MCD": "0000063908",
    "LOW": "0000060667",
    "HD": "0000354950",
    "DIS": "0001744489",
    "NKE": "0000320187",
    "CVS": "0000064803",
    "WBA": "0001618921",

    # INDUSTRIALS & ENERGY
    "XOM": "0000034088",
    "CVX": "0000093410",
    "COP": "0001163165",
    "MPC": "0001510295",
    "VLO": "0001035002",
    "PSX": "0001534701",
    "MMM": "0000066740",
    "BA": "0000012927",
    "GE": "0000040545",
    "LMT": "0000936468",
    "RTX": "0000101829",
    "NOC": "0001133421",
    "CAT": "0000018230",

    # FINANCIALS & PAYMENT
    "V": "0001403161",
    "MA": "0001141391",
    "PYPL": "0001633917",
    "SQ": "0001512673",
    "COIN": "0001679788",
    "AMP": "0000820027",

    # SEMICONDUCTORS
    "AMD": "0000002488",
    "INTC": "0000050863",
    "QCOM": "0000804328",
    "AVGO": "0001730168",
    "MU": "0000723125",
    "LRCX": "0000707549",
    "ASML": "0000937966",
    "MRVL": "0001835632",

    # SOFTWARE & SERVICES
    "ADBE": "0000796343",
    "CRM": "0001108524",
    "NFLX": "0001065280",
    "ORCL": "0001341439",
    "IBM": "0000051143",
    "INTU": "0000896878",
    "NOW": "0001373715",
    "DDOG": "0001561550",
    "SNOW": "0001640147",
    "CRWD": "0001535527",
    "OKTA": "0001660134",

    # COMMUNICATIONS
    "VZ": "0000732712",
    "T": "0000732717",
    "CMCSA": "0001166691",
    "CHTR": "0001091667",
    "TMUS": "0001283699",

    # UTILITIES
    "NEE": "0000753308",
    "DUK": "0001326160",
    "SO": "0000092122",
    "EXC": "0001109357",
    "RUN": "0001469367",

    # RETAIL & GAMING
    "GME": "0001326380",  # GameStop - The key fix!
    "AMC": "0001411579",
    "BBBY": "0001130713",

    # OTHER MAJOR
    "TSM": "0001046179",
    "PLTR": "0001321655",
    "NVO": "0000353278",
    "AZN": "0000901832",
    "NVS": "0001114448",
    "HSBC": "0001089113",
    "SAP": "0001000184",
    "BABA": "0001577552",
    "SONY": "0000313838",
    "PDD": "0001737806",
    "ARM": "0001973239",
    "UBER": "0001543151",
    "DE": "0000315189",
    "SCCO": "0001001838",
    "FCX": "0000831259",
    "RIO": "0000863064",

    # ETFs & FUNDS (where CIK exists)
    "SPY": "0001555280",
    "QQQ": "0001092865",
    "IWM": "0001074632",
}

# ============================================================
# VALIDATION MODELS
# ============================================================

class CIKValidator(BaseModel):
    """Validate CIK (Central Index Key) input"""
    cik: str = Field(..., min_length=1, max_length=10)

    @field_validator('cik')

    @classmethod
    def validate_cik(cls, v):
        # Remove any non-numeric characters and pad with zeros
        cik_clean = re.sub(r'[^0-9]', '', str(v))
        if not cik_clean:
            raise ValueError(f"Invalid CIK format: {v}")
        return cik_clean.zfill(10)  # SEC CIKs are 10 digits with leading zeros


class TickerToCIKValidator(BaseModel):
    """Validate ticker symbol and convert to CIK"""
    ticker: str = Field(..., min_length=1, max_length=10)

    @field_validator('ticker')

    @classmethod
    def validate_ticker(cls, v):
        ticker_upper = str(v).upper().strip()
        if not re.match(r'^[A-Z0-9.\-]+$', ticker_upper):
            raise ValueError(f"Invalid ticker symbol format: {v}")
        return ticker_upper


class FormTypeValidator(BaseModel):
    """Validate SEC form type"""
    form_type: Union[str, List[str]] = Field(...)

    @field_validator('form_type')

    @classmethod
    def validate_form_type(cls, v):
        items = v if isinstance(v, list) else [v]
        validated_list = []
        for item in items:
            form_upper = re.sub(r'\s+', ' ', str(item).upper().strip())
            if not FORM_PATTERN.match(form_upper):
                raise ValueError(f"Invalid form type: {item}. Examples: {', '.join(list(SEC_FORM_TYPES)[:12])}")
            if form_upper not in SEC_FORM_TYPES:
                logger.info(f"Form type {form_upper} is not in the known list; matching it exactly")
            validated_list.append(form_upper)
        return validated_list if isinstance(v, list) else validated_list[0]


FORM_PATTERN = re.compile(r'^[A-Z0-9][A-Z0-9 ./\-]{0,24}$')


def form_list(form_type: Optional[Union[str, List[str]]]) -> List[str]:
    """Normalize a form type argument (string, comma-separated string or list) to a list"""
    if not form_type:
        return []
    if isinstance(form_type, str):
        form_type = [f for f in form_type.split(",") if f.strip()]
    validated = FormTypeValidator(form_type=list(form_type)).form_type
    return validated


class DateRangeValidator(BaseModel):
    """Validate date range parameters"""
    start_date: Optional[str] = Field(default=None)
    end_date: Optional[str] = Field(default=None)

    @field_validator('start_date', 'end_date')

    @classmethod
    def validate_dates(cls, v):
        if v is None:
            return v
        try:
            # Try to parse the date
            parsed_date = dateutil_parser.parse(v)
            return parsed_date.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            raise ValueError(f"Invalid date format: {v}. Use YYYY-MM-DD format.")


# ============================================================
# UTILITY DECORATORS & HELPERS
# ============================================================

def retry_with_backoff(max_retries: int = 3, base_wait: float = 1.0, max_wait: float = 10.0):
    """
    Decorator for retrying functions with exponential backoff.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except (requests.exceptions.RequestException,
                        requests.exceptions.Timeout,
                        ConnectionError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = min(base_wait * (2 ** attempt), max_wait)
                        logger.warning(f"Retry {attempt + 1}/{max_retries} for {func.__name__} after {wait_time}s: {e}")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"Failed after {max_retries} attempts: {func.__name__}")
                except Exception as e:
                    # Don't retry on non-network errors
                    raise
            raise last_exception
        return wrapper
    return decorator


def rate_limit():
    """Simple rate limiting decorator for SEC API compliance"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Simple rate limiting - wait 0.1 seconds between calls
            await asyncio.sleep(0.1)
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def safe_sec_call(func):
    """Decorator for safe SEC API calls with error handling"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.warning("Rate limit exceeded, waiting...")
                await asyncio.sleep(1)
                return await func(self, *args, **kwargs)
            else:
                logger.error(f"HTTP error in {func.__name__}: {e}")
                return {"error": f"HTTP error: {e.response.status_code}"}
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            return {"error": str(e)}
    return wrapper


# Cache for dynamic CIK lookups to avoid repeated API calls
_cik_cache = {}


def ticker_to_cik(ticker: str) -> Optional[str]:
    """
    Convert ticker symbol to CIK using three-tier fallback approach:
    1. Check hardcoded COMMON_CIKS dictionary (100+ major stocks)
    2. Try SEC company_tickers.json API endpoint
    3. Return None if all methods exhausted

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'GME')

    Returns:
        CIK as 10-digit zero-padded string, or None if not found
    """
    ticker_upper = str(ticker).upper().strip().replace(".", "-").replace("/", "-")
    logger.debug(f"Attempting to resolve CIK for ticker: {ticker_upper}")

    # A numeric value is already a CIK (funds, 13F managers, private issuers)
    if ticker_upper.isdigit() and len(ticker_upper) <= 10:
        return ticker_upper.zfill(10)

    # Tier 1: Check cache first
    if ticker_upper in _cik_cache:
        logger.debug(f"CIK for {ticker_upper} found in cache: {_cik_cache[ticker_upper]}")
        return _cik_cache[ticker_upper]

    # Tier 2: Check hardcoded mappings (100+ stocks)
    if ticker_upper in COMMON_CIKS:
        cik = COMMON_CIKS[ticker_upper]
        logger.info(f"✓ CIK found in hardcoded mapping: {ticker_upper} → {cik}")
        _cik_cache[ticker_upper] = cik
        return cik

    logger.debug(f"  {ticker_upper} not in hardcoded list, trying SEC API...")

    # Tier 3: Try SEC company_tickers.json endpoint (dynamic lookup)
    try:
        logger.debug(f"  Fetching SEC company_tickers.json...")
        with SecSession() as session:
            response = session.get(f"{SEC_BASE_URL}/files/company_tickers.json", timeout=10)

        if response.status_code == 200:
            tickers_data = response.json()
            logger.debug(f"  Received {len(tickers_data)} companies from SEC API")

            for company_data in tickers_data.values():
                if company_data.get('ticker', '').upper() == ticker_upper:
                    cik = str(company_data.get('cik_str', '')).zfill(10)
                    logger.info(f"✓ CIK found via SEC API: {ticker_upper} → {cik}")
                    _cik_cache[ticker_upper] = cik
                    return cik

            logger.warning(f"⚠ Ticker not found in SEC company_tickers: {ticker_upper}")
        else:
            logger.error(f"⚠ SEC API returned status {response.status_code} for company_tickers")

    except requests.exceptions.Timeout:
        logger.error(f"⚠ Timeout fetching SEC company_tickers for {ticker_upper}")
    except requests.exceptions.RequestException as e:
        logger.error(f"⚠ Network error fetching SEC company_tickers: {e}")
    except (json.JSONDecodeError, ValueError, KeyError) as e:
        logger.error(f"⚠ Error parsing SEC API response: {e}")
    except Exception as e:
        logger.error(f"⚠ Unexpected error during CIK lookup: {e}")

    logger.error(f"✗ Could not find CIK for ticker: {ticker_upper}")
    return None


def format_filing_date(date_str: str) -> str:
    """Format filing date for display"""
    try:
        dt = dateutil_parser.parse(date_str)
        return dt.strftime('%Y-%m-%d')
    except:
        return date_str


def preview_with_guide(html_content: str, filing_url: str, preview_chars: int) -> Dict[str, Any]:
    """First preview_chars of a filing plus how to read the rest (download_filing_text)"""
    full = extract_text_from_html(html_content, max_length=len(html_content) + 1)
    total = len(full)
    partial = total > preview_chars
    out = {
        "content_preview": full[:preview_chars],
        "preview_characters": min(preview_chars, total),
        "total_characters": total,
        "preview_is_partial": partial,
    }
    if partial:
        out["read_more"] = (
            f"The preview is only the first {preview_chars:,} of {total:,} characters (cover page and the first "
            f"statements). It is NOT the whole filing. To read more, call download_filing_text("
            f"filing_url='{filing_url}', offset={preview_chars}) and keep going with next_offset; or jump to a "
            f"section with download_filing_text(filing_url=..., search='<phrase>'), e.g. search='medical care ratio', "
            f"'Results of Operations', 'Item 7', 'Risk Factors'. Use max_length to fit your context window. Prefer "
            f"figures the company reports in the text over figures you compute yourself."
        )
    return out


def extract_text_from_html(html_content: str, max_length: int = 1000000) -> str:
    """Extract clean text from HTML content"""
    try:
        try:
            soup = BeautifulSoup(html_content, 'lxml')
        except Exception:
            soup = BeautifulSoup(html_content, 'html.parser')
        # Remove script/style and hidden inline-XBRL blocks (ix:header, display:none)
        for script in soup(["script", "style", "ix:header"]):
            script.decompose()
        for hidden in soup.select('[style*="display:none"], [style*="display: none"]'):
            hidden.decompose()
        text = soup.get_text(separator=" ")
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        return text[:max_length] if len(text) > max_length else text
    except:
        return html_content[:max_length] if len(html_content) > max_length else html_content


# ============================================================
# MAIN SEC-AI TOOLS CLASS
# ============================================================

class Tools:
    """
    SEC-AI Tools - Comprehensive SEC Filing Access Suite

    This class provides 23 tools for accessing SEC filings, company data,
    insider trading information, and more through the SEC's EDGAR database.
    """

    def __init__(self):
        """Initialize SEC-AI Tools"""
        self.session = SecSession()
        logger.info("SEC-AI Tools initialized")

    # ============================================================
    # CORE SEC FILING TOOLS
    # ============================================================

    @safe_sec_call
    @rate_limit()
    async def download_filing_text(
        self,
        filing_url: str,
        max_length: int = TEXT_PAGE_CHARS,
        offset: int = 0,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Read or search the text of one SEC filing document. Three modes, chosen automatically:

        - mode 'text': returns `content` in pages of max_length characters. If has_more is
          true, call again with offset=next_offset to keep reading.
        - mode 'search': when `search` is given, returns snippets around each match with its
          position (use offset=position to read that part).
        - mode 'link_only': when the document is larger than the size limit, returns only the
          link and size so the user can open it. The exact size is checked BEFORE downloading.

        Args:
            filing_url: Filing document URL (https://www.sec.gov/Archives/edgar/data/...)
            max_length: Characters per page (default 50,000)
            offset: Character position to start reading from (default 0)
            search: Optional word or phrase to find inside the filing (case-insensitive)

        Returns:
            Dictionary with mode, filing_url, size_mb, total_characters and content/snippets
        """
        logger.info(f"=== download_filing_text({filing_url}) ===")

        # Security: Restrict to official SEC domains to prevent SSRF.
        # SecSession re-checks every redirect hop and caps the streamed body.
        if not is_sec_url(filing_url):
            logger.error(f"Security blocked: Attempted access to non-SEC URL: {filing_url}")
            return {
                "error": "Security violation: Only official SEC EDGAR URLs (https://*.sec.gov) are allowed.",
                "filing_url": filing_url
            }
        try:
            return self._read_filing(filing_url, max_length=max_length, offset=offset, search=search)
        except Exception as e:
            logger.error(f"Error downloading filing: {e}")
            return {"error": str(e), "filing_url": filing_url}

    def _link_only(self, filing_url: str, size_bytes: int, exact: bool = True) -> Dict[str, Any]:
        """Build the link-only answer for a document over the size limit"""
        size_mb = round(size_bytes / (1024 * 1024), 2)
        size_text = f"{size_mb}MB" if exact else f"more than {MAX_FILING_BYTES // (1024 * 1024)}MB"
        return {
            "mode": "link_only",
            "filing_url": filing_url,
            "size_mb": size_mb if exact else None,
            "ai_note": (
                f"This document is {size_text}, above the {MAX_FILING_BYTES // (1024 * 1024)}MB text limit. "
                f"Give the user this link to open it: {filing_url}. For numbers use get_filing_content "
                f"or get_company_concept; for smaller parts use get_filing_documents to list exhibits."
            )
        }

    def _read_filing(
        self,
        filing_url: str,
        max_length: int = TEXT_PAGE_CHARS,
        offset: int = 0,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Size-check, download and return one page of text, search snippets, or a link"""
        size = self._document_size(filing_url)
        if size and size > MAX_FILING_BYTES:
            return self._link_only(filing_url, size)
        try:
            response = self.session.get(filing_url, timeout=60, max_bytes=MAX_FILING_BYTES)
        except ResponseTooLargeError as e:
            return self._link_only(filing_url, e.size, exact=e.size == size)
        response.raise_for_status()

        text = extract_text_from_html(response.text, max_length=len(response.text) + 1)
        total = len(text)
        base = {
            "filing_url": filing_url,
            "size_mb": round((size or len(response.content)) / (1024 * 1024), 2),
            "total_characters": total,
        }

        if search:
            needle = str(search).lower()
            haystack = text.lower()
            positions, start = [], haystack.find(needle)
            while start != -1:
                positions.append(start)
                start = haystack.find(needle, start + len(needle))
            snippets = [{"position": pos, "text": text[max(0, pos - 400):pos + len(needle) + 400]}
                        for pos in positions[:20]]
            return {
                **base,
                "mode": "search",
                "search": search,
                "total_matches": len(positions),
                "snippets": snippets,
                "ai_note": "To read around a match, call download_filing_text with offset=<position minus a few thousand>."
            }

        offset = max(0, int(offset or 0))
        max_length = max(1000, min(int(max_length or TEXT_PAGE_CHARS), 500000))
        chunk = text[offset:offset + max_length]
        has_more = offset + len(chunk) < total
        return {
            **base,
            "mode": "text",
            "offset": offset,
            "content_length": len(chunk),
            "content": chunk,
            "has_more": has_more,
            "next_offset": offset + len(chunk) if has_more else None,
            "ai_note": (f"Showing characters {offset}-{offset + len(chunk)} of {total}. "
                        + ("Call again with offset=next_offset for more, or use search='keyword' to jump to a topic."
                           if has_more else "This is the end of the document."))
        }

    @safe_sec_call
    @rate_limit()
    async def get_company_filings(
        self,
        ticker: str,
        form_type: Optional[Union[str, List[str]]] = None,
        limit: int = 10,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get SEC filings for a company by ticker symbol.

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL', 'TSLA')
            form_type: SEC form type (e.g., '10-K', '10-Q', '8-K'). 
                       Can be a single string or a list of strings.
                       If None, returns all forms.
            limit: Maximum number of filings to return (default: 10)
            start_date: Start date for filing search (YYYY-MM-DD format)
            end_date: End date for filing search (YYYY-MM-DD format)

        Returns:
            Dictionary containing filing information
        """
        logger.info(f"=== get_company_filings(ticker={ticker}, form_type={form_type}, limit={limit}) ===")
        # Validate inputs
        ticker_validator = TickerToCIKValidator(ticker=ticker)
        validated_ticker = ticker_validator.ticker
        
        if isinstance(form_type, str) and "," in form_type:
            form_type = [f for f in form_type.split(",") if f.strip()]
        if form_type:
            form_validator = FormTypeValidator(form_type=form_type)
            validated_form = form_validator.form_type
        else:
            validated_form = None
            
        if start_date or end_date:
            date_validator = DateRangeValidator(start_date=start_date, end_date=end_date)
            validated_start = date_validator.start_date
            validated_end = date_validator.end_date
        else:
            validated_start = validated_end = None

        # Convert ticker to CIK
        cik = ticker_to_cik(validated_ticker)
        if not cik:
            logger.error(f"CIK lookup failed for ticker: {validated_ticker}")
            return {
                "error": "CIK lookup failed",
                "ticker": validated_ticker,
                "message": f"Could not find CIK for ticker '{validated_ticker}'",
                "suggestion": f"Verify '{validated_ticker}' is a valid US stock ticker symbol",
                "note": "Any company registered in EDGAR resolves by ticker or by CIK. Check the symbol, or pass the numeric CIK."
            }

        try:
            # Get company submissions
            url = f"{SEC_API_BASE}/submissions/CIK{cik}.json"
            logger.debug(f"Fetching filings from SEC: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()
            company_name = data.get('name', 'Unknown')
            logger.info(f"✓ Retrieved filings for {company_name} ({validated_ticker})")
            filings = data.get('filings', {}).get('recent', {})
            
            if not filings:
                return {"error": "No filings found"}

            # "recent" holds the latest ~1000 filings; older ones are in extra pages
            def filing_rows():
                pages = [filings]
                older = data.get('filings', {}).get('files', [])
                page_index = 0
                while page_index < len(pages):
                    page = pages[page_index]
                    page_index += 1
                    for i in range(min(len(page.get('form', [])), len(page.get('filingDate', [])), len(page.get('accessionNumber', [])))):
                        docs = page.get('primaryDocument', [])
                        yield page['form'][i], page['filingDate'][i], page['accessionNumber'][i], docs[i] if i < len(docs) else ""
                    if older and (validated_form or validated_start):
                        if validated_start and page.get('filingDate') and min(page['filingDate']) < validated_start:
                            continue
                        name = older.pop(0)['name']
                        older_resp = self.session.get(f"{SEC_API_BASE}/submissions/{name}", timeout=30)
                        older_resp.raise_for_status()
                        pages.append(older_resp.json())

            # Process filings
            filing_list = []
            
            for form, filing_date, accession, primary_doc in filing_rows():
                
                # Filter by form type if specified
                if validated_form:
                    if isinstance(validated_form, list):
                        if form not in validated_form:
                            continue
                    elif form != validated_form:
                        continue
                    
                # Filter by date range if specified
                if validated_start and filing_date < validated_start:
                    continue
                if validated_end and filing_date > validated_end:
                    continue
                
                # Build filing URL
                accession_clean = accession.replace('-', '')
                cik_no_zeros = cik.lstrip('0')
                filing_url = f"{SEC_EDGAR_BASE}/{cik_no_zeros}/{accession_clean}/{primary_doc}"
                
                filing_info = {
                    "form": form,
                    "filing_date": format_filing_date(filing_date),
                    "accession_number": accession,
                    "primary_document": primary_doc,
                    "filing_url": filing_url,
                    "description": SEC_FORM_TYPES.get(form, "Unknown Form Type")
                }
                
                filing_list.append(filing_info)
                
                if len(filing_list) >= limit:
                    break

            return {
                "ticker": validated_ticker,
                "cik": cik,
                "company_name": data.get('name', 'Unknown'),
                "total_filings": len(filing_list),
                "filings": filing_list
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch filings: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    @safe_sec_call
    @rate_limit()
    async def get_latest_10k(self, ticker: str) -> Dict[str, Any]:
        """
        Get the latest 10-K filing for a company: filing link plus a SHORT preview of its text.

        The preview is only the first 10,000 characters (cover page and first statements). When
        preview_is_partial is true, follow read_more: download_filing_text(filing_url, offset=...) pages
        through the rest, download_filing_text(filing_url, search='...') jumps to a section.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with the 10-K filing: filing_url, content_preview, preview_characters,
            total_characters, preview_is_partial and read_more
        """
        logger.info(f"=== get_latest_10k({ticker}) ===")
        result = await self.get_company_filings(ticker, form_type="10-K", limit=1)

        if "error" in result or not result.get("filings"):
            return result

        latest_10k = result["filings"][0]

        # Extract content
        try:
            response = self.session.get(latest_10k["filing_url"], timeout=30, max_bytes=MAX_FILING_BYTES)
            if response.status_code == 200:
                latest_10k.update(preview_with_guide(response.text, latest_10k["filing_url"], 10000))
                logger.info(f"✓ Retrieved 10-K content")
        except ResponseTooLargeError as e:
            latest_10k.update(self._link_only(latest_10k["filing_url"], e.size, exact=False))
        except Exception as e:
            logger.debug(f"Could not extract content: {e}")

        return {
            "ticker": result["ticker"],
            "company_name": result["company_name"],
            "latest_10k": latest_10k
        }

    @safe_sec_call
    @rate_limit()
    async def get_latest_10q(self, ticker: str) -> Dict[str, Any]:
        """
        Get the latest 10-Q filing for a company: filing link plus a SHORT preview of its text.

        The preview is only the first 10,000 characters (cover page and first statements). When
        preview_is_partial is true, follow read_more: download_filing_text(filing_url, offset=...) pages
        through the rest, download_filing_text(filing_url, search='...') jumps to a section.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary with the 10-Q filing: filing_url, content_preview, preview_characters,
            total_characters, preview_is_partial and read_more
        """
        logger.info(f"=== get_latest_10q({ticker}) ===")
        result = await self.get_company_filings(ticker, form_type="10-Q", limit=1)

        if "error" in result or not result.get("filings"):
            return result

        latest_10q = result["filings"][0]

        # Extract content
        try:
            response = self.session.get(latest_10q["filing_url"], timeout=30, max_bytes=MAX_FILING_BYTES)
            if response.status_code == 200:
                latest_10q.update(preview_with_guide(response.text, latest_10q["filing_url"], 10000))
                logger.info(f"✓ Retrieved 10-Q content")
        except ResponseTooLargeError as e:
            latest_10q.update(self._link_only(latest_10q["filing_url"], e.size, exact=False))
        except Exception as e:
            logger.debug(f"Could not extract content: {e}")

        return {
            "ticker": result["ticker"],
            "company_name": result["company_name"],
            "latest_10q": latest_10q
        }

    @safe_sec_call
    @rate_limit()
    async def get_recent_8k_filings(self, ticker: str, limit: int = 5) -> Dict[str, Any]:
        """
        Get recent 8-K filings for a company with a SHORT preview of each.

        Each preview is only the first 5,000 characters. When preview_is_partial is true, follow
        read_more: download_filing_text(filing_url, offset=...) or download_filing_text(filing_url, search='...').

        Args:
            ticker: Stock ticker symbol
            limit: Number of recent 8-K filings to return

        Returns:
            Dictionary with 8-K filings: filing_url, content_preview, preview_characters,
            total_characters, preview_is_partial, read_more and extracted items
        """
        logger.info(f"=== get_recent_8k_filings({ticker}, limit={limit}) ===")
        result = await self.get_company_filings(ticker, form_type="8-K", limit=limit)

        if "error" in result or "filings" not in result:
            return result

        # Extract content from each 8-K filing
        enhanced_filings = []
        for filing in result.get("filings", []):
            enhanced_filing = filing.copy()

            try:
                filing_url = filing["filing_url"]
                logger.debug(f"Fetching 8-K content from: {filing_url}")
                response = self.session.get(filing_url, timeout=30, max_bytes=MAX_FILING_BYTES)
                if response.status_code == 200:
                    # Extract text content from HTML
                    enhanced_filing.update(preview_with_guide(response.text, filing_url, 5000))
                    content = enhanced_filing["content_preview"]

                    # Try to extract key event items (Item 1-9 of 8-K)
                    try:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        # Look for Item headers in 8-K
                        item_text = soup.get_text()
                        if "Item" in item_text:
                            enhanced_filing["has_event_details"] = True
                    except:
                        pass

                    logger.info(f"✓ Extracted content for {filing['filing_date']}")
            except ResponseTooLargeError as e:
                enhanced_filing.update(self._link_only(filing["filing_url"], e.size, exact=False))
            except Exception as e:
                logger.debug(f"Could not extract 8-K content: {e}")

            enhanced_filings.append(enhanced_filing)

        result["filings"] = enhanced_filings
        return result

    def _extract_8k_summary(self, text: str) -> Dict[str, Any]:
        """Extract key information from 8-K plain text."""
        lines = text.split('\n')
        summary = {
            "events": [],
            "key_text": ""
        }

        # Look for Item entries (simplified)
        in_content = False
        content_lines = []

        for i, line in enumerate(lines):
            line = line.strip()

            # Detect important items
            if line.startswith("Item 2."):
                summary["events"].append("Material change or acquisition")
            elif line.startswith("Item 3."):
                summary["events"].append("Corporate governance change")
            elif line.startswith("Item 5."):
                summary["events"].append("Executive or director change")
            elif line.startswith("Item 8."):
                summary["events"].append("Regulatory/other event")
            elif line and not line.startswith("Item") and len(line) > 20:
                content_lines.append(line)

        # Get summary text (first meaningful paragraph)
        if content_lines:
            summary["key_text"] = " ".join(content_lines[:5])[:500]

        return summary

    @safe_sec_call
    @rate_limit()
    async def analyze_8k_filing(self, ticker: str) -> Dict[str, Any]:
        """
        Get and summarize the latest 8-K filing for a company.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Dictionary containing 8-K summary with actual content
        """
        logger.info(f"=== analyze_8k_filing({ticker}) ===")

        # Get latest 8-K
        filings_result = await self.get_company_filings(ticker, form_type="8-K", limit=1)

        if "error" in filings_result or not filings_result.get("filings"):
            return {"error": "Could not find 8-K filings"}

        filing = filings_result["filings"][0]

        try:
            # Get filing content
            filing_url = filing["filing_url"]
            logger.info(f"Fetching 8-K: {filing_url}")
            try:
                response = self.session.get(filing_url, timeout=30, max_bytes=MAX_FILING_BYTES)
            except ResponseTooLargeError as e:
                return {"ticker": ticker, "filing_date": filing.get("filing_date"),
                        **self._link_only(filing_url, e.size, exact=False)}

            if response.status_code != 200:
                return {"error": f"Could not access filing: HTTP {response.status_code}"}

            # Extract text (first 5,000 characters, with how to read the rest)
            preview = preview_with_guide(response.text, filing_url, 5000)
            content = preview["content_preview"]
            summary = self._extract_8k_summary(content)

            logger.info(f"✓ 8-K analyzed for {filing['filing_date']}")

            return {
                "ticker": ticker,
                "company_name": filings_result.get("company_name"),
                "filing_date": filing["filing_date"],
                "filing_url": filing["filing_url"],
                "accession": filing["accession_number"],
                "events": summary["events"],
                "summary": summary["key_text"],
                **preview
            }

        except Exception as e:
            logger.error(f"Error analyzing 8-K: {e}")
            return {
                "error": f"Failed to analyze: {str(e)}",
                "filing_date": filing.get("filing_date"),
                "filing_url": filing.get("filing_url")
            }

    @safe_sec_call
    @rate_limit()
    async def get_proxy_statements(self, ticker: str, limit: int = 3) -> Dict[str, Any]:
        """
        Get proxy statements (DEF 14A) for a company.
        
        Args:
            ticker: Stock ticker symbol
            limit: Number of proxy statements to return
            
        Returns:
            Dictionary containing proxy statement information
        """
        return await self.get_company_filings(ticker, form_type="DEF 14A", limit=limit)

    # ============================================================
    # INSIDER TRADING & OWNERSHIP TOOLS
    # ============================================================

    @safe_sec_call
    @rate_limit()
    async def get_insider_transactions(self, ticker: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get insider trading transactions (Forms 3, 4, 5) for a company.
        
        Args:
            ticker: Stock ticker symbol
            limit: Number of transactions to return
            
        Returns:
            Dictionary containing insider transaction information
        """
        # Get Forms 4 (most common insider trading form)
        result = await self.get_company_filings(ticker, form_type="4", limit=limit)
        
        if "error" in result:
            return result
            
        # Enhance with transaction details where possible
        enhanced_filings = []
        for filing in result.get("filings", []):
            enhanced_filing = filing.copy()
            
            # Try to extract transaction details from the filing
            try:
                filing_url = filing["filing_url"]
                response = self.session.get(filing_url, timeout=15)
                if response.status_code == 200:
                    # Parse XML content for transaction details
                    soup = BeautifulSoup(response.text, 'xml')
                    
                    # Extract key information
                    owner_name = soup.find('rptOwnerName')
                    if owner_name:
                        enhanced_filing["owner_name"] = owner_name.get_text(strip=True)
                    
                    # Look for transaction information
                    transactions = soup.find_all('nonDerivativeTransaction')
                    if transactions:
                        transaction_info = []
                        for trans in transactions[:3]:  # Limit to first 3 transactions
                            trans_data = {}
                            
                            # Transaction date
                            trans_date = trans.find('transactionDate')
                            if trans_date:
                                trans_data["transaction_date"] = trans_date.find('value').get_text(strip=True)
                            
                            # Transaction code (P=Purchase, S=Sale, etc.)
                            trans_code = trans.find('transactionCode')
                            if trans_code:
                                trans_data["transaction_code"] = trans_code.get_text(strip=True)
                            
                            # Shares
                            shares = trans.find('transactionShares')
                            if shares:
                                trans_data["shares"] = shares.find('value').get_text(strip=True)
                            
                            # Price
                            price = trans.find('transactionPricePerShare')
                            if price:
                                trans_data["price_per_share"] = price.find('value').get_text(strip=True)
                            
                            transaction_info.append(trans_data)
                        
                        enhanced_filing["transactions"] = transaction_info
                        
            except Exception as e:
                logger.warning(f"Could not parse insider transaction details: {e}")
            
            enhanced_filings.append(enhanced_filing)
        
        result["filings"] = enhanced_filings
        return result

    @safe_sec_call
    @rate_limit()
    async def get_beneficial_ownership(self, ticker: str, limit: int = 10, schedule: str = "all") -> Dict[str, Any]:
        """
        Get beneficial ownership reports (13D, 13G) for a company.

        Args:
            ticker: Stock ticker symbol
            limit: Number of reports to return
            schedule: 'all' (default), '13D' (activist or control intent) or '13G' (passive holder)
            
        Returns:
            Dictionary containing beneficial ownership information
        """
        # Get both 13D and 13G filings (including variants and amendments)
        forms_13d = ["13D", "13D/A", "SC 13D", "SC 13D/A", "SCHEDULE 13D", "SCHEDULE 13D/A"]
        forms_13g = ["13G", "13G/A", "SC 13G", "SC 13G/A", "SCHEDULE 13G", "SCHEDULE 13G/A"]
        
        schedule = str(schedule).upper().replace("SC ", "").strip()
        results_13d = await self.get_company_filings(ticker, form_type=forms_13d, limit=limit) if schedule in ("ALL", "13D") else {}
        results_13g = await self.get_company_filings(ticker, form_type=forms_13g, limit=limit) if schedule in ("ALL", "13G") else {}
        
        combined_filings = []
        
        # Combine results
        if "filings" in results_13d:
            combined_filings.extend(results_13d["filings"])
        if "filings" in results_13g:
            combined_filings.extend(results_13g["filings"])
        
        # Sort by filing date (most recent first)
        combined_filings.sort(key=lambda x: x["filing_date"], reverse=True)
        
        return {
            "ticker": ticker,
            "schedule": schedule,
            "total_filings": len(combined_filings[:limit]),
            "filings": combined_filings[:limit],
            "note": "13D = activist or control intent (>5%); 13G = passive holder (>5%). Use schedule='13D' or '13G' to filter."
        }

    # ============================================================
    # COMPANY FACTS & FINANCIAL DATA TOOLS
    # ============================================================

    @safe_sec_call
    @rate_limit()
    async def get_company_facts(self, ticker: str) -> Dict[str, Any]:
        """
        Get company facts from SEC XBRL data.
        
        Args:
            ticker: Stock ticker symbol
            
        Returns:
            Dictionary containing company facts and financial metrics
        """
        # Convert ticker to CIK
        cik = ticker_to_cik(ticker)
        if not cik:
            logger.error(f"CIK lookup failed for ticker: {ticker}")
            return {
                "error": "CIK lookup failed",
                "ticker": ticker,
                "message": f"Could not find CIK for ticker '{ticker}'",
                "suggestion": f"Verify '{ticker}' is a valid US stock ticker symbol"
            }

        try:
            url = f"{SEC_API_BASE}/api/xbrl/companyfacts/CIK{cik}.json"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract key financial metrics
            facts = data.get('facts', {})
            us_gaap = facts.get('us-gaap', {})
            
            # Key metrics to extract
            key_metrics = {
                'Revenues': us_gaap.get('Revenues', {}),
                'RevenueFromContractWithCustomerExcludingAssessedTax': us_gaap.get('RevenueFromContractWithCustomerExcludingAssessedTax', {}),
                'NetIncomeLoss': us_gaap.get('NetIncomeLoss', {}),
                'Assets': us_gaap.get('Assets', {}),
                'AssetsCurrent': us_gaap.get('AssetsCurrent', {}),
                'Liabilities': us_gaap.get('Liabilities', {}),
                'LiabilitiesCurrent': us_gaap.get('LiabilitiesCurrent', {}),
                'StockholdersEquity': us_gaap.get('StockholdersEquity', {}),
                'CashAndCashEquivalentsAtCarryingValue': us_gaap.get('CashAndCashEquivalentsAtCarryingValue', {}),
                'PropertyPlantAndEquipmentNet': us_gaap.get('PropertyPlantAndEquipmentNet', {}),
                'CommonStockSharesOutstanding': us_gaap.get('CommonStockSharesOutstanding', {}),
                'EarningsPerShareBasic': us_gaap.get('EarningsPerShareBasic', {}),
                'EarningsPerShareDiluted': us_gaap.get('EarningsPerShareDiluted', {})
            }
            
            # Process metrics to get latest values
            processed_metrics = {}
            for metric_name, metric_data in key_metrics.items():
                if metric_data and 'units' in metric_data:
                    # Get USD values if available
                    usd_data = metric_data['units'].get('USD', [])
                    if usd_data:
                        # Get most recent annual value
                        annual_values = [item for item in usd_data if item.get('form') in ['10-K', '10-K/A']]
                        if annual_values:
                            latest = max(annual_values, key=lambda x: x.get('end', ''))
                            processed_metrics[metric_name] = {
                                'value': latest.get('val'),
                                'end_date': latest.get('end'),
                                'form': latest.get('form'),
                                'filed': latest.get('filed')
                            }
            
            return {
                "ticker": ticker,
                "cik": cik,
                "company_name": data.get('entityName', 'Unknown'),
                "sic": data.get('sic', 'Unknown'),
                "sic_description": data.get('sicDescription', 'Unknown'),
                "key_metrics": processed_metrics,
                "data_as_of": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch company facts: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    @safe_sec_call
    @rate_limit()
    async def get_company_concept(self, ticker: str, concept: str) -> Dict[str, Any]:
        """
        Get specific financial concept data for a company.
        
        Args:
            ticker: Stock ticker symbol
            concept: XBRL concept (e.g., 'Revenues', 'NetIncomeLoss', 'Assets')
            
        Returns:
            Dictionary containing concept data over time
        """
        # Convert ticker to CIK
        cik = ticker_to_cik(ticker)
        if not cik:
            logger.error(f"CIK lookup failed for ticker: {ticker}")
            return {
                "error": "CIK lookup failed",
                "ticker": ticker,
                "message": f"Could not find CIK for ticker '{ticker}'",
                "suggestion": f"Verify '{ticker}' is a valid US stock ticker symbol"
            }

        try:
            url = f"{SEC_API_BASE}/api/xbrl/companyconcept/CIK{cik}/us-gaap/{concept}.json"
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Process the concept data
            units = data.get('units', {})
            usd_data = units.get('USD', [])
            
            if not usd_data:
                return {"error": f"No USD data found for concept: {concept}"}
            
            # Sort by end date
            usd_data.sort(key=lambda x: x.get('end', ''), reverse=True)
            
            # Get annual and quarterly data separately
            annual_data = [item for item in usd_data if item.get('form') in ['10-K', '10-K/A']][:5]
            quarterly_data = [item for item in usd_data if item.get('form') in ['10-Q', '10-Q/A']][:8]
            
            return {
                "ticker": ticker,
                "cik": cik,
                "concept": concept,
                "label": data.get('label', concept),
                "description": data.get('description', ''),
                "annual_data": annual_data,
                "quarterly_data": quarterly_data,
                "data_as_of": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch concept data: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    # ============================================================
    # SEARCH & DISCOVERY TOOLS
    # ============================================================

    @safe_sec_call
    @rate_limit()
    async def search_filings(
        self,
        query: str,
        form_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search SEC filings by company name or other criteria.
        
        Args:
            query: Search query (company name, ticker, etc.)
            form_type: SEC form type to filter by
            start_date: Start date for search (YYYY-MM-DD)
            end_date: End date for search (YYYY-MM-DD)
            limit: Maximum number of results
            
        Returns:
            Dictionary containing search results
        """
        try:
            # Use SEC's company tickers endpoint to find matching companies
            response = self.session.get(f"{SEC_BASE_URL}/files/company_tickers.json", timeout=30)
            response.raise_for_status()
            
            tickers_data = response.json()
            
            # Search for matching companies
            matching_companies = []
            query_lower = query.lower()
            
            for company_data in tickers_data.values():
                company_name = company_data.get('title', '').lower()
                ticker = company_data.get('ticker', '').lower()
                
                if (query_lower in company_name or 
                    query_lower in ticker or 
                    ticker == query_lower):
                    matching_companies.append({
                        'cik': str(company_data.get('cik_str', '')).zfill(10),
                        'ticker': company_data.get('ticker', ''),
                        'company_name': company_data.get('title', ''),
                        'exchange': company_data.get('exchange', '')
                    })
            
            if not matching_companies:
                return {"error": f"No companies found matching query: {query}"}
            
            # Get filings for matching companies
            all_results = []
            
            for company in matching_companies[:5]:  # Limit to first 5 matching companies
                try:
                    filings_result = await self.get_company_filings(
                        company['ticker'],
                        form_type=form_type,
                        limit=limit//len(matching_companies[:5]),
                        start_date=start_date,
                        end_date=end_date
                    )
                    
                    if "filings" in filings_result:
                        for filing in filings_result["filings"]:
                            filing["company_info"] = company
                            all_results.append(filing)
                            
                except Exception as e:
                    logger.warning(f"Error getting filings for {company['ticker']}: {e}")
                    continue
            
            # Sort by filing date (most recent first)
            all_results.sort(key=lambda x: x.get("filing_date", ""), reverse=True)
            
            return {
                "query": query,
                "matching_companies": matching_companies,
                "total_results": len(all_results),
                "results": all_results[:limit]
            }

        except Exception as e:
            return {"error": f"Search failed: {str(e)}"}

    # ============================================================
    # FILING SIZE, DOCUMENTS & SEARCH TOOLS
    # ============================================================

    def _filing_folder(self, filing_url: str) -> Optional[Tuple[str, str, str]]:
        """Return (folder_url, cik, accession_no_dashes) for an EDGAR Archives URL"""
        if not is_sec_url(filing_url):
            return None
        match = re.search(r'/Archives/edgar/data/(\d+)/(\d{18})(?:/|$)', urlparse(filing_url).path)
        if not match:
            match = re.search(r'/Archives/edgar/data/(\d+)/(\d{10}-\d{2}-\d{6})', urlparse(filing_url).path)
            if not match:
                return None
        cik, accession = match.group(1), match.group(2).replace('-', '')
        return f"{SEC_EDGAR_BASE}/{cik}/{accession}", cik, accession

    def _filing_index(self, filing_url: str) -> Optional[List[Dict[str, Any]]]:
        """List the files of a filing with their sizes in bytes (from EDGAR index.json)"""
        folder = self._filing_folder(filing_url)
        if not folder:
            return None
        response = self.session.get(f"{folder[0]}/index.json", timeout=20)
        response.raise_for_status()
        items = response.json().get('directory', {}).get('item', [])
        files = []
        for item in items:
            size = str(item.get('size', '')).strip()
            files.append({
                "name": item.get('name', ''),
                "size_bytes": int(size) if size.isdigit() else None,
                "url": f"{folder[0]}/{item.get('name', '')}",
            })
        return files

    def _document_size(self, filing_url: str) -> Optional[int]:
        """Exact size in bytes of the document a filing URL points to, or None if unknown"""
        try:
            files = self._filing_index(filing_url)
        except Exception as e:
            logger.warning(f"Could not read filing index for {filing_url}: {e}")
            return None
        if not files:
            return None
        name = urlparse(filing_url).path.rstrip('/').rsplit('/', 1)[-1]
        for f in files:
            if f["name"] == name:
                return f["size_bytes"]
        return None

    @safe_sec_call
    @rate_limit()
    async def get_filing_size(self, filing_url: str) -> Dict[str, Any]:
        """
        Get the exact size of a filing document BEFORE downloading it.

        Use this to decide between reading the text (download_filing_text) and
        giving the user the link only. Sizes come from the EDGAR filing index.

        Args:
            filing_url: Filing document URL (https://www.sec.gov/Archives/edgar/data/...)

        Returns:
            size_bytes, size_mb, recommendation ('read_text' or 'link_only') and filing_url
        """
        if not is_sec_url(filing_url):
            return {"error": "Only https://*.sec.gov URLs are allowed", "filing_url": filing_url}
        size = self._document_size(filing_url)
        if size is None:
            return {"filing_url": filing_url, "size_bytes": None,
                    "note": "Size not listed in the EDGAR index. download_filing_text still stops safely at its size limit."}
        return {
            "filing_url": filing_url,
            "size_bytes": size,
            "size_mb": round(size / (1024 * 1024), 2),
            "recommendation": "read_text" if size <= MAX_FILING_BYTES else "link_only",
            "note": f"Documents up to {MAX_FILING_BYTES // (1024 * 1024)}MB can be read as text (in pages) or searched; larger ones are returned as a link."
        }

    @safe_sec_call
    @rate_limit()
    async def get_filing_documents(self, filing_url: str) -> Dict[str, Any]:
        """
        List every document in a filing (main document, exhibits, XBRL, XML) with sizes and links.

        Args:
            filing_url: Any URL inside the filing folder (https://www.sec.gov/Archives/edgar/data/CIK/ACCESSION/...)

        Returns:
            Dictionary with the filing folder and its documents (name, size_bytes, url)
        """
        folder = self._filing_folder(filing_url)
        if not folder:
            return {"error": "Not an EDGAR filing URL (expected https://www.sec.gov/Archives/edgar/data/CIK/ACCESSION/...)", "filing_url": filing_url}
        files = self._filing_index(filing_url) or []
        documents = [f for f in files if not f["name"].endswith(('-index.html', '-index-headers.html'))]
        return {
            "filing_folder": folder[0],
            "cik": folder[1],
            "accession_number": f"{folder[2][:10]}-{folder[2][10:12]}-{folder[2][12:]}",
            "total_documents": len(documents),
            "documents": documents
        }

    def _efts(self, params: Dict[str, str], limit: int) -> List[Dict[str, Any]]:
        """Query EDGAR full-text search and return simplified hits"""
        response = self.session.get(SEC_EFTS_URL, params=params, timeout=30)
        response.raise_for_status()
        hits = response.json().get('hits', {}).get('hits', [])
        results = []
        for hit in hits[:max(1, min(int(limit), 100))]:
            src = hit.get('_source', {})
            adsh, _, document = hit.get('_id', '').partition(':')
            ciks = src.get('ciks') or ['']
            cik = ciks[0].lstrip('0')
            results.append({
                "company": (src.get('display_names') or [''])[0],
                "cik": cik,
                "form": src.get('form') or src.get('file_type'),
                "filing_date": src.get('file_date'),
                "period_ending": src.get('period_ending'),
                "accession_number": adsh,
                "filing_url": f"{SEC_EDGAR_BASE}/{cik}/{adsh.replace('-', '')}/{document}" if cik and adsh else None,
            })
        return results

    @safe_sec_call
    @rate_limit()
    async def full_text_search(
        self,
        query: str,
        form_type: Optional[Union[str, List[str]]] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Search the full text of every EDGAR filing since 2001 (words or "exact phrase").

        Args:
            query: Words to find, e.g. 'tariffs' or '"going concern"' for an exact phrase
            form_type: Optional form filter, e.g. '8-K' or '10-K,10-Q'
            start_date: Optional YYYY-MM-DD (default: one year ago; use '2001-01-01' for all history)
            end_date: Optional YYYY-MM-DD (default: today)
            limit: Max results (1-100, default 20)

        Returns:
            Matching filings (newest first) with company, form, date and a link to the matching document
        """
        query = str(query or '').strip()
        if not query:
            return {"error": "query is required"}
        params = {"q": query}
        forms = form_list(form_type)
        if forms:
            params["forms"] = ",".join(forms)
        dates = DateRangeValidator(start_date=start_date, end_date=end_date)
        params.update(dateRange="custom",
                      startdt=dates.start_date or (date.today() - timedelta(days=365)).isoformat(),
                      enddt=dates.end_date or date.today().isoformat())
        results = self._efts(params, 100)
        results.sort(key=lambda r: r.get("filing_date") or "", reverse=True)
        results = results[:max(1, min(int(limit), 100))]
        return {"query": query, "forms": forms or "all", "date_range": f"{params['startdt']} to {params['enddt']}",
                "total_results": len(results), "results": results}

    @safe_sec_call
    @rate_limit()
    async def get_recent_ipos(self, limit: int = 20, days: int = 30) -> Dict[str, Any]:
        """
        Get recent IPO activity from EDGAR.

        Args:
            limit: Max companies per list (default 20)
            days: Look-back window in days (default 30)

        Returns:
            priced: final prospectuses (424B4, filed when an offering is priced)
            registrations: new S-1 / F-1 registration statements (companies preparing to list)
        """
        days = max(1, min(int(days), 365))
        window = {"dateRange": "custom", "startdt": (date.today() - timedelta(days=days)).isoformat(),
                  "enddt": date.today().isoformat()}

        def unique(rows):
            seen, out = set(), []
            for row in rows:
                if row["cik"] not in seen:
                    seen.add(row["cik"])
                    out.append(row)
            return out[:limit]

        priced = unique(self._efts({**window, "forms": "424B4"}, 100))
        registrations = unique(self._efts({**window, "forms": "S-1,F-1"}, 100))
        return {
            "window": f"last {days} days",
            "priced": priced,
            "registrations": registrations,
            "note": "424B4 = priced offering (IPOs and some follow-on offerings). S-1/F-1 = registration filed, not yet priced."
        }

    @safe_sec_call
    @rate_limit()
    async def get_13f_holdings(self, ticker_or_cik: str, limit: int = 25) -> Dict[str, Any]:
        """
        Get the latest 13F portfolio of an institutional investment manager.

        Args:
            ticker_or_cik: Manager ticker (e.g. 'BRK-B') or CIK (e.g. '1350694' for Bridgewater)
            limit: Number of top positions to return (default 25)

        Returns:
            Report period, total value, top_issuers (one row per company, share classes combined;
            use this for "largest holdings") and top_positions (one row per security: CUSIP,
            share class, put/call)
        """
        cik = ticker_to_cik(str(ticker_or_cik))
        if not cik:
            return {"error": f"Could not resolve '{ticker_or_cik}' to a CIK. Pass the manager's CIK."}
        response = self.session.get(f"{SEC_API_BASE}/submissions/CIK{cik}.json", timeout=30)
        response.raise_for_status()
        data = response.json()
        recent = data.get('filings', {}).get('recent', {})
        forms = recent.get('form', [])
        index = next((i for i, f in enumerate(forms) if f in ("13F-HR", "13F-HR/A")), None)
        if index is None:
            return {"error": f"No 13F-HR filing found for {data.get('name', cik)}", "cik": cik}
        accession = recent['accessionNumber'][index]
        folder = f"{SEC_EDGAR_BASE}/{int(cik)}/{accession.replace('-', '')}"
        files = self._filing_index(folder + "/") or []
        table = next((f for f in files if f["name"].lower().endswith('.xml') and f["name"].lower() != 'primary_doc.xml'), None)
        if not table:
            return {"error": "13F information table not found", "filing_folder": folder}
        root = ET.fromstring(self.session.get(table["url"], timeout=30).content)

        def text(node, tag):
            found = node.find(f'.//{{*}}{tag}')
            return found.text.strip() if found is not None and found.text else ''

        positions = {}
        for row in root.iter():
            if not row.tag.endswith('infoTable'):
                continue
            key = (text(row, 'nameOfIssuer'), text(row, 'cusip'), text(row, 'putCall'))
            value = float(text(row, 'value') or 0)
            shares = float(text(row, 'sshPrnamt') or 0)
            current = positions.setdefault(key, {"issuer": key[0], "cusip": key[1], "class": text(row, 'titleOfClass'),
                                                 "put_call": key[2] or None, "value_usd": 0.0, "shares": 0.0})
            current["value_usd"] += value
            current["shares"] += shares
        ranked = sorted(positions.values(), key=lambda p: p["value_usd"], reverse=True)
        total = sum(p["value_usd"] for p in ranked)
        for p in ranked:
            p["weight_pct"] = round(100 * p["value_usd"] / total, 2) if total else None
        issuers = {}
        for p in ranked:
            row = issuers.setdefault(p["issuer"], {"issuer": p["issuer"], "value_usd": 0.0, "securities": []})
            row["value_usd"] += p["value_usd"]
            row["securities"].append(p["class"] + (f" ({p['put_call']})" if p["put_call"] else ""))
        by_issuer = sorted(issuers.values(), key=lambda p: p["value_usd"], reverse=True)
        for p in by_issuer:
            p["weight_pct"] = round(100 * p["value_usd"] / total, 2) if total else None
        return {
            "manager": data.get('name'),
            "cik": cik,
            "form": forms[index],
            "filing_date": recent['filingDate'][index],
            "report_period": (recent.get('reportDate') or [''] * len(forms))[index],
            "total_value_usd": total,
            "total_issuers": len(by_issuer),
            "top_issuers": by_issuer[:max(1, int(limit))],
            "total_positions": len(ranked),
            "top_positions": ranked[:max(1, int(limit))],
            "filing_folder": folder,
            "note": ("top_issuers combines every share class, put and call of a company: use it for the largest "
                     "holdings. top_positions lists each security (CUSIP) separately. Values in US dollars as "
                     "reported (filings before 2023 reported thousands).")
        }

    @safe_sec_call
    @rate_limit()
    async def get_xbrl_frames(
        self,
        concept: str,
        period: str,
        unit: str = "USD",
        taxonomy: str = "us-gaap",
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Compare one financial concept across ALL reporting companies for one period.

        Args:
            concept: XBRL tag, e.g. 'Revenues', 'NetIncomeLoss', 'Assets'
            period: 'CY2024' (annual), 'CY2024Q3' (quarter) or 'CY2024Q4I' (balance-sheet instant)
            unit: 'USD' (default), 'USD-per-shares', 'shares'
            taxonomy: 'us-gaap' (default), 'ifrs-full', 'dei'
            limit: Number of top companies to return (default 20)

        Returns:
            Companies ranked by value for that concept and period
        """
        if not re.match(r'^[A-Za-z0-9_]+$', concept or ''):
            return {"error": f"Invalid concept: {concept}"}
        period = str(period).upper()
        if not re.match(r'^CY\d{4}(Q[1-4]I?)?$', period):
            return {"error": "period must look like CY2024, CY2024Q3 or CY2024Q4I"}
        if not re.match(r'^[A-Za-z0-9\-]+$', unit or '') or not re.match(r'^[a-z\-]+$', taxonomy or ''):
            return {"error": "Invalid unit or taxonomy"}
        response = self.session.get(f"{SEC_API_BASE}/api/xbrl/frames/{taxonomy}/{concept}/{unit}/{period}.json", timeout=30)
        if response.status_code == 404:
            return {"error": f"No data for {taxonomy}/{concept}/{unit}/{period}"}
        response.raise_for_status()
        data = response.json()
        rows = sorted(data.get('data', []), key=lambda r: r.get('val') or 0, reverse=True)
        return {
            "concept": concept,
            "label": data.get('label'),
            "period": period,
            "unit": unit,
            "total_companies": len(rows),
            "top": [{"company": r.get('entityName'), "cik": r.get('cik'), "value": r.get('val'),
                     "period_end": r.get('end'), "accession_number": r.get('accn')}
                    for r in rows[:max(1, int(limit))]]
        }

    # ============================================================
    # UTILITY & TESTING TOOLS
    # ============================================================

    async def get_sec_api_status(self) -> Dict[str, Any]:
        """
        Check SEC API status and connectivity.
        
        Returns:
            Dictionary containing API status information
        """
        try:
            # Test basic connectivity
            start_time = time.time()
            response = self.session.get(f"{SEC_BASE_URL}/files/company_tickers.json", timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "status": "operational",
                    "response_time_ms": round(response_time * 1000, 2),
                    "total_companies": len(data),
                    "last_checked": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {
                    "status": "error",
                    "status_code": response.status_code,
                    "last_checked": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "last_checked": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

    async def run_self_test(self) -> Dict[str, Any]:
        """
        Run comprehensive self-test of all SEC-AI tools.
        
        Returns:
            Dictionary containing test results
        """
        test_results = {
            "test_started": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "tests": {},
            "summary": {}
        }
        
        # Test cases
        test_cases = [
            ("API Status", self.get_sec_api_status),
            ("Company Filings", lambda: self.get_company_filings("AAPL", limit=3)),
            ("Latest 10-K", lambda: self.get_latest_10k("AAPL")),
            ("Latest 10-Q", lambda: self.get_latest_10q("AAPL")),
            ("Recent 8-K", lambda: self.get_recent_8k_filings("AAPL", limit=2)),
            ("Analyze 8-K", lambda: self.analyze_8k_filing("AAPL")),
            ("Proxy Statements", lambda: self.get_proxy_statements("AAPL", limit=1)),
            ("Company Facts", lambda: self.get_company_facts("AAPL")),
            ("Company Concept", lambda: self.get_company_concept("AAPL", "Assets")),
            ("Insider Transactions", lambda: self.get_insider_transactions("AAPL", limit=3)),
            ("Beneficial Ownership", lambda: self.get_beneficial_ownership("AAPL", limit=1)),
            ("Available Metrics", lambda: self.get_available_metrics("AAPL")),
            ("Filing Content (Smart Mode)", lambda: self.get_filing_content("AAPL")),
            ("Full Content Download", lambda: self.get_filing_content("AAPL", get_full_content=True)),
            ("Download Filing Text Tool", lambda: self.download_filing_text("https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm", max_length=1000)),
            ("Recent IPOs", lambda: self.get_recent_ipos(limit=5)),
            ("Filing Size", lambda: self.get_filing_size("https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm")),
            ("Filing Documents", lambda: self.get_filing_documents("https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm")),
            ("Search Inside Filing", lambda: self.download_filing_text("https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm", search="iPhone")),
            ("Full-Text Search", lambda: self.full_text_search('"going concern"', form_type="8-K", limit=3)),
            ("13F Holdings", lambda: self.get_13f_holdings("BRK-B", limit=5)),
            ("XBRL Frames", lambda: self.get_xbrl_frames("Revenues", "CY2024", limit=5)),
            ("Older Filings", lambda: self.get_company_filings("AAPL", form_type="10-K", limit=15)),
            ("Share Class Ticker", lambda: self.get_company_filings("BRK.B", limit=1)),
            ("Schedule 13D Only", lambda: self.get_beneficial_ownership("AAPL", limit=1, schedule="13D")),
            ("Search Filings", lambda: self.search_filings("Apple", limit=3)),
            ("Dynamic Ticker", lambda: self.get_company_filings("HOOD", limit=1)),
            ("Available Functions", lambda: {"functions": self.get_available_functions()})
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in test_cases:
            try:
                start_time = time.time()
                # Handle both sync and async functions
                if asyncio.iscoroutinefunction(test_func) or (hasattr(test_func, 'func') and asyncio.iscoroutinefunction(test_func.func)):
                    result = await test_func()
                elif callable(test_func):
                    # Check if it's a lambda or function that returns a coroutine
                    res = test_func()
                    if asyncio.iscoroutine(res):
                        result = await res
                    else:
                        result = res
                else:
                    result = test_func
                
                execution_time = time.time() - start_time
                
                if "error" not in result:
                    test_results["tests"][test_name] = {
                        "status": "PASSED",
                        "execution_time_ms": round(execution_time * 1000, 2),
                        "data_points": len(result) if isinstance(result, dict) else 1
                    }
                    passed += 1
                else:
                    test_results["tests"][test_name] = {
                        "status": "FAILED",
                        "error": result["error"],
                        "execution_time_ms": round(execution_time * 1000, 2)
                    }
                    failed += 1
                    
            except Exception as e:
                test_results["tests"][test_name] = {
                    "status": "FAILED",
                    "error": str(e),
                    "execution_time_ms": 0
                }
                failed += 1
        
        test_results["summary"] = {
            "total_tests": len(test_cases),
            "passed": passed,
            "failed": failed,
            "success_rate": f"{(passed/len(test_cases)*100):.1f}%",
            "test_completed": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return test_results

    # ============================================================
    # METRIC DISCOVERY & FILTERING TOOLS
    # ============================================================

    @safe_sec_call
    @rate_limit()
    async def get_available_metrics(self, ticker: str, search_term: str = None) -> Dict[str, Any]:
        """
        Discover available financial metrics for a company from SEC XBRL data.

        This function lists ALL available metrics that can be requested via specific_metrics.
        Useful for AI to find exactly which metrics are available before requesting them.

        Args:
            ticker: Stock ticker symbol (e.g., 'GME', 'AAPL')
            search_term: Optional search term to filter metrics (e.g., 'EBITDA', 'Revenue', 'Debt')

        Returns:
            Dict containing:
            - all_metrics: List of ALL available metric names
            - filtered_metrics: List of metrics matching search_term (if provided)
            - metric_categories: Organized by category (income, balance_sheet, cash_flow, etc)
            - total_available: Total number of available metrics
            - example_ttm_metrics: Example metrics useful for TTM calculations
        """
        try:
            logger.info(f"Discovering metrics for {ticker}...")

            # Get CIK (ticker_to_cik is a regular function, not async - returns CIK string or None)
            cik = ticker_to_cik(ticker)
            if not cik:
                return {"error": f"Failed to find CIK for ticker {ticker}"}

            # Get all available metrics from SEC API
            facts_url = f"{SEC_API_BASE}/api/xbrl/companyfacts/CIK{cik}.json"
            response = self.session.get(facts_url, timeout=30)
            response.raise_for_status()

            data = response.json()
            us_gaap = data.get("facts", {}).get("us-gaap", {})
            all_metrics = sorted(list(us_gaap.keys()))

            # Categorize metrics based on naming patterns
            categories = {
                "income_statement": [],
                "balance_sheet": [],
                "cash_flow": [],
                "earnings_per_share": [],
                "shares_and_stock": [],
                "segment_data": [],
                "other": []
            }

            income_keywords = ["Income", "Loss", "Revenues", "Expense", "Earnings", "Operating", "Gross"]
            balance_keywords = ["Assets", "Liabilities", "Equity", "Stockholders", "Payable", "Receivable"]
            cashflow_keywords = ["CashFlow", "Cash", "Depreciation", "Amortization"]
            eps_keywords = ["EPS", "EarningsPerShare", "Weighted"]
            shares_keywords = ["Shares", "Outstanding", "Stock"]
            segment_keywords = ["Segment"]

            for metric in all_metrics:
                categorized = False

                for keyword in income_keywords:
                    if keyword.lower() in metric.lower():
                        categories["income_statement"].append(metric)
                        categorized = True
                        break

                if not categorized:
                    for keyword in balance_keywords:
                        if keyword.lower() in metric.lower():
                            categories["balance_sheet"].append(metric)
                            categorized = True
                            break

                if not categorized:
                    for keyword in cashflow_keywords:
                        if keyword.lower() in metric.lower():
                            categories["cash_flow"].append(metric)
                            categorized = True
                            break

                if not categorized:
                    for keyword in eps_keywords:
                        if keyword.lower() in metric.lower():
                            categories["earnings_per_share"].append(metric)
                            categorized = True
                            break

                if not categorized:
                    for keyword in shares_keywords:
                        if keyword.lower() in metric.lower():
                            categories["shares_and_stock"].append(metric)
                            categorized = True
                            break

                if not categorized:
                    for keyword in segment_keywords:
                        if keyword.lower() in metric.lower():
                            categories["segment_data"].append(metric)
                            categorized = True
                            break

                if not categorized:
                    categories["other"].append(metric)

            # Filter by search term if provided
            filtered_metrics = []
            if search_term:
                search_lower = search_term.lower()
                filtered_metrics = [m for m in all_metrics if search_lower in m.lower()]
                logger.info(f"Found {len(filtered_metrics)} metrics matching '{search_term}'")

            # Common TTM calculation metrics
            ttm_example_metrics = [
                "NetIncomeLoss",
                "Revenues",
                "InterestExpense",
                "IncomeTaxExpenseBenefit",
                "OperatingIncomeLoss",
                "DepreciationDepletionAndAmortization",
                "GrossProfit",
                "OperatingExpenses"
            ]

            result = {
                "ticker": ticker,
                "company_name": data.get("entityName", ticker),
                "total_available": len(all_metrics),
                "all_metrics": all_metrics,
                "categories": {k: v for k, v in categories.items() if v},
                "category_counts": {k: len(v) for k, v in categories.items() if v},
                "data_source": "SEC EDGAR XBRL",
                "discovery_timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "usage_tips": {
                    "generic_mode": "Call get_filing_content() without specific_metrics to get 13 essential metrics (default, token-efficient)",
                    "specific_mode": "Call get_filing_content() with specific_metrics=['MetricName1', 'MetricName2', ...] to get only what you need",
                    "ttm_calculation": "For TTM calculations, use specific_metrics with these: " + str(ttm_example_metrics),
                    "metric_search": "Use get_available_metrics(ticker='GME', search_term='EBITDA') to find related metrics"
                }
            }

            if filtered_metrics:
                result["filtered_metrics"] = filtered_metrics
                result["filtered_count"] = len(filtered_metrics)

            logger.info(f"✓ Found {len(all_metrics)} total metrics for {ticker}")
            return result

        except requests.exceptions.RequestException as e:
            logger.error(f"SEC API failed: {e}")
            return {"error": f"SEC API failed: {str(e)}", "ticker": ticker}
        except Exception as e:
            logger.error(f"Error discovering metrics: {e}", exc_info=True)
            return {"error": str(e), "ticker": ticker}

    @safe_sec_call
    @rate_limit()
    async def get_filing_content(self, ticker: str, filing_type: str = None, get_full_content: bool = False, specific_metrics: list = None) -> Optional[Dict[str, Any]]:
        """
        Get SEC financial data - SMART & EFFICIENT dual-mode approach.

        ╔════════════════════════════════════════════════════════════════════╗
        ║  GENERIC MODE (no specific_metrics parameter)                      ║
        ║  - Returns 13 essential metrics for any financial analysis         ║
        ║  - 5 historical values per metric (sufficient for TTM calc)        ║
        ║  - Most token-efficient for general questions                      ║
        ║  - Includes: Net Income, Revenues, Interest Expense, Taxes,        ║
        ║    Operating Income, Gross Profit, Assets, Liabilities, Equity,   ║
        ║    Depreciation, Shares Outstanding, Cash, Long-term Debt         ║
        ╚════════════════════════════════════════════════════════════════════╝

        ╔════════════════════════════════════════════════════════════════════╗
        ║  SPECIFIC MODE (provide specific_metrics parameter)                ║
        ║  - Returns ONLY the requested metrics you specify                  ║
        ║  - Perfect for targeted analysis (TTM EBITDA, leverage ratios)    ║
        ║  - Minimal token usage - only fetch what you need                  ║
        ║  - Example: ['NetIncomeLoss', 'DepreciationDepletionAndAmortization',║
        ║    'InterestExpense', 'IncomeTaxExpenseBenefit']                   ║
        ║  - Use get_available_metrics(ticker) to discover all metrics      ║
        ╚════════════════════════════════════════════════════════════════════╝

        WORKFLOW FOR TTM CALCULATIONS:
        1. Call: get_available_metrics(ticker='GME', search_term='Depreciation')
        2. Find needed metrics from results
        3. Call: get_filing_content(ticker='GME', specific_metrics=['NetIncomeLoss', ...])
        4. Calculate TTM from 5 historical values (last 4 quarters + 1 prior)

        FILE HANDLING (get_full_content=True):
        - The exact document size is checked first (EDGAR filing index)
        - Up to 25MB: first 50,000 characters in full_content; if has_more, continue with
          download_filing_text(filing_url, offset=next_offset) or search it with search='keyword'
        - Over 25MB: link only (file_too_large=True), AI told via ai_note

        Args:
            ticker: Stock ticker symbol (e.g., 'GME', 'AAPL')
            filing_type: Type of filing - '10-Q', '10-K', '8-K', etc. (None = get latest)
            get_full_content: If True, check and optionally download full filing text
            specific_metrics: List of specific metric names to fetch.
                            If None, returns 13 essential metrics (generic mode).
                            Example: ['NetIncomeLoss', 'Revenues', 'DepreciationDepletionAndAmortization']
                            Use get_available_metrics() to discover what's available.

        Returns:
            Dict containing:
            - ticker, cik, company_name: Company identification
            - financial_metrics: Dict of requested/essential metrics with 5 historical values each
            - filing_date, filing_type: Filing metadata
            - mode: "generic" or "specific"
            - metrics_returned, values_per_metric: Data shape info
            - content_mode: 'text' or 'link_only'
            - full_content, has_more, next_offset: first page of the filing text
            - file_size_mb, filing_url, ai_note: size, link and what to do next
        """
        try:
            logger.info(f"Fetching SEC data for {ticker}...")

            # Step 1: Get filings metadata
            filings_result = await self.get_company_filings(ticker, form_type=filing_type, limit=1)

            if "error" in filings_result:
                return {"error": f"Failed to fetch filings: {filings_result.get('error')}"}

            cik = filings_result.get("cik")
            company_name = filings_result.get("company_name")

            # Step 2: Get financial data but ONLY keep requested/essential metrics (save tokens)
            facts_url = f"{SEC_API_BASE}/api/xbrl/companyfacts/CIK{cik}.json"
            logger.info(f"Fetching financial metrics...")

            response = self.session.get(facts_url, timeout=30)
            response.raise_for_status()

            raw_financial_data = response.json()

            # Determine which metrics to fetch
            if specific_metrics:
                # AI requested specific metrics only (save maximum tokens)
                metrics_to_fetch = specific_metrics
                logger.info(f"Specific mode: Fetching {len(metrics_to_fetch)} requested metrics")
            else:
                # Generic mode: Return essentials for any question
                metrics_to_fetch = [
                    "NetIncomeLoss", "Revenues", "InterestExpense",
                    "IncomeTaxExpenseBenefit", "OperatingIncomeLoss",
                    "GrossProfit", "Assets", "Liabilities", "StockholdersEquity",
                    "DepreciationDepletionAndAmortization", "CommonStockSharesOutstanding",
                    "CashAndCashEquivalentsAtCarryingValue", "LongTermDebt"
                ]
                logger.info(f"Generic mode: Fetching {len(metrics_to_fetch)} essential metrics")

            us_gaap = raw_financial_data.get("facts", {}).get("us-gaap", {})
            financial_data_slim = {}

            for metric in metrics_to_fetch:
                if metric in us_gaap:
                    metric_info = us_gaap[metric].copy()
                    if "units" in metric_info and "USD" in metric_info["units"]:
                        # Keep last 5 values for proper TTM calculations
                        metric_info["units"]["USD"] = metric_info["units"]["USD"][-5:]
                    financial_data_slim[metric] = metric_info

            logger.info(f"✓ Kept {len(financial_data_slim)} metrics (last 5 values each)")

            # Step 3: Build base response (lean)
            response_data = {
                "ticker": ticker,
                "cik": cik,
                "company_name": company_name,
                "financial_metrics": financial_data_slim,
                "filing_date": filings_result.get("filings", [{}])[0].get("filing_date"),
                "filing_type": filing_type or "Latest",
                "data_source": "SEC EDGAR API",
                "mode": "specific" if specific_metrics else "generic",
                "metrics_returned": len(financial_data_slim),
                "values_per_metric": 5
            }

            # Step 4: Handle full content request
            if get_full_content and filings_result.get("filings"):
                latest_filing = filings_result["filings"][0]
                filing_url = latest_filing.get("filing_url")

                logger.info(f"Checking filing size for URL: {filing_url}")

                try:
                    filing = self._read_filing(filing_url, max_length=TEXT_PAGE_CHARS)
                    response_data["filing_url"] = filing_url
                    response_data["content_mode"] = filing["mode"]
                    response_data["file_size_mb"] = filing.get("size_mb")
                    response_data["ai_note"] = filing.get("ai_note")
                    if filing["mode"] == "link_only":
                        response_data["file_too_large"] = True
                    else:
                        response_data["full_content"] = filing["content"]
                        response_data["total_characters"] = filing["total_characters"]
                        response_data["has_more"] = filing["has_more"]
                        response_data["next_offset"] = filing["next_offset"]
                except Exception as e:
                    logger.error(f"Error reading filing: {e}")
                    response_data["filing_url"] = filing_url
                    response_data["note"] = f"Could not read the filing text. Link: {filing_url}"

            logger.info(f"✓ Response ready")
            return response_data

        except requests.exceptions.RequestException as e:
            logger.error(f"SEC API failed: {e}")
            return {"error": f"SEC API failed: {str(e)}", "ticker": ticker}
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            return {"error": str(e), "ticker": ticker}

    def get_available_functions(self) -> List[Dict[str, Any]]:
        """
        List every callable SEC-AI function with its parameters and summary.

        Returns:
            List of {"name", "description", "parameters"} built from the code itself
        """
        functions = []
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if name.startswith('_') or name in ('get_available_functions', 'run_self_test'):
                continue
            doc = inspect.getdoc(method) or ''
            params = {}
            for pname, param in inspect.signature(method).parameters.items():
                params[pname] = "required" if param.default is inspect.Parameter.empty else f"optional, default {param.default!r}"
            functions.append({
                "name": name,
                "description": doc.strip().splitlines()[0] if doc.strip() else "",
                "parameters": params
            })
        return functions

# ============================================================
# OPENWEBUI FUNCTION EXPORTS
# ============================================================

# Initialize the tools instance
tools = Tools()

# Export individual functions for OpenWebUI
async def get_company_filings(ticker: str, form_type: str = None, limit: int = 10, start_date: str = None, end_date: str = None) -> dict:
    """Get SEC filings for a company by ticker symbol"""
    return await tools.get_company_filings(ticker, form_type, limit, start_date, end_date)

async def get_latest_10k(ticker: str) -> dict:
    """Get the latest 10-K filing for a company"""
    return await tools.get_latest_10k(ticker)

async def get_latest_10q(ticker: str) -> dict:
    """Get the latest 10-Q filing for a company"""
    return await tools.get_latest_10q(ticker)

async def get_recent_8k_filings(ticker: str, limit: int = 5) -> dict:
    """Get recent 8-K filings for a company"""
    return await tools.get_recent_8k_filings(ticker, limit)

async def get_proxy_statements(ticker: str, limit: int = 3) -> dict:
    """Get proxy statements for a company"""
    return await tools.get_proxy_statements(ticker, limit)

async def get_insider_transactions(ticker: str, limit: int = 20) -> dict:
    """Get insider trading transactions for a company"""
    return await tools.get_insider_transactions(ticker, limit)

async def get_beneficial_ownership(ticker: str, limit: int = 10, schedule: str = "all") -> dict:
    """Get beneficial ownership reports for a company"""
    return await tools.get_beneficial_ownership(ticker, limit, schedule)

async def get_company_facts(ticker: str) -> dict:
    """Get company facts from SEC XBRL data"""
    return await tools.get_company_facts(ticker)

async def get_company_concept(ticker: str, concept: str) -> dict:
    """Get specific financial concept data for a company"""
    return await tools.get_company_concept(ticker, concept)

async def get_available_metrics(ticker: str, search_term: str = None) -> dict:
    """Discover all available financial metrics for a company from SEC XBRL data"""
    return await tools.get_available_metrics(ticker, search_term)

async def search_filings(query: str, form_type: str = None, start_date: str = None, end_date: str = None, limit: int = 20) -> dict:
    """Search SEC filings by company name or criteria"""
    return await tools.search_filings(query, form_type, start_date, end_date, limit)

async def get_sec_api_status() -> dict:
    """Check SEC API status and connectivity"""
    return await tools.get_sec_api_status()

async def download_filing_text(filing_url: str, max_length: int = TEXT_PAGE_CHARS, offset: int = 0, search: str = None) -> dict:
    return await tools.download_filing_text(filing_url, max_length, offset, search)

async def get_filing_size(filing_url: str) -> dict:
    return await tools.get_filing_size(filing_url)

async def get_filing_documents(filing_url: str) -> dict:
    return await tools.get_filing_documents(filing_url)

async def full_text_search(query: str, form_type: str = None, start_date: str = None, end_date: str = None, limit: int = 20) -> dict:
    return await tools.full_text_search(query, form_type, start_date, end_date, limit)

async def get_13f_holdings(ticker_or_cik: str, limit: int = 25) -> dict:
    return await tools.get_13f_holdings(ticker_or_cik, limit)

async def get_xbrl_frames(concept: str, period: str, unit: str = "USD", taxonomy: str = "us-gaap", limit: int = 20) -> dict:
    return await tools.get_xbrl_frames(concept, period, unit, taxonomy, limit)

async def get_filing_content(ticker: str, filing_type: str = "10-Q", get_full_content: bool = False, specific_metrics: list = None) -> dict:
    """
    Get SEC financial data - SMART dual-mode approach.

    GENERIC MODE (no specific_metrics):
    - Returns 13 essential metrics with 5 historical values each
    - Most token-efficient for general financial analysis
    - Default behavior when specific_metrics not provided

    SPECIFIC MODE (provide specific_metrics):
    - Returns ONLY the metrics you specify with 5 historical values each
    - Perfect for TTM calculations, leverage ratios, custom analysis
    - Minimal token usage - only fetch what you actually need
    - Example: specific_metrics=['NetIncomeLoss', 'InterestExpense', 'DepreciationDepletionAndAmortization']

    FILE HANDLING (get_full_content=True):
    - Size is checked first from the EDGAR index
    - Up to 25MB: first 50,000 characters in full_content; if has_more, continue with
      download_filing_text(filing_url, offset=next_offset) or search it with search='keyword'
    - Over 25MB: link only (file_too_large=True) with an ai_note

    WORKFLOW:
    1. Get available metrics: get_available_metrics(ticker='GME', search_term='Depreciation')
    2. Request specific data: get_filing_content(ticker='GME', specific_metrics=['NetIncomeLoss', 'InterestExpense', ...])
    3. Calculate TTM using 5 historical values per metric
    """
    result = await tools.get_filing_content(ticker, filing_type, get_full_content, specific_metrics)
    return result if result else {"error": f"Failed to fetch {filing_type} for {ticker}"}

async def run_self_test() -> dict:
    """Run comprehensive self-test of all SEC-AI tools"""
    return await tools.run_self_test()

# For direct Python usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Example usage
        tools_instance = Tools()
        
        print("SEC-AI Tools - Example Usage")
        print("=" * 50)
        
        # Test API status
        status = await tools_instance.get_sec_api_status()
        print(f"SEC API Status: {status}")
        
        # Get Apple's latest 10-K
        result = await tools_instance.get_latest_10k("AAPL")
        print(f"\nApple's Latest 10-K: {result}")
        
        # Run self-test
        test_results = await tools_instance.run_self_test()
        print(f"\nSelf-Test Results: {test_results['summary']}")
    
    asyncio.run(main())
