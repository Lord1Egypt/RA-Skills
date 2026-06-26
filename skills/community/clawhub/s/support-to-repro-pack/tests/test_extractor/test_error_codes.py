"""Tests for error code extraction."""

from repro_pack.extractor.error_codes import extract_error_codes


class TestHTTPCodes:
    def test_extract_500(self):
        codes = extract_error_codes("HTTP 500 Internal Server Error")
        assert any(c.code == "500" for c in codes)

    def test_extract_status_code(self):
        codes = extract_error_codes("status: 404 not found")
        assert any(c.code == "404" for c in codes)

    def test_category_client(self):
        codes = extract_error_codes("returned status: 403")
        c = [x for x in codes if x.code == "403"]
        assert c[0].category == "http_client"

    def test_category_server(self):
        codes = extract_error_codes("HTTP 502 Bad Gateway")
        c = [x for x in codes if x.code == "502"]
        assert c[0].category == "http_server"


class TestAppErrors:
    def test_extract_err_code(self):
        codes = extract_error_codes("error_code: ERR_TIMEOUT_5001")
        assert any("ERR" in c.code for c in codes)

    def test_extract_error_prefix(self):
        codes = extract_error_codes("got ERR001 from service")
        assert any(c.category == "app_error" for c in codes)


class TestGRPCCodes:
    def test_extract_grpc(self):
        codes = extract_error_codes("gRPC call failed: DEADLINE_EXCEEDED")
        assert any(c.code == "DEADLINE_EXCEEDED" for c in codes)
        assert any(c.category == "grpc" for c in codes)


class TestNoErrors:
    def test_no_errors_in_clean_text(self):
        codes = extract_error_codes("Everything is working fine today")
        assert codes == []
