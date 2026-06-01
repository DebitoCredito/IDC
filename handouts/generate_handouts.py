#!/usr/bin/env python3
"""Generate handout PDFs for 4-day AI & Cloud Accounting course."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
import os, sys, platform

# Register Thai font — cross-platform (Windows / macOS / Linux)
def _register_thai_font():
    candidates = [
        # Windows — THSarabunNew (preferred — official Thai font)
        ('C:/Windows/Fonts/THSarabunNew.ttf',      'C:/Windows/Fonts/THSarabunNew Bold.ttf'),
        ('C:/Windows/Fonts/THSarabun.ttf',         'C:/Windows/Fonts/THSarabun Bold.ttf'),
        # Windows — Leelawadee UI (fallback)
        ('C:/Windows/Fonts/leelawui.ttf',          'C:/Windows/Fonts/leelawdb.ttf'),
        ('C:/Windows/Fonts/leelawad.ttf',          'C:/Windows/Fonts/leelawdb.ttf'),
        # Windows — Tahoma (last resort)
        ('C:/Windows/Fonts/tahoma.ttf',            'C:/Windows/Fonts/tahomabd.ttf'),
    ]
    for regular, bold in candidates:
        if os.path.exists(regular) and os.path.exists(bold):
            pdfmetrics.registerFont(TTFont('ThaiBody',     regular))
            pdfmetrics.registerFont(TTFont('ThaiBody-Bold', bold))
            print(f"  [OK] Using font: {os.path.basename(regular)}")
            return
    # macOS Thonburi (legacy fallback)
    mac_thon = '/System/Library/Fonts/Supplemental/Thonburi.ttc'
    if os.path.exists(mac_thon):
        pdfmetrics.registerFont(TTFont('ThaiBody',      mac_thon, subfontIndex=0))
        pdfmetrics.registerFont(TTFont('ThaiBody-Bold', mac_thon, subfontIndex=1))
        return
    raise RuntimeError("ไม่พบฟอนต์ภาษาไทยในระบบ — กรุณาติดตั้ง THSarabunNew หรือ Leelawadee UI")

_register_thai_font()

# Brand colors
NAVY = HexColor('#003D7A')
NAVY_DEEP = HexColor('#002A55')
SKY = HexColor('#4A90E2')
PURPLE = HexColor('#7B4FBF')
LIGHT_BG = HexColor('#F5F8FC')
BORDER = HexColor('#D6E1EE')
TEXT_MUTED = HexColor('#5A6B85')

W, H = A4  # 595.28 x 841.89 points

COURSE_TITLE_TH = "การประยุกต์โปรแกรมบัญชีคลาวด์และเทคโนโลยีปัญญาประดิษฐ์เพื่องานบัญชี"
COURSE_TITLE_EN = "Applying Cloud Accounting Software and AI Technology for Accounting"
INSTRUCTOR = "Assoc. Prof. Dr. Uthen Laonamtha"
INSTRUCTOR_TH = "รศ.ดร.อุเทน เลานำทา"
FACULTY = "สาขาการบัญชี คณะบริหารธุรกิจและการบัญชี มหาวิทยาลัยขอนแก่น"

DAYS = [
    {
        "num": 1,
        "date_en": "12 September 2026",
        "date_th": "12 กันยายน 2569",
        "module": "Module 01 · Foundation",
        "title_th": "การพัฒนาระบบบัญชีดิจิทัลด้วย Cloud + AI",
        "title_en": "Foundation: AI-Era Accountant · Modern AIS · Cloud · RPA",
        "sections": [
            ("Section 1", "นักบัญชียุค AI — บทบาทที่เปลี่ยนไป", "AI-Era Accountant: The Changing Role"),
            ("Section 2", "ระบบสารสนเทศทางการบัญชีสมัยใหม่", "Modern Accounting Information Systems (AIS)"),
            ("Section 3", "ซอฟต์แวร์บัญชีคลาวด์ — Express Online", "Cloud Accounting Software — Express Online"),
            ("Section 4", "RPA & Automation สำหรับงานบัญชี", "RPA & Automation for Accounting"),
            ("Section 5", "PDPA & Cybersecurity สำหรับนักบัญชี", "PDPA & Cybersecurity for Accountants"),
        ],
        "keywords": ["AI-Era Accountant", "Modern AIS", "Cloud Software", "RPA & Automation", "PDPA & Cybersecurity"],
    },
    {
        "num": 2,
        "date_en": "13 September 2026",
        "date_th": "13 กันยายน 2569",
        "module": "Module 02 · Applied AI",
        "title_th": "การประยุกต์ใช้ปัญญาประดิษฐ์ในงานบัญชี",
        "title_en": "Applied AI: Landscape · RICIOV · Use Cases · Governance",
        "sections": [
            ("Section 1", "AI Landscape 2026 — ภูมิทัศน์ปัญญาประดิษฐ์", "AI Architectures & Landscape 2026"),
            ("Section 2", "RICIOV Prompt Engineering Framework", "Prompt Engineering with RICIOV Framework"),
            ("Section 3", "5 Use Cases: AI ในงานบัญชี", "5 Applied AI Use Cases for Accounting"),
            ("Section 4", "AI Governance & จริยธรรม", "AI Governance, Ethics & Responsible Use"),
        ],
        "keywords": ["AI Landscape 2026", "RICIOV Framework", "5 Use Cases", "NotebookLM", "AI Governance"],
    },
    {
        "num": 3,
        "date_en": "3 October 2026",
        "date_th": "3 ตุลาคม 2569",
        "module": "Module 03 · Reporting & Dashboard",
        "title_th": "วิเคราะห์ & ออกแบบรายงานบัญชีด้วย Dashboard",
        "title_en": "Reporting: Express Reports · Excel · CLEAR · Power BI",
        "sections": [
            ("Section 1", "Analytics Overview — ภาพรวมการวิเคราะห์", "Analytics Overview & Data-Driven Decisions"),
            ("Section 2", "Express Reports — รายงานจากระบบ", "Express Accounting Reports Deep Dive"),
            ("Section 3", "Excel Data Prep — Power Query & Pivot", "Excel Data Preparation with Power Query"),
            ("Section 4", "Dashboard Design — CLEAR Framework", "Dashboard Design with CLEAR Framework"),
            ("Section 5", "Dashboard Workshop — ลงมือสร้าง", "Hands-on Dashboard Workshop"),
            ("Section 6", "Future Reporting — AI + BI", "Future of Reporting: AI & Business Intelligence"),
        ],
        "keywords": ["Express Reports", "Power Query", "Pivot · SUMIFS", "CLEAR Framework", "Power BI"],
    },
    {
        "num": 4,
        "date_en": "4 October 2026",
        "date_th": "4 ตุลาคม 2569",
        "module": "Module 04 · Capstone Integration",
        "title_th": "Capstone: บูรณาการระบบบัญชีดิจิทัลครบวงจร",
        "title_en": "Capstone: Blueprint · AI Workflow · Mgmt Report · Presentation",
        "sections": [
            ("Section 1", "Integration Review — ทบทวนบูรณาการ", "Integration Review: Days 1–3 Recap"),
            ("Section 2", "System Design — พิมพ์เขียวระบบ", "System Blueprint Design"),
            ("Section 3", "AI Workflow — ออกแบบกระบวนการ AI", "AI Workflow Design for Accounting"),
            ("Section 4", "Dashboard & Report — รายงานผู้บริหาร", "Management Dashboard & Report"),
            ("Section 5", "Capstone Presentation — นำเสนอผลงาน", "Capstone Project Presentation"),
            ("Section 6", "Future-Ready Accountant — นักบัญชีแห่งอนาคต", "Future-Ready Digital Accountant"),
        ],
        "keywords": ["System Blueprint", "AI Workflow", "5-Section Report", "Capstone Project", "30/60/90 Roadmap"],
    },
]


def _fit_text(c, text, font, max_width, start_size, min_size=8):
    """Shrink font size until text fits within max_width."""
    size = start_size
    while size > min_size and c.stringWidth(text, font, size) > max_width:
        size -= 0.5
    return size


def draw_header(c, day):
    """Draw the header band with course info — auto-fit titles to avoid clipping."""
    # Navy header band
    c.setFillColor(NAVY_DEEP)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)

    # Day badge on the right (defines title width budget)
    badge_w, badge_h = 80, 64
    badge_x = W - 25 - badge_w
    badge_y = H - 78
    c.setFillColor(SKY)
    c.roundRect(badge_x, badge_y, badge_w, badge_h, 8, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('ThaiBody', 10)
    c.drawCentredString(badge_x + badge_w / 2, H - 32, "DAY")
    c.setFont('ThaiBody-Bold', 30)
    c.drawCentredString(badge_x + badge_w / 2, H - 65, f"0{day['num']}")

    # Title width budget = from x=25 to badge - 15 padding
    title_max_w = badge_x - 25 - 15

    # Course title (auto-fit)
    c.setFillColor(white)
    th_size = _fit_text(c, COURSE_TITLE_TH, 'ThaiBody-Bold', title_max_w, start_size=15, min_size=10)
    c.setFont('ThaiBody-Bold', th_size)
    c.drawString(25, H - 32, COURSE_TITLE_TH)

    en_size = _fit_text(c, COURSE_TITLE_EN, 'ThaiBody', title_max_w, start_size=11, min_size=8)
    c.setFont('ThaiBody', en_size)
    c.drawString(25, H - 50, COURSE_TITLE_EN)

    # Faculty line
    c.setFillColor(HexColor('#BBDEFB'))
    fac_text = f"{FACULTY}  |  {INSTRUCTOR_TH}"
    fac_size = _fit_text(c, fac_text, 'ThaiBody', title_max_w, start_size=10, min_size=7)
    c.setFont('ThaiBody', fac_size)
    c.drawString(25, H - 70, fac_text)


def draw_day_title(c, day, y):
    """Draw the day title section."""
    # Module tag
    c.setFillColor(PURPLE)
    c.setFont('ThaiBody', 10)
    c.drawString(25, y, day['module'])

    y -= 28
    # Thai title
    c.setFillColor(NAVY)
    c.setFont('ThaiBody-Bold', 18)
    c.drawString(25, y, day['title_th'])

    y -= 22
    # English subtitle
    c.setFillColor(TEXT_MUTED)
    c.setFont('ThaiBody', 11)
    c.drawString(25, y, day['title_en'])

    y -= 18
    # Date
    c.setFont('ThaiBody', 10)
    c.drawString(25, y, f"{day['date_en']}  ·  {day['date_th']}")

    return y - 15


def draw_section_table(c, day, y):
    """Draw the sections table — text auto-wraps to fit columns."""
    # Column geometry (left edges + widths in points)
    COL_SEC_X,  COL_SEC_W  = 35,  150        # Section label
    COL_TH_X,   COL_TH_W   = 195, 215        # Thai description
    COL_EN_X,   COL_EN_W   = 415, W - 25 - 415   # English description
    PAD_TOP    = 8                            # padding inside row
    PAD_BOT    = 8

    # Header band
    c.setFillColor(NAVY)
    c.roundRect(25, y - 24, W - 50, 26, 4, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('ThaiBody-Bold', 12)
    c.drawString(COL_SEC_X, y - 17, "หัวข้อ / Section")
    c.drawString(COL_TH_X,  y - 17, "รายละเอียด (TH)")
    c.drawString(COL_EN_X,  y - 17, "Description (EN)")

    y -= 32

    # Paragraph styles (auto-wrap)
    style_th = ParagraphStyle('th', fontName='ThaiBody', fontSize=12, leading=15, textColor=black)
    style_en = ParagraphStyle('en', fontName='ThaiBody', fontSize=10, leading=13, textColor=TEXT_MUTED)
    style_sec = ParagraphStyle('sec', fontName='ThaiBody-Bold', fontSize=11, leading=14, textColor=NAVY)

    for i, (sec, th_desc, en_desc) in enumerate(day['sections']):
        # Build paragraphs and measure required height per cell
        p_sec = Paragraph(sec, style_sec)
        p_th  = Paragraph(th_desc, style_th)
        p_en  = Paragraph(en_desc, style_en)

        h_sec = p_sec.wrap(COL_SEC_W, 200)[1]
        h_th  = p_th.wrap(COL_TH_W,  200)[1]
        h_en  = p_en.wrap(COL_EN_W,  200)[1]
        row_h = max(h_sec, h_th, h_en) + PAD_TOP + PAD_BOT

        # Row background
        bg = LIGHT_BG if i % 2 == 0 else white
        c.setFillColor(bg)
        c.rect(25, y - row_h, W - 50, row_h, fill=1, stroke=0)

        # Render cells (top of each Paragraph is row_top - PAD_TOP)
        top = y - PAD_TOP
        p_sec.drawOn(c, COL_SEC_X, top - h_sec)
        p_th .drawOn(c, COL_TH_X,  top - h_th)
        p_en .drawOn(c, COL_EN_X,  top - h_en)

        # Bottom border
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.5)
        c.line(25, y - row_h, W - 25, y - row_h)

        y -= row_h

    return y - 10


def draw_keywords(c, day, y):
    """Draw keyword pills."""
    c.setFillColor(NAVY)
    c.setFont('ThaiBody-Bold', 11)
    c.drawString(25, y, "คำสำคัญ · Keywords")
    y -= 22

    x = 25
    for kw in day['keywords']:
        tw = c.stringWidth(kw, 'ThaiBody', 9) + 20
        # Pill background
        c.setFillColor(HexColor('#E8F2FC'))
        c.roundRect(x, y - 4, tw, 20, 10, fill=1, stroke=0)
        # Pill text
        c.setFillColor(NAVY)
        c.setFont('ThaiBody', 9)
        c.drawString(x + 10, y + 2, kw)
        x += tw + 8
        if x > W - 80:
            x = 25
            y -= 28

    return y - 25


def draw_notes_section(c, y):
    """Draw notes lines for student to write on."""
    c.setFillColor(NAVY)
    c.setFont('ThaiBody-Bold', 11)
    c.drawString(25, y, "บันทึก · Notes")
    y -= 20

    c.setStrokeColor(BORDER)
    c.setLineWidth(0.4)
    line_spacing = 24
    while y > 80:
        c.line(25, y, W - 25, y)
        y -= line_spacing

    return y


def draw_footer(c, day):
    """Draw footer."""
    c.setFillColor(BORDER)
    c.line(25, 55, W - 25, 55)
    c.setFillColor(TEXT_MUTED)
    c.setFont('ThaiBody', 7)
    c.drawString(25, 40, f"Handout · Day {day['num']:02d} · {COURSE_TITLE_EN}")
    c.drawRightString(W - 25, 40, f"© 2026 · {FACULTY}")


def create_handout(day, output_dir):
    """Create a handout PDF for one day."""
    filename = os.path.join(output_dir, f"day{day['num']}-handout.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    c.setTitle(f"Day {day['num']} Handout - {day['title_en']}")
    c.setAuthor(INSTRUCTOR)
    c.setSubject(COURSE_TITLE_EN)

    # === PAGE 1: Cover + Sections ===
    draw_header(c, day)
    y = H - 115
    y = draw_day_title(c, day, y)
    y -= 10
    y = draw_section_table(c, day, y)
    y -= 5
    y = draw_keywords(c, day, y)
    draw_footer(c, day)

    # === PAGE 2: Notes ===
    c.showPage()
    draw_header(c, day)
    y = H - 115
    y = draw_notes_section(c, y)
    draw_footer(c, day)

    c.save()
    print(f"  [OK] Created: {filename}")
    return filename


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = script_dir

    print("Generating handout PDFs...")
    for day in DAYS:
        create_handout(day, output_dir)
    print(f"\nDone! 4 handout PDFs created in {output_dir}")
