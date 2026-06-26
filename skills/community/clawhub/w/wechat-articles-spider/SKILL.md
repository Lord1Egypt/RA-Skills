---
name: wechat-article-crawler
version: "2.0.4"
description: WeChat Official Account article crawler with x402 micropayments. Requires Chrome browser and interactive WeChat QR login on first use. Harvest articles for research and analysis with pay-as-you-go Base USDC pricing.
allowed-tools: Bash(python3:*) Read Write Edit
metadata:
  clawdbot:
    emoji: 🕷️
    requires:
      anyBins: ["python3", "google-chrome"]
      env: ["USER_ID"]
      localFiles:
        - "./weixin_credentials.py"
        - "./data/users/"
        - "./data/queue/"
    os: ["linux", "darwin", "win32"]
  openclaw:
    skillKey: wechat-article-crawler
    x402:
      enabled: true
      chain: base
      token: USDC
      pricing:
        per_article: 0.1
        per_account: 10
        monthly: 100
      receiving_address: "0x172444FC64e2E370fCcF297dB865831A1555b07A"
---

# WeChat Article Crawler with x402 Payment

微信公众号文章爬虫 - **x402 支付版**

支持实时支付（小额）和异步支付（大额）混合模式，使用 Base 链 USDC 支付。

## When to Use

Use this skill when you need to:

- **Monitor competitor accounts**: Track what other WeChat Official Accounts are publishing
- **Content research**: Gather articles from specific niches for analysis
- **Archive building**: Download complete post history from valuable accounts
- **Keyword filtering**: Find articles matching specific topics with weighted scoring
- **Automated reporting**: Schedule daily crawls of key accounts
- **Price**: Free tier (10 articles), then $0.1/article or $10/account via x402 on Base

## Pricing

| 计费模式 | 价格 | 说明 |
|---------|------|------|
| **按篇** | $0.1 USDC/篇 | 适合少量精准获取 |
| **按号** | $10 USDC/号 | 批量获取某号全部历史文章 |
| **包月** | $100 USDC/月 | 30天无限使用 |
| **免费** | 10篇 | 新用户免费体验 |

## Payment Modes

### 实时支付（<$5）
- 小额支付，即时确认
- 支付后立即开始爬取
- 适合：按篇计费、少量文章

### 异步支付（≥$5）
- 大额支付，后台处理
- 支付确认后加入队列
- 完成后通过 webhook 通知
- 适合：按号计费、批量爬取

## Quick Start

### 1. Set User ID (Required)
```bash
export USER_ID="0xYourWalletAddress"
```

### 2. Check Status
```bash
python3 spider_cli.py status --user $USER_ID
```

### 3. Crawl with Free Quota
```bash
python3 spider_cli.py crawl --user $USER_ID --account 机器之心 --max 5 --mode free
```

### 4. Real-time Payment (small amount)
```bash
python3 spider_cli.py crawl --user $USER_ID --account 机器之心 --max 20
# System prompts payment of $2 USDC
# Complete transfer and enter transaction hash
```

### 5. Async Payment (large amount)
```bash
python3 spider_cli.py crawl --user $USER_ID --account 机器之心 --max 100 --mode async
# Pay $10 USDC, task enters queue for background processing
```

### 6. Check Task Status
```bash
python3 spider_cli.py status TASK-1711523456-7890
```

### 7. Subscribe Monthly
```bash
python3 spider_cli.py subscribe --user $USER_ID
# Pay $100 USDC for 30 days unlimited usage
```

## x402 Payment Flow

```
User requests crawl → System calculates price → 
  ├─ <$5 → Real-time payment → User transfers → Confirm → Crawl immediately
  └─ ≥$5 → Async payment → User transfers → Confirm → Add to queue → Background crawl → Notify completion
```

## File Structure

```
wechat_articles_spider/
├── SKILL.md                    # This documentation
├── config.py                   # Configuration (pricing, receiving address)
├── spider_cli.py              # CLI entry point
├── spider_api.py              # API layer
├── x402_core.py               # x402 payment core
├── quota_manager.py           # User quota management
├── async_queue.py             # Async task queue
├── blockchain_verifier.py     # On-chain verification
├── wechat_mp_crawler.py       # Core crawler logic
├── requirements.txt           # Python dependencies
└── data/                      # Data storage
    ├── users/                 # User data (quotas, subscriptions)
    └── queue/                 # Async task queue
```

## Configuration

Edit `config.py` to customize:

```python
# Receiving address (already set)
RECEIVING_ADDRESS = "0x172444FC64e2E370fCcF297dB865831A1555b07A"

# Pricing (USDC)
PRICING = {
    "per_article": 0.1,
    "per_account": 10.0,
    "monthly": 100.0,
}

# Async threshold
ASYNC_THRESHOLD = 5.0  # Use async for payments >= $5
```

## Dependencies

```bash
pip install -r requirements.txt
```

Required: Python 3.8+, Google Chrome browser

## Workflow Examples

### Example 1: New User with Free Quota
```
$ python3 spider_cli.py crawl --user 0xNewUser --account 机器之心 --max 5 --mode free

🎁 Free quota: 10/10 articles
📅 Monthly subscription: ❌ Not active

🚀 Crawling 5 articles with free quota...
✅ Success!
   Articles: 5
   Cost: $0 USDC
   Payment method: free
   Remaining free quota: 5
```

### Example 2: Real-time Payment
```
$ python3 spider_cli.py crawl --user 0xUser --account 机器之心 --max 20

🎁 Free quota: 0/10 articles
📅 Monthly subscription: ❌ Not active

💳 Payment required: $2.0 USDC
   Receiving address: 0x172444FC64e2E370fCcF297dB865831A1555b07A
   Network: Base
   
Steps:
1. Open your wallet (MetaMask / Coinbase Wallet)
2. Switch to Base network
3. Send $2.0 USDC to: 0x172444FC64e2E370fCcF297dB865831A1555b07A
4. Copy transaction hash

Enter transaction hash (0x...): 0xabc123...

✅ Success!
   Articles: 20
   Cost: $2.0 USDC
   Payment method: x402
   Transaction: 0xabc123...
```

### Example 3: Async Payment
```
$ python3 spider_cli.py crawl --user 0xUser --account 机器之心 --max 200 --mode async

💳 Payment required: $10.0 USDC
   ...

Enter transaction hash (0x...): 0xdef456...

✅ Payment confirmed, task queued
   Task ID: TASK-1711523456-7890
   Check status with: status TASK-1711523456-7890

$ python3 spider_cli.py status TASK-1711523456-7890

📋 Task status: TASK-1711523456-7890
   Account: 机器之心
   Status: processing
   ...

# 10 minutes later

📋 Task status: TASK-1711523456-7890
   Status: completed
   Result: {"articles_count": 200}
```

## Troubleshooting

### Payment Issues

**"Transaction not found"**
- Ensure you're on Base network (not Ethereum mainnet)
- Wait 30-60 seconds for transaction to be mined
- Check transaction on [BaseScan](https://basescan.org)

**"Insufficient amount"**
- Verify you sent enough USDC (include decimals)
- Check transaction details for exact amount sent

**"Payment expired"**
- Payment requests expire after 5 minutes
- Create a new crawl request

### Crawl Issues

**"WeChat login failed"**
- Close VPN before running
- Delete `weixin_credentials.py` and retry
- Use a different WeChat account (small accounts have lower ban risk)

**"No articles found"**
- Verify the account name is correct (case-sensitive)
- Account may not have published recently
- Try searching for account first

**"Account blocked"**
- WeChat detected automated access
- Wait 24 hours before retrying
- Reduce crawl frequency (built-in 5-15s delays help)

**"Chrome not found"**
- Install Google Chrome: https://www.google.com/chrome/
- Or set CHROME_BIN environment variable to Chrome executable path

### Installation Issues

**"ModuleNotFoundError: No module named 'selenium'"**
```bash
pip install -r requirements.txt
```

**"ChromeDriver version mismatch"**
```bash
# webdriver-manager should auto-download, but if issues occur:
pip install --upgrade webdriver-manager
```

## Important Notes

1. **WeChat Account Risk**
   - WeChat may ban accounts used for crawling
   - Use a secondary/dedicated account
   - Never use your primary WeChat account

2. **VPN Must Be Disabled**
   - Close all VPN connections before crawling
   - VPN causes WeChat login timeouts

3. **Rate Limiting**
   - Built-in 5-15 second random delays between requests
   - Don't run multiple crawls simultaneously
   - Daily limit: 100-200 articles recommended

4. **Base Chain Requirements**
   - Ensure wallet has Base network USDC
   - Keep small amount of ETH for gas fees
   - Verify receiving address before sending

## On-Chain Verification

Enable on-chain verification for production:

```bash
# Using public RPC (free, rate-limited)
export X402_ONCHAIN_VERIFY=true
export BASE_NETWORK=mainnet

# Using Alchemy/Infura (recommended for production)
export X402_ONCHAIN_VERIFY=true
export BASE_NETWORK=mainnet
export BASE_API_KEY=your_alchemy_api_key

# Using BaseScan API
export X402_ONCHAIN_VERIFY=true
export USE_BASESCAN=true
export BASE_API_KEY=your_basescan_api_key
```

## Security Considerations

- **Receiving Address**: Double-check `0x172444FC64e2E370fCcF297dB865831A1555b07A` before sending payments
- **Private Keys**: Never share wallet private keys; skill only needs public address
- **Data Storage**: User data stored locally in `data/` directory
- **WeChat Credentials**: Saved in `weixin_credentials.py`; keep this file secure

## Data Storage Locations

The skill stores data in the following locations (relative to skill directory):

```
~/.wechat_article_crawler/
├── weixin_credentials.py       # WeChat login tokens (sensitive)
└── data/
    ├── users/                  # User quotas and subscriptions
    │   └── {user_id}.json
    └── queue/                  # Async task queue
        └── tasks.json
```

## Tips

- **Free tier first**: Always test with 10 free articles before paying
- **Batch efficiently**: Crawl full account history ($10) instead of many small payments
- **Subscribe if regular**: Monthly subscription pays for itself after 1000 articles
- **Monitor task status**: Async tasks can be checked anytime with `status TASK-ID`
- **Use testnet first**: Test on Base Sepolia with test USDC before mainnet
- **Save credentials**: After first login, `weixin_credentials.py` allows 24hr re-access
- **Account safety**: Rotate WeChat accounts monthly to reduce ban risk
- **VPN reminder**: Always disable VPN; check with `curl ipinfo.io` if unsure
- **Payment receipts**: Keep transaction hashes for dispute resolution
- **Error logs**: Check `data/queue/tasks.json` for failed task details

## License

MIT License - For educational and research purposes only

---

**x402 Powered** ⚡️ Programmatic payments via x402 protocol on Base
