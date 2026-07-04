import streamlit as st
import requests

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🩺",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.main{
    background:#f5f7fb;
}

.title{
    font-size:42px;
    font-weight:700;
    text-align:center;
    color:#1f4e79;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

.stButton>button{
    width:100%;
    background:linear-gradient(90deg,#2563eb,#3b82f6);
    color:white;
    border-radius:12px;
    border:none;
    height:50px;
    font-size:18px;
    font-weight:bold;
}

.metric-card{
    background:white;
    padding:18px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 2px 10px rgba(0,0,0,0.1);
}

.result{
    padding:25px;
    border-radius:15px;
    text-align:center;
    font-size:28px;
    font-weight:bold;
}

.high{
    background:#ffebee;
    color:#c62828;
}

.medium{
    background:#fff8e1;
    color:#ef6c00;
}

.low{
    background:#e8f5e9;
    color:#2e7d32;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Title ---------------- #

st.markdown("<div class='title'>🏥 Insurance Premium Predictor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Predict whether your insurance premium is Low, Medium or High using Machine Learning.</div>", unsafe_allow_html=True)

# ---------------- Layout ---------------- #

col1,col2=st.columns([2,1])

with col1:

    age=st.slider("Age",18,80,25)

    sex=st.selectbox(
        "Gender",
        ["male","female"]
    )

    weight=st.number_input(
        "Weight (kg)",
        min_value=30.0,
        max_value=200.0,
        value=70.0
    )

    height=st.number_input(
        "Height (cm)",
        min_value=120.0,
        max_value=220.0,
        value=170.0
    )

    smoker=st.selectbox(
        "Smoker",
        ["no","yes"]
    )

    region=st.selectbox(
        "Region",
        [
            "northwest",
            "northeast",
            "southwest",
            "southeast"
        ]
    )

with col2:

    bmi=weight/((height/100)**2)

    st.markdown(f"""<div style="background:white;padding:20px;border-radius:15px;box-shadow:0 4px 12px rgba(0,0,0,.1);text-align:center;"><h3 style="color:#555;">BMI</h3><h1 style="color:#2563eb;">{bmi:.2f}</h1></div>""", unsafe_allow_html=True)

    if bmi<18.5:
        bmi_status="Underweight"

    elif bmi<25:
        bmi_status="Healthy"

    elif bmi<30:
        bmi_status="Overweight"

    else:
        bmi_status="Obese"

    st.markdown(f"""<div style="background:white;padding:20px;border-radius:15px;box-shadow:0 4px 12px rgba(0,0,0,.1);text-align:center;margin-top:20px;"><h3 style="color:#555;">BMI Status</h3><h2 style="color:#111827;">{bmi_status}</h2></div>""", unsafe_allow_html=True)

    if smoker == "yes" and bmi_status in ["Overweight", "Obese"]:
        lifestyle_risk = "High"
        lifestyle_note = "Smoking and BMI may increase risk."
    elif smoker == "yes" or bmi_status in ["Overweight", "Obese"]:
        lifestyle_risk = "Moderate"
        lifestyle_note = "One or more risk factors are present."
    else:
        lifestyle_risk = "Low"
        lifestyle_note = "Current lifestyle inputs look healthier."

    st.markdown(f"""<div style="background:white;padding:20px;border-radius:15px;box-shadow:0 4px 12px rgba(0,0,0,.1);text-align:center;margin-top:20px;"><h3 style="color:#555;">Lifestyle Risk</h3><h2 style="color:#111827;">{lifestyle_risk}</h2><p style="color:#6b7280;margin:0;">{lifestyle_note}</p></div>""", unsafe_allow_html=True)

# ---------------- Predict ---------------- #

if st.button("Predict Premium"):

    payload={

        "age":age,
        "sex":sex,
        "weight_kg":weight,
        "height_cm":height,
        "smoker":smoker,
        "region":region

    }

    with st.spinner("Predicting..."):

        response = requests.post(
            "https://insurance-premium-api-8l5n.onrender.com/predict",
            json=payload
        )

    if response.status_code==200:

        prediction=response.json()["predicted_category"]

        if prediction=="High Premium":

            css="high"

            emoji="🔴"

        elif prediction=="Medium Premium":

            css="medium"

            emoji="🟡"

        else:

            css="low"

            emoji="🟢"

        st.markdown(f"""
        <br>
        <div class="result {css}">
        {emoji}<br><br>

        Predicted Insurance Premium

        <br><br>

        {prediction}

        </div>
        """,unsafe_allow_html=True)

    else:

        st.error("Could not connect to FastAPI.")