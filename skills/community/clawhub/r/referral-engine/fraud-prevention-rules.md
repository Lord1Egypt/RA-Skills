# Referral Fraud Prevention Rules

## Fraud Risk by Program Type

| Program type | Fraud risk | Primary attack vectors |
|---|---|---|
| Open referral (any customer) | Medium | Self-referral, fake account creation |
| Post-purchase gated | Low-Medium | Family/household self-referral |
| High-value rewards ($50+) | High | Organized fraud rings, fake account farms |
| Free product reward | High | Bulk account creation to claim free items |

## Tier 1 Controls — Implement for Every Program

### 1. Reward on shipped order, never on sign-up or add-to-cart
- Fraud attack: Create fake account → use referral code → claim reward without buying
- Control: Reward credit is issued only after referred order ships and return window opens

### 2. Self-referral email domain detection
- Fraud attack: Customer uses their own code with a second email address
- Control: If referrer email domain matches referee email domain → flag for review
- Also flag: obvious pattern variations (john@gmail.com refers johnny.smith@gmail.com)

### 3. Minimum order value threshold
- Set minimum: $25–$50 before referred order qualifies
- Prevents: Creating an account, ordering the cheapest item to unlock a $15 credit

### 4. Duplicate IP address detection
- If 3+ referral code uses originate from the same IP in 24 hours → auto-flag
- Legitimate use case: family member also orders (allow 2 per IP; flag at 3+)

## Tier 2 Controls — Add for High-Value Programs

### 5. Payout delay = return window
- If your return policy is 30 days, don't issue reward until Day 31
- Prevents: Order → claim referral discount → immediately return the order

### 6. Device fingerprinting
- Most referral platforms (Friendbuy, Impact.com) offer this as a paid feature
- Detects same physical device using multiple accounts
- Useful for free product programs where creating 10 fake accounts is worth effort

### 7. Temporary email domain blocklist
Common disposable email domains to block from receiving referee rewards:
- mailinator.com, guerrillamail.com, tempmail.com, throwam.com, yopmail.com, dispostable.com

### 8. Phone number verification for high-value rewards
- Require SMS verification before reward activates
- One phone number = one referee account
- Significantly reduces fake account creation

## Tier 3 Controls — For Enterprise / High-Fraud-Risk Programs

### 9. Manual review queue
- Auto-flag any order that triggers 2+ fraud signals
- Human review before reward issuance
- Target: review within 24 hours

### 10. Velocity rules
- Max referral rewards per customer per month: 5–10 (above this = abnormal)
- If referrer earns 5+ rewards in 30 days → pause account pending review
- Legitimate super-referrers are rare; high volume almost always indicates fraud

## Red Flags Requiring Investigation

| Signal | What it likely means |
|---|---|
| 10+ referral uses from same IP in one day | Fraud ring or organized abuse |
| Referee email addresses follow a pattern (user1@, user2@, user3@) | Bulk fake account creation |
| Referrer redeems reward immediately after referee order ships | Possible family/self-referral collusion |
| High referral code usage rate but low referee repeat purchases | Discount hunters, not real customers |
| Multiple referral accounts with same shipping address | Same household; review for self-referral |

## Acceptable Fraud Rate

Industry benchmark: 3–8% of referral transactions contain some fraud signal.

- Below 3%: Controls may be too aggressive — check if legitimate referrals are being blocked
- 8–15%: Tighten Tier 1 controls; add Tier 2
- Above 15%: Program mechanics are exploitable; consider structural redesign

## Fraud Investigation Workflow

1. Flag triggered → automatic reward hold (don't cancel — investigate first)
2. Customer service review within 48 hours
3. If legitimate: release reward and whitelist account
4. If confirmed fraud: cancel reward, flag account, review all associated accounts
5. If unclear: request order verification (ID match, phone verification)
6. Document pattern and update blocklist/rules accordingly
