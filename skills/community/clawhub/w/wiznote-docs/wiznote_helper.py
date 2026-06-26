from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import re
from urllib.parse import quote


@dataclass(frozen=True)
class LoginResult:
    token: str
    kb_server: str
    kb_guid: str


def parse_login_result(payload: dict) -> LoginResult:
    code = payload.get("returnCode")
    if code != 200:
        raise ValueError(f"WizNote login failed with returnCode={code}: {payload.get('returnMessage', '')}")
    result = payload.get("result")
    if not isinstance(result, dict):
        raise ValueError("WizNote login payload missing result object")
    token = result.get("token")
    kb_server = result.get("kbServer")
    kb_guid = result.get("kbGuid")
    if not isinstance(token, str) or not token:
        raise ValueError("WizNote login payload missing token")
    if not isinstance(kb_server, str) or not kb_server:
        raise ValueError("WizNote login payload missing kbServer")
    if not isinstance(kb_guid, str) or not kb_guid:
        raise ValueError("WizNote login payload missing kbGuid")
    return LoginResult(
        token=token,
        kb_server=kb_server.rstrip("/"),
        kb_guid=kb_guid,
    )


def normalize_category_root(category_root: str) -> str:
    if not isinstance(category_root, str) or not category_root:
        raise ValueError("Category root must be a non-empty string")
    normalized = category_root if category_root.endswith("/") else f"{category_root}/"
    path = PurePosixPath(normalized)
    if not path.is_absolute():
        raise ValueError(f"Category root must be an absolute WizNote path: {category_root}")
    parts = path.parts[1:]
    if not parts:
        raise ValueError("Category root must not be the WizNote root")
    if any(part in {".", ".."} for part in parts):
        raise ValueError(f"Category root contains invalid path segments: {category_root}")
    return "/" + "/".join(parts) + "/"


def resolve_category(category_root: str, category: str = "") -> str:
    root = PurePosixPath(normalize_category_root(category_root))
    if not category:
        return str(root)
    category_path = PurePosixPath(category)
    if category_path.is_absolute():
        candidate = category_path
    else:
        candidate = root.joinpath(category_path)
    parts = candidate.parts[1:]
    root_parts = root.parts[1:]
    if parts[: len(root_parts)] != root_parts:
        raise ValueError(f"Category {category} is outside category root {root}")
    if any(part in {".", ".."} for part in parts):
        raise ValueError(f"Category {category} is outside category root {root}")
    return "/" + "/".join(parts) + "/"


def note_list_path(kb_guid: str, category: str, *, start: int = 0, count: int = 100) -> str:
    encoded = quote(category, safe="")
    return (
        f"/ks/note/list/category/{kb_guid}"
        f"?start={start}&count={count}&category={encoded}&orderBy=modified&ascending=desc"
    )


def mirror_output_path(repo_root: Path, category_root: str, category: str, title: str) -> Path:
    root = PurePosixPath(normalize_category_root(category_root))
    target = PurePosixPath(resolve_category(category_root, category))
    root_parts = root.parts[1:]
    target_parts = target.parts[1:]
    remainder = target_parts[len(root_parts):]
    if any(sep in title for sep in ("/", "\\")) or ".." in title:
        raise ValueError(f"Unsafe note title: {title}")
    normalized_title = " ".join(title.split()).strip()
    slug = re.sub(r"\s+", "-", normalized_title)
    if not slug:
        raise ValueError(f"Unsafe note title: {title}")
    base = repo_root / "docs" / "wiznote-mirror"
    for part in remainder:
        base = base / part
    final_path = (base / f"{slug}.md").resolve(strict=False)
    mirror_root = (repo_root / "docs" / "wiznote-mirror").resolve(strict=False)
    if mirror_root not in final_path.parents:
        raise ValueError(f"Mirror path escaped root: {final_path}")
    return final_path


class _BodyExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.in_body = False
        self.parts: list[str] = []
        self.found_body = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "body":
            self.in_body = True
            self.found_body = True
            return
        if self.in_body:
            start_tag = self.get_starttag_text()
            if start_tag is not None:
                self.parts.append(start_tag)

    def handle_endtag(self, tag: str) -> None:
        if tag == "body":
            self.in_body = False
            return
        if self.in_body:
            self.parts.append(f"</{tag}>")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.in_body:
            start_tag = self.get_starttag_text()
            if start_tag is not None:
                self.parts.append(start_tag)

    def handle_data(self, data: str) -> None:
        if self.in_body:
            self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        if self.in_body:
            self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self.in_body:
            self.parts.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        if self.in_body:
            self.parts.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        if self.in_body:
            self.parts.append(f"<!{decl}>")

    def handle_pi(self, data: str) -> None:
        if self.in_body:
            self.parts.append(f"<?{data}>")


def extract_html_body(html: str) -> str:
    extractor = _BodyExtractor()
    extractor.feed(html)
    extractor.close()
    if extractor.found_body:
        return "".join(extractor.parts)
    return html
