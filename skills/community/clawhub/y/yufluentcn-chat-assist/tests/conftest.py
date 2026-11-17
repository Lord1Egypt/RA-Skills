import pytest
from tokenapi_harness.paths import discover_harness_root


@pytest.fixture
def harness_root():
    return discover_harness_root()
