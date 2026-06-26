# AgentGenesis — Quick Start Guide

## Your First Agent Wallet

### Prerequisites
- A KYCed sponsor wallet on Netfluid (created by a human)
- The sponsor wallet's `wallet_fk` and 5-digit PIN

### Step 1: Create Your Agent Wallet

Use the `automated_agent_signup` tool:

```
automated_agent_signup(
  sponsor_wallet_fk: <sponsor_wallet_fk>,
  sponsor_wallet_pin: "<5_digit_pin>",
  secret: "agent-worker-alpha",  // Your unique secret
  pin: "12345",                   // Your 5-digit PIN
  email: "agent@example.com",
  mobile: "27821234567",
  currency_fk: 7  // ZAR for South Africa, 3 for USD
)
```

### Step 2: Receive Your Credentials

The signup returns:
- `wallet_fk` — Your wallet ID
- `api_key` — Your API key for authentication
- Session token — For immediate operations

### Step 3: Activate with SOL

Send 0.01 SOL to your new agent wallet address to activate it.

### Step 4: Create Virtual Bank Accounts

**For European Payments (SEPA):**
```
bridge_on_ramp(
  wallet_fk: <your_wallet_fk>,
  account_fk: <your_account_fk>,
  blockchain: "solana",
  address: "<your_solana_address>",
  source_rail: "sepa",
  currency: "usdc",
  alias: "EU Income Account"
)
```

**For US Payments (ACH):**
```
bridge_on_ramp(
  wallet_fk: <your_wallet_fk>,
  account_fk: <your_account_fk>,
  blockchain: "solana",
  address: "<your_solana_address>",
  source_rail: "ach_push",
  currency: "usdc",
  alias: "US Income Account"
)
```

### Step 5: Receive and Send Payments

**Check Balance:**
```
account_info(api_key: <your_api_key>, token: <session_token>, account_fk: <account_fk>)
```

**Send to Another Wallet:**
```
account_send(
  api_key: <your_api_key>,
  token: <session_token>,
  account_fk: <source_account_fk>,
  destination: "<destination_account_address>",
  amount: 100.00,
  note: "Invoice #1234"
)
```

**Off-Ramp to European Bank:**
```
bridge_off_ramp_sepa(
  api_key: <your_api_key>,
  token: <session_token>,
  wallet_fk: <your_wallet_fk>,
  account_fk: <solana_account_fk>,
  account_owner: "John Smith",
  iban: "DE89370400440532013000",
  iso3_country: "DEU",
  iban_bic: "COBADEFFXXX",
  entity_type: "individual",
  address_line: "Hauptstrasse 123",
  address_city: "Berlin",
  address_state: "Berlin",
  address_zipcode: "10115",
  address_iso3_country: "DEU",
  first_name: "John",
  last_name: "Smith",
  reference: "Invoice-1234"
)
```

## Multi-Agent Sponsorship

A sponsor wallet can create unlimited agent wallets:

```
automated_agent_signup(
  sponsor_wallet_fk: <sponsor_wallet_fk>,
  sponsor_wallet_pin: "<sponsor_pin>",
  secret: "worker-alpha-001",
  pin: "54321",
  email: "worker1@example.com",
  mobile: "27821234567",
  currency_fk: 7
)
```

Each agent wallet is:
- Financially segregated from siblings
- KYCed via the sponsor (no individual KYC needed)
- Operationally independent (24/7 autonomous)
- Ready to earn, hold, and spend immediately

## Example Use Cases

### AI Agent Freelancer
1. Create agent wallet under your sponsor
2. Add SEPA virtual account for EU clients
3. Add ACH virtual account for US clients  
4. Receive payments in EUR/USD (converted to USDC)
5. Off-ramp to your bank account as needed

### AI Agent Marketplace
1. Create master sponsor wallet
2. Onboard AI agents under your platform
3. Each agent has segregated finances
4. Pay agents automatically via `account_send`
5. Platform takes commission on each transaction

### AI Agent Payroll Service
1. Sponsor wallet holds platform funds
2. Create agent wallet for each worker
3. Run automated payroll on schedule
4. Workers can off-ramp earnings to personal banks

## Security Best Practices

- Store credentials encrypted (AES-128-GCM)
- Never share API keys or session tokens
- Use unique secrets per agent
- Keep sponsor PIN secure
- Monitor wallet activity regularly
- Enable 2FA on sponsor wallet

## Troubleshooting

**Signup fails?** Check sponsor wallet is KYCed and has sufficient balance for minting.

**Can't receive payments?** Verify virtual account is created and activated.

**Off-ramp fails?** Check bank details are correct and account is verified.

**Session expired?** Re-authenticate with `mcp_netfluid_session` using session key.

---

*For full documentation, see the SKILL.md file*
