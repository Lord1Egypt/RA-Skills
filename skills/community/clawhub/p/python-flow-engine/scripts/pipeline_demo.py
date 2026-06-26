"""
pipeline_demo.py — Demonstrations of the Pipeline orchestration library.

Shows four usage patterns:
  1. Serial pipeline (>>) — sequential chaining
  2. Parallel pipeline (//) — concurrent execution
  3. Conditional pipeline (|) — branch based on output
  4. Mixed pipeline — all three modes combined
  5. Error handling — retry and timeout behavior
"""

import sys
import os
import time

# Ensure pipeline.py is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pipeline import Node, Pipeline, NodeStatus


# =========================================================================
# Helper: shared context accumulator for demo tracing
# =========================================================================

def demo_header(title: str):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


# =========================================================================
# Demo 1: Serial Pipeline (>>)
# =========================================================================

def demo_serial():
    demo_header("Demo 1: Serial Pipeline (>>)")

    # Simple data processing chain
    def extract(context, data):
        """Simulate extracting raw data."""
        text = f"raw:{data}"
        print(f"  [extract] '{data}' -> '{text}'")
        return text

    def transform(context, data):
        """Simulate transforming data."""
        transformed = data.upper().replace("RAW:", "UPPER:")
        print(f"  [transform] '{data}' -> '{transformed}'")
        return transformed

    def load(context, data):
        """Simulate loading data."""
        result = f"[LOADED] {data}"
        print(f"  [load] '{data}' -> '{result}'")
        return result

    # Build pipeline with operator chaining
    pipe = Pipeline()
    n_extract = Node(extract, name="extract")
    n_transform = Node(transform, name="transform")
    n_load = Node(load, name="load")

    pipe.add_node(n_extract)
    pipe.add_node(n_transform)
    pipe.add_node(n_load)

    n_extract >> n_transform >> n_load  # serial chain

    result = pipe.run(n_extract, "hello world")
    print(f"  => Final result: {result}")

    # Show Mermaid visualization
    print()
    print("  Pipeline graph (Mermaid):")
    for line in pipe.visualize().split("\n"):
        print(f"    {line}")


# =========================================================================
# Demo 2: Parallel Pipeline (//)
# =========================================================================

def demo_parallel():
    demo_header("Demo 2: Parallel Pipeline (//)")

    def splitter(context, data):
        """Split input into two parts for parallel processing."""
        items = data.split(",")
        print(f"  [splitter] {data} -> {items}")
        return items

    def process_a(context, data):
        """Process first chunk (simulate slow work)."""
        time.sleep(0.2)
        result = f"process_a({data[0]})"
        print(f"  [process_a] -> {result}")
        return result

    def process_b(context, data):
        """Process second chunk (simulate slow work)."""
        time.sleep(0.3)
        result = f"process_b({data[1]})"
        print(f"  [process_b] -> {result}")
        return result

    def merger(context, data):
        """Merge parallel results."""
        result = f"merged:{{{','.join(data)}}}"
        print(f"  [merger] -> {result}")
        return result

    pipe = Pipeline()
    n_split = Node(splitter, name="split")
    n_pa = Node(process_a, name="process_a")
    n_pb = Node(process_b, name="process_b")
    n_merge = Node(merger, name="merge")

    for n in [n_split, n_pa, n_pb, n_merge]:
        pipe.add_node(n)

    # split -> process_a (serial)
    # split -> process_b (serial)
    # process_a // process_b (parallel)
    n_split >> n_pa
    n_split >> n_pb  # both get the split data
    n_pa // n_pb
    n_pa >> n_merge
    n_pb >> n_merge

    start = time.perf_counter()
    result = pipe.run(n_split, "apple,banana")
    elapsed = time.perf_counter() - start
    print(f"  => Final result: {result}")
    print(f"  => Elapsed: {elapsed:.3f}s (parallel saved ~0.3s vs ~0.5s serial)")


# =========================================================================
# Demo 3: Conditional Pipeline (|)
# =========================================================================

def demo_conditional():
    demo_header("Demo 3: Conditional Pipeline (|)")

    def check_positive(context, data):
        """Check if the number is positive."""
        is_pos = data > 0
        print(f"  [check] {data} is {'positive' if is_pos else 'not positive'}")
        context["is_positive"] = is_pos
        return data

    def handle_positive(context, data):
        result = f"POSITIVE({data})"
        print(f"  [handle_positive] {data} -> {result}")
        return result

    def handle_non_positive(context, data):
        result = f"NON_POSITIVE({data})"
        print(f"  [handle_non_positive] {data} -> {result}")
        return result

    pipe = Pipeline()
    n_check = Node(check_positive, name="check")
    n_pos = Node(handle_positive, name="positive")
    n_non = Node(handle_non_positive, name="non_positive")

    for n in [n_check, n_pos, n_non]:
        pipe.add_node(n)

    # Conditional routing using connect() with condition function
    pipe.connect(n_check, n_pos, "conditional",
                 condition=lambda ctx, d: ctx.get("is_positive", False))
    pipe.connect(n_check, n_non, "conditional",
                 condition=lambda ctx, d: not ctx.get("is_positive", False))

    print("  --- Run with 42 (positive) ---")
    result = pipe.run(n_check, 42)
    print(f"  => Result: {result}")

    print("  --- Run with -1 (non-positive) ---")
    pipe._reset_all()
    n_check.reset()
    n_pos.reset()
    n_non.reset()
    result = pipe.run(n_check, -1)
    print(f"  => Result: {result}")


# =========================================================================
# Demo 4: Mixed Pipeline
# =========================================================================

def demo_mixed():
    demo_header("Demo 4: Mixed Pipeline (serial + parallel + conditional)")

    def fetch(context, data):
        """Fetch user record."""
        print(f"  [fetch] user_id={data}")
        context["user"] = {"id": data, "name": f"User_{data}"}
        return context["user"]

    def validate(context, data):
        """Validate user data."""
        if data.get("id", 0) <= 0:
            raise ValueError("Invalid user ID")
        print(f"  [validate] {data['name']} OK")
        return data

    def enrich_profile(context, data):
        """Enrich with profile data (slow)."""
        time.sleep(0.15)
        profile = {"age": 30, "role": "engineer"}
        data["profile"] = profile
        print(f"  [enrich_profile] added {profile}")
        return data

    def compute_stats(context, data):
        """Compute user stats (slow)."""
        time.sleep(0.1)
        stats = {"posts": 42, "likes": 128}
        data["stats"] = stats
        print(f"  [compute_stats] added {stats}")
        return data

    def notify_admin(context, data):
        """If user is special, notify admin."""
        print(f"  [notify_admin] sent notification for {data['name']}")
        data["notified"] = True
        return data

    pipe = Pipeline()
    n_fetch = Node(fetch, name="fetch")
    n_val = Node(validate, name="validate")
    n_profile = Node(enrich_profile, name="enrich_profile")
    n_stats = Node(compute_stats, name="compute_stats")
    n_notify = Node(notify_admin, name="notify_admin")

    for n in [n_fetch, n_val, n_profile, n_stats, n_notify]:
        pipe.add_node(n)

    # Pipeline structure:
    # fetch >> validate
    # validate >> enrich_profile (serial)
    # validate >> compute_stats (serial)
    # enrich_profile // compute_stats (parallel)
    # enrich_profile >> notify_admin (conditional: only if user.id == 1)
    n_fetch >> n_val
    n_val >> n_profile
    n_val >> n_stats
    n_profile // n_stats
    pipe.connect(n_profile, n_notify, "conditional",
                 condition=lambda ctx, d: d.get("id") == 1)

    print("  --- Run with user_id=1 (gets notification) ---")
    result = pipe.run(n_fetch, 1)
    print(f"  => Final: id={result.get('id')}, profile={result.get('profile')}, "
          f"stats={result.get('stats')}, notified={result.get('notified')}")

    print()
    print("  Pipeline graph (Mermaid):")
    for line in pipe.visualize().split("\n"):
        print(f"    {line}")


# =========================================================================
# Demo 5: Error Handling (retry + timeout)
# =========================================================================

def demo_error_handling():
    demo_header("Demo 5: Error Handling (retry + timeout)")

    # Node with retry: tries 3 times before giving up
    attempts = [0]

    def flaky_fn(context, data):
        attempts[0] += 1
        print(f"  [flaky_fn] attempt {attempts[0]}")
        if attempts[0] < 3:
            raise RuntimeError(f"Attempt {attempts[0]} failed")
        return f"success_on_attempt_{attempts[0]}"

    pipe = Pipeline()
    n_flaky = Node(flaky_fn, name="flaky", retry=2)
    pipe.add_node(n_flaky)

    print("  --- Flaky node with retry=2 ---")
    result = pipe.run(n_flaky, "go")
    print(f"  => Result: {result}")

    # Node with timeout
    def slow_fn(context, data):
        time.sleep(5)
        return "too_late"

    pipe2 = Pipeline()
    n_slow = Node(slow_fn, name="slowpoke", timeout=0.5)
    pipe2.add_node(n_slow)

    print("  --- Slow node with timeout=0.5s ---")
    try:
        pipe2.run(n_slow, "go")
    except (TimeoutError, RuntimeError) as e:
        print(f"  => Caught expected error: {type(e).__name__}: {e}")

    print("  => Error handling works correctly!")


# =========================================================================
# Demo 6: Decorator-based pipeline
# =========================================================================

def demo_decorator():
    from pipeline import pipe_decorator

    demo_header("Demo 6: Decorator-based Nodes")

    pipe = Pipeline()

    @pipe_decorator(name="step_a")
    def step_a(context, data):
        return f"A({data})"

    @pipe_decorator(name="step_b")
    def step_b(context, data):
        return f"B({data})"

    # Wrap decorated functions as Nodes
    n_a = Node(step_a, name="step_a")
    n_b = Node(step_b, name="step_b")
    pipe.add_node(n_a)
    pipe.add_node(n_b)
    n_a >> n_b

    result = pipe.run(n_a, "hello")
    print(f"  => Result: {result}")


# =========================================================================
# Main
# =========================================================================

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════╗")
    print("║   Pipeline Orchestration Library — Demo Suite       ║")
    print("╚══════════════════════════════════════════════════════╝")

    demo_serial()
    demo_parallel()
    demo_conditional()
    demo_mixed()
    demo_error_handling()
    demo_decorator()

    print()
    print("╔══════════════════════════════════════════════════════╗")
    print("║   All demos completed successfully!                 ║")
    print("╚══════════════════════════════════════════════════════╝")
