#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Index Colourfulife2System Project Document to ChromaDB
将 Colourfulife2System 项目文档向量化并存入向量数据库
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import hashlib

try:
    from langchain_chroma import Chroma
    from langchain_core.documents import Document
    import dashscope
    from dashscope import TextEmbedding
except ImportError as e:
    print(f"[ERROR] Missing package: {e}")
    print("Run: pip install langchain-chroma dashscope langchain-core")
    sys.exit(1)


class AliyunEmbeddings:
    """Aliyun Embedding Wrapper"""
    
    def __init__(self, api_key: str, model: str = "text-embedding-v3"):
        dashscope.api_key = api_key
        self.model = model
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple documents"""
        try:
            # Batch embedding (max 25 per batch)
            all_embeddings = []
            for i in range(0, len(texts), 25):
                batch = texts[i:i+25]
                response = TextEmbedding.call(
                    model=self.model,
                    input=batch
                )
                if response.status_code == 200:
                    embeddings = [item["embedding"] for item in response.output["embeddings"]]
                    all_embeddings.extend(embeddings)
                else:
                    print(f"[ERROR] API Error: {response.code} - {response.message}")
                    return []
            return all_embeddings
        except Exception as e:
            print(f"[ERROR] Embedding Error: {e}")
            return []
    
    def embed_query(self, query: str) -> List[float]:
        """Generate query embedding"""
        result = self.embed_documents([query])
        return result[0] if result else []


class DocumentIndexer:
    """Document Indexer for ChromaDB"""
    
    def __init__(self, 
                 chroma_dir: str,
                 collection_name: str,
                 api_key: str):
        """
        Initialize Document Indexer
        
        Args:
            chroma_dir: Path to Chroma database
            collection_name: Collection name
            api_key: Aliyun API Key
        """
        self.embeddings = AliyunEmbeddings(api_key=api_key)
        
        # Initialize Chroma
        self.vectorstore = Chroma(
            persist_directory=chroma_dir,
            collection_name=collection_name,
            embedding_function=self.embeddings
        )
        
        print(f"[INFO] DocumentIndexer initialized")
        print(f"   - Chroma DB: {chroma_dir}")
        print(f"   - Collection: {collection_name}")
    
    def split_document(self, content: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """
        Split document into chunks
        
        Args:
            content: Document content
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
        
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        content_length = len(content)
        
        while start < content_length:
            end = start + chunk_size
            chunk = content[start:end]
            chunks.append(chunk)
            start = end - chunk_overlap
        
        return chunks
    
    def index_document(self, 
                      doc_id: str,
                      title: str,
                      content: str,
                      metadata: Dict[str, Any] = None) -> int:
        """
        Index a document
        
        Args:
            doc_id: Document ID
            title: Document title
            content: Document content
            metadata: Additional metadata
        
        Returns:
            Number of chunks indexed
        """
        # Split document
        chunks = self.split_document(content)
        print(f"[INFO] Split document into {len(chunks)} chunks")
        
        # Create documents
        documents = []
        for i, chunk in enumerate(chunks):
            doc_metadata = {
                "doc_id": doc_id,
                "title": title,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "type": "project_document",
                "date": "2026-03-13",
                **(metadata or {})
            }
            
            documents.append(
                Document(
                    page_content=chunk,
                    metadata=doc_metadata
                )
            )
        
        # Add to vectorstore
        try:
            self.vectorstore.add_documents(documents)
            print(f"[SUCCESS] Indexed {len(documents)} chunks for document '{title}'")
            return len(documents)
        except Exception as e:
            print(f"[ERROR] Failed to index document: {e}")
            return 0
    
    def index_sections(self,
                      doc_id: str,
                      title: str,
                      sections: Dict[str, str],
                      metadata: Dict[str, Any] = None) -> int:
        """
        Index document by sections
        
        Args:
            doc_id: Document ID
            title: Document title
            sections: Dict of section_name -> content
            metadata: Additional metadata
        
        Returns:
            Total number of chunks indexed
        """
        total_chunks = 0
        
        for section_name, content in sections.items():
            print(f"\n[INFO] Indexing section: {section_name}")
            
            section_metadata = {
                "section": section_name,
                **(metadata or {})
            }
            
            chunks = self.split_document(content, chunk_size=800, chunk_overlap=150)
            print(f"   Split into {len(chunks)} chunks")
            
            documents = []
            for i, chunk in enumerate(chunks):
                doc_metadata = {
                    "doc_id": doc_id,
                    "title": title,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "type": "project_document",
                    "date": "2026-03-13",
                    "section": section_name,
                    **(metadata or {})
                }
                
                documents.append(
                    Document(
                        page_content=chunk,
                        metadata=doc_metadata
                    )
                )
            
            try:
                self.vectorstore.add_documents(documents)
                print(f"   ✓ Indexed {len(documents)} chunks")
                total_chunks += len(documents)
            except Exception as e:
                print(f"   ✗ Error: {e}")
        
        return total_chunks


