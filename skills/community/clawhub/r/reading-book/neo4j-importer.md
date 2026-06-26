# 🔌 Neo4j导入技能 (Neo4j Importer Skill)

> **创建日期**: 2026-03-22
> **版本**: 1.0
> **用途**: 执行批次化Cypher语句到Neo4j数据库
> **标签**: #Neo4j #数据导入 #验证 #批次执行

---

## 🎯 核心职责

接收批次化的Cypher语句，按顺序逐批执行导入到Neo4j数据库，并验证每批次的执行结果。

---

## 📋 操作流程

### Step 1: 接收批次数据

**输入格式**:
```json
{
  "book_title": "Security Analysis",
  "chapter": 1,
  "batches": [
    {
      "batch_id": 1,
      "type": "index",
      "cypher": "CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name)",
      "statement": "{\"statements\": [{\"statement\": \"CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name)\"}]}"
    },
    {
      "batch_id": 2,
      "type": "concepts",
      "count": 3,
      "cypher": "CREATE (:Concept {name: 'A'...}); CREATE (:Concept {name: 'B'...})",
      "statement": "{\"statements\": [{\"statement\": \"...\"}]}"
    }
  ],
  "total_batches": 5,
  "total_concepts": 5,
  "total_relationships": 3
}
```

---

### Step 2: 配置Neo4j连接

**连接参数**:
```powershell
$uri = "http://localhost:7474/db/neo4j/tx/commit"
$headers = @{"Content-Type"="application/json"}
$credential = New-Object System.Management.Automation.PSCredential(
    "neo4j",
    (ConvertTo-SecureString "12358lpok" -AsPlainText -Force)
)
```

---

### Step 3: 逐批执行导入

**执行流程**:
```powershell
function Invoke-Neo4jBatch {
    param(
        [string]$Uri,
        [hashtable]$Headers,
        [PSCredential]$Credential,
        [hashtable]$Batch
    )

    Write-Output "Executing Batch $($Batch.batch_id) - $($Batch.type)..."

    try {
        $response = Invoke-WebRequest `
            -Uri $Uri `
            -Headers $Headers `
            -Credential $Credential `
            -Method Post `
            -Body $Batch.statement `
            -UseBasicParsing

        $result = $response.Content | ConvertFrom-Json

        # 检查是否有错误
        if ($result.errors -and $result.errors.Count -gt 0) {
            Write-Output "ERROR in Batch $($Batch.batch_id):"
            $result.errors | ForEach-Object { Write-Output "  - $($_.message)" }
            return @{
                "batch_id" = $Batch.batch_id
                "type" = $Batch.type
                "success" = $false
                "error" = $result.errors[0].message
            }
        }

        Write-Output "Batch $($Batch.batch_id) completed successfully"
        return @{
            "batch_id" = $Batch.batch_id
            "type" = $Batch.type
            "success" = $true
            "stats" = $result.results[0].stats
        }
    }
    catch {
        Write-Output "EXCEPTION in Batch $($Batch.batch_id): $($_.Exception.Message)"
        return @{
            "batch_id" = $Batch.batch_id
            "type" = $Batch.type
            "success" = $false
            "error" = $_.Exception.Message
        }
    }
}
```

**批次执行顺序**:
1. **索引批次** (batch_id 1)
2. **概念批次** (batch_id 2, 3, ...)
3. **关系批次** (最后几个batch_id)

---

### Step 4: 验证导入结果

**验证查询**:
```powershell
function Test-Neo4jImport {
    param(
        [string]$Uri,
        [hashtable]$Headers,
        [PSCredential]$Credential,
        [int]$Chapter
    )

    # 验证概念数量
    $verifyConcepts = @{
        "statements" = @(
            @{
                "statement" = "MATCH (c:Concept) WHERE c.chapter = $Chapter RETURN count(c) as count"
            }
        )
    } | ConvertTo-Json

    $result = Invoke-WebRequest `
        -Uri $Uri `
        -Headers $Headers `
        -Credential $Credential `
        -Method Post `
        -Body $verifyConcepts `
        -UseBasicParsing

    $data = $result.Content | ConvertFrom-Json
    $conceptCount = $data.results[0].data[0].row[0]

    # 验证关系数量
    $verifyRels = @{
        "statements" = @(
            @{
                "statement" = "MATCH (a:Concept)-[r]->(b:Concept) WHERE a.chapter = $Chapter OR b.chapter = $Chapter RETURN count(r) as count"
            }
        )
    } | ConvertTo-Json

    $resultRels = Invoke-WebRequest `
        -Uri $Uri `
        -Headers $Headers `
        -Credential $Credential `
        -Method Post `
        -Body $verifyRels `
        -UseBasicParsing

    $dataRels = $resultRels.Content | ConvertFrom-Json
    $relCount = $dataRels.results[0].data[0].row[0]

    return @{
        "concepts_imported" = $conceptCount
        "relationships_imported" = $relCount
    }
}
```

