# Cross-Project Wisdom

Total: **8**

## `CW-DERIVATIVES-PRICING-001` — Strict input validation before financial calculations
**From**: FinancePy, QuantLib-SWIG · **Applicable to**: derivatives-pricing

Both FinancePy and QuantLib-SWIG enforce strict validation of all input parameters before any financial computation. FinancePy validates day count types, date arguments, tolerance parameters, and max iterations. QuantLib-SWIG validates exercise types and swap direction enums. This pattern prevents corrupted calculations and provides clear error messages. Apply this pattern by validating all inputs at function entry points.

## `CW-DERIVATIVES-PRICING-002` — Bootstrap requires ordered instrument calibration
**From**: FinancePy, QuantLib-SWIG · **Applicable to**: derivatives-pricing

Both FinancePy and QuantLib-SWIG require calibration instruments to be provided in strict maturity order for curve bootstrapping. FinancePy enforces monotonically increasing time points and validates instrument sequencing (deposits before FRAs before swaps). QuantLib-SWIG uses bootstrap helpers (DepositRateHelper, FraRateHelper, SwapRateHelper) that assume ordered inputs. This ensures the bootstrap algorithm solves for discount factors at mathematically correct time points.

## `CW-DERIVATIVES-PRICING-003` — Handle pattern for lazy evaluation chains
**From**: QuantLib-SWIG · **Applicable to**: derivatives-pricing

QuantLib-SWIG requires wrapping market data (quotes, term structures) in Handle objects to enable lazy evaluation and automatic recalculation. QuoteHandle for market quotes and Handle for term structures enable the observer pattern. When market data updates, all dependent instruments automatically recalculate. This pattern is essential for live pricing systems where prices must reflect current market conditions.

## `CW-DERIVATIVES-PRICING-004` — Parameter composition requires fixed ordering and partitioning
**From**: arch · **Applicable to**: derivatives-pricing

arch enforces a strict parameter composition pattern where mean, volatility, and distribution parameters must be concatenated in fixed order with explicit offset partitioning. The offsets array partitions the unified parameter vector into components. This pattern prevents parameter assignment errors that would corrupt model components. Apply this when composing financial models from multiple sub-components.

## `CW-DERIVATIVES-PRICING-005` — Strict mathematical constraint enforcement
**From**: arch, py_vollib · **Applicable to**: derivatives-pricing

Both arch and py_vollib enforce strict mathematical constraints: arch enforces volatility model stationarity constraints (A.dot(params) - b >= 0) for SLSQP optimization; py_vollib validates implied volatility is positive and option prices within intrinsic/maximum bounds. Violating these constraints produces mathematically invalid results. Always enforce domain constraints on all financial model parameters.

## `CW-DERIVATIVES-PRICING-006` — Forward price adjustment for dividend yield in BSM
**From**: py_vollib · **Applicable to**: derivatives-pricing

py_vollib demonstrates the correct BSM implementation: compute forward price F = S * exp((r-q)*t) to adjust for continuous dividend yield before passing to the pricing engine. This pattern is essential for all options on dividend-paying assets. Forgetting the dividend adjustment causes systematic mispricing for the entire equity derivatives book.

## `CW-DERIVATIVES-PRICING-007` — Monotonicity validation for interpolation arrays
**From**: FinancePy · **Applicable to**: derivatives-pricing

FinancePy enforces strictly monotonically increasing time arrays before interpolation operations. This prevents undefined behavior at crossing times and ensures each time point maps to exactly one discount factor. Apply this validation whenever implementing interpolation over financial time series (discount curves, volatility surfaces, forward rates).

## `CW-DERIVATIVES-PRICING-008` — Production vs reference implementation selection
**From**: py_vollib · **Applicable to**: derivatives-pricing

py_vollib explicitly distinguishes between ref_python (slow, educational) and production (fast, C-based lets_be_rational) implementations. Using the reference implementation in production causes 10-100x performance degradation. Always select the appropriate implementation tier based on use case requirements—reference for testing/education, optimized for production trading systems.
