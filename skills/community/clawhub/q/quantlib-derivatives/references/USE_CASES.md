# Known Use Cases (KUC)

Total: **35**

## `KUC-101`
**Source**: `Python/test/test_marketelements.py`

Verifies that market quotes (SimpleQuote) properly notify registered observers when their values change, ensuring reactive pricing systems work correctly.

## `KUC-102`
**Source**: `Python/test/test_americanquantooption.py`

Tests finite difference method pricing for American quanto options, which have payoff dependent on both equity and foreign exchange movements.

## `KUC-103`
**Source**: `Python/test/test_basket_option.py`

Validates pricing of basket options involving multiple underlying assets and spread options, which are used for correlation trading and cross-asset strategies.

## `KUC-104`
**Source**: `Python/test/test_cms.py`

Tests CMS (Constant Maturity Swap) pricing engines that handle swap-rate based coupons, used in structured products and interest rate derivatives.

## `KUC-105`
**Source**: `Python/test/test_bonds.py`

Tests fixed rate bond pricing with scheduled coupon payments, used for government and corporate bond valuation and analysis.

## `KUC-106`
**Source**: `Python/test/test_bondfunctions.py`

Tests bond analytics functions including yield calculation, duration, convexity, and other fixed income risk measures.

## `KUC-107`
**Source**: `Python/test/test_termstructures.py`

Tests yield term structure creation, interpolation methods, and forward rate calculations essential for pricing each interest rate derivatives.

## `KUC-108`
**Source**: `Python/test/test_options.py`

Tests finite difference method pricing for options under Heston Hull-White stochastic volatility model, capturing equity-interest rate correlation.

## `KUC-109`
**Source**: `Python/test/test_calendars.py`

Tests joint calendar functionality combining multiple country calendars to determine valid business days for cross-border trading.

## `KUC-110`
**Source**: `Python/test/test_sabr.py`

Tests SABR (Stochastic Alpha, Beta, Rho) volatility model for smile fitting in interest rate and FX markets.

## `KUC-111`
**Source**: `Python/test/test_volatilities.py`

Tests swaption volatility term structure handling for interest rate derivatives pricing and calibration.

## `KUC-112`
**Source**: `Python/test/test_futures.py`

Tests perpetual futures pricing models used in cryptocurrency exchanges for continuous futures contracts without expiration.

## `KUC-113`
**Source**: `Python/test/test_currencies.py`

Tests currency class construction including default, standard (EUR), and bespoke currencies for multi-currency instrument pricing.

## `KUC-114`
**Source**: `Python/test/test_swap.py`

Tests interest rate swap pricing engines with historical rate fixings, used for vanilla IRS valuation and curve bootstrapping validation.

## `KUC-115`
**Source**: `Python/test/test_integrals.py`

Tests numerical integration methods used in pricing analytics for computing expected values and option premiums.

## `KUC-116`
**Source**: `Python/test/test_swaption.py`

Tests swaption pricing with various settlement types and calculates Greeks for interest rate option risk management.

## `KUC-117`
**Source**: `Python/test/test_ode.py`

Tests ordinary differential equation solvers (Runge-Kutta) used in pricing models for term structure evolution and boundary value problems.

## `KUC-118`
**Source**: `Python/test/test_slv.py`

Tests Stochastic Local Volatility (SLV) process generation combining Heston stochastic vol with local vol for more accurate calibration.

## `KUC-119`
**Source**: `Python/test/test_coupons.py`

Tests Ibor index coupon construction and floating leg generation for interest rate derivatives including rate averaging methods.

## `KUC-120`
**Source**: `Python/test/test_fdm.py`

Tests finite difference method meshers and solvers used for PDE-based option pricing across various boundary conditions.

## `KUC-121`
**Source**: `Python/test/test_daycounters.py`

Tests day count conventions including Business252 used for interest accrual calculations in Brazilian and other markets.

## `KUC-122`
**Source**: `Python/test/test_ratehelpers.py`

Tests rate helpers used in bootstrapping yield curves from market instruments like deposits, futures, and swaps.

## `KUC-123`
**Source**: `Python/test/test_fxforward.py`

Tests FX forward pricing with cross-currency discount curves, used for currency hedging and FX derivative valuation.

## `KUC-124`
**Source**: `Python/test/test_solvers1d.py`

Tests root-finding algorithms (Brent, Bisection, Secant, etc.) used for implied volatility calculation and calibration.

## `KUC-125`
**Source**: `Python/test/test_extrapolation.py`

Tests Richardson extrapolation for improving numerical accuracy, used in pricing model convergence acceleration.

## `KUC-126`
**Source**: `Python/test/test_equityindex.py`

Tests equity index valuation with dividend yields and interest rates, used for index derivative pricing.

## `KUC-127`
**Source**: `Python/test/test_instruments.py`

Tests instrument observability pattern for stocks, ensuring market data changes properly propagate through to instrument valuations.

## `KUC-128`
**Source**: `Python/test/test_linear_algebra.py`

Tests array and matrix operations used throughout QuantLib for numerical computations in pricing and risk models.

## `KUC-129`
**Source**: `Python/test/test_date.py`

Tests date arithmetic operations including periods, schedules, and date adjustments used throughout financial calculations.

## `KUC-130`
**Source**: `Python/test/test_blackformula.py`

Tests Black-Scholes-Merton formula implementation for vanilla option pricing, the foundational model for equity derivatives.

## `KUC-131`
**Source**: `Python/test/test_inflation.py`

Tests inflation term structures and CPI index handling for inflation-linked derivatives like inflation swaps and bonds.

## `KUC-132`
**Source**: `Python/test/test_money.py`

Tests Money class comparison and arithmetic operations for proper handling of multi-currency quantities.

## `KUC-133`
**Source**: `Python/test/test_capfloor.py`

Tests cap and floor pricing engines for interest rate risk management, used for hedging rate movements and callable structures.

## `KUC-134`
**Source**: `Python/test/test_settings.py`

Tests global settings management including evaluation date control and fixing behavior configuration.

## `KUC-135`
**Source**: `Python/test/test_iborindex.py`

Tests Ibor index fixing management and historical fixings handling for floating rate instruments.
