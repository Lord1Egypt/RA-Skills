# Depth-Anchored Risk Model for Permissionless On-Chain Lending

*A formal analysis of Torch Market's layered defense system*

---

## Abstract

We present a lending model for constant-product AMM pools where the maximum permissible loan-to-value ratio is a pure function of pool liquidity depth. Combined with per-user borrow caps ($\mu = 23$) proportional to total token supply and a global utilization ceiling, the system creates a graduated risk regime: fresh tokens are structurally protected (3% effective LTV, 95% drop to liquidate), while mature tokens with deep treasuries graduate into functional margin markets (20-45% LTV, 31-69% drop to liquidate). This graduation is emergent from the interaction of three independent caps, not from any single mechanism. Short positions do not share this protective property due to the asymmetric nature of upward price movement, and remain liquidatable by design. No oracles, no keepers, and no stored baseline are required. The pool itself is the sole source of truth. Economic simulation confirms the model under adversarial conditions including cascade liquidations.

---

## 1. Constant Product Pool Fundamentals

A constant-product automated market maker maintains the invariant:

$$x \cdot y = k$$

where $x$ is the SOL reserve (in lamports) and $y$ is the token reserve (in base units). The spot price of a token in SOL is:

$$P = \frac{x}{y}$$

A trade that inputs $\Delta x$ SOL returns:

$$\Delta y = \frac{y \cdot \Delta x}{x + \Delta x}$$

Post-trade reserves become $(x + \Delta x, \; y - \Delta y)$, and $k$ is preserved.

### 1.1 Manipulation Cost

To move the price by a factor $\alpha$ (e.g., $\alpha = 1.2$ for a 20% pump), an attacker must input:

$$\Delta x = x \cdot (\alpha - 1)$$

**Proof.** After buying, the new SOL reserve is $x' = x + \Delta x$. The new token reserve is $y' = k / x' = xy / (x + \Delta x)$. The new price is:

