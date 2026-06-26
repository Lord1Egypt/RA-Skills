# Crypto Trading Bots - Validations

## Private key in source code

### **Id**
exposed-private-key
### **Severity**
error
### **Type**
regex
### **Pattern**
  - privateKey\s*[=:]\s*["\x27]0x[a-fA-F0-9]{64}
  - PRIVATE_KEY\s*=\s*["\x27]0x
### **Message**
Never hardcode private keys - use environment variables
### **Fix Action**
Move to .env file and use process.env.PRIVATE_KEY
### **Applies To**
  - *.ts
  - *.js

## Trading without slippage protection

### **Id**
no-slippage-protection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - minAmountOut\s*[=:]\s*0|minOut\s*=\s*0
### **Message**
Zero slippage protection allows complete loss
### **Fix Action**
Calculate reasonable minOut based on expected price
### **Applies To**
  - *.ts
  - *.js