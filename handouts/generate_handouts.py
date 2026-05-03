#!/usr/bin/env python3
"""Generate handout PDFs for 4-day AI & Cloud Accounting course."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

# Register Thai font
pdfmetrics.registerFont(TTFont('Thonburi', '/System/Library/Fonts/Supplemental/Thonburi.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('Thonburi-Bold', '/System/Library/Fonts/Supplemental/Thonburi.ttc', subfontIndex=1))

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


def draw_header(c, day):
    """Draw the header band with course info."""
    # Navy header band
    c.setFillColor(NAVY_DEEP)
    c.rect(0, H - 90, W, 90, fill=1, stroke=0)

    # Course title
    c.setFillColor(white)
    c.setFont('Thonburi-Bold', 13)
    c.drawString(25, H - 35, COURSE_TITLE_TH)
    c.setFont('Thonburi', 9)
    c.drawString(25, H - 52, COURSE_TITLE_EN)

    # Faculty line
    c.setFillColor(HexColor('#BBDEFB'))
    c.setFont('Thonburi', 8)
    c.drawString(25, H - 72, f"{FACULTY}  |  {INSTRUCTOR_TH}")

    # Day badge on right
    c.setFillColor(SKY)
    c.roundRect(W - 95, H - 78, 75, 60, 8, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Thonburi', 9)
    c.drawCentredString(W - 57, H - 35, "DAY")
    c.setFont('Thonburi-Bold', 30)
    c.drawCentredString(W - 57, H - 68, f"0{day['num']}")


def draw_day_title(c, day, y):
    """Draw the day title section."""
    # Module tag
    c.setFillColor(PURPLE)
    c.setFont('Thonburi', 10)
    c.drawString(25, y, day['module'])

    y -= 28
    # Thai title
    c.setFillColor(NAVY)
    c.setFont('Thonburi-Bold', 18)
    c.drawString(25, y, day['title_th'])

    y -= 22
    # English subtitle
    c.setFillColor(TEXT_MUTED)
    c.setFont('Thonburi', 11)
    c.drawString(25, y, day['title_en'])

    y -= 18
    # Date
    c.setFont('Thonburi', 10)
    c.drawString(25, y, f"{day['date_en']}  ·  {day['date_th']}")

    return y - 15


def draw_section_table(c, day, y):
    """Draw the sections table."""
    # Table header
    c.setFillColor(NAVY)
    c.roundRect(25, y - 24, W - 50, 26, 4, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Thonburi-Bold', 10)
    c.drawString(35, y - 18, "หัวข้อ / Section")
    c.drawString(200, y - 18, "รายละเอียด (TH)")
    c.drawString(420, y - 18, "Description (EN)")

    y -= 30
    row_h = 32

    for i, (sec, th_desc, en_desc) in enumerate(day['sections']):
        bg = LIGHT_BG if i % 2 == 0 else white
        c.setFillColor(bg)
        c.rect(25, y - row_h + 6, W - 50, row_h, fill=1, stroke=0)

        # Section number
        c.setFillColor(NAVY)
        c.setFont('Thonburi-Bold', 9)
        c.drawString(35, y - 8, sec)

        # Thai description
        c.setFillColor(black)
        c.setFont('Thonburi', 9)
        # Truncate if too long
        th_text = th_desc[:28] if len(th_desc) > 28 else th_desc
        c.drawString(200, y - 8, th_text)

        # English description
        c.setFillColor(TEXT_MUTED)
        c.setFont('Thonburi', 8)
        en_text = en_desc[:35] if len(en_desc) > 35 else en_desc
        c.drawString(420, y - 8, en_text)

        # Bottom border
        c.setStrokeColor(BORDER)
        c.setLineWidth(0.5)
        c.line(25, y - row_h + 6, W - 25, y - row_h + 6)

        y -= row_h

    return y - 10


def draw_keywords(c, day, y):
    """Draw keyword pills."""
    c.setFillColor(NAVY)
    c.setFont('Thonburi-Bold', 11)
    c.drawString(25, y, "คำสำคัญ · Keywords")
    y -= 22

    x = 25
    for kw in day['keywords']:
        tw = c.stringWidth(kw, 'Thonburi', 9) + 20
        # Pill background
        c.setFillColor(HexColor('#E8F2FC'))
        c.roundRect(x, y - 4, tw, 20, 10, fill=1, stroke=0)
        # Pill text
        c.setFillColor(NAVY)
        c.setFont('Thonburi', 9)
        c.drawString(x + 10, y + 2, kw)
        x += tw + 8
        if x > W - 80:
            x = 25
            y -= 28

    return y - 25


def draw_notes_section(c, y):
    """Draw notes lines for student to write on."""
    c.setFillColor(NAVY)
    c.setFont('Thonburi-Bold', 11)
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
    c.setFont('Thonburi', 7)
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
    print(f"  ✅ Created: {filename}")
    return filename


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = script_dir

    print("🔨 Generating handout PDFs...")
    for day in DAYS:
        create_handout(day, output_dir)
    print(f"\n✨ Done! 4 handout PDFs created in {output_dir}")
