"""
LeadFoundry spinner messages – Industrial Foundry Theme
Molten metal aesthetics with orange/gold accents
"""

_SPINNER_MESSAGES = {
    "intake": (
        "📐 Target Definition",
        "Locking parameters and preparing the discovery pipeline."
    ),
    "research": (
        "⚒️ Multi-Source Discovery",
        "Mining, filtering, and validating lead signals."
    ),
    "finalize": (
        "🔥 Signal Refinement",
        "Tempering data and casting final deliverables."
    ),
}




def _normalize_step(step: str) -> str:
    step = step.lower()

    if "intake" in step:
        return "intake"
    if "research" in step:
        return "research"
    if "final" in step or "optimize" in step:
        return "finalize"

    return step


def render_spinning_status(html_placeholder, progress_placeholder, step, progress_fraction):
    normalized_step = _normalize_step(step)

    if normalized_step in _SPINNER_MESSAGES:
        title, subtitle = _SPINNER_MESSAGES[normalized_step]
    else:
        title, subtitle = "⏳ Working…", "Processing your request."

    html = f"""
    <style>
    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}

    .lf-spinner {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        margin: 1.5rem 0;
        border-radius: 14px;
        background: linear-gradient(
            135deg,
            rgba(18,20,23,0.95),
            rgba(26,30,34,0.9)
        );
        border: 1px solid rgba(255,138,61,0.25);
    }}

    .lf-spinner-wheel {{
        width: 56px;
        height: 56px;
        border-radius: 50%;
        border: 4px solid rgba(255,138,61,0.25);
        border-top-color: #FF8A3D;
        animation: spin 1s linear infinite;
        margin-bottom: 1.25rem;
    }}

    .lf-spinner-title {{
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        background: linear-gradient(135deg, #FFB341, #FF8A3D);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-align: center;
    }}

    .lf-spinner-subtitle {{
        font-size: 0.95rem;
        color: rgba(244,245,246,0.7);
        text-align: center;
        max-width: 520px;
        line-height: 1.5;
    }}

    @media (prefers-reduced-motion: reduce) {{
        .lf-spinner-wheel {{
            animation: none;
        }}
    }}
    </style>

    <div class="lf-spinner">
        <div class="lf-spinner-wheel"></div>
        <div class="lf-spinner-title">{title}</div>
        <div class="lf-spinner-subtitle">{subtitle}</div>
    </div>
    """

    html_placeholder.markdown(html, unsafe_allow_html=True)

    try:
        progress_placeholder.progress(progress_fraction)
    except Exception:
        pass
