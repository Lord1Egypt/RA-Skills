"""Import immutable module documents and their chapter/scene indexes."""

from __future__ import annotations

import hashlib
import re
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, cast

from sqlalchemy import func, select

from .campaigns import CampaignNotFoundError
from .database import Database
from .models import (
    Campaign,
    EmbeddingModel,
    ModuleChapter,
    ModuleChunk,
    ModuleSource,
    SceneIndex,
    ToolAudit,
)
from ..modules.chunking import parse_module_markdown
from ..modules.pdf_parser import convert_pdf_to_markdown, page_for_offset
from ..modules.scene_utils import (
    detect_scene_heading_level,
    heading_prefix,
    merge_bilingual_scenes,
    preamble_title,
)
from ..rules.embedding import BgeM3Embedder, Embedder

DEFAULT_EMBEDDING_MODEL_ID = "embedding-bge-m3"
SUPPORTED_MODULE_EXTENSIONS = {
    ".md",
    ".markdown",
    ".pdf",
    ".docx",
    ".pptx",
    ".xlsx",
    ".xls",
    ".html",
    ".htm",
    ".txt",
    ".csv",
    ".json",
    ".xml",
}


class ModuleImportError(RuntimeError):
    """Base error for module document imports."""


class ModuleAlreadyExistsError(ModuleImportError):
    """The campaign already has a module source with this name."""


@dataclass(frozen=True)
class ModuleInfo:
    id: str
    campaign_id: str
    name: str
    source_path: str
    checksum: str | None
    is_active: bool
    chapter_count: int
    scene_count: int
    chunk_count: int
    embeddings: int


@dataclass(frozen=True)
class SceneContentInfo:
    scene_id: str
    module_name: str
    chapter_key: str
    chapter_title: str
    scene_title: str
    start_line: int
    end_line: int
    keywords: list[str]
    content: str


@dataclass(frozen=True)
class _ChapterDocument:
    source_path: Path
    chapter_key: str
    title: str
    content: str
    order_key: tuple[int, str]
    metadata: dict[str, object]


_CHAPTER_PATTERNS = (
    re.compile(r"(?:^|\W)ch(?:apter)?\.?\s*(\d+)", re.IGNORECASE),
    re.compile(r"第\s*(\d+)\s*章"),
)
_CHINESE_CHAPTER_RE = re.compile(r"第\s*([一二三四五六七八九十]+)\s*章")
_CHINESE_NUMBERS = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


def _number_in(value: str) -> int | None:
    for pattern in _CHAPTER_PATTERNS:
        match = pattern.search(value)
        if match:
            return int(match.group(1))
    match = _CHINESE_CHAPTER_RE.search(value)
    return _CHINESE_NUMBERS.get(match.group(1)) if match else None


def _chapter_number(path: Path, fallback: int) -> int:
    return _number_in(path.stem) or fallback


def _chapter_key(title: str, fallback: int) -> tuple[str, tuple[int, str]]:
    number = _number_in(title)
    if number is not None:
        return f"ch.{number}", (number, title)
    appendix = re.search(r"附录\s*([A-ZＡ-Ｚ])", title, re.IGNORECASE)
    if appendix:
        letter = appendix.group(1)
        if "Ａ" <= letter <= "Ｚ":
            letter = chr(ord(letter) - 0xFEE0)
        letter = letter.lower()
        return f"appendix.{letter}", (100 + ord(letter), title)
    return f"ch.{fallback}", (fallback, title)


def _split_pdf_chapters(path: Path, content: str, metadata: dict[str, object]) -> list[_ChapterDocument]:
    headings = list(re.finditer(r"(?m)^#\s+(.+?)\s*$", content))
    candidates: list[dict[str, object]] = []
    for index, heading in enumerate(headings):
        original_end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
        title = heading.group(1).strip()
        key, order_key = _chapter_key(title, index + 1)
        candidates.append(
            {
                "heading": heading,
                "title": title,
                "key": key,
                "order_key": order_key,
                "original_length": original_end - heading.start(),
            }
        )

    selected: list[dict[str, object]] = []
    for number in range(1, 6):
        matches = [item for item in candidates if item["key"] == f"ch.{number}"]
        if matches:
            selected.append(max(matches, key=lambda item: int(item["original_length"])))
    chapter_five_start = min(
        (
            item["heading"].start()
            for item in selected
            if item["key"] == "ch.5"
        ),
        default=len(content),
    )
    selected.extend(
        item
        for item in candidates
        if str(item["key"]).startswith("appendix.")
        and item["heading"].start() > chapter_five_start
    )
    selected.sort(key=lambda item: item["heading"].start())

    used_appendices: set[str] = set()
    documents: list[_ChapterDocument] = []
    first_start = selected[0]["heading"].start() if selected else len(content)
    if content[:first_start].strip():
        front = content[:first_start].strip() + "\n"
        documents.append(
            _ChapterDocument(
                source_path=path,
                chapter_key="frontmatter",
                title="Front Matter",
                content=front,
                order_key=(0, "frontmatter"),
                metadata={
                    **metadata,
                    "page_start": page_for_offset(content, 0),
                    "page_end": page_for_offset(content, first_start),
                },
            )
        )
    for index, item in enumerate(selected):
        heading = item["heading"]
        end = selected[index + 1]["heading"].start() if index + 1 < len(selected) else len(content)
        title = str(item["title"])
        key = str(item["key"])
        order_key = item["order_key"]
        if key.startswith("appendix.") and key in used_appendices:
            suffix = chr(ord(key[-1]) + 1)
            while f"appendix.{suffix}" in used_appendices:
                suffix = chr(ord(suffix) + 1)
            key = f"appendix.{suffix}"
            order_key = (100 + ord(suffix), title)
        if key.startswith("appendix."):
            used_appendices.add(key)
        page_start = page_for_offset(content, heading.start())
        chapter_content = content[heading.start() : end].strip() + "\n"
        if page_start is not None and not chapter_content.startswith("<!-- page:"):
            chapter_content = f"<!-- page: {page_start} -->\n\n{chapter_content}"
        documents.append(
            _ChapterDocument(
                source_path=path,
                chapter_key=key,
                title=title,
                content=chapter_content,
                order_key=order_key,
                metadata={
                    **metadata,
                    "page_start": page_start,
                    "page_end": page_for_offset(content, end),
                },
            )
        )
    return documents


def _title(path: Path, lines: list[str]) -> str:
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def _tags(title: str) -> list[str]:
    lowered = title.lower()
    groups = (
        ("combat", ("combat", "battle", "fight", "encounter", "战斗", "遭遇", "伏击")),
        ("social", ("tavern", "inn", "npc", "酒馆", "旅馆", "交涉")),
        ("transition", ("travel", "journey", "depart", "旅行", "前往", "离开")),
        ("exploration", ("dungeon", "temple", "crypt", "地城", "神殿", "墓穴")),
    )
    found = [tag for tag, words in groups if any(word in lowered for word in words)]
    return found or ["exploration"]


def _scenes(lines: list[str]) -> list[dict[str, object]]:
    """Split lines into scenes; auto-detect heading level for scene boundaries."""
    scene_level, sub_level, _room_level = detect_scene_heading_level(lines)
    scene_prefix = heading_prefix(scene_level)
    sub_prefix = heading_prefix(sub_level) if sub_level else None

    starts = [index for index, line in enumerate(lines) if line.startswith(scene_prefix)]
    if not starts and lines:
        return [
            {
                "title": "Chapter Content",
                "start_line": 1,
                "end_line": len(lines),
                "headings": [],
                "keywords": ["exploration"],
            }
        ]
    scenes: list[dict[str, object]] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        title = lines[start][scene_level + 1 :].strip()
        headings = [
            line.lstrip("# ").strip()
            for line in lines[start + 1 : end]
            if sub_prefix and line.startswith(sub_prefix)
        ]
        scenes.append(
            {
                "title": title,
                "start_line": start + 1,
                "end_line": end,
                "headings": headings,
                "keywords": _tags(title),
            }
        )

    # Preamble before the first scene heading
    if scenes and int(scenes[0]["start_line"]) > 1:
        pend = int(scenes[0]["start_line"]) - 1
        ptitle = preamble_title(lines, pend)
        pheadings = [
            l.lstrip("# ").strip()
            for l in lines[:pend]
            if sub_prefix and l.startswith(sub_prefix)
        ]
        scenes.insert(
            0,
            {
                "title": ptitle,
                "start_line": 1,
                "end_line": pend,
                "headings": pheadings,
                "keywords": _tags(ptitle),
            },
        )

    # Merge adjacent empty scenes (bilingual-split fix)
    return merge_bilingual_scenes(
        scenes,
        subs_key="headings",
        tags_key="keywords",
    )


def _parse_scene_index(lines: list[str]) -> list[dict[str, object]]:
    """Re-parse chapter content with scene/sub-section/room heading logic.

    The heading level used for scene boundaries is auto-detected:
    - H2 (``## ``) is preferred; if none are found H3 (``### ``) is used instead.
    - The level immediately below the scene level becomes untyped sub-sections.
    - Two levels below becomes ``type: "room"`` sub-sections.

    Tags follow the same English + Chinese keyword heuristics as the reference
    ``scene_index.py``.
    """
    scene_level, sub_level, room_level = detect_scene_heading_level(lines)
    scene_prefix = heading_prefix(scene_level)
    sub_prefix = heading_prefix(sub_level) if sub_level else None
    room_prefix = heading_prefix(room_level) if room_level else None

    def _strip_heading(text: str) -> str:
        return text.lstrip("#").strip()

    scenes: list[dict[str, object]] = []
    current_scene: dict[str, object] | None = None

    for i, line in enumerate(lines):
        s = line.strip()
        if s.startswith(scene_prefix) and (sub_prefix is None or not s.startswith(sub_prefix)):
            if current_scene is not None:
                current_scene["end_line"] = i
                scenes.append(current_scene)
            title = _strip_heading(s)
            current_scene = {
                "title": title,
                "start_line": i + 1,
                "end_line": len(lines),
                "type": "section",
                "subsections": [],
                "line_count": 0,
                "tags": cast(list[str], []),
            }
            current_scene["tags"] = _scene_tags(title)

        elif sub_prefix and s.startswith(sub_prefix) and current_scene is not None:
            sub_title = _strip_heading(s)
            current_scene["subsections"].append(
                {"title": sub_title, "line": i + 1, "tags": cast(list[str], [])}
            )
            combat_sub_kw = ["战斗", "遭遇", "陷阱", "推销", "巡逻"]
            if any(kw in sub_title for kw in combat_sub_kw):
                existing = cast(list[str], current_scene["tags"])
                if "combat" not in existing:
                    existing.append("combat")

        elif room_prefix and s.startswith(room_prefix) and current_scene is not None:
            sub_title = _strip_heading(s)
            current_scene["subsections"].append(
                {"title": sub_title, "line": i + 1, "type": "room"}
            )

    if current_scene is not None:
        current_scene["end_line"] = len(lines)
        scenes.append(current_scene)

    # Preamble before the first scene heading
    if scenes and int(scenes[0]["start_line"]) > 1:
        pend = int(scenes[0]["start_line"]) - 1
        ptitle = preamble_title(lines, pend)
        scenes.insert(
            0,
            {
                "title": ptitle,
                "start_line": 1,
                "end_line": pend,
                "type": "section",
                "subsections": [],
                "line_count": pend,
                "tags": _scene_tags(ptitle),
            },
        )

    for scene in scenes:
        scene["line_count"] = int(scene["end_line"]) - int(scene["start_line"]) + 1

    return merge_bilingual_scenes(scenes)


def _scene_tags(title: str) -> list[str]:
    """Assign scene-level tags using the same heuristics as the reference scene_index.py."""
    title_lower = title.lower()

    intro_kw = ["运作", "运行"]
    intro_kw_en = ["running the", "how to", "running this", "about this"]
    if any(kw in title for kw in intro_kw) or any(kw in title_lower for kw in intro_kw_en):
        return ["intro"]

    combat_kw = ["战斗", "遭遇", "冲突", "攻击", "伏击"]
    combat_kw_en = ["battle", "fight", "combat", "ambush", "assault", "skirmish"]
    if any(kw in title for kw in combat_kw) or any(kw in title_lower for kw in combat_kw_en):
        return ["combat", "encounter"]

    dungeon_kw = ["大厅", "地城", "教堂", "墓", "要塞", "堡垒", "塔", "神殿", "墓穴"]
    dungeon_kw_en = [
        "dungeon", "temple", "keep", "fort", "castle", "tower",
        "cathedral", "crypt",
    ]
    if any(kw in title for kw in dungeon_kw) or any(kw in title_lower for kw in dungeon_kw_en):
        return ["exploration", "dungeon"]

    trans_kw = ["逃出", "离开", "前往", "穿越", "旅行", "出发"]
    trans_kw_en = ["escape", "depart", "travel", "journey", "road", "toward", "leave"]
    if any(kw in title for kw in trans_kw) or any(kw in title_lower for kw in trans_kw_en):
        return ["transition"]

    social_kw = ["小镇", "村庄", "城市", "旅馆", "市场", "广场", "港口", "酒馆"]
    social_kw_en = ["town", "village", "city", "tavern", "inn", "market", "harbor", "square"]
    if any(kw in title for kw in social_kw) or any(kw in title_lower for kw in social_kw_en):
        return ["exploration", "social"]

    return ["exploration"]


class ModuleImportService:
    """Register module Markdown files as immutable campaign content."""

    def __init__(
        self,
        database: Database,
        *,
        embedder: Embedder | None = None,
        converter: Callable[[Path], str] | None = None,
    ) -> None:
        self.database = database
        self.embedder = embedder
        self.converter = converter

    def _read_document(self, path: Path) -> tuple[str, dict[str, object]]:
        if path.suffix.lower() in {".md", ".markdown", ".txt"}:
            return path.read_text(encoding="utf-8-sig"), {"converter": "direct-text"}
        if self.converter is not None:
            return self.converter(path), {"converter": "custom"}
        if path.suffix.lower() == ".pdf":
            result = convert_pdf_to_markdown(path)
            if result.warnings:
                raise ModuleImportError("; ".join(result.warnings))
            return result.content, {
                "converter": "pypdf-structured-v1",
                "page_count": result.page_count,
                "bookmark_count": result.bookmark_count,
                "matched_bookmarks": result.matched_bookmarks,
                "heading_count": result.heading_count,
                "room_heading_count": result.room_heading_count,
            }
        from markitdown import MarkItDown

        result = MarkItDown(enable_plugins=False).convert(str(path))
        content = getattr(result, "text_content", None)
        if not isinstance(content, str) or not content.strip():
            raise ModuleImportError(f"MarkItDown produced no text: {path}")
        return content, {"converter": "markitdown"}

    def import_path(
        self,
        campaign_id: str,
        source_path: str | Path = "",
        *,
        name: str | None = None,
        content: str | None = None,
        activate: bool = True,
        embed: bool = True,
        actor_id: str | None = None,
    ) -> ModuleInfo:
        if content:
            cid = campaign_id
            txt = content
            return self._import_content(
                cid, txt,
                name=name,
                activate=activate,
                embed=embed,
                actor_id=actor_id,
            )

        source = Path(source_path).expanduser().resolve()
        files = [source] if source.is_file() else sorted(source.rglob("*"))
        files = [
            path
            for path in files
            if path.is_file() and path.suffix.lower() in SUPPORTED_MODULE_EXTENSIONS
        ]
        if not files:
            raise ModuleImportError(f"no supported module documents found: {source}")
        module_name = (name or source.stem if source.is_file() else name or source.name).strip()
        if not module_name:
            raise ModuleImportError("module name must not be empty")
        embedder = self.embedder or (BgeM3Embedder(show_progress=True) if embed else None)

        digest = hashlib.sha256()
        parsed: list[_ChapterDocument] = []
        for fallback, path in enumerate(files, start=1):
            raw = path.read_bytes()
            digest.update(path.relative_to(source.parent if source.is_file() else source).as_posix().encode())
            digest.update(b"\0")
            digest.update(raw)
            content, conversion_metadata = self._read_document(path)
            if path.suffix.lower() == ".pdf":
                parsed.extend(_split_pdf_chapters(path, content, conversion_metadata))
            else:
                lines = content.splitlines()
                number = _chapter_number(path, fallback)
                parsed.append(
                    _ChapterDocument(
                        source_path=path,
                        chapter_key=f"ch.{number}",
                        title=_title(path, lines),
                        content=content,
                        order_key=(number, path.name.lower()),
                        metadata=conversion_metadata,
                    )
                )
        parsed.sort(key=lambda item: item.order_key)
        return self._finish_import(
            campaign_id, module_name, str(source), digest, parsed,
            embedder, embed, activate, actor_id,
            format_label="converted-markdown",
            source_extensions=sorted({path.suffix.lower() for path in files}),
        )

    def list(self, campaign_id: str) -> list[ModuleInfo]:
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            modules = list(
                session.scalars(
                    select(ModuleSource)
                    .where(ModuleSource.campaign_id == campaign_id)
                    .order_by(ModuleSource.created_at, ModuleSource.id)
                )
            )
            return [self._module_info(session, m, campaign_id) for m in modules]

    def index(self, campaign_id: str) -> list[dict[str, object]]:
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            modules = session.scalars(
                select(ModuleSource)
                .where(ModuleSource.campaign_id == campaign_id)
                .order_by(ModuleSource.name, ModuleSource.id)
            )
            result: list[dict[str, object]] = []
            for module in modules:
                chapters_payload: list[dict[str, object]] = []
                chapters = session.scalars(
                    select(ModuleChapter)
                    .where(ModuleChapter.module_id == module.id)
                    .order_by(ModuleChapter.order_index, ModuleChapter.id)
                )
                for chapter in chapters:
                    scenes = session.scalars(
                        select(SceneIndex)
                        .where(SceneIndex.chapter_id == chapter.id)
                        .order_by(SceneIndex.start_line, SceneIndex.id)
                    )
                    chapters_payload.append(
                        {
                            "id": chapter.id,
                            "chapter_key": chapter.chapter_key,
                            "title": chapter.title,
                            "status": chapter.status,
                            "scenes": [
                                {
                                    "id": scene.id,
                                    "scene_key": scene.scene_key,
                                    "title": scene.title,
                                    "keywords": list(scene.keywords or []),
                                }
                                for scene in scenes
                            ],
                        }
                    )
                result.append(
                    {
                        "id": module.id,
                        "name": module.name,
                        "is_active": module.is_active,
                        "chapters": chapters_payload,
                    }
                )
            return result

    def delete(self, campaign_id: str, module_id: str) -> None:
        """Delete a module and all its chapters, scenes, chunks, and embeddings."""
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            module = session.get(ModuleSource, module_id)
            if module is None or module.campaign_id != campaign_id:
                raise ModuleImportError(
                    f"module not found in campaign {campaign_id}: {module_id}"
                )
            session.delete(module)

    def set_active(self, campaign_id: str, module_id: str, *, active: bool) -> ModuleInfo:
        """Activate or deactivate a module."""
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            module = session.get(ModuleSource, module_id)
            if module is None or module.campaign_id != campaign_id:
                raise ModuleImportError(
                    f"module not found in campaign {campaign_id}: {module_id}"
                )
            if active and not module.is_active:
                for other in session.scalars(
                    select(ModuleSource).where(ModuleSource.campaign_id == campaign_id)
                ):
                    other.is_active = False
            module.is_active = active
            session.flush()
            return self._module_info(session, module, campaign_id)

    def rename(self, campaign_id: str, module_id: str, name: str) -> ModuleInfo:
        """Rename a module subject to the per-campaign unique constraint."""
        name = name.strip()
        if not name:
            raise ValueError("module name must not be empty")
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            module = session.get(ModuleSource, module_id)
            if module is None or module.campaign_id != campaign_id:
                raise ModuleImportError(
                    f"module not found in campaign {campaign_id}: {module_id}"
                )
            existing = session.scalar(
                select(ModuleSource).where(
                    ModuleSource.campaign_id == campaign_id,
                    ModuleSource.name == name,
                    ModuleSource.id != module_id,
                )
            )
            if existing is not None:
                raise ModuleAlreadyExistsError(
                    f"module already exists in campaign {campaign_id}: {name}"
                )
            module.name = name
            session.flush()
            return self._module_info(session, module, campaign_id)

    def _import_content(
        self,
        campaign_id: str,
        text: str,
        *,
        name: str | None = None,
        activate: bool = True,
        embed: bool = True,
        actor_id: str | None = None,
    ) -> ModuleInfo:
        """Import module from a Markdown string (LLM-generated or inline)."""
        if not name:
            # Extract title from first H1
            for line in text.splitlines():
                s = line.strip()
                if s.startswith("# ") and not s.startswith("## "):
                    name = s[2:].strip()
                    break
        if not name:
            raise ModuleImportError("module name must not be empty")
        module_name = name.strip()

        embedder = self.embedder or (BgeM3Embedder(show_progress=True) if embed else None)

        # Split text into chapters by H1 headings
        lines = text.splitlines()
        h1_positions = [
            i for i, l in enumerate(lines)
            if l.startswith("# ") and not l.startswith("## ")
        ]

        if not h1_positions:
            # No H1 — treat entire text as one chapter
            chapters_raw = [(module_name, text, 0)]
        else:
            chapters_raw = []
            for idx, pos in enumerate(h1_positions):
                title = lines[pos][2:].strip()
                end = h1_positions[idx + 1] if idx + 1 < len(h1_positions) else len(lines)
                chapter_text = "\n".join(lines[pos:end])
                chapters_raw.append((title, chapter_text, idx))

        digest = hashlib.sha256(text.encode("utf-8"))
        source = Path("generated://") / module_name
        parsed: list[_ChapterDocument] = []
        for title, chapter_text, idx in chapters_raw:
            parsed.append(
                _ChapterDocument(
                    source_path=source,
                    chapter_key=f"ch.{idx + 1}" if idx > 0 else "frontmatter",
                    title=title,
                    content=chapter_text + "\n",
                    order_key=(idx, title.lower()),
                    metadata={"converter": "generated-v1"},
                )
            )
        parsed.sort(key=lambda item: item.order_key)
        return self._finish_import(
            campaign_id, module_name, str(source), digest, parsed,
            embedder, embed, activate, actor_id,
            format_label="generated-v1",
            source_extensions=[".gen"],
        )

    def _finish_import(
        self,
        campaign_id: str,
        module_name: str,
        source_str: str,
        digest: "hashlib._Hash",
        parsed: list[_ChapterDocument],
        embedder: Any,
        embed: bool,
        activate: bool,
        actor_id: str | None,
        *,
        format_label: str = "converted-markdown",
        source_extensions: list[str] | None = None,
    ) -> ModuleInfo:
        """Shared tail of import_path and _import_content."""
        with self.database.transaction() as session:
            campaign = session.get(Campaign, campaign_id)
            if campaign is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            existing = session.scalar(
                select(ModuleSource).where(
                    ModuleSource.campaign_id == campaign_id,
                    ModuleSource.name == module_name,
                )
            )
            if existing is not None:
                raise ModuleAlreadyExistsError(
                    f"module already exists in campaign {campaign_id}: {module_name}"
                )
            if activate:
                for item in session.scalars(
                    select(ModuleSource).where(ModuleSource.campaign_id == campaign_id)
                ):
                    item.is_active = False

            model_row = None
            if embedder is not None:
                model_row = session.get(EmbeddingModel, DEFAULT_EMBEDDING_MODEL_ID)
                if model_row is None:
                    model_row = EmbeddingModel(
                        id=DEFAULT_EMBEDDING_MODEL_ID,
                        provider="sentence-transformers",
                        model_name=embedder.model_name,
                        dimensions=embedder.dimensions,
                    )
                    session.add(model_row)
                elif (
                    model_row.model_name != embedder.model_name
                    or model_row.dimensions != embedder.dimensions
                ):
                    raise ValueError(
                        "active embedding model metadata does not match the embedder"
                    )
                session.flush()

            module = ModuleSource(
                id=f"module_{uuid.uuid4().hex[:16]}",
                campaign_id=campaign_id,
                name=module_name,
                source_path=source_str,
                checksum=digest.hexdigest(),
                is_active=activate,
                metadata_json={
                    "format": format_label,
                    "chapter_count": len(parsed),
                    "source_extensions": source_extensions or [".gen"],
                },
            )
            session.add(module)
            session.flush()
            scene_count = chunk_count = embedding_count = 0
            current_assigned = False
            for order, document in enumerate(parsed):
                path = document.source_path
                content = document.content
                lines = content.splitlines()
                if document.chapter_key == "frontmatter" or document.chapter_key.startswith(
                    "appendix."
                ):
                    status = "reference"
                elif activate and not current_assigned:
                    status = "current"
                    current_assigned = True
                else:
                    status = "locked"
                chapter = ModuleChapter(
                    id=f"chapter_{uuid.uuid4().hex[:16]}",
                    module_id=module.id,
                    chapter_key=document.chapter_key,
                    title=document.title,
                    source_path=str(path),
                    content=content,
                    order_index=order,
                    status=status,
                    metadata_json={
                        "checksum": hashlib.sha256(content.encode("utf-8")).hexdigest(),
                        "line_count": len(lines),
                        **document.metadata,
                    },
                )
                session.add(chapter)
                session.flush()
                scene_rows: list[SceneIndex] = []
                for scene_order, scene in enumerate(_scenes(lines), start=1):
                    scene_row = SceneIndex(
                        id=f"scene_{uuid.uuid4().hex[:16]}",
                        chapter_id=chapter.id,
                        scene_key=f"scene_{scene_order:03d}",
                        title=str(scene["title"]),
                        start_line=int(scene["start_line"]),
                        end_line=int(scene["end_line"]),
                        headings=list(scene["headings"]),
                        keywords=list(scene["keywords"]),
                    )
                    session.add(scene_row)
                    scene_rows.append(scene_row)
                    scene_count += 1
                session.flush()

                parsed_chunks = parse_module_markdown(content)
                parsed_chunks = [
                    chunk for chunk in parsed_chunks if chunk.chunk_type != "toc"
                ]
                embedding_texts = [
                    f"{module_name} | {chapter.chapter_key} | "
                    f"{' → '.join(chunk.heading_path)}\n{chunk.text}"
                    for chunk in parsed_chunks
                ]
                vectors = (
                    embedder.encode(embedding_texts)
                    if embedder is not None
                    else [None] * len(embedding_texts)
                )
                for chunk, embedding_text, vector in zip(
                    parsed_chunks, embedding_texts, vectors, strict=True
                ):
                    scene_row = next(
                        (
                            scene
                            for scene in scene_rows
                            if scene.start_line <= chunk.start_line <= scene.end_line
                        ),
                        None,
                    )
                    breadcrumb = " → ".join(chunk.heading_path)
                    session.add(
                        ModuleChunk(
                            id=f"module_chunk_{uuid.uuid4().hex[:16]}",
                            module_id=module.id,
                            chapter_id=chapter.id,
                            scene_id=scene_row.id if scene_row else None,
                            embedding_model_id=model_row.id if model_row else None,
                            chunk_index=chunk.chunk_index,
                            heading=chunk.heading,
                            breadcrumb=breadcrumb,
                            start_line=chunk.start_line,
                            end_line=chunk.end_line,
                            char_start=chunk.char_start,
                            char_end=chunk.char_end,
                            page_start=chunk.page_start,
                            page_end=chunk.page_end,
                            chunk_type=chunk.chunk_type,
                            token_count=max(1, len(chunk.text) // 4),
                            content_hash=hashlib.sha256(
                                chunk.text.encode("utf-8")
                            ).hexdigest(),
                            chunk_text=chunk.text,
                            search_text=f"{module_name}\n{chapter.title}\n{breadcrumb}\n{chunk.text}",
                            embedding_json=vector,
                            metadata_json={
                                "embedding_text_hash": hashlib.sha256(
                                    embedding_text.encode("utf-8")
                                ).hexdigest(),
                                "overlap_chars": chunk.overlap_chars,
                            },
                        )
                    )
                    chunk_count += 1
                    embedding_count += vector is not None
            if activate:
                campaign.module_name = module_name
            session.flush()
            session.add(
                ToolAudit(
                    id=f"audit_module_{uuid.uuid4().hex[:16]}",
                    request_id=f"module-import:{uuid.uuid4().hex}",
                    campaign_id=campaign_id,
                    actor_id=actor_id,
                    tool_name="dnd_module_import",
                    engine_function="database.module.import",
                    arguments_json={"name": module_name, "source": source_str},
                    result_json={
                        "module_id": module.id,
                        "chapter_count": len(parsed),
                        "scene_count": scene_count,
                        "chunk_count": chunk_count,
                        "embeddings": embedding_count,
                    },
                    success=True,
                )
            )
            return ModuleInfo(
                id=module.id,
                campaign_id=campaign_id,
                name=module.name,
                source_path=module.source_path,
                checksum=module.checksum,
                is_active=module.is_active,
                chapter_count=len(parsed),
                scene_count=scene_count,
                chunk_count=chunk_count,
                embeddings=embedding_count,
            )

    @staticmethod
    def _module_info(session: Any, module: ModuleSource, campaign_id: str) -> ModuleInfo:
        chapters = list(
            session.scalars(
                select(ModuleChapter).where(ModuleChapter.module_id == module.id)
            )
        )
        chapter_ids = [c.id for c in chapters]
        scene_count = (
            session.scalar(
                select(func.count()).where(SceneIndex.chapter_id.in_(chapter_ids))
            )
            if chapter_ids
            else 0
        )
        chunk_count = session.scalar(
            select(func.count()).where(ModuleChunk.module_id == module.id)
        )
        embedding_count = session.scalar(
            select(func.count()).where(
                ModuleChunk.module_id == module.id,
                ModuleChunk.embedding_json.isnot(None),
            )
        )
        return ModuleInfo(
            id=module.id,
            campaign_id=campaign_id,
            name=module.name,
            source_path=module.source_path,
            checksum=module.checksum,
            is_active=module.is_active,
            chapter_count=len(chapters),
            scene_count=scene_count or 0,
            chunk_count=chunk_count or 0,
            embeddings=embedding_count or 0,
        )

    def read_scene(self, campaign_id: str, scene_id: str) -> SceneContentInfo:
        with self.database.transaction() as session:
            row = session.execute(
                select(SceneIndex, ModuleChapter, ModuleSource)
                .join(ModuleChapter, ModuleChapter.id == SceneIndex.chapter_id)
                .join(ModuleSource, ModuleSource.id == ModuleChapter.module_id)
                .where(
                    SceneIndex.id == scene_id,
                    ModuleSource.campaign_id == campaign_id,
                )
            ).first()
            if row is None:
                raise ModuleImportError(
                    f"scene not found in campaign {campaign_id}: {scene_id}"
                )
            scene, chapter, module = row
            lines = chapter.content.splitlines(keepends=True)
            content = "".join(lines[scene.start_line - 1 : scene.end_line])
            return SceneContentInfo(
                scene_id=scene.id,
                module_name=module.name,
                chapter_key=chapter.chapter_key,
                chapter_title=chapter.title,
                scene_title=scene.title,
                start_line=scene.start_line,
                end_line=scene.end_line,
                keywords=list(scene.keywords or []),
                content=content,
            )

    def export_scene_index(
        self, campaign_id: str, *, output_path: str | Path | None = None
    ) -> dict[str, object]:
        """Export all module scenes in the same format as the dnd-dm-skill scenes_index.json.

        Re-parses chapter content with H2/H3/H4 heading logic that matches the
        reference ``scene_index.py`` parser — H2 boundaries create ``"section"``
        scenes, H3 headings become untyped sub-sections, and H4 headings become
        ``"room"`` sub-sections.  Tags follow the same keyword heuristics.
        """
        with self.database.transaction() as session:
            if session.get(Campaign, campaign_id) is None:
                raise CampaignNotFoundError(f"campaign not found: {campaign_id}")
            modules = session.scalars(
                select(ModuleSource)
                .where(ModuleSource.campaign_id == campaign_id)
                .order_by(ModuleSource.name, ModuleSource.id)
            ).all()

            result: dict[str, object] = {
                "_current_scene": None,
                "_current_module_file": None,
            }
            for module in modules:
                chapters = session.scalars(
                    select(ModuleChapter)
                    .where(ModuleChapter.module_id == module.id)
                    .order_by(ModuleChapter.order_index, ModuleChapter.id)
                ).all()
                for chapter in chapters:
                    content = chapter.content
                    lines = content.splitlines(keepends=True)
                    raw_lines = content.splitlines()
                    parsed = _parse_scene_index(raw_lines)
                    store_key = f"{module.name}:{chapter.title}"
                    result[store_key] = {
                        "filepath": chapter.source_path,
                        "total_lines": len(raw_lines),
                        "scenes": parsed,
                    }
                    if result["_current_module_file"] is None:
                        result["_current_module_file"] = store_key

            if output_path is not None:
                import json

                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(
                    json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            return result
