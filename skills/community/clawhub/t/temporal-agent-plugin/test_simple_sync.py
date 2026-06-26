#!/usr/bin/env python3
import time
import sys
import os

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.distributed_clock_sync import DistributedClockSync


def test_simple_sync():
    print("Testing simple sync...")
    sync = DistributedClockSync(agent_id="test_agent")
    sync.register_agent("agent1")
    
    print("Syncing...")
    start = time.time()
    results = sync.sync_clocks()
    end = time.time()
    print(f"Sync completed in {end - start:.3f}s")
    print(f"Results: {results}")

if __name__ == "__main__":
    test_simple_sync()
