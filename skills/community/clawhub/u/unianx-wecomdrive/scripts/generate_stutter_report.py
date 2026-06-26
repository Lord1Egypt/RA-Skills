#!/usr/bin/env python3

import argparse
import html
import zipfile
from collections import Counter
from datetime import UTC, datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def col_to_num(col: str) -> int:
    value = 0
    for ch in col:
        if ch.isalpha():
            value = value * 26 + ord(ch.upper()) - 64
    return value


def excel_date(raw: str) -> str:
    base = datetime(1899, 12, 30)
    return (base + timedelta(days=float(raw))).strftime("%Y-%m-%d")


def clean_text(value: str) -> str:
    return (value or "").replace("\n", " ").strip()


def percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def read_shared_strings(book: zipfile.ZipFile) -> list[str]:
    root = ET.fromstring(book.read("xl/sharedStrings.xml"))
    strings = []
    for si in root.findall(f"{NS}si"):
        strings.append("".join(node.text or "" for node in si.iter(f"{NS}t")))
    return strings


def read_sheet(book: zipfile.ZipFile, index: int, shared_strings: list[str]) -> list[list[str]]:
    root = ET.fromstring(book.read(f"xl/worksheets/sheet{index}.xml"))
    rows = []
    max_col = 0
    for row in root.find(f"{NS}sheetData").findall(f"{NS}row"):
        values = {}
        for cell in row.findall(f"{NS}c"):
            ref = cell.attrib["r"]
            col_index = col_to_num("".join(ch for ch in ref if ch.isalpha()))
            max_col = max(max_col, col_index)
            cell_type = cell.attrib.get("t")
            value_node = cell.find(f"{NS}v")
            value = "" if value_node is None else (value_node.text or "")
            if cell_type == "s" and value:
                value = shared_strings[int(value)]
            values[col_index] = value
        rows.append([values.get(col, "") for col in range(1, max_col + 1)])
    return rows


def load_workbook(xlsx_path: Path) -> dict[str, list[list[str]]]:
    with zipfile.ZipFile(xlsx_path) as book:
        shared_strings = read_shared_strings(book)
        return {
            "卡顿数据": read_sheet(book, 1, shared_strings),
            "严重卡顿记录": read_sheet(book, 2, shared_strings),
            "工作表1": read_sheet(book, 3, shared_strings),
        }


def parse_daily(rows: list[list[str]]) -> list[dict]:
    result = []
    for row in rows[1:]:
        if not row or not row[0]:
            continue
        try:
            result.append(
                {
                    "date": excel_date(row[0]),
                    "stutters": int(float(row[1] or 0)),
                    "plays": int(float(row[2] or 0)),
                    "rate": float(row[3] or 0),
                    "gt10": int(float(row[4] or 0)) if row[4] else 0,
                    "gt20": int(float(row[5] or 0)) if row[5] else 0,
                    "note": clean_text(row[6] if len(row) > 6 else ""),
                }
            )
        except ValueError:
            continue
    return result


def parse_severe(rows: list[list[str]]) -> list[dict]:
    result = []
    for row in rows[1:]:
        if not row or not row[0]:
            continue
        try:
            result.append(
                {
                    "date": excel_date(row[0]),
                    "play_time": float(row[1] or 0),
                    "trace": clean_text(row[2]),
                    "resolution": clean_text(row[3]) or "未知",
                    "video": clean_text(row[4]),
                    "session": clean_text(row[5]),
                    "first_frame_ms": int(float(row[6] or 0)),
                    "stall_ms": int(float(row[7] or 0)),
                    "network": clean_text(row[8]) or "未知",
                    "ip": clean_text(row[9]) or "未知",
                    "device": clean_text(row[10]) or "未知",
                }
            )
        except ValueError:
            continue
    return result


def parse_playback(rows: list[list[str]]) -> list[dict]:
    result = []
    for row in rows:
        if len(row) < 10 or not clean_text(row[1]):
            continue
        result.append(
            {
                "scene": clean_text(row[1]),
                "video": clean_text(row[2]),
                "session": clean_text(row[3]),
                "status": clean_text(row[5]),
                "first_frame_ms": float(row[6] or 0),
                "stall_ms": float(row[7] or 0),
            }
        )
    return result


def top_counter(records: list[dict], key: str, limit: int = 10) -> list[tuple[str, int]]:
    return Counter(clean_text(record[key]) or "未知" for record in records).most_common(limit)


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    thead = "".join(f"<th>{html.escape(str(header))}</th>" for header in headers)
    body_rows = []
    for row in rows:
        body_rows.append(
            "<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>"
        )
    return (
        '<table><thead><tr>'
        + thead
        + "</tr></thead><tbody>"
        + "".join(body_rows)
        + "</tbody></table>"
    )


def build_report(xlsx_path: Path, workbook: dict[str, list[list[str]]]) -> str:
    daily = parse_daily(workbook["卡顿数据"])
    severe = parse_severe(workbook["严重卡顿记录"])
    playback = parse_playback(workbook["工作表1"])

    total_stutters = sum(item["stutters"] for item in daily)
    total_plays = sum(item["plays"] for item in daily)
    avg_rate = sum(item["rate"] for item in daily) / len(daily)
    total_gt10 = sum(item["gt10"] for item in daily)
    total_gt20 = sum(item["gt20"] for item in daily)
    max_rate_day = max(daily, key=lambda item: item["rate"])
    min_rate_day = min(daily, key=lambda item: item["rate"])
    noted_days = [item for item in daily if item["note"]]
    severe_by_date = Counter(item["date"] for item in severe).most_common()
    top_networks = top_counter(severe, "network")
    top_resolutions = top_counter(severe, "resolution")
    top_devices = top_counter(severe, "device")
    top_videos = top_counter(severe, "video")
    top_stall = sorted(severe, key=lambda item: item["stall_ms"], reverse=True)[:10]
    top_first_frame = sorted(severe, key=lambda item: item["first_frame_ms"], reverse=True)[:10]
    playback_status = Counter(item["status"] for item in playback).most_common()

    daily_rows = [
        [
            item["date"],
            item["stutters"],
            item["plays"],
            percent(item["rate"]),
            item["gt10"],
            item["gt20"],
            item["note"],
        ]
        for item in daily
    ]

    severe_rows = [
        [
            item["date"],
            item["stall_ms"],
            item["first_frame_ms"],
            item["network"],
            item["resolution"],
            item["device"],
            item["ip"],
            item["video"],
        ]
        for item in top_stall
    ]

    observations = [
        (
            f"统计周期为 {daily[0]['date']} 至 {daily[-1]['date']}，"
            f"共记录播放 {total_plays} 次、卡顿 {total_stutters} 次，平均卡顿率 {percent(avg_rate)}。"
        ),
        (
            f"卡顿率最高日期为 {max_rate_day['date']}，当天 {max_rate_day['stutters']} 次卡顿、"
            f"{max_rate_day['plays']} 次播放，卡顿率 {percent(max_rate_day['rate'])}。"
        ),
        (
            f"卡顿率最低日期为 {min_rate_day['date']}，当天卡顿率 {percent(min_rate_day['rate'])}。"
        ),
        (
            f"严重卡顿明细共 {len(severe)} 条，其中卡顿超过 10 秒 {total_gt10} 次，"
            f"超过 20 秒 {total_gt20} 次。"
        ),
        (
            "从备注看，8 月 7 日开始加入 iOS 数据；8 月 13 日至 8 月 20 日连续出现“标清分辨率”；"
            "8 月 19 日记录了“死亡课上线”。"
        ),
        (
            f"严重卡顿网络类型以 WIFI 为主（{top_networks[0][1]} 条），"
            f"其次为 4G、Mobile:NR 和 5G，说明问题不完全局限于单一移动网络。"
        ),
        (
            f"严重卡顿分辨率以 848*478 为主（{top_resolutions[0][1]} 条），"
            f"1920*1080 次之，和“标清分辨率”备注相互印证。"
        ),
        (
            f"工作表1 中播放事件共 {len(playback)} 条，状态为“异常”{dict(playback_status).get('异常', 0)} 条，"
            f"“播放完成”{dict(playback_status).get('播放完成', 0)} 条。"
        ),
    ]

    def bullet_list(items: list[str]) -> str:
        return "<ul>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"

    def pair_list(title: str, items: list[tuple[str, int]]) -> str:
        rows = [[name, count] for name, count in items]
        return f"<h3>{html.escape(title)}</h3>" + render_table(["维度", "次数"], rows)

    style = """
    body { font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; margin: 36px; color: #1f2937; line-height: 1.65; }
    h1, h2, h3 { color: #0f172a; }
    h1 { font-size: 24px; margin-bottom: 4px; }
    h2 { font-size: 18px; margin-top: 28px; margin-bottom: 8px; border-bottom: 1px solid #dbe3ee; padding-bottom: 6px; }
    h3 { font-size: 15px; margin-top: 20px; margin-bottom: 8px; }
    p.meta { color: #475569; margin-top: 0; }
    .card { background: #f8fafc; border: 1px solid #dbe3ee; padding: 12px 14px; margin: 10px 0; border-radius: 8px; }
    .metrics { display: grid; grid-template-columns: repeat(2, minmax(180px, 1fr)); gap: 10px; margin: 14px 0 18px; }
    .metric { border: 1px solid #dbe3ee; border-radius: 8px; padding: 12px; background: #ffffff; }
    .metric strong { display: block; font-size: 20px; color: #0f766e; }
    table { width: 100%; border-collapse: collapse; margin: 10px 0 18px; font-size: 12px; }
    th, td { border: 1px solid #cbd5e1; padding: 6px 8px; vertical-align: top; }
    th { background: #e2e8f0; }
    ul { margin-top: 8px; }
    .small { font-size: 12px; color: #64748b; }
    """

    metrics_html = """
    <div class="metrics">
      <div class="metric"><span>统计周期</span><strong>{period}</strong></div>
      <div class="metric"><span>总播放次数</span><strong>{plays}</strong></div>
      <div class="metric"><span>总卡顿次数</span><strong>{stutters}</strong></div>
      <div class="metric"><span>平均卡顿率</span><strong>{avg_rate}</strong></div>
      <div class="metric"><span>严重卡顿明细</span><strong>{severe_count}</strong></div>
      <div class="metric"><span>播放事件抽样</span><strong>{playback_count}</strong></div>
    </div>
    """.format(
        period=html.escape(f"{daily[0]['date']} 至 {daily[-1]['date']}"),
        plays=total_plays,
        stutters=total_stutters,
        avg_rate=html.escape(percent(avg_rate)),
        severe_count=len(severe),
        playback_count=len(playback),
    )

    note_rows = [[item["date"], item["note"]] for item in noted_days]

    html_parts = [
        "<html><head><meta charset='utf-8'><style>",
        style,
        "</style></head><body>",
        "<h1>阿里云视频卡顿排查数据分析报告</h1>",
        f"<p class='meta'>来源文件：{html.escape(xlsx_path.name)}<br>生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        metrics_html,
        "<h2>一、结论摘要</h2>",
        bullet_list(observations),
        "<h2>二、每日汇总</h2>",
        render_table(
            ["日期", "卡顿次数", "总播放次数", "卡顿率", ">10s", ">20s", "备注"],
            daily_rows,
        ),
        "<h2>三、关键节点备注</h2>",
        render_table(["日期", "事件"], note_rows),
        "<h2>四、严重卡顿明细分析</h2>",
        pair_list("按日期分布", severe_by_date),
        pair_list("按网络类型分布", top_networks),
        pair_list("按分辨率分布", top_resolutions),
        pair_list("按设备类型分布", top_devices),
        pair_list("按视频 ID 分布", top_videos),
        "<h3>卡顿时长 Top 10</h3>",
        render_table(
            ["日期", "卡顿时长(ms)", "首帧耗时(ms)", "网络", "分辨率", "设备", "地区", "视频ID"],
            severe_rows,
        ),
        "<h3>首帧耗时 Top 10</h3>",
        render_table(
            ["日期", "首帧耗时(ms)", "卡顿时长(ms)", "网络", "分辨率", "设备", "地区", "视频ID"],
            [
                [
                    item["date"],
                    item["first_frame_ms"],
                    item["stall_ms"],
                    item["network"],
                    item["resolution"],
                    item["device"],
                    item["ip"],
                    item["video"],
                ]
                for item in top_first_frame
            ],
        ),
        "<h2>五、播放事件抽样（工作表1）</h2>",
        pair_list("播放状态分布", playback_status),
        pair_list("抽样视频分布", Counter(item["video"] for item in playback).most_common(10)),
        (
            "<div class='card'><strong>建议</strong><br>"
            "1. 优先排查 848*478 标清分辨率链路与相关转码模板。<br>"
            "2. 针对高频视频 ID 单独核查 CDN、首帧耗时与源文件编码参数。<br>"
            "3. 针对首帧耗时 15000ms 的明细重点复核客户端超时、预加载、首包策略。<br>"
            "4. 对 8 月 7 日 iOS 数据接入、8 月 13 日后标清分辨率变更、8 月 19 日“死亡课上线”三个时间点做版本回溯。"
            "</div>"
        ),
        "<p class='small'>说明：本报告基于原始工作簿中的三个工作表自动汇总生成。</p>",
        "</body></html>",
    ]
    return "".join(html_parts)


def build_docx_lines(xlsx_path: Path, workbook: dict[str, list[list[str]]]) -> list[str]:
    daily = parse_daily(workbook["卡顿数据"])
    severe = parse_severe(workbook["严重卡顿记录"])
    playback = parse_playback(workbook["工作表1"])

    total_stutters = sum(item["stutters"] for item in daily)
    total_plays = sum(item["plays"] for item in daily)
    avg_rate = sum(item["rate"] for item in daily) / len(daily)
    total_gt10 = sum(item["gt10"] for item in daily)
    total_gt20 = sum(item["gt20"] for item in daily)
    max_rate_day = max(daily, key=lambda item: item["rate"])
    min_rate_day = min(daily, key=lambda item: item["rate"])
    noted_days = [item for item in daily if item["note"]]
    severe_by_date = Counter(item["date"] for item in severe).most_common()
    top_networks = top_counter(severe, "network", limit=5)
    top_resolutions = top_counter(severe, "resolution", limit=5)
    top_devices = top_counter(severe, "device", limit=8)
    top_videos = top_counter(severe, "video", limit=8)
    top_stall = sorted(severe, key=lambda item: item["stall_ms"], reverse=True)[:10]
    top_first_frame = sorted(severe, key=lambda item: item["first_frame_ms"], reverse=True)[:10]
    playback_status = Counter(item["status"] for item in playback).most_common()

    lines = [
        "阿里云视频卡顿排查数据分析报告",
        f"来源文件：{xlsx_path.name}",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "一、整体结论",
        f"统计周期：{daily[0]['date']} 至 {daily[-1]['date']}。",
        f"总播放次数：{total_plays}；总卡顿次数：{total_stutters}；平均卡顿率：{percent(avg_rate)}。",
        f"严重卡顿（>10s）：{total_gt10} 次；严重卡顿（>20s）：{total_gt20} 次；严重卡顿明细：{len(severe)} 条。",
        f"卡顿率最高日期：{max_rate_day['date']}，卡顿率 {percent(max_rate_day['rate'])}，卡顿 {max_rate_day['stutters']} 次。",
        f"卡顿率最低日期：{min_rate_day['date']}，卡顿率 {percent(min_rate_day['rate'])}，卡顿 {min_rate_day['stutters']} 次。",
        "",
        "二、关键观察",
        "1. 8 月 7 日开始加入 iOS 数据，说明这一时间点前后需要分开看趋势。",
        "2. 8 月 13 日至 8 月 20 日连续备注“标清分辨率”，与严重卡顿记录中 848*478 分辨率占比最高相互印证。",
        "3. 8 月 19 日出现“死亡课上线”备注，建议与上线版本、素材变更、转码参数一起回溯。",
        f"4. 严重卡顿网络类型以 {top_networks[0][0]} 为主，共 {top_networks[0][1]} 条，说明问题并非只集中在移动网络。",
        f"5. 工作表1 中播放事件抽样共 {len(playback)} 条，其中异常 {dict(playback_status).get('异常', 0)} 条，播放完成 {dict(playback_status).get('播放完成', 0)} 条。",
        "",
        "三、每日汇总",
        "日期 | 卡顿次数 | 总播放次数 | 卡顿率 | >10s | >20s | 备注",
    ]

    for item in daily:
        lines.append(
            f"{item['date']} | {item['stutters']} | {item['plays']} | {percent(item['rate'])} | "
            f"{item['gt10']} | {item['gt20']} | {item['note'] or '-'}"
        )

    lines.extend(["", "四、关键节点备注"])
    for item in noted_days:
        lines.append(f"{item['date']}：{item['note']}")

    lines.extend(["", "五、严重卡顿分布"])
    lines.append("按日期分布：")
    lines.extend([f"- {name}：{count}" for name, count in severe_by_date])
    lines.append("按网络类型分布：")
    lines.extend([f"- {name}：{count}" for name, count in top_networks])
    lines.append("按分辨率分布：")
    lines.extend([f"- {name}：{count}" for name, count in top_resolutions])
    lines.append("按设备类型分布：")
    lines.extend([f"- {name}：{count}" for name, count in top_devices])
    lines.append("按视频 ID 分布：")
    lines.extend([f"- {name}：{count}" for name, count in top_videos])

    lines.extend(["", "六、卡顿时长 Top 10", "日期 | 卡顿时长(ms) | 首帧耗时(ms) | 网络 | 分辨率 | 设备 | 地区 | 视频ID"])
    for item in top_stall:
        lines.append(
            f"{item['date']} | {item['stall_ms']} | {item['first_frame_ms']} | {item['network']} | "
            f"{item['resolution']} | {item['device']} | {item['ip']} | {item['video']}"
        )

    lines.extend(["", "七、首帧耗时 Top 10", "日期 | 首帧耗时(ms) | 卡顿时长(ms) | 网络 | 分辨率 | 设备 | 地区 | 视频ID"])
    for item in top_first_frame:
        lines.append(
            f"{item['date']} | {item['first_frame_ms']} | {item['stall_ms']} | {item['network']} | "
            f"{item['resolution']} | {item['device']} | {item['ip']} | {item['video']}"
        )

    lines.extend(
        [
            "",
            "八、建议",
            "1. 优先排查 848*478 标清分辨率链路与相关转码模板。",
            "2. 对高频异常视频 ID 做 CDN、首帧耗时、源文件编码参数复核。",
            "3. 对首帧耗时达到 15000ms 的明细重点检查客户端超时与预加载策略。",
            "4. 以 2025-08-07、2025-08-13、2025-08-19 为版本回溯关键时间点。",
        ]
    )
    return lines


def build_docx_document_xml(lines: list[str]) -> str:
    paragraphs = []
    for index, line in enumerate(lines):
        safe = xml_escape(line)
        if index == 0:
            paragraphs.append(
                "<w:p><w:r><w:rPr><w:b/><w:sz w:val=\"32\"/></w:rPr>"
                f"<w:t>{safe}</w:t></w:r></w:p>"
            )
        elif line == "":
            paragraphs.append("<w:p/>")
        elif line.endswith("、整体结论") or line.endswith("、关键观察") or line.endswith("、每日汇总") or line.endswith("、关键节点备注") or line.endswith("、严重卡顿分布") or line.endswith("、卡顿时长 Top 10") or line.endswith("、首帧耗时 Top 10") or line.endswith("、建议"):
            paragraphs.append(
                "<w:p><w:r><w:rPr><w:b/><w:sz w:val=\"28\"/></w:rPr>"
                f"<w:t>{safe}</w:t></w:r></w:p>"
            )
        else:
            text = safe.replace(" ", "</w:t><w:t xml:space=\"preserve\"> </w:t><w:t>")
            paragraphs.append(f"<w:p><w:r><w:t>{text}</w:t></w:r></w:p>")

    body = "".join(paragraphs) + "<w:sectPr><w:pgSz w:w=\"11906\" w:h=\"16838\"/><w:pgMar w:top=\"1440\" w:right=\"1440\" w:bottom=\"1440\" w:left=\"1440\"/></w:sectPr>"
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>"
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" "
        "xmlns:mc=\"http://schemas.openxmlformats.org/markup-compatibility/2006\" "
        "xmlns:o=\"urn:schemas-microsoft-com:office:office\" "
        "xmlns:r=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" "
        "xmlns:m=\"http://schemas.openxmlformats.org/officeDocument/2006/math\" "
        "xmlns:v=\"urn:schemas-microsoft-com:vml\" "
        "xmlns:wp14=\"http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing\" "
        "xmlns:wp=\"http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing\" "
        "xmlns:w10=\"urn:schemas-microsoft-com:office:word\" "
        "xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" "
        "xmlns:w14=\"http://schemas.microsoft.com/office/word/2010/wordml\" "
        "xmlns:wpg=\"http://schemas.microsoft.com/office/word/2010/wordprocessingGroup\" "
        "xmlns:wpi=\"http://schemas.microsoft.com/office/word/2010/wordprocessingInk\" "
        "xmlns:wne=\"http://schemas.microsoft.com/office/word/2006/wordml\" "
        "xmlns:wps=\"http://schemas.microsoft.com/office/word/2010/wordprocessingShape\" "
        "mc:Ignorable=\"w14 wp14\">"
        f"<w:body>{body}</w:body></w:document>"
    )


def write_minimal_docx(docx_path: Path, lines: list[str]) -> None:
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>"""
    core = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>阿里云视频卡顿排查数据分析报告</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")}</dcterms:modified>
</cp:coreProperties>"""
    app = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex</Application>
</Properties>"""
    document = build_docx_document_xml(lines)

    with zipfile.ZipFile(docx_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types)
        archive.writestr("_rels/.rels", rels)
        archive.writestr("docProps/core.xml", core)
        archive.writestr("docProps/app.xml", app)
        archive.writestr("word/document.xml", document)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a DOCX report from a WeCom stutter workbook export.")
    parser.add_argument("xlsx_path", help="Path to the exported .xlsx file")
    parser.add_argument("--output-dir", default=None, help="Directory for generated files")
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx_path).expanduser().resolve()
    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else Path(__file__).resolve().parent.parent / ".outputs"
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    workbook = load_workbook(xlsx_path)
    html_content = build_report(xlsx_path, workbook)
    docx_lines = build_docx_lines(xlsx_path, workbook)

    stem = xlsx_path.stem + "-分析报告"
    html_path = output_dir / f"{stem}.html"
    docx_path = output_dir / f"{stem}.docx"
    html_path.write_text(html_content, encoding="utf-8")
    write_minimal_docx(docx_path, docx_lines)

    print(f"HTML: {html_path}")
    print(f"DOCX: {docx_path}")


if __name__ == "__main__":
    main()
