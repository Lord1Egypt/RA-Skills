# RAG Pipeline Starter

Production-grade RAG pipeline setup with chunking strategies, embedding benchmarks, and retrieval tuning for 50K-500K row datasets.

## Overview

This skill provides a complete toolkit for building and optimizing RAG (Retrieval-Augmented Generation) pipelines. It analyzes your data, recommends optimal chunking strategies, benchmarks embedding models, and helps tune retrieval parameters for maximum accuracy.

## When to Use

- Building a new RAG system from scratch
- Optimizing an existing RAG pipeline's retrieval quality
- Choosing the right embedding model for your domain
- Processing large document collections (50K-500K rows)
- Need to balance speed vs. accuracy for your use case

## Scripts

### chunking_analyzer.py
Analyzes documents and recommends optimal chunking strategies based on content structure.

**Usage:**
```bash
# Assess data and get strategy recommendation
python chunking_analyzer.py --assess ./data

# Apply chunking strategy to documents
python chunking_analyzer.py --strategy recursive --input ./data/doc.txt --output ./chunks/ --chunk-size 500 --overlap 50
```

**Options:**
- `--assess <dir>` - Analyze documents and recommend strategy
- `--strategy <name>` - Chunking strategy: fixed, semantic, recursive, hierarchical
- `--input <path>` - Input file or directory
- `--output <dir>` - Output directory for chunks
- `--chunk-size <int>` - Chunk size (default: 500)
- `--overlap <int>` - Overlap between chunks (default: 50)

### embedding_benchmark.py
Tests multiple embedding models on your data to find the best fit for your domain.

**Usage:**
```bash
python embedding_benchmark.py --data ./chunks/ --domain finance --output results.json
```

**Options:**
- `--embeddings <models>` - Embedding models to test (space-separated)
- `--data <dir>` - Directory with chunked text files (required)
- `--domain <name>` - Domain name for context-specific recommendations
- `--output <file>` - Output file for results (JSON)

**Supported Embeddings:**
- sentence-transformers/all-MiniLM-L6-v2 (384 dims, fast, free)
- sentence-transformers/all-mpnet-base-v2 (768 dims, medium, free)
- openai/text-embedding-ada-002 (1536 dims, fast, paid)
- cohere/embed-english-v3.0 (1024 dims, fast, paid)
- bm25 (sparse, fast, free)

### retrieval_tuner.py
Optimizes retrieval parameters (top-k, similarity threshold) for your specific use case.

**Usage:**
```bash
python retrieval_tuner.py --index ./vector_store/ --queries ./test_queries.json --output tuning_results.json
```

**Options:**
- `--index <dir>` - Vector store index directory
- `--queries <file>` - JSON file with test queries and expected results
- `--output <file>` - Output file for tuning results
- `--top-k-range <min> <max>` - Range of top-k values to test (default: 1 20)
- `--threshold-range <min> <max> <step>` - Similarity threshold range

### vector_store_manager.py
Manages vector store operations: create, update, search, and maintain indexes.

**Usage:**
```bash
# Create index from chunks
python vector_store_manager.py --create --chunks ./chunks/ --index ./vector_store/ --embedding sentence-transformers/all-MiniLM-L6-v2

# Search index
python vector_store_manager.py --search --index ./vector_store/ --query "your search query" --top-k 5
```

**Options:**
- `--create` - Create new index from chunks
- `--chunks <dir>` - Directory with chunked text files
- `--index <dir>` - Vector store directory
- `--embedding <model>` - Embedding model to use
- `--search` - Search existing index
- `--query <text>` - Search query
- `--top-k <int>` - Number of results to return (default: 5)
- `--update` - Update index with new documents
- `--stats` - Show index statistics

## Pricing Strategy

**Free tier** (this skill): Core chunking + embedding benchmark tools  
**Paid guide** ($49): Complete production RAG setup with:
- Multi-modal document processing
- Hybrid search (dense + sparse)
- Re-ranking pipeline
- Evaluation framework
- Deployment scripts

## Workflow

1. **Assess your data**
   ```bash
   python chunking_analyzer.py --assess ./your_data/
   ```

2. **Apply chunking strategy**
   ```bash
   python chunking_analyzer.py --strategy recursive --input ./data/ --output ./chunks/
   ```

3. **Benchmark embeddings**
   ```bash
   python embedding_benchmark.py --data ./chunks/ --domain your_domain
   ```

4. **Create vector store**
   ```bash
   python vector_store_manager.py --create --chunks ./chunks/ --index ./vector_store/ --embedding <recommended_model>
   ```

5. **Tune retrieval** (optional)
   ```bash
   python retrieval_tuner.py --index ./vector_store/ --queries ./test_queries.json
   ```

## Requirements

- Python 3.8+
- Dependencies: numpy, sentence-transformers (optional for real embeddings)

## Files

- `chunking_analyzer.py` - Document analysis and chunking
- `embedding_benchmark.py` - Embedding model benchmarking
- `retrieval_tuner.py` - Retrieval parameter optimization
- `vector_store_manager.py` - Vector store operations
- `skill.json` - Skill metadata