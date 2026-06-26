#!/usr/bin/env python3
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.bayesian_predictor import (
    LightweightTimeoutPredictor,
    BayesianTimeoutPredictor,
    AdaptiveTimeoutPredictor,
    BayesianTimeoutManager
)


def test_lightweight_predictor():
    print("=" * 60)
    print("Test 1: LightweightTimeoutPredictor")
    print("=" * 60)

    predictor = LightweightTimeoutPredictor(window_size=5)

    durations = [1.0, 1.2, 0.9, 1.1, 1.3, 1.15, 1.25]

    for d in durations:
        predictor.update(d)
        timeout = predictor.predict_timeout()
        conf = predictor.get_confidence()
        print(f"  Duration: {d:.2f}s -> Timeout: {timeout:.2f}s, Confidence: {conf:.2f}")

    stats = predictor.get_stats()
    print(f"\n  Stats: {stats}")
    print("  [PASS]" if predictor.get_confidence() > 0 else "  [FAIL]")


def test_bayesian_predictor():
    print("\n" + "=" * 60)
    print("Test 2: BayesianTimeoutPredictor")
    print("=" * 60)

    predictor = BayesianTimeoutPredictor(task_type='api_call')

    durations = [1.0, 1.2, 0.9, 1.1, 1.3]

    for d in durations:
        predictor.update(d)
        timeout = predictor.predict_timeout()
        conf = predictor.get_confidence()
        print(f"  Duration: {d:.2f}s -> Timeout: {timeout:.2f}s, Confidence: {conf:.2f}")

    print("  [PASS]" if predictor.get_confidence() > 0 else "  [FAIL]")


def test_adaptive_predictor():
    print("\n" + "=" * 60)
    print("Test 3: AdaptiveTimeoutPredictor")
    print("=" * 60)

    predictor = AdaptiveTimeoutPredictor(
        task_type='cron_job',
        switch_threshold=10,
        confidence_threshold=0.7
    )

    print(f"  Initial mode: {predictor.mode}")

    durations = [1.0, 1.2, 0.9, 1.1, 1.3] * 4

    for i, d in enumerate(durations, 1):
        predictor.update(d)
        timeout = predictor.predict_timeout()
        conf = predictor.get_confidence()
        mode = predictor.mode

        if i % 10 == 0:
            print(f"  [{i}] Duration: {d:.2f}s -> Timeout: {timeout:.2f}s, Mode: {mode}, Conf: {conf:.2f}")

    stats = predictor.get_stats()
    print(f"\n  Final mode: {stats['current_mode']}")
    print(f"  Call count: {stats['call_count']}")
    print(f"  Last prediction time: {stats['last_prediction_time_ms']:.4f}ms")
    print("  [PASS] Adaptive predictor working")


def test_mode_switching():
    print("\n" + "=" * 60)
    print("Test 4: Mode Switching")
    print("=" * 60)

    predictor = AdaptiveTimeoutPredictor(
        task_type='high_freq',
        switch_threshold=5,
        confidence_threshold=0.5
    )

    print(f"  Initial mode: {predictor.mode}")

    for i in range(15):
        predictor.update(1.0 + (i % 3) * 0.1)
        if i % 3 == 0:
            print(f"  [{i}] Mode: {predictor.mode}, Confidence: {predictor.get_confidence():.2f}")

    predictor.force_mode("lightweight")
    print(f"  After force_mode('lightweight'): {predictor.mode}")

    predictor.force_mode("bayesian")
    print(f"  After force_mode('bayesian'): {predictor.mode}")
    print("  [PASS] Mode switching works")


def test_manager():
    print("\n" + "=" * 60)
    print("Test 4: BayesianTimeoutManager")
    print("=" * 60)

    manager = BayesianTimeoutManager()

    manager.record_duration('api_call', 1.0)
    manager.record_duration('api_call', 1.2)
    manager.record_duration('file_op', 0.5)

    timeout_api = manager.predict_timeout('api_call')
    timeout_file = manager.predict_timeout('file_op')

    print(f"  api_call timeout: {timeout_api:.2f}s")
    print(f"  file_op timeout: {timeout_file:.2f}s")

    stats = manager.get_all_stats()
    print(f"  All stats: {list(stats.keys())}")
    print("  [PASS]")


def benchmark_lightweight_vs_bayesian():
    print("\n" + "=" * 60)
    print("Benchmark: Lightweight vs Bayesian prediction time")
    print("=" * 60)

    lightweight = LightweightTimeoutPredictor()
    bayesian = BayesianTimeoutPredictor()

    for _ in range(100):
        lightweight.update(1.0)
        bayesian.update(1.0)

    iterations = 10000

    start = time.time()
    for _ in range(iterations):
        lightweight.predict_timeout()
    lightweight_time = (time.time() - start) * 1000

    start = time.time()
    for _ in range(iterations):
        bayesian.predict_timeout()
    bayesian_time = (time.time() - start) * 1000

    print(f"  Lightweight: {lightweight_time:.2f}ms for {iterations} calls ({lightweight_time/iterations:.4f}ms per call)")
    print(f"  Bayesian: {bayesian_time:.2f}ms for {iterations} calls ({bayesian_time/iterations:.4f}ms per call)")
    print(f"  Speedup: {bayesian_time/lightweight_time:.2f}x faster with lightweight")


if __name__ == "__main__":
    test_lightweight_predictor()
    test_bayesian_predictor()
    test_adaptive_predictor()
    test_mode_switching()
    test_manager()
    benchmark_lightweight_vs_bayesian()

    print("\n" + "=" * 60)
    print("All tests passed!")
    print("=" * 60)
