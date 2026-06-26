METRIC_INFO_KEYS = {
    "trailing_pe": ("trailingPE",),
    "forward_pe": ("forwardPE",),
    "peg_ratio": ("pegRatio",),
    "price_to_sales": ("priceToSalesTrailing12Months",),
    "price_to_book": ("priceToBook",),
    "ev_to_ebitda": ("enterpriseToEbitda",),
    "gross_margin": ("grossMargins",),
    "operating_margin": ("operatingMargins",),
    "profit_margin": ("profitMargins",),
    "return_on_equity": ("returnOnEquity",),
    "return_on_assets": ("returnOnAssets",),
    "revenue_growth": ("revenueGrowth",),
    "earnings_growth": ("earningsGrowth",),
    "cash": ("totalCash",),
    "debt": ("totalDebt",),
    "debt_to_equity": ("debtToEquity",),
    "current_ratio": ("currentRatio",),
    "free_cash_flow": ("freeCashflow",),
    "dividend_yield": ("dividendYield",),
    "payout_ratio": ("payoutRatio",),
    "target_mean_price": ("targetMeanPrice",),
    "recommendation": ("recommendationKey",),
}

BALANCE_SHEET_CASH_LABELS = [
    "Cash And Cash Equivalents",
    "Cash Cash Equivalents And Short Term Investments",
    "Cash",
]

BALANCE_SHEET_DEBT_LABELS = ["Total Debt", "Long Term Debt", "Current Debt"]
CASHFLOW_FCF_LABELS = ["Free Cash Flow"]
INCOME_STATEMENT_NET_INCOME_LABELS = ["Net Income", "Net Income Common Stockholders"]
INCOME_STATEMENT_REVENUE_LABELS = ["Total Revenue", "Operating Revenue"]

HIGHLIGHT_THRESHOLDS = {
    "gross_margin": 45,
    "operating_margin": 20,
    "revenue_growth": 10,
    "earnings_growth": 10,
    "current_ratio": 1.5,
    "return_on_equity": 15,
    "dividend_yield": 2,
}

WATCH_THRESHOLDS = {
    "profit_margin": 5,
    "debt_to_equity": 150,
    "current_ratio": 1,
    "forward_pe": 30,
}
