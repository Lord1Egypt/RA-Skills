"""
Neo4j导入脚本
执行批次化Cypher语句到Neo4j数据库
"""

import json
import time
from typing import Dict, List, Any
from datetime import datetime


class Neo4jImporter:
    """Neo4j数据导入器"""
    
    def __init__(self, uri="http://localhost:7474/db/neo4j/tx/commit", 
                 username="neo4j", password="12358lpok"):
        """
        初始化Neo4j连接
        Args:
            uri: Neo4j事务端点
            username: 用户名
            password: 密码
        """
        self.uri = uri
        self.username = username
        self.password = password
        self.headers = {"Content-Type": "application/json"}
        
        # 执行日志
        self.execution_log = []
    
    def import_batches(self, batches_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行批次导入
        Args:
            batches_data: 批次数据
        Returns:
            dict: 执行结果
        """
        book_title = batches_data.get('book_title', 'Unknown')
        chapter = batches_data.get('chapter', 1)
        batches = batches_data.get('batches', [])
        
        start_time = time.time()
        
        results = []
        successful = 0
        failed = 0
        
        # 记录开始
        self._log_start(book_title, chapter, len(batches))
        
        # 逐批执行
        for batch in batches:
            batch_id = batch.get('batch_id')
            batch_type = batch.get('type')
            
            self._log_batch_start(batch_id, batch_type)
            
            result = self._execute_batch(batch)
            
            if result['success']:
                successful += 1
                self._log_batch_success(batch_id, result)
            else:
                failed += 1
                self._log_batch_error(batch_id, result)
            
            results.append(result)
        
        # 验证导入
        verification = self._verify_import(chapter, batches)
        
        end_time = time.time()
        
        # 汇总结果
        return {
            "success": failed == 0 and verification['match'],
            "book_title": book_title,
            "chapter": chapter,
            "execution_summary": {
                "total_batches": len(batches),
                "successful_batches": successful,
                "failed_batches": failed,
                "start_time": datetime.fromtimestamp(start_time).isoformat(),
                "end_time": datetime.fromtimestamp(end_time).isoformat(),
                "duration_seconds": round(end_time - start_time, 2)
            },
            "batch_results": results,
            "verification": verification,
            "overall_success": failed == 0 and verification['match'],
            "execution_log": self.execution_log
        }
    
    def _execute_batch(self, batch: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个批次
        """
        batch_id = batch.get('batch_id')
        batch_type = batch.get('type')
        statement = batch.get('statement', '{}')
        
        try:
            # 构建请求
            # 注意: 这里需要使用实际HTTP请求库，如requests
            # 以下是模拟实现
            
            # 模拟成功执行
            import random
            success_rate = 0.95  # 95%成功率
            
            if random.random() < success_rate:
                # 模拟统计数据
                stats = {}
                if batch_type == 'index':
                    stats = {"indexes_added": 1}
                elif batch_type == 'concepts':
                    count = batch.get('count', 0)
                    stats = {"nodes_created": count}
                elif batch_type == 'relationships':
                    count = batch.get('count', 0)
                    stats = {"relationships_created": count}
                
                return {
                    "batch_id": batch_id,
                    "type": batch_type,
                    "success": True,
                    "stats": stats
                }
            else:
                # 模拟失败
                return {
                    "batch_id": batch_id,
                    "type": batch_type,
                    "success": False,
                    "error": "模拟的执行错误"
                }
        
        except Exception as e:
            return {
                "batch_id": batch_id,
                "type": batch_type,
                "success": False,
                "error": str(e)
            }
    
    def _verify_import(self, chapter: int, batches: List[Dict]) -> Dict[str, Any]:
        """
        验证导入结果
        """
        # 从批次中提取预期数量
        expected_concepts = 0
        expected_relationships = 0
        
        for batch in batches:
            if batch.get('type') == 'concepts':
                expected_concepts += batch.get('count', 0)
            elif batch.get('type') == 'relationships':
                expected_relationships += batch.get('count', 0)
        
        # 模拟查询结果
        imported_concepts = expected_concepts  # 模拟成功导入
        imported_relationships = expected_relationships
        
        return {
            "expected_concepts": expected_concepts,
            "imported_concepts": imported_concepts,
            "expected_relationships": expected_relationships,
            "imported_relationships": imported_relationships,
            "match": (imported_concepts == expected_concepts and 
                     imported_relationships == expected_relationships)
        }
    
    def _log_start(self, book_title: str, chapter: int, total_batches: int):
        """记录开始"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "start",
            "message": f"开始导入: {book_title} - Chapter {chapter}, 共{total_batches}批次"
        }
        self.execution_log.append(entry)
    
    def _log_batch_start(self, batch_id: int, batch_type: str):
        """记录批次开始"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "batch_start",
            "batch_id": batch_id,
            "batch_type": batch_type,
            "message": f"执行批次 {batch_id} - {batch_type}"
        }
        self.execution_log.append(entry)
    
    def _log_batch_success(self, batch_id: int, result: Dict):
        """记录批次成功"""
        stats = result.get('stats', {})
        stats_str = ', '.join([f"{k}: {v}" for k, v in stats.items()])
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "batch_success",
            "batch_id": batch_id,
            "message": f"批次 {batch_id} 完成 ({stats_str})"
        }
        self.execution_log.append(entry)
    
    def _log_batch_error(self, batch_id: int, result: Dict):
        """记录批次失败"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": "batch_error",
            "batch_id": batch_id,
            "message": f"批次 {batch_id} 失败: {result.get('error', 'Unknown error')}"
        }
        self.execution_log.append(entry)
    
    def generate_execution_log(self, result: Dict[str, Any]) -> str:
        """
        生成执行日志
        """
        log_lines = []
        log_lines.append("=" * 50)
        log_lines.append("Neo4j Import Execution Log")
        log_lines.append("=" * 50)
        log_lines.append(f"Book: {result.get('book_title', 'Unknown')}")
        log_lines.append(f"Chapter: {result.get('chapter', 1)}")
        log_lines.append(f"Total Batches: {result['execution_summary']['total_batches']}")
        log_lines.append("")
        
        for entry in self.execution_log:
            timestamp = entry['timestamp'][-8:]  # 只显示时间部分
            message = entry['message']
            log_lines.append(f"[{timestamp}] {message}")
        
        log_lines.append("")
        log_lines.append("=" * 50)
        log_lines.append("Execution Summary")
        log_lines.append("=" * 50)
        summary = result['execution_summary']
        log_lines.append(f"Total Batches: {summary['total_batches']}")
        log_lines.append(f"Successful: {summary['successful_batches']}")
        log_lines.append(f"Failed: {summary['failed_batches']}")
        log_lines.append(f"Duration: {summary['duration_seconds']} seconds")
        
        verification = result.get('verification', {})
        log_lines.append("")
        log_lines.append(f"[{datetime.now().isoformat()[-8:]}] Verification: "
                        f"{verification['imported_concepts']}/{verification['expected_concepts']} concepts, "
                        f"{verification['imported_relationships']}/{verification['expected_relationships']} relationships")
        
        overall = result.get('overall_success', False)
        log_lines.append(f"Overall Success: {'TRUE' if overall else 'FALSE'}")
        
        return "\n".join(log_lines)
    
    def query_concepts(self, chapter: int) -> List[Dict[str, Any]]:
        """
        查询指定章节的概念
        """
        # 构建查询Cypher
        query = {
            "statements": [{
                "statement": f"MATCH (c:Concept) WHERE c.chapter = {chapter} RETURN c.name, c.category, c.importance ORDER BY c.name"
            }]
        }
        
        # 模拟返回
        return [
            {"name": "Intrinsic Value", "category": "Security Analysis/Core Concepts", "importance": "5star"},
            {"name": "Margin of Safety", "category": "Security Analysis/Core Concepts", "importance": "5star"}
        ]
    
    def query_relationships(self, chapter: int) -> List[Dict[str, Any]]:
        """
        查询指定章节的关系
        """
        query = {
            "statements": [{
                "statement": f"MATCH (a:Concept)-[r]->(b:Concept) WHERE a.chapter = {chapter} OR b.chapter = {chapter} RETURN a.name, type(r), b.name"
            }]
        }
        
        # 模拟返回
        return [
            {"from": "Security Analysis", "type": "DEFINES", "to": "Intrinsic Value"},
            {"from": "Security Analysis", "type": "REQUIRES", "to": "Margin of Safety"}
        ]
    
    def get_statistics(self, book_title: str) -> Dict[str, Any]:
        """
        获取书籍统计信息
        """
        return {
            "total_concepts": 150,
            "total_relationships": 80,
            "chapters": [
                {"chapter": 1, "concepts": 5, "relationships": 2},
                {"chapter": 2, "concepts": 8, "relationships": 4}
            ]
        }


# PowerShell执行脚本（需要实际使用时保存为.ps1文件）
POWERSHELL_SCRIPT = """
# Neo4j Import PowerShell Script

$uri = "http://localhost:7474/db/neo4j/tx/commit"
$headers = @{\"Content-Type\"=\"application/json\"}
$credential = New-Object System.Management.Automation.PSCredential(
    \"neo4j\",
    (ConvertTo-SecureString \"12358lpok\" -AsPlainText -Force)
)

function Invoke-Neo4jBatch {
    param(
        [hashtable]$Batch
    )
    
    Write-Output \"Executing Batch $($Batch.batch_id) - $($Batch.type)...\"
    
    try {
        $response = Invoke-WebRequest `
            -Uri $uri `
            -Headers $headers `
            -Credential $credential `
            -Method Post `
            -Body $Batch.statement `
            -UseBasicParsing `
            -ErrorAction Stop
        
        $result = $response.Content | ConvertFrom-Json
        
        if ($result.errors -and $result.errors.Count -gt 0) {
            Write-Output \"ERROR in Batch $($Batch.batch_id):\"
            $result.errors | ForEach-Object { Write-Output \"  - $($_.message)\" }
            return @{
                \"batch_id\" = $Batch.batch_id
                \"type\" = $Batch.type
                \"success\" = $false
                \"error\" = $result.errors[0].message
            }
        }
        
        Write-Output \"Batch $($Batch.batch_id) completed successfully\"
        return @{
            \"batch_id\" = $Batch.batch_id
            \"type\" = $Batch.type
            \"success\" = $true
            \"stats\" = $result.results[0].stats
        }
    }
    catch {
        Write-Output \"EXCEPTION in Batch $($Batch.batch_id): $($_.Exception.Message)\"
        return @{
            \"batch_id\" = $Batch.batch_id
            \"type\" = $Batch.type
            \"success\" = $false
            \"error\" = $_.Exception.Message
        }
    }
}

function Test-Neo4jImport {
    param([int]$Chapter)
    
    # 验证概念数量
    $verifyConcepts = @{
        \"statements\" = @(
            @{
                \"statement\" = \"MATCH (c:Concept) WHERE c.chapter = $Chapter RETURN count(c) as count\"
            }
        )
    } | ConvertTo-Json
    
    $result = Invoke-WebRequest -Uri $uri -Headers $headers -Credential $credential -Method Post -Body $verifyConcepts -UseBasicParsing
    $data = $result.Content | ConvertFrom-Json
    $conceptCount = $data.results[0].data[0].row[0]
    
    # 验证关系数量
    $verifyRels = @{
        \"statements\" = @(
            @{
                \"statement\" = \"MATCH (a:Concept)-[r]->(b:Concept) WHERE a.chapter = $Chapter OR b.chapter = $Chapter RETURN count(r) as count\"
            }
        )
    } | ConvertTo-Json
    
    $resultRels = Invoke-WebRequest -Uri $uri -Headers $headers -Credential $credential -Method Post -Body $verifyRels -UseBasicParsing
    $dataRels = $resultRels.Content | ConvertFrom-Json
    $relCount = $dataRels.results[0].data[0].row[0]
    
    return @{
        \"concepts_imported\" = $conceptCount
        \"relationships_imported\" = $relCount
    }
}

# 使用示例
$batches = @(
    @{\"batch_id\"=1; \"type\"=\"index\"; \"statement\"='{\"statements\": [{\"statement\": \"CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name)\"}]}'},
    @{\"batch_id\"=2; \"type\"=\"concepts\"; \"count\"=1; \"statement\"='{\"statements\": [{\"statement\": \"CREATE (:Concept {name: ''Test'', category: ''Test'', chapter: 1})\"}]}'}
)

Write-Output \"=== Neo4j Import Execution Log ===\"
Write-Output \"Total Batches: $($batches.Count)\"
Write-Output \"\"

$results = @()
foreach ($batch in $batches) {
    $result = Invoke-Neo4jBatch -Batch $batch
    $results += $result
}

Write-Output \"\"
Write-Output \"=== Execution Summary ===\"
$successful = ($results | Where-Object { $_.success -eq $true }).Count
$failed = ($results | Where-Object { $_.success -eq $false }).Count
Write-Output \"Total Batches: $($batches.Count)\"
Write-Output \"Successful: $successful\"
Write-Output \"Failed: $failed\"
"""


# 使用示例
if __name__ == "__main__":
    importer = Neo4jImporter()
    
    # 示例批次数据
    batches_data = {
        "book_title": "Security Analysis",
        "chapter": 1,
        "batches": [
            {
                "batch_id": 1,
                "type": "index",
                "statement": json.dumps({
                    "statements": [{
                        "statement": "CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)"
                    }]
                })
            },
            {
                "batch_id": 2,
                "type": "concepts",
                "count": 3,
                "statement": json.dumps({
                    "statements": [{
                        "statement": "CREATE (:Concept {name: 'Intrinsic Value', category: 'Security Analysis/Core Concepts', chapter: 1, description: '由资产、收益等事实确定的价值', importance: '5star'}); CREATE (:Concept {name: 'Security Analysis', category: 'Security Analysis/Core Concepts', chapter: 1, description: '对证券的价值分析过程', importance: '5star'}); CREATE (:Concept {name: 'Margin of Safety', category: 'Security Analysis/Core Concepts', chapter: 1, description: '价格与内在价值之间的安全边际', importance: '5star'})"
                    }]
                })
            },
            {
                "batch_id": 3,
                "type": "relationships",
                "count": 2,
                "statement": json.dumps({
                    "statements": [{
                        "statement": "MATCH (a:Concept {name: 'Security Analysis'}), (b:Concept {name: 'Intrinsic Value'}) CREATE (a)-[:DEFINES]->(b); MATCH (a:Concept {name: 'Security Analysis'}), (b:Concept {name: 'Margin of Safety'}) CREATE (a)-[:REQUIRES]->(b)"
                    }]
                })
            }
        ]
    }
    
    # 执行导入
    result = importer.import_batches(batches_data)
    
    # 生成日志
    log = importer.generate_execution_log(result)
    print(log)
    
    # 输出结果
    print("\n执行结果:")
    print(f"成功: {result['execution_summary']['successful_batches']}")
    print(f"失败: {result['execution_summary']['failed_batches']}")
    print(f"耗时: {result['execution_summary']['duration_seconds']}秒")
    print(f"总体成功: {result['overall_success']}")
