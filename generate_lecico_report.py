"""
generate_lecico_report.py
شغّله في نفس مجلد الـ charts (C:/LCSW/ أو نفس مجلد الـ notebook)
بيعمل ملف lecico_report.html جاهز للطباعة كـ PDF
"""

import base64, os, sys
from pathlib import Path

# ── الـ charts بالترتيب مع عناوينها ──────────────────────────────────────────
CHARTS = [
    ("lecico_currency_illusion.png",  "Currency Illusion Analysis",          "EGP vs GBP — نمو حقيقي أم وهم؟"),
    ("lecico_profit_chart.png",       "Profitability Overview",               "الربحية عبر السنوات"),
    ("lecico_revenue_breakdown.png",  "Revenue Breakdown",                    "تفصيل الإيرادات"),
    ("lecico_ccc.png",                "Cash Conversion Cycle",                "دورة تحويل النقد"),
    ("lecico_summary.png",            "Executive Summary",                    "الملخص التنفيذي"),
    ("lecico_thesis.png",             "Investment Thesis",                    "أطروحة الاستثمار"),
    ("lecico_q2_forecast.png",        "Q2 2026 — Revenue Forecast",           "توقع إيرادات الربع الثاني"),
    ("lecico_revenue_forecast.png",   "Revenue Forecast — Scenarios",         "سيناريوهات الإيرادات"),
    ("lecico_q2_gp_forecast.png",     "Q2 2026 — Gross Profit Forecast",      "توقع الربح الإجمالي"),
    ("lecico_gm_forecast.png",        "Gross Margin Forecast",                "توقع هامش الربح الإجمالي"),
    ("lecico_ebit_forecast.png",      "EBIT Forecast",                        "توقع الربح التشغيلي"),
    ("lecico_np_forecast_v2.png",     "Net Profit Forecast",                  "توقع صافي الربح"),
    ("lecico_cascade_final.png",      "P&L Cascade — Bull / Base / Bear",     "سيناريوهات الأرباح والخسائر"),
]

# ── اقرأ كل صورة وحوّلها لـ base64 عشان تتضمّن في الـ HTML ──────────────────
def img_to_b64(path: str) -> str | None:
    p = Path(path)
    if not p.exists():
        return None
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ── بناء بطاقات الـ charts ───────────────────────────────────────────────────
cards_html = ""
found, missing = 0, []

for filename, title_en, title_ar in CHARTS:
    b64 = img_to_b64(filename)
    if b64 is None:
        missing.append(filename)
        continue
    found += 1
    cards_html += f"""
    <div class="chart-card">
      <div class="card-header">
        <div class="card-title-en">{title_en}</div>
        <div class="card-title-ar">{title_ar}</div>
      </div>
      <div class="card-body">
        <img src="data:image/png;base64,{b64}" alt="{title_en}" />
      </div>
    </div>
"""

# ── الـ HTML الكامل ───────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lecico Egypt — Financial Analysis Report</title>
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Sans+3:wght@300;400;600&display=swap');

  /* ── Reset & Base ── */
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --navy:   #1B3D5F;
    --gold:   #C49A2A;
    --ink:    #1A1818;
    --soft:   #4A5568;
    --muted:  #8B95A8;
    --rule:   #DDE3EC;
    --bg:     #F7F4EE;
    --white:  #FFFFFF;
  }}

  html {{ font-size: 15px; }}
  body {{
    font-family: 'Source Sans 3', 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--ink);
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  /* ── COVER PAGE ── */
  .cover {{
    width: 100%;
    min-height: 100vh;
    background: var(--navy);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 4rem 2rem;
    page-break-after: always;
    break-after: page;
  }}

  .cover-logo {{
    width: 72px; height: 72px;
    border: 3px solid var(--gold);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 2rem;
    font-size: 1.6rem; font-weight: 900;
    color: var(--gold);
    letter-spacing: 2px;
  }}

  .cover-company {{
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 900;
    color: var(--white);
    letter-spacing: 6px;
    text-transform: uppercase;
    line-height: 1.1;
    margin-bottom: 0.5rem;
  }}

  .cover-ticker {{
    font-size: 0.95rem;
    color: var(--gold);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 3rem;
    font-weight: 600;
  }}

  .cover-divider {{
    width: 80px; height: 3px;
    background: var(--gold);
    margin: 0 auto 3rem;
  }}

  .cover-title {{
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: var(--white);
    font-weight: 700;
    margin-bottom: 0.75rem;
    max-width: 600px;
  }}

  .cover-subtitle {{
    font-size: 1.05rem;
    color: rgba(255,255,255,0.6);
    max-width: 500px;
    line-height: 1.6;
    margin-bottom: 4rem;
  }}

  .cover-meta {{
    display: flex;
    gap: 3rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: auto;
  }}

  .cover-meta-item {{
    text-align: center;
  }}

  .cover-meta-label {{
    font-size: 0.7rem;
    color: var(--gold);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
    font-weight: 600;
  }}

  .cover-meta-value {{
    font-size: 0.95rem;
    color: rgba(255,255,255,0.85);
    font-weight: 400;
  }}

  /* ── BODY LAYOUT ── */
  .report-body {{
    max-width: 960px;
    margin: 0 auto;
    padding: 3rem 2rem;
  }}

  /* ── SECTION HEADER ── */
  .section-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 3.5rem 0 2rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid var(--navy);
  }}

  .section-number {{
    width: 36px; height: 36px;
    background: var(--navy);
    color: var(--white);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    flex-shrink: 0;
  }}

  /* ── CHART CARD ── */
  .chart-card {{
    background: var(--white);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 2.5rem;
    box-shadow: 0 2px 12px rgba(27,61,95,0.08);
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .card-header {{
    background: var(--navy);
    padding: 0.9rem 1.4rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1rem;
  }}

  .card-title-en {{
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    color: var(--white);
    font-weight: 700;
  }}

  .card-title-ar {{
    font-size: 0.85rem;
    color: var(--gold);
    font-weight: 600;
    text-align: right;
    opacity: 0.9;
  }}

  .card-body {{
    padding: 1.2rem;
    background: var(--white);
  }}

  .card-body img {{
    width: 100%;
    height: auto;
    display: block;
    border-radius: 4px;
  }}

  /* ── FOOTER ── */
  .report-footer {{
    text-align: center;
    padding: 2.5rem 1rem;
    margin-top: 3rem;
    border-top: 1px solid var(--rule);
    color: var(--muted);
    font-size: 0.8rem;
    line-height: 1.8;
  }}

  .footer-brand {{
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    color: var(--navy);
    font-weight: 700;
    margin-bottom: 0.4rem;
  }}

  /* ── PRINT RULES ── */
  @media print {{
    body {{ background: var(--bg) !important; }}
    .cover {{ min-height: 100vh; }}
    .chart-card {{ box-shadow: none; border: 1px solid var(--rule); }}
    @page {{
      size: A4;
      margin: 1.2cm 1.5cm;
    }}
  }}
</style>
</head>
<body>

<!-- ══ COVER ══════════════════════════════════════════════════════════════ -->
<div class="cover">
  <div class="cover-logo">L</div>
  <div class="cover-company">Lecico</div>
  <div class="cover-ticker">EGX : LCSW &nbsp;·&nbsp; Ceramics &amp; Sanitary Ware</div>
  <div class="cover-divider"></div>
  <div class="cover-title">Financial Analysis Report</div>
  <div class="cover-subtitle">
    تحليل مالي شامل · FY 2021 – FY 2025<br>
    مع توقعات Q2 2026
  </div>
  <div class="cover-meta">
    <div class="cover-meta-item">
      <div class="cover-meta-label">Sector</div>
      <div class="cover-meta-value">Building Materials</div>
    </div>
    <div class="cover-meta-item">
      <div class="cover-meta-label">Coverage Period</div>
      <div class="cover-meta-value">2021 – 2026</div>
    </div>
    <div class="cover-meta-item">
      <div class="cover-meta-label">Charts</div>
      <div class="cover-meta-value">{found} Exhibits</div>
    </div>
    <div class="cover-meta-item">
      <div class="cover-meta-label">Source</div>
      <div class="cover-meta-value">Annual Financials</div>
    </div>
  </div>
</div>

<!-- ══ BODY ═══════════════════════════════════════════════════════════════ -->
<div class="report-body">
{cards_html}

  <!-- ── FOOTER ── -->
  <div class="report-footer">
    <div class="footer-brand">Lecico Egypt S.A.E. — Financial Analysis</div>
    Source: Lecico Annual Income Statement · Balance Sheet · Cash Flow Statements<br>
    FX: EGP/GBP annual averages · Analysis covers FY 2021 – Q1 2026<br>
    <em>For informational purposes only. Not investment advice.</em>
  </div>
</div>

</body>
</html>
"""

# ── اكتب الملف ────────────────────────────────────────────────────────────────
out = Path("lecico_report.html")
out.write_text(HTML, encoding="utf-8")

print(f"✅ التقرير جاهز: {out.resolve()}")
print(f"   • charts مُدرجة: {found}")
if missing:
    print(f"   • مش موجودة ({len(missing)}): {', '.join(missing)}")
print("\n👉 افتح الملف في Chrome أو Edge")
print("   ثم: Ctrl+P  →  Destination: Save as PDF")
print("   ✓ شيل علامة 'Headers and footers'")
print("   ✓ خلي 'Background graphics' مفعّل عشان الألوان تظهر")
