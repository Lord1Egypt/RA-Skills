# 动态测试指南 - SkillsBench Evaluator

## 概述

本文档详细说明如何对 Agent Skills 进行动态测试,验证实际功能是否与文档描述一致。

---

## 动态测试的价值

### **为什么需要动态测试?**

**静态分析的局限性:**
- ❌ 只能检查文档写得好不好
- ❌ 无法验证功能是否真的有效
- ❌ 可能存在"文档完美但实际不工作"的情况

**动态测试的优势:**
- ✅ 验证功能是否正常工作
- ✅ 检测文档与实际的差异
- ✅ 发现运行时错误
- ✅ 验证输出格式是否准确
- ✅ 测试边界情况和错误处理

---

## 测试用例设计原则

### **1. 覆盖核心功能**

**示例 - westock-data:**
```json
{
  "testCases": [
    {
      "name": "搜索股票代码",
      "command": "node scripts/index.js search 茅台",
      "expectedFormat": "markdown-table",
      "expectedFields": ["code", "name", "type"],
      "shouldSucceed": true
    },
    {
      "name": "查询实时行情",
      "command": "node scripts/index.js quote sh600519",
      "expectedFormat": "markdown-table",
      "expectedFields": ["code", "name", "price", "change"],
      "shouldSucceed": true
    }
  ]
}
```

---

### **2. 测试不同参数组合**

**示例 - K线查询:**
```json
{
  "name": "日K线查询",
  "command": "node scripts/index.js kline sh600519 --period day --limit 5",
  "expectedFormat": "markdown-table",
  "expectedFields": ["date", "open", "close", "high", "low"],
  "shouldSucceed": true
}
```

---

### **3. 验证批量查询**

**示例 - 批量行情:**
```json
{
  "name": "批量查询行情",
  "command": "node scripts/index.js quote sh600519,sz000001",
  "expectedFormat": "markdown-table",
  "expectedFields": ["code", "name", "price"],
  "shouldSucceed": true
}
```

---

### **4. 测试错误处理**

**示例 - 无效股票代码:**
```json
{
  "name": "错误处理-无效代码",
  "command": "node scripts/index.js quote invalid123",
  "expectedFormat": "json-error",
  "expectedFields": ["success", "error"],
  "shouldSucceed": false
}
```

---

### **5. 边界情况测试**

**示例 - 极限查询:**
```json
{
  "name": "边界测试-最大limit",
  "command": "node scripts/index.js kline sh600519 --limit 2000",
  "expectedFormat": "markdown-table",
  "shouldSucceed": true
}
```

---

## 测试执行流程

### **Step 1: 识别可测试命令**

从 SKILL.md 中提取:

**扫描关键词:**
- 代码块中的命令示例
- "示例"、"用法"、"Example" 等章节
- 带有 `bash`、`python`、`node` 标记的代码块

**提取信息:**
- 完整命令
- 参数说明
- 预期输出格式描述

---

### **Step 2: 构建测试用例**

**基于文档自动生成:**

```markdown
## SKILL.md 示例:

​```bash
westock-data quote sh600000                      # 单股
westock-data quote sh600000,sz000001,hk00700     # 批量
​```

**返回:** Markdown 表格,包含价格、涨跌幅、成交量等
```

**自动生成测试用例:**
```json
[
  {
    "name": "单股行情查询",
    "command": "westock-data quote sh600000",
    "expectedFormat": "markdown-table",
    "expectedFields": ["price", "change", "volume"],
    "source": "SKILL.md line 42"
  },
  {
    "name": "批量行情查询",
    "command": "westock-data quote sh600000,sz000001,hk00700",
    "expectedFormat": "markdown-table",
    "expectedFields": ["code", "price"],
    "source": "SKILL.md line 43"
  }
]
```

---

### **Step 3: 执行测试**

**执行方法:**

```bash
# 1. 确定 Skill 路径
SKILL_PATH=~/.openclaw/skills/westock-data

# 2. 确定执行方式
cd $SKILL_PATH

# 3. 运行命令
node scripts/index.js quote sh600519

# 4. 捕获输出
OUTPUT=$(node scripts/index.js quote sh600519 2>&1)

# 5. 记录执行时间
START=$(date +%s%3N)
node scripts/index.js quote sh600519
END=$(date +%s%3N)
DURATION=$((END - START))
```

---

### **Step 4: 验证返回格式**

**检查项:**

1. **输出格式类型**
   ```python
   # Markdown 表格检测
   if output.startswith("|") and "---" in output:
       format_type = "markdown-table"
   
   # JSON 检测
   elif output.strip().startswith("{") or output.strip().startswith("["):
       format_type = "json"
   
   # 纯文本
   else:
       format_type = "text"
   ```

2. **字段完整性**
   ```python
   # 提取 Markdown 表格的列名
   if format_type == "markdown-table":
       header_line = output.split("\n")[0]
       actual_fields = [f.strip() for f in header_line.split("|")[1:-1]]
       
       # 检查是否包含预期字段
       missing_fields = set(expected_fields) - set(actual_fields)
       extra_fields = set(actual_fields) - set(expected_fields)
   ```

3. **数据类型**
   ```python
   # 检查数据行
   data_line = output.split("\n")[2]  # 跳过表头和分隔符
   values = [v.strip() for v in data_line.split("|")[1:-1]]
   
   # 验证数值字段
   if "price" in expected_fields:
       price_value = values[actual_fields.index("price")]
       assert is_number(price_value), "price 应该是数值"
   ```

---

### **Step 5: 对比文档描述**

**文档说明:**
```markdown
**返回:** Markdown 表格,包含价格、涨跌幅、成交量等
```

**实际返回:**
```markdown
| code | name | price | change | volume | amount | ... |
```

**验证结果:**
- ✅ 格式正确: Markdown 表格
- ✅ 包含字段: price, change, volume
- ⚠️ 额外字段: code, name, amount (文档未提及)
- ✅ 结论: 与文档描述基本一致,额外字段不影响

---

### **Step 6: 记录测试结果**

**测试结果数据结构:**
```json
{
  "testCase": {
    "name": "查询实时行情",
    "command": "node scripts/index.js quote sh600519"
  },
  "result": {
    "status": "passed",
    "duration": 1234,
    "output": "| code | name | price | ...",
    "formatCorrect": true,
    "fieldsCorrect": true,
    "errors": [],
    "warnings": [
      "文档未提及 code 和 name 字段,但实际返回了"
    ]
  }
}
```

---

## 测试结果分析

### **通过率计算**

```
通过率 = (通过的测试用例数 / 总测试用例数) × 100%
```

**示例:**
- 总测试用例: 5
- 完全通过: 3
- 部分通过: 1
- 失败: 1

**通过率:** 3/5 = 60% (完全通过) 或 4/5 = 80% (包含部分通过)

---

### **评分调整规则**

**基于动态测试结果调整执行完整性得分:**

| 通过率 | 评分调整 | 说明 |
|--------|---------|------|
| 100% | +5 分 | 所有测试通过,文档与实际完全一致 |
| 80-99% | 0 分 | 大部分测试通过,少量问题 |
| 60-79% | -5 分 | 存在明显问题,需要改进 |
| 40-59% | -10 分 | 重大功能问题 |
| <40% | -15 分 | 严重问题,基本不可用 |

**文档准确性扣分:**

| 问题类型 | 扣分 | 说明 |
|---------|------|------|
| 返回格式与文档不符 | -5 分 | 如文档说 JSON,实际返回 Markdown |
| 缺少文档承诺的字段 | -3 分/字段 | 文档说有某字段,实际没有 |
| 错误处理不规范 | -3 分 | 错误返回格式不统一 |
| 示例命令无法运行 | -5 分/命令 | 文档中的示例实际运行失败 |

---

## 常见问题处理

### **Q1: 测试需要环境依赖怎么办?**

**A:** 在测试前进行环境检查:

```bash
# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️ 需要 Node.js 环境"
    echo "请安装后再测试"
    exit 1
fi

# 检查版本
NODE_VERSION=$(node --version | cut -d'v' -f2)
if [[ "$NODE_VERSION" < "18.0.0" ]]; then
    echo "⚠️ 需要 Node.js >= v18"
    exit 1
fi
```

如果环境不满足,在报告中说明:
```markdown
## ⚠️ 动态测试未执行

**原因:** 环境依赖不满足
- 需要: Node.js >= v18
- 当前: Node.js v16.14.0

**建议:** 请在满足环境要求后重新测试
```

---

### **Q2: 测试需要 API Key 或认证怎么办?**

**A:** 在测试前询问用户:

```markdown
⚠️ 该 Skill 需要 API 认证

westock-data 使用腾讯自选股 API,可能需要:
- 网络访问 api.woas.com
- 内网认证 token

是否继续执行动态测试?
- 如果有内网环境: 可以继续
- 如果没有认证: 仅进行静态分析
```

如果用户确认继续,执行测试并记录:
```markdown
## 动态测试环境说明

- 测试环境: 腾讯内网
- 认证方式: TAI_IT_TOKEN (自动注入)
- 网络访问: 正常
```

---

### **Q3: 测试可能有副作用怎么办?**

**A:** 识别敏感操作并警告:

**敏感操作类型:**
- 删除文件 (`rm`, `trash`, `delete`)
- 发送消息 (`message send`, `email`, `slack`)
- 修改数据 (`update`, `modify`, `write`)
- 网络请求 (`curl`, `wget`, `fetch`)

**处理方式:**
```markdown
⚠️ 检测到敏感操作

该 Skill 的测试可能会:
- 发送企业微信消息
- 创建临时文件

建议:
1. 使用测试账号
2. 设置测试环境变量
3. 测试后清理临时数据

是否继续? (需要用户确认)
```

---

### **Q4: 测试超时怎么办?**

**A:** 设置超时保护:

```python
import subprocess
import time

def run_test_with_timeout(command, timeout=10):
    """运行测试,带超时保护"""
    start_time = time.time()
    
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 等待完成或超时
        stdout, stderr = process.communicate(timeout=timeout)
        duration = int((time.time() - start_time) * 1000)
        
        return {
            "status": "success",
            "output": stdout.decode(),
            "error": stderr.decode(),
            "duration": duration
        }
    
    except subprocess.TimeoutExpired:
        process.kill()
        return {
            "status": "timeout",
            "error": f"测试超时 ({timeout}s)",
            "duration": timeout * 1000
        }
```

**记录超时结果:**
```markdown
| 测试用例 | 状态 | 执行时间 | 备注 |
|---------|------|---------|------|
| 大量数据查询 | ⏱️ 超时 | 10.0s | 超过设定的 10s 超时 |
```

---

## 最佳实践

### **1. 选择代表性测试用例**

不需要测试所有命令,选择:
- ✅ 核心功能 (最重要的 3-5 个命令)
- ✅ 典型使用场景
- ✅ 文档中重点介绍的功能
- ✅ 容易出错的边界情况

---

### **2. 测试用例优先级**

**P0 - 必须测试:**
- 核心功能命令
- 文档中的第一个示例

**P1 - 应该测试:**
- 参数组合
- 批量查询
- 错误处理

**P2 - 可选测试:**
- 边界情况
- 性能测试
- 高级功能

---

### **3. 测试结果呈现**

**清晰的表格:**
```markdown
| 测试用例 | 状态 | 执行时间 | 备注 |
|---------|------|---------|------|
| 搜索股票 | ✅ 通过 | 0.8s | - |
| 查询行情 | ✅ 通过 | 1.2s | 返回格式正确 |
| 批量查询 | ✅ 通过 | 2.1s | - |
| 错误处理 | ⚠️ 部分通过 | 0.5s | 格式不统一 |
```

**详细的问题说明:**
```markdown
### 发现的问题

#### 问题 1: 错误返回格式不统一

**文档说明:**
> 查询失败时输出 JSON 格式错误信息,含 `success: false` 和 `error` 对象

**实际测试:**
​```bash
$ node scripts/index.js quote invalid123
数据为空
​```

**问题分析:**
- 实际返回纯文本 "数据为空"
- 不符合文档描述的 JSON 格式
- 难以程序化处理错误

**改进建议:**
统一错误返回格式:
​```json
{
  "success": false,
  "error": {
    "code": "INVALID_SYMBOL",
    "message": "股票代码格式错误: invalid123"
  }
}
​```
```

---

### **4. 持续集成建议**

**对于 Skill 作者:**

1. **创建测试脚本**
   ```bash
   # test.sh
   #!/bin/bash
   
   echo "Running tests for westock-data..."
   
   # 测试 1: 搜索
   node scripts/index.js search 茅台
   
   # 测试 2: 行情
   node scripts/index.js quote sh600519
   
   # 测试 3: K线
   node scripts/index.js kline sh600519 --limit 5
   
   echo "All tests passed!"
   ```

2. **添加到 CI/CD**
   ```yaml
   # .github/workflows/test.yml
   name: Test Skill
   
   on: [push, pull_request]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - uses: actions/setup-node@v2
           with:
             node-version: '18'
         - run: bash test.sh
   ```

---

## 总结

动态测试是验证 Skill 质量的关键环节:

| 维度 | 静态分析 | 动态测试 |
|------|---------|---------|
| 速度 | ⚡ 快 | 🐢 慢 |
| 准确性 | 🟡 70-80% | ✅ 95-100% |
| 安全性 | ✅ 完全安全 | ⚠️ 需要注意 |
| 适用场景 | 初步评估 | 深度验证 |

**建议的测试策略:**
1. **初次评估**: 静态分析
2. **上线前验证**: 静态 + 动态
3. **持续优化**: 定期动态测试
4. **问题排查**: 动态测试定位问题

---

**更新时间:** 2026-04-23  
**文档版本:** v2.0