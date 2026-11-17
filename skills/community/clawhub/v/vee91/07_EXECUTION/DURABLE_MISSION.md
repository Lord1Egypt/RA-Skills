# Durable Mission Engine

Represent work as resumable state:
mission -> tasks -> dependencies -> attempts -> artifacts -> verification -> checkpoint.

Support retry, pause, resume, cancellation, timeout, compensation, and rollback. Never assume a long-running job will finish in one session.
