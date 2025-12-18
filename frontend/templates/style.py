import base64
from pathlib import Path
import streamlit as st
import uuid


LF_STYLE = r"""
:root{
    --bg-1: #0f1214;
    --bg-2: #1a1e22;
    --bg-3: #22262a;
    --accent-1: #FF8A3D;
    --accent-2: #FFB341;
    --accent-glow: rgba(255,138,61,0.15);
    --metal-1: #2f3438;
    --text: #eef0f1;
    --text-muted: #a8abaf;
    --text-subtle: #787b7f;
    --input-text: #EDE6DC;
    --input-placeholder: rgba(237,230,220,0.45);
    --glass: rgba(255,255,255,0.03);
    --glass-border: rgba(255,255,255,0.08);
    --card-glow: 0 8px 30px rgba(255,138,61,0.12);
    --radius-lg: 14px;
    --radius-md: 10px;
    --radius-sm: 8px;
    --mono: ui-monospace, "SF Mono", "Roboto Mono", "Segoe UI Mono", Consolas, monospace;
}

/* Base and background */
html, body, [class*="css"] {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: var(--text);
    background: 
        radial-gradient(1400px 700px at 15% 25%, rgba(255,138,61,0.05), transparent 14%),
        radial-gradient(1200px 600px at 85% 75%, rgba(255,179,65,0.04), transparent 12%),
        linear-gradient(165deg, var(--bg-1) 0%, var(--bg-2) 40%, var(--bg-3) 100%);
    background-attachment: fixed;
}

/* Subtle film grain texture */
body::before{
    content: "";
    position: fixed;
    inset: 0;
    background-image: url('data:image/svg+xml;utf8,\
      <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">\
      <filter id="noise"><feTurbulence baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/></filter>\
      <rect width="100%" height="100%" filter="url(%23noise)" opacity="0.035"/></svg>');
    opacity: 0.8;
    pointer-events: none;
    z-index: 0;
    mix-blend-mode: overlay;
}

/* Hero title - molten metal animation */
.lf-hero-title {
    font-family: "Sora", "Inter", system-ui, sans-serif;
    font-size: clamp(2rem, 4vw, 3.4rem);
    font-weight: 900;
    background: linear-gradient(110deg, var(--accent-1) 0%, var(--accent-2) 45%, #FFD580 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    letter-spacing: -0.025em;
    line-height: 1.1;
    background-size: 300% 300%;
    animation: molten-sheen 8s ease-in-out infinite;
    filter: drop-shadow(0 4px 20px rgba(255,138,61,0.2));
    margin: 0.5rem 0;
}

@keyframes molten-sheen {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

/* Tagline and subtle text */
.lf-hero-tagline { 
    color: var(--text-muted); 
    font-size: 1.05rem; 
    line-height: 1.65; 
    font-weight: 400;
    margin-top: 0.75rem;
}

.lf-subtle { 
    color: var(--text-subtle); 
    font-size: 0.88rem; 
    font-style: italic; 
    opacity: 0.9;
}

/* Section headers with animated glow */
.lf-section-title {
    font-size: 1.1rem;
    font-weight: 800;
    color: #FFE9C7;
    padding-bottom: 0.65rem;
    margin-bottom: 1.2rem;
    margin-top: 2rem;
    border-bottom: 2px solid transparent;
    position: relative;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.lf-section-title::after{
    content: "";
    position: absolute;
    left: 0;
    bottom: -2px;
    width: 80%;
    max-width: 300px;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-1) 0%, var(--accent-2) 50%, transparent 100%);
    filter: blur(4px);
    opacity: 0.8;
    animation: glow-pulse 3s ease-in-out infinite;
}

@keyframes glow-pulse {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 0.95; }
}

/* Sidebar - Control Console */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c0f12 0%, #13171b 40%, #171b20 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
    box-shadow: inset -1px 0 0 rgba(255,255,255,0.04), 6px 0 30px rgba(0,0,0,0.6);
}

section[data-testid="stSidebar"] > div {
    padding: 1.2rem 1rem;
}

.lf-sidebar-brand {
    margin-bottom: 1.2rem;
}

.lf-sidebar-brand-title {
    font-family: "Sora", "Inter", system-ui, sans-serif;
    font-size: 1.05rem;
    font-weight: 900;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    background: linear-gradient(110deg, var(--accent-1) 0%, var(--accent-2) 55%, #FFD580 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    text-shadow: 0 0 18px rgba(255,138,61,0.35), 0 0 32px rgba(255,138,61,0.15);
    margin-bottom: 0.25rem;
}

.lf-sidebar-brand-subtitle {
    font-family: "IBM Plex Sans", "Inter", system-ui, sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255,217,163,0.7);
    opacity: 0.9;
}

.lf-sidebar-title {
    font-size: 0.95rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #ffd9a3;
    margin-bottom: 0.25rem;
}

.lf-sidebar-subtitle {
    font-size: 0.82rem;
    color: var(--text-subtle);
    margin-bottom: 1.2rem;
    line-height: 1.4;
}

.lf-sidebar-section {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.45);
    margin: 1.2rem 0 0.5rem;
}

.lf-sidebar-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,138,61,0.35), transparent);
    margin: 0.8rem 0;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    font-size: 0.85rem !important;
    padding: 0.55rem 0.9rem !important;
}

section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] textarea,
section[data-testid="stSidebar"] [data-baseweb="select"] {
    font-size: 0.85rem !important;
}

/* Pipeline step chips */
.lf-step-chip{ 
    display: flex; 
    gap: 0.7rem; 
    align-items: center; 
    padding: 0.7rem 1rem; 
    border-radius: var(--radius-sm); 
    font-size: 0.95rem; 
    background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.005)); 
    border: 1px solid var(--glass-border);
    margin-bottom: 0.5rem;
    transition: all 0.2s ease;
}

.lf-step-chip .icon{ 
    width: 26px; 
    height: 26px; 
    display: inline-flex; 
    align-items: center;
    justify-content: center;
    border-radius: 6px; 
    background: linear-gradient(135deg, rgba(0,0,0,0.2), rgba(255,255,255,0.03)); 
    font-size: 0.9rem;
    flex-shrink: 0;
}

.lf-step-done{ 
    color: #c8cacc; 
    border-left: 3px solid rgba(100,200,150,0.3);
    background: linear-gradient(135deg, rgba(100,200,150,0.04), transparent);
}

.lf-step-active{ 
    background: linear-gradient(120deg, var(--accent-glow), rgba(255,179,65,0.08)); 
    border: 1px solid rgba(255,138,61,0.25);
    border-left: 4px solid var(--accent-1); 
    color: var(--text);
    font-weight: 700; 
    box-shadow: 0 8px 24px rgba(255,138,61,0.15);
}

.lf-step-active .icon {
    background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
    color: #0f1214;
    font-weight: 800;
}

.lf-step-upcoming{ 
    color: var(--text-subtle); 
    opacity: 0.7;
    border-left: 3px solid rgba(255,255,255,0.06);
}

/* Form inputs - FIXED TEXT VISIBILITY */
.stTextInput > div > input,
.stNumberInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div,
.stSelectbox input,
textarea,
input {
    font-family: "IBM Plex Sans", "Inter", system-ui, sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.01em;
    color: #EDE6DC !important;
    -webkit-text-fill-color: #EDE6DC !important;
    border-radius: var(--radius-md) !important;
    background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01)) !important;
    border: 1.5px solid var(--glass-border) !important;
    padding: 0.65rem 0.9rem !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    backdrop-filter: blur(8px);
}

/* More specific selectors for stubborn overrides */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    color: #EDE6DC !important;
    -webkit-text-fill-color: #EDE6DC !important;
}

/* Selectbox selected value and button */
.stSelectbox [data-baseweb="select"] [data-baseweb="tag"] {
    color: #EDE6DC !important;
}

.stSelectbox div[role="button"] {
    color: #EDE6DC !important;
}

input::placeholder,
textarea::placeholder {
    color: rgba(237,230,220,0.45) !important;
    -webkit-text-fill-color: rgba(237,230,220,0.45) !important;
    font-weight: 400;
}

.stTextInput > div > input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus,
textarea:focus {
    outline: none !important;
    box-shadow: 0 0 0 3px var(--accent-glow), 0 8px 24px rgba(255,138,61,0.15) !important;
    border-color: var(--accent-1) !important;
    transform: translateY(-1px);
    background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02)) !important;
}

/* Dropdown menu items */
.stSelectbox div[data-baseweb="menu"] {
    font-family: "IBM Plex Sans", "Inter", system-ui, sans-serif !important;
    font-weight: 500 !important;
    color: #1A1D21 !important;
}

/* Buttons - industrial strength */
.stButton > button, 
button[kind="primary"]{
    font-family: "Inter", system-ui, sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.025em !important;
    text-transform: uppercase;
    border-radius: var(--radius-md) !important; 
    padding: 0.7rem 1.5rem !important; 
    background: linear-gradient(135deg, var(--accent-1) 0%, var(--accent-2) 100%) !important;
    color: #0a0c0e !important; 
    border: none !important;
    box-shadow: 
        0 1px 0 0 rgba(255,255,255,0.2) inset,
        0 12px 28px rgba(0,0,0,0.4), 
        0 4px 12px var(--accent-glow) !important;
    transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.2), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.stButton > button:hover{ 
    transform: translateY(-2px) !important; 
    box-shadow: 
        0 1px 0 0 rgba(255,255,255,0.25) inset,
        0 16px 38px rgba(0,0,0,0.5), 
        0 6px 20px var(--accent-glow) !important;
}

.stButton > button:hover::before {
    opacity: 1;
}

.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow: 
        0 1px 3px rgba(0,0,0,0.3) inset,
        0 8px 20px rgba(0,0,0,0.4) !important;
}

/* Preview/content blocks */
.lf-preview-block{ 
    border-radius: var(--radius-lg); 
    padding: 1.25rem; 
    background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); 
    border: 1px solid var(--glass-border); 
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    backdrop-filter: blur(10px);
    margin: 1rem 0;
}

/* Cards - for grouping content */
.lf-card {
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    background: linear-gradient(135deg, rgba(255,255,255,0.025), rgba(255,255,255,0.01));
    border: 1px solid var(--glass-border);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    margin: 1rem 0;
}

/* Code blocks */
.lf-code {
    font-family: var(--mono);
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: var(--radius-sm);
    padding: 0.15rem 0.4rem;
    font-size: 0.88rem;
    color: #ffd580;
}

/* Divider */
.lf-divider{ 
    height: 3px; 
    background: linear-gradient(90deg, transparent 0%, var(--accent-1) 50%, transparent 100%); 
    border-radius: 3px; 
    margin: 2rem 0;
    opacity: 0.4;
}

/* Utility classes */
.lf-small-muted{ 
    color: var(--text-muted); 
    font-size: 0.85rem; 
}

.lf-success{ 
    background: linear-gradient(135deg, rgba(80,200,130,0.08), rgba(80,200,120,0.04)); 
    border: 1px solid rgba(80,200,140,0.2); 
    padding: 0.75rem 1rem; 
    border-radius: var(--radius-md); 
    color: #b5f0d0;
    border-left: 3px solid rgba(80,200,140,0.6);
}

.lf-warning {
    background: linear-gradient(135deg, rgba(255,179,65,0.08), rgba(255,138,61,0.04));
    border: 1px solid rgba(255,179,65,0.2);
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    color: #ffd9a3;
    border-left: 3px solid rgba(255,179,65,0.6);
}

.lf-error {
    background: linear-gradient(135deg, rgba(255,80,80,0.08), rgba(200,60,60,0.04));
    border: 1px solid rgba(255,80,80,0.2);
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md);
    color: #ffb3b3;
    border-left: 3px solid rgba(255,80,80,0.6);
}

/* Ensure app content stays above decorations */
.stApp > *{ 
    position: relative; 
    z-index: 2; 
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Animated SVG heatwave decoration */
.lf-heatwave{
    position: fixed;
    left: 0;
    right: 0;
    bottom: -10vh;
    height: 35vh;
    z-index: 1;
    pointer-events: none;
    opacity: 0.22;
    filter: blur(20px) saturate(1.15);
    transform: translateZ(0);
}

/* Accessibility: reduced motion support */
@media (prefers-reduced-motion: reduce) {
    .lf-hero-title, 
    .stButton > button, 
    .lf-step-active, 
    body::after,
    .lf-section-title::after { 
        animation: none !important; 
        transition: none !important; 
    }
    .lf-heatwave { 
        display: none; 
    }
}

/* Mobile responsiveness */
@media (max-width: 768px) {
    .lf-hero-title { font-size: 2rem; }
    .lf-section-title { font-size: 1rem; }
    .lf-step-chip { padding: 0.6rem 0.8rem; font-size: 0.9rem; }
    .stButton > button { padding: 0.6rem 1.2rem !important; }
}
"""

HEATWAVE_SVG = r'''
<svg class="lf-heatwave" viewBox="0 0 1400 220" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="heatGrad" x1="0" x2="1" y1="0" y2="0">
      <stop offset="0%" stop-color="#ffb341" stop-opacity="0.28"/>
      <stop offset="40%" stop-color="#ff8a3d" stop-opacity="0.38"/>
      <stop offset="70%" stop-color="#d4693b" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#ffb341" stop-opacity="0.15"/>
    </linearGradient>
    <filter id="heatBlur" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="22" result="blur"/>
      <feBlend in="SourceGraphic" in2="blur" mode="normal"/>
    </filter>
  </defs>
  <g filter="url(#heatBlur)">
    <path fill="url(#heatGrad)" d="M0 140 C200 50, 400 180, 700 130 C1000 80, 1200 170, 1400 110 L1400 240 L0 240 Z">
      <animate 
        attributeName="d" 
        dur="7s" 
        repeatCount="indefinite"
        values="M0 140 C200 50, 400 180, 700 130 C1000 80, 1200 170, 1400 110 L1400 240 L0 240 Z;
                M0 110 C200 100, 400 130, 700 160 C1000 190, 1200 140, 1400 130 L1400 240 L0 240 Z;
                M0 130 C200 70, 400 160, 700 120 C1000 90, 1200 150, 1400 120 L1400 240 L0 240 Z;
                M0 140 C200 50, 400 180, 700 130 C1000 80, 1200 170, 1400 110 L1400 240 L0 240 Z"/>
    </path>
  </g>
</svg>
'''




def apply_lf_styles(accent_hex: str = "#FF8A3D", enable_heatwave: bool = True):

    img_path = Path(__file__).parent / "background.png"
    bg_url = ""
    
    if img_path.exists():
        try:
            with img_path.open("rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            bg_url = f"data:image/png;base64,{b64}"
        except Exception:
            pass
    
    unique_id = uuid.uuid4().hex[:8]
    style_with_accent = LF_STYLE.replace("--accent-1: #FF8A3D;", f"--accent-1: {accent_hex};")
    
    html_parts = [f'<style id="lf-style-{unique_id}">\n{style_with_accent}\n']
    
    if bg_url:
        html_parts.append(
            ".stApp::before { "
            'content: ""; '
            "position: fixed; "
            "inset: 0; "
            f'background-image: url("{bg_url}"); '
            "background-size: cover; "
            "background-position: center; "
            "background-repeat: no-repeat; "
            "opacity: 0.12; "
            "pointer-events: none; "
            "z-index: -1; "
            "filter: contrast(1.1) brightness(0.75); "
            "}\n"
        )
    
    html_parts.append("</style>")
    
    if enable_heatwave:
        html_parts.append(HEATWAVE_SVG)
    
    st.markdown("".join(html_parts), unsafe_allow_html=True)
