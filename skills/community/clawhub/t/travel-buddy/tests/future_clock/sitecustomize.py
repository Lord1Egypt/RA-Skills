"""Move this interpreter's clock to FAKE_TODAY, for the CI run that looks for date-bound tests.

On 2026-10-09 two test files began failing on an unchanged tree: their fixture trip started on
2026-09-28, replan_trip.py refuses to move a plan into the past, and the calendar had passed the
fixture. CI had been green two weeks earlier, so nothing changed except the date. Any test that
compares a fixed fixture date with the real clock is that bomb with a later fuse. CI runs the suite a
second time with this directory on PYTHONPATH and FAKE_TODAY about three years ahead, so a new one
fails the day it is written instead of the day its date passes.

Python imports `sitecustomize` at start-up from PYTHONPATH, and subprocesses inherit the variable,
so the scripts the tests launch see the same date. date.today(), datetime.now(), datetime.today()
and datetime.utcnow() move by the same offset; time.time() does not, because durations are not dates.
Unset FAKE_TODAY and this file does nothing.
"""
import os, datetime as _dt
_fake = os.environ.get("FAKE_TODAY")
if _fake:
    _d = _dt.date.fromisoformat(_fake)
    _real_dt = _dt.datetime
    _offset = _real_dt.combine(_d, _dt.time()) - _real_dt.combine(_dt.date.today(), _dt.time())
    class FakeDate(_dt.date):
        @classmethod
        def today(cls):
            return cls(_d.year, _d.month, _d.day)
    class FakeDatetime(_real_dt):
        @classmethod
        def now(cls, tz=None):
            r = _real_dt.now(tz) + _offset
            return cls(r.year, r.month, r.day, r.hour, r.minute, r.second, r.microsecond, r.tzinfo)
        @classmethod
        def today(cls):
            return cls.now()
        @classmethod
        def utcnow(cls):
            r = _real_dt.utcnow() + _offset
            return cls(r.year, r.month, r.day, r.hour, r.minute, r.second, r.microsecond)
    _dt.date = FakeDate
    _dt.datetime = FakeDatetime
