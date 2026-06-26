---
name: security-defense-line
description: |
  安全防线 - 全方位安全防护与威胁防御系统。
  当用户需要以下功能时触发此skill：
  (1) 智能合约安全审计与漏洞检测
  (2) 钱包安全检测与防护
  (3) 交易安全验证与风险预警
  (4) 钓鱼网站/诈骗检测
  (5) 私钥/助记词安全管理
  (6) 多签钱包配置与管理
  (7) 安全事件响应与应急处理
  (8) 安全策略制定与合规检查
---

# Security Defense Line

> 💰 **本 Skill 已接入 SkillPay 付费系统**
> - 每次调用费用：**0.01 USDT**
> - 支付方式：BNB Chain USDT
> - 请先确保账户有足够余额

安全防线 — 守护数字资产，构筑安全堡垒

## 核心能力

### 1. 智能合约安全审计
- **静态分析** - Slither、Mythril、Aderyn自动扫描
- **漏洞检测** - 重入攻击、溢出、权限控制等
- **Gas优化** - 效率分析、成本优化建议
- **代码规范** - Solidity/ Rust最佳实践检查
- **依赖审计** - 第三方库安全评估
- **形式化验证** - 关键逻辑数学证明

### 2. 钱包安全检测
- **地址安全** - 黑名单检查、关联风险分析
- **私钥强度** - 熵值检测、弱密钥识别
- **助记词安全** - 泄露检测、生成验证
- **硬件钱包** - 固件验证、连接安全
- **热钱包防护** - 隔离策略、访问控制
- **备份验证** - 恢复测试、存储安全

### 3. 交易安全验证
- **交易预执行** - 模拟执行、结果预览
- **权限检查** - 授权额度、无限授权检测
- **价格影响** - 滑点分析、MEV风险评估
- **合约验证** - 目标合约安全评级
- **异常检测** - 可疑模式识别
- **多重确认** - 大额交易额外验证

### 4. 钓鱼与诈骗防护
- **域名验证** - 仿冒网站识别
- **URL分析** - 恶意链接检测
- **社交工程** - 诈骗话术识别
- **空投陷阱** - 虚假空投识别
- **假客服** - 冒充官方检测
- **二维码安全** - 恶意二维码扫描

### 5. 私钥与助记词管理
- **生成验证** - 真随机数检测
- **分层派生** - HD钱包路径验证
- **分片存储** - Shamir秘密共享
- **多重备份** - 多地备份策略
- **恢复演练** - 定期恢复测试
- **紧急冻结** - 泄露响应机制

### 6. 多签钱包管理
- **方案设计** - M-of-N策略制定
- **成员管理** - 签名者增删改
- **日常操作** - 发起、签名、执行
- **紧急处理** - 社会恢复、紧急转移
- **权限分层** - 操作权限分级
- **审计日志** - 完整操作记录

### 7. 安全事件响应
- **事件检测** - 异常行为监控
- **紧急冻结** - 资产快速锁定
- **损失评估** - 影响范围分析
- **取证分析** - 攻击链还原
- **恢复计划** - 系统重建方案
- **事后复盘** - 改进建议生成

### 8. 安全策略与合规
- **安全基线** - 最低安全配置
- **定期检查** - 自动化安全扫描
- **员工培训** - 安全意识提升
- **合规检查** - 法规要求对照
- **保险配置** - 安全保险建议
- **文档管理** - 安全策略文档

## 使用工作流

### 快速开始

```bash
# 1. 审计智能合约
python scripts/contract_auditor.py --address 0x... --network ethereum

# 2. 检测钱包安全
python scripts/wallet_guardian.py --address 0x... --full-scan

# 3. 验证交易安全
python scripts/tx_validator.py --tx-hash 0x... --simulate

# 4. 检查钓鱼风险
python scripts/phishing_detector.py --url https://suspicious-site.com

# 5. 管理多签钱包
python scripts/multisig_manager.py --wallet 0x... --operation status

# 6. 启动安全监控
python scripts/security_monitor.py --monitor-all --alert-telegram
```

