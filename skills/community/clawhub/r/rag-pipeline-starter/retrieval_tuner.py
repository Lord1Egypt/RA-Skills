#!/usr/bin/env python3
"""
RAG Pipeline Starter: Retrieval Tuner
Optimizes retrieval parameters (top-k, similarity threshold) for maximum accuracy.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from collections import defaultdict


def load_queries(queries_path: str) -> List[Dict[str, Any]]:
    """Load test queries from JSON file."""
    with open(queries_path, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, list):
        return data
    elif isinstance(data, dict) and 'queries' in data:
        return data['queries']
    else:
        raise ValueError("Queries must be a list or dict with 'queries' key")


def load_search_results(results_dir: str) -> Dict[str, List[str]]:
    """Load pre-computed search results for each query."""
    results = {}
    path = Path(results_dir)
    
    if not path.is_dir():
        return results
    
    for f in path.glob("*.json"):
        query_name = f.stem
        data = json.loads(f.read_text())
        
        if isinstance(data, list):
            results[query_name] = [item.get('doc_id', item.get('id', str(i))) for i, item in enumerate(data)]
        elif isinstance(data, dict) and 'results' in data:
            results[query_name] = [item.get('doc_id', item.get('id', str(i))) for i, item in enumerate(data['results'])]
    
    return results


def compute_recall(retrieved: List[str], relevant: List[str]) -> float:
    """Compute recall: what fraction of relevant docs were retrieved."""
    if not relevant:
        return 1.0
    retrieved_set = set(retrieved)
    relevant_set = set(relevant)
    return len(retrieved_set & relevant_set) / len(relevant_set)


def compute_precision(retrieved: List[str], relevant: List[str]) -> float:
    """Compute precision: what fraction of retrieved docs are relevant."""
    if not retrieved:
        return 0.0
    retrieved_set = set(retrieved)
    relevant_set = set(relevant)
    return len(retrieved_set & relevant_set) / len(retrieved_set)


def compute_mrr(retrieved_list: List[List[str]], relevant_list: List[List[str]]) -> float:
    """Compute Mean Reciprocal Rank."""
    reciprocals = []
    
    for retrieved, relevant in zip(retrieved_list, relevant_list):
        retrieved_set = set(retrieved)
        relevant_set = set(relevant)
        
        for i, doc_id in enumerate(retrieved, 1):
            if doc_id in relevant_set:
                reciprocals.append(1.0 / i)
                break
        else:
            reciprocals.append(0.0)
    
    return sum(reciprocals) / len(reciprocals) if reciprocals else 0.0


def simulate_search_results(query: str, index_data: List[Dict], top_k: int, threshold: float) -> List[str]:
    """
    Simulate search results based on query match score.
    In production, this would query the actual vector store.
    """
    # Mock implementation - in real use, query your vector DB
    results = []
    for item in index_data:
        score = item.get('score', 0.5)
        if score >= threshold:
            results.append((item.get('doc_id', ''), score))
    
    # Sort by score descending
    results.sort(key=lambda x: x[1], reverse=True)
    return [doc_id for doc_id, _ in results[:top_k]]


def tune_top_k(index_data: List[Dict], queries: List[Dict], k_range: tuple) -> Dict[str, Any]:
    """Find optimal top-k value."""
    results = []
    
    for k in range(k_range[0], k_range[1] + 1):
        recalls = []
        precisions = []
        
        for q in queries:
            query = q.get('query', '')
            relevant = q.get('relevant_docs', q.get('relevant', []))
            
            retrieved = simulate_search_results(query, index_data, k, 0.0)
            
            if relevant:
                recalls.append(compute_recall(retrieved, relevant))
                precisions.append(compute_precision(retrieved, relevant))
        
        avg_recall = sum(recalls) / len(recalls) if recalls else 0
        avg_precision = sum(precisions) / len(precisions) if precisions else 0
        f1 = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0
        
        results.append({
            'top_k': k,
            'recall': avg_recall,
            'precision': avg_precision,
            'f1': f1
        })
    
    # Find best F1
    best = max(results, key=lambda x: x['f1'])
    
    return {
        'parameter': 'top_k',
        'tested_range': list(range(k_range[0], k_range[1] + 1)),
        'results': results,
        'optimal_value': best['top_k'],
        'optimal_metrics': {
            'recall': best['recall'],
            'precision': best['precision'],
            'f1': best['f1']
        }
    }


def tune_threshold(index_data: List[Dict], queries: List[Dict], threshold_range: tuple) -> Dict[str, Any]:
    """Find optimal similarity threshold."""
    step = threshold_range[2] if len(threshold_range) > 2 else 0.05
    thresholds = []
    
    t = threshold_range[0]
    while t <= threshold_range[1]:
        thresholds.append(round(t, 2))
        t += step
    
    results = []
    
    for threshold in thresholds:
        recalls = []
        precisions = []
        
        for q in queries:
            query = q.get('query', '')
            relevant = q.get('relevant_docs', q.get('relevant', []))
            
            retrieved = simulate_search_results(query, index_data, 10, threshold)
            
            if relevant and retrieved:
                recalls.append(compute_recall(retrieved, relevant))
                precisions.append(compute_precision(retrieved, relevant))
            elif not relevant and not retrieved:
                recalls.append(1.0)
                precisions.append(1.0)
        
        avg_recall = sum(recalls) / len(recalls) if recalls else 0
        avg_precision = sum(precisions) / len(precisions) if precisions else 0
        f1 = 2 * (avg_precision * avg_recall) / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0
        
        results.append({
            'threshold': threshold,
            'recall': avg_recall,
            'precision': avg_precision,
            'f1': f1
        })
    
    # Find best F1
    best = max(results, key=lambda x: x['f1'])
    
    return {
        'parameter': 'threshold',
        'tested_values': thresholds,
        'results': results,
        'optimal_value': best['threshold'],
        'optimal_metrics': {
            'recall': best['recall'],
            'precision': best['precision'],
            'f1': best['f1']
        }
    }


def main():
    parser = argparse.ArgumentParser(description="RAG Retrieval Tuner")
    parser.add_argument("--index", type=str, required=True, help="Vector store index directory")
    parser.add_argument("--queries", type=str, required=True, help="JSON file with test queries")
    parser.add_argument("--output", type=str, help="Output file for results")
    parser.add_argument("--top-k-range", type=int, nargs=2, default=[1, 20], 
                        help="Range of top-k values to test (min max)")
    parser.add_argument("--threshold-range", type=float, nargs=3, default=[0.0, 1.0, 0.1],
                        help="Similarity threshold range (min max step)")
    parser.add_argument("--tune", type=str, choices=["top-k", "threshold", "both"], default="both",
                        help="What to tune")
    
    args = parser.parse_args()
    
    # Load queries
    print(f"Loading queries from: {args.queries}")
    queries = load_queries(args.queries)
    print(f"Loaded {len(queries)} test queries")
    
    # Load index data (mock for demo)
    # In production, load actual vector store
    index_path = Path(args.index)
    index_data = []
    
    if index_path.is_dir():
        for f in index_path.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                index_data.append({
                    'doc_id': f.stem,
                    'score': data.get('score', 0.5)
                })
            except:
                pass
    
    # If no data, create mock for demo
    if not index_data:
        print("Note: Using mock index data for demonstration")
        index_data = [
            {'doc_id': f'doc_{i:04d}', 'score': 0.9 - (i * 0.01)}
            for i in range(100)
        ]
    
    print(f"Index contains {len(index_data)} documents")
    
    results = {}
    
    # Tune top-k
    if args.tune in ['top-k', 'both']:
        print(f"\nTuning top-k (range: {args.top_k_range[0]}-{args.top_k_range[1]})...")
        results['top_k_tuning'] = tune_top_k(index_data, queries, tuple(args.top_k_range))
        print(f"Optimal top-k: {results['top_k_tuning']['optimal_value']} (F1: {results['top_k_tuning']['optimal_metrics']['f1']:.3f})")
    
    # Tune threshold
    if args.tune in ['threshold', 'both']:
        print(f"\nTuning threshold (range: {args.threshold_range[0]}-{args.threshold_range[1]})...")
        results['threshold_tuning'] = tune_threshold(index_data, queries, tuple(args.threshold_range))
        print(f"Optimal threshold: {results['threshold_tuning']['optimal_value']} (F1: {results['threshold_tuning']['optimal_metrics']['f1']:.3f})")
    
    # Summary
    summary = {
        'queries_tested': len(queries),
        'index_size': len(index_data),
        'tuning_results': results
    }
    
    print("\n=== Tuning Summary ===")
    if 'top_k_tuning' in results:
        tk = results['top_k_tuning']
        print(f"Top-k: {tk['optimal_value']} (recall: {tk['optimal_metrics']['recall']:.3f}, precision: {tk['optimal_metrics']['precision']:.3f})")
    if 'threshold_tuning' in results:
        th = results['threshold_tuning']
        print(f"Threshold: {th['optimal_value']} (recall: {th['optimal_metrics']['recall']:.3f}, precision: {th['optimal_metrics']['precision']:.3f})")
    
    if args.output:
        Path(args.output).write_text(json.dumps(summary, indent=2))
        print(f"\nResults saved to: {args.output}")
    
    return summary


if __name__ == "__main__":
    main()