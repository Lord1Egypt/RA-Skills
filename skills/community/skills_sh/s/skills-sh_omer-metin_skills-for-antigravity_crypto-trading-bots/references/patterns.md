# Crypto Trading Bot Engineer

## Patterns


---
  #### **Id**
dex-sniper
  #### **Name**
DEX Token Sniper
  #### **Description**
    Fast execution bot for buying tokens immediately
    after liquidity is added
    
  #### **When To Use**
    - New token launches
    - Liquidity events
    - Time-sensitive trades
  #### **Implementation**
    // TypeScript sniper structure
    import { ethers } from 'ethers';
    import { FlashbotsBundleProvider } from '@flashbots/ethers-provider-bundle';
    
    class TokenSniper {
        private provider: ethers.Provider;
        private wallet: ethers.Wallet;
        private router: ethers.Contract;
    
        async snipeOnLiquidity(
            tokenAddress: string,
            wethAmount: bigint,
            slippageBps: number = 5000 // 50% for new tokens
        ) {
            // 1. Calculate minimum output with slippage
            const path = [WETH_ADDRESS, tokenAddress];
            const amounts = await this.router.getAmountsOut(wethAmount, path);
            const minOut = amounts[1] * BigInt(10000 - slippageBps) / 10000n;
    
            // 2. Build swap transaction
            const deadline = Math.floor(Date.now() / 1000) + 60;
            const swapData = this.router.interface.encodeFunctionData(
                'swapExactETHForTokensSupportingFeeOnTransferTokens',
                [minOut, path, this.wallet.address, deadline]
            );
    
            // 3. Use Flashbots for private submission
            const flashbotsProvider = await FlashbotsBundleProvider.create(
                this.provider,
                this.wallet
            );
    
            const bundle = [{
                transaction: {
                    to: ROUTER_ADDRESS,
                    value: wethAmount,
                    data: swapData,
                    gasLimit: 300000n,
                    maxFeePerGas: ethers.parseUnits('100', 'gwei'),
                    maxPriorityFeePerGas: ethers.parseUnits('50', 'gwei'),
                },
                signer: this.wallet
            }];
    
            const blockNumber = await this.provider.getBlockNumber();
            const result = await flashbotsProvider.sendBundle(bundle, blockNumber + 1);
    
            return result;
        }
    }
    
    Safety Checks Before Snipe:
    - Verify contract is not honeypot
    - Check for malicious functions (mint, pause, blacklist)
    - Verify liquidity lock
    - Check tax percentages
    - Simulate sell transaction
    
  #### **Security Notes**
    - Use dedicated wallet with limited funds
    - Never expose private keys
    - Implement max spend limits
    - Use Flashbots to avoid front-running

---
  #### **Id**
arbitrage-detector
  #### **Name**
DEX Arbitrage Detection
  #### **Description**
    Monitor price discrepancies across DEXs for
    profitable arbitrage opportunities
    
  #### **When To Use**
    - Cross-DEX arbitrage
    - Triangle arbitrage
    - Cross-chain arbitrage
  #### **Implementation**
    class ArbitrageScanner {
        private dexes: DEXInterface[] = [];
    
        async findOpportunities(tokenA: string, tokenB: string) {
            const opportunities: ArbitrageOp[] = [];
    
            // Get prices from all DEXs
            const prices = await Promise.all(
                this.dexes.map(async dex => ({
                    dex: dex.name,
                    price: await dex.getPrice(tokenA, tokenB),
                    liquidity: await dex.getLiquidity(tokenA, tokenB)
                }))
            );
    
            // Find profitable pairs
            for (let i = 0; i < prices.length; i++) {
                for (let j = i + 1; j < prices.length; j++) {
                    const spread = Math.abs(prices[i].price - prices[j].price);
                    const spreadPct = spread / Math.min(prices[i].price, prices[j].price);
    
                    // Account for gas and slippage
                    const minSpread = 0.005; // 0.5% minimum
                    if (spreadPct > minSpread) {
                        const buyDex = prices[i].price < prices[j].price ? i : j;
                        const sellDex = buyDex === i ? j : i;
    
                        opportunities.push({
                            buyOn: prices[buyDex].dex,
                            sellOn: prices[sellDex].dex,
                            spread: spreadPct,
                            maxSize: Math.min(prices[buyDex].liquidity, prices[sellDex].liquidity) * 0.1
                        });
                    }
                }
            }
    
            return opportunities;
        }
    }
    
    // Flash loan arbitrage
    contract FlashLoanArbitrage {
        function executeArbitrage(
            address token,
            uint256 amount,
            address buyDex,
            address sellDex
        ) external {
            // 1. Flash borrow
            IERC20(token).flashLoan(amount);
    
            // 2. Buy on cheaper DEX
            IDex(buyDex).swap(token, amount);
    
            // 3. Sell on expensive DEX
            IDex(sellDex).swap(token, receivedAmount);
    
            // 4. Repay flash loan + fee
            // Keep profit
        }
    }
    
  #### **Security Notes**
    - Include gas costs in profitability calc
    - Account for price impact
    - Flash loan fees reduce profit

---
  #### **Id**
antirug-checks
  #### **Name**
Anti-Rug Detection
  #### **Description**
    Automated checks to detect potential rug pulls
    before buying tokens
    
  #### **When To Use**
    - Before any token purchase
    - New token analysis
    - Risk assessment
  #### **Implementation**
    interface TokenSafetyCheck {
        isHoneypot: boolean;
        sellTax: number;
        buyTax: number;
        hasBlacklist: boolean;
        hasPausable: boolean;
        hasMintFunction: boolean;
        liquidityLocked: boolean;
        ownerBalance: number;
        topHolderPct: number;
    }
    
    async function checkTokenSafety(tokenAddress: string): Promise<TokenSafetyCheck> {
        const checks: TokenSafetyCheck = {
            isHoneypot: false,
            sellTax: 0,
            buyTax: 0,
            hasBlacklist: false,
            hasPausable: false,
            hasMintFunction: false,
            liquidityLocked: false,
            ownerBalance: 0,
            topHolderPct: 0
        };
    
        // 1. Simulate buy and sell
        try {
            const buyResult = await simulateBuy(tokenAddress, ETH_AMOUNT);
            const sellResult = await simulateSell(tokenAddress, buyResult.tokensReceived);
    
            checks.buyTax = 100 - (buyResult.tokensReceived / expectedTokens * 100);
            checks.sellTax = 100 - (sellResult.ethReceived / expectedEth * 100);
    
            if (sellResult.reverted) {
                checks.isHoneypot = true;
            }
        } catch {
            checks.isHoneypot = true;
        }
    
        // 2. Check contract for dangerous functions
        const code = await provider.getCode(tokenAddress);
        checks.hasBlacklist = code.includes(BLACKLIST_SELECTOR);
        checks.hasPausable = code.includes(PAUSE_SELECTOR);
        checks.hasMintFunction = code.includes(MINT_SELECTOR);
    
        // 3. Check liquidity lock
        const lpToken = await getPairAddress(tokenAddress, WETH);
        checks.liquidityLocked = await isLiquidityLocked(lpToken);
    
        // 4. Check holder distribution
        const holders = await getTopHolders(tokenAddress);
        checks.topHolderPct = holders[0].percentage;
        checks.ownerBalance = await getOwnerBalance(tokenAddress);
    
        return checks;
    }
    
    Red Flags:
    - Sell tax > 10%
    - Honeypot (can't sell)
    - Mint function accessible
    - No liquidity lock
    - Owner holds > 10%
    - Top holder > 20%
    
  #### **Security Notes**
    - Simulations can be bypassed by time-delayed rugs
    - Check contract proxy implementations
    - Monitor for owner actions post-purchase

## Anti-Patterns


---
  #### **Id**
exposed-keys
  #### **Name**
Private keys in bot code
  #### **Severity**
critical
  #### **Description**
    Hardcoding private keys in bot source code
    
  #### **Consequence**
    Keys leaked via logs, repos, or memory dumps
    

---
  #### **Id**
no-spend-limits
  #### **Name**
No maximum spend per trade
  #### **Severity**
high
  #### **Description**
    Bot can spend unlimited funds on single trade
    
  #### **Consequence**
    Bugs or exploits can drain entire wallet
    