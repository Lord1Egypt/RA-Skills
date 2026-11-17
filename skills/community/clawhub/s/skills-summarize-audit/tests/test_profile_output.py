import importlib.util
import json
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "analyze_project_profile.py"
spec = importlib.util.spec_from_file_location("analyze_project_profile", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_runtime_sqlite_cache_is_not_project_evidence(tmp_path):
    write(tmp_path / ".codegraph" / "codegraph.db", "SQLite format 3")
    write(tmp_path / "MediaCrawler" / "browser_data" / "Cookies", "cache")
    write(tmp_path / ".pytest_cache" / "package.json", '{"dependencies":{"react":"0.0.0"}}')
    write(tmp_path / "src" / "main.py", "print('ok')")

    files, truncated = module.iter_files(tmp_path, 2000, 10)

    assert not truncated
    assert all(".codegraph" not in str(path) for path in files)
    assert all("browser_data" not in str(path) for path in files)
    assert all(".pytest_cache" not in str(path) for path in files)


def test_nested_package_versions_and_dependency_scope(tmp_path):
    write(tmp_path / "apps" / "web" / "package.json", json.dumps({"dependencies": {"react": "18.3.1", "react-dom": "18.3.1"}}))
    write(tmp_path / "packages" / "legacy" / "package.json", json.dumps({"dependencies": {"react": "17.0.2"}}))
    write(tmp_path / "apps" / "web" / "src" / "App.jsx", "import React from 'react'\n")

    report = module.detect(tmp_path)
    react = next(item for item in report["detected_technologies"] if item["id"] == "react")
    assert react["version"] in {"18.3.1", "17.0.2"}
    assert react["version_status"] == "declared_range"
    react_paths = {item["path"] for item in react["evidence"]}
    assert any(path.endswith("package.json") for path in react_paths)
    react_recommendation = next(item for item in report["recommendations"] if item["project_type"] == "Web前端-React")
    assert react_recommendation["fact_status"] == "inferred"
    assert react_recommendation["status"] == "rule_based_candidate"
    assert react_recommendation["availability"] == "installable_unverified"
    assert react_recommendation["market_status"] == "not_verified"
    assert all(skill.get("effect") != "减少随机试错，提升调试效率" for skill in react_recommendation["skills"])
    assert all(skill["priority"] == "candidate" and skill["availability"] == "unavailable" for skill in react_recommendation["skills"])


def test_recommendation_does_not_use_root_dependency_for_nested_rule(tmp_path):
    write(tmp_path / "package.json", json.dumps({"name": "root", "dependencies": {}}))
    write(tmp_path / "packages" / "app" / "package.json", json.dumps({"dependencies": {"react": "18.2.0", "react-dom": "18.2.0"}}))
    write(tmp_path / "packages" / "app" / "src" / "App.jsx", "import React from 'react'\n")

    report = module.detect(tmp_path)
    assert any(item["project_type"] == "Web前端-React" for item in report["recommendations"])


def test_depth_limit_is_reported(tmp_path):
    write(tmp_path / "one/two/three/package.json", "{}")
    assert module.detect(tmp_path, max_depth=1)["limits"]["truncated"]
