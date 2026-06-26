# Anti-Patterns (Cross-Project)

Total: **15**

## FinancePy (finance-bp-101) (3)

### `AP-DERIVATIVES-PRICING-003` — Negative discount factors passed to log-domain interpolation <sub>(high)</sub>

When Numba-jitted interpolation functions perform log transformation on discount factors, negative or zero values cause domain errors. This occurs because log(-x) and log(0) are mathematically undefined. The consequence is runtime crashes in jitted functions and complete failure of discount curve interpolation, blocking all downstream pricing calculations.

### `AP-DERIVATIVES-PRICING-004` — Non-monotonic time points in discount curve interpolation <sub>(high)</sub>

Interpolation over non-monotonically increasing time points produces undefined behavior at crossing times, causing discount factors to be incorrectly computed where time values overlap. This corrupts the entire term structure because the bootstrap algorithm cannot determine which discount factor corresponds to which maturity. The consequence is incorrect present value calculations across all downstream products priced against the curve.

### `AP-DERIVATIVES-PRICING-005` — Bootstrap calibration instruments not in maturity order <sub>(high)</sub>

When building yield curves from market instruments (deposits, FRAs, swaps), the instruments must be provided in strictly increasing maturity order. Out-of-order instruments cause the bootstrap algorithm to solve for discount factors at incorrect time points, corrupting the entire term structure. The consequence is wrong forward rates and discount factors that propagate into all priced instruments.

## QuantLib-SWIG (finance-bp-123) (4)

### `AP-DERIVATIVES-PRICING-001` — Instrument NPV called without attached pricing engine <sub>(high)</sub>

Calling NPV() on a derivatives instrument without first calling setPricingEngine() returns uninitialized garbage values or throws null pointer exceptions. This occurs because the Instrument class relies on the attached PricingEngine to perform actual valuation logic. The consequence is silently incorrect pricing results that appear valid, potentially leading to bad trading decisions.

### `AP-DERIVATIVES-PRICING-006` — Option Exercise type mismatches VanillaOption constructor <sub>(high)</sub>

VanillaOption requires both a StrikedTypePayoff and a matching Exercise object. Using wrong Exercise type (e.g., AmericanExercise for European option) causes compilation failures in C++ or runtime errors in SWIG bindings. The consequence is the pricing system cannot initialize options, blocking all option pricing workflows.

### `AP-DERIVATIVES-PRICING-013` — Evaluation date not set before QuantLib term structure construction <sub>(medium)</sub>

QuantLib requires ql.Settings.instance().evaluationDate to be set before constructing yield term structures and instruments. Without an explicit evaluation date, the curve reference date becomes undefined, causing date calculations to fail or produce incorrect settlement dates. The consequence is wrong discount factors and NPV calculations across the entire portfolio.

### `AP-DERIVATIVES-PRICING-014` — Market quotes passed without QuoteHandle wrapper <sub>(medium)</sub>

QuantLib's observer pattern requires all market quotes to be wrapped in QuoteHandle before passing to rate helpers. Raw quote values bypass the observable notification mechanism, causing dependent instruments to never recalculate when market data updates. The consequence is stale pricing that doesn't reflect current market conditions.

## arch (finance-bp-124) (2)

### `AP-DERIVATIVES-PRICING-007` — NaN/inf values in ARCH model input data <sub>(high)</sub>

ARCH model estimation relies on recursive variance computations and scipy optimize. Non-finite input values (NaN, inf) cause optimizers to produce NaN results and recursive variance calculations to fail. The consequence is complete model estimation failure with meaningless outputs that appear valid, leading to incorrect volatility forecasts and risk misestimation.

### `AP-DERIVATIVES-PRICING-008` — ARCH parameter array concatenation in wrong order <sub>(high)</sub>

ARCHModel composes from three components (mean, volatility, distribution) and requires parameter arrays concatenated in fixed order: [mean_params, volatility_params, distribution_params]. Incorrect ordering causes _parse_parameters to assign wrong values to wrong components, producing mathematically invalid models (e.g., volatility parameters interpreted as distribution parameters). The consequence is invalid conditional variance forecasts.

## py_vollib (finance-bp-127) (6)

### `AP-DERIVATIVES-PRICING-002` — BSM forward price ignores dividend yield <sub>(high)</sub>

When calculating option prices on dividend-paying stocks using BSM, the forward price must be adjusted as F = S * exp((r-q)*t). Omitting the dividend yield adjustment (using F = S * exp(r*t)) causes systematic mispricing for all dividend-paying assets. The consequence is consistently wrong option prices that diverge from market prices, leading to arbitrage opportunities and trading losses.

### `AP-DERIVATIVES-PRICING-009` — Zero or negative time-to-expiration in option pricing <sub>(high)</sub>

Option pricing formulas (Black-Scholes, Black model) compute sqrt(t) in the denominator. Zero time causes division by zero; negative time produces NaN in d1/d2 calculations. The consequence is invalid option prices (NaN, inf) that break downstream Greeks calculations and hedging workflows.

### `AP-DERIVATIVES-PRICING-010` — Black model applies spot price instead of forward price <sub>(high)</sub>

The Black model is designed for options on futures/forwards and expects futures price F as input, not spot price S. Using spot directly causes incorrect pricing because the Black formula assumes the underlying follows geometric Brownian motion with drift equal to the risk-free rate (i.e., forward dynamics). The consequence is systematically wrong forward option prices.

### `AP-DERIVATIVES-PRICING-011` — Missing discount factor in Black model pricing <sub>(medium)</sub>

Black model pricing must apply time value discounting with deflater = exp(-r*t) to undiscounted option prices. Omitting the discount factor produces forward option prices that exceed their fair value by the risk-free compounding amount. The consequence is violation of time value of money principles and prices that cannot be used for fair valuation or hedging.

### `AP-DERIVATIVES-PRICING-012` — Invalid flag parameter ('c'/'p') passed to py_vollib without validation <sub>(medium)</sub>

py_vollib binary_flag dict only contains keys 'c' and 'p'. Passing any other flag value causes KeyError exception. The library lacks input validation and crashes on invalid inputs. The consequence is unhandled exceptions in production systems when flag values come from external sources with unexpected formats.

### `AP-DERIVATIVES-PRICING-015` — Implied volatility computed without proper bounds validation <sub>(medium)</sub>

When computing implied volatility, option prices outside theoretical bounds (below intrinsic value or above maximum) must raise appropriate exceptions. Returning invalid IV values (negative volatility or extreme values) violates mathematical definitions and leads to incorrect pricing, risk calculations, and hedging ratios. The consequence is systemic pricing errors across all vol-dependent derivatives.