---

### Step 5: 生成执行报告

**输出格式**:
```json
{
  "book_title": "Security Analysis",
  "chapter": 1,
  "execution_summary": {
    "total_batches": 5,
    "successful_batches": 5,
    "failed_batches": 0,
    "start_time": "2026-03-22T18:30:00Z",
    "end_time": "2026-03-22T18:30:05Z",
    "duration_seconds": 5
  },
  "batch_results": [
    {
      "batch_id": 1,
      "type": "index",
      "success": true,
      "stats": {
        "indexes_added": 2
      }
    },
    {
      "batch_id": 2,
      "type": "concepts",
      "success": true,
      "stats": {
        "nodes_created": 3
      }
    },
    {
      "batch_id": 3,
      "type": "concepts",
      "success": true,
      "stats": {
        "nodes_created": 2
      }
    },
    {
      "batch_id": 4,
      "type": "relationships",
      "success": true,
      "stats": {
        "relationships_created": 2
      }
    },
    {
      "batch_id": 5,
      "type": "relationships",
      "success": true,
      "stats": {
        "relationships_created": 1
      }
    }
  ],
  "verification": {
    "expected_concepts": 5,
    "imported_concepts": 5,
    "expected_relationships": 3,
    "imported_relationships": 3,
    "match": true
  },
  "overall_success": true
}
```

---

## 📊 执行日志格式

**控制台输出**:
```powershell
=== Neo4j Import Execution Log ===
Book: Security Analysis
Chapter: 1
Total Batches: 5

[18:30:00] Executing Batch 1 - index...
[18:30:00] Batch 1 completed successfully (indexes_added: 2)

[18:30:01] Executing Batch 2 - concepts...
[18:30:01] Batch 2 completed successfully (nodes_created: 3)

[18:30:02] Executing Batch 3 - concepts...
[18:30:02] Batch 3 completed successfully (nodes_created: 2)

[18:30:03] Executing Batch 4 - relationships...
[18:30:03] Batch 4 completed successfully (relationships_created: 2)

[18:30:04] Executing Batch 5 - relationships...
[18:30:04] Batch 5 completed successfully (relationships_created: 1)

[18:30:05] Verifying import...
[18:30:05] Verification: 5/5 concepts imported, 3/3 relationships imported

=== Execution Summary ===
Total Batches: 5
Successful: 5
Failed: 0
Duration: 5 seconds
Overall Success: TRUE
```

---

## 🔧 错误处理

### 常见错误类型

| 错误类型 | 检测方式 | 处理策略 |
|---------|---------|---------|
| **连接失败** | 无法连接到Neo4j | 返回连接错误，提示检查服务状态 |
| **认证失败** | 401 Unauthorized | 返回认证错误，提示检查密码 |
| **Cypher语法错误** | errors数组非空 | 停止执行，返回具体错误信息 |
| **节点已存在** | ConstraintViolationError | 记录警告但继续执行 |
| **参数过长** | HTTP 414或类似 | 返回批次过大错误，建议重新分批 |

### 错误恢复策略

**策略1: 停止并报告**
- 用于严重错误（连接失败、认证失败）
- 返回完整错误信息
- 不执行后续批次

**策略2: 记录并继续**
- 用于非致命错误（节点已存在）
- 记录警告信息
- 继续执行后续批次

**策略3: 重试机制**
- 用于网络抖动等临时错误
- 每批次最多重试3次
- 间隔1秒

---

## ✅ 质量检查清单

### 执行前检查
- [ ] Neo4j服务运行正常
- [ ] 连接参数正确（URI、用户名、密码）
- [ ] 输入的batches数组完整
- [ ] batch_id连续无重复

### 执行中检查
- [ ] 每批次执行后检查response
- [ ] 记录每批次的执行结果
- [ ] 捕获并记录异常

### 执行后验证
- [ ] 验证概念数量与预期一致
- [ ] 验证关系数量与预期一致
- [ ] 验证索引已创建
- [ ] 测试查询功能正常

---

## 🎓 使用示例

**输入**:
```json
{
  "book_title": "Security Analysis",
  "chapter": 1,
  "batches": [
    {
      "batch_id": 1,
      "type": "index",
      "statement": "{\"statements\": [{\"statement\": \"CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name)\"}]}"
    },
    {
      "batch_id": 2,
      "type": "concepts",
      "statement": "{\"statements\": [{\"statement\": \"CREATE (:Concept {name: 'Intrinsic Value', category: 'Security Analysis/Core Concepts', chapter: 1, description: '由资产、收益等事实确定的价值', importance: '5star'})\"}]}"
    }
  ],
  "total_batches": 2,
  "total_concepts": 1,
  "total_relationships": 0
}
```

**输出**:
```json
{
  "book_title": "Security Analysis",
  "chapter": 1,
  "execution_summary": {
    "total_batches": 2,
    "successful_batches": 2,
    "failed_batches": 0,
    "duration_seconds": 2
  },
  "batch_results": [
    {
      "batch_id": 1,
      "type": "index",
      "success": true,
      "stats": {"indexes_added": 1}
    },
    {
      "batch_id": 2,
      "type": "concepts",
      "success": true,
      "stats": {"nodes_created": 1}
    }
  ],
  "verification": {
    "expected_concepts": 1,
    "imported_concepts": 1,
    "expected_relationships": 0,
    "imported_relationships": 0,
    "match": true
  },
  "overall_success": true
}
```

---

## 🔄 与其他模块的接口

**上游模块**:
- `neo4j-cypher-generator`: 接收batches列表

**下游模块**:
- `book-learning-coordinator`: 接收执行报告用于进度更新

---

## 📝 Neo4j查询工具函数

**常用查询**:
```powershell
# 查询某章节的所有概念
$query = @{
    "statements" = @(
        @{
            "statement" = "MATCH (c:Concept) WHERE c.chapter = 1 RETURN c.name, c.category, c.importance"
        }
    )
}

# 查询概念之间的关系
$query = @{
    "statements" = @(
        @{
            "statement" = "MATCH (a:Concept)-[r]->(b:Concept) WHERE a.chapter = 1 OR b.chapter = 1 RETURN a.name, type(r), b.name"
        }
    )
}

# 统计每个章节的概念数
$query = @{
    "statements" = @(
        @{
            "statement" = "MATCH (c:Concept) RETURN c.chapter as chapter, count(c) as concepts ORDER BY chapter"
        }
    )
}
```

---

## ⚠️ 注意事项

1. **批次顺序**: 必须先执行索引批次，再执行概念批次，最后执行关系批次
2. **幂等性**: 使用CREATE INDEX IF NOT EXISTS和IF NOT EXISTS确保幂等
3. **错误隔离**: 单批次失败不应影响其他批次（除非是索引批次）
4. **性能**: 大批量导入时考虑在导入前禁用约束，导入后重建

---

## 🛠️ OpenClaw 脚本配置

**脚本文件**: `neo4j-importer-script.py`
**脚本类型**: Python
**调用方式**: 外部工具
**依赖**: 需要先执行 neo4j-cypher-generator-script.py 获取批次数据

### 执行命令
```bash
python neo4j-importer-script.py --batches_data <JSON数据>
```

### 输入参数
```json
{
  "book_title": "Security Analysis",
  "chapter": 1,
  "batches": [
    {
      "batch_id": 1,
      "type": "index",
      "statement": "{\"statements\": [{\"statement\": \"CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name)\"}]}"
    },
    {
      "batch_id": 2,
      "type": "concepts",
      "statement": "{\"statements\": [{\"statement\": \"CREATE (:Concept {name: 'Intrinsic Value', category: 'Security Analysis/Core Concepts', chapter: 1, description: '由资产、收益等事实确定的价值', importance: '5star'})\"}]}"
    }
  ],
  "total_batches": 2,
  "total_concepts": 1,
  "total_relationships": 0
}
```

### 输出格式
```json
{
  "success": true,
  "book_title": "Security Analysis",
  "chapter": 1,
  "execution_summary": {
    "total_batches": 2,
    "successful_batches": 2,
    "failed_batches": 0,
    "start_time": "2026-03-22T18:30:00Z",
    "end_time": "2026-03-22T18:30:02Z",
    "duration_seconds": 2
  },
  "batch_results": [
    {
      "batch_id": 1,
      "type": "index",
      "success": true,
      "stats": {"indexes_added": 1}
    },
    {
      "batch_id": 2,
      "type": "concepts",
      "success": true,
      "stats": {"nodes_created": 1}
    }
  ],
  "verification": {
    "expected_concepts": 1,
    "imported_concepts": 1,
    "expected_relationships": 0,
    "imported_relationships": 0,
    "match": true
  },
  "overall_success": true,
  "execution_log": [...]
}
```

### OpenClaw 调用逻辑
1. 接收批次数据（来自 neo4j-cypher-generator）
2. 连接到Neo4j数据库
3. 按顺序逐批执行Cypher语句
4. 验证每批次的执行结果
5. 执行导入验证查询
6. 生成执行日志和报告
7. 返回执行结果

### 错误处理
- 连接失败 → 提示检查Neo4j服务状态
- 认证失败 → 提示检查用户名密码
- 批次执行失败 → 记录错误，决定是否继续
- 验证不匹配 → 返回详细差异信息

---

_Neo4j Importer v1.0 · 2026-03-22_ 🔌
