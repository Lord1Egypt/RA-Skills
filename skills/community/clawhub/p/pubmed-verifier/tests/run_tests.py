#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CI entry (v7.0.0, test-line horizontal item #1): run the offline matrix
in one command — python3 tests/run_tests.py; --verbose / -v prints every
test line (unittest verbosity=2) plus a one-line milestone summary.

This file ships inside the package (the family packager copies it), so a
downloaded copy can be verified the same way; it is pure unittest discovery
over the offline matrix — no subprocess, no network (the real-network
acceptance suite stays opt-in and repo-only). In a package copy the matrix
is absent by design: the runner says so and points at --self-check, which
carries the in-package promises."""
import os
import sys
import unittest

VERBOSE = "--verbose" in sys.argv or "-v" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
for p in (ROOT, os.path.join(ROOT, "scripts")):
    if p not in sys.path:
        sys.path.insert(0, p)
# recursion guard: the matrix contains the CI-entry test itself; mark child
# runs so that test skips instead of spawning run_tests.py again forever
os.environ.setdefault("PV_RUNTESTS_CHILD", "1")
# cwd-proof: some legacy tests spawn CLIs with repo-relative paths, so the
# CI entry anchors the working directory at the repo root before discovery
os.chdir(ROOT)

loader = unittest.TestLoader()
suite = loader.discover(HERE, pattern="test_offline_matrix.py")
runner = unittest.TextTestRunner(verbosity=2 if VERBOSE else 1)
result = runner.run(suite)

n, bad = result.testsRun, len(result.failures) + len(result.errors)
if n == 0:
    print("milestone: no offline tests found in this copy (the matrix is "
          "repo-only) — run `python3 scripts/verify_pmids.py --self-check` "
          "for the in-package promises.")
    sys.exit(0)
print(f"milestone: {n - bad}/{n} tests passed"
      + ("" if bad == 0 else f", {bad} FAILED"))
sys.exit(0 if bad == 0 else 1)