### 配置示例

```yaml
# config/security_config.yaml
security:
  # 审计配置
  audit:
    tools:
      - slither
      - mythril
      - aderyn
    severity_threshold: medium
    fail_on_critical: true
  
  # 监控配置
  monitoring:
    wallets:
      - address: "0x..."
        name: "Main Wallet"
        alert_threshold: 1.0  # ETH
    
    contracts:
      - address: "0x..."
        name: "DeFi Position"
        events: ["Withdraw", "EmergencyShutdown"]
  
  # 告警配置
  alerts:
    telegram:
      enabled: true
      bot_token: "${TELEGRAM_BOT_TOKEN}"
      chat_id: "${TELEGRAM_CHAT_ID}"
    
    email:
      enabled: true
      smtp_server: "smtp.gmail.com"
      to: "security@example.com"
  
  # 防护规则
  protection:
    max_slippage: 3  # %
    max_gas_price: 500  # gwei
    block_suspicious_contracts: true
    require_confirmation_above: 10  # ETH
```

## 脚本说明

### scripts/contract_auditor.py
智能合约审计器

```bash
# 基础审计
python scripts/contract_auditor.py --address 0xA0b86a33E6441E6C7D3D4b4f6e5a5b6c7d8e9f0a1 --network ethereum

# 深度审计（包含依赖）
python scripts/contract_auditor.py --address 0x... --deep --include-deps

# 本地文件审计
python scripts/contract_auditor.py --file ./MyContract.sol

# 生成审计报告
python scripts/contract_auditor.py --address 0x... --report pdf
```

### scripts/wallet_guardian.py
钱包安全卫士

```bash
# 地址安全检查
python scripts/wallet_guardian.py --address 0x...

# 完整安全扫描
python scripts/wallet_guardian.py --address 0x... --full-scan

# 生成安全评分
python scripts/wallet_guardian.py --address 0x... --score

# 批量检查
python scripts/wallet_guardian.py --file addresses.txt
```

### scripts/tx_validator.py
交易安全验证器

```bash
# 验证待签名交易
python scripts/tx_validator.py --tx-data 0x... --simulate

# 验证已发送交易
python scripts/tx_validator.py --tx-hash 0x... --analyze

# 授权检查
python scripts/tx_validator.py --address 0x... --check-approvals

# 撤销授权
python scripts/tx_validator.py --address 0x... --revoke-all
```

### scripts/phishing_detector.py
钓鱼检测器

```bash
# 检查URL
python scripts/phishing_detector.py --url https://example.com

# 检查域名
python scripts/phishing_detector.py --domain example.com

# 检查智能合约
python scripts/phishing_detector.py --contract 0x...

# 实时防护模式
python scripts/phishing_detector.py --watch-clipboard --auto-block
```

### scripts/multisig_manager.py
多签钱包管理器

```bash
# 查看钱包状态
python scripts/multisig_manager.py --wallet 0x... --status

# 发起交易
python scripts/multisig_manager.py --wallet 0x... --propose --to 0x... --value 1.0

# 签名交易
python scripts/multisig_manager.py --wallet 0x... --sign --tx-id 1

# 执行交易
python scripts/multisig_manager.py --wallet 0x... --execute --tx-id 1

# 管理成员
python scripts/multisig_manager.py --wallet 0x... --add-owner 0x...
```

### scripts/incident_responder.py
安全事件响应器

```bash
# 紧急冻结
python scripts/incident_responder.py --emergency-freeze --wallet 0x...

# 事件分析
python scripts/incident_responder.py --analyze --tx-hash 0x...

# 损失评估
python scripts/incident_responder.py --assess-loss --address 0x...

# 生成报告
python scripts/incident_responder.py --generate-report --incident-id 1
```

### scripts/security_monitor.py
安全监控中心

