# app.py

import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="API RP 574 Piping Calculator", layout="wide")

st.title("🔧 Piping Inspection & Calculation Tool - API RP 574")
st.caption("Developed by: **Mohamed Ahmed Abedalla Mohamed** 🇪🇬 | Piping Integrity Specialist")

# --- 1. PIPING DIMENSIONS DATABASE (API RP 574 / ASME B36.10) ---
pipe_database = {
    'NPS 1/2" (OD: 0.840")': {'OD': 0.840, 'Schedules': {'Sch 5S': 0.083, 'Sch 10S': 0.083, 'Sch 40 / STD': 0.109, 'Sch 80 / XS': 0.147, 'Sch 160': 0.187, 'XXS': 0.294}},
    'NPS 3/4" (OD: 1.050")': {'OD': 1.050, 'Schedules': {'Sch 5S': 0.083, 'Sch 10S': 0.083, 'Sch 40 / STD': 0.113, 'Sch 80 / XS': 0.154, 'Sch 160': 0.219, 'XXS': 0.308}},
    'NPS 1" (OD: 1.315")': {'OD': 1.315, 'Schedules': {'Sch 5S': 0.065, 'Sch 10S': 0.109, 'Sch 40 / STD': 0.133, 'Sch 80 / XS': 0.179, 'Sch 160': 0.250, 'XXS': 0.358}},
    'NPS 1.25" (OD: 1.660")': {'OD': 1.660, 'Schedules': {'Sch 5S': 0.065, 'Sch 10S': 0.109, 'Sch 40 / STD': 0.140, 'Sch 80 / XS': 0.191, 'Sch 160': 0.250, 'XXS': 0.382}},
    'NPS 1.5" (OD: 1.900")': {'OD': 1.900, 'Schedules': {'Sch 5S': 0.065, 'Sch 10S': 0.109, 'Sch 40 / STD': 0.145, 'Sch 80 / XS': 0.200, 'Sch 160': 0.281, 'XXS': 0.400}},
    'NPS 2" (OD: 2.375")': {'OD': 2.375, 'Schedules': {'Sch 5S': 0.065, 'Sch 10S': 0.109, 'Sch 40 / STD': 0.154, 'Sch 80 / XS': 0.218, 'Sch 160': 0.344, 'XXS': 0.436}},
    'NPS 2.5" (OD: 2.875")': {'OD': 2.875, 'Schedules': {'Sch 5S': 0.083, 'Sch 10S': 0.120, 'Sch 40 / STD': 0.203, 'Sch 80 / XS': 0.276, 'Sch 160': 0.375, 'XXS': 0.552}},
    'NPS 3" (OD: 3.500")': {'OD': 3.500, 'Schedules': {'Sch 5S': 0.083, 'Sch 10S': 0.120, 'Sch 40 / STD': 0.216, 'Sch 80 / XS': 0.300, 'Sch 160': 0.438, 'XXS': 0.600}},
    'NPS 3.5" (OD: 4.000")': {'OD': 4.000, 'Schedules': {'Sch 5S': 0.083, 'Sch 10S': 0.120, 'Sch 40 / STD': 0.226, 'Sch 80 / XS': 0.318, 'Sch 160': 0.469, 'XXS': 0.636}},
    'NPS 4" (OD: 4.500")': {'OD': 4.500, 'Schedules': {'Sch 5S': 0.083, 'Sch 10S': 0.120, 'Sch 40 / STD': 0.237, 'Sch 80 / XS': 0.337, 'Sch 160': 0.531, 'XXS': 0.674}},
    'NPS 5" (OD: 5.563")': {'OD': 5.563, 'Schedules': {'Sch 5S': 0.109, 'Sch 10S': 0.134, 'Sch 40 / STD': 0.258, 'Sch 80 / XS': 0.375, 'Sch 160': 0.625, 'XXS': 0.750}},
    'NPS 6" (OD: 6.625")': {'OD': 6.625, 'Schedules': {'Sch 5S': 0.109, 'Sch 10S': 0.134, 'Sch 40 / STD': 0.280, 'Sch 80 / XS': 0.432, 'Sch 120': 0.562, 'Sch 160': 0.718, 'XXS': 0.864}},
    'NPS 8" (OD: 8.625")': {'OD': 8.625, 'Schedules': {'Sch 5S': 0.109, 'Sch 10S': 0.148, 'Sch 40 / STD': 0.322, 'Sch 80 / XS': 0.500, 'Sch 120': 0.718, 'Sch 160': 0.906, 'XXS': 0.875}},
    'NPS 10" (OD: 10.750")': {'OD': 10.750, 'Schedules': {'Sch 5S': 0.134, 'Sch 10S': 0.165, 'Sch 40 / STD': 0.365, 'Sch 80 / XS': 0.593, 'Sch 120': 0.844, 'Sch 160': 1.000, 'XXS': 1.000}},
    'NPS 12" (OD: 12.750")': {'OD': 12.750, 'Schedules': {'Sch 5S': 0.156, 'Sch 10S': 0.180, 'Sch 40 / STD': 0.406, 'Sch 80 / XS': 0.687, 'Sch 120': 1.000, 'Sch 160': 1.125, 'XXS': 1.000}}
}

