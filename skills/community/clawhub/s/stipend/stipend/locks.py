"""One payment at a time, enforced by the operating system.

Every limit in this wallet was check-then-act. Read the daily total, decide,
then write it back — and nothing stopped a second process reading the same total
in between. Measured on 10 August 2026, against a $100 daily cap and a $25
per-payment cap:

    8 concurrent processes x $20   ->  $160 sent, none refused
    the ledger then recorded       ->  $60 of that $160
    one single-use approval        ->  found and consumed by 6 processes

The ledger number is the worse half. `record_spend` was read-modify-write, so
the lost updates left the total permanently understated, and every later payment
was then measured against a figure that never happened. A cap that fails once is
a bug; a cap that quietly stays wrong afterwards is a different thing.

It needs no sub-agents. Two payments in parallel is enough, which means an agent
doing the obvious thing — working through a queue concurrently — is enough.

The fix is deliberately the boring one: serialise payments with an exclusive
lock held across check, send and record. A wallet is not a payments processor
and has no throughput problem worth trading correctness for. The lock is an OS
file lock rather than anything of our own, so it is released even when a process
is killed outright — the failure mode that makes hand-rolled lock files worse
than none at all.

Advisory, not mandatory: it stops our own code racing itself. Nothing here
defends against a caller that deliberately bypasses it, and nothing can — that
is what the key passphrase and the spending limits are for.
"""

import contextlib
import errno
import os
import time

from .config import CONFIG_DIR, ensure_dirs

LOCK_NAME = "payment.lock"

# How long to wait for the other payment to finish. A relayed send can take the
# full 45-second network timeout, and a caller that has queued behind one should
# wait for it rather than fail — the whole point is that the second payment
# happens after the first is counted, not instead of it.
DEFAULT_TIMEOUT = 90.0
POLL = 0.05


class LockBusy(RuntimeError):
    """Another payment is in progress and did not finish in time."""


def _acquire(fd):
    """True if we now hold the lock. Never blocks."""
    try:
        try:
            import fcntl
        except ImportError:
            import msvcrt
            msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
        else:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except OSError as e:
        # EACCES/EAGAIN on POSIX, EDEADLOCK/EACCES from msvcrt: all mean held.
        if e.errno in (errno.EACCES, errno.EAGAIN, errno.EDEADLK, 36):
            return False
        raise


def _release(fd):
    try:
        try:
            import fcntl
        except ImportError:
            import msvcrt
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(fd, fcntl.LOCK_UN)
    except OSError:
        pass          # closing the descriptor releases it regardless


@contextlib.contextmanager
def payment_lock(timeout=DEFAULT_TIMEOUT):
    """Hold the payment lock, or raise LockBusy.

    Wraps check, send and record as one unit. Anything that can move money goes
    inside it, including the read of the daily total the decision is made from —
    a check performed outside the lock is exactly the bug this exists for.
    """
    ensure_dirs()
    path = CONFIG_DIR / LOCK_NAME
    fd = os.open(str(path), os.O_RDWR | os.O_CREAT, 0o600)
    deadline = time.time() + timeout
    try:
        while True:
            if _acquire(fd):
                break
            if time.time() >= deadline:
                raise LockBusy(
                    "Another payment has held the lock for %ds.\n"
                    "Only one payment runs at a time, so the spending limits "
                    "are measured against a total that is actually current.\n"
                    "If nothing else is running, remove:\n  %s"
                    % (int(timeout), path))
            time.sleep(POLL)
        try:
            yield
        finally:
            _release(fd)
    finally:
        os.close(fd)