```bash
# 启动监控
python scripts/security_monitor.py --daemon

# 监控特定地址
python scripts/security_monitor.py --watch 0x... --events all

# 监控合约事件
python scripts/security_monitor.py --contract 0x... --events "Transfer,Approval"

# Web Dashboard
python scripts/security_monitor.py --dashboard --port 8080
```

## 安全检测清单

### 智能合约审计清单
- [ ] 重入攻击防护
- [ ] 整数溢出检查
- [ ] 访问控制验证
- [ ] 时间操控防护
- [ ] 随机数安全
- [ ] 预言机依赖
- [ ] Gas优化
- [ ] 升级机制
- [ ] 紧急暂停
- [ ] 事件日志

### 钱包安全检查清单
- [ ] 私钥离线存储
- [ ] 助记词备份验证
- [ ] 多重备份策略
- [ ] 地址黑名单检查
- [ ] 授权额度审查
- [ ] 历史交易审查
- [ ] 硬件钱包验证
- [ ] 恢复流程测试

### 交易安全清单
- [ ] 目标合约验证
- [ ] 交易模拟执行
- [ ] 滑点确认
- [ ] Gas估算
- [ ] 权限检查
- [ ] 价格验证
- [ ] 链ID确认
- [ ] 收款地址核对

## 威胁响应等级

### 🔴 P0 - 紧急 (立即响应)
- 私钥泄露 suspected
- 大额异常转出
- 合约被攻击
- 多签被篡改

### 🟠 P1 - 高危 (1小时内)
- 可疑授权
- 异常登录
- 新设备访问
- 钓鱼尝试

### 🟡 P2 - 中危 (24小时内)
- 配置变更
- 权限调整
- 备份失败
- 扫描告警

### 🟢 P3 - 低危 (常规处理)
- 更新提醒
- 优化建议
- 信息通知

## 最佳实践

### 私钥管理黄金法则
1. **永不触网** - 私钥永不在联网设备生成或存储
2. **多重备份** - 至少3份备份，分地存储
3. **定期测试** - 每季度恢复测试
4. **分级管理** - 按金额分级存储策略

### 交易安全原则
1. **小额测试** - 新合约先小额测试
2. **官方验证** - 只使用官方验证的合约地址
3. **双重确认** - 大额交易多渠道确认
4. **及时清理** - 用完即撤销授权

### 多签最佳实践
1. **分散控制** - 签名者分布在不同地理位置
2. **冷热分离** - 日常操作与紧急恢复分开
3. **定期轮换** - 定期更换签名者
4. **完整测试** - 定期执行完整流程测试

## 安全资源

### 审计工具
| 工具 | 用途 | 推荐度 |
|------|------|--------|
| Slither | 静态分析 | ⭐⭐⭐⭐⭐ |
| Mythril | 符号执行 | ⭐⭐⭐⭐ |
| Aderyn | Rust合约审计 | ⭐⭐⭐⭐ |
| Echidna | 模糊测试 | ⭐⭐⭐⭐ |
| Manticore | 符号执行 | ⭐⭐⭐ |

### 情报源
- **SlowMist** - 区块链安全情报
- **CertiK** - 安全评级与监控
- **Chainalysis** - 链上分析
- **Etherscan** - 合约验证与监控
- **Forta** - 实时威胁检测

### 学习资源
- **Secureum** - 智能合约安全学习
- **Damn Vulnerable DeFi** - 实战训练
- **OpenZeppelin** - 安全开发指南
- **Consensys** - 最佳实践文档

## 警告与免责

⚠️ **重要提示**

- 本工具提供安全检测建议，不构成绝对安全保证
- 任何安全工具都无法替代人工判断
- 使用本工具产生的任何损失，开发者不承担责任
- 建议关键操作寻求专业安全团队审计
- 安全是持续过程，不是一次性检查

---

*安全第一，预防为主。守好最后一道防线。*
