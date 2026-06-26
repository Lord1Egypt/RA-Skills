# 智能合约安全审计技术手册

## 常见漏洞类型

### 1. 重入攻击 (Reentrancy)

**漏洞描述**
合约在转账后更新状态，攻击者可递归调用。

**检测代码**
```python
def detect_reentrancy(code: str) -> List[Dict]:
    """检测重入漏洞"""
    issues = []
    
    # 模式：转账后没有更新状态
    patterns = [
        r'(call|send|transfer)\([^)]+\).*\n.*[^=]=',  # 转账后赋值
        r'function\s+\w+.*\{[^}]*call[^}]*\}',  # 函数中包含call
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, code, re.DOTALL)
        for match in matches:
            issues.append({
                'type': 'REENTRANCY',
                'severity': 'CRITICAL',
                'line': code[:match.start()].count('\n') + 1,
                'description': 'Potential reentrancy vulnerability detected',
                'fix': 'Use Checks-Effects-Interactions pattern and ReentrancyGuard'
            })
    
    return issues
```

**防护方案**
```solidity
// 使用检查-生效-交互模式
function withdraw() public {
    uint256 amount = balances[msg.sender];
    require(amount > 0, "No balance");
    
    // 先更新状态
    balances[msg.sender] = 0;
    
    // 再转账
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}

// 或使用重入锁
modifier nonReentrant() {
    require(!locked, "Reentrant call");
    locked = true;
    _;
    locked = false;
}
```

### 2. 整数溢出 (Integer Overflow)

**漏洞描述**
Solidity < 0.8.0 无内置溢出检查。

**检测**
```python
def detect_overflow(code: str, pragma: str) -> List[Dict]:
    """检测整数溢出风险"""
    issues = []
    
    # 检查编译器版本
    version_match = re.search(r'pragma solidity \^?(\d+)\.(\d+)', pragma)
    if version_match:
        major = int(version_match.group(1))
        minor = int(version_match.group(2))
        
        if major < 0 or (major == 0 and minor < 8):
            # 检查是否使用SafeMath
            if 'SafeMath' not in code:
                issues.append({
                    'type': 'INTEGER_OVERFLOW',
                    'severity': 'HIGH',
                    'description': 'Using Solidity < 0.8.0 without SafeMath',
                    'fix': 'Upgrade to Solidity ^0.8.0 or use SafeMath library'
                })
    
    return issues
```

### 3. 访问控制缺失

**检测**
```python
def detect_access_control(code: str) -> List[Dict]:
    """检测访问控制问题"""
    issues = []
    
    # 检查特权函数
    privileged_functions = [
        r'function\s+(mint|burn|transferOwnership|pause|unpause|upgrade)',
        r'function\s+\w+.*onlyOwner',
        r'selfdestruct'
    ]
    
    for pattern in privileged_functions:
        matches = re.finditer(pattern, code, re.IGNORECASE)
        for match in matches:
            func_start = match.start()
            func_end = code.find('}', func_start)
            func_body = code[func_start:func_end]
            
            # 检查是否有访问控制修饰符
            if not any(x in func_body for x in ['onlyOwner', 'onlyAdmin', 'require']):
                issues.append({
                    'type': 'MISSING_ACCESS_CONTROL',
                    'severity': 'CRITICAL',
                    'description': f'Privileged function without access control',
                    'fix': 'Add onlyOwner or similar modifier'
                })
    
    return issues
```

### 4. 时间操控 (Timestamp Dependence)

**检测**
```python
def detect_timestamp_dependence(code: str) -> List[Dict]:
    """检测时间戳依赖"""
    issues = []
    
    # 危险的时间戳使用模式
    dangerous_patterns = [
        r'block\.timestamp\s*[<>=!]+',  # 时间戳比较
        r'block\.number\s*[<>=!]+',  # 区块号比较
        r'now\s*[<>=!]+'  # now关键字
    ]
    
    for pattern in dangerous_patterns:
        matches = re.finditer(pattern, code)
        for match in matches:
            issues.append({
                'type': 'TIMESTAMP_DEPENDENCE',
                'severity': 'MEDIUM',
                'description': 'Contract relies on block.timestamp which can be manipulated by miners',
                'fix': 'Use block.number for longer time periods or accept small manipulation risk'
            })
    
    return issues
```

## 自动化审计流程

### 使用Slither

```python
import subprocess
import json

def run_slither_analysis(contract_path: str) -> Dict:
    """运行Slither分析"""
    try:
        result = subprocess.run(
            ['slither', contract_path, '--json', '-'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {'error': result.stderr}
    except Exception as e:
        return {'error': str(e)}
```

### 使用Mythril

```python
def run_mythril_analysis(contract_path: str) -> Dict:
    """运行Mythril符号执行"""
    try:
        result = subprocess.run(
            ['myth', 'analyze', contract_path, '-o', 'json'],
            capture_output=True,
            text=True,
            timeout=600
        )
        
        return json.loads(result.stdout)
    except Exception as e:
        return {'error': str(e)}
```

## 审计报告模板

```markdown
# 智能合约安全审计报告

## 项目信息
- 项目名称: 
- 合约地址: 
- 审计日期: 
- 审计工具: Slither, Mythril, Manual Review

## 漏洞汇总
| 严重程度 | 数量 |
|----------|------|
| Critical | 0 |
| High     | 1 |
| Medium   | 3 |
| Low      | 5 |
| Info     | 10 |

## 详细发现

### [H-1] 重入攻击风险
**位置**: `Vault.sol:45-52`
**描述**: withdraw函数在转账后更新余额
**修复建议**: 使用Checks-Effects-Interactions模式
**状态**: 已修复 ✅

### [M-1] 时间戳依赖
...

## 安全建议
1. 实施多签管理
2. 添加紧急暂停功能
3. 使用经过审计的库

## 免责声明
本审计报告仅供参考...
```

## 参考资源

- [SWC Registry](https://swcregistry.io/) - 智能合约漏洞分类
- [Consensys Best Practices](https://consensys.github.io/smart-contract-best-practices/)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)
- [Certora Prover](https://www.certora.com/) - 形式化验证

---

*安全无小事，审计须谨慎。*
