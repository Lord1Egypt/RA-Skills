# Balance Reference

## Scope

- Spot/futures balances
- Positions and position mode
- Margin visibility
- Account detail queries

## Read-Only Rule (P0)

- Do not execute order write scripts from balance workflows.

## Account Type to Script Mapping (Binance)

### PM Account

- Spot balance: `get_account_balance.py`
- Spot margin (cross-margin detail): `get_cross_margin_account_detail.py`
- U-margined futures positions: `get_pm_positions.py`
- U-margined futures margin: `get_pm_margin.py`
- Coin-margined account/positions: `get_cm_account.py`
- Optional PM detail: `get_pv1_balance.py`

### Normal Account (Non-PM)

- Spot balance: `get_account_balance.py`
- Spot margin (cross-margin detail): `get_cross_margin_account_detail.py`
- U-margined futures positions: `get_fapi_positions.py`
- U-margined futures margin: `get_fapi_margin.py`
- Coin-margined account/positions: `get_dapi_account.py`

### Selection Rule

1. Check account type from `list_exchange_apis.py` (`isPm`).
2. If `isPm=true`, use PM scripts.
3. If `isPm=false`, use normal-account scripts.
4. For Binance spot margin on either account type, use `get_cross_margin_account_detail.py`.

## How To Query Spot Margin (Normal Account)

1. Get the normal account `binding-id` from `list_exchange_apis.py` (`isPm=false`).
2. Query spot margin (cross-margin) detail with `get_cross_margin_account_detail.py`.
3. Read `userAssets` for position/asset details and `borrowed`/`interest` for liabilities.

```bash
# 1) Find binding-id for normal account
python3 scripts/list_exchange_apis.py --exchange Binance --page 1 --page-size 50

# 2) Query spot margin positions/liabilities
python3 scripts/get_cross_margin_account_detail.py --binding-id <normal_account_binding_id>
```

## How To Query OKX Spot And Derivatives

1. Find the OKX account `binding-id` from `list_exchange_apis.py`.
2. Query spot/asset balances with `get_okx_balance.py`.
3. Query derivatives positions with `get_okx_positions.py`.
4. If needed, query max order size with `get_okx_account_max_size.py`.

```bash
# 1) Find OKX binding-id
python3 scripts/list_exchange_apis.py --exchange OKX --page 1 --page-size 50

# 2) Spot / asset balances
python3 scripts/get_okx_balance.py --binding-id <okx_binding_id>

# 3) Derivatives positions (SWAP/FUTURES/OPTION if returned by API)
python3 scripts/get_okx_positions.py --binding-id <okx_binding_id>

# 4) Optional: max order size check
python3 scripts/get_okx_account_max_size.py --binding-id <okx_binding_id> --inst-id BTC-USDT-SWAP --td-mode cross
```

## How To Query LTP Spot, Margin, And Derivatives

1. Find the LTP account `binding-id` from `list_exchange_apis.py`.
2. Query account-level balance/margin overview with `get_ltp_balance.py`.
3. Query portfolio-asset detail (spot assets + borrow/debt) with `get_ltp_portfolio_asset.py`.
4. Query derivatives positions with `get_ltp_positions.py`.

```bash
# 1) Find LTP binding-id
python3 scripts/list_exchange_apis.py --exchange LTP --page 1 --page-size 50

# 2) Account-level balance and margin overview
python3 scripts/get_ltp_balance.py --binding-id <ltp_binding_id>

# 3) Spot assets and margin debt detail
python3 scripts/get_ltp_portfolio_asset.py --binding-id <ltp_binding_id>

# 4) Derivatives positions
python3 scripts/get_ltp_positions.py --binding-id <ltp_binding_id>
```

### LTP Output Interpretation

- Spot balance:
  - Use `get_ltp_portfolio_asset.py` and read per-coin fields like `coin`, `available`, `balance`, `equity`.
- Margin balance/debt:
  - `get_ltp_balance.py`: account-level fields like `availableMargin`, `debtMargin`, `equity`, `riskRatio`.
  - `get_ltp_portfolio_asset.py`: coin-level fields like `borrow`, `debt`, `debtMargin`, `overdraw`.
- Derivatives positions:
  - `get_ltp_positions.py` fields `sym`, `positionQty`, `positionValue`, `positionMargin`, `unrealizedPnl`.

## How To Query Deribit Spot And Derivatives

1. Find the Deribit account `binding-id` from `list_exchange_apis.py`.
2. Query account balances with `get_deribit_balance.py`.
3. Query derivatives positions with `get_deribit_positions.py`.

```bash
# 1) Find Deribit binding-id
python3 scripts/list_exchange_apis.py --exchange Deribit --page 1 --page-size 50

# 2) Account balances
python3 scripts/get_deribit_balance.py --binding-id <deribit_binding_id>

# 3) Derivatives positions
python3 scripts/get_deribit_positions.py --binding-id <deribit_binding_id>
```

### Deribit Output Interpretation

- Spot/account balance:
  - Read `currency`, `balance`, `equity`, `availableFunds`, `marginBalance`.
- Derivatives positions:
  - Read `instrumentName`, `kind`, `direction`, `size`, `sizeCurrency`, `markPrice`, `totalProfitLoss`.

## How To Query Hyperliquid Spot And Perp Positions

1. Find the Hyperliquid account `binding-id` from `list_exchange_apis.py`.
2. Query spot balances with `get_hyperliquid_balance.py`.
3. Query perpetual positions with `get_hyperliquid_positions.py`.

```bash
# 1) Find Hyperliquid binding-id
python3 scripts/list_exchange_apis.py --exchange Hyperliquid --page 1 --page-size 50

# 2) Spot balances
python3 scripts/get_hyperliquid_balance.py --binding-id <hyperliquid_binding_id>

# 3) Perpetual positions
python3 scripts/get_hyperliquid_positions.py --binding-id <hyperliquid_binding_id>
```

### Hyperliquid Output Interpretation

- Spot balance:
  - `availableMargin` and `balances[]` (`coin`, `available`, `total`, `totalValue`).
- Perp positions:
  - `positions[]`, `accountValue`, `totalNtlPos`, `totalMarginUsed`, `withdrawable`.

## Core Commands

```bash
python3 scripts/get_account_balance.py --help
python3 scripts/get_pv1_balance.py --help
python3 scripts/get_okx_balance.py --help
python3 scripts/get_ltp_balance.py --help
python3 scripts/get_deribit_balance.py --help
python3 scripts/get_pm_positions.py --help
python3 scripts/get_fapi_positions.py --help
python3 scripts/get_okx_positions.py --help
python3 scripts/get_ltp_positions.py --help
python3 scripts/get_deribit_positions.py --help
python3 scripts/get_pm_margin.py --help
python3 scripts/get_fapi_margin.py --help
python3 scripts/get_cm_account.py --help
python3 scripts/get_dapi_account.py --help
python3 scripts/get_cross_margin_account_detail.py --help
python3 scripts/get_ltp_portfolio_asset.py --help
python3 scripts/get_okx_account_max_size.py --help
```
