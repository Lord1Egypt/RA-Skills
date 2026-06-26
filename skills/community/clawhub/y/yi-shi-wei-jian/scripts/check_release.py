from __future__ import annotations

import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SLUG = "yi-shi-wei-jian"
EXPECTED_REPO = "LearnFromHistory-skill"
EXPECTED_HOMEPAGE = "https://github.com/GreatXiaoRY/LearnFromHistory-skill"
EXPECTED_LICENSE = "MIT"
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "homepage",
    "user-invocable",
    "metadata",
}


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def parse_frontmatter(path: Path) -> dict[str, str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError("SKILL.md 缺少 YAML frontmatter。")

    end_marker = "\n---\n"
    end_index = content.find(end_marker, 4)
    if end_index == -1:
        raise ValueError("SKILL.md frontmatter 结束标记不正确。")

    frontmatter = content[4:end_index]
    result: dict[str, str] = {}
    for raw_line in frontmatter.splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            raise ValueError(f"frontmatter 行格式无效: {raw_line}")
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in result:
            raise ValueError(f"frontmatter 存在重复字段: {key}")
        result[key] = value
    return result


def main() -> int:
    required_paths = [
        REPO_ROOT / "SKILL.md",
        REPO_ROOT / "README.md",
        REPO_ROOT / "LICENSE",
        REPO_ROOT / "skill.json",
        REPO_ROOT / "manifest.json",
        REPO_ROOT / "data" / "user_cases.json",
        REPO_ROOT / "examples" / "case_submission_template.json",
        REPO_ROOT / "prompts" / "add_case_intake.md",
        REPO_ROOT / "scripts" / "add_case.py",
        REPO_ROOT / "src" / "case_store.py",
        REPO_ROOT / ".clawhubignore",
        REPO_ROOT / ".github" / "workflows" / "ci.yml",
    ]
    missing = [str(path.relative_to(REPO_ROOT)) for path in required_paths if not path.exists()]
    if missing:
        return fail(f"缺少发布关键文件: {', '.join(missing)}")

    skill_json = json.loads((REPO_ROOT / "skill.json").read_text(encoding="utf-8"))
    manifest_json = json.loads((REPO_ROOT / "manifest.json").read_text(encoding="utf-8"))

    if skill_json.get("slug") != EXPECTED_SLUG:
        return fail("skill.json 的 slug 不正确。")
    if skill_json.get("repository_name") != EXPECTED_REPO:
        return fail("skill.json 的 repository_name 不正确。")
    if skill_json.get("license") != EXPECTED_LICENSE:
        return fail("skill.json 的 license 不正确。")
    if skill_json.get("homepage") != EXPECTED_HOMEPAGE:
        return fail("skill.json 的 homepage 不正确。")

    if manifest_json.get("slug") != EXPECTED_SLUG:
        return fail("manifest.json 的 slug 不正确。")
    if manifest_json.get("repository_name") != EXPECTED_REPO:
        return fail("manifest.json 的 repository_name 不正确。")
    if manifest_json.get("license") != EXPECTED_LICENSE:
        return fail("manifest.json 的 license 不正确。")
    if manifest_json.get("homepage") != EXPECTED_HOMEPAGE:
        return fail("manifest.json 的 homepage 不正确。")

    skill_version = skill_json.get("version")
    manifest_version = manifest_json.get("version")
    if not skill_version or skill_version != manifest_version:
        return fail("skill.json 与 manifest.json 的 version 不一致。")

    try:
        frontmatter = parse_frontmatter(REPO_ROOT / "SKILL.md")
    except ValueError as exc:
        return fail(str(exc))

    unexpected_keys = sorted(set(frontmatter) - ALLOWED_FRONTMATTER_KEYS)
    if unexpected_keys:
        return fail(f"SKILL.md frontmatter 包含非发布友好字段: {', '.join(unexpected_keys)}")

    if frontmatter.get("name") != EXPECTED_SLUG:
        return fail("SKILL.md frontmatter 的 name 必须等于 skill slug。")
    description = frontmatter.get("description", "")
    required_description_markers = [
        "请用/使用/调用",
        "以史为鉴",
        "借古鉴今",
        "历史类比",
        "沙盘推演",
        "organization/business/team",
        "reform",
        "internal conflict",
        "unstable alliance",
        "control-right",
        "leadership/personnel",
    ]
    for marker in required_description_markers:
        if marker not in description:
            return fail(f"SKILL.md frontmatter description 缺少触发提示: {marker}")
    if frontmatter.get("homepage") != EXPECTED_HOMEPAGE:
        return fail("SKILL.md frontmatter 的 homepage 不正确。")
    if frontmatter.get("user-invocable") != "true":
        return fail("SKILL.md frontmatter 的 user-invocable 必须为 true。")

    metadata_text = frontmatter.get("metadata")
    if not metadata_text:
        return fail("SKILL.md frontmatter 缺少 metadata。")

    try:
        metadata = json.loads(metadata_text)
    except json.JSONDecodeError as exc:
        return fail(f"SKILL.md frontmatter 的 metadata 不是有效 JSON: {exc}")

    if metadata.get("slug") != EXPECTED_SLUG:
        return fail("SKILL.md metadata.slug 不正确。")
    if metadata.get("repo_name") != EXPECTED_REPO:
        return fail("SKILL.md metadata.repo_name 不正确。")
    if metadata.get("version") != skill_version:
        return fail("SKILL.md metadata.version 必须与 JSON 元数据一致。")

    openclaw_metadata = metadata.get("openclaw", {})
    if openclaw_metadata.get("always") is True:
        return fail("SKILL.md metadata.openclaw.always 不能为 true，避免请求不必要的常驻权限。")
    if openclaw_metadata.get("skillKey") != EXPECTED_SLUG:
        return fail("SKILL.md metadata.openclaw.skillKey 不正确。")
    if openclaw_metadata.get("homepage") != EXPECTED_HOMEPAGE:
        return fail("SKILL.md metadata.openclaw.homepage 不正确。")

    license_text = (REPO_ROOT / "LICENSE").read_text(encoding="utf-8")
    if "MIT License" not in license_text:
        return fail("LICENSE 文件不是 MIT License。")

    clawhubignore = (REPO_ROOT / ".clawhubignore").read_text(encoding="utf-8").splitlines()
    if "AGENTS.md" not in {line.strip() for line in clawhubignore}:
        return fail(".clawhubignore 必须排除 AGENTS.md，避免把本地 agent 协作指令发布到 ClawHub。")

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    required_readme_markers = [
        EXPECTED_REPO,
        EXPECTED_SLUG,
        "以史为鉴",
        "OpenClaw",
        "--stdin",
        "user_cases.json",
        "MIT",
    ]
    for marker in required_readme_markers:
        if marker not in readme:
            return fail(f"README.md 缺少发布所需说明: {marker}")

    print("发布检查通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
