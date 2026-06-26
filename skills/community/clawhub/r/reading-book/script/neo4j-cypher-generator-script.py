"""
Neo4j Cypher生成脚本
将概念列表转换为分批次的Neo4j Cypher语句
"""

import json
from typing import Dict, List, Any


class Neo4jCypherGenerator:
    """Neo4j Cypher语句生成器"""
    
    def __init__(self):
        self.batch_size_concepts = 4  # 每批3-5个概念
        self.batch_size_relationships = 2  # 每批2-3个关系
    
    def escape_single_quote(self, text: str) -> str:
        """
        转义单引号
        Args:
            text: 原始文本
        Returns:
            str: 转义后的文本
        """
        return text.replace("'", "\\'")
    
    def generate_batches(self, concepts_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        构建批次化Cypher语句
        Args:
            concepts_data: 概念数据
                {
                    "book_title": str,
                    "chapter": int,
                    "concepts": list,
                    "relationships": list
                }
        Returns:
            dict: 批次化结果
        """
        book_title = concepts_data.get('book_title', 'Unknown')
        chapter = concepts_data.get('chapter', 1)
        concepts = concepts_data.get('concepts', [])
        relationships = concepts_data.get('relationships', [])
        
        batches = []
        batch_id = 1
        
        # Batch 1: 创建索引（单独）
        batches.append(self._create_index_batch(batch_id))
        batch_id += 1
        
        # Batches: 创建概念（每批3-5个）
        concept_batches = [concepts[i:i+self.batch_size_concepts] 
                          for i in range(0, len(concepts), self.batch_size_concepts)]
        
        for batch_concepts in concept_batches:
            if batch_concepts:
                batch = self._create_concept_batch(batch_id, batch_concepts, chapter)
                batches.append(batch)
                batch_id += 1
        
        # Batches: 创建关系（每批2-3个）
        rel_batches = [relationships[i:i+self.batch_size_relationships] 
                      for i in range(0, len(relationships), self.batch_size_relationships)]
        
        for batch_rels in rel_batches:
            if batch_rels:
                batch = self._create_relationship_batch(batch_id, batch_rels)
                batches.append(batch)
                batch_id += 1
        
        # 统计信息
        total_concepts = len(concepts)
        total_relationships = len(relationships)
        
        return {
            "success": True,
            "book_title": book_title,
            "chapter": chapter,
            "batches": batches,
            "total_batches": len(batches),
            "total_concepts": total_concepts,
            "total_relationships": total_relationships
        }
    
    def _create_index_batch(self, batch_id: int) -> Dict[str, Any]:
        """
        创建索引批次
        """
        cypher = "CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.name); CREATE INDEX IF NOT EXISTS FOR (c:Concept) ON (c.category)"
        statement = json.dumps({
            "statements": [{
                "statement": cypher
            }]
        })
        
        return {
            "batch_id": batch_id,
            "type": "index",
            "cypher": cypher,
            "statement": statement
        }
    
    def _create_concept_batch(self, batch_id: int, concepts: List[Dict], chapter: int) -> Dict[str, Any]:
        """
        创建概念批次
        """
        cypher_statements = []
        
        for concept in concepts:
            # 构建属性
            props = [
                f"name: '{self.escape_single_quote(concept['name'])}'",
                f"category: '{self.escape_single_quote(concept.get('category', 'Unknown'))}'",
                f"chapter: {chapter}"
            ]
            
            # 添加可选属性
            if concept.get('description'):
                props.append(f"description: '{self.escape_single_quote(concept['description'])}'")
            
            if concept.get('formula'):
                props.append(f"formula: '{self.escape_single_quote(concept['formula'])}'")
            
            if concept.get('importance'):
                props.append(f"importance: '{concept['importance']}'")
            
            if concept.get('author_quote'):
                props.append(f"author_quote: '{self.escape_single_quote(concept['author_quote'])}'")
            
            # 构建CREATE语句
            props_str = ', '.join(props)
            cypher_statements.append(f"CREATE (:Concept {{{props_str}}})")
        
        # 合并所有语句
        cypher = "; ".join(cypher_statements)
        
        # 构建JSON statement
        statement = json.dumps({
            "statements": [{
                "statement": cypher
            }]
        })
        
        return {
            "batch_id": batch_id,
            "type": "concepts",
            "count": len(concepts),
            "cypher": cypher,
            "statement": statement
        }
    
    def _create_relationship_batch(self, batch_id: int, relationships: List[Dict]) -> Dict[str, Any]:
        """
        创建关系批次
        """
        cypher_statements = []
        
        for rel in relationships:
            from_name = self.escape_single_quote(rel.get('from', ''))
            to_name = self.escape_single_quote(rel.get('to', ''))
            rel_type = rel.get('type', 'RELATED_TO')
            
            # 使用MATCH-CREATE模式
            cypher_statements.append(
                f"MATCH (a:Concept {{name: '{from_name}'}}), (b:Concept {{name: '{to_name}'}}) "
                f"CREATE (a)-[:{rel_type}]->(b)"
            )
        
        # 合并所有语句
        cypher = "; ".join(cypher_statements)
        
        # 构建JSON statement
        statement = json.dumps({
            "statements": [{
                "statement": cypher
            }]
        })
        
        return {
            "batch_id": batch_id,
            "type": "relationships",
            "count": len(relationships),
            "cypher": cypher,
            "statement": statement
        }
    
    def generate_batch_summary(self, batches_result: Dict[str, Any]) -> str:
        """
        生成批次统计表格
        """
        summary = "| 批次ID | 类型 | 数量 | Cypher预览 |\n"
        summary += "|--------|------|------|-----------|\n"
        
        for batch in batches_result.get('batches', []):
            batch_id = batch['batch_id']
            batch_type = batch['type']
            count = batch.get('count', 0)
            
            # 预览（截取前80个字符）
            cypher_preview = batch['cypher'][:80] + '...' if len(batch['cypher']) > 80 else batch['cypher']
            cypher_preview = cypher_preview.replace('|', '\\|')  # 转义Markdown表格
            
            # 类型显示
            type_display = {
                'index': '索引',
                'concepts': '概念',
                'relationships': '关系'
            }.get(batch_type, batch_type)
            
            # 数量显示
            count_display = count if count > 0 else '-'
            
            summary += f"| {batch_id} | {type_display} | {count_display} | `{cypher_preview}` |\n"
        
        summary += f"\n**总计**: {batches_result['total_batches']}批次, "
        summary += f"{batches_result['total_concepts']}概念, "
        summary += f"{batches_result['total_relationships']}关系\n"
        
        return summary
    
    def validate_batch_syntax(self, batch: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证批次语法
        """
        issues = []
        
        # 检查必填字段
        required_fields = ['batch_id', 'type', 'cypher', 'statement']
        for field in required_fields:
            if field not in batch:
                issues.append(f"缺少必填字段: {field}")
        
        # 检查statement是否为有效JSON
        try:
            statement_json = json.loads(batch['statement'])
            if 'statements' not in statement_json:
                issues.append("statement中缺少statements字段")
            elif len(statement_json['statements']) == 0:
                issues.append("statements数组为空")
        except json.JSONDecodeError:
            issues.append("statement不是有效的JSON")
        
        # 检查引号使用
        if batch.get('type') in ['concepts', 'relationships']:
            cypher = batch.get('cypher', '')
            if '"' in cypher:
                issues.append("Cypher语句中使用了双引号，应该使用单引号")
        
        # 检查批次大小
        if batch.get('type') == 'concepts':
            count = batch.get('count', 0)
            if count > 5:
                issues.append(f"概念批次过大: {count}个概念，建议不超过5个")
        
        if batch.get('type') == 'relationships':
            count = batch.get('count', 0)
            if count > 3:
                issues.append(f"关系批次过大: {count}个关系，建议不超过3个")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }
    
    def validate_all_batches(self, batches_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证所有批次
        """
        all_issues = []
        valid_count = 0
        
        for batch in batches_result.get('batches', []):
            validation = self.validate_batch_syntax(batch)
            if validation['valid']:
                valid_count += 1
            else:
                all_issues.extend([
                    f"批次{batch['batch_id']}: {issue}" 
                    for issue in validation['issues']
                ])
        
        return {
            "all_valid": len(all_issues) == 0,
            "valid_batches": valid_count,
            "total_batches": len(batches_result.get('batches', [])),
            "issues": all_issues
        }


# 使用示例
if __name__ == "__main__":
    generator = Neo4jCypherGenerator()
    
    # 示例概念数据
    concepts_data = {
        "book_title": "Security Analysis",
        "chapter": 1,
        "concepts": [
            {
                "name": "Intrinsic Value",
                "category": "Security Analysis/Core Concepts",
                "chapter": 1,
                "description": "由资产、收益、股息等事实确定的内在价值",
                "importance": "5star",
                "author_quote": "The intrinsic value of a business is determined by its assets, earnings, dividends and definite future prospects."
            },
            {
                "name": "Security Analysis",
                "category": "Security Analysis/Core Concepts",
                "chapter": 1,
                "description": "对证券的价值分析过程",
                "importance": "5star"
            },
            {
                "name": "Margin of Safety",
                "category": "Security Analysis/Core Concepts",
                "chapter": 1,
                "description": "价格与内在价值之间的安全边际",
                "importance": "5star"
            },
            {
                "name": "Market Price",
                "category": "Security Analysis/Market",
                "chapter": 1,
                "description": "证券的市场交易价格",
                "importance": "4star"
            },
            {
                "name": "Book Value",
                "category": "Security Analysis/Valuation",
                "chapter": 1,
                "description": "基于资产的账面价值",
                "importance": "4star"
            }
        ],
        "relationships": [
            {
                "from": "Security Analysis",
                "to": "Intrinsic Value",
                "type": "DEFINES",
                "description": "Security analysis defines intrinsic value"
            },
            {
                "from": "Security Analysis",
                "to": "Margin of Safety",
                "type": "REQUIRES",
                "description": "Security analysis requires margin of safety"
            },
            {
                "from": "Intrinsic Value",
                "to": "Book Value",
                "type": "RELATED_TO",
                "description": "Intrinsic value related to book value"
            }
        ]
    }
    
    # 生成批次
    result = generator.generate_batches(concepts_data)
    
    if result['success']:
        print(f"成功生成 {result['total_batches']} 个批次")
        print(f"总概念数: {result['total_concepts']}")
        print(f"总关系数: {result['total_relationships']}")
        
        # 生成统计表格
        print("\n批次统计:")
        print(generator.generate_batch_summary(result))
        
        # 验证批次
        validation = generator.validate_all_batches(result)
        if validation['all_valid']:
            print("✅ 所有批次验证通过")
        else:
            print("❌ 发现问题:")
            for issue in validation['issues']:
                print(f"  - {issue}")
    else:
        print("批次生成失败!")
