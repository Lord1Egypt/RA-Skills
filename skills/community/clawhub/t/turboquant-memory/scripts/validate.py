#!/usr/bin/env python3
"""
TurboQuant Distribution Validation Tool

Validates that SRHT rotation produces the expected Gaussian distribution
for TurboQuant algorithm. Reads embeddings from OpenClaw sqlite-vec tables.

Usage:
    python validate.py --db /path/to/memory.db --table vectors
    python validate.py --db /path/to/memory.db --auto-detect
"""

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

# Import from same directory
sys.path.insert(0, str(Path(__file__).parent))
from turboquant import SRHTRotate, TurboQuantProd


def detect_vec0_tables(conn: sqlite3.Connection) -> List[str]:
    """Detect tables using vec0 extension."""
    cursor = conn.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND sql LIKE '%USING vec0%'
    """)
    return [row[0] for row in cursor.fetchall()]


class OpenClawVecReader:
    """Reader for OpenClaw vec0 embedding tables."""
    
    def __init__(self, conn: sqlite3.Connection, table_name: str, embedding_col: str = "embedding"):
        self.conn = conn
        self.table_name = table_name
        self.embedding_col = embedding_col
        
        # Detect dimension from first row
        self.dim = self._detect_dimension()
    
    def _detect_dimension(self) -> Optional[int]:
        """Detect embedding dimension from first non-null row."""
        try:
            cursor = self.conn.execute(
                f"SELECT {self.embedding_col} FROM {self.table_name} "
                f"WHERE {self.embedding_col} IS NOT NULL LIMIT 1"
            )
            row = cursor.fetchone()
            if row and row[0]:
                # vec0 stores as float32 blob
                vec = np.frombuffer(row[0], dtype=np.float32)
                return len(vec)
        except Exception as e:
            print(f"Warning: Could not detect dimension: {e}")
        return None
    
    def read_embeddings(self, limit: Optional[int] = None) -> np.ndarray:
        """Read all embeddings as numpy array."""
        if self.dim is None:
            raise ValueError("Could not detect embedding dimension")
        
        limit_clause = f"LIMIT {limit}" if limit else ""
        cursor = self.conn.execute(
            f"SELECT {self.embedding_col} FROM {self.table_name} "
            f"WHERE {self.embedding_col} IS NOT NULL {limit_clause}"
        )
        
        embeddings = []
        for row in cursor:
            if row[0]:
                vec = np.frombuffer(row[0], dtype=np.float32)
                if len(vec) == self.dim:
                    embeddings.append(vec)
        
        if not embeddings:
            raise ValueError("No valid embeddings found")
        
        return np.array(embeddings)


def jarque_bera_test(x: np.ndarray) -> Tuple[float, float]:
    """
    Jarque-Bera test for normality.
    Returns (statistic, p_value_approx).
    """
    n = len(x)
    if n < 30:
        return np.nan, np.nan
    
    # Compute skewness and kurtosis
    mean_x = np.mean(x)
    std_x = np.std(x)
    
    if std_x < 1e-12:
        return np.nan, np.nan
    
    # Standardize
    z = (x - mean_x) / std_x
    
    # Sample skewness (third moment)
    skewness = np.mean(z**3)
    
    # Sample excess kurtosis (fourth moment - 3)
    kurtosis = np.mean(z**4) - 3
    
    # Jarque-Bera statistic
    jb = n * (skewness**2 / 6 + kurtosis**2 / 24)
    
    # Approximate p-value using chi-square distribution with 2 dof
    # For JB > 6, p ≈ exp(-JB/2) (rough approximation)
    p_value = np.exp(-jb / 2) if jb < 10 else 0.0
    
    return jb, p_value


def analyze_distribution(X_rotated: np.ndarray, target_std: float) -> Dict:
    """Analyze distribution of rotated coordinates."""
    n_samples, dim = X_rotated.shape
    
    # Aggregate statistics across all coordinates
    all_coords = X_rotated.flatten()
    
    # Basic statistics
    stats = {
        'n_samples': n_samples,
        'dimension': dim,
        'target_std': target_std,
        'mean': float(np.mean(all_coords)),
        'std': float(np.std(all_coords)),
        'skewness': float(np.mean((all_coords - np.mean(all_coords))**3) / np.std(all_coords)**3),
        'kurtosis': float(np.mean((all_coords - np.mean(all_coords))**4) / np.std(all_coords)**4 - 3),
    }
    
    # Jarque-Bera test for normality
    jb_stat, jb_pvalue = jarque_bera_test(all_coords)
    stats['jarque_bera_stat'] = float(jb_stat) if not np.isnan(jb_stat) else None
    stats['jarque_bera_pvalue'] = float(jb_pvalue) if not np.isnan(jb_pvalue) else None
    
    # Quantile analysis (compare to theoretical standard normal)
    quantiles = [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]
    theoretical_quantiles = [
        -2.326, -1.645, -0.674, 0.0, 0.674, 1.645, 2.326
    ]
    
    # Scale theoretical quantiles by target std
    theoretical_scaled = [q * target_std for q in theoretical_quantiles]
    empirical = [float(np.percentile(all_coords, q * 100)) for q in quantiles]
    
    quantile_errors = [abs(emp - theo) for emp, theo in zip(empirical, theoretical_scaled)]
    
    stats['quantiles'] = {
        'levels': quantiles,
        'theoretical': theoretical_scaled, 
        'empirical': empirical,
        'errors': quantile_errors,
        'max_error': max(quantile_errors)
    }
    
    # Inter-dimension correlation check
    if dim > 1:
        # Sample 100 pairs of coordinates to check independence
        n_pairs = min(100, dim * (dim - 1) // 2)
        correlations = []
        
        for i in range(min(50, dim)):
            for j in range(i + 1, min(i + 50, dim)):
                corr = np.corrcoef(X_rotated[:, i], X_rotated[:, j])[0, 1]
                if not np.isnan(corr):
                    correlations.append(abs(corr))
        
        if correlations:
            stats['independence'] = {
                'mean_abs_correlation': float(np.mean(correlations)),
                'max_abs_correlation': float(np.max(correlations)),
                'n_pairs_tested': len(correlations)
            }
    
    return stats


def validate_quantization(embeddings: np.ndarray, bits: int = 4, n_test: int = 100) -> Dict:
    """Test quantization MSE and recall quality."""
    if len(embeddings) < n_test:
        n_test = len(embeddings)
    
    # Sample test vectors
    indices = np.random.choice(len(embeddings), n_test, replace=False)
    test_vectors = embeddings[indices]
    
    # Normalize
    test_vectors = test_vectors / np.linalg.norm(test_vectors, axis=1, keepdims=True)
    
    quantizer = TurboQuantProd(test_vectors.shape[1], bits=bits)
    
    # Quantization MSE
    mse_total = 0
    for v in test_vectors:
        data = quantizer.quantize(v)
        
        # Reconstruct MSE part only for MSE calculation
        mse_data = {
            'norm': data['norm'],
            'scale': data['scale'],
            'indices': data['mse_indices']
        }
        v_mse = quantizer.mse_quantizer.dequantize(mse_data)
        mse = np.mean((v - v_mse)**2)
        mse_total += mse
    
    avg_mse = mse_total / n_test
    
    # Recall test (small scale)
    if len(embeddings) >= 50:
        n_db = min(50, len(embeddings))
        n_queries = min(10, n_db)
        
        db_indices = np.random.choice(len(embeddings), n_db, replace=False)
        query_indices = np.random.choice(db_indices, n_queries, replace=False)
        
        db_vectors = embeddings[db_indices]
        db_vectors = db_vectors / np.linalg.norm(db_vectors, axis=1, keepdims=True)
        
        # Quantize database  
        db_quantized = [quantizer.quantize(v) for v in db_vectors]
        
        recall_1 = 0
        for qi in query_indices:
            query_idx = np.where(db_indices == qi)[0][0]
            query = db_vectors[query_idx]
            
            # True ranking
            true_scores = [np.dot(query, v) for i, v in enumerate(db_vectors) if i != query_idx]
            true_top1 = np.argmax(true_scores)
            if true_top1 >= query_idx:
                true_top1 += 1  # Adjust for excluded query
            
            # Quantized ranking  
            results = quantizer.search(query, db_quantized, top_k=n_db-1)
            results = [(i, s) for i, s in results if i != query_idx]
            if results:
                est_top1 = results[0][0]
                if est_top1 == true_top1:
                    recall_1 += 1
        
        recall_1_rate = recall_1 / n_queries if n_queries > 0 else 0
    else:
        recall_1_rate = None
    
    return {
        'avg_mse': avg_mse,
        'recall_1': recall_1_rate,
        'n_test_vectors': n_test
    }


def print_validation_report(stats: Dict, quantization_stats: Optional[Dict] = None):
    """Print formatted validation report."""
    print("=" * 70)
    print("TurboQuant Distribution Validation Report")
    print("=" * 70)
    
    print(f"\n📊 Dataset: {stats['n_samples']} vectors, {stats['dimension']} dimensions")
    print(f"🎯 Target std: {stats['target_std']:.6f} (1/√d)")
    
    print(f"\n📈 Basic Statistics:")
    print(f"   Mean:     {stats['mean']:+.6f} (should be ≈ 0)")
    print(f"   Std:      {stats['std']:.6f} (should be ≈ {stats['target_std']:.6f})")
    print(f"   Skewness: {stats['skewness']:+.6f} (should be ≈ 0)")
    print(f"   Kurtosis: {stats['kurtosis']:+.6f} (should be ≈ 0)")
    
    # Pass/fail indicators
    mean_ok = abs(stats['mean']) < 0.01
    std_ok = abs(stats['std'] - stats['target_std']) < 0.1 * stats['target_std'] 
    skew_ok = abs(stats['skewness']) < 0.2
    kurt_ok = abs(stats['kurtosis']) < 0.5
    
    print(f"   Status:   {'✓' if mean_ok else '✗'} Mean  {'✓' if std_ok else '✗'} Std  {'✓' if skew_ok else '✗'} Skew  {'✓' if kurt_ok else '✗'} Kurt")
    
    # Normality test
    if stats['jarque_bera_stat'] is not None:
        jb_ok = stats['jarque_bera_stat'] < 20 or stats['jarque_bera_pvalue'] > 0.01
        print(f"\n🔬 Jarque-Bera normality test:")
        print(f"   Statistic: {stats['jarque_bera_stat']:.2f}")
        print(f"   P-value:   {stats['jarque_bera_pvalue']:.6f}")
        print(f"   Status:    {'✓ Normal' if jb_ok else '✗ Non-normal'}")
    
    # Quantile analysis
    q_stats = stats['quantiles']
    max_q_error = q_stats['max_error']
    q_ok = max_q_error < 0.1 * stats['target_std']
    
    print(f"\n📏 Quantile Analysis:")
    print(f"   Max error: {max_q_error:.6f} (should be < {0.1 * stats['target_std']:.6f})")
    print(f"   Status:    {'✓ Good fit' if q_ok else '✗ Poor fit'}")
    
    # Independence check
    if 'independence' in stats:
        ind_stats = stats['independence']
        mean_corr = ind_stats['mean_abs_correlation']
        max_corr = ind_stats['max_abs_correlation']
        ind_ok = mean_corr < 0.1 and max_corr < 0.3
        
        print(f"\n🔀 Independence Check:")
        print(f"   Mean |corr|: {mean_corr:.4f} (should be < 0.1)")
        print(f"   Max |corr|:  {max_corr:.4f} (should be < 0.3)")
        print(f"   Pairs tested: {ind_stats['n_pairs_tested']}")
        print(f"   Status:      {'✓ Independent' if ind_ok else '✗ Correlated'}")
    
    # Quantization quality
    if quantization_stats:
        q_stats = quantization_stats
        mse_ok = q_stats['avg_mse'] < 0.01
        recall_ok = q_stats['recall_1'] is None or q_stats['recall_1'] > 0.7
        
        print(f"\n🎯 Quantization Quality:")
        print(f"   Avg MSE:    {q_stats['avg_mse']:.6f} (should be < 0.01)")
        if q_stats['recall_1'] is not None:
            print(f"   Recall@1:   {q_stats['recall_1']:.2%} (should be > 70%)")
        print(f"   Test size:  {q_stats['n_test_vectors']} vectors")
        print(f"   Status:     {'✓' if mse_ok else '✗'} MSE  {'✓' if recall_ok else '✗'} Recall")
    
    # Overall assessment
    all_checks = [mean_ok, std_ok, skew_ok, kurt_ok, q_ok]
    if 'independence' in stats:
        all_checks.append(ind_ok)
    if quantization_stats:
        all_checks.extend([mse_ok, recall_ok])
    
    overall_ok = sum(all_checks) >= len(all_checks) * 0.8
    
    print(f"\n🏆 Overall Assessment: {'✅ PASS' if overall_ok else '❌ FAIL'}")
    print(f"   Passed: {sum(all_checks)}/{len(all_checks)} checks")
    
    if not overall_ok:
        print("\n⚠️  Recommendations:")
        if not mean_ok:
            print("   - Mean is too far from zero; check rotation implementation")
        if not std_ok:
            print("   - Standard deviation mismatch; verify scaling")
        if not skew_ok or not kurt_ok:
            print("   - Distribution is not Gaussian; check FWHT implementation")
        if 'independence' in stats and not ind_ok:
            print("   - Coordinates are correlated; check random sampling")
        if quantization_stats and not mse_ok:
            print("   - High quantization error; consider more bits or better codebooks")
    
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="TurboQuant Distribution Validation")
    parser.add_argument("--db", required=True, help="Path to SQLite database")
    parser.add_argument("--table", help="Table name (if not auto-detecting)")
    parser.add_argument("--auto-detect", action="store_true", help="Auto-detect vec0 tables")
    parser.add_argument("--embedding-col", default="embedding", help="Embedding column name")
    parser.add_argument("--limit", type=int, help="Limit number of embeddings to analyze")
    parser.add_argument("--bits", type=int, default=4, help="Bits for quantization test")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--vec-ext", help="Path to sqlite-vec extension (.dylib/.so)")
    
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"❌ Database not found: {args.db}")
        sys.exit(1)
    
    np.random.seed(args.seed)
    
    # Auto-detect sqlite-vec extension path
    vec_ext_paths = [
        args.vec_ext,
        os.environ.get("SQLITE_VEC_PATH"),
        os.path.expanduser("~/.npm-global/lib/node_modules/openclaw/node_modules/sqlite-vec-darwin-arm64/vec0.dylib"),
        os.path.expanduser("~/.npm-global/lib/node_modules/openclaw/node_modules/sqlite-vec-linux-x64/vec0.so"),
    ]
    
    try:
        conn = sqlite3.connect(args.db)
        
        # Try to load sqlite-vec extension for vec0 table support
        for ext_path in vec_ext_paths:
            if ext_path and os.path.exists(ext_path):
                try:
                    conn.enable_load_extension(True)
                    conn.load_extension(ext_path.replace('.dylib', '').replace('.so', ''))
                    print(f"📦 Loaded sqlite-vec from {ext_path}")
                    break
                except Exception as e:
                    print(f"⚠️  Could not load sqlite-vec from {ext_path}: {e}")
        
        # Detect tables
        if args.auto_detect:
            tables = detect_vec0_tables(conn)
            if not tables:
                print("❌ No vec0 tables found")
                return
            table_name = tables[0]
            print(f"📋 Auto-detected table: {table_name}")
        else:
            table_name = args.table
            if not table_name:
                print("❌ Must specify --table or use --auto-detect")
                return
        
        # Read embeddings
        print(f"📥 Reading embeddings from {table_name}...")
        reader = OpenClawVecReader(conn, table_name, args.embedding_col)
        
        if reader.dim is None:
            print("❌ Could not detect embedding dimension")
            return
        
        embeddings = reader.read_embeddings(args.limit)
        print(f"✅ Loaded {len(embeddings)} embeddings, dim={reader.dim}")
        
        # Normalize embeddings
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Apply SRHT rotation
        print("🔄 Applying SRHT rotation...")
        rotation = SRHTRotate(reader.dim, reader.dim, args.seed)
        embeddings_rotated = rotation.apply_batch(embeddings)
        
        # Analyze distribution
        target_std = 1.0 / np.sqrt(reader.dim)
        print("📊 Analyzing distribution...")
        stats = analyze_distribution(embeddings_rotated, target_std)
        
        # Test quantization
        print("🎯 Testing quantization...")
        quantization_stats = validate_quantization(embeddings, args.bits)
        
        # Generate report
        print_validation_report(stats, quantization_stats)
        
        # Save to JSON if requested
        if args.output:
            output_data = {
                'dataset': {
                    'database': args.db,
                    'table': table_name,
                    'n_embeddings': len(embeddings),
                    'dimension': reader.dim,
                    'limit': args.limit
                },
                'parameters': {
                    'seed': args.seed,
                    'bits': args.bits
                },
                'distribution_analysis': stats,
                'quantization_analysis': quantization_stats
            }
            
            with open(args.output, 'w') as f:
                json.dump(output_data, f, indent=2)
            print(f"\n💾 Results saved to {args.output}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()


if __name__ == "__main__":
    main()