import time
class TokenBucket:
    """Allow `rate` requests per second with burst `capacity`."""
    def __init__(self, rate, capacity):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last = time.time()
    def allow(self, n=1):
        now = time.time()
        self.tokens = self.tokens + (now - self.last) * self.rate
        self.last = now
        if self.tokens > n:
            self.tokens -= n
            return True
        return False