# --- 1.2 API RP 574 TABLE 5 (MINIMUM STRUCTURAL THICKNESS) ---
def get_structural_thickness(nps_str):
    if "1/2" in nps_str or "3/4" in nps_str or "1\"" in nps_str:
        return 0.07
    elif "1.25" in nps_str or "1.5" in nps_str or "2\"" in nps_str:
        return 0.07
    elif "3\"" in nps_str:
        return 0.08
    elif "3.5" in nps_str or "4\"" in nps_str:
        return 0.09
    elif "5\"" in nps_str or "6\"" in nps_str or "8\"" in nps_str or "10\"" in nps_str or "12\"" in nps_str:
        return 0.11
    else:
        return 0.07

# --- 2. COMPREHENSIVE MATERIAL STRESS DATA ---
grade_stress_map = {
    "ASTM A106 Grade A": 16000.0,
    "ASTM A106 Grade B": 20000.0,
    "ASTM A106 Grade C": 23300.0,
    "ASTM A53 Grade A (Seamless)": 16000.0,
    "ASTM A53 Grade B (Seamless)": 20000.0,
    "ASTM A53 Grade A (ERW/EFW)": 13600.0,
    "ASTM A53 Grade B (ERW/EFW)": 17000.0,
    "ASTM A53 Type F (Furnace Butt-Welded)": 11000.0,
    "ASTM A134 (Steel Plate Pipe)": 12000.0,
    "ASTM A135 Grade A": 13600.0,
    "ASTM A135 Grade B": 17000.0,
    "ASTM A139 Grade A": 13600.0,
    "ASTM A139 Grade B": 16000.0,
    "ASTM A333 Grade 1 (Low Temp)": 20000.0,
    "ASTM A333 Grade 3 (Low Temp)": 20000.0,
    "ASTM A333 Grade 4 (Low Temp)": 20000.0,
    "ASTM A333 Grade 6 (Low Temp)": 20000.0,
    "ASTM A333 Grade 7 (Low Temp)": 20000.0,
    "ASTM A333 Grade 8 (Low Temp)": 33300.0,
    "ASTM A333 Grade 9 (Low Temp)": 21000.0,
    "ASTM A671 Grade CC60": 17500.0,
    "ASTM A671 Grade CC65": 19200.0,
    "ASTM A671 Grade CC70": 21700.0,
    "ASTM A672 Grade C60": 17500.0,
    "ASTM A672 Grade C65": 19200.0,
    "ASTM A672 Grade C70": 21700.0,
    "API 5L Grade A25": 14700.0,
    "API 5L Grade A": 16000.0,
    "API 5L Grade B": 20000.0,
    "API 5L X42": 21000.0,
    "API 5L X46": 23000.0,
    "API 5L X52": 26000.0,
    "API 5L X56": 28000.0,
    "API 5L X60": 30000.0,
    "API 5L X65": 32500.0,
    "API 5L X70": 35000.0,
    "API 5L X80": 40000.0,
    "ASTM A312 TP304 (Seamless)": 20000.0,
    "ASTM A312 TP304L (Seamless)": 16700.0,
    "ASTM A312 TP304H (Seamless)": 20000.0,
    "ASTM A312 TP316 (Seamless)": 20000.0,
    "ASTM A312 TP316L (Seamless)": 16700.0,
    "ASTM A312 TP316H (Seamless)": 20000.0,
    "ASTM A312 TP309S": 20000.0,
    "ASTM A312 TP310S": 15000.0,
    "ASTM A312 TP317": 20000.0,
    "ASTM A312 TP317L": 16700.0,
    "ASTM A312 TP321": 20000.0,
    "ASTM A312 TP321H": 20000.0,
    "ASTM A312 TP347": 20000.0,
    "ASTM A312 TP347H": 20000.0,
    "ASTM A312 TP348": 20000.0,
    "ASTM A312 TP904L": 22000.0,
    "ASTM A790 UNS S31803 (Duplex 2205)": 25700.0,
    "ASTM A790 UNS S32750 (Super Duplex 2507)": 28700.0,
    "ASTM A335 P1 (0.5% Mo)": 15000.0,
    "ASTM A335 P2 (0.5% Cr, 0.5% Mo)": 15000.0,
    "ASTM A335 P5 (5% Cr, 0.5% Mo)": 20000.0,
    "ASTM A335 P5b": 20000.0,
    "ASTM A335 P5c": 20000.0,
    "ASTM A335 P9 (9% Cr, 1% Mo)": 20000.0,
    "ASTM A335 P11 (1.25% Cr, 0.5% Mo)": 20000.0,
    "ASTM A335 P12 (1% Cr, 0.5% Mo)": 18900.0,
    "ASTM A335 P21 (3% Cr, 1% Mo)": 20000.0,
    "ASTM A335 P22 (2.25% Cr, 1% Mo)": 20000.0,
    "ASTM A335 P91 (9% Cr, 1% Mo, V)": 25000.0,
    "ASTM A335 P92": 25000.0,
    "ASTM B161 Nickel 200": 10000.0,
    "ASTM B161 Nickel 201": 8000.0,
    "ASTM B165 Monel 400": 17500.0,
    "ASTM B407 Incoloy 800": 18700.0,
    "ASTM B407 Incoloy 800H": 16300.0,
    "ASTM B444 Inconel 625 (Grade 1)": 30000.0,
    "ASTM B444 Inconel 625 (Grade 2)": 25000.0,
    "ASTM B167 Inconel 600": 20000.0,
    "ASTM B622 Hastelloy C-276": 25000.0,
    "ASTM B622 Hastelloy C-22": 25000.0,
    "ASTM B622 Hastelloy B-2": 27500.0,
    "ASTM B423 Incoloy 825": 23300.0,
    "ASTM B315 Copper-Nickel 90-10": 10000.0,
    "ASTM B315 Copper-Nickel 70-30": 15000.0,
    "SA-516 Grade 55": 13800.0,
    "SA-516 Grade 55 (Normalized)": 13800.0,
    "SA-516 Grade 60": 15000.0,
    "SA-516 Grade 60 (Normalized)": 15000.0,
    "SA-516 Grade 65": 17500.0,
    "SA-516 Grade 65 (Normalized)": 17500.0,
    "SA-516 Grade 70": 20000.0,
    "SA-516 Grade 70 (Normalized / 70N)": 20000.0,
    "SA-105": 20000.0,
    "SA-105N (Normalized)": 20000.0,
    "Chinese Steel 20# (Carbon Steel)": 20000.0,
    "Chinese Steel 20G (Boiler/Pressure Pipe)": 20000.0
}

# --- SIDEBAR INPUTS ---
st.sidebar.header("🛠️ **Inspector Profile**")
st.sidebar.info(f"**Inspector:** Mohamed Ahmed Abedalla Mohamed\n🇪🇬 Egypt\nPiping Integrity Specialist")
st.sidebar.markdown("---")

st.sidebar.header("📦 **Pipe Selection & Dimensions**")
selected_nps = st.sidebar.selectbox("Nominal Pipe Size (NPS)", list(pipe_database.keys()))
pipe_info = pipe_database[selected_nps]
default_od = pipe_info['OD']

selected_schedule = st.sidebar.selectbox("Schedule (Sch)", list(pipe_info['Schedules'].keys()))
nominal_thickness = pipe_info['Schedules'][selected_schedule]
t_structural = get_structural_thickness(selected_nps)

od = st.sidebar.number_input("Actual Measured Outside Diameter (D) [Inches]", value=default_od)

st.sidebar.markdown("---")
st.sidebar.header("📋 **Material & Design Parameters**")
selected_grade = st.sidebar.selectbox("Material Grade", list(grade_stress_map.keys()))
S = grade_stress_map[selected_grade]
st.sidebar.markdown(f"**Allowable Stress (S) [PSI]:** `{S}`")

P = st.sidebar.number_input("Internal Pressure (P) [PSI]", value=150.0)
E = st.sidebar.number_input("Joint Efficiency (E)", value=1.0)

st.sidebar.markdown("---")
st.sidebar.header("⏱️ **Thickness & Corrosion Inputs**")
t_actual = st.sidebar.number_input("Actual Thickness (t_actual) [Inches]", value=0.109)
t_previous = st.sidebar.number_input("Previous Thickness (t_prev) [Inches]", value=0.149)
years = st.sidebar.number_input("Time Interval Between Readings (Years)", value=5.0)

st.sidebar.markdown("---")
run_calc = st.sidebar.button("🚀 Run Calculation", type="primary", use_container_width=True)

# --- CALCULATIONS (BARLOW FORMULA: t = PD / 2SE) ---
denominator = 2 * S * E
t_pressure = (P * od) / denominator if denominator > 0 else 0.0
t_min = max(t_pressure, t_structural)

inside_diameter = od - (2 * t_actual)
corrosion_rate = (t_previous - t_actual) / years if years > 0 else 0.0
remaining_life = (t_actual - t_min) / corrosion_rate if corrosion_rate > 0 else 0.0

is_acceptable = t_actual >= t_min

# --- MAIN DISPLAY (UI) WITH SMALL TEXT & NO TRUNCATION ---
st.markdown("### 📊 **Selected Pipe Specification Summary**")
col_spec1, col_spec2, col_spec3, col_spec4 = st.columns(4)
with col_spec1:
    st.markdown(f"<small><b>Measured OD</b></small><br>`{od:.3f} in`", unsafe_allow_html=True)
with col_spec2:
    st.markdown(f"<small><b>Nominal Thickness</b></small><br>`{nominal_thickness:.3f} in`", unsafe_allow_html=True)
with col_spec3:
    st.markdown(f"<small><b>Inside Diameter (ID)</b></small><br>`{inside_diameter:.3f} in`", unsafe_allow_html=True)
with col_spec4:
    st.markdown(f"<small><b>Material Grade</b></small><br>`{selected_grade}`", unsafe_allow_html=True)

st.markdown("---")

st.markdown("### 🔍 **Thickness & Life Evaluation Results**")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown(f"<small><b>Pressure Design (t_p)</b></small><br>`{t_pressure:.4f} in`", unsafe_allow_html=True)
with col2:
    st.markdown(f"<small><b>Structural Min (t_str)</b></small><br>`{t_structural:.4f} in`", unsafe_allow_html=True)
with col3:
    st.markdown(f"<small><b>Governing t_min</b></small><br>`{t_min:.4f} in`", unsafe_allow_html=True)
with col4:
    st.markdown(f"<small><b>Corrosion Rate</b></small><br>`{corrosion_rate:.4f} in/yr`", unsafe_allow_html=True)
with col5:
    st.markdown(f"<small><b>Remaining Life</b></small><br>`{remaining_life:.1f} Years`", unsafe_allow_html=True)

st.markdown("")
if is_acceptable:
    st.success("✅ **Current thickness is ACCEPTABLE**")
else:
    st.error("❌ **Current thickness is UNACCEPTABLE (Below minimum required)**")

st.markdown("---")

