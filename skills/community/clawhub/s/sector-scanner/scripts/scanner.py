from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Callable

from models import SectorDefinition, SectorScanResult, StockDefinition
from scorer import heat_label, HEAT_LABEL_CN, score_stock
from tdx_client import TdxClient, TdxServer

ProgressCallback = Callable[[int, int, str], None]


class ScanEngine:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parent
        self.config_dir = self.base_dir / "config"
        self.settings = self._read_json(self.config_dir / "settings.json", {})
        self.sectors = self._load_sectors()

    def _read_json(self, path: Path, default: object) -> object:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def _load_sectors(self) -> list[SectorDefinition]:
        payload = self._read_json(self.config_dir / "sectors.json", [])
        sectors: list[SectorDefinition] = []
        for item in payload:
            stocks = [StockDefinition(code=s["code"], name=s["name"]) for s in item["stocks"]]
            sectors.append(
                SectorDefinition(
                    id=item["id"],
                    name=item["name"],
                    emoji=item.get("emoji", ""),
                    stocks=stocks,
                )
            )
        return sectors

    def scan(
        self,
        sector_ids: list[str] | None = None,
        progress_callback: ProgressCallback | None = None,
    ) -> list[SectorScanResult]:
        selected = [sector for sector in self.sectors if not sector_ids or sector.id in sector_ids]
        if not selected:
            return []

        total = self._stock_count(selected)
        if progress_callback:
            progress_callback(0, total, "Connecting to TDX market data server")

        return self._scan_tdx(selected, progress_callback)

    def _scan_tdx(
        self,
        sectors: list[SectorDefinition],
        progress_callback: ProgressCallback | None,
    ) -> list[SectorScanResult]:
        servers = [
            TdxServer(
                name=str(item.get("name", item.get("host", item.get("ip", "TDX")))),
                host=str(item.get("host", item.get("ip", ""))),
                port=int(item.get("port", 7709)),
            )
            for item in self.settings.get("tdx_servers", [])
            if item.get("host") or item.get("ip")
        ]
        if not servers:
            raise RuntimeError("settings.json has no TDX servers configured")

        timeout = int(self.settings.get("scan_timeout_seconds", 5))
        retry_count = int(self.settings.get("retry_count", 3))
        current = 0
        results: list[SectorScanResult] = []

        if progress_callback:
            progress_callback(0, self._stock_count(sectors), "Connecting to TDX server")

        with TdxClient(servers, timeout=timeout, retry_count=retry_count) as client:
            total = self._stock_count(sectors)
            if not total:
                raise RuntimeError("No stocks to scan")

            for sector in sectors:
                if progress_callback:
                    progress_callback(current, total, f"Fetching quotes for {sector.name}")
                quotes = client.get_quotes(sector.stocks)
                stock_scores = []
                errors: list[str] = []
                for stock in sector.stocks:
                    current += 1
                    if progress_callback:
                        progress_callback(current, total, f"Scanning {sector.name} / {stock.name}")

                    quote = quotes.get(stock.code)
                    if quote is None:
                        errors.append(f"{stock.code} {stock.name}: quote missing")
                        continue
                    bars = []
                    try:
                        bars = client.get_bars(stock)
                    except Exception as exc:
                        errors.append(f"{stock.code} {stock.name}: kline failed: {exc}")
                    stock_scores.append(score_stock(quote, bars))

                results.append(
                    self._build_sector_result(
                        sector=sector,
                        stocks=stock_scores,
                        source=client.connected_server.name if client.connected_server else "tdx",
                        errors=errors,
                    )
                )
        return self._sort_results(results)

    def _build_sector_result(
        self,
        sector: SectorDefinition,
        stocks: list,
        source: str,
        errors: list[str],
    ) -> SectorScanResult:
        if not stocks:
            return SectorScanResult(
                id=sector.id,
                name=sector.name,
                emoji=sector.emoji,
                average_score=0.0,
                heat_label="no_data",
                flow_label="no_data",
                flow_level=0,
                red_count=0,
                total_count=len(sector.stocks),
                up_ratio=0.0,
                avg_pct_chg=0.0,
                stocks=[],
                scanned_at=datetime.now(),
                source=source,
                errors=errors,
            )

        average_score = mean(stock.score for stock in stocks)
        red_count = sum(1 for stock in stocks if stock.pct_chg > 0)
        avg_pct_chg = mean(stock.pct_chg for stock in stocks)
        flow_level = round(mean(stock.flow_level for stock in stocks))
        flow_label = self._sector_flow_label(flow_level)
        heat_key = heat_label(average_score)
        return SectorScanResult(
            id=sector.id,
            name=sector.name,
            emoji=sector.emoji,
            average_score=round(average_score, 1),
            heat_label=HEAT_LABEL_CN.get(heat_key, heat_key),
            flow_label=flow_label,
            flow_level=flow_level,
            red_count=red_count,
            total_count=len(stocks),
            up_ratio=red_count / len(stocks),
            avg_pct_chg=round(avg_pct_chg, 2),
            stocks=sorted(stocks, key=lambda item: item.score, reverse=True),
            scanned_at=datetime.now(),
            source=source,
            errors=errors,
        )

    def _sector_flow_label(self, level: int) -> str:
        if level >= 2:
            return "主力流入"
        if level == 1:
            return "微流入"
        if level <= -2:
            return "主力流出"
        if level == -1:
            return "微流出"
        return "平衡"

    def _sort_results(self, results: list[SectorScanResult]) -> list[SectorScanResult]:
        return sorted(results, key=lambda item: item.average_score, reverse=True)

    def _stock_count(self, sectors: list[SectorDefinition]) -> int:
        return sum(len(sector.stocks) for sector in sectors)
