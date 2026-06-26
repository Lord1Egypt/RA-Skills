"""Shared test fixtures."""

import os
import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
EXAMPLES_DIR = os.path.join(os.path.dirname(__file__), "..", "examples")


@pytest.fixture
def fixtures_dir():
    return FIXTURES_DIR


@pytest.fixture
def examples_dir():
    return EXAMPLES_DIR


@pytest.fixture
def dirty_log():
    return """2024-03-25T14:02:10.123Z INFO User john@example.com logged in from 192.168.1.100
2024-03-25T14:02:11.456Z ERROR Authentication failed for user admin, api_key=sk-abc123def456ghi789jkl012
2024-03-25T14:02:12.789Z WARN Rate limit exceeded for IP 10.0.0.55, Bearer tok.fake.demotokenfortest
2024-03-25T14:02:13.012Z INFO Phone verification sent to +1-415-555-0198
2024-03-25T14:02:14.345Z INFO Payment processed for card 4111111111111111
2024-03-25T14:02:15.678Z DEBUG AWS credentials: AKIAFAKEKEY00EXAMPLE
2024-03-25T14:02:16.901Z INFO User 张三 (ID: 110105199003071234) logged in, password=SuperSecret123!
2024-03-25T14:02:17.234Z INFO Cookie: session=abc123def456; user_id=12345; auth_token=xyz789
2024-03-25T14:02:18.567Z INFO Connected to db://admin:dbpassword@db.internal:5432/prod
"""


@pytest.fixture
def clean_ticket():
    return """# Bug Report: Dashboard Timeout

## Environment
- Version: v1.2.3
- Browser: Firefox 124
- OS: Windows 11

## Description
The dashboard times out when loading reports for the past 30 days.
Error code: ERR_TIMEOUT_5001

## Steps to Reproduce
1. Login to dashboard
2. Select "Past 30 days"
3. Wait for timeout error
"""


@pytest.fixture
def python_stack_trace():
    return """Traceback (most recent call last):
  File "/app/main.py", line 42, in handle_request
    result = process_data(payload)
  File "/app/services/processor.py", line 87, in process_data
    return transform(data)
  File "/app/utils/transform.py", line 15, in transform
    return data["items"].map(convert)
TypeError: 'NoneType' object is not subscriptable"""


@pytest.fixture
def java_stack_trace():
    return """java.lang.NullPointerException: Cannot invoke method on null object
	at com.app.service.UserService.getUser(UserService.java:45)
	at com.app.controller.UserController.show(UserController.java:23)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)"""


@pytest.fixture
def js_stack_trace():
    return """TypeError: Cannot read properties of undefined (reading 'map')
    at ExportService.transform (/app/src/services/export.ts:142)
    at async handleExport (/app/src/handlers/report.ts:87)
    at async Router.handle (/app/src/router.ts:23)"""


@pytest.fixture
def json_log():
    return """{"timestamp":"2024-03-25T10:00:01Z","level":"INFO","message":"Server started","source":"main"}
{"timestamp":"2024-03-25T10:00:05Z","level":"ERROR","message":"Connection refused to database","source":"db-pool"}
{"timestamp":"2024-03-25T10:00:06Z","level":"WARN","message":"Retrying database connection, attempt 1","source":"db-pool"}
{"timestamp":"2024-03-25T10:00:10Z","level":"INFO","message":"Database connection established","source":"db-pool"}"""


@pytest.fixture
def syslog():
    return """Mar 25 10:00:01 web-server-01 nginx[1234]: INFO GET /api/users 200 45ms
Mar 25 10:00:02 web-server-01 nginx[1234]: ERROR GET /api/export 500 12003ms
Mar 25 10:00:03 web-server-01 nginx[1234]: WARN GET /api/reports timeout after 30000ms"""


@pytest.fixture
def ua_string():
    return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36"