def main():
    """Main function"""
    print("=" * 70)
    print("Colourfulife2System Project Document Indexer")
    print("Colourfulife2System 项目文档向量化索引")
    print("=" * 70)
    
    # Configuration
    api_key = os.getenv("ALIYUN_API_KEY")
    if not api_key:
        print("[ERROR] ALIYUN_API_KEY environment variable not set")
        sys.exit(1)
    
    chroma_dir = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")
    collection_name = "colourfulife2system_project"
    
    # Document content (from Feishu doc)
    doc_id = "colourfulife2system_project_init"
    doc_title = "Colourfulife2System 项目立项文档"
    
    # Project document sections
    sections = {
        "项目概述": """
Colourfulife2System 是一个宏大的企业级数据智能系统项目，旨在打通系统后台数据库到用户端的直接访问，实现数据民主化和智能化。

核心定位：
- 企业数据中枢 - 成为社会运转的大脑体系
- 透明盒子 - 逻辑来自用户，代码公开透明
- 零数据团队 - 企业不需要专门的数据团队
- 多源兼容 - 兼容各种数据库和数据载体

与 Colourfulife 项目关系：
- Colourfulife：标准化卡片工具（前端交互层）
- Colourfulife2System：完整的数据智能系统（后端 + 前端 + 智能层）
""",
        
        "项目愿景": """
核心愿景：打造一个透明、开放、智能的数据访问和处理系统，让每个企业都能轻松访问和利用自己的数据资产。

愿景细节：
- 数据库兼容：打通系统后台数据库到用户端的直接访问，兼容 MySQL/SQL Server 等各种数据库
- 载体兼容：兼容飞书多维表、设备扫描等各种数据载体
- 统一架构：整合到统一知识库架构，形成单一事实来源
- RAG 支持：支持 RAG 访问和查询，实现自然语言交互
- 业务逻辑：支持环比/同比/增长速度等业务逻辑加工
- 零门槛：企业不需要数据团队，业务人员即可使用
- 透明公开：透明盒子，逻辑来自用户，代码公开透明
- 区块链接入：未来接入区块链网络，实现数据可信存证
- 社会大脑：成为社会运转的大脑体系

长期目标：
- 短期（1 年）：完成核心功能开发，支持主流数据库和飞书多维表
- 中期（3 年）：形成完整生态，接入 1000+ 企业
- 长期（5 年）：成为社会级数据基础设施，接入区块链网络
""",
        
        "核心场景": """
场景一：企业数据查询
- 用户用自然语言查询销售数据，不需要学习 SQL
- 流程：用户提问 → RAG 理解意图 → 生成查询 → 执行数据库 → 返回结果 → 可视化展示
- 示例："上个月 A 产品的销售额是多少？"、"对比一下今年和去年的同比增长率"

场景二：多源数据整合
- 整合来自 MySQL 数据库、飞书多维表和 Excel 的数据，形成统一视图
- 数据源 → 统一数据模型 → 统一知识库 → RAG 查询层

场景三：业务逻辑自动化
- 自动计算环比、同比、增长速度等指标
- 支持的计算类型：环比（MoM）、同比（YoY）、增长速度（CAGR）、自定义指标

场景四：设备扫描数据接入
- 扫描设备录入数据，实时查询库存状态
- 支持二维码、条形码、RFID 等多种扫描方式

场景五：区块链存证（未来）
- 关键数据哈希上链，智能合约自动执行，去中心化数据验证
""",
        
        "核心能力": """
数据接入能力：
- MySQL、SQL Server、PostgreSQL、飞书多维表、Excel/CSV、API 接口、设备扫描

数据处理能力：
- 数据清洗、数据转换 ETL、数据标准化、实时处理

智能查询能力：
- 自然语言查询、语义理解、智能推荐、多轮对话

业务逻辑能力：
- 环比计算、同比计算、趋势分析、自定义公式

可视化能力：
- 图表展示、仪表盘、报告生成、数据导出
""",
        
        "技术架构": """
整体架构分层：
1. 数据源层：MySQL、SQL Server、PostgreSQL、飞书多维表、Excel/CSV、设备扫描
2. 数据接入层：数据库连接器、API 网关、文件解析器、扫描设备接口
3. 数据处理层：数据清洗、数据转换 ETL、数据标准化、实时处理
4. 统一知识库：关系型存储、向量数据库 ChromaDB、缓存层 Redis
5. 智能服务层：RAG 查询引擎、业务逻辑引擎、自然语言理解、智能推荐
6. 应用层：Web 界面、API 接口、移动端、Colourfulife 卡片
7. 区块链层（未来）：数据哈希上链、智能合约、去中心化验证

技术栈选型：
- 后端框架：Python FastAPI
- 数据库连接：SQLAlchemy + PyODBC
- 向量数据库：ChromaDB
- Embedding：阿里云通义千问
- LLM：阿里云 Qwen
- 缓存：Redis
- 消息队列：Apache Kafka
- ETL：Apache Airflow
- 前端：React + ECharts
- 部署：Docker + K8s
""",
        
        "实施路线": """
第一阶段：基础建设（2026-03-13 至 2026-04-30）
- 需求分析（30 天）
- 技术选型（20 天）
- 架构设计（30 天）

第二阶段：核心开发（2026-04-15 至 2026-06-30）
- 数据库连接器（45 天）
- RAG 引擎开发（60 天）
- 业务逻辑引擎（45 天）

第三阶段：集成测试（2026-07-01 至 2026-08-31）
- 系统集成（30 天）
- 测试优化（45 天）
- 用户验收（30 天）

第四阶段：上线运营（2026-09-01 至 2027-02-28）
- 试点上线（30 天）
- 全面推广（60 天）
- 持续优化（90 天）

关键里程碑：
- 项目立项：2026-03-13
- MVP 完成：2026-06-30
- 试点上线：2026-09-30
- 版本 1.0：2027-02-28
""",
        
        "预期价值": """
商业价值：
- 降低成本：企业无需组建数据团队，节省人力成本 80%+
- 提升效率：数据查询从小时级降至分钟级，效率提升 10 倍+
- 降低门槛：业务人员可直接查询数据，数据使用率提升 5 倍
- 决策支持：实时数据支持快速决策，决策速度提升 3 倍

技术价值：
- 技术积累：形成完整的数据智能技术栈
- 开源贡献：核心模块开源，建立影响力
- 生态建设：吸引开发者共建生态
- 标准制定：参与行业标准制定

社会价值：
- 数据民主化：让每个企业都能利用数据
- 透明公开：代码开源，逻辑透明
- 就业影响：降低数据岗位门槛
- 产业升级：推动企业数字化转型

投资回报：
- 投资回收期：2.5 年
- 5 年累计 ROI：5700%
- IRR（内部收益率）：85%
""",
        
        "风险与挑战": """
技术风险：
- 数据库兼容性（中概率，高影响）
- 性能瓶颈（中概率，高影响）
- 数据安全问题（低概率，极高影响）
- AI 准确性（中概率，中影响）

市场风险：
- 竞争激烈（高概率，中影响）
- 需求变化（中概率，中影响）
- 市场接受度（中概率，高影响）

运营风险：
- 团队稳定性（低概率，高影响）
- 资金链（低概率，极高影响）
- 法律合规（中概率，高影响）

应对策略：
- 建立技术委员会，定期评审技术方案
- 关键模块双备份，降低单点故障
- 建立完善的监控和告警体系
- 深入调研目标用户，精准定位
- 快速迭代，小步快跑验证需求
""",
    }
    
    # Initialize indexer
    print(f"\n[INFO] Initializing DocumentIndexer...")
    indexer = DocumentIndexer(
        chroma_dir=chroma_dir,
        collection_name=collection_name,
        api_key=api_key
    )
    
    # Index sections
    print(f"\n[INFO] Starting to index document sections...")
    total_chunks = indexer.index_sections(
        doc_id=doc_id,
        title=doc_title,
        sections=sections,
        metadata={
            "project": "Colourfulife2System",
            "version": "v1.0",
            "status": "project_initiation",
            "url": "https://feishu.cn/docx/AjXmdOb27oPjQHxVr5wcYwP9nte"
        }
    )
    
    print(f"\n" + "=" * 70)
    print(f"[SUCCESS] Document indexing complete!")
    print(f"   - Document: {doc_title}")
    print(f"   - Total chunks indexed: {total_chunks}")
    print(f"   - Collection: {collection_name}")
    print(f"   - Chroma DB: {chroma_dir}")
    print("=" * 70)
    
    # Test search
    print(f"\n[INFO] Testing search functionality...")
    try:
        from skills.rag_search.src.search import MemorySearcher
        
        searcher = MemorySearcher(
            chroma_dir=chroma_dir,
            collection_name=collection_name,
            api_key=api_key
        )
        
        test_query = "Colourfulife2System 项目愿景"
        results = searcher.search(test_query, k=3)
        
        print(f"\n[TEST] Query: '{test_query}'")
        if results:
            print(f"   Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"   {i}. [{result['section']}] (similarity: {result['similarity']})")
                print(f"      {result['preview'][:100]}...")
        else:
            print("   No results found")
        
    except Exception as e:
        print(f"[WARN] Search test failed: {e}")
    
    print(f"\n[INFO] All done! ✨")


if __name__ == "__main__":
    main()
