from sherpamind.rate_limit import RequestPacer


def test_request_pacer_initializes() -> None:
    pacer = RequestPacer(min_interval_seconds=0)
    pacer.wait()
    pacer.wait()
