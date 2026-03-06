import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import plotly.graph_objects as go

st.set_page_config(page_title="AI Clinical Assistant", layout="wide")

# --------------------------------------------------
# MODERN UI STYLE
# --------------------------------------------------

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
background: linear-gradient(120deg,#0f2027,#203a43,#2c5364);
}

section[data-testid="stSidebar"]{
background:#0f172a;
}

.card{
background:white;
padding:20px;
border-radius:14px;
box-shadow:0px 6px 18px rgba(0,0,0,0.25);
}

.metric-title{
font-size:14px;
color:#555;
}

.metric-value{
font-size:30px;
font-weight:700;
color:#111;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏥 AI Clinical Response Assistant")
st.caption("AI powered support system for hospital staff")

# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("medquad_dataset.csv")
    df = df.dropna()
    return df

data = load_data()

questions = data["question"].tolist()
answers = data["answer"].tolist()

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("paraphrase-MiniLM-L3-v2")

model = load_model()

# --------------------------------------------------
# CREATE FAISS INDEX
# --------------------------------------------------

@st.cache_resource
def create_index():

    embeddings = model.encode(questions)
    embeddings = np.array(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index

index = create_index()

# --------------------------------------------------
# ANSWER SHORTENER
# --------------------------------------------------

def summarize_answer(text):

    sentences = text.split(".")
    short = ". ".join(sentences[:2])

    return short + "."

# --------------------------------------------------
# SIDEBAR PATIENT INPUT
# --------------------------------------------------

st.sidebar.header("Patient Vitals")

height = st.sidebar.slider("Height (cm)",120,210,170)
weight = st.sidebar.slider("Weight (kg)",30,150,70)

bmi = weight / ((height/100)**2)

st.sidebar.metric("BMI", round(bmi,2))

heart_rate = st.sidebar.slider("Heart Rate",40,160,80)
temperature = st.sidebar.slider("Temperature",35.0,41.0,37.0)
oxygen = st.sidebar.slider("Oxygen Saturation",70,100,98)
bp = st.sidebar.slider("Blood Pressure",80,180,120)
resp = st.sidebar.slider("Respiratory Rate",10,40,18)

# --------------------------------------------------
# VITAL CARDS
# --------------------------------------------------

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card">
    <div class="metric-title">❤️ Heart Rate</div>
    <div class="metric-value">{heart_rate} bpm</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
    <div class="metric-title">🫁 Oxygen</div>
    <div class="metric-value">{oxygen}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
    <div class="metric-title">🌡 Temperature</div>
    <div class="metric-value">{temperature} °C</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card">
    <div class="metric-title">🩸 Blood Pressure</div>
    <div class="metric-value">{bp}</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --------------------------------------------------
# PATIENT QUESTION
# --------------------------------------------------

st.subheader("💬 Patient Question")

query = st.text_input("Enter patient question")

if query:

    query_embedding = model.encode([query])
    D,I = index.search(np.array(query_embedding),k=1)

    idx = I[0][0]

    answer = summarize_answer(answers[idx])

    confidence = float(1/(1+D[0][0]))

    response = f"""
The symptoms described may indicate a condition associated with the patient's vital signs.

{answer}

Recommended actions:
• Monitor symptoms
• Maintain hydration
• Seek medical consultation if symptoms persist
"""

    st.subheader("🤖 AI Suggested Response")

    st.info(response)

    st.metric("AI Confidence Score", round(confidence,2))

    st.divider()

# --------------------------------------------------
# CLINICAL ALERTS
# --------------------------------------------------

    st.subheader("⚠ Clinical Alerts")

    if heart_rate > 120:
        st.error("High Heart Rate Detected")

    if oxygen < 92:
        st.error("Low Oxygen Level")

    if temperature > 38:
        st.warning("Fever Detected")

# --------------------------------------------------
# VITAL COMPARISON GRAPH
# --------------------------------------------------

    st.subheader("📊 Clinical Vital Comparison")

    categories = ["Heart Rate","Temperature","Oxygen","Respiratory"]

    patient_values = [heart_rate,temperature,oxygen,resp]
    normal_values = [75,37,98,16]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=normal_values,
        name="Normal Range",
        marker_color="#22c55e"
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=patient_values,
        name="Patient",
        marker_color="#ef4444"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=420,
        title="Patient vs Normal Vital Signs",
        margin=dict(l=20,r=20,t=40,b=20)
    )

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# HEART MONITOR SIMULATION
# --------------------------------------------------

    st.subheader("📈 Heart Rate Monitor")

    t = np.linspace(0,20,300)

    ecg = heart_rate + 4*np.sin(t*2) + np.random.normal(0,0.8,len(t))

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=t,
        y=ecg,
        mode="lines",
        line=dict(color="#00ff9c",width=3)
    ))

    fig2.update_layout(
        template="plotly_dark",
        height=350,
        xaxis_title="Time",
        yaxis_title="Heart Rate",
        title="Live Heart Rhythm Simulation"
    )

    st.plotly_chart(fig2,use_container_width=True)

# --------------------------------------------------
# DOCTOR REVIEW PANEL
# --------------------------------------------------

    st.subheader("👨‍⚕ Doctor Review Panel")

    edited = st.text_area(
        "Edit response before sending",
        response,
        height=160
    )

    if st.button("Send Response"):
        st.success("Response sent to patient successfully!")