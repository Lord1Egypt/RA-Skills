#!/usr/bin/env python3
"""
RAG Pipeline Starter: Chunking Analyzer
Analyzes data and recommends chunking strategy based on document characteristics.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


def analyze_document(doc_path: str) -> Dict[str, Any]:
    """Analyze a single document for chunking strategy recommendations."""
    path = Path(doc_path)
    
    if not path.exists():
        return {"error": f"File not found: {doc_path}"}
    
    # Get file info
    file_size = path.stat().st_size
    content = path.read_text(encoding='utf-8', errors='ignore')
    
    lines = content.split('\n')
    num_lines = len(lines)
    avg_line_length = sum(len(l) for l in lines) / max(num_lines, 1)
    
    # Detect structure
    has_headers = any(line.strip().startswith(('#', '##', '###', '//', '--')) for line in lines)
    has_code_blocks = '```' in content or '    ' in content
    has_lists = any(line.strip().startswith(('-', '*', '1.', '•')) for line in lines)
    
    return {
        "path": str(path),
        "size_bytes": file_size,
        "lines": num_lines,
        "avg_line_length": avg_line_length,
        "structure": {
            "has_headers": has_headers,
            "has_code_blocks": has_code_blocks,
            "has_lists": has_lists
        }
    }


def recommend_strategy(doc_info: Dict[str, Any]) -> str:
    """Recommend chunking strategy based on document analysis."""
    structure = doc_info.get("structure", {})
    lines = doc_info.get("lines", 0)
    avg_line_length = doc_info.get("avg_line_length", 0)
    
    # Hierarchical for long docs with structure
    if lines > 1000 and structure.get("has_headers"):
        return "hierarchical"
    
    # Recursive for docs with clear structure
    if structure.get("has_headers") or structure.get("has_code_blocks"):
        return "recursive"
    
    # Semantic for moderate-length docs
    if 100 < lines <= 1000:
        return "semantic"
    
    # Fixed for simple, uniform content
    return "fixed"


def chunk_text_fixed(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Fixed-size chunking with overlap."""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    return chunks


def chunk_text_recursive(text: str, separators: List[str] = None) -> List[str]:
    """Recursive chunking that splits on natural boundaries."""
    if separators is None:
        separators = ['\n\n', '\n', '. ', ' ']
    
    chunks = []
    segments = [text]
    
    for sep in separators:
        new_segments = []
        for segment in segments:
            parts = segment.split(sep)
            new_segments.extend([p.strip() for p in parts if p.strip()])
        segments = new_segments
    
    # Combine small chunks
    current = ""
    for seg in segments:
        if len(current) + len(seg) < 500:
            current += ". " + seg if current else seg
        else:
            if current:
                chunks.append(current)
            current = seg
    if current:
        chunks.append(current)
    
    return chunks if chunks else [text]


def main():
    parser = argparse.ArgumentParser(description="RAG Chunking Analyzer")
    parser.add_argument("--assess", type=str, help="Path to data directory to assess")
    parser.add_argument("--strategy", type=str, choices=["fixed", "semantic", "recursive", "hierarchical"],
                        help="Chunking strategy to use")
    parser.add_argument("--input", type=str, help="Input file or directory")
    parser.add_argument("--output", type=str, help="Output directory for chunks")
    parser.add_argument("--chunk-size", type=int, default=500, help="Chunk size for fixed strategy")
    parser.add_argument("--overlap", type=int, default=50, help="Overlap for fixed strategy")
    
    args = parser.parse_args()
    
    if args.assess:
        # Assess mode: analyze data and recommend strategy
        path = Path(args.assess)
        results = []
        
        if path.is_file():
            results.append(analyze_document(str(path)))
        elif path.is_dir():
            for ext in ['*.txt', '*.md', '*.py', '*.json', '*.html', '*.xml']:
                for f in path.rglob(ext):
                    results.append(analyze_document(str(f)))
        
        # Recommend strategy
        if results:
            avg_lines = sum(r.get("lines", 0) for r in results) / len(results)
            recommended = recommend_strategy(results[0])
            
            print(json.dumps({
                "documents_analyzed": len(results),
                "avg_lines": avg_lines,
                "recommended_strategy": recommended,
                "details": results[:5]  # First 5 for brevity
            }, indent=2))
        else:
            print(json.dumps({"error": "No documents found"}))
            sys.exit(1)
    
    elif args.strategy and args.input and args.output:
        # Chunk mode
        os.makedirs(args.output, exist_ok=True)
        path = Path(args.input)
        
        if path.is_file():
            content = path.read_text(encoding='utf-8', errors='ignore')
            
            if args.strategy == "fixed":
                chunks = chunk_text_fixed(content, args.chunk_size, args.overlap)
            elif args.strategy == "recursive":
                chunks = chunk_text_recursive(content)
            else:
                chunks = chunk_text_fixed(content, args.chunk_size, args.overlap)
            
            # Write chunks
            for i, chunk in enumerate(chunks):
                output_path = Path(args.output) / f"chunk_{i:04d}.txt"
                output_path.write_text(chunk)
            
            print(json.dumps({
                "strategy": args.strategy,
                "chunks_created": len(chunks),
                "output_dir": args.output
            }, indent=2))
        else:
            print(json.dumps({"error": "Input must be a file"}))
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
