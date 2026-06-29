"""rtc-work — demand-side client for the RustChain RIP-302 agent job market.

Turns the deployed-but-inert escrow marketplace into a usable labor market:
discover jobs that match your skills + reward floor + reputation, claim them,
and deliver — so RTC has a job market behind it, not just speculation.

Flat routing only (no DAG recursion). Claim/deliver do not move the worker's
money — escrow is the poster's and releases on poster `/accept`.
"""

__version__ = "0.1.1"
