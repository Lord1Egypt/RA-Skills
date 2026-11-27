import sys; sys.path.insert(0,"src")
from limiter import TokenBucket
def test_creates():
    b = TokenBucket(5, 10)
    assert b is not None
def test_allow_runs():
    b = TokenBucket(5, 10)
    b.allow()
