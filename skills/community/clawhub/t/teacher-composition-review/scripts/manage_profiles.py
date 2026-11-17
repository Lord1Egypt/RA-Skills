"""维护小学作文学生成长档案，并提供安全的本地 JSON 命令行工具。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import unicodedata
from datetime import date
from pathlib import Path
from typing import Any


# 这组等级是教学协议固定的显示顺序，任何自定义顺序都会让跨次趋势失去可比性。
RATINGS = ["优秀", "良好", "合格", "待提高"]
ALLOWED_GRADE_LEVELS = {3, 4, 5, 6}
ALLOWED_REVISION_LEVELS = {"minimal", "moderate", "developmental"}
ALLOWED_COMMENT_STYLES = {"gentle", "professional", "humorous", "concise"}
SETTINGS_FIELDS = {
    "grade_levels",
    "revision_level",
    "comment_style",
    "ratings",
    "profile_enabled",
    "privacy_notice_confirmed",
}
REVIEW_FIELDS = {
    "review_id",
    "date",
    "title",
    "composition_type",
    "grade_level",
    "rating",
    "dimension_ratings",
    "strengths",
    "recurring_issues",
    "next_goals",
}
STAGE_SUMMARY_FIELDS = {"rating", "strengths", "recurring_issues", "next_goals"}
TREND_DIMENSIONS = ("content", "structure", "language", "conventions")
DIMENSION_TREND_FIELDS = {"date", "rating"}
INITIAL_PROFILE_FIELDS = {
    "student_name",
    "class_name",
    "current_grade_level",
    "created_date",
    "feedback_preferences",
    "review_records",
    "stage_summaries",
    "dimension_trends",
    "recurring_issues",
    "documented_progress",
    "current_goals",
}
CURRENT_PROFILE_FIELDS = INITIAL_PROFILE_FIELDS | {"used_review_id_hashes"}
PORTABLE_FIELDS = {"schema_version", "teacher_settings", "student_profile"}


def _store_root(store_dir: Path) -> Path:
    """解析并建立存储根目录，后续所有文件都以这个已解析目录作为安全边界。"""
    root = Path(store_dir).expanduser().resolve()
    if root.exists() and not root.is_dir():
        raise ValueError("档案存储目录不是目录。")
    root.mkdir(parents=True, exist_ok=True)
    return root


def _safe_path(root: Path, *parts: str) -> Path:
    """返回位于存储根目录内的已解析路径，阻止任何路径穿越或符号链接逃逸。"""
    candidate = root.joinpath(*parts).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError("档案路径必须位于指定的 store_dir 内。") from error
    return candidate


def _identity_value(value: str, label: str) -> tuple[str, str]:
    """校验身份显示值并生成稳定键材料，同时保留教师输入的显示文字。"""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label}不能为空。")
    normalized = unicodedata.normalize("NFKC", value).strip()
    # 虽然档案文件名最终使用哈希，仍拒绝路径控制符，避免身份值在其他输出场景被误当作路径。
    if "\x00" in normalized or "/" in normalized or "\\" in normalized or ".." in normalized:
        raise ValueError(f"{label}不能包含路径穿越字符。")
    return value, normalized


def profile_key(class_name: str, student_name: str) -> str:
    """将班级和姓名规范化后哈希为安全键，避免文件名暴露学生身份或碰撞串档。"""
    _, normalized_class = _identity_value(class_name, "班级")
    _, normalized_student = _identity_value(student_name, "姓名")
    material = f"{normalized_class}\n{normalized_student}".encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def _profile_path(store_dir: Path, class_name: str, student_name: str) -> Path:
    """只通过安全哈希键定位学生档案，并再次确认目标路径没有离开存储根目录。"""
    root = _store_root(store_dir)
    return _safe_path(root, "profiles", f"{profile_key(class_name, student_name)}.json")


def _load_json(path: Path, kind: str) -> dict[str, Any]:
    """读取对象 JSON；解析失败时停止操作，绝不以新内容覆盖可能可恢复的旧文件。"""
    if not path.is_file():
        raise ValueError(f"{kind}不存在。")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{kind}文件损坏，未覆盖原文件。") from error
    if not isinstance(value, dict):
        raise ValueError(f"{kind}文件损坏，未覆盖原文件。")
    return value


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """在同目录完成临时写入、刷盘与原子替换，避免中途故障留下半份档案。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        # 同目录临时文件保证 os.replace 处于同一文件系统，替换操作才具有原子性。
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as temporary:
            temporary_name = temporary.name
            json.dump(payload, temporary, ensure_ascii=False, indent=2)
            temporary.write("\n")
            # flush 将 Python 缓冲交给系统，fsync 要求操作系统把文件内容落盘后才允许替换旧档。
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_name, path)
        temporary_name = None
        # 目录刷盘让新文件名替换也尽可能在断电后保持；不支持目录 fsync 的平台可安全跳过。
        try:
            directory_fd = os.open(path.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except OSError:
            pass
    finally:
        if temporary_name is not None:
            try:
                Path(temporary_name).unlink(missing_ok=True)
            except OSError:
                pass


def _validate_settings(settings: dict[str, Any]) -> dict[str, Any]:
    """验证教师长期设置的完整字段集合，防止单次偏好或未知隐私字段混入持久化数据。"""
    if not isinstance(settings, dict) or set(settings) != SETTINGS_FIELDS:
        raise ValueError("教师设置字段必须且只能包含规定字段。")
    grades = settings["grade_levels"]
    if not isinstance(grades, list) or not grades or any(type(item) is not int or item not in ALLOWED_GRADE_LEVELS for item in grades):
        raise ValueError("任教年级必须是 3 到 6 的非空集合。")
    if len(set(grades)) != len(grades):
        raise ValueError("任教年级不能重复。")
    if settings["revision_level"] not in ALLOWED_REVISION_LEVELS:
        raise ValueError("修改尺度不合法。")
    if settings["comment_style"] not in ALLOWED_COMMENT_STYLES:
        raise ValueError("评语风格不合法。")
    if settings["ratings"] != RATINGS:
        raise ValueError("等级必须按固定四级顺序保存。")
    if type(settings["profile_enabled"]) is not bool:
        raise ValueError("档案开关必须是布尔值。")
    # 隐私告知是保存长期设置的硬门槛，必须是字面量 True，不能接受 1 等真值替代。
    if settings["privacy_notice_confirmed"] is not True:
        raise ValueError("必须先确认已完成档案隐私告知，才能保存教师设置。")
    return dict(settings)


def save_teacher_settings(store_dir: Path, settings: dict) -> dict:
    """校验并原子保存教师设置，返回独立副本供调用方展示。"""
    checked = _validate_settings(settings)
    root = _store_root(store_dir)
    _atomic_write_json(_safe_path(root, "teacher-settings.json"), checked)
    return checked


def get_teacher_settings(store_dir: Path) -> dict:
    """读取并重新校验教师设置，避免损坏或旧格式数据被静默当成有效设置。"""
    root = _store_root(store_dir)
    return _validate_settings(_load_json(_safe_path(root, "teacher-settings.json"), "教师设置"))


def _validate_grade_level(grade_level: int) -> None:
    """统一拒绝布尔值和三至六年级以外的值，避免 Python 的 bool/int 混淆。"""
    if type(grade_level) is not int or grade_level not in ALLOWED_GRADE_LEVELS:
        raise ValueError("年级必须是 3 到 6 的整数。")


def _validate_string_list(value: Any, label: str) -> list[str]:
    """限制摘要数组为非空文字列表，确保不会把图片、全文或结构化隐私数据写入档案。"""
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{label}必须是非空文字组成的列表。")
    return list(value)


def _validate_stage_summary(summary: Any) -> dict[str, Any]:
    """校验结构化阶段摘要，只保留重建派生字段所需的四项教学数据。"""
    if not isinstance(summary, dict) or set(summary) != STAGE_SUMMARY_FIELDS:
        raise ValueError("学生档案文件损坏：阶段总结格式不兼容或字段不完整，未覆盖原文件。")
    if summary["rating"] not in RATINGS:
        raise ValueError("学生档案文件损坏：阶段总结等级不合法，未覆盖原文件。")
    return {
        "rating": summary["rating"],
        "strengths": _validate_string_list(summary["strengths"], "阶段总结优点"),
        "recurring_issues": _validate_string_list(summary["recurring_issues"], "阶段总结持续问题"),
        "next_goals": _validate_string_list(summary["next_goals"], "阶段总结下一步目标"),
    }


def _validate_stage_summaries(value: Any) -> list[dict[str, Any]]:
    """拒绝无法无损恢复数组边界的旧字符串摘要，并返回结构化摘要副本。"""
    if not isinstance(value, list):
        raise ValueError("学生档案文件损坏：阶段总结必须是结构化对象列表，未覆盖原文件。")
    return [_validate_stage_summary(summary) for summary in value]


def _new_profile(class_name: str, student_name: str, grade_level: int, feedback_preferences: list[str] | None) -> dict[str, Any]:
    """构造协议要求的最小档案结构；默认只保存教学摘要，不设置任何图片或全文位置。"""
    display_class, _ = _identity_value(class_name, "班级")
    display_student, _ = _identity_value(student_name, "姓名")
    _validate_grade_level(grade_level)
    preferences = [] if feedback_preferences is None else _validate_string_list(feedback_preferences, "反馈偏好")
    return {
        "student_name": display_student,
        "class_name": display_class,
        "current_grade_level": grade_level,
        "created_date": date.today().isoformat(),
        "feedback_preferences": preferences,
        "review_records": [],
        "used_review_id_hashes": [],
        "stage_summaries": [],
        "dimension_trends": {dimension: [] for dimension in TREND_DIMENSIONS},
        "recurring_issues": [],
        "documented_progress": [],
        "current_goals": [],
    }


def create_profile(
    store_dir: Path,
    *,
    class_name: str,
    student_name: str,
    grade_level: int,
    confirmed: bool,
    feedback_preferences: list[str] | None = None,
) -> dict:
    """仅在老师明确确认后建档，已有或损坏文件均拒绝覆盖。"""
    # 确认检查必须发生在解析 store_dir 之前，否则一次未确认操作也会留下空目录等身份痕迹。
    if confirmed is not True:
        raise ValueError("必须获得老师确认后才能创建学生档案。")
    path = _profile_path(store_dir, class_name, student_name)
    if path.exists():
        # 先读取可让损坏文件报出清晰错误；有效文件也不允许“建档”覆盖其历史。
        _load_json(path, "学生档案")
        raise ValueError("学生档案已存在，未覆盖原文件。")
    profile = _new_profile(class_name, student_name, grade_level, feedback_preferences)
    _atomic_write_json(path, profile)
    return profile


def _load_profile(store_dir: Path, class_name: str, student_name: str) -> tuple[Path, dict[str, Any]]:
    """取得安全路径和已存在的档案，同时核对键所对应的原始显示身份没有串档。"""
    path = _profile_path(store_dir, class_name, student_name)
    profile = _load_json(path, "学生档案")
    stored_class, normalized_class = _identity_value(profile.get("class_name"), "档案班级")
    stored_student, normalized_student = _identity_value(profile.get("student_name"), "档案姓名")
    _, requested_class = _identity_value(class_name, "班级")
    _, requested_student = _identity_value(student_name, "姓名")
    if (normalized_class, normalized_student) != (requested_class, requested_student):
        raise ValueError("学生档案身份不匹配，未写入。")
    # 上述变量用于确保显示值可校验；保留赋值以让错误数据不被静默忽略。
    _ = (stored_class, stored_student)
    # 阶段摘要属于所有查询、导出和写入都会接触的核心协议，加载边界即拒绝早期歧义字符串格式。
    profile["stage_summaries"] = _validate_stage_summaries(profile.get("stage_summaries"))
    return path, profile


def get_profile(store_dir: Path, *, class_name: str, student_name: str) -> dict:
    """读取指定班级和学生的档案，并返回 JSON 可序列化的独立对象。"""
    _, profile = _load_profile(store_dir, class_name, student_name)
    # 查询也是协议边界：缺四维评级、损坏趋势或派生摘要不一致时，
    # 不得向 Skill 返回一份表面可用的历史档案，也不在读取时自动猜测修复。
    return _validate_current_profile(profile)


def _validate_review(review: dict[str, Any]) -> dict[str, Any]:
    """只接受协议规定的确认后摘要字段，直接阻止原文、图片路径等额外数据落盘。"""
    if not isinstance(review, dict) or set(review) != REVIEW_FIELDS:
        raise ValueError("批改记录字段不合法，不能保存原文或图片路径。")
    for field in ("review_id", "date", "title", "composition_type"):
        if not isinstance(review[field], str) or not review[field].strip():
            raise ValueError(f"{field}必须是非空文字。")
    try:
        date.fromisoformat(review["date"])
    except ValueError as error:
        raise ValueError("批改日期必须为 YYYY-MM-DD。") from error
    _validate_grade_level(review["grade_level"])
    if review["rating"] not in RATINGS:
        raise ValueError("批改等级不合法。")
    dimension_ratings = review["dimension_ratings"]
    if not isinstance(dimension_ratings, dict) or set(dimension_ratings) != set(TREND_DIMENSIONS):
        raise ValueError("维度评级必须且只能包含 content、structure、language 和 conventions。")
    if any(dimension_ratings[dimension] not in RATINGS for dimension in TREND_DIMENSIONS):
        raise ValueError("维度评级必须使用固定四级之一。")
    for field, label in (("strengths", "优点"), ("recurring_issues", "持续问题"), ("next_goals", "下一步目标")):
        _validate_string_list(review[field], label)
    checked = {field: review[field] for field in REVIEW_FIELDS}
    checked["dimension_ratings"] = dict(dimension_ratings)
    return checked


def _extend_unique(existing: list[str], incoming: list[str]) -> list[str]:
    """按首次出现顺序合并摘要，避免重复问题或目标在档案中无限堆积。"""
    result = list(existing)
    for item in incoming:
        if item not in result:
            result.append(item)
    return result


def _compress_record(record: dict[str, Any]) -> dict[str, Any]:
    """生成结构化阶段摘要，不保存题目、日期、原文或图片路径，也不依赖文本分隔符。"""
    return _validate_stage_summary(
        {
            "rating": record["rating"],
            "strengths": record["strengths"],
            "recurring_issues": record["recurring_issues"],
            "next_goals": record["next_goals"],
        }
    )


def _rebuild_derived_fields(profile: dict[str, Any]) -> None:
    """重建教学摘要、当前目标、年级与最近十次四维趋势。"""
    recurring_issues: list[str] = []
    documented_progress: list[str] = []
    stage_summaries = _validate_stage_summaries(profile.get("stage_summaries"))
    for summary in stage_summaries:
        recurring_issues = _extend_unique(recurring_issues, summary["recurring_issues"])
        documented_progress = _extend_unique(documented_progress, summary["strengths"])
    checked_records: list[dict[str, Any]] = []
    for record in profile["review_records"]:
        checked = _validate_review(record)
        checked_records.append(checked)
        recurring_issues = _extend_unique(recurring_issues, checked["recurring_issues"])
        documented_progress = _extend_unique(documented_progress, checked["strengths"])
    profile["recurring_issues"] = recurring_issues
    profile["documented_progress"] = documented_progress
    # 当前目标是“下一篇”的焦点，不是历史目标合集；优先取最新详细记录，
    # 仅当详细记录全部不存在时才回退到最新阶段总结，并稳定去重后限制为两项。
    goal_source = checked_records[-1]["next_goals"] if checked_records else stage_summaries[-1]["next_goals"] if stage_summaries else []
    profile["current_goals"] = _extend_unique([], goal_source)[:2]

    trends = {dimension: [] for dimension in TREND_DIMENSIONS}
    for checked in checked_records[-10:]:
        for dimension in TREND_DIMENSIONS:
            trends[dimension].append({"date": checked["date"], "rating": checked["dimension_ratings"][dimension]})
    profile["dimension_trends"] = trends
    if checked_records:
        profile["current_grade_level"] = checked_records[-1]["grade_level"]


def _validate_dimension_trends(value: Any) -> dict[str, list[dict[str, str]]]:
    """严格校验四维趋势的日期与评级形状，拒绝旧字符串数组。"""
    if not isinstance(value, dict) or set(value) != set(TREND_DIMENSIONS):
        raise ValueError("维度趋势必须包含固定四个维度。")
    checked: dict[str, list[dict[str, str]]] = {}
    for dimension in TREND_DIMENSIONS:
        entries = value[dimension]
        if not isinstance(entries, list) or len(entries) > 10:
            raise ValueError(f"{dimension} 趋势必须是最多 10 条的列表。")
        checked_entries: list[dict[str, str]] = []
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != DIMENSION_TREND_FIELDS:
                raise ValueError(f"{dimension} 趋势项必须且只能包含 date 与 rating。")
            if not isinstance(entry["date"], str):
                raise ValueError(f"{dimension} 趋势日期必须是文字。")
            date.fromisoformat(entry["date"])
            if entry["rating"] not in RATINGS:
                raise ValueError(f"{dimension} 趋势评级不合法。")
            checked_entries.append(dict(entry))
        checked[dimension] = checked_entries
    return checked


def _review_id_hash(review_id: str) -> str:
    """把已使用的 review_id 转换为不可逆固定长度指纹，用于跨压缩记录去重且不保留原始编号。"""
    return hashlib.sha256(review_id.encode("utf-8")).hexdigest()


def _validate_profile_missing_only_hashes(profile: dict[str, Any]) -> list[dict[str, Any]]:
    """完整校验仅缺少已用 ID 指纹的当前格式档案，并返回详细记录。

    唯一允许缺少的是 `used_review_id_hashes`；ReviewRecord 四维评级、结构化趋势与
    其他当前字段均不做兼容猜测。迁移前先完成整体验证，避免把损坏内容包装成合法档案。
    """
    try:
        if set(profile) != INITIAL_PROFILE_FIELDS:
            raise ValueError("待迁移档案字段集合不完整或含有未知字段。")
        _identity_value(profile["class_name"], "档案班级")
        _identity_value(profile["student_name"], "档案姓名")
        _validate_grade_level(profile["current_grade_level"])
        if not isinstance(profile["created_date"], str):
            raise ValueError("建档日期必须是文字。")
        date.fromisoformat(profile["created_date"])

        _validate_string_list(profile["feedback_preferences"], "反馈偏好")
        _validate_stage_summaries(profile["stage_summaries"])
        _validate_string_list(profile["recurring_issues"], "持续问题")
        _validate_string_list(profile["documented_progress"], "进步记录")
        _validate_string_list(profile["current_goals"], "当前目标")

        _validate_dimension_trends(profile["dimension_trends"])

        records = profile["review_records"]
        if not isinstance(records, list) or len(records) > 10:
            raise ValueError("详细批改记录必须是最多 10 条的列表。")
        checked_records = [_validate_review(record) for record in records]
        review_ids = [record["review_id"] for record in checked_records]
        if len(review_ids) != len(set(review_ids)):
            raise ValueError("详细批改记录编号不能重复。")
        return checked_records
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("学生档案文件损坏，未覆盖原文件。") from error


def _load_or_migrate_used_review_hashes(path: Path, profile: dict[str, Any]) -> list[str]:
    """读取已用编号指纹，或仅为缺少该字段的其余当前格式档案安全迁移。"""
    if "used_review_id_hashes" not in profile:
        # 只有指纹字段恰好缺失且其余当前结构完整合法时才允许迁移。
        checked_records = _validate_profile_missing_only_hashes(profile)
        recovered_hashes: list[str] = []
        for checked_record in checked_records:
            recovered_hash = _review_id_hash(checked_record["review_id"])
            recovered_hashes.append(recovered_hash)
        migration_candidate = {**profile, "used_review_id_hashes": recovered_hashes}
        # 指纹补全只是格式迁移，不能修复或掩盖年级、趋势、目标等已损坏的派生状态。
        # 因此在改动原 profile 或写盘前，先将候选对象通过完整当前档案校验。
        _validate_current_profile(migration_candidate)
        # 已压缩阶段摘要没有原始 review_id，无法恢复也绝不猜测；只迁移仍存在的详细记录编号。
        profile["used_review_id_hashes"] = recovered_hashes
        # 在继续追加前立即原子写回迁移结果，确保迁移本身也不会留下半份档案。
        _atomic_write_json(path, profile)
        return recovered_hashes

    used_hashes = profile["used_review_id_hashes"]
    if (
        not isinstance(used_hashes, list)
        or any(not isinstance(item, str) or len(item) != 64 for item in used_hashes)
        or len(used_hashes) != len(set(used_hashes))
    ):
        raise ValueError("学生档案文件损坏，未覆盖原文件。")
    return used_hashes


def _validate_current_profile(profile: dict[str, Any]) -> dict[str, Any]:
    """完整验证当前档案格式，供便携导入在落盘前拒绝损坏或越权字段。

    导入不允许沿用旧版缺少指纹的宽容迁移规则：便携文件必须是当前完整格式，
    否则无法可靠判断压缩记录之外的编号是否曾被使用，也可能把不完整隐私数据带入新存储。
    """
    try:
        if not isinstance(profile, dict) or set(profile) != CURRENT_PROFILE_FIELDS:
            raise ValueError("学生档案字段不完整或含有未知字段。")
        student_name, _ = _identity_value(profile["student_name"], "档案姓名")
        class_name, _ = _identity_value(profile["class_name"], "档案班级")
        _validate_grade_level(profile["current_grade_level"])
        if not isinstance(profile["created_date"], str):
            raise ValueError("建档日期必须是文字。")
        date.fromisoformat(profile["created_date"])

        checked_lists: dict[str, list[str]] = {}
        for field, label in (
            ("feedback_preferences", "反馈偏好"),
            ("recurring_issues", "持续问题"),
            ("documented_progress", "进步记录"),
            ("current_goals", "当前目标"),
        ):
            checked_lists[field] = _validate_string_list(profile[field], label)
        checked_stage_summaries = _validate_stage_summaries(profile["stage_summaries"])

        checked_dimensions = _validate_dimension_trends(profile["dimension_trends"])

        records = profile["review_records"]
        if not isinstance(records, list) or len(records) > 10:
            raise ValueError("详细批改记录必须是最多 10 条的列表。")
        checked_records = [_validate_review(record) for record in records]
        review_ids = [record["review_id"] for record in checked_records]
        if len(review_ids) != len(set(review_ids)):
            raise ValueError("详细批改记录编号不能重复。")

        hashes = profile["used_review_id_hashes"]
        if (
            not isinstance(hashes, list)
            or any(not isinstance(item, str) or len(item) != 64 or any(char not in "0123456789abcdef" for char in item) for item in hashes)
            or len(hashes) != len(set(hashes))
        ):
            raise ValueError("已用编号指纹必须是唯一的 SHA-256 十六进制值。")
        # 所有尚保留的详细记录都必须能在指纹集合中找到；额外指纹允许代表已经压缩或删除的旧记录。
        if not {_review_id_hash(review_id) for review_id in review_ids}.issubset(hashes):
            raise ValueError("已用编号指纹缺少详细记录对应值。")

        if checked_records:
            expected_grade = checked_records[-1]["grade_level"]
            if profile["current_grade_level"] != expected_grade:
                raise ValueError("当前年级与最新详细记录不一致。")
            expected_trends = {dimension: [] for dimension in TREND_DIMENSIONS}
            for checked_record in checked_records[-10:]:
                for dimension in TREND_DIMENSIONS:
                    expected_trends[dimension].append(
                        {"date": checked_record["date"], "rating": checked_record["dimension_ratings"][dimension]}
                    )
            if checked_dimensions != expected_trends:
                raise ValueError("维度趋势与最近详细记录不一致。")
            expected_goals = _extend_unique([], checked_records[-1]["next_goals"])[:2]
        else:
            expected_goals = _extend_unique([], checked_stage_summaries[-1]["next_goals"])[:2] if checked_stage_summaries else []
            if any(checked_dimensions[dimension] for dimension in TREND_DIMENSIONS):
                raise ValueError("无详细记录时维度趋势应为空。")
        if checked_lists["current_goals"] != expected_goals:
            raise ValueError("当前目标与最新可用记录不一致。")

        expected_issues: list[str] = []
        expected_progress: list[str] = []
        for checked_summary in checked_stage_summaries:
            expected_issues = _extend_unique(expected_issues, checked_summary["recurring_issues"])
            expected_progress = _extend_unique(expected_progress, checked_summary["strengths"])
        for checked_record in checked_records:
            expected_issues = _extend_unique(expected_issues, checked_record["recurring_issues"])
            expected_progress = _extend_unique(expected_progress, checked_record["strengths"])
        if checked_lists["recurring_issues"] != expected_issues:
            raise ValueError("持续问题与详细记录及阶段总结不一致。")
        if checked_lists["documented_progress"] != expected_progress:
            raise ValueError("进步记录与详细记录及阶段总结不一致。")

        return {
            "student_name": student_name,
            "class_name": class_name,
            "current_grade_level": profile["current_grade_level"],
            "created_date": profile["created_date"],
            "feedback_preferences": checked_lists["feedback_preferences"],
            "review_records": checked_records,
            "used_review_id_hashes": list(hashes),
            "stage_summaries": checked_stage_summaries,
            "dimension_trends": checked_dimensions,
            "recurring_issues": checked_lists["recurring_issues"],
            "documented_progress": checked_lists["documented_progress"],
            "current_goals": checked_lists["current_goals"],
        }
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("学生档案文件损坏或含有不允许的隐私字段，未导入。") from error


def append_review(
    store_dir: Path,
    *,
    class_name: str,
    student_name: str,
    review: dict,
    confirmed: bool,
) -> dict:
    """仅在老师明确确认后写入一条摘要，并将第 11 条到来的最早记录压缩。"""
    if confirmed is not True:
        raise ValueError("必须获得老师确认后才能写入档案。")
    checked = _validate_review(review)
    path, loaded_profile = _load_profile(store_dir, class_name, student_name)
    # 追加前完整校验现有档案，避免用新记录重建、掩盖已损坏的年级、趋势或隐私边界。
    if "used_review_id_hashes" not in loaded_profile:
        _load_or_migrate_used_review_hashes(path, loaded_profile)
    profile = _validate_current_profile(loaded_profile)
    records = profile.get("review_records")
    if not isinstance(records, list):
        raise ValueError("学生档案文件损坏，未覆盖原文件。")
    used_hashes = profile["used_review_id_hashes"]
    review_hash = _review_id_hash(checked["review_id"])
    if review_hash in used_hashes:
        raise ValueError("review_id 重复，未写入档案。")
    records.append(checked)
    # 指纹在详细记录压缩或删除后仍保留，确保一个编号在该学生档案生命周期内只能使用一次。
    used_hashes.append(review_hash)
    if len(records) > 10:
        earliest = records.pop(0)
        summaries = profile.get("stage_summaries")
        if not isinstance(summaries, list):
            raise ValueError("学生档案文件损坏，未覆盖原文件。")
        summaries.append(_compress_record(earliest))
    _rebuild_derived_fields(profile)
    _atomic_write_json(path, profile)
    return profile


def delete_review(store_dir: Path, *, class_name: str, student_name: str, review_id: str) -> dict:
    """仅按准确的 review_id 删除一条详细记录，避免模糊匹配误删其他作文。"""
    if not isinstance(review_id, str) or not review_id:
        raise ValueError("review_id必须是非空文字。")
    path, loaded_profile = _load_profile(store_dir, class_name, student_name)
    # 删除前必须先迁移并完整校验受支持的初版档案，否则被删记录会在迁移输入中消失，其编号便可被再次使用。
    if "used_review_id_hashes" not in loaded_profile:
        _load_or_migrate_used_review_hashes(path, loaded_profile)
    profile = _validate_current_profile(loaded_profile)
    records = profile.get("review_records")
    if not isinstance(records, list):
        raise ValueError("学生档案文件损坏，未覆盖原文件。")
    matches = [item for item in records if isinstance(item, dict) and item.get("review_id") == review_id]
    if len(matches) != 1:
        raise ValueError("指定 review_id 不存在，未删除。")
    profile["review_records"] = [item for item in records if item is not matches[0]]
    # 派生字段不能继续暴露或影响已删除记录；编号指纹则按协议保留，防止删除后复用。
    _rebuild_derived_fields(profile)
    _atomic_write_json(path, profile)
    return profile


def update_review(
    store_dir: Path,
    *,
    class_name: str,
    student_name: str,
    review_id: str,
    review: dict,
    confirmed: bool,
) -> dict:
    """仅在老师确认后精确替换一条尚保留明细的批改记录。"""
    # 确认门槛必须先于 store_dir 解析、文件读取和替换记录校验，
    # 以保证 API 与 CLI 的未确认调用均为零副作用。
    if confirmed is not True:
        raise ValueError("必须获得老师确认后才能修正已入档记录。")
    if not isinstance(review_id, str) or not review_id:
        raise ValueError("review_id必须是非空文字。")
    checked = _validate_review(review)
    if checked["review_id"] != review_id:
        raise ValueError("替换记录的 review_id 必须与目标 review_id 完全一致。")

    path, loaded_profile = _load_profile(store_dir, class_name, student_name)
    # 修正涉及所有派生状态，先严格校验完整当前档案并在内存副本上操作，
    # 任何损坏都会在原子写入前被拒绝，不覆盖原文件。
    profile = _validate_current_profile(loaded_profile)
    matches = [index for index, item in enumerate(profile["review_records"]) if item["review_id"] == review_id]
    if len(matches) != 1:
        raise ValueError("指定 review_id 不存在于详细记录中，已压缩记录不能修正。")
    profile["review_records"][matches[0]] = checked
    # used_review_id_hashes 不从详细记录重算，因为其中还保留已压缩或已删除记录的指纹。
    _rebuild_derived_fields(profile)
    _atomic_write_json(path, profile)
    return profile


def delete_profile(store_dir: Path, *, class_name: str, student_name: str, confirmed: bool = False) -> None:
    """只有显式确认时才删除整份档案，并在删除前解析文件以避免误删损坏证据。"""
    if confirmed is not True:
        raise ValueError("删除整个档案必须明确确认。")
    path, _ = _load_profile(store_dir, class_name, student_name)
    # path 已经由 _safe_path 解析并限制在 store_dir 内，unlink 不会触及目录外文件。
    path.unlink()


def export_portable(
    store_dir: Path,
    *,
    class_name: str,
    student_name: str,
    output_path: Path,
) -> Path:
    """导出 UTF-8 便携 JSON，内容只含版本、设置和经严格字段校验的学生档案。"""
    root = _store_root(store_dir)
    output = _safe_path(root, *Path(output_path).parts) if not Path(output_path).is_absolute() else Path(output_path).resolve()
    try:
        output.relative_to(root)
    except ValueError as error:
        raise ValueError("导出路径必须位于指定的 store_dir 内。") from error
    settings = get_teacher_settings(root)
    profile_path, loaded_profile = _load_profile(root, class_name, student_name)
    # 导出与追加使用同一个受限迁移：仅当旧档案唯一缺少 ID 指纹且
    # 其余当前必需字段（包括每条四维评级）全部合法时，才恢复详细记录的指纹。
    _load_or_migrate_used_review_hashes(profile_path, loaded_profile)
    profile = _validate_current_profile(loaded_profile)
    payload = {
        "schema_version": 1,
        "teacher_settings": settings,
        "student_profile": profile,
    }
    # 隐私边界由 TeacherSettings、StudentProfile、ReviewRecord 和 StageSummary
    # 的严格字段白名单保证。允许字段中的题目、目标等是自然语言，
    # 不能再按“字符串看起来像路径”的启发式规则误删合法教学内容。
    _atomic_write_json(output, payload)
    return output


def import_portable(
    store_dir: Path,
    portable_path: str | Path,
    *,
    confirmed: bool = False,
    overwrite: bool = False,
) -> dict:
    """经明确确认后从 store_dir 内恢复一份完整便携档案，并拒绝无意覆盖同名档案。"""
    # 确认必须先于路径解析、读取和建目录，确保 API 与 CLI 均满足未确认导入零副作用。
    if confirmed is not True:
        raise ValueError("必须获得老师确认后才能导入便携档案。")
    payload = _read_json_argument(store_dir, str(portable_path), "便携档案")
    # 先校验便携对象顶层字段，再递进到设置与档案各自的严格 schema；
    # 题目、优点、问题或目标等已允许文字字段只做类型校验，原文保留。
    if set(payload) != PORTABLE_FIELDS or payload.get("schema_version") != 1:
        raise ValueError("便携档案版本或顶层字段不合法，未导入。")
    settings = _validate_settings(payload["teacher_settings"])
    profile = _validate_current_profile(payload["student_profile"])

    root = _store_root(store_dir)
    profile_path = _safe_path(root, "profiles", f"{profile_key(profile['class_name'], profile['student_name'])}.json")
    if profile_path.exists():
        # 先验证旧文件，避免用“覆盖”掩盖本地已有的损坏证据；检查和新档校验均在写入之前完成。
        _validate_current_profile(_load_json(profile_path, "学生档案"))
        if overwrite is not True:
            raise ValueError("同名学生档案已存在；需在确认后显式允许覆盖。")

    # 两个文件分别使用同目录原子替换；所有输入与既有档案已经先完成校验，写入阶段不会因格式错误破坏旧档。
    _atomic_write_json(_safe_path(root, "teacher-settings.json"), settings)
    _atomic_write_json(profile_path, profile)
    return profile


def _read_json_argument(store_dir: Path, path: str, label: str) -> dict:
    """只从 store_dir 内读取 CLI JSON 对象，并将路径、文件或格式问题转换为中文错误。"""
    root = _store_root(store_dir)
    supplied = Path(path)
    # 相对路径一律以显式 store_dir 为基准，而不是随进程当前目录变化；绝对路径仍需通过同一边界检查。
    candidate = supplied.resolve() if supplied.is_absolute() else root.joinpath(supplied).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"{label}路径必须位于指定的 store_dir 内。") from error
    try:
        value = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{label}必须是可读取的 JSON 文件。") from error
    if not isinstance(value, dict):
        raise ValueError(f"{label}必须是 JSON 对象。")
    return value


def _print_json(value: Any) -> None:
    """统一输出 UTF-8 JSON，让教师工具与其他自动化流程都能稳定解析。"""
    print(json.dumps(value, ensure_ascii=False, indent=2))


def main() -> None:
    """解析档案管理子命令；所有写操作都在对应函数内继续执行确认和路径校验。"""
    parser = argparse.ArgumentParser(description="管理小学作文学生成长档案")
    parser.add_argument("--store-dir", required=True, help="档案根目录；必须由调用者显式提供")
    commands = parser.add_subparsers(dest="command", required=True)
    settings_set = commands.add_parser("settings-set")
    settings_set.add_argument("--settings", required=True)
    commands.add_parser("settings-get")
    create = commands.add_parser("create")
    create.add_argument("--class-name", required=True)
    create.add_argument("--student-name", required=True)
    create.add_argument("--grade-level", required=True, type=int)
    create.add_argument("--feedback-preferences")
    create.add_argument("--confirmed", action="store_true", help="老师已明确确认学生身份并同意建档")
    get = commands.add_parser("get")
    get.add_argument("--class-name", required=True)
    get.add_argument("--student-name", required=True)
    append = commands.add_parser("append")
    append.add_argument("--class-name", required=True)
    append.add_argument("--student-name", required=True)
    append.add_argument("--review", required=True)
    append.add_argument("--confirmed", action="store_true", help="老师已明确确认本次摘要")
    update_one = commands.add_parser("update-review")
    update_one.add_argument("--class-name", required=True)
    update_one.add_argument("--student-name", required=True)
    update_one.add_argument("--review-id", required=True)
    update_one.add_argument("--review", required=True)
    update_one.add_argument("--confirmed", action="store_true", help="老师已明确确认修正后的最终摘要")
    delete_one = commands.add_parser("delete-review")
    delete_one.add_argument("--class-name", required=True)
    delete_one.add_argument("--student-name", required=True)
    delete_one.add_argument("--review-id", required=True)
    delete_all = commands.add_parser("delete-profile")
    delete_all.add_argument("--class-name", required=True)
    delete_all.add_argument("--student-name", required=True)
    delete_all.add_argument("--confirm-delete", action="store_true", help="明确确认删除整个档案")
    export = commands.add_parser("export")
    export.add_argument("--class-name", required=True)
    export.add_argument("--student-name", required=True)
    export.add_argument("--output", required=True)
    import_command = commands.add_parser("import")
    import_command.add_argument("--input", required=True)
    import_command.add_argument("--confirmed", action="store_true", help="老师已明确确认恢复便携档案")
    import_command.add_argument("--overwrite", action="store_true", help="明确允许覆盖同名学生档案")
    arguments = parser.parse_args()
    # CLI 建档确认是最前置硬门槛：必须先于 store_dir 的 Path 构造、解析、建目录及偏好文件读取。
    # API 内仍保留同一检查，避免绕过 CLI 直接调用函数时失去保护。
    if arguments.command == "create" and arguments.confirmed is not True:
        parser.error("必须获得老师确认后才能创建学生档案。")
    if arguments.command == "update-review" and arguments.confirmed is not True:
        parser.error("必须获得老师确认后才能修正已入档记录。")
    if arguments.command == "import" and arguments.confirmed is not True:
        parser.error("必须获得老师确认后才能导入便携档案。")
    store_dir = Path(arguments.store_dir)
    try:
        if arguments.command == "settings-set":
            _print_json(save_teacher_settings(store_dir, _read_json_argument(store_dir, arguments.settings, "教师设置")))
        elif arguments.command == "settings-get":
            _print_json(get_teacher_settings(store_dir))
        elif arguments.command == "create":
            preferences = None
            if arguments.feedback_preferences:
                loaded = _read_json_argument(store_dir, arguments.feedback_preferences, "反馈偏好")
                preferences = loaded.get("feedback_preferences")
            _print_json(create_profile(store_dir, class_name=arguments.class_name, student_name=arguments.student_name, grade_level=arguments.grade_level, confirmed=arguments.confirmed, feedback_preferences=preferences))
        elif arguments.command == "get":
            _print_json(get_profile(store_dir, class_name=arguments.class_name, student_name=arguments.student_name))
        elif arguments.command == "append":
            _print_json(append_review(store_dir, class_name=arguments.class_name, student_name=arguments.student_name, review=_read_json_argument(store_dir, arguments.review, "批改记录"), confirmed=arguments.confirmed))
        elif arguments.command == "update-review":
            _print_json(update_review(store_dir, class_name=arguments.class_name, student_name=arguments.student_name, review_id=arguments.review_id, review=_read_json_argument(store_dir, arguments.review, "替换批改记录"), confirmed=arguments.confirmed))
        elif arguments.command == "delete-review":
            _print_json(delete_review(store_dir, class_name=arguments.class_name, student_name=arguments.student_name, review_id=arguments.review_id))
        elif arguments.command == "delete-profile":
            delete_profile(store_dir, class_name=arguments.class_name, student_name=arguments.student_name, confirmed=arguments.confirm_delete)
            _print_json({"deleted": True})
        elif arguments.command == "export":
            _print_json({"output_path": str(export_portable(store_dir, class_name=arguments.class_name, student_name=arguments.student_name, output_path=Path(arguments.output)))})
        elif arguments.command == "import":
            _print_json(import_portable(store_dir, arguments.input, confirmed=arguments.confirmed, overwrite=arguments.overwrite))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
