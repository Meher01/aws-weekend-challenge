from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from botocore.exceptions import BotoCoreError, ClientError

from agent import generate_article, generate_plan


st.set_page_config(
    page_title="Weekend Spark · your agent idea, made real",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

speech_input = components.declare_component(
    "weekend_spark_speech_input",
    path=str(Path(__file__).parent / "components" / "speech_input"),
)

DEFAULT_BRIEF = {
    "project_name": "Weekend Spark",
    "audience": "AWS builders with one weekend and a promising idea",
    "problem": "Turning a fuzzy agent idea into a realistic weekend build and a clear Builder Center story.",
    "delightful_detail": "Celebrate one tiny, finishable next step instead of overwhelming people with a giant roadmap.",
}

if (
    st.query_params.get("demo") == "1"
    and "plan" not in st.session_state
    and not st.session_state.get("demo_plan_initialized")
):
    st.session_state["brief"] = DEFAULT_BRIEF.copy()
    st.session_state["plan"] = generate_plan(**DEFAULT_BRIEF)
    st.session_state["demo_plan_initialized"] = True

if "problem" not in st.session_state:
    st.session_state["problem"] = DEFAULT_BRIEF["problem"]

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
    :root {
        --ink: #392630;
        --muted: #76636e;
        --pink: #f3dce6;
        --pink-deep: #b86f8d;
        --paper: #fff9fb;
    }
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; font-size: 17px; }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stSidebar"] { background: #fff1f6; border-right: 1px solid #f0dce5; }
    [data-testid="stSidebar"] > div { padding-top: 1.4rem; }
    h1, h2, h3 { font-family: 'Manrope', sans-serif; letter-spacing: -0.035em; color: var(--ink); }
    h1 { font-size: 2.35rem; }
    h2 { font-size: 1.8rem; }
    h3 { font-size: 1.45rem; }
    p, li, label, [data-testid="stCaptionContainer"] { font-size: 1.04rem; }
    .voice-heading { font-family: 'Manrope', sans-serif; color: var(--ink); font-size: 1.15rem; font-weight: 700; margin: .6rem 0 .25rem; }
    .hero { background: linear-gradient(135deg, #fff0f6 0%, #f7e3ec 100%); color: var(--ink); border: 1px solid #f0d8e3; border-radius: 24px; padding: 2.5rem 2.65rem; margin: .5rem 0 1.4rem; }
    .hero h1 { color: var(--ink); font-size: clamp(2.45rem, 5.3vw, 3.7rem); line-height: 1.08; margin: .7rem 0 .9rem; }
    .hero p { color: #624b57; max-width: 700px; font-size: 1.15rem; line-height: 1.7; margin-bottom: 0; }
    .eyebrow { text-transform: uppercase; color: #a65375; font-size: .88rem; font-weight: 700; letter-spacing: .16em; }
    .pill { display: inline-block; background: #fbe8ef; color: #784358; border-radius: 999px; padding: .42rem .8rem; font-size: .88rem; font-weight: 700; margin: 0 .35rem .35rem 0; }
    .soft-card { background: #fff; border: 1px solid #f0dfe6; padding: 1.2rem 1.35rem; border-radius: 17px; height: 100%; }
    .soft-card p { color: var(--muted); margin-bottom: 0; }
    .stButton > button, .stDownloadButton > button {
        background: #fbeaf0 !important;
        border: 1px solid #efd4df !important;
        color: #684252 !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: background .16s ease, border-color .16s ease, transform .16s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #f5dce6 !important;
        border-color: #e7c1d0 !important;
        color: #563446 !important;
        transform: translateY(-1px);
    }
    .stButton > button[kind*="primary"] {
        background: #b86f8d !important;
        border-color: #ad6482 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    .stButton > button[kind*="primary"]:hover {
        background: #a85e7d !important;
        border-color: #9c5574 !important;
        color: #ffffff !important;
    }
    [data-testid="stMetric"] { background: white; border: 1px solid #f0dfe6; border-radius: 15px; padding: .9rem 1rem; }
    div[data-testid="stForm"] { background: white; border: 1px solid #f0dfe6; border-radius: 19px; padding: 1.1rem 1.25rem; }
    .footer { color: #8a7480; text-align: center; font-size: .95rem; padding: 2rem 0 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.markdown("## ✨ Weekend Spark")
    st.caption("Your friendly co-builder for a small, shippable AI agent.")
    st.markdown("---")
    provider = st.radio(
        "How should Spark think?",
        ["Local preview", "Amazon Bedrock"],
        help="Local preview works without AWS. Bedrock uses your configured AWS credentials and Bedrock model access.",
    )
    region = st.text_input(
        "AWS Region",
        value=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        disabled=provider != "Amazon Bedrock",
    )
    model_id = st.text_input(
        "Bedrock model or inference profile ID",
        value=os.getenv("BEDROCK_MODEL_ID", ""),
        placeholder="Paste an ID available in your region",
        disabled=provider != "Amazon Bedrock",
        help="Choose an ID available to your account and region. Newer models may require an inference profile ID.",
    )
    if provider == "Amazon Bedrock":
        st.info("Uses Bedrock Runtime Converse. Your AWS credentials stay on your machine; nothing is deployed by this app.")
        if not model_id.strip():
            st.warning("Add a model or inference profile ID before generating.")
    else:
        st.success("Ready to play — local preview needs no AWS account.")
    st.markdown("---")
    st.caption("A weekend prototype, built for builders.")

st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">A little momentum goes a long way</div>
      <h1>Turn a weekend idea<br>into a real agent.</h1>
      <p>Describe or speak your project idea. Get a practical solution path, AWS services matched to what you want to build, and an article draft based on your blueprint.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

badges = st.columns(3)
for col, title, desc in zip(
    badges,
    ("01 · Find the spark", "02 · Make it buildable", "03 · Tell the story"),
    ("A clear audience and real problem.", "Small milestones, sensible AWS choices.", "A ready-to-edit #agents article."),
):
    with col:
        st.markdown(f'<div class="soft-card"><span class="pill">{title}</span><p>{desc}</p></div>', unsafe_allow_html=True)

st.write("")
st.markdown('<div class="voice-heading">Tell Spark about your idea</div>', unsafe_allow_html=True)
st.caption("Speak your idea or type it below. Review the transcript under 'Share your Blueprint' section -- in the description -- before generating. Browser speech recognition may use your browser's speech service. If you choose Bedrock, Spark sends the submitted project brief—including this transcript—to Bedrock; local preview sends no project content to AWS.")
voice_result = speech_input(key="spoken_project_idea", default=None)
if isinstance(voice_result, dict):
    transcript = voice_result.get("text")
    nonce = voice_result.get("nonce")
    if isinstance(transcript, str) and transcript.strip() and nonce != st.session_state.get("last_voice_nonce"):
        st.session_state["problem"] = transcript.strip()
        st.session_state["last_voice_nonce"] = nonce

left, right = st.columns([1.05, 0.95], gap="large")
with left:
    st.subheader("Shape your blueprint")
    with st.form("project_brief", border=False):
        project_name = st.text_input("What should we call it?", value=DEFAULT_BRIEF["project_name"], max_chars=100)
        audience = st.text_input("Who is it for?", value=DEFAULT_BRIEF["audience"], max_chars=300)
        problem = st.text_area(
            "Describe the project idea and what it should help people do",
            key="problem",
            height=105,
            max_chars=1200,
        )
        delightful_detail = st.text_area(
            "What should make using it feel good?",
            value=DEFAULT_BRIEF["delightful_detail"],
            height=80,
            max_chars=300,
        )
        submitted = st.form_submit_button("Make my project blueprint  →", type="primary", use_container_width=True)

    if submitted:
        if not all(value.strip() for value in (project_name, audience, problem, delightful_detail)):
            st.error("Add a project name, audience, problem, and delightful detail so Spark can make this yours.")
        elif provider == "Amazon Bedrock" and (not model_id.strip() or not region.strip()):
            st.error("For Bedrock mode, enter both an AWS Region and a model or inference profile ID.")
        else:
            try:
                with st.spinner("Spark is sketching the smallest useful version…"):
                    plan = generate_plan(
                        project_name=project_name.strip(),
                        audience=audience.strip(),
                        problem=problem.strip(),
                        delightful_detail=delightful_detail.strip(),
                        use_bedrock=provider == "Amazon Bedrock",
                        region=region.strip(),
                        model_id=model_id.strip(),
                    )
                st.session_state["plan"] = plan
                st.session_state["brief"] = {
                    "project_name": project_name.strip(),
                    "audience": audience.strip(),
                    "problem": problem.strip(),
                    "delightful_detail": delightful_detail.strip(),
                }
                st.session_state.pop("article", None)
            except (BotoCoreError, ClientError) as exc:
                st.error(f"Amazon Bedrock could not complete this request: {exc}")
                st.info("Check your AWS credentials, region, model access, and bedrock:InvokeModel permission, then try again.")
            except ValueError as exc:
                st.error(str(exc))

with right:
    st.subheader("The shape of the experience")
    st.markdown(
        """
        <div class="soft-card">
          <span class="pill">Small by design</span>
          <p><strong>Your idea, translated into a first build.</strong><br><br>
          Spark identifies the core user task, suggests a short implementation path, and recommends only the AWS services that match your description.</p>
          <br><span class="pill">Honest about AWS</span>
          <p>Try the complete experience locally. Bedrock is optional. The AWS architecture below is a proposal—not infrastructure this project has deployed.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

if st.session_state.get("plan"):
    st.write("")
    st.markdown("---")
    heading_col, action_col = st.columns([1, 0.26], vertical_alignment="center")
    with heading_col:
        st.subheader("Your project blueprint")
    with action_col:
        if st.button("🗑 Discard plan", key="discard_plan", type="secondary", use_container_width=True):
            st.session_state["confirm_discard"] = True

    if st.session_state.get("confirm_discard"):
        st.warning("Discard this plan and its article draft?")
        confirm_col, keep_col, _ = st.columns([0.22, 0.2, 0.58])
        with confirm_col:
            if st.button("Yes, discard", key="confirm_discard_plan", type="secondary"):
                st.session_state.pop("plan", None)
                st.session_state.pop("brief", None)
                st.session_state.pop("article", None)
                st.session_state.pop("confirm_discard", None)
                st.toast("Plan discarded. Your idea is ready for another try.")
                st.rerun()
        with keep_col:
            if st.button("Keep it", key="keep_discarded_plan", type="secondary"):
                st.session_state.pop("confirm_discard", None)
                st.rerun()

    st.markdown(st.session_state["plan"])
    st.caption("The AWS services described here are a proposed next step. This local prototype does not create AWS resources.")

    st.write("")
    tab_plan, tab_article = st.tabs(["🧭 Build plan", "✍️ Builder Center draft"])
    with tab_plan:
        st.markdown(
            '<div class="soft-card"><strong>Tailored suggestions, not deployment.</strong><p>The service recommendations above are inferred from your idea. Treat them as a starting point, then verify fit, availability, and cost before building. Spark does not create AWS resources or upload your idea in local preview.</p></div>',
            unsafe_allow_html=True,
        )
    with tab_article:
        brief = st.session_state.get("brief", {})
        st.markdown("Draft an article about the project in your brief, not just about Spark.")
        st.caption("The draft starts with your project title and description, then explains the proposed AWS workflow and what each suggested service does. AWS services are proposals, not deployed resources.")
        if st.button("Write my project article (500–800 words)", type="primary"):
            try:
                with st.spinner("Writing a story you can make your own…"):
                    st.session_state["article"] = generate_article(
                        brief=brief,
                        plan=st.session_state["plan"],
                        use_bedrock=provider == "Amazon Bedrock",
                        region=region.strip(),
                        model_id=model_id.strip(),
                    )
            except (BotoCoreError, ClientError) as exc:
                st.error(f"Amazon Bedrock could not draft the article: {exc}")
                st.info("Check your AWS credentials, region, model access, and bedrock:InvokeModel permission, then try again.")
            except ValueError as exc:
                st.error(str(exc))
        article = st.session_state.get("article")
        if article:
            word_count = len(article.split())
            st.metric("Draft word count", word_count, delta="Within 800-word limit" if word_count <= 800 else "Over the requested limit")
            if word_count > 800:
                st.error("This draft exceeds 800 words. Regenerate it in Bedrock mode or shorten it before publishing.")
            if word_count < 500:
                st.warning("This draft is under the challenge's 500-word minimum. Add detail before publishing.")
            st.markdown(article)
            st.download_button(
                "Download article as Markdown",
                data=article,
                file_name="builder-center-article.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            st.info("Your draft will use your project name as its title, describe the project and audience, and explain the architecture flow and proposed AWS services with relevant tags.")

st.markdown(
    '<div class="footer">Built for builders who want a little less blank page and a little more “I shipped it.”</div>',
    unsafe_allow_html=True,
)
