# 🏥 AI Clinical Response Assistant

An AI-powered system that assists hospital staff by generating **draft responses to patient queries** while allowing **human review and editing before sending**.

The system analyzes patient symptoms and vital signs, retrieves medical knowledge from the MedQuAD dataset, and suggests clinically relevant responses.

---

# 🚀 Project Overview

Hospitals receive a large number of patient queries every day. Responding to them manually can be time-consuming.

This system provides **AI-assisted response suggestions** that help medical staff reply faster while ensuring that final decisions remain under human supervision.

---

# 🎯 Problem Statement

Develop a system that assists hospital staff by suggesting **draft responses to patient queries**.

Requirements:

- AI suggests responses
- Staff reviews and edits before sending
- Supports medical knowledge retrieval
- Provides patient vitals analysis

---

# 🧠 System Architecture
Patient Query
↓
Sentence Transformer Model
↓
Vector Search (FAISS)
↓
MedQuAD Medical Knowledge Base
↓
AI Draft Response
↓
Doctor Review Panel
↓
Send Response to Patient


---

# ✨ Key Features

### 🤖 AI Response Suggestions
- Uses semantic search with Sentence Transformers
- Retrieves relevant medical knowledge
- Generates concise clinical draft responses

### 🩺 Patient Vital Monitoring
- Heart Rate
- Temperature
- Oxygen Saturation
- Blood Pressure
- Respiratory Rate
- BMI calculation

### ⚠ Clinical Alerts
Detects abnormal vitals and provides warnings.

Examples:

- High heart rate
- Fever detection
- Low oxygen levels

### 📊 Interactive Health Visualizations
- Patient vs Normal Vital Comparison
- Heart Rate Trend Graphs

### 👨‍⚕ Human Review System
Doctors can:
- Review AI response
- Edit the response
- Send the final message to patients

---


---

# ✨ Key Features

### 🤖 AI Response Suggestions
- Uses semantic search with Sentence Transformers
- Retrieves relevant medical knowledge
- Generates concise clinical draft responses

### 🩺 Patient Vital Monitoring
- Heart Rate
- Temperature
- Oxygen Saturation
- Blood Pressure
- Respiratory Rate
- BMI calculation

### ⚠ Clinical Alerts
Detects abnormal vitals and provides warnings.

Examples:

- High heart rate
- Fever detection
- Low oxygen levels

### 📊 Interactive Health Visualizations
- Patient vs Normal Vital Comparison
- Heart Rate Trend Graphs

### 👨‍⚕ Human Review System
Doctors can:
- Review AI response
- Edit the response
- Send the final message to patients


---

# 🛠 Tech Stack

Frontend  
- React
- Tailwind CSS
- Chart.js / Plotly

Backend  
- FastAPI
- Python

AI & Data  
- Sentence Transformers
- FAISS Vector Search
- MedQuAD Medical Dataset

---


The AI system will suggest a draft response for staff review.

---

# 📊 Example Dashboard

The system provides:

- Vital monitoring
- AI response suggestions
- Clinical alerts
- Interactive health graphs

---

# ⚠ Disclaimer

This system is designed to assist healthcare professionals and **should not replace medical judgment**.

All AI responses must be reviewed by qualified staff.

---

# 👨‍💻 Authors

Developed as part of a healthcare AI hackathon project.

---

# 📜 License

MIT License

