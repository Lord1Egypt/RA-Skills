"""
Tariff Search Library – rewritten client for TurtleClassify API

Provides functions to classify products and fetch tariff information.
All logic mirrors the original implementation, but identifiers and comments have been renamed.
"""

import json
import sys
import time
import random
from typing import List, Dict, Any, Tuple, Union
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import os

# Ensure the repository's root is on the Python path for imports
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

class TariffSearch:
    """Client for accessing the TurtleClassify tariff service.

    Core responsibilities:
    * Validate incoming product dictionaries
    * Batch‑process up to 50 items concurrently while respecting a 10 QPS ceiling
    * Translate the API's nested JSON into a flat structure convenient for pandas/DataFrame use
    """

    BASE_URL = "https://www.accio.com"
    MAX_BATCH = 50
    MAX_TOTAL = 100

    def __init__(self, base_url: str = "", timeout: int = 300):
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout

    # ---------------------------------------------------------------------
    # Public entry point
    # ---------------------------------------------------------------------
    def search_tariff(self, items: List[Dict[str, Any]], return_type: str = "list") -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Query tariff data for a collection of products.

        Parameters
        ----------
        items: List[Dict]
            Each entry must contain ``originCountryCode``, ``destinationCountryCode`` and ``productName``.
        return_type: str, optional
            ``"list"`` (default) yields a flat list ready for CSV export.
            ``"detail"`` returns a richer payload with processing metadata.
        """
        start = time.time()
        validated = []
        for idx, prod in enumerate(items):
            ok, msg = self._check_product(prod)
            if not ok:
                if return_type == "detail":
                    return {"success": False, "error": f"Item {idx+1}: {msg}", "results": []}
                print(f"[WARN] Item {idx+1} skipped – {msg}")
            else:
                validated.append(prod)

        try:
            raw = self._process_items(validated)
            elapsed = time.time() - start
            if return_type == "detail":
                return {
                    "success": True,
                    "results": raw,
                    "processing_time": elapsed,
                    "raw_response": raw,
                }
            # Default – flatten for easy consumption
            flat = []
            for i, res in enumerate(raw):
                src = validated[i] if i < len(validated) else {}
                flat.append(self._flatten(res.get("data", {}), src))
            return flat
        except Exception as exc:
            print(f"[ERROR] search_tariff failed: {exc}")
            if return_type == "detail":
                return {"success": False, "error": str(exc), "results": []}
            return []

    # ---------------------------------------------------------------------
    # Internals
    # ---------------------------------------------------------------------
    def _check_product(self, prod: Dict[str, Any]) -> Tuple[bool, str]:
        """Ensure mandatory fields are present and sensible."""
        for field in ("originCountryCode", "destinationCountryCode", "productName"):
            if not prod.get(field):
                return False, f"Missing {field}"
        digit = prod.get("digit")
        if digit is not None and digit not in (8, 10):
            return False, "digit must be 8 or 10"
        prod.setdefault("source", "alibaba")
        return True, ""

    def _call_api(self, prod: Dict[str, Any]) -> Dict[str, Any]:
        """POST request to the TurtleClassify endpoint and unwrap the nested JSON."""
        endpoint = f"{self.base_url.rstrip('/')}/api/turtle/classify"
        payload = {
            "source": prod.get("source", "alibaba"),
            "originCountryCode": prod["originCountryCode"],
            "destinationCountryCode": prod["destinationCountryCode"],
            "productName": prod["productName"],
        }
        # bubble up any optional values
        for opt in ("digit", "productId", "productSource", "productCategoryId", "productCategoryName",
                    "productProperties", "productKeywords", "channel"):
            if opt in prod:
                payload[opt] = prod[opt]
        try:
            resp = requests.post(endpoint, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            outer = resp.json()
            if not outer.get("success"):
                return {}
            inner_raw = outer.get("data", "")
            if isinstance(inner_raw, str):
                inner = json.loads(inner_raw)
            else:
                inner = inner_raw
            if not inner.get("success"):
                return {}
            return {"data": inner.get("data", {}), "raw": inner}
        except Exception as e:
            print(f"[ERR] API call issue: {e}")
            return {}

    def _process_batch(self, batch: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Concurrent processing of a batch respecting QPS limits."""
        n = len(batch)
        max_delay = n / 10.0  # keep average rate ≤10 QPS
        results = [None] * n
        with ThreadPoolExecutor(max_workers=self.MAX_BATCH) as pool:
            futures = {}
            for i, itm in enumerate(batch):
                delay = random.uniform(0, max_delay)
                futures[pool.submit(self._delayed_call, itm, delay)] = i
            for fut in as_completed(futures):
                idx = futures[fut]
                try:
                    results[idx] = fut.result()
                except Exception as exc:
                    print(f"[WARN] Item {idx} failed: {exc}")
                    results[idx] = {}
        return results

    def _delayed_call(self, prod: Dict[str, Any], pause: float) -> Dict[str, Any]:
        if pause:
            time.sleep(pause)
        return self._call_api(prod)

    def _process_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Split the full list into chunks and run each through ``_process_batch``."""
        if len(items) <= self.MAX_BATCH:
            return self._process_batch(items)
        out = []
        for start in range(0, len(items), self.MAX_BATCH):
            out.extend(self._process_batch(items[start:start + self.MAX_BATCH]))
        return out[: self.MAX_TOTAL]

    def _flatten(self, data: Dict[str, Any], src: Dict[str, Any]) -> Dict[str, Any]:
        """Transform API payload into a single‑level dictionary suitable for CSV/DF.

        Missing fields are populated with sensible defaults.
        """
        hs = data.get("hscodeStr") or data.get("hscodeInfo", {}).get("hscode", "")
        desc = data.get("hscodeDesc") or data.get("hscodeInfo", {}).get("descriptionEn", "")
        rate_raw = data.get("tariffRate", 0)
        try:
            rate = float(rate_raw) if isinstance(rate_raw, str) else rate_raw
        except ValueError:
            rate = 0.0
        formula = data.get("tariffFormula") or f"Base Rate: {rate}%"
        calc_type = data.get("tariffCalculateType") or "AD_VALOREM"
        return {
            "hsCode": hs,
            "hsCodeDescription": desc,
            "tariffRate": rate,
            "tariffFormula": formula,
            "tariffCalculateType": calc_type,
            "originCountryCode": src.get("originCountryCode", ""),
            "destinationCountryCode": src.get("destinationCountryCode", ""),
            "productName": src.get("productName", ""),
            "calculationDetails": data,
        }

# End of rewritten client
""