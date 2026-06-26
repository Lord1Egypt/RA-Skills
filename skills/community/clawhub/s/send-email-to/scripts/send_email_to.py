# -*- coding: utf-8 -*-
"""发送金融市场日报邮件"""
import sys
sys.path.insert(0, r"C:\Users\qu669\.openclaw\workspace-yoyo")
sys.stdout.reconfigure(encoding='utf-8')
import os, json, datetime, smtplib, logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import encode_rfc2231
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(config.LOG_FILE, encoding="utf-8"), logging.StreamHandler(sys.stdout)])
log = logging.getLogger(__name__)

log.info(f"📧 发送邮件... 日期: {config.REPORT_DATE}  收件人: {config.RECIPIENT_EMAIL}")

data = {}
if os.path.exists(config.MARKET_DATA_FILE):
    with open(config.MARKET_DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

def gp(k): d=data.get(k,{}); return d.get('price',0) if isinstance(d,dict) else 0
def gc(k): d=data.get(k,{}); return d.get('change',0) if isinstance(d,dict) else 0
def fp(v): return "N/A" if v==0 else (f"{v:,.0f}" if abs(v)>=10000 else f"{v:,.2f}" if abs(v)>=100 else f"{v:,.4f}")
def fpc(v): return "N/A" if v==0 else f"{'+' if v>0 else ''}{v:.2f}%"

dji=(gp('道琼斯工业平均指数'),gc('道琼斯工业平均指数'))
spx=(gp('标普500指数'),gc('标普500指数'))
nasdaq=(gp('纳斯达克综合指数'),gc('纳斯达克综合指数'))
sh=(gp('上证指数'),gc('上证指数'))
sz=(gp('深证成指'),gc('深证成指'))
cy=(gp('创业板指'),gc('创业板指'))
hsi=(gp('恒生指数'),gc('恒生指数'))
gold=(gp('黄金期货'),gc('黄金期货'))
oil=(gp('原油期货'),gc('原油期货'))
usdcny=gp('USD/CNY'); eurusd=gp('EUR/USD')

today_str = config.TODAY.strftime("%Y%m%d")
all_files = os.listdir(config.OUTPUT_DIR) if os.path.exists(config.OUTPUT_DIR) else []
word_files = [f for f in all_files if f.endswith(f'_{today_str}.docx')]
ppt_files = [f for f in all_files if f.endswith(f'_{today_str}.pptx')]

body = f"""您好！

{config.REPORT_DATE}金融市场日报已生成，数据截至{config.DATA_DATE}。

■ 主要市场表现：

【美国股市】
- 道琼斯工业平均指数：{fp(dji[0])}点，{fpc(dji[1])}
- 标普500指数：{fp(spx[0])}点，{fpc(spx[1])}
- 纳斯达克综合指数：{fp(nasdaq[0])}点，{fpc(nasdaq[1])}

【A股】
- 上证指数：{fp(sh[0])}点，{fpc(sh[1])}
- 深证成指：{fp(sz[0])}点，{fpc(sz[1])}
- 创业板指：{fp(cy[0])}点，{fpc(cy[1])}

【港股】
- 恒生指数：{fp(hsi[0])}点，{fpc(hsi[1])}

【外汇】
- USD/CNY：{fp(usdcny)}
- EUR/USD：{fp(eurusd)}

【大宗商品】
- 黄金期货：约${fp(gold[0])}/盎司，{fpc(gold[1])}
- 原油期货：约${fp(oil[0])}/桶，{fpc(oil[1])}

■ 备注：
- 详细晨会内容请查看附件 Word 文档及 PPT 简报

---
本报告由自动系统生成，数据仅供参考，不构成投资建议。
"""

msg = MIMEMultipart()
msg['From'] = config.SENDER_EMAIL
msg['To'] = config.RECIPIENT_EMAIL
msg['Subject'] = f"【每日金融晨报】{config.REPORT_DATE} - 数据截至{config.DATA_DATE}"
msg.attach(MIMEText(body, 'plain', 'utf-8'))

for fname in word_files + ppt_files:
    fpath = os.path.join(config.OUTPUT_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename*={encode_rfc2231(fname, "utf-8")}')
        if fname.endswith('.docx'):
            part.replace_header('Content-Type', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        elif fname.endswith('.pptx'):
            part.replace_header('Content-Type', 'application/vnd.openxmlformats-officedocument.presentationml.presentation')
        msg.attach(part)
        log.info(f"  📎 附件: {fname} ({os.path.getsize(fpath):,} bytes)")

try:
    server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
    server.starttls()
    server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
    server.sendmail(config.SENDER_EMAIL, config.RECIPIENT_EMAIL, msg.as_string())
    server.quit()
    log.info(f"\n✅ 邮件发送成功！")
except Exception as e:
    log.error(f"\n❌ 邮件发送失败: {e}")