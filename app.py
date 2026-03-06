import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="AI Clinical Assistant", layout="wide")

# --------------------------------------------------
# UI STYLE
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
padding:18px;
border-radius:12px;
box-shadow:0 4px 14px rgba(0,0,0,0.25);
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

.response-box{
background:white;
padding:20px;
border-radius:12px;
color:black;
box-shadow:0 4px 14px rgba(0,0,0,0.2);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🏥 AI Clinical Response Assistant")
st.caption("AI powered support system for hospital staff")

# --------------------------------------------------
# LOAD DATA
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
# MODEL
# --------------------------------------------------

@st.cache_resource
def load_model():
    return SentenceTransformer("paraphrase-MiniLM-L3-v2")

model = load_model()

# --------------------------------------------------
# FAISS INDEX
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
oxygen = st.sidebar.slider("Oxygen",70,100,98)
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
# PATIENT QUERY
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

    st.markdown("<div class='response-box'>", unsafe_allow_html=True)

    st.subheader("🤖 AI Suggested Response")
    st.write(response)
    st.metric("AI Confidence Score", round(confidence,2))

    st.markdown("</div>", unsafe_allow_html=True)

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
# RISK SCORE GAUGE
# --------------------------------------------------

    risk = 0

    if heart_rate > 120:
        risk += 30

    if oxygen < 92:
        risk += 40

    if temperature > 38:
        risk += 20

    if bp > 140:
        risk += 10

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={'text': "Patient Risk Score"},
        gauge={
            'axis': {'range': [0,100]},
            'bar': {'color': "red"},
            'steps': [
                {'range':[0,30],'color':'green'},
                {'range':[30,70],'color':'yellow'},
                {'range':[70,100],'color':'red'}
            ]
        }
    ))

    st.plotly_chart(fig_gauge, use_container_width=True)

# --------------------------------------------------
# VITAL COMPARISON
# --------------------------------------------------

    st.subheader("Patient vs Normal Vitals")

    categories = ["Heart Rate","Temperature","Oxygen","Respiratory"]

    patient_values = [heart_rate,temperature,oxygen,resp]
    normal_values = [75,37,98,16]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=categories,
        y=normal_values,
        name="Normal"
    ))

    fig.add_trace(go.Bar(
        x=categories,
        y=patient_values,
        name="Patient"
    ))

    fig.update_layout(template="plotly_dark")

    st.plotly_chart(fig,use_container_width=True)

# --------------------------------------------------
# HEART RATE MONITOR
# --------------------------------------------------

    st.subheader("Heart Rate Monitor Simulation")

    time = np.arange(0,60)

    hr_data = heart_rate + np.sin(time/3)*5 + np.random.normal(0,1,len(time))

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=time,
        y=hr_data,
        mode='lines',
        line=dict(width=3)
    ))

    fig2.update_layout(
        template="plotly_dark",
        xaxis_title="Time",
        yaxis_title="Heart Rate"
    )

    st.plotly_chart(fig2,use_container_width=True)

# --------------------------------------------------
# DOCTOR REVIEW PANEL
# --------------------------------------------------

    st.subheader("Doctor Review")

    edited = st.text_area(
        "Edit response before sending",
        response,
        height=160
    )

    if st.button("Send Response"):
        st.success("Response sent to patient successfully")