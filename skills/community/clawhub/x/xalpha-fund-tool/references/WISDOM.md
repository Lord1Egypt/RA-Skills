# Cross-Project Wisdom

Total: **10**

## `CW-PORTFOLIO-ANALYTICS-001` — Defensive zero-division guards with explicit handling
**From**: finance-bp-066--wealthbot, finance-bp-082--stock-screener, finance-bp-093--PyPortfolioOpt · **Applicable to**: portfolio-analytics

Always guard division operations with explicit zero-value checks before executing. In price ratio calculations, filter out securities where old_price is zero before calling getPricesDiff. In composite score calculations, guard against total_weight of zero and return 0.0 for empty input lists. This prevents NaN/infinity propagation that corrupts downstream calculations and crashes pipelines.

## `CW-PORTFOLIO-ANALYTICS-002` — Covariance matrix positive-semidefiniteness verification
**From**: finance-bp-093--PyPortfolioOpt, finance-bp-117--Riskfolio-Lib · **Applicable to**: portfolio-analytics

Always verify covariance matrix is positive-semidefinite before passing to CVXPY optimization. Apply eigenvalue clipping if violated, as non-PSD matrices cause Cholesky decomposition failures. Both PyPortfolioOpt and Riskfolio-Lib enforce this constraint to prevent optimizer from finding mathematically invalid solutions or crashing entirely.

## `CW-PORTFOLIO-ANALYTICS-003` — Geometric compounding for cumulative returns
**From**: finance-bp-068--xalpha, finance-bp-106--pyfolio-reloaded, finance-bp-107--empyrical-reloaded · **Applicable to**: portfolio-analytics

Compute cumulative returns using geometric compounding via cumprod(1 + returns), never arithmetic cumulation via cumsum. Arithmetic cumulative sum overstates gains and understates losses, causing cumulative returns to diverge significantly from actual portfolio performance over volatile periods. This principle applies to total return index construction and any cumulative performance calculation.

## `CW-PORTFOLIO-ANALYTICS-004` — Temporal shift enforcement to prevent look-ahead bias
**From**: finance-bp-108--finmarketpy, finance-bp-106--pyfolio-reloaded · **Applicable to**: portfolio-analytics

Enforce proper temporal shifting in signal generation and position calculations. Use shift(-1) for exit signals to prevent look-ahead bias, and shift(1) when estimating intraday positions from EOD data. Forward-fill carry data and backward-fill only old data gaps, never forward-fill spot prices. Violations cause live trading returns to diverge from backtested results.

## `CW-PORTFOLIO-ANALYTICS-005` — DCP-compliant convex optimization construction
**From**: finance-bp-093--PyPortfolioOpt, finance-bp-117--Riskfolio-Lib · **Applicable to**: portfolio-analytics

Use only DCP-compliant convex objectives and constraints in CVXPY. Provide constraints as callable functions accepting weight variables, use valid bounds formats matching n_assets length, and verify target parameters (volatility, return) are within feasible ranges. Non-convex or infeasible problems fail with DCPError or OptimizationError, preventing optimization entirely.

## `CW-PORTFOLIO-ANALYTICS-006` — Correct Sharpe ratio formula with risk-free rate subtraction
**From**: finance-bp-107--empyrical-reloaded, finance-bp-118--FinanceToolkit · **Applicable to**: portfolio-analytics

Calculate Sharpe ratio using (mean returns - risk_free) / std(returns) * sqrt(annualization) with sample standard deviation (ddof=1). Subtract risk-free rate from asset returns before dividing by volatility. Incorrect Sharpe ratio calculation produces misleading risk-adjusted return estimates, causing poor investment decisions based on faulty performance attribution.

## `CW-PORTFOLIO-ANALYTICS-007` — Immutable FIFO position tracking with chronological ordering
**From**: finance-bp-068--xalpha, finance-bp-066--wealthbot · **Applicable to**: portfolio-analytics

Maintain FIFO position tracking with strictly increasing date order for position entries. Use copy() function to create independent copies before mutating remtable to avoid side effects. Enforce chronological ordering in sell operations to ensure correct cost basis and holding period calculation, particularly important for funds with tiered fees by holding period.

## `CW-PORTFOLIO-ANALYTICS-008` — Validation at system boundaries with descriptive errors
**From**: finance-bp-082--stock-screener, finance-bp-093--PyPortfolioOpt, finance-bp-117--Riskfolio-Lib · **Applicable to**: portfolio-analytics

Enforce validation at system boundaries with descriptive error messages. Validate expected returns matches covariance matrix dimensions, score values are within [0, 100], confidence values within [0, 1], and required DataFrame columns are present. Invalid inputs should raise ValueError with descriptive messages listing valid options to prevent silent failures or corrupted calculations.

## `CW-PORTFOLIO-ANALYTICS-009` — Decimal rounding for monetary calculations
**From**: finance-bp-068--xalpha, finance-bp-107--empyrical-reloaded · **Applicable to**: portfolio-analytics

Use Decimal with explicit rounding (myround) for each monetary calculation to avoid floating-point errors that cause share miscalculation and incorrect cost basis. This prevents rounding errors from propagating to XIRR and portfolio valuation calculations. Direct floating-point operations in financial calculations accumulate errors that become material over many transactions.

## `CW-PORTFOLIO-ANALYTICS-010` — Cash flow sign convention enforcement
**From**: finance-bp-106--pyfolio-reloaded, finance-bp-068--xalpha · **Applicable to**: portfolio-analytics

Mark cash outflows as negative and cash inflows as positive in cftable. Incorrect cash flow signs cause NPV calculation to invert, producing negative returns for profitable trades and vice versa. Verify sum of round trip PnLs equals total realized transaction dollars to catch sign convention errors before they corrupt performance attribution.
