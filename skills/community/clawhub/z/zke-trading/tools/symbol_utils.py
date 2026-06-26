from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional

from tools.common import normalize_symbol, format_decimal_by_precision


class SymbolNotFoundError(Exception):
    pass


class SymbolValidationError(Exception):
    pass


class SpotSymbolRegistry:
    def __init__(self, symbols_payload: Dict[str, Any]):
        raw_symbols = symbols_payload.get("symbols", [])
        self.raw_symbols: List[Dict[str, Any]] = raw_symbols

        self.by_api_symbol: Dict[str, Dict[str, Any]] = {}
        self.by_display_symbol: Dict[str, Dict[str, Any]] = {}
        self.by_base_quote: Dict[str, Dict[str, Any]] = {}

        for item in raw_symbols:
            api_symbol = str(item.get("symbol", "")).strip().lower()
            base_asset = str(item.get("baseAssetName") or item.get("baseAsset") or "").strip().upper()
            quote_asset = str(item.get("quoteAssetName") or item.get("quoteAsset") or "").strip().upper()

            symbol_name = str(item.get("SymbolName") or item.get("symbolName") or "").strip().upper()
            if not symbol_name and base_asset and quote_asset:
                symbol_name = f"{base_asset}/{quote_asset}"

            merged = f"{base_asset}{quote_asset}"
            compact_display = symbol_name.replace("/", "").replace(" ", "")

            if api_symbol:
                self.by_api_symbol[api_symbol] = item

            if compact_display:
                self.by_display_symbol[compact_display] = item

            if merged:
                self.by_base_quote[merged] = item

    def resolve(self, symbol: str) -> Dict[str, Any]:
        raw = symbol.strip()
        lower = raw.lower()
        upper = normalize_symbol(raw).replace("/", "").replace(" ", "")

        if lower in self.by_api_symbol:
            return self.by_api_symbol[lower]

        if upper in self.by_display_symbol:
            return self.by_display_symbol[upper]

        if upper in self.by_base_quote:
            return self.by_base_quote[upper]

        raise SymbolNotFoundError(f"找不到交易对: {symbol}")

    def get_api_symbol(self, symbol: str) -> str:
        item = self.resolve(symbol)
        return str(item.get("symbol", "")).strip().lower()

    def get_display_symbol(self, symbol: str) -> str:
        item = self.resolve(symbol)

        symbol_name = str(item.get("SymbolName") or item.get("symbolName") or "").strip().upper()
        if symbol_name:
            return symbol_name

        base_asset = str(item.get("baseAssetName") or item.get("baseAsset") or "").strip().upper()
        quote_asset = str(item.get("quoteAssetName") or item.get("quoteAsset") or "").strip().upper()

        if base_asset and quote_asset:
            return f"{base_asset}/{quote_asset}"

        return str(item.get("symbol", "")).strip().upper()

    def get_meta(self, symbol: str) -> Dict[str, Any]:
        return self.resolve(symbol)

    def validate_order(
        self,
        symbol: str,
        volume: str,
        price: Optional[str],
        order_type: str
    ) -> Dict[str, Any]:
        meta = self.resolve(symbol)

        quantity_precision = int(meta.get("quantityPrecision", 8) or 8)
        price_precision = int(meta.get("pricePrecision", 8) or 8)

        limit_volume_min = str(meta.get("limitVolumeMin", "0") or "0")
        limit_price_min = str(meta.get("limitPriceMin", "0") or "0")
        limit_amount_min = str(meta.get("limitAmountMin", "0") or "0")

        try:
            volume_dec = Decimal(str(volume))
        except (InvalidOperation, ValueError):
            raise SymbolValidationError("下单数量格式无效。")

        if volume_dec <= 0:
            raise SymbolValidationError("下单数量必须大于 0。")

        if volume_dec < Decimal(limit_volume_min):
            raise SymbolValidationError(
                f"下单数量过小。当前交易对最小下单量为 {limit_volume_min}。"
            )

        fixed_volume = format_decimal_by_precision(str(volume), quantity_precision)
        if Decimal(fixed_volume) != volume_dec:
            raise SymbolValidationError(
                f"下单数量精度过高。该交易对数量精度为 {quantity_precision} 位。"
            )

        fixed_price = None
        if str(order_type).strip().upper() == "LIMIT":
            if price is None:
                raise SymbolValidationError("LIMIT 订单必须提供 price。")

            try:
                price_dec = Decimal(str(price))
            except (InvalidOperation, ValueError):
                raise SymbolValidationError("订单价格格式无效。")

            if price_dec <= 0:
                raise SymbolValidationError("订单价格必须大于 0。")

            if price_dec < Decimal(limit_price_min):
                raise SymbolValidationError(
                    f"订单价格过低。当前交易对最小价格为 {limit_price_min}。"
                )

            fixed_price = format_decimal_by_precision(str(price), price_precision)
            if Decimal(fixed_price) != price_dec:
                raise SymbolValidationError(
                    f"订单价格精度过高。该交易对价格精度为 {price_precision} 位。"
                )

            if Decimal(limit_amount_min) > 0:
                amount = Decimal(fixed_price) * Decimal(fixed_volume)
                if amount < Decimal(limit_amount_min):
                    raise SymbolValidationError(
                        f"下单金额过小。当前交易对最小下单金额为 {limit_amount_min}。"
                    )

        return {
            "api_symbol": str(meta.get("symbol", "")).strip().lower(),
            "display_symbol": self.get_display_symbol(symbol),
            "quantity_precision": quantity_precision,
            "price_precision": price_precision,
            "fixed_volume": fixed_volume,
            "fixed_price": fixed_price,
            "meta": meta,
        }