# --- HIGH-END PROFESSIONAL PDF REPORT GENERATION ---
def generate_pdf_report(D, nom_thick, act_thick, t_final, corr_rate, rem_life, grade, t_str, t_pr, acceptable):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=15,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=4,
        alignment=1,
        fontName='Helvetica-Bold'
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontSize=8.5,
        textColor=colors.HexColor('#4B5563'),
        spaceAfter=15,
        alignment=1,
        fontName='Helvetica'
    )
    section_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontSize=10.5,
        textColor=colors.HexColor('#111827'),
        spaceBefore=10,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )

    elements.append(Paragraph("API RP 574 PIPING INSPECTION REPORT", title_style))
    elements.append(Paragraph("Inspector: Mohamed Ahmed Abedalla Mohamed &nbsp;|&nbsp; Specialization: Piping Integrity Specialist &nbsp;|&nbsp; Standard: API RP 574", subtitle_style))
    elements.append(Spacer(1, 5))

    # Section 1: Pipe Specification Table
    elements.append(Paragraph("1. Pipe & Material Specification Summary", section_heading))
    spec_data = [
        [Paragraph("<b>Material Grade</b>", styles['Normal']), Paragraph(str(grade), styles['Normal'])],
        [Paragraph("<b>Outside Diameter (OD)</b>", styles['Normal']), Paragraph(f"{D:.3f} inches", styles['Normal'])],
        [Paragraph("<b>Nominal Thickness</b>", styles['Normal']), Paragraph(f"{nom_thick:.3f} inches", styles['Normal'])],
        [Paragraph("<b>Actual Measured Thickness</b>", styles['Normal']), Paragraph(f"{act_thick:.3f} inches", styles['Normal'])],
    ]
    t1 = Table(spec_data, colWidths=[200, 340])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F9FAFB')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 8))

    # Section 2: Evaluation Results Table
    elements.append(Paragraph("2. Thickness Evaluation & Remaining Life Analysis", section_heading))
    eval_data = [
        [Paragraph("<b>Pressure Design Thickness (t_p)</b>", styles['Normal']), Paragraph(f"{t_pr:.4f} in", styles['Normal'])],
        [Paragraph("<b>Structural Minimum Thickness (Table 5)</b>", styles['Normal']), Paragraph(f"{t_str:.4f} in", styles['Normal'])],
        [Paragraph("<b>Governing Minimum Required Thickness (t_min)</b>", styles['Normal']), Paragraph(f"<b>{t_final:.4f} in</b>", styles['Normal'])],
        [Paragraph("<b>Corrosion Rate</b>", styles['Normal']), Paragraph(f"{corr_rate:.4f} in/year", styles['Normal'])],
        [Paragraph("<b>Remaining Life</b>", styles['Normal']), Paragraph(f"<b>{rem_life:.1f} Years</b>", styles['Normal'])],
    ]
    t2 = Table(eval_data, colWidths=[200, 340])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F9FAFB')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 10))

    # Section 3: Status Box
    status_text = "CURRENT THICKNESS IS ACCEPTABLE (FIT FOR SERVICE)" if acceptable else "CURRENT THICKNESS IS UNACCEPTABLE (BELOW MINIMUM REQUIRED)"
    status_color = colors.HexColor('#15803D') if acceptable else colors.HexColor('#B91C1C')
    bg_color = colors.HexColor('#DCFCE7') if acceptable else colors.HexColor('#FEE2E2')
    
    status_data = [[Paragraph(f"<font color='{status_color.hexval()}'><b>STATUS: {status_text}</b></font>", ParagraphStyle('StatusStyle', parent=styles['Normal'], alignment=1, fontSize=9.5))]]
    t3 = Table(status_data, colWidths=[540])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 0.5, status_color),
        ('PADDING', (0,0), (-1,-1), 7),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(t3)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

if st.button("📥 **Download PDF Inspection Report**"):
    pdf_buffer = generate_pdf_report(od, nominal_thickness, t_actual, t_min, corrosion_rate, remaining_life, selected_grade, t_structural, t_pressure, is_acceptable)
    st.download_button(
        label="📄 Click Here to Save PDF Report",
        data=pdf_buffer,
        file_name="API_574_Inspection_Report.pdf",
        mime="application/pdf"
    )