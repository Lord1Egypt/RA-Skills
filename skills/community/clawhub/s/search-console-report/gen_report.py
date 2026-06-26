import json, os, datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.font_manager as fm
import pandas as pd

# ---------------------------------------------------------------
# Matplotlib font setup
# Use Arial Unicode MS (bundled with macOS) for full CJK + Korean support.
# Falls back to STHeiti if Arial Unicode is not found.
# NEVER use STHeiti alone — it lacks Korean glyphs (shows hollow rectangles).
# ---------------------------------------------------------------
_cn_font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False
try:
    _unicode_font_path = '/Library/Fonts/Arial Unicode.ttf'
    if not os.path.exists(_unicode_font_path):
        _unicode_font_path = _cn_font_path  # fallback to STHeiti
    fm.fontManager.addfont(_unicode_font_path)
    _ufname = fm.FontProperties(fname=_unicode_font_path).get_name()
    matplotlib.rcParams['font.sans-serif'] = [_ufname, 'DejaVu Sans']
except Exception:
    pass

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------
# ReportLab font setup
# Use STHeiti via TTFont — do NOT use UnicodeCIDFont('STSong-Light'),
# which causes narrow English spacing and garbled bullet chars (e.g. • → 煉).
# ---------------------------------------------------------------
pdfmetrics.registerFont(TTFont('CNFont', '/System/Library/Fonts/STHeiti Medium.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('CNFontLight', '/System/Library/Fonts/STHeiti Light.ttc', subfontIndex=0))
pdfmetrics.registerFontFamily('CNFont', normal='CNFontLight', bold='CNFont')

CHART_DIR = "/tmp/report_charts"
os.makedirs(CHART_DIR, exist_ok=True)

with open("/tmp/sc_detailed_data.json") as f:
    raw = json.load(f)

START = raw["start"]
END = raw["end"]
sites_data = raw["sites"]

SITE_NAMES = {
    "https://www.dingtalk-global.com/": "DingTalk Global",
    "https://www.dingtalk.com.hk/": "DingTalk HK",
    "https://www.dingtalk-macau.com/": "DingTalk Macau",
    "https://www.dingtalk-asia.com/": "DingTalk Asia",
}

COLORS = ["#1a73e8", "#e53935", "#43a047", "#fb8c00"]

def get_totals(site):
    rows = sites_data[site]["trend"].get("rows", [])
    clicks = sum(r["clicks"] for r in rows)
    impressions = sum(r["impressions"] for r in rows)
    ctr = (clicks / impressions * 100) if impressions else 0
    positions = [r["position"] for r in rows if r.get("position")]
    avg_pos = sum(positions) / len(positions) if positions else 0
    return clicks, impressions, ctr, avg_pos

# Chart 1: Click trends for all sites
def chart_trends():
    fig, ax = plt.subplots(figsize=(10, 4))
    for i, (site, name) in enumerate(SITE_NAMES.items()):
        rows = sites_data[site]["trend"].get("rows", [])
        if not rows:
            continue
        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["keys"].apply(lambda x: x[0]))
        df = df.sort_values("date")
        ax.plot(df["date"], df["clicks"], label=name, color=COLORS[i], linewidth=2)
    ax.set_title("Daily Clicks - All Sites (90 Days)", fontsize=13, fontweight='bold')
    ax.set_xlabel("Date")
    ax.set_ylabel("Clicks")
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    plt.tight_layout()
    path = f"{CHART_DIR}/trend_all.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path

# Chart 2: Summary bar chart (Clicks vs Impressions)
def chart_summary():
    names = list(SITE_NAMES.values())
    clicks_list = []
    impressions_list = []
    for site in SITE_NAMES:
        c, imp, _, _ = get_totals(site)
        clicks_list.append(c)
        impressions_list.append(imp)

    x = range(len(names))
    fig, ax1 = plt.subplots(figsize=(9, 4))
    ax1.bar([i - 0.2 for i in x], clicks_list, width=0.35, label="Clicks", color=COLORS[0], alpha=0.85)
    ax2 = ax1.twinx()
    ax2.bar([i + 0.2 for i in x], impressions_list, width=0.35, label="Impressions", color=COLORS[1], alpha=0.55)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(names, fontsize=10)
    ax1.set_ylabel("Clicks", color=COLORS[0])
    ax2.set_ylabel("Impressions", color=COLORS[1])
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax1.set_title("Clicks vs Impressions by Site (90 Days)", fontsize=13, fontweight='bold')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    plt.tight_layout()
    path = f"{CHART_DIR}/summary_bar.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path

# Chart per site: top keywords (horizontal bar)
def chart_keywords(site, name, idx):
    rows = sites_data[site]["keywords"].get("rows", [])[:10]
    if not rows:
        return None
    keywords = [r["keys"][0][:30] for r in rows]
    clicks = [r["clicks"] for r in rows]
    fig, ax = plt.subplots(figsize=(9, 3.5))
    ax.barh(keywords[::-1], clicks[::-1], color=COLORS[idx], alpha=0.85)
    ax.set_title(f"{name} - Top Keywords by Clicks", fontsize=12, fontweight='bold')
    ax.set_xlabel("Clicks")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    plt.tight_layout()
    path = f"{CHART_DIR}/kw_{idx}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path

# Chart per site: country pie chart
# NOTE: figsize=(10,7) and radius=0.9 are intentional — smaller sizes make the pie hard to read.
# In the PDF, this chart is placed on its own row (not side-by-side with keywords) for max size.
def chart_countries(site, name, idx):
    rows = sites_data[site]["countries"].get("rows", [])[:8]
    if not rows:
        return None
    countries = [r["keys"][0].upper() for r in rows]
    clicks = [r["clicks"] for r in rows]
    fig, ax = plt.subplots(figsize=(10, 7))
    wedges, texts, autotexts = ax.pie(
        clicks, labels=countries, autopct='%1.1f%%',
        colors=plt.cm.Set3.colors[:len(clicks)], startangle=140,
        textprops={'fontsize': 13}, radius=0.9
    )
    for t in autotexts:
        t.set_fontsize(12)
    ax.set_title(f"{name} - Traffic by Country", fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    path = f"{CHART_DIR}/country_{idx}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    return path

print("Generating charts...")
trend_chart = chart_trends()
summary_chart = chart_summary()
kw_charts = []
country_charts = []
for i, (site, name) in enumerate(SITE_NAMES.items()):
    kw_charts.append(chart_keywords(site, name, i))
    country_charts.append(chart_countries(site, name, i))
print("Charts done.")

# ---------------------------------------------------------------
# PDF Generation
# Margins: 1.2cm on all sides (tighter than default 2cm for more content per page).
# Usable width: A4 (21cm) - 2*1.2cm = 18.6cm.
# All charts and tables use 18.6cm width accordingly.
# ---------------------------------------------------------------
OUTPUT = f"/Users/admin/.accio/accounts/7083102932/agents/DID-F456DA-2B0D4C/project/reports/search_console_report_{datetime.date.today()}.pdf"
doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
                        leftMargin=1.2*cm, rightMargin=1.2*cm,
                        topMargin=1.2*cm, bottomMargin=1.2*cm)

styles = getSampleStyleSheet()
style_h1 = ParagraphStyle('H1', fontName='CNFont', fontSize=22, spaceAfter=6, textColor=colors.HexColor('#1a73e8'))
style_h2 = ParagraphStyle('H2', fontName='CNFont', fontSize=15, spaceAfter=4, spaceBefore=12, textColor=colors.HexColor('#333333'))
style_h3 = ParagraphStyle('H3', fontName='CNFont', fontSize=12, spaceAfter=3, spaceBefore=8, textColor=colors.HexColor('#555555'))
style_body = ParagraphStyle('Body', fontName='CNFontLight', fontSize=10, spaceAfter=4, leading=16)
style_bullet = ParagraphStyle('Bullet', fontName='CNFontLight', fontSize=10, spaceAfter=3, leftIndent=15, leading=15)
style_small = ParagraphStyle('Small', fontName='CNFontLight', fontSize=8, textColor=colors.grey)

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#dddddd'), spaceAfter=8, spaceBefore=4)

def img(path, width=18.6*cm):
    if path and os.path.exists(path):
        return Image(path, width=width, height=width*0.42)
    return Spacer(1, 0.5*cm)

def bullet(text):
    return Paragraph(f"\u2022 {text}", style_bullet)

def table_style():
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a73e8')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'CNFont'),
        ('FONTNAME', (0, 1), (-1, -1), 'CNFontLight'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ])

story = []

# Cover
story.append(Spacer(1, 2*cm))
story.append(Paragraph("Google Search Console", style_h1))
story.append(Paragraph("SEO Performance Report", ParagraphStyle('Cover', fontName='CNFont', fontSize=18, textColor=colors.HexColor('#333333'), spaceAfter=8)))
story.append(hr())
story.append(Paragraph(f"Report Period: {START} to {END} (90 Days)", style_body))
story.append(Paragraph(f"Generated: {datetime.date.today()}", style_body))
story.append(Paragraph("Sites: DingTalk Global / HK / Macau / Asia", style_body))
story.append(Spacer(1, 1*cm))

# Executive Summary table
story.append(Paragraph("Executive Summary", style_h2))
summary_rows = [["Site", "Clicks", "Impressions", "CTR", "Avg. Position"]]
for site, name in SITE_NAMES.items():
    c, imp, ctr, pos = get_totals(site)
    summary_rows.append([name, f"{c:,}", f"{imp:,}", f"{ctr:.2f}%", f"{pos:.1f}"])
t = Table(summary_rows, colWidths=[5.5*cm, 3*cm, 4*cm, 3*cm, 3.1*cm])
t.setStyle(table_style())
story.append(t)
story.append(Spacer(1, 0.5*cm))

# Trend charts
story.append(Paragraph("Traffic Trends", style_h2))
story.append(img(trend_chart, width=18.6*cm))
story.append(Spacer(1, 0.3*cm))
story.append(img(summary_chart, width=18.6*cm))
story.append(PageBreak())

# Per-site sections
for i, (site, name) in enumerate(SITE_NAMES.items()):
    c, imp, ctr, pos = get_totals(site)
    story.append(Paragraph(name, style_h2))
    story.append(hr())

    # KPI metrics row
    metrics = [["Clicks", "Impressions", "CTR", "Avg. Position"],
               [f"{c:,}", f"{imp:,}", f"{ctr:.2f}%", f"{pos:.1f}"]]
    mt = Table(metrics, colWidths=[4.65*cm, 4.65*cm, 4.65*cm, 4.65*cm])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8f0fe')),
        ('FONTNAME', (0, 0), (-1, 0), 'CNFont'),
        ('FONTNAME', (0, 1), (-1, 1), 'CNFont'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.HexColor('#cccccc')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(mt)
    story.append(Spacer(1, 0.4*cm))

    # Keywords chart (full width)
    story.append(Paragraph("Top Keywords by Clicks", style_h3))
    story.append(img(kw_charts[i], width=18.6*cm))
    story.append(Spacer(1, 0.3*cm))

    # Country pie chart — separate row for maximum size
    story.append(Paragraph("Traffic by Country", style_h3))
    story.append(img(country_charts[i], width=16*cm))

    # Top Pages table
    # IMPORTANT: Use Paragraph() for all cells (especially Page column) to enable word-wrap.
    # Plain strings do NOT wrap and will overflow into adjacent columns.
    story.append(Paragraph("Top Pages", style_h3))
    style_cell = ParagraphStyle('Cell', fontName='CNFontLight', fontSize=9, leading=13, wordWrap='CJK')
    style_cell_hd = ParagraphStyle('CellHd', fontName='CNFont', fontSize=9, leading=13, textColor=colors.white)
    page_rows = [[Paragraph("Page", style_cell_hd), Paragraph("Clicks", style_cell_hd),
                  Paragraph("Impressions", style_cell_hd), Paragraph("CTR", style_cell_hd),
                  Paragraph("Position", style_cell_hd)]]
    for r in sites_data[site]["pages"].get("rows", [])[:8]:
        page = r["keys"][0].replace("https://", "").replace(site.replace("https://", ""), "")
        page_rows.append([
            Paragraph(page, style_cell),
            Paragraph(f"{r['clicks']:,}", style_cell),
            Paragraph(f"{r['impressions']:,}", style_cell),
            Paragraph(f"{r['ctr']*100:.2f}%", style_cell),
            Paragraph(f"{r['position']:.1f}", style_cell),
        ])
    pt = Table(page_rows, colWidths=[9*cm, 2.4*cm, 3.2*cm, 2*cm, 2*cm])
    pt.setStyle(table_style())
    story.append(pt)
    story.append(PageBreak())

# SEO Recommendations
story.append(Paragraph("SEO Recommendations", style_h2))
story.append(hr())

for i, (site, name) in enumerate(SITE_NAMES.items()):
    c, imp, ctr, pos = get_totals(site)
    story.append(Paragraph(f"{name}", style_h3))

    recs = []
    if ctr < 5:
        recs.append(f"[P0] CTR is {ctr:.2f}% (below 5%) — optimize page titles and meta descriptions to improve click-through rate.")
    if pos > 15:
        recs.append(f"[P0] Average position {pos:.1f} is low — focus on content quality and backlink building.")
    elif 5 < pos <= 15:
        recs.append(f"[P1] Average position {pos:.1f} is on page 1-2 boundary — optimize target keywords to break into top 5.")

    countries = sites_data[site]["countries"].get("rows", [])
    if countries:
        top_country = countries[0]["keys"][0].upper()
        recs.append(f"[P1] Top traffic country is {top_country} — create more localized content for this market.")

    devices = sites_data[site]["devices"].get("rows", [])
    mobile_clicks = sum(r["clicks"] for r in devices if r["keys"][0].lower() == "mobile")
    total_clicks = sum(r["clicks"] for r in devices) or 1
    if mobile_clicks / total_clicks > 0.6:
        recs.append("[P1] Mobile traffic exceeds 60% — prioritize mobile UX and Core Web Vitals optimization.")

    recs.append("[P2] Implement hreflang tags for all multi-language/region pages to avoid duplicate content issues.")
    recs.append("[P2] Submit complete sitemap including all article URLs to Google Search Console.")

    for rec in recs:
        story.append(bullet(rec))
    story.append(Spacer(1, 0.3*cm))

story.append(hr())
story.append(Paragraph(f"Report generated by Accio | {datetime.date.today()} | Data source: Google Search Console API", style_small))

print("Building PDF...")
doc.build(story)
print(f"PDF saved to: {OUTPUT}")
