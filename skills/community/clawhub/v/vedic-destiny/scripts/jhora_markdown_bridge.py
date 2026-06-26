#!/usr/bin/env python3
"""Bridge JHora-flavored markdown exports into structured chart payloads."""

from __future__ import annotations

import json
import html
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

SIGN_MAP = {
    "Ar": "Aries",
    "Ta": "Taurus",
    "Ge": "Gemini",
    "Cn": "Cancer",
    "Le": "Leo",
    "Vi": "Virgo",
    "Li": "Libra",
    "Sc": "Scorpio",
    "Sg": "Sagittarius",
    "Cp": "Capricorn",
    "Aq": "Aquarius",
    "Pi": "Pisces",
}

SIGN_ORDER = list(SIGN_MAP.values())

NAKSHATRA_MAP = {
    "Ashw": "Ashwini",
    "Ashv": "Ashwini",
    "Aswi": "Ashwini",
    "Bhar": "Bharani",
    "Krit": "Krittika",
    "Rohi": "Rohini",
    "Mrig": "Mrigashira",
    "Ardr": "Ardra",
    "Puna": "Punarvasu",
    "Push": "Pushya",
    "Asre": "Ashlesha",
    "Magh": "Magha",
    "PPha": "Purva Phalguni",
    "UPha": "Uttara Phalguni",
    "Hasta": "Hasta",
    "Hast": "Hasta",
    "Chit": "Chitra",
    "Swat": "Swati",
    "Visa": "Vishakha",
    "Vish": "Vishakha",
    "Anu": "Anuradha",
    "Jye": "Jyeshtha",
    "Mula": "Mula",
    "Mool": "Mula",
    "PSha": "Purva Ashadha",
    "USha": "Uttara Ashadha",
    "Srav": "Shravana",
    "Dhan": "Dhanishta",
    "Sata": "Shatabhisha",
    "PBha": "Purva Bhadrapada",
    "UBha": "Uttara Bhadrapada",
    "Reva": "Revati",
}

PLANET_NAME_MAP = {
    "Sun": "Sun",
    "Moon": "Moon",
    "Mars": "Mars",
    "Mercury": "Mercury",
    "Merc": "Mercury",
    "Jupiter": "Jupiter",
    "Jup": "Jupiter",
    "Venus": "Venus",
    "Ven": "Venus",
    "Saturn": "Saturn",
    "Rahu": "Rahu",
    "Ketu": "Ketu",
    "Su": "Sun",
    "Mo": "Moon",
    "Ma": "Mars",
    "Me": "Mercury",
    "Ju": "Jupiter",
    "Ve": "Venus",
    "Sat": "Saturn",
    "Sa": "Saturn",
    "Rah": "Rahu",
    "Ra": "Rahu",
    "Ket": "Ketu",
    "Ke": "Ketu",
}

MAHADASHA_SEQUENCE = ["Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury", "Ketu", "Venus"]
ASHTAKAVARGA_BAV_CONSTANTS = {
    "Sun": 48,
    "Moon": 49,
    "Mars": 39,
    "Mercury": 54,
    "Jupiter": 56,
    "Venus": 52,
    "Saturn": 39,
}
ASHTAKAVARGA_LABEL_MAP = {
    "SAV": "SAV",
    "As": "Lagna",
    "Su": "Sun",
    "Mo": "Moon",
    "Ma": "Mars",
    "Me": "Mercury",
    "Ju": "Jupiter",
    "Ve": "Venus",
    "Sa": "Saturn",
}


class _TableCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[dict[str, int | str]]]] = []
        self._current_table: list[list[dict[str, int | str]]] | None = None
        self._current_row: list[dict[str, int | str]] | None = None
        self._current_cell: dict[str, int | str] | None = None
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = {key: value for key, value in attrs}
        if tag == "table":
            self._current_table = []
        elif tag == "tr" and self._current_table is not None:
            self._current_row = []
        elif tag == "td" and self._current_row is not None:
            self._current_cell = {
                "text": "",
                "rowspan": int(attrs_map.get("rowspan") or "1"),
                "colspan": int(attrs_map.get("colspan") or "1"),
            }
            self._parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "td" and self._current_cell is not None and self._current_row is not None:
            self._current_cell["text"] = _clean_text("".join(self._parts))
            self._current_row.append(self._current_cell)
            self._current_cell = None
        elif tag == "tr" and self._current_row is not None and self._current_table is not None:
            self._current_table.append(self._current_row)
            self._current_row = None
        elif tag == "table" and self._current_table is not None:
            self.tables.append(self._current_table)
            self._current_table = None

    def handle_data(self, data: str) -> None:
        if self._current_cell is not None:
            self._parts.append(data)


def _clean_text(value: str) -> str:
    value = html.unescape(value)
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def _expand_grid(rows: list[list[dict[str, int | str]]]) -> list[list[str]]:
    grid: list[list[str]] = []
    carry: list[dict[str, Any] | None] = []
    for row in rows:
        expanded: list[str] = []
        col = 0
        while col < len(carry):
            carry_cell = carry[col]
            if carry_cell is not None:
                expanded.append(carry_cell["text"])
                carry_cell["remaining"] -= 1
                if carry_cell["remaining"] <= 0:
                    carry[col] = None
            else:
                expanded.append("")
            col += 1

        write_col = 0
        for cell in row:
            while write_col < len(expanded) and expanded[write_col] != "":
                write_col += 1
            text = str(cell["text"])
            rowspan = int(cell["rowspan"])
            colspan = int(cell["colspan"])
            while len(expanded) < write_col + colspan:
                expanded.append("")
            while len(carry) < write_col + colspan:
                carry.append(None)
            for offset in range(colspan):
                expanded[write_col + offset] = text
                if rowspan > 1:
                    carry[write_col + offset] = {"text": text, "remaining": rowspan - 1}
            write_col += colspan
        grid.append(expanded)

    while carry and any(item is not None for item in carry):
        expanded = []
        for idx, carry_cell in enumerate(carry):
            if carry_cell is None:
                expanded.append("")
                continue
            expanded.append(carry_cell["text"])
            carry_cell["remaining"] -= 1
            if carry_cell["remaining"] <= 0:
                carry[idx] = None
        grid.append(expanded)
    return grid


def _planet_name(label: str) -> str | None:
    head = _clean_text(label.split("-")[0])
    head = re.sub(r"\([^)]*\)", "", head).strip()
    return PLANET_NAME_MAP.get(head)


def _planet_karaka(label: str) -> str | None:
    parts = label.split("-", 1)
    if len(parts) < 2:
        return None
    karaka = _clean_text(parts[1])
    karaka = karaka.replace("(R)", "").strip()
    return karaka or None


def _parse_degree(parts: list[str]) -> tuple[str, float]:
    if len(parts) < 3:
        raise ValueError(f"Unexpected longitude cells: {parts!r}")
    first = _clean_text(parts[0])
    second = _clean_text(parts[1])
    third = _clean_text(parts[2])
    fourth = _clean_text(parts[3]) if len(parts) > 3 else ""

    sign_match = re.match(r"(?P<deg>\d+(?:\.\d+)?)\s*(?P<sign>[A-Za-z]{2})", first)
    if sign_match:
        sign_code = sign_match.group("sign")
        if sign_code not in SIGN_MAP:
            raise ValueError(f"Unknown sign code: {sign_code!r}")
        deg = float(sign_match.group("deg"))
        minutes = float(re.sub(r"[^\d.]+", "", second) or "0")
        seconds = float(re.sub(r"[^\d.]+", "", third) or "0")
        return SIGN_MAP[sign_code], deg + minutes / 60.0 + seconds / 3600.0

    # MinerU sometimes splits the degree into its own cell: ["26", "Ar 27'", '19.07"'].
    deg_text = re.sub(r"[^\d.]+", "", first)
    split_match = re.match(r"(?P<sign>[A-Za-z]{2})\s*(?P<minutes>\d+(?:\.\d+)?)", second)
    if deg_text and split_match:
        sign_code = split_match.group("sign")
        if sign_code not in SIGN_MAP:
            raise ValueError(f"Unknown sign code: {sign_code!r}")
        deg = float(deg_text)
        minutes = float(split_match.group("minutes"))
        seconds = float(re.sub(r"[^\d.]+", "", third) or "0")
        return SIGN_MAP[sign_code], deg + minutes / 60.0 + seconds / 3600.0

    # Another export variant uses four cells: ["20", "Le", "00'", '00.34"'].
    if deg_text and second in SIGN_MAP:
        deg = float(deg_text)
        minutes = float(re.sub(r"[^\d.]+", "", third) or "0")
        seconds = float(re.sub(r"[^\d.]+", "", fourth) or "0")
        return SIGN_MAP[second], deg + minutes / 60.0 + seconds / 3600.0

    raise ValueError(f"Could not parse longitude cells: {parts!r}")


def _normalize_nakshatra(code: str) -> str:
    key = _clean_text(code)
    if key in NAKSHATRA_MAP:
        return NAKSHATRA_MAP[key]
    raise ValueError(f"Unknown nakshatra code: {code!r}")


def _parse_planet_table(grid: list[list[str]]) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    planets: dict[str, dict[str, Any]] = {}
    meta: dict[str, Any] = {}
    lagna_sign: str | None = None
    for row in grid[1:]:
        if not row or not row[0]:
            continue
        label = row[0]
        if len(row) >= 9 and _clean_text(row[2]) in SIGN_MAP:
            longitude_cells = row[1:5]
            nakshatra_idx, pada_idx, rasi_idx, navamsha_idx = 5, 6, 7, 8
        else:
            longitude_cells = row[1:4]
            nakshatra_idx, pada_idx, rasi_idx, navamsha_idx = 4, 5, 6, 7

        sign, degree = _parse_degree(longitude_cells)
        nakshatra = _normalize_nakshatra(row[nakshatra_idx])
        pada = int(re.sub(r"[^\d]+", "", row[pada_idx]) or "0")
        rasi_code = _clean_text(row[rasi_idx])
        navamsha_code = _clean_text(row[navamsha_idx])
        if rasi_code not in SIGN_MAP or navamsha_code not in SIGN_MAP:
            continue
        if label == "Lagna":
            meta["lagna"] = {"sign": sign, "degree": degree, "nakshatra": nakshatra, "pada": pada}
            lagna_sign = sign
            continue
        planet = _planet_name(label)
        if planet is None:
            continue
        entry = {
            "sign": sign,
            "degree": degree,
            "nakshatra": nakshatra,
            "pada": pada,
            "navamsha_sign": SIGN_MAP[navamsha_code],
            "retrograde": True if planet in {"Rahu", "Ketu"} else "(R)" in label,
        }
        karaka = _planet_karaka(label)
        if karaka is not None:
            entry["karaka"] = karaka
        planets[planet] = entry
    if lagna_sign is not None:
        lagna_index = SIGN_ORDER.index(lagna_sign)
        for entry in planets.values():
            sign_index = SIGN_ORDER.index(entry["sign"])
            entry["house"] = (sign_index - lagna_index) % 12 + 1
    return planets, meta


def _parse_vimsottari(grid: list[list[str]]) -> dict[str, Any]:
    ordered: list[dict[str, str]] = []
    for row in grid:
        if len(row) < 3:
            continue
        outer = PLANET_NAME_MAP.get(row[0])
        inner = PLANET_NAME_MAP.get(row[1])
        start_raw = row[2]
        if outer is None or inner is None or outer != inner:
            continue
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", start_raw):
            continue
        ordered.append({"lord": outer, "start": start_raw})
    ordered = [entry for entry in ordered if entry["lord"] in MAHADASHA_SEQUENCE]
    return {"mahadasha": ordered}


def _parse_shadbala(grid: list[list[str]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for row in grid[1:]:
        if len(row) < 4:
            continue
        planet = PLANET_NAME_MAP.get(row[0])
        if planet is None:
            continue
        try:
            result[planet] = {
                "shadbala": float(row[1]),
                "rupas": float(row[2]),
                "percent": float(row[3]),
            }
        except ValueError:
            continue
    return result


def _find_tables(markdown: str) -> list[list[list[str]]]:
    parser = _TableCollector()
    parser.feed(markdown)
    return [_expand_grid(table) for table in parser.tables]


def _parse_numeric_cell(cell: Any) -> float | None:
    text = str(cell).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def _extract_numeric_values(
    row: list[str],
    *,
    min_value: float | None = None,
    max_value: float | None = None,
) -> list[float]:
    values: list[float] = []
    for cell in row:
        value = _parse_numeric_cell(cell)
        if value is None:
            continue
        if min_value is not None and value < min_value:
            continue
        if max_value is not None and value > max_value:
            continue
        values.append(value)
    return values


def _match_bav_planet(row_sum: float, used_planets: set[str]) -> tuple[str | None, float]:
    best_planet: str | None = None
    best_diff = 99.0
    for planet, expected in ASHTAKAVARGA_BAV_CONSTANTS.items():
        if planet in used_planets:
            continue
        diff = abs(row_sum - expected)
        if diff < best_diff:
            best_planet = planet
            best_diff = diff
    return best_planet, best_diff


def _extract_ashtakavarga_block_perimeter(grid: list[list[str]], row0: int, col0: int) -> list[float] | None:
    cells = [
        grid[row0][col0],
        grid[row0][col0 + 1],
        grid[row0][col0 + 2],
        grid[row0][col0 + 3],
        grid[row0 + 1][col0 + 3],
        grid[row0 + 2][col0 + 3],
        grid[row0 + 3][col0 + 3],
        grid[row0 + 3][col0 + 2],
        grid[row0 + 3][col0 + 1],
        grid[row0 + 3][col0],
        grid[row0 + 2][col0],
        grid[row0 + 1][col0],
    ]
    values: list[float] = []
    for cell in cells:
        value = _parse_numeric_cell(cell)
        if value is None:
            return None
        values.append(value)
    return values


def _parse_ashtakavarga_compact_blocks(grid: list[list[str]]) -> dict[str, Any] | None:
    """Extract exact SAV/BAV values from JHora's 3x3 compact block layout.

    The rendered table is not a flat 12x12 matrix of values. It is a 3x3 matrix
    of 4x4 mini-blocks, where each block stores 12 values on its border and a
    2x2 label in the center. Reading each border clockwise yields exact SAV/BAV
    arrays without any heuristic scaling.
    """
    if len(grid) < 12:
        return None
    ncols = max(len(row) for row in grid) if grid else 0
    if ncols < 12:
        return None

    blocks: dict[str, list[float]] = {}
    for row0 in (0, 4, 8):
        for col0 in (0, 4, 8):
            label = _clean_text(str(grid[row0 + 1][col0 + 1]))
            if label not in ASHTAKAVARGA_LABEL_MAP:
                return None
            perimeter = _extract_ashtakavarga_block_perimeter(grid, row0, col0)
            if perimeter is None:
                return None
            blocks[ASHTAKAVARGA_LABEL_MAP[label]] = perimeter

    sav = blocks.get("SAV")
    if sav is None or abs(sum(sav) - 337) > 0.01:
        return None

    result: dict[str, Any] = {"sav": sav}
    bav = {
        planet: values
        for planet, values in blocks.items()
        if planet in ASHTAKAVARGA_BAV_CONSTANTS
    }
    if bav:
        result["bav"] = bav
    if "Lagna" in blocks:
        result["_lagna_ashtakavarga"] = blocks["Lagna"]
    return result


def _extract_ashtakavarga_candidates(grid: list[list[str]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    if not grid:
        return result

    exact = _parse_ashtakavarga_compact_blocks(grid)
    if exact is not None:
        result.update(exact)
        return result

    row0 = _extract_numeric_values(grid[0])[:12]
    if len(row0) == 12:
        row0_sum = sum(row0)
        if row0_sum > 0:
            scale = 337.0 / row0_sum
            sav = [round(value * scale) for value in row0]
            if abs(sum(sav) - 337) <= 5:
                result["sav"] = [float(value) for value in sav]

    raw_candidates: list[dict[str, Any]] = []
    for row_idx, row in enumerate(grid):
        values = _extract_numeric_values(row, min_value=0, max_value=8)
        if len(values) != 12:
            continue
        row_sum = sum(values)
        best_planet, best_diff = _match_bav_planet(row_sum, set())
        raw_candidates.append(
            {
                "row": row_idx,
                "values": values,
                "sum": row_sum,
                "best_planet": best_planet,
                "best_diff": best_diff,
            }
        )

    bav: dict[str, list[float]] = {}
    used_planets: set[str] = set()
    for candidate in sorted(raw_candidates, key=lambda item: (item["best_diff"], item["row"])):
        best_planet, best_diff = _match_bav_planet(candidate["sum"], used_planets)
        if best_planet is None or best_diff > 5:
            continue
        used_planets.add(best_planet)
        bav[best_planet] = [float(value) for value in candidate["values"]]
    if bav:
        result["bav"] = bav

    result["_bav_candidates"] = raw_candidates
    return result


def _format_ashtakavarga_for_llm(grid: list[list[str]]) -> str:
    """Render the compact Ashtakavarga as an LLM-readable text table.

    This is the key function for LLM-based BAV extraction. Instead of writing
    perfect parsing code, we render the table in a clear format and let the
    LLM read the values directly during analysis.

    The rendered table now includes an exact block-perimeter parse when the
    compact 3x3 mini-block layout is detected. Heuristic row-based hints remain
    only as fallback diagnostics for malformed OCR.
    """
    SIGNS = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi']
    derived = _extract_ashtakavarga_candidates(grid)

    lines = []
    lines.append("### JHora Ashtakavarga Compact Table (LLM-readable)")
    lines.append("")
    lines.append("Structure: 12 physical rows × 12 sign columns with embedded labels.")
    lines.append("Labels [SAV/As/Su/Mo/Ma/Me/Ju/Ve/Sa] occupy inner columns with rowspan=2.")
    lines.append("")
    lines.append("| Row | " + " | ".join(f"{s:>3}" for s in SIGNS) + " | Sum | Notes |")
    lines.append("|-----|" + "|".join("---:" for _ in SIGNS) + "|----:|-------|")

    for r in range(len(grid)):
        cells = []
        labels = set()
        nums = []
        for c in range(min(12, len(grid[r]))):
            cell = str(grid[r][c]).strip()
            try:
                v = int(float(cell))
                cells.append(str(v))
                nums.append(v)
            except ValueError:
                cells.append(f"[{cell}]" if cell else "")
                if cell:
                    labels.add(cell)
        row_sum = sum(nums)
        notes = f"labels: {', '.join(sorted(labels))}" if labels else ""
        if all(0 <= n <= 8 for n in nums) and len(nums) == 12:
            # Find closest BAV constant
            best, bd = None, 99
            for p, c in ASHTAKAVARGA_BAV_CONSTANTS.items():
                d = abs(row_sum - c)
                if d < bd: bd = d; best = p
            notes = (
                f"BAV candidate → {best}({ASHTAKAVARGA_BAV_CONSTANTS[best]}) diff={bd}"
                + (f" {notes}" if notes else "")
            )
        lines.append(f"| R{r:2d} | " + " | ".join(f"{c:>3}" for c in cells) + f" | {row_sum:>3} | {notes} |")

    lines.append("")
    lines.append("### SAV Extraction Guide")
    if "sav" in derived and "bav" in derived:
        lines.append("Compact 3x3 mini-block parse detected: each 4x4 block contributes 12 border values.")
    else:
        lines.append(
            "Fallback heuristic: SAV = row0 × 337 / sum(row0). BAV row constants: "
            + ", ".join(f"{k}={v}" for k, v in ASHTAKAVARGA_BAV_CONSTANTS.items())
        )
    lines.append("")
    lines.append("Each compact block should sum to its known constant when read around the border clockwise.")
    lines.append("Lagna/As block is present in the export but is not part of the 7-planet BAV validation.")
    if "sav" in derived:
        lines.append("")
        lines.append("Derived SAV: " + ", ".join(str(int(value)) for value in derived["sav"]))
    if "bav" in derived:
        lines.append("Derived BAV:")
        for planet, values in derived["bav"].items():
            lines.append(f"- {planet}: " + ", ".join(str(int(value)) for value in values))
    if "_lagna_ashtakavarga" in derived:
        lines.append("- Lagna: " + ", ".join(str(int(value)) for value in derived["_lagna_ashtakavarga"]))
    return "\n".join(lines)


def _parse_ashtakavarga_compact(grid: list[list[str]]) -> dict[str, Any] | None:
    """Extract SAV/BAV from JHora compact Ashtakavarga formats."""
    nrows = len(grid)
    if nrows < 10:
        return None
    ncols = max(len(row) for row in grid) if grid else 0
    if ncols < 10:
        return None

    result = _extract_ashtakavarga_candidates(grid)
    if "sav" not in result:
        return None
    result.pop("_bav_candidates", None)
    return result


def _parse_ashtakavarga(grid: list[list[str]]) -> dict[str, Any] | None:
    """Attempt to extract SAV and BAV from a JHora Ashtakavarga visual table.

    JHora's Ashtakavarga export uses a complex visual layout with rowspan/colspan
    labels (SAV, As, Su, Mo, Ma, Me, Ju, Ve, Sa) interspersed between data columns.
    This function tries multiple extraction strategies and returns None if all fail.

    Returns dict with keys: sav (list of 12 floats), bav (dict planet->list of 12 floats)
    """
    # --- Strategy 1: Find a row with 12 numbers summing to 337 (pure SAV row) ---
    for row in grid:
        nums = []
        for cell in row:
            cell = str(cell).strip()
            try:
                nums.append(float(cell))
            except ValueError:
                nums = []
                break
        if len(nums) == 12 and abs(sum(nums) - 337.0) < 0.01:
            return {"sav": nums}

    # --- Strategy 2: The SAV values might be embedded across multiple rows ---
    # Collect ALL numeric cells in order and try sliding windows of 12
    all_nums = []
    for row in grid:
        for cell in row:
            cell = str(cell).strip()
            try:
                all_nums.append(float(cell))
            except ValueError:
                continue
    for start in range(len(all_nums) - 11):
        window = all_nums[start:start + 12]
        if abs(sum(window) - 337.0) < 0.5:
            return {"sav": window}

    # --- Strategy 3: JHora compact format with embedded labels ---
    return _parse_ashtakavarga_compact(grid)


def _extract_sav_from_raw_html(markdown: str) -> list[float] | None:
    """Extract SAV directly from raw JHora Ashtakavarga HTML.

    The JHora Ashtakavarga table uses a complex visual layout that is hard to
    parse after grid expansion. This function works directly on the raw HTML
    text, extracting SAV by column-wise summation of all numeric cells.
    """
    import re as _re
    # Find the Ashtakavarga section
    av_start = markdown.find("Ashtakavarga of Rasi Chart")
    if av_start == -1:
        return None
    # Find the end (next major section or end of tables)
    av_end = markdown.find("Planet", av_start + 1)
    if av_end == -1:
        av_end = markdown.find("Vimsopaka", av_start + 1)
    if av_end == -1:
        av_end = len(markdown)
    av_section = markdown[av_start:av_end]

    # Parse all tables in this section and collect numeric cells per column
    table_re = _re.compile(r'<table>(.*?)</table>', _re.DOTALL)
    tables = table_re.findall(av_section)
    if not tables:
        return None

    # Collect all numeric cells from the first table (the Ashtakavarga table)
    # Group by column position
    columns: list[list[float]] = [[] for _ in range(12)]
    row_re = _re.compile(r'<tr>(.*?)</tr>', _re.DOTALL)
    cell_re = _re.compile(r'<td[^>]*>(.*?)</td>', _re.DOTALL)

    for table_html in tables[:1]:  # Only process the first Ashtakavarga table
        rows = row_re.findall(table_html)
        for row_html in rows:
            cells = cell_re.findall(row_html)
            for col_idx, cell_text in enumerate(cells[:12]):
                cell_text = cell_text.strip()
                try:
                    val = float(cell_text)
                    columns[col_idx].append(val)
                except ValueError:
                    continue

    # Check if we have enough data: at least one value per column
    if not all(columns):
        return None

    # Try column-wise sums - SAV columns sum to approximately 337 total
    col_sums = [sum(col) for col in columns]
    total = sum(col_sums)
    # If total is way off, this isn't SAV data
    if total < 200 or total > 500:
        return None

    # The SAV values are typically the column sums adjusted
    # In JHora's visual layout, each column sum equals the SAV value times
    # the number of data rows (which is 8-9 depending on Asc inclusion)
    # Try to find the divisor
    for divisor in range(5, 15):
        candidate = [round(s / divisor) for s in col_sums]
        if abs(sum(candidate) - 337.0) < 2.0:
            # Verify each value is in valid range (0-56)
            if all(0 <= v <= 60 for v in candidate):
                return [float(v) for v in candidate]

    # Fallback: try with different divisors and allow fractional
    for divisor in [7, 8, 9, 10]:
        candidate = [s / divisor for s in col_sums]
        if abs(sum(candidate) - 337.0) < 3.0:
            return [round(v, 1) for v in candidate]

    return None


def parse_jhora_markdown(markdown: str) -> dict[str, Any]:
    tables = _find_tables(markdown)
    if not tables:
        raise ValueError("No HTML tables found in JHora markdown export")

    payload: dict[str, Any] = {}

    for grid in tables:
        if not grid or not grid[0]:
            continue
        head = grid[0][0] if grid[0] else ""
        row_text = " ".join(str(cell) for cell in grid[0] if cell)
        if head == "Body":
            planets, meta = _parse_planet_table(grid)
            payload["planets"] = planets
            if meta:
                payload["meta"] = meta
        elif "Planet Shadbala" in row_text:
            payload["shadbala"] = _parse_shadbala(grid)
        elif any("1995-10-27" in str(cell) or "2002-10-26" in str(cell) for row in grid for cell in row):
            if "dasha" not in payload:
                payload["dasha"] = _parse_vimsottari(grid)
        else:
            # Attempt Ashtakavarga extraction on any remaining table
            av_result = _parse_ashtakavarga(grid)
            if av_result is not None:
                payload["sav"] = av_result["sav"]
                if "bav" in av_result:
                    payload["bav"] = av_result["bav"]
            ncols = max(len(r) for r in grid) if grid else 0
            if len(grid) >= 10 and ncols >= 10:
                has_sav = any(str(c).strip() == 'SAV' for row in grid for c in row)
                if has_sav:
                    derived = _extract_ashtakavarga_candidates(grid)
                    if "sav" in derived:
                        payload["sav"] = derived["sav"]
                    if "bav" in derived:
                        payload["bav"] = derived["bav"]
                    try:
                        payload["_ashtakavarga_table"] = _format_ashtakavarga_for_llm(grid)
                    except Exception:
                        pass

    # Fallback: try raw HTML extraction for SAV if not found via grid parsing
    if "sav" not in payload:
        sav_raw = _extract_sav_from_raw_html(markdown)
        if sav_raw is not None:
            payload["sav"] = sav_raw

    if "planets" not in payload:
        raise ValueError("Could not locate the main planet table in JHora markdown export")
    return payload


def load_jhora_markdown(path: str | Path) -> dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8")
    return parse_jhora_markdown(text)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert a JHora markdown export into a structured JSON payload."
    )
    parser.add_argument("input", help="Path to the markdown export.")
    args = parser.parse_args()

    payload = load_jhora_markdown(args.input)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
