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
    @keyframes rotate-cw {{
        to {{ transform: rotate(360deg); }}
    }}

    @keyframes rotate-ccw {{
        to {{ transform: rotate(-360deg); }}
    }}

    @keyframes heat-pulse {{
        0% {{ box-shadow: 0 0 12px rgba(255,138,61,0.25); }}
        50% {{ box-shadow: 0 0 22px rgba(255,138,61,0.45); }}
        100% {{ box-shadow: 0 0 12px rgba(255,138,61,0.25); }}
    }}

    .lf-spinner {{
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 2.2rem;
        margin: 1.6rem 0;
        border-radius: 16px;
        background: linear-gradient(
            135deg,
            rgba(18,20,23,0.96),
            rgba(28,32,36,0.92)
        );
        border: 1px solid rgba(255,138,61,0.28);
        animation: heat-pulse 2.8s ease-in-out infinite;
    }}

    .lf-gear-wrap {{
        position: relative;
        width: 78px;
        height: 56px;
        margin-bottom: 1.4rem;
    }}

    .lf-gear {{
        position: absolute;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        border: 4px solid rgba(255,138,61,0.35);
        background:
            radial-gradient(circle at center, rgba(255,138,61,0.15), transparent 60%);
    }}

    .lf-gear::before {{
        content: "";
        position: absolute;
        inset: -6px;
        border-radius: 50%;
        border: 2px dashed rgba(255,179,65,0.45);
    }}

    .lf-gear-a {{
        left: 0;
        top: 10px;
        animation: rotate-cw 1.4s linear infinite;
    }}

    .lf-gear-b {{
        right: 0;
        top: 10px;
        animation: rotate-ccw 1.4s linear infinite;
    }}

    .lf-spinner-title {{
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
        background: linear-gradient(135deg, #FFB341, #FF8A3D);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-align: center;
        letter-spacing: 0.02em;
    }}

    .lf-spinner-subtitle {{
        font-size: 0.95rem;
        color: rgba(244,245,246,0.72);
        text-align: center;
        max-width: 520px;
        line-height: 1.5;
    }}

    @media (prefers-reduced-motion: reduce) {{
        .lf-gear-a,
        .lf-gear-b {{
            animation: none;
        }}
        .lf-spinner {{
            animation: none;
        }}
    }}
    </style>

    <div class="lf-spinner">
        <div class="lf-gear-wrap">
            <div class="lf-gear lf-gear-a"></div>
            <div class="lf-gear lf-gear-b"></div>
        </div>
        <div class="lf-spinner-title">{title}</div>
        <div class="lf-spinner-subtitle">{subtitle}</div>
    </div>
    """

    html_placeholder.markdown(html, unsafe_allow_html=True)

    try:
        progress_placeholder.progress(progress_fraction)
    except Exception:
        pass
