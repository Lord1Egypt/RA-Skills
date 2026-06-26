"""Tests for environment facts extraction."""

from repro_pack.extractor.env_facts import extract_env_facts


class TestVersionExtraction:
    def test_extract_version(self):
        facts = extract_env_facts("Running version 2.4.1 on staging")
        assert facts.app_version == "2.4.1"

    def test_extract_version_v_prefix(self):
        facts = extract_env_facts("app v3.0.0-beta.1 deployed")
        assert facts.app_version == "3.0.0-beta.1"

    def test_extract_build_number(self):
        facts = extract_env_facts("build 8837 is live")
        assert facts.build_number == "8837"


class TestEnvironment:
    def test_detect_production(self):
        facts = extract_env_facts("deployed to production cluster")
        assert facts.environment == "production"

    def test_detect_staging(self):
        facts = extract_env_facts("testing on staging environment")
        assert facts.environment == "staging"

    def test_detect_dev(self):
        facts = extract_env_facts("running in development mode")
        assert facts.environment == "development"


class TestRegion:
    def test_detect_aws_region(self):
        facts = extract_env_facts("server in us-east-1")
        assert facts.region == "us-east-1"

    def test_detect_eu_region(self):
        facts = extract_env_facts("deployed to eu-west-1")
        assert facts.region == "eu-west-1"


class TestFeatureFlags:
    def test_extract_feature_flag(self):
        facts = extract_env_facts("feature_flag: new_export_engine = true")
        assert "new_export_engine" in facts.feature_flags

    def test_no_false_positive_flags(self):
        facts = extract_env_facts("version=2.0 debug=false")
        assert "version" not in facts.feature_flags


class TestRole:
    def test_extract_role(self):
        facts = extract_env_facts("user role: workspace-admin")
        assert facts.user_role == "workspace-admin"


class TestErrorCodes:
    def test_extract_http_error(self):
        facts = extract_env_facts("server returned HTTP 500")
        assert "500" in facts.error_codes

    def test_extract_app_error(self):
        facts = extract_env_facts("error_code: ERR_TIMEOUT_5001")
        assert any("ERR" in c for c in facts.error_codes)


class TestURLs:
    def test_extract_urls(self):
        facts = extract_env_facts("visit https://app.example.com/dashboard")
        assert any("example.com" in u for u in facts.urls)


class TestToDict:
    def test_to_dict_excludes_empty(self):
        facts = extract_env_facts("version 1.0")
        d = facts.to_dict()
        assert "app_version" in d
        assert "region" not in d  # None values excluded
