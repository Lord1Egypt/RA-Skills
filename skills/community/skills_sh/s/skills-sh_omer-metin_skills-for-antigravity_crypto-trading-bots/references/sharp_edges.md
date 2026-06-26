# Crypto Trading Bots - Sharp Edges

## Sandwich Victim

### **Id**
sandwich-victim
### **Summary**
Your bot gets sandwiched by MEV bots
### **Severity**
high
### **Situation**
  You submit trade to public mempool. MEV bot sees it, front-runs
  your buy, and back-runs your sell. You get worse price.
  
### **Solution**
  // Use private mempool (Flashbots)
  const flashbots = await FlashbotsBundleProvider.create(provider, wallet);
  await flashbots.sendPrivateTransaction(signedTx);
  
  // Or use MEV-protected RPC
  // - Flashbots Protect
  // - MEV Blocker
  // - Private RPCs
  

## Revert On Tax

### **Id**
revert-on-tax
### **Summary**
Transaction reverts due to token transfer tax
### **Severity**
medium
### **Situation**
  You use swapExactTokensForTokens. Token has 5% tax. Expected
  output doesn't match, transaction reverts.
  
### **Solution**
  // Use fee-on-transfer variant
  router.swapExactETHForTokensSupportingFeeOnTransferTokens(
      minOut,
      path,
      recipient,
      deadline
  );
  // This tolerates tokens with transfer taxes
  

## Frontrun Own Bot

### **Id**
frontrun-own-bot
### **Summary**
Running multiple bots that compete with each other
### **Severity**
medium
### **Situation**
  You run multiple sniper instances. They detect same opportunity
  and compete, driving up gas costs and reducing profit.
  
### **Solution**
  // Coordinate via shared state or leader election
  // Use nonce management to prevent conflicts
  const nonce = await nonceManager.getNextNonce(wallet.address);
  