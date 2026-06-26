# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('MSYH', 'C:/Windows/Fonts/msyh.ttc'))
pdfmetrics.registerFont(TTFont('MSYHBD', 'C:/Windows/Fonts/msyhbd.ttc'))
pdfmetrics.registerFont(TTFont('SIMHEI', 'C:/Windows/Fonts/simhei.ttf'))
pdfmetrics.registerFont(TTFont('STKAITI', 'C:/Windows/Fonts/STKAITI.TTF'))

PRIMARY = HexColor('#1677FF')
DARK = HexColor('#262626')
BODY = HexColor('#595959')
GREEN = HexColor('#52C41A')
YELLOW = HexColor('#FAAD14')
RED = HexColor('#FF4D4F')
BORDER = HexColor('#D9D9D9')
LIGHT_BG = HexColor('#F5F5F5')
CARD_BG = HexColor('#FAFAFA')
GRAY = HexColor('#8C8C8C')

# Helper styles
cs = lambda t, c=PRIMARY: Paragraph(f'<font color="{c}"><b>{t}</b></font>',
    ParagraphStyle('CS_'+t[:4], fontName='SIMHEI', fontSize=9, leading=14, textColor=c))
bd = lambda t: Paragraph(t, ParagraphStyle('BD', fontName='MSYH', fontSize=10, leading=17, textColor=BODY, spaceAfter=5))

def hr():
    return HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceBefore=5, spaceAfter=5)

def make_table(headers, rows, col_widths=None, hc=PRIMARY):
    ths = ParagraphStyle('TH', fontName='SIMHEI', fontSize=9, leading=14, textColor=white)
    tds = ParagraphStyle('TD', fontName='MSYH', fontSize=9, leading=15, textColor=BODY)
    data = [[Paragraph(f'<b>{h}</b>', ths) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(c), tds) if not isinstance(c, Paragraph) else c for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), hc),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    return t

def bullet(text):
    return Paragraph(f'\u2022 {text}',
        ParagraphStyle('BL', fontName='MSYH', fontSize=10, leading=17, textColor=BODY, leftIndent=12, spaceAfter=3))

def h1(text):
    return Paragraph(text, ParagraphStyle('H1', fontName='MSYHBD', fontSize=18, leading=26, textColor=DARK, spaceBefore=22, spaceAfter=8))

def h2(text):
    return Paragraph(text, ParagraphStyle('H2', fontName='MSYHBD', fontSize=13, leading=20, textColor=DARK, spaceBefore=14, spaceAfter=6))

def center_text(text, fontName='MSYH', size=11, color=BODY):
    return Paragraph(text, ParagraphStyle('CT', fontName=fontName, fontSize=size, leading=int(size*1.5), textColor=color, alignment=TA_CENTER))

# === BUILD ===
output_path = r"D:\work\新城控股\新城开发skill\tmp\pdfs\seazenai-intro.pdf"
doc = SimpleDocTemplate(output_path, pagesize=A4,
    leftMargin=22*mm, rightMargin=22*mm, topMargin=18*mm, bottomMargin=18*mm)
S = []

# Cover
S.append(Spacer(1, 50*mm))
S.append(Paragraph('新城控股研发统筹智能体',
    ParagraphStyle('TT', fontName='MSYHBD', fontSize=26, leading=36, textColor=DARK, alignment=TA_CENTER)))
S.append(Paragraph('seazenai-orchestrator  v2.1.0',
    ParagraphStyle('ST', fontName='MSYH', fontSize=13, leading=20, textColor=GRAY, alignment=TA_CENTER, spaceAfter=10)))
S.append(hr())
S.append(center_text('基于 Prompt-as-Code 的 AI 研发协作系统', 'STKAITI', 13, GRAY))
S.append(Spacer(1, 10))
S.append(center_text('覆盖需求分析 \u00b7 开发编排 \u00b7 测试审查全流程'))
S.append(center_text('四阶段渐进式落地  \u00b7  八部分完整方案'))
S.append(PageBreak())

# 1
S.append(h1('一、角色定位'))
S.append(hr())
S.append(bd('我是公司级研发统筹系统的<b>安装和引导助手</b>。我只做三件事，<b>不参与具体的编码或测试</b>——那些由安装到项目中的智能体承担。'))
S.append(Spacer(1, 4))
S.append(make_table(['入口', '触发方式', '功能'],
    [[cs('init'), '"初始化研发统筹"', '收集项目信息，安装 .seazenai/ 智能体文件体系'],
     [cs('guide', GREEN), '"当前阶段该做什么"', '检测项目状态，输出下一步操作清单'],
     [cs('update', YELLOW), '"检查研发统筹更新"', '对比公司模板与项目文件，安全合并更新']],
    [55, 130, 275]))

# 2
S.append(h1('二、安装的文件体系（init 产物）'))
S.append(hr())
S.append(make_table(['文件 / 目录', '说明'],
    [[cs('.seazenai/knowledge/'), '系统知识库：数据模型、API目录、业务规则、数据流'],
     [cs('.seazenai/requirements/'), '需求对话智能体 + 需求文档（in-progress / archive）'],
     [cs('.seazenai/development/'), '开发编排智能体 + 任务拆解 + Review清单'],
     [cs('.seazenai/testing/'), '测试审查智能体 + 盲区清单 + 用例模板'],
     [cs('.seazenai/conventions/'), '编码规范（Java/.NET/Vue2/Vue3/样式设计）'],
     [cs('seazenai.md'), '入口路由文件，按角色分发到对应 Agent']],
    [150, 310]))

S.append(PageBreak())

# 3
S.append(h1('三、四阶段渐进式落地'))
S.append(hr())
S.append(make_table(['阶段', '名称', '周期', '核心内容'],
    [[cs('Phase 1'), '知识注入', '2-3 周', '10步知识提取：模块边界\u2192代码风格\u2192API目录\u2192数据流\u2192业务规则\u2192人工验证'],
     [cs('Phase 2', GREEN), '需求对话', '3-4 周', '冷启动3个训练需求\u2192追问规则(A/B/C三类)\u2192反向确认'],
     [cs('Phase 3', YELLOW), '开发编排', '6-8 周', 'CP0-CP5：任务初始化\u2192需求理解\u2192自主开发\u2192Review\u2192提交测试'],
     [cs('Phase 4', RED), '测试审查', '并行', '盲区清单驱动\u2192三层测试生成(L1/L2/L3)\u2192探索性测试']],
    [52, 56, 52, 300]))

# 4
S.append(h1('四、开发约束体系'))
S.append(hr())
S.append(h2('4.1 硬性安全边界'))
S.append(bullet('<b>自修复预算：</b>代码\u2192测试失败\u2192修复，最多 3 轮，超限强制终止'))
S.append(bullet('<b>Review 限制：</b>打回最多 2 次，超过由开发经理和 AI 同步修改'))
S.append(bullet('<b>决策点：</b>不确定时必须上报 CP2，给出 2-3 个方案，禁止自行决定'))
S.append(Spacer(1, 4))
S.append(make_table(['风险级别', '范围', '示例'],
    [[cs('\U0001f7e2 低风险', GREEN), '可直接做', '新增单表、新增API、新增Service方法、基础前端页面'],
     [cs('\U0001f7e1 中风险', YELLOW), '稳定后可做', '给已有接口加可选参数、Service新增方法不改签名'],
     [cs('\U0001f534 高风险', RED), '禁止，需人工', '改已有必填参数/返回结构、改表字段、跨模块、状态机改造']],
    [80, 80, 300]))

S.append(h2('4.2 六条行为红线'))
S.append(make_table(['红线', '说明'],
    [[cs('\U0001f534 存量代码保护（最高优先级）', RED),
      '新增开发，存量保留。旧代码不符合新规范也不得修改；禁顺手重构、统一风格、提取重复代码、批量格式化'],
     [cs('\U0001f534 严禁越权', RED), '不随手优化、不自加功能、不擅引第三方库'],
     [cs('\U0001f534 严禁猜测', RED), '需求含糊须提问，不确定须上报CP2'],
     [cs('\U0001f534 严禁安全违规', RED), '禁SQL拼接、禁日志打印密码/Token、禁URL传敏感数据'],
     [cs('\U0001f534 严禁破坏', RED), '不改迁移脚本、不删已有类/方法，破环操作用@Deprecated过渡'],
     [cs('\U0001f534 严禁假做', RED), '代码须完整实现、测试须覆盖异常流程、禁修改测试来通过']],
    [155, 305]))

S.append(PageBreak())

# 5
S.append(h1('五、编码规范（conventions/）'))
S.append(hr())
S.append(make_table(['文件', '覆盖内容'],
    [[cs('java-backend.md'), 'Spring Boot分层、MyBatis-Plus、RESTful、事务、异常、日志、安全'],
     [cs('net-backend.md'), 'ASP.NET Core分层、EF Core、依赖注入、异常、日志、安全'],
     [cs('vue-frontend.md'), 'Vue3 + Composition API + Pinia + TypeScript'],
     [cs('vue2-frontend.md'), 'Vue2 + Options API + Vuex + Element UI'],
     [cs('design-style.md'), '参考Ant Design 5.0 & TDesign：色彩/阴影/圆角/间距/布局/动效，PC与移动端双规格']],
    [115, 345]))

# 6
S.append(h1('六、命名规范'))
S.append(hr())
S.append(bd('需求/开发/测试文件夹统一命名格式：'))
S.append(Spacer(1, 4))
S.append(Paragraph('<b><font color="#1677FF" size="13">YYYY-MM-DD-简要描述</font></b>   （描述 \u2264 20 字）',
    ParagraphStyle('NM', fontName='STKAITI', fontSize=13, leading=22, textColor=DARK, alignment=TA_CENTER, spaceAfter=6)))
S.append(bd('示例：<font color="#595959">2026-05-29-用户登录</font>（日期取创建当天，描述由用户输入）'))
S.append(Spacer(1, 4))

# 7
S.append(h1('七、阶段无缝衔接流程'))
S.append(hr())
S.append(bd('需求方新建需求 \u2192 AI 追问分析 \u2192 生成需求文档 \u2192 需求方确认归档'))
S.append(bd('\u2192 自动询问"是否进入开发？" \u2192 开发Agent 接手 CP0\u2192CP5'))
S.append(bd('\u2192 开发完成自动询问"是否进入测试？" \u2192 测试Agent 接手 TP0\u2192CP4'))
S.append(Spacer(1, 8))
S.append(bd('整个过程在同一个 Git 仓库中完成，所有文件（需求文档、知识库、开发任务、测试用例）全部版本化。'))

# Footer
S.append(Spacer(1, 14*mm))
S.append(hr())
S.append(Paragraph('新城控股研发统筹智能体  \u00b7  seazenai-orchestrator v2.1.0  \u00b7  Prompt-as-Code',
    ParagraphStyle('FT', fontName='MSYH', fontSize=8, leading=12, textColor=GRAY, alignment=TA_CENTER)))

doc.build(S)
print(f'SUCCESS: {output_path}')
print(f'SIZE: {os.path.getsize(output_path)} bytes')
