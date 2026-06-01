import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AquaChem IKA",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

:root {
    --teal:   #0EB8A4;
    --blue:   #1A6EFC;
    --dark:   #0D1117;
    --card:   #161B25;
    --border: #242C3D;
    --text:   #E8EDF5;
    --muted:  #7A8BA6;
    --good:   #22C55E;
    --warn:   #F59E0B;
    --bad:    #EF4444;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--dark);
    color: var(--text);
}

#MainMenu, footer, header {visibility: hidden;}

section[data-testid="stSidebar"] {
    background: var(--card);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

.hero {
    background: linear-gradient(135deg, #0D1117 0%, #0a2a40 50%, #0D1117 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 40px 36px 32px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 280px; height: 280px;
    background: radial-gradient(circle, rgba(14,184,164,0.18) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #0EB8A4, #1A6EFC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px 0;
}
.hero-sub { color: var(--muted); font-size: 1rem; margin: 0; }
.hero-badge {
    display: inline-block;
    background: rgba(14,184,164,0.12);
    border: 1px solid rgba(14,184,164,0.4);
    color: var(--teal);
    border-radius: 20px;
    padding: 3px 14px;
    font-size: 0.72rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.param-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 24px 22px;
    height: 100%;
}
.param-card:hover { border-color: var(--teal); }
.param-title { font-family: 'Space Mono', monospace; font-size: 1rem; color: var(--teal); margin-bottom: 6px; font-weight: 700; }
.param-fullname { color: var(--muted); font-size: 0.8rem; margin-bottom: 16px; }
.param-value { font-size: 2.4rem; font-weight: 800; color: var(--text); line-height: 1; margin-bottom: 4px; }
.param-unit { font-size: 0.8rem; color: var(--muted); margin-bottom: 14px; }
.status-chip { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }
.status-good { background: rgba(34,197,94,0.15);  color: #22C55E; border: 1px solid rgba(34,197,94,0.35); }
.status-warn { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.35); }
.status-bad  { background: rgba(239,68,68,0.15);  color: #EF4444; border: 1px solid rgba(239,68,68,0.35); }

.ref-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
.ref-table th { background: rgba(14,184,164,0.1); color: var(--teal); font-family: 'Space Mono', monospace; font-size: 0.75rem; padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--border); }
.ref-table td { padding: 10px 14px; border-bottom: 1px solid var(--border); color: var(--text); }
.ref-table tr:last-child td { border-bottom: none; }
.ref-table tr:hover td { background: rgba(255,255,255,0.02); }

.sec-head { font-family: 'Space Mono', monospace; font-size: 0.75rem; letter-spacing: 2px; color: var(--teal); text-transform: uppercase; margin: 32px 0 16px 0; display: flex; align-items: center; gap: 10px; }
.sec-head::after { content: ""; flex: 1; height: 1px; background: var(--border); }

.ika-score { font-family: 'Space Mono', monospace; font-size: 3.8rem; font-weight: 700; line-height: 1; }
.ika-label { font-size: 0.85rem; color: var(--muted); margin-top: 6px; }
.ika-cat   { font-size: 1.1rem; font-weight: 700; margin-top: 8px; }

.info-box { background: rgba(14,184,164,0.06); border: 1px solid rgba(14,184,164,0.25); border-left: 4px solid var(--teal); border-radius: 8px; padding: 14px 18px; font-size: 0.88rem; color: var(--text); margin: 10px 0; line-height: 1.6; }
.warn-box { background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.25); border-left: 4px solid #F59E0B; border-radius: 8px; padding: 14px 18px; font-size: 0.88rem; color: var(--text); margin: 10px 0; line-height: 1.6; }
.bad-box  { background: rgba(239,68,68,0.06);  border: 1px solid rgba(239,68,68,0.25);  border-left: 4px solid #EF4444; border-radius: 8px; padding: 14px 18px; font-size: 0.88rem; color: var(--text); margin: 10px 0; line-height: 1.6; }

.about-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 28px 26px; margin-bottom: 18px; }
.about-label { font-family: 'Space Mono', monospace; font-size: 0.7rem; letter-spacing: 2px; color: var(--teal); text-transform: uppercase; margin-bottom: 8px; }
.about-title { font-size: 1.3rem; font-weight: 700; color: var(--text); margin-bottom: 10px; }
.about-body  { color: var(--muted); font-size: 0.9rem; line-height: 1.7; }

.stButton > button {
    background: linear-gradient(135deg, var(--teal), var(--blue));
    color: white; border: none; border-radius: 8px;
    font-family: 'Space Mono', monospace; font-size: 0.8rem;
    letter-spacing: 1px; padding: 10px 24px; width: 100%;
}
div[data-testid="stExpander"] { background: var(--card); border: 1px solid var(--border) !important; border-radius: 10px !important; }
div[data-testid="stExpander"] summary { color: var(--text) !important; }
.stTabs [data-baseweb="tab-list"] { background: var(--card); border-radius: 10px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--muted) !important; border-radius: 7px !important; font-size: 0.85rem; font-weight: 600; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, rgba(14,184,164,0.25), rgba(26,110,252,0.25)) !important; color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
if "app_name"   not in st.session_state: st.session_state.app_name   = "AquaChem IKA"
if "group_name" not in st.session_state: st.session_state.group_name = "Kelompok 4"
if "group_desc" not in st.session_state: st.session_state.group_desc = "Deskripsi kelompok belum diisi."
if "web_desc"   not in st.session_state: st.session_state.web_desc   = "Aplikasi analisis kualitas air berdasarkan parameter kimia pH, BOD, dan COD sesuai PP No. 22 Tahun 2021."

# ─────────────────────────────────────────────
#  REFERENSI DATA
# ─────────────────────────────────────────────
PH_REF = [
    {"Kategori": "Normal / Baku Mutu",            "Rentang": "6.5 – 8.0",              "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Mendekati Normal",               "Rentang": "6.0–6.5 atau 8.0–8.5",  "Status": "🟡 Tercemar Ringan",   "Kelas": "warn"},
    {"Kategori": "Asam / Basa Ringan",             "Rentang": "5.0–6.0 atau 8.5–9.0",  "Status": "⚠️ Tercemar Sedang",  "Kelas": "warn"},
    {"Kategori": "Sangat Asam / Basa (Berbahaya)", "Rentang": "< 5.0 atau > 9.0",      "Status": "💀 Tercemar Berat",    "Kelas": "bad"},
]
BOD_REF = [
    {"Kategori": "Sangat Baik",          "Rentang": "< 2 mg/L",   "Status": "✅ Tidak Tercemar",    "Kelas": "good"},
    {"Kategori": "Baik",                 "Rentang": "2 – 3 mg/L", "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Sedang",      "Rentang": "3 – 6 mg/L", "Status": "⚠️ Tercemar Sedang",  "Kelas": "warn"},
    {"Kategori": "Tercemar Berat",       "Rentang": "6 – 12 mg/L","Status": "🔴 Tercemar Berat",    "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar",      "Rentang": "> 12 mg/L",  "Status": "💀 Sangat Tercemar",   "Kelas": "bad"},
]
COD_REF = [
    {"Kategori": "Sangat Baik",          "Rentang": "< 10 mg/L",    "Status": "✅ Tidak Tercemar",    "Kelas": "good"},
    {"Kategori": "Baik (Kelas I/II)",    "Rentang": "10 – 25 mg/L", "Status": "✅ Memenuhi Baku Mutu", "Kelas": "good"},
    {"Kategori": "Tercemar Ringan–Sedang","Rentang": "25 – 50 mg/L","Status": "⚠️ Tercemar Sedang",  "Kelas": "warn"},
    {"Kategori": "Tercemar Berat",       "Rentang": "50 – 100 mg/L","Status": "🔴 Tercemar Berat",    "Kelas": "bad"},
    {"Kategori": "Sangat Tercemar",      "Rentang": "> 100 mg/L",   "Status": "💀 Sangat Tercemar",   "Kelas": "bad"},
]

# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────
def get_ph_status(v):
    if 6.5 <= v <= 8.0:              return "Memenuhi Baku Mutu", "good", 100
    elif (6.0<=v<6.5)or(8.0<v<=8.5): return "Tercemar Ringan",   "warn", 60
    elif (5.0<=v<6.0)or(8.5<v<=9.0): return "Tercemar Sedang",   "warn", 35
    else:                             return "Tercemar Berat",     "bad",  10

def get_bod_status(v):
    if v < 2:   return "Tidak Tercemar",    "good", 100
    elif v <= 3: return "Memenuhi Baku Mutu","good", 85
    elif v <= 6: return "Tercemar Sedang",   "warn", 50
    elif v <=12: return "Tercemar Berat",    "bad",  25
    else:        return "Sangat Tercemar",   "bad",  5

def get_cod_status(v):
    if v < 10:   return "Tidak Tercemar",    "good", 100
    elif v <= 25: return "Memenuhi Baku Mutu","good", 80
    elif v <= 50: return "Tercemar Sedang",   "warn", 45
    elif v <=100: return "Tercemar Berat",    "bad",  20
    else:         return "Sangat Tercemar",   "bad",  5

def calc_ika(ph, bod, cod):
    _, _, si_ph  = get_ph_status(ph)
    _, _, si_bod = get_bod_status(bod)
    _, _, si_cod = get_cod_status(cod)
    ika = 0.30*si_ph + 0.35*si_bod + 0.35*si_cod
    return round(ika, 1), si_ph, si_bod, si_cod

def ika_category(s):
    if s >= 80: return "Baik 🟢",                      "#22C55E"
    elif s >= 50: return "Tercemar Ringan–Sedang 🟡",  "#F59E0B"
    elif s >= 25: return "Tercemar Berat 🔴",           "#EF4444"
    else:         return "Sangat Tercemar Berat ☠️",    "#EF4444"

def status_chip(label, cls):
    return f'<span class="status-chip status-{cls}">{label}</span>'

def render_ref_table(data):
    rows = "".join(
        f"<tr><td>{r['Kategori']}</td><td>{r['Rentang']}</td>"
        f"<td>{status_chip(r['Status'], r['Kelas'])}</td></tr>"
        for r in data
    )
    st.markdown(f"""
    <table class="ref-table">
      <thead><tr><th>Kategori</th><th>Rentang</th><th>Status</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:18px 0 8px 0;">
        <div style="font-family:'Space Mono',monospace;font-size:1.1rem;font-weight:700;
                    background:linear-gradient(90deg,#0EB8A4,#1A6EFC);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
            💧 AquaChem IKA
        </div>
        <div style="color:#7A8BA6;font-size:0.78rem;margin-top:4px;">Indeks Kualitas Air</div>
    </div>
    <hr style="border:none;border-top:1px solid #242C3D;margin:12px 0 20px 0;">
    """, unsafe_allow_html=True)

    st.markdown("**📥 Masukkan Nilai Parameter**")
    ph_val  = st.slider("pH",         0.0,  14.0,  7.0, 0.1)
    bod_val = st.slider("BOD (mg/L)", 0.0,  30.0,  2.0, 0.5)
    cod_val = st.slider("COD (mg/L)", 0.0, 200.0, 15.0, 1.0)

    st.markdown("<hr style='border:none;border-top:1px solid #242C3D;margin:20px 0;'>", unsafe_allow_html=True)

    with st.expander("⚙️  Pengaturan Aplikasi"):
        new_app  = st.text_input("Nama Aplikasi",      value=st.session_state.app_name)
        new_grp  = st.text_input("Nama Kelompok",      value=st.session_state.group_name)
        new_gdesc= st.text_area("Deskripsi Kelompok",  value=st.session_state.group_desc, height=80)
        new_wdesc= st.text_area("Deskripsi Website",   value=st.session_state.web_desc,   height=100)
        if st.button("💾  SIMPAN PENGATURAN"):
            st.session_state.app_name   = new_app
            st.session_state.group_name = new_grp
            st.session_state.group_desc = new_gdesc
            st.session_state.web_desc   = new_wdesc
            st.success("Pengaturan tersimpan!")

    st.markdown("""
    <div style="margin-top:24px;padding:12px;background:#0D1117;border-radius:8px;
                border:1px solid #242C3D;font-size:0.75rem;color:#7A8BA6;">
        📋 Referensi: PP No. 22/2021<br>Baku mutu air kelas II
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KALKULASI
# ─────────────────────────────────────────────
ika_score, ph_si, bod_si, cod_si = calc_ika(ph_val, bod_val, cod_val)
ika_cat, ika_color = ika_category(ika_score)
ph_label,  ph_cls,  _ = get_ph_status(ph_val)
bod_label, bod_cls, _ = get_bod_status(bod_val)
cod_label, cod_cls, _ = get_cod_status(cod_val)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-badge">INDEKS KUALITAS AIR</div>
  <h1 class="hero-title">{st.session_state.app_name}</h1>
  <p class="hero-sub">{st.session_state.web_desc}</p>
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Analisis Parameter",
    "📖  Referensi Standar",
    "📈  Visualisasi",
    "ℹ️  Tentang",
])

# ══════════════════════════════════════════════
#  TAB 1 — ANALISIS
# ══════════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-head">Indeks Kualitas Air (IKA)</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1.2, 1, 1, 1])

    with c1:
        st.markdown(f"""
        <div class="param-card" style="border-color:{ika_color}40;">
          <div style="text-align:center;padding:16px 0;">
            <div class="ika-score" style="color:{ika_color};">{ika_score}</div>
            <div class="ika-label">Skor IKA (0–100)</div>
            <div class="ika-cat"  style="color:{ika_color};">{ika_cat}</div>
          </div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="param-card">
          <div class="param-title">pH</div>
          <div class="param-fullname">Derajat Keasaman</div>
          <div class="param-value">{ph_val}</div>
          <div class="param-unit">skala</div>
          {status_chip(ph_label, ph_cls)}
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="param-card">
          <div class="param-title">BOD</div>
          <div class="param-fullname">Biochemical Oxygen Demand</div>
          <div class="param-value">{bod_val}</div>
          <div class="param-unit">mg/L</div>
          {status_chip(bod_label, bod_cls)}
        </div>""", unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="param-card">
          <div class="param-title">COD</div>
          <div class="param-fullname">Chemical Oxygen Demand</div>
          <div class="param-value">{cod_val}</div>
          <div class="param-unit">mg/L</div>
          {status_chip(cod_label, cod_cls)}
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Detail Parameter</div>', unsafe_allow_html=True)

    # pH
    with st.expander("🔵  pH — Derajat Keasaman Air", expanded=True):
        ca, cb = st.columns([1, 1.4])
        with ca:
            st.markdown("""
            **Apa itu pH?**
            pH mengukur konsentrasi ion hidrogen dalam air (skala 0–14).
            Nilai 7 bersifat netral; < 7 asam; > 7 basa.

            **Mengapa penting?**
            Nilai di luar 6.5–8.0 mengganggu kehidupan biota air,
            meningkatkan kelarutan logam berat, dan menandakan pencemaran.
            """)
        with cb:
            if ph_cls == "good":
                st.markdown(f'<div class="info-box">✅ <b>pH {ph_val}</b> — Memenuhi baku mutu (6.5–8.0). Air dalam kondisi normal dan aman.</div>', unsafe_allow_html=True)
            elif ph_cls == "warn":
                st.markdown(f'<div class="warn-box">⚠️ <b>pH {ph_val}</b> — Di luar baku mutu optimal. Perlu monitoring lebih lanjut.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <b>pH {ph_val}</b> — Nilai ekstrem! Berbahaya bagi biota air dan tidak layak pakai.</div>', unsafe_allow_html=True)

    # BOD
    with st.expander("🟢  BOD — Biochemical Oxygen Demand", expanded=True):
        ca, cb = st.columns([1, 1.4])
        with ca:
            st.markdown("""
            **Apa itu BOD?**
            Jumlah oksigen yang dibutuhkan mikroorganisme untuk mengurai
            bahan organik secara biologis (5 hari, 20°C).

            **Mengapa penting?**
            BOD tinggi → deplesi oksigen terlarut → membunuh ikan dan
            biota akuatik. Sumber utama: limbah domestik & industri.
            """)
        with cb:
            if bod_cls == "good":
                st.markdown(f'<div class="info-box">✅ <b>BOD {bod_val} mg/L</b> — Memenuhi baku mutu (≤ 3 mg/L). Kandungan bahan organik rendah.</div>', unsafe_allow_html=True)
            elif bod_cls == "warn":
                st.markdown(f'<div class="warn-box">⚠️ <b>BOD {bod_val} mg/L</b> — Melampaui baku mutu. Air terindikasi tercemar bahan organik.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <b>BOD {bod_val} mg/L</b> — Jauh melampaui baku mutu! Pencemaran organik berat.</div>', unsafe_allow_html=True)

    # COD
    with st.expander("🔴  COD — Chemical Oxygen Demand", expanded=True):
        ca, cb = st.columns([1, 1.4])
        with ca:
            st.markdown("""
            **Apa itu COD?**
            Total oksigen untuk mengoksidasi semua bahan organik
            (termasuk yang tidak bisa diurai biologis) dengan oksidator kimia.

            **Mengapa penting?**
            Rasio COD/BOD besar → ada senyawa rekalcitran (pestisida,
            deterjen, limbah kimia industri).
            """)
        with cb:
            if cod_cls == "good":
                st.markdown(f'<div class="info-box">✅ <b>COD {cod_val} mg/L</b> — Memenuhi baku mutu (≤ 25 mg/L). Beban pencemar kimia aman.</div>', unsafe_allow_html=True)
            elif cod_cls == "warn":
                st.markdown(f'<div class="warn-box">⚠️ <b>COD {cod_val} mg/L</b> — Melampaui baku mutu. Perlu investigasi sumber pencemar.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="bad-box">🚨 <b>COD {cod_val} mg/L</b> — Sangat tinggi! Pencemaran kimia berat, butuh pengolahan khusus.</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Analisis Lanjutan</div>', unsafe_allow_html=True)
    if cod_val > 0:
        ratio = round(bod_val / cod_val, 3)
        col1, col2 = st.columns(2)
        with col1:
            if ratio >= 0.5:   bio = '✅ <b style="color:#22C55E">Mudah terurai biologis</b> — cocok untuk IPAL biologis.'
            elif ratio >= 0.3: bio = '⚠️ <b style="color:#F59E0B">Cukup dapat terurai</b> — perlu kombinasi biologis & kimia.'
            else:               bio = '🔴 <b style="color:#EF4444">Sulit terurai biologis</b> — perlu pengolahan kimia-fisika.'
            st.markdown(f"""
            <div class="param-card">
              <div class="param-title">Rasio BOD/COD</div>
              <div class="param-fullname">Biodegradabilitas Limbah</div>
              <div class="param-value">{ratio}</div>
              <div style="margin-top:10px;font-size:0.83rem;color:#7A8BA6;line-height:1.6;">{bio}</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="param-card">
              <div class="param-title">Sub-Indeks Tiap Parameter</div>
              <div class="param-fullname">Kontribusi terhadap IKA</div>
              <div style="margin-top:14px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                  <span style="color:#7A8BA6;font-size:0.83rem;">pH (bobot 30%)</span>
                  <span style="font-family:'Space Mono',monospace;color:#0EB8A4;">{ph_si}</span>
                </div>
                <div style="background:#242C3D;border-radius:4px;height:6px;margin-bottom:12px;">
                  <div style="background:#0EB8A4;width:{ph_si}%;height:100%;border-radius:4px;"></div>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                  <span style="color:#7A8BA6;font-size:0.83rem;">BOD (bobot 35%)</span>
                  <span style="font-family:'Space Mono',monospace;color:#1A6EFC;">{bod_si}</span>
                </div>
                <div style="background:#242C3D;border-radius:4px;height:6px;margin-bottom:12px;">
                  <div style="background:#1A6EFC;width:{bod_si}%;height:100%;border-radius:4px;"></div>
                </div>
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                  <span style="color:#7A8BA6;font-size:0.83rem;">COD (bobot 35%)</span>
                  <span style="font-family:'Space Mono',monospace;color:#8B5CF6;">{cod_si}</span>
                </div>
                <div style="background:#242C3D;border-radius:4px;height:6px;">
                  <div style="background:#8B5CF6;width:{cod_si}%;height:100%;border-radius:4px;"></div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 2 — REFERENSI
# ══════════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-head">Baku Mutu Air — PP No. 22 Tahun 2021</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    📋 Referensi: <b>PP No. 22 Tahun 2021</b> tentang Penyelenggaraan Perlindungan dan Pengelolaan
    Lingkungan Hidup & <b>PermenLHK</b> Baku Mutu Air Permukaan. Acuan: <b>Air Kelas II</b>
    (rekreasi, budidaya ikan, peternakan).
    </div>""", unsafe_allow_html=True)

    st.markdown("#### 🔵 pH — Derajat Keasaman")
    render_ref_table(PH_REF)

    st.markdown("#### 🟢 BOD — Biochemical Oxygen Demand")
    st.markdown('<div style="font-size:0.83rem;color:#7A8BA6;margin-bottom:10px;">Baku mutu BOD kelas II: <b style="color:#0EB8A4;">≤ 3 mg/L</b></div>', unsafe_allow_html=True)
    render_ref_table(BOD_REF)

    st.markdown("#### 🔴 COD — Chemical Oxygen Demand")
    st.markdown('<div style="font-size:0.83rem;color:#7A8BA6;margin-bottom:10px;">Baku mutu COD kelas II: <b style="color:#0EB8A4;">≤ 25 mg/L</b></div>', unsafe_allow_html=True)
    render_ref_table(COD_REF)

    st.markdown('<div class="sec-head">Kategori IKA</div>', unsafe_allow_html=True)
    ika_ref = [
        {"Skor": "80–100", "Kategori": "Baik",                   "Keterangan": "Aman semua peruntukan",              "Kelas": "good"},
        {"Skor": "50–79",  "Kategori": "Tercemar Ringan–Sedang", "Keterangan": "Perlu monitoring",                   "Kelas": "warn"},
        {"Skor": "25–49",  "Kategori": "Tercemar Berat",         "Keterangan": "Tidak layak pakai langsung",         "Kelas": "bad"},
        {"Skor": "0–24",   "Kategori": "Sangat Tercemar Berat",  "Keterangan": "Berbahaya, butuh remediasi intensif","Kelas": "bad"},
    ]
    rows = "".join(
        f"<tr><td><b style='font-family:Space Mono;color:#0EB8A4;'>{r['Skor']}</b></td>"
        f"<td>{status_chip(r['Kategori'],r['Kelas'])}</td><td>{r['Keterangan']}</td></tr>"
        for r in ika_ref
    )
    st.markdown(f"""
    <table class="ref-table">
      <thead><tr><th>Skor IKA</th><th>Kategori</th><th>Keterangan</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
#  TAB 3 — VISUALISASI
# ══════════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-head">Visualisasi Posisi Parameter</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ika_score,
            title={"text": "Indeks Kualitas Air (IKA)", "font": {"color": "#E8EDF5", "size": 14}},
            number={"font": {"color": ika_color, "size": 48}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#7A8BA6", "tickfont": {"color": "#7A8BA6", "size": 11}},
                "bar": {"color": ika_color, "thickness": 0.25},
                "bgcolor": "#161B25",
                "borderwidth": 0,
                "steps": [
                    {"range": [0,  25],  "color": "rgba(239,68,68,0.15)"},
                    {"range": [25, 50],  "color": "rgba(239,68,68,0.08)"},
                    {"range": [50, 80],  "color": "rgba(245,158,11,0.10)"},
                    {"range": [80, 100], "color": "rgba(34,197,94,0.12)"},
                ],
                "threshold": {"line": {"color": ika_color, "width": 3}, "thickness": 0.75, "value": ika_score},
            }
        ))
        fig_gauge.update_layout(paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                                font={"color": "#E8EDF5"}, height=300,
                                margin=dict(l=30,r=30,t=40,b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        categories = ["pH", "BOD", "COD"]
        values     = [ph_si, bod_si, cod_si]
        fig_radar  = go.Figure(go.Scatterpolar(
            r=values+[values[0]], theta=categories+[categories[0]],
            fill="toself", fillcolor="rgba(14,184,164,0.15)",
            line=dict(color="#0EB8A4", width=2), name="Sub-Indeks",
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=[100,100,100,100], theta=categories+[categories[0]],
            fill="toself", fillcolor="rgba(255,255,255,0.02)",
            line=dict(color="#242C3D", width=1, dash="dot"), name="Maks",
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#161B25",
                radialaxis=dict(visible=True, range=[0,100],
                                tickfont={"color":"#7A8BA6","size":10},
                                gridcolor="#242C3D", linecolor="#242C3D"),
                angularaxis=dict(tickfont={"color":"#E8EDF5","size":12},
                                 gridcolor="#242C3D", linecolor="#242C3D"),
            ),
            paper_bgcolor="#0D1117", font={"color":"#E8EDF5"},
            showlegend=False,
            title={"text":"Sub-Indeks Tiap Parameter","font":{"color":"#E8EDF5","size":14}},
            height=300, margin=dict(l=30,r=30,t=50,b=20)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown('<div class="sec-head">Posisi Nilai vs Batas Baku Mutu</div>', unsafe_allow_html=True)
    fig_bar = make_subplots(rows=1, cols=3, subplot_titles=["pH","BOD (mg/L)","COD (mg/L)"])

    fig_bar.add_trace(go.Bar(x=["Nilai"], y=[ph_val],
        marker_color=("#22C55E" if ph_cls=="good" else "#F59E0B" if ph_cls=="warn" else "#EF4444")), row=1, col=1)
    fig_bar.add_hline(y=6.5, line_dash="dash", line_color="#7A8BA6",
        annotation_text="Min 6.5", annotation_font_color="#7A8BA6", row=1, col=1)
    fig_bar.add_hline(y=8.0, line_dash="dash", line_color="#7A8BA6",
        annotation_text="Max 8.0", annotation_font_color="#7A8BA6", row=1, col=1)

    fig_bar.add_trace(go.Bar(x=["Nilai"], y=[bod_val],
        marker_color=("#22C55E" if bod_cls=="good" else "#F59E0B" if bod_cls=="warn" else "#EF4444")), row=1, col=2)
    fig_bar.add_hline(y=3.0, line_dash="dash", line_color="#7A8BA6",
        annotation_text="Batas 3", annotation_font_color="#7A8BA6", row=1, col=2)

    fig_bar.add_trace(go.Bar(x=["Nilai"], y=[cod_val],
        marker_color=("#22C55E" if cod_cls=="good" else "#F59E0B" if cod_cls=="warn" else "#EF4444")), row=1, col=3)
    fig_bar.add_hline(y=25.0, line_dash="dash", line_color="#7A8BA6",
        annotation_text="Batas 25", annotation_font_color="#7A8BA6", row=1, col=3)

    fig_bar.update_layout(paper_bgcolor="#0D1117", plot_bgcolor="#0D1117",
                          font={"color":"#E8EDF5"}, showlegend=False, height=320,
                          margin=dict(l=20,r=20,t=50,b=20))
    fig_bar.update_xaxes(showgrid=False, zeroline=False)
    fig_bar.update_yaxes(gridcolor="#242C3D", zeroline=False)
    for ann in fig_bar.layout.annotations:
        ann.font.color = "#E8EDF5"
    st.plotly_chart(fig_bar, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 4 — TENTANG
# ══════════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-head">Tentang Aplikasi & Kelompok</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="about-card">
          <div class="about-label">Tentang Aplikasi</div>
          <div class="about-title">💧 {st.session_state.app_name}</div>
          <div class="about-body">{st.session_state.web_desc}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="about-card">
          <div class="about-label">Tentang Kelompok</div>
          <div class="about-title">👥 {st.session_state.group_name}</div>
          <div class="about-body">{st.session_state.group_desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="about-card">
      <div class="about-label">Metodologi IKA</div>
      <div class="about-title">📐 Cara Perhitungan Indeks</div>
      <div class="about-body">
        Indeks Kualitas Air dihitung dengan sistem sub-indeks berbobot:<br><br>
        <code style="background:#0D1117;padding:10px 16px;border-radius:6px;border:1px solid #242C3D;
                     display:block;font-family:'Space Mono',monospace;color:#0EB8A4;font-size:0.85rem;">
          IKA = (0.30 × SI_pH) + (0.35 × SI_BOD) + (0.35 × SI_COD)
        </code>
        <br>SI (Sub-Indeks) bernilai 0–100 berdasarkan posisi nilai terhadap baku mutu.
        BOD dan COD diberi bobot lebih besar karena mencerminkan beban pencemaran organik utama.
      </div>
    </div>
    <div style="text-align:center;padding:24px 0 8px;color:#7A8BA6;font-size:0.78rem;font-family:'Space Mono',monospace;">
        Referensi: PP No. 22/2021 · PermenLHK P.22/2021 · SNI 6989<br>
        Built with Streamlit & Plotly
    </div>""", unsafe_allow_html=True)
