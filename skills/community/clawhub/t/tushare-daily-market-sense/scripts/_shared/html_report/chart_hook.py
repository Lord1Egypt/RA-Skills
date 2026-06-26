"""Chart contribution unit. Each ``ChartHook`` is one chart bundle a skill
attaches to the HTML report: a JSON ``payload`` (merged into the page's
``<script id="chart-data">`` envelope under ``hook.name``) plus a ``js`` body
that draws the chart at view time.

The JS body runs inside an IIFE wrapped by the builder. It can read its own
payload via ``window.__chartData["<name>"]`` (a convenience) or by parsing
``document.getElementById("chart-data").textContent`` directly.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ChartHook:
    name: str
    payload: Any
    js: str