$$P' = \frac{x'}{y'} = \frac{(x + \Delta x)^2}{xy}$$

Setting $P' = \alpha \cdot P$:

$$\frac{(x + \Delta x)^2}{xy} = \alpha \cdot \frac{x}{y}$$

$$(x + \Delta x)^2 = \alpha \cdot x^2$$

$$\Delta x = x(\sqrt{\alpha} - 1)$$

For small $\alpha$, $\sqrt{\alpha} - 1 \approx (\alpha - 1)/2$, so a 20% price move costs approximately $0.1x$ SOL. For a pool with $x = 500$ SOL, this is 50 SOL.

This cost scales linearly with pool depth, making deeper pools proportionally more expensive to manipulate.

---

## 2. Depth-Based Risk Bands

### 2.1 Definition

We define a step function $L: \mathbb{R}_{\geq 0} \to \{0, L_0, L_1, L_2, L_3\}$ that maps pool SOL reserves to a maximum LTV:

$$L(x) = \begin{cases}
0 & \text{if } x < \tau_0 \\
L_0 & \text{if } \tau_0 \leq x < \tau_1 \\
L_1 & \text{if } \tau_1 \leq x < \tau_2 \\
L_2 & \text{if } \tau_2 \leq x < \tau_3 \\
L_3 & \text{if } x \geq \tau_3
\end{cases}$$

With parameters (in lamports and basis points):

| Symbol | Value | Description |
|--------|-------|-------------|
| $\tau_0$ | 5 SOL | Minimum pool depth |
| $\tau_1$ | 50 SOL | Tier 1 threshold |
| $\tau_2$ | 200 SOL | Tier 2 threshold |
| $\tau_3$ | 500 SOL | Tier 3 threshold |
| $L_0$ | 2500 bps (25%) | Max LTV below 50 SOL |
| $L_1$ | 3500 bps (35%) | Max LTV 50-200 SOL |
| $L_2$ | 4500 bps (45%) | Max LTV 200-500 SOL |
| $L_3$ | 5000 bps (50%) | Max LTV above 500 SOL |

### 2.2 Properties

**Monotonicity.** $L$ is non-decreasing: $x_1 \leq x_2 \implies L(x_1) \leq L(x_2)$.

**Self-defense.** To move from tier $i$ to tier $i+1$, an attacker must increase pool SOL from $\tau_i$ to $\tau_{i+1}$ by buying tokens. This requires depositing real SOL, which:
1. Deepens the pool (increasing manipulation cost)
2. Moves tokens to the attacker (who needs them as collateral to borrow)

The attacker cannot inflate the tier without increasing their own cost of attack.

**Graceful degradation.** If pool SOL decreases (due to selling), $L$ decreases, tightening the LTV cap for new positions. Existing positions are unaffected (their LTV was valid at creation) but become more likely to be liquidated if their collateral value drops proportionally.

### 2.3 Effective LTV

The protocol also stores a per-token treasury parameter $L_T$ (`treasury.max_ltv_bps`), set at token creation. The effective maximum LTV is:

$$L_{\text{eff}}(x) = \min(L(x), L_T)$$

This allows individual tokens to have stricter limits than the depth band permits.

---

## 3. Per-User Borrow Cap

### 3.1 Definition

For a user with $c$ tokens of collateral, the maximum SOL they may borrow is:

$$B_{\max}(c) = \frac{M \cdot c \cdot \mu}{S}$$

where:
- $M$ = maximum lendable SOL (utilization cap applied to treasury balance)
- $c$ = user's collateral in base token units
- $\mu = 23$ = borrow share multiplier
- $S = 10^{15}$ = total token supply (1 billion tokens at 6 decimals)

### 3.2 Interpretation

The user's maximum borrow is proportional to their share of total token supply:

$$B_{\max}(c) = M \cdot \mu \cdot \frac{c}{S}$$

A user holding 1% of total supply ($c/S = 0.01$) can borrow at most $0.01 \times 23 \times M = 0.23M$, or 23% of lendable SOL. Four such users fill the pool.

### 3.3 Implied LTV Ceiling

The per-user cap creates an implied LTV that may be stricter than the depth band. The user's collateral value in SOL is:

$$V(c) = c \cdot P = c \cdot \frac{x}{y}$$

Their actual LTV if borrowing the maximum is:

$$\text{LTV}_{\text{cap}} = \frac{B_{\max}(c)}{V(c)} = \frac{M \cdot c \cdot \mu}{S} \cdot \frac{y}{c \cdot x} = \frac{M \cdot \mu \cdot y}{S \cdot x}$$

Note that $c$ cancels. The cap-implied LTV depends only on the pool ratio and treasury size, not on individual position size. This prevents concentration regardless of how many tokens a single user holds.

### 3.4 Numerical Examples

Post-migration pool: $x = 200$ SOL, $y = 145 \times 10^6$ tokens ($145 \times 10^{12}$ base units).

**Fresh treasury (22 SOL).** Utilization cap 80%: $M = 17.6$ SOL.

$$\text{LTV}_{\text{cap}} = \frac{17.6 \times 23 \times 145 \times 10^{12}}{10^{15} \times 200} = 0.029 = 3.0\%$$

At 3% effective LTV, the token price would need to drop **95%** before the position reaches the 65% liquidation threshold. Structurally near-impossible.

**Moderate treasury (150 SOL).** $M = 120$ SOL.

$$\text{LTV}_{\text{cap}} = \frac{120 \times 23 \times 145 \times 10^{12}}{10^{15} \times 200} = 0.20 = 20\%$$

At 20% effective LTV, a **69% price drop** triggers liquidation. Rare but real — this is a functional margin market.

**Deep treasury (500 SOL).** $M = 400$ SOL.

$$\text{LTV}_{\text{cap}} = \frac{400 \times 23 \times 145 \times 10^{12}}{10^{15} \times 200} = 0.67$$

Per-user cap exceeds the depth band (45% for 200 SOL pool). Depth band becomes the binding constraint at 45% LTV — a **31% price drop** triggers liquidation.

### 3.5 Treasury Graduation

The protocol naturally graduates from "near-impossible to liquidate" to "real margin market" as treasury grows:

| Treasury | Max Lendable | Effective LTV | Drop to Liquidate | Regime |
|----------|-------------|---------------|-------------------|--------|
| 22 SOL | 17.6 SOL | 3% | 95% | Protected — fresh token |
| 150 SOL | 120 SOL | 20% | 69% | Active — real margin |
| 300 SOL | 240 SOL | 41% | 37% | Mature — liquidation likely in crashes |
| 500+ SOL | 400+ SOL | 45% (depth capped) | 31% | Deep — depth band is the ceiling |

This graduation is emergent, not designed. It arises from the interaction of three independent caps, each with a different scaling relationship to treasury size.

---

## 4. Global Utilization Cap

### 4.1 Definition

Total SOL lent across all positions is bounded by:

$$\sum_i b_i \leq \frac{T_{\text{sol}} \cdot U}{10000}$$

where $T_{\text{sol}}$ is treasury SOL balance (excluding short collateral), $U = 8000$ bps (80%), and $b_i$ is user $i$'s borrowed amount.

### 4.2 Treasury Solvency

This guarantees $T_{\text{sol}} - \sum b_i \geq 0.2 \cdot T_{\text{sol}}$. Even if every borrower defaults simultaneously, 20% of treasury SOL remains unlent. Combined with seized collateral from liquidations, the treasury maintains positive balance under total default.

---

## 5. Liquidation Threshold Analysis

### 5.1 When Does Liquidation Occur?

A position with initial collateral value $V_0$ and borrowed amount $b$ is liquidated when:

$$\text{LTV} = \frac{b + I}{V} > \theta$$

where $\theta = 6500$ bps (65%), $I$ is accrued interest, and $V$ is current collateral value.

Ignoring interest, the required price decline from position creation for liquidation is:

$$\frac{V}{V_0} < \frac{b}{\theta \cdot V_0} = \frac{\text{LTV}_0}{\theta}$$

Or equivalently, price must drop by a factor:

$$\delta > 1 - \frac{\text{LTV}_0}{\theta}$$

### 5.2 Depth Band Alone

At maximum depth-band LTV ($L_3 = 50\%$):

$$\delta > 1 - \frac{0.50}{0.65} = 1 - 0.769 = 0.231$$

A **23.1% price drop** triggers liquidation. This is the least conservative case (500+ SOL pool, maximum LTV used).

At minimum depth-band LTV ($L_0 = 25\%$):

$$\delta > 1 - \frac{0.25}{0.65} = 1 - 0.385 = 0.615$$

A **61.5% price drop** is required. Fresh pools are significantly safer.

### 5.3 Per-User Cap Interaction

With $\mu = 23$, the per-user cap produces a graduated LTV curve that transitions from protective (fresh tokens) to functional (mature tokens). From Section 3.5:

- Fresh treasury (22 SOL): 3% LTV → **95% drop** to liquidate
- Moderate treasury (150 SOL): 20% LTV → **69% drop** to liquidate
- Deep treasury (500+ SOL): depth-band capped at 45% → **31% drop** to liquidate

### 5.4 Regime Map

| Regime | Binding Constraint | Typical LTV | Price Drop for Liquidation |
|--------|-------------------|-------------|---------------------------|
| Fresh treasury (< 50 SOL) | Per-user cap | 3% | 95% |
| Growing treasury (50-150 SOL) | Per-user cap | 7-20% | 69-89% |
| Mature treasury (150-500 SOL) | Per-user cap → depth band | 20-45% | 31-69% |
| Deep treasury (500+ SOL) | Depth band | 45-50% | 23-31% |

The per-user cap dominates whenever $M \cdot \mu \cdot y / (S \cdot x) < L(x) / 10000$. With $\mu = 23$, this transition occurs around 400-500 SOL treasury for a 200 SOL pool — the point where the token has proven itself through sustained volume and the depth band takes over as the safety ceiling.

### 5.5 Simulation Validation

Economic simulation confirms the regime map. In a cascade stress test with 150 SOL treasury and 422 SOL pool:
- Two positions opened at 42.5-42.8% LTV (per-user cap near depth band ceiling)
- 55% price crash triggered both liquidations
- Liquidator dumped seized collateral, pushing price to 59.7% total decline
- Bad debt absorbed by treasury (137 SOL remaining from 150)
- System remained solvent with zero contagion to other positions

The liquidation engine is not decorative — it functions exactly as designed when treasury depth makes leverage real.

---

## 6. Long-Short Asymmetry

The structural near-impossibility of liquidation applies **only to long positions** (SOL borrowed against token collateral). Short positions (tokens borrowed against SOL collateral) do not share this property.

### 6.1 Why Longs Are Safe

A long borrower deposits tokens and receives SOL. Liquidation requires the token price to *fall*, reducing collateral value. In a constant-product pool, price falling means SOL leaving the pool. But:

- Price drops are bounded: a token's price cannot fall below zero
- Large drops require proportionally large sell volume
- The maximum possible drop is 100% (total value loss)

With effective LTV at 0.29%, even the theoretical maximum drop (100%) only barely breaches the liquidation threshold.

### 6.2 Why Shorts Are Vulnerable

A short seller deposits SOL and borrows tokens. Liquidation requires the token price to *rise*, increasing the SOL value of the token debt. Price increases are **unbounded** — a token can 2x, 10x, or 100x.

The debt value for a short position is:

$$D = \frac{n \cdot x}{y}$$

where $n$ is tokens borrowed. As price rises ($x/y$ increases), $D$ grows without bound. A 3x price increase triples the debt value, pushing a 50% LTV short to 150% — deep into liquidation.

### 6.3 Formal Comparison

For a long position at initial LTV $\ell_0$, the price must drop by $\delta$ for liquidation:

$$\delta_{\text{long}} > 1 - \frac{\ell_0}{\theta}$$

For a short position at initial LTV $\ell_0$, the price must rise by factor $\alpha$ for liquidation:

$$\alpha_{\text{short}} > \frac{\theta}{\ell_0}$$

At $\ell_0 = 0.50$ and $\theta = 0.65$:
- **Long:** needs a 23% drop (bounded, requires real sell pressure)
- **Short:** needs a 1.3x pump (unbounded, common in volatile markets)

At $\ell_0 = 0.0029$ (per-user cap dominated):
- **Long:** needs a 99.6% drop (near-impossible)
- **Short:** needs a 224x pump (extremely unlikely but theoretically possible)

### 6.4 Design Implication

This asymmetry is correct and intentional. Borrowing SOL against tokens you hold (long) is a bet that the token retains some value — a conservative position. Shorting is a bet that the token will decline — an inherently riskier directional trade.

The protocol reflects this: long positions are structurally protected by the cap interaction. Short positions are protected by the depth band and per-user caps, but remain liquidatable under adverse price movement. The liquidation mechanism exists primarily to service short positions.

---

## 7. Transfer Fee as Treasury Growth Engine

Treasury SOL accumulates from two sources: bonding curve fee splits (pre-migration) and transfer fee harvesting (post-migration). Both are significantly more productive than naive models suggest.

### 7.1 Pre-Migration: PVP Bonding Multiplier

During bonding, each buy contributes a dynamic treasury share (17.5% at start, decaying to 2.5% at completion). The naive model assumes one-way buying to target — e.g., 200 SOL of buys for a Torch-tier bond.

In practice, bonding curves exhibit heavy PVP (player vs player) trading: traders buy, take profit, re-enter, panic sell, etc. Empirical observation on Pyre.world (built on Torch) shows tokens reaching 80+ SOL in treasury at only 50% bonded — implying gross buy volume of 5-10x the net curve progression.

The treasury contribution from a single buy at reserves $r$ with amount $a$ is:

$$T_{\text{buy}} = a \cdot (1 - \frac{f_p}{10000}) \cdot \frac{\text{rate}(r)}{10000}$$

where $f_p = 50$ bps (protocol fee) and $\text{rate}(r)$ decays from 1750 to 250 bps. When the same SOL cycles through buys and sells multiple times, the treasury captures the rate on every buy. A 3x volume multiplier (common for active tokens) yields roughly 3x the treasury SOL at migration.

| Volume Multiplier | Estimated Treasury at Migration (Torch tier) |
|-------------------|----------------------------------------------|
| 1x (no PVP) | ~22 SOL |
| 2x | ~35 SOL |
| 5x | ~70 SOL |
| 10x (heavy PVP) | ~100+ SOL |

### 7.2 Post-Migration: Transfer Fee Harvesting

Every token transfer incurs a 0.07% fee ($f = 7$ bps) via the Token-2022 extension. This fee is:
1. Withheld from the transfer amount (in tokens)
2. Accumulated in the token mint
3. Harvested to the treasury token account (permissionless)
4. Swapped to SOL via the pool

The naive linear model assumes constant token price:

$$\dot{T}_{\text{naive}} = V_d \cdot \frac{f}{10000}$$

This significantly underestimates real treasury growth because **transfer fees are collected in tokens, and token value fluctuates**. The correct model:

$$\dot{T} = \sum_i \frac{f \cdot n_i}{10000} \cdot P(t_h)$$

where $n_i$ is the token amount transferred in trade $i$, and $P(t_h)$ is the token price at harvest time — not at transfer time. Since harvesting is batched and permissionless, the treasury benefits from price appreciation between transfers and harvest.

### 7.3 Price-Volume Correlation

Price and volume are positively correlated — pumps drive both higher. During a pump:
- More trades occur (higher $n_i$)
- Each trade transfers more tokens (larger position sizes)
- Accumulated fee tokens are worth more at harvest ($P(t_h)$ elevated)

This creates a multiplicative effect. A 4x200 SOL buy sequence might generate 320K tokens in fees. If price has doubled during the sequence, those tokens harvest for 2x the naive estimate.

**Empirical example:** 4 buys of 200 SOL on Pyre.world generated ~80K tokens in fees, harvesting for 1.2 SOL in a single swap — because price was elevated at harvest time.

### 7.4 Compounding Effect

Treasury growth compounds through three reinforcing loops:

$$T(t+1) = T(t) + H(t) + I(t) + B(t)$$

where:
- $H(t)$ = SOL from harvest-and-swap (transfer fee conversion)
- $I(t)$ = interest collected from active loans
- $B(t)$ = bonding fee accumulation (pre-migration only)

As treasury grows, more SOL is lendable. More lending generates more interest. More interest deepens the treasury. The lending pool is self-funding and self-accelerating.

### 7.5 Community Token Model

For community tokens (no creator fee split), 100% of harvested fees and bonding splits flow to treasury. The protocol extracts nothing post-migration. All value generated by trading activity stays within the token's ecosystem.

---

## 8. Invariants

The following properties hold at all times:

**I1: Supply conservation.** Total token supply is exactly $S = 10^{15}$. No minting occurs post-creation. Mint authority is revoked at migration.

**I2: Pool invariant.** $k' \geq k$ after every swap. $k$ is non-decreasing (no liquidity removal; LP tokens are burned at migration).

**I3: Treasury solvency.** $T_{\text{sol}} \geq \sum b_i \cdot (1 - U/10000)$. At least 20% of treasury SOL is always unlent.

**I4: Position isolation.** Each user has at most one `LoanPosition` and one `ShortPosition` per token. No cross-collateralization exists.

**I5: Depth monotonicity.** $L(x_1) \leq L(x_2)$ for $x_1 \leq x_2$. Deeper pools always permit equal or higher LTV.

**I6: Cap independence.** The per-user borrow cap $B_{\max}(c)$ is independent of other users' positions. One user's borrow does not affect another user's cap (only the global utilization ceiling creates interaction).

---

## 9. Attack Analysis

### 9.1 Price Pump and Borrow

**Attack:** Buy tokens to inflate price, borrow SOL at inflated collateral value, let price revert.

**Defense:** The attacker must spend $\Delta x = x(\sqrt{\alpha} - 1)$ SOL to pump price by $\alpha$. At a 200 SOL pool, a 20% pump costs ~19 SOL. The attacker receives tokens worth $\Delta x$ SOL at the inflated price.

Even at maximum depth-band LTV (50%), the attacker can borrow at most $0.5 \cdot \Delta x = 9.5$ SOL against those tokens. Their net cost is $\Delta x - 0.5 \cdot \Delta x = 0.5 \cdot \Delta x$. They lose money.

**With per-user cap:** The attacker's maximum borrow is further limited to $B_{\max}(c) \ll 0.5 \cdot V(c)$, making the attack strictly unprofitable.

### 9.2 Price Dump and Liquidation Hunting

**Attack:** Sell tokens to crash price, liquidate other users' positions, collect bonus.

**Defense:** With effective LTV at 0.29% (per-user cap dominated), a 99.6% price crash is needed. This would require the attacker to sell enough tokens to remove 99.6% of pool SOL — approximately the entire pool. The attacker would receive far less SOL than they spend in tokens due to constant-product slippage.

### 9.3 Sybil Borrowing

**Attack:** Use many wallets to circumvent per-user cap.

**Defense:** Each wallet needs real token collateral. Total borrowing across all sybil wallets is still bounded by the global utilization cap ($0.8 \cdot T_{\text{sol}}$). The per-user cap prevents any single wallet from taking a disproportionate share, but the utilization cap is the hard ceiling regardless.

### 9.4 Interest Accrual Liquidation

**Attack:** Open position, wait for interest to push LTV past liquidation threshold.

**Analysis:** Interest accrues at $r = 200$ bps per epoch (~7 days). Starting at 0.29% LTV:

$$\text{Epochs to liquidation} = \frac{(\theta - \text{LTV}_0) \cdot 10000}{r} = \frac{(6500 - 29)}{200} = 32.4 \text{ epochs} \approx 227 \text{ days}$$

The borrower has over 7 months to repay before interest alone triggers liquidation. At depth-band maximum (50% LTV):

$$\text{Epochs} = \frac{(6500 - 5000)}{200} = 7.5 \text{ epochs} \approx 52 \text{ days}$$

Still nearly 2 months, and this assumes zero price movement.

---

## 10. Comparison to Traditional DeFi Lending

| Property | Torch Market | Aave/Compound |
|----------|-------------|---------------|
| Price oracle | Pool reserves (on-chain) | Chainlink (off-chain) |
| Maximum LTV | 0.29-50% (regime dependent) | 75-85% |
| Liquidation frequency | Near-zero (structural) | Regular (by design) |
| Liquidator dependency | Minimal | Critical |
| Capital efficiency | Low (safety-first) | High (leverage-first) |
| Treasury funding | Self-funded (transfer fee) | External (governance) |
| Admin keys | None post-migration | Governance multisig |
| Cross-collateral | No | Yes |

The fundamental difference: traditional DeFi lending maximizes capital efficiency and relies on active liquidation to maintain solvency. Torch Market minimizes the probability of liquidation by constraining leverage at the protocol level. This trades capital efficiency for systemic safety.

---

## 11. Conclusion

The depth-anchored risk model creates a lending system where:

1. Maximum LTV adapts to pool manipulation resistance (no stored state)
2. Per-user caps ($\mu = 23$) create graduated leverage — 3% at fresh treasury, scaling to 45% at depth band ceiling
3. Fresh tokens are structurally protected; mature tokens graduate into functional margin markets
4. Treasury grows perpetually from transfer fees (PVP bonding multiplier + price-correlated harvesting) without protocol extraction
5. No oracles, keepers, or governance are required
6. The liquidation engine is functional and validated — not decorative

The result is a permissionless, self-sustaining lending protocol with a natural lifecycle: tokens begin with near-zero liquidation risk (per-user cap dominance) and graduate into real margin markets as treasury depth proves sustained demand. Short positions remain liquidatable at any stage due to the asymmetric nature of upward price risk.

The safety of the system is not a parameter choice — it is a mathematical consequence of the supply split ($y/S \approx 0.15$), the constant-product invariant, and the depth-based LTV ceiling. These properties are immutable post-deployment and hold for all valid inputs, as verified by 71 Kani proof harnesses and economic simulation under adversarial conditions.
