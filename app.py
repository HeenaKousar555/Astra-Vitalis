
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import IsolationForest
from datetime import datetime

# =========================================================
# ASTRA VITALIS | ASTRONAUT HEALTH INTELLIGENCE SYSTEM
# SOLVYRIS| SPACE HEALTH RESEARCH DIVISION
# =========================================================

st.set_page_config(
    page_title="ASTRA VITALIS | Mission Health",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- COSMIC DESIGN -----------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #080817, #11102b, #17112f);
    color: #eeeaff;
}
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #c8a7ff !important;
}
p, label, span {
    font-family: 'Inter', sans-serif;
}
[data-testid="stMetric"] {
    background: rgba(115, 78, 180, 0.12);
    border: 1px solid rgba(180, 140, 255, 0.25);
    padding: 17px;
    border-radius: 12px;
}
[data-testid="stMetricValue"] {
    color: #d6c0ff;
}
section[data-testid="stSidebar"] {
    background: #0c0b20;
    border-right: 1px solid #39305b;
}
.stButton button, .stFormSubmitButton button {
    background: #7445bb;
    color: white;
    border-radius: 9px;
    border: none;
}
.stButton button:hover, .stFormSubmitButton button:hover {
    background: #9365dc;
    color: white;
}
div[role="radiogroup"] label {
    background: rgba(115, 78, 180, 0.10);
    padding: 9px 12px;
    border-radius: 8px;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)


# -------------------- SIMULATED DATA ----------------------

@st.cache_data
def generate_health_data():

    rng = np.random.default_rng(42)
    days = 30

    data = pd.DataFrame({
        "Mission Day": np.arange(1, days + 1),
        "Heart Rate": rng.normal(72, 5, days),
        "Sleep Hours": rng.normal(7.5, 0.7, days),
        "Activity Minutes": rng.normal(65, 12, days),
        "Stress Score": rng.normal(3, 0.8, days),
        "SpO2": rng.normal(97, 1, days)
    })

    # Illustrative unusual events
    data.loc[8, "Heart Rate"] = 112
    data.loc[8, "Sleep Hours"] = 4.1
    data.loc[17, "Stress Score"] = 8.5
    data.loc[23, "Activity Minutes"] = 15
    data.loc[26, "SpO2"] = 90

    return data.round(2)


# -------------------- ANOMALY MODEL -----------------------

def detect_anomalies(data):

    features = [
        "Heart Rate",
        "Sleep Hours",
        "Activity Minutes",
        "Stress Score",
        "SpO2"
    ]

    model = IsolationForest(
        contamination=0.12,
        random_state=42,
        n_estimators=150
    )

    result = data.copy()
    result["Anomaly"] = model.fit_predict(
        result[features]
    ) == -1

    return result


# -------------------- CHART HELPER -----------------------

def create_line_chart(data, column, title, y_title, color):

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data["Mission Day"],
        y=data[column],
        mode="lines+markers",
        name=column,
        line=dict(color=color, width=3),
        marker=dict(size=7)
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Mission Day",
        yaxis_title=y_title,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(20,15,42,0.5)",
        margin=dict(l=20, r=20, t=55, b=20)
    )

    return fig


# -------------------- SESSION STATE -----------------------

if "checkins" not in st.session_state:
    st.session_state.checkins = []


# -------------------- SIDEBAR NAVIGATION ------------------

st.sidebar.markdown("# ASTRA VITALIS")
st.sidebar.caption("MISSION CONTROL INTERFACE")
st.sidebar.divider()

astronaut = st.sidebar.selectbox(
    "SELECT CREW MEMBER",
    [
        "Astronaut A-01",
        "Astronaut A-02",
        "Astronaut A-03"
    ]
)

mission_day = st.sidebar.slider(
    "MISSION DAY",
    min_value=1,
    max_value=30,
    value=30
)

st.sidebar.divider()

st.sidebar.markdown("### SYSTEM MODULES")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Mission Overview",
        "Cardiovascular Monitoring",
        "Sleep Monitoring",
        "Activity Monitoring",
        "Behavioral Health",
        "AI Anomaly Detection",
        "Astronaut Daily Check-in",
        "NASA Research Archive"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.caption("SOLVYRIS")
st.sidebar.caption("DEEP SPACE RESEARCH DIVISION")


# -------------------- PROCESS DATA ------------------------

raw_data = generate_health_data()

# Illustrative crew profile variations
if astronaut == "Astronaut A-02":
    raw_data["Heart Rate"] += 2

elif astronaut == "Astronaut A-03":
    raw_data["Sleep Hours"] -= 0.3

data = detect_anomalies(raw_data)

visible_data = data[
    data["Mission Day"] <= mission_day
].copy()

latest = visible_data.iloc[-1]
anomaly_count = int(visible_data["Anomaly"].sum())


# -------------------- COMMON HEADER -----------------------

st.markdown("""
# ASTRA VITALIS
### ASTRONAUT HEALTH INTELLIGENCE SYSTEM

**SOLVYRIS | SPACE HEALTH RESEARCH DIVISION**

Monitoring human health beyond Earth.
""")

st.caption(
    "MISSION STATUS: ACTIVE  |  PROTOTYPE VERSION 2.0  |  "
    "DATA MODE: SIMULATED"
)

st.divider()


# =========================================================
# PAGE 1: MISSION OVERVIEW
# =========================================================

if page == "Mission Overview":

    st.markdown("## CREW HEALTH OVERVIEW")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Heart Rate",
        f"{latest['Heart Rate']:.1f} bpm"
    )

    c2.metric(
        "Sleep Duration",
        f"{latest['Sleep Hours']:.1f} hrs"
    )

    c3.metric(
        "Activity",
        f"{latest['Activity Minutes']:.0f} min"
    )

    c4.metric(
        "SpO2",
        f"{latest['SpO2']:.1f}%"
    )

    st.caption(
        "All readings are simulated for software demonstration. "
        "They are not real astronaut measurements."
    )

    st.divider()

    st.markdown("## MISSION HEALTH INTELLIGENCE")

    left, right = st.columns(2)

    with left:
        st.markdown("### PATTERN ANALYSIS")

        if latest["Anomaly"]:
            st.warning(
                "Unusual measurement pattern detected. "
                "Review the recorded indicators."
            )
        else:
            st.success(
                "No unusual pattern detected in the latest record."
            )

        st.metric("Flagged Records", anomaly_count)

    with right:
        st.markdown("### MONITORING SUMMARY")

        st.write(f"**Crew Member:** {astronaut}")
        st.write(f"**Mission Day:** {mission_day}")
        st.write(f"**Records Analyzed:** {len(visible_data)}")
        st.write("**Detection Engine:** Isolation Forest")
        st.write("**Monitoring Status:** Active")

    st.divider()

    st.markdown("## PHYSIOLOGICAL DATA TIMELINE")

    tab1, tab2, tab3 = st.tabs([
        "Cardiovascular",
        "Sleep & Activity",
        "Behavioral Health"
    ])

    with tab1:
        st.plotly_chart(
            create_line_chart(
                visible_data,
                "Heart Rate",
                "Heart Rate Over Mission Duration",
                "Heart Rate (BPM)",
                "#bd91ff"
            ),
            use_container_width=True
        )

        st.plotly_chart(
            create_line_chart(
                visible_data,
                "SpO2",
                "Oxygen Saturation Trend",
                "SpO2 (%)",
                "#55d9e9"
            ),
            use_container_width=True
        )

    with tab2:
        st.plotly_chart(
            create_line_chart(
                visible_data,
                "Sleep Hours",
                "Sleep Duration",
                "Hours",
                "#9b8cff"
            ),
            use_container_width=True
        )

        fig = px.bar(
            visible_data,
            x="Mission Day",
            y="Activity Minutes",
            title="Daily Physical Activity",
            template="plotly_dark",
            color="Activity Minutes",
            color_continuous_scale="Purples"
        )

        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.plotly_chart(
            create_line_chart(
                visible_data,
                "Stress Score",
                "Daily Self-Reported Stress Indicator",
                "Illustrative Stress Score",
                "#ff9bba"
            ),
            use_container_width=True
        )


# =========================================================
# PAGE 2: CARDIOVASCULAR MONITORING
# =========================================================

elif page == "Cardiovascular Monitoring":

    st.markdown("## ♥ CARDIOVASCULAR MONITORING")

    st.write(
        "Explore simulated cardiovascular indicators "
        "across the mission timeline."
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Latest Heart Rate",
        f"{latest['Heart Rate']:.1f} BPM"
    )

    c2.metric(
        "Latest SpO2",
        f"{latest['SpO2']:.1f}%"
    )

    st.divider()

    st.plotly_chart(
        create_line_chart(
            visible_data,
            "Heart Rate",
            "HEART RATE TIMELINE",
            "Beats per minute",
            "#bd91ff"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        create_line_chart(
            visible_data,
            "SpO2",
            "OXYGEN SATURATION TIMELINE",
            "SpO2 (%)",
            "#55d9e9"
        ),
        use_container_width=True
    )

    st.markdown("### RECORDED MEASUREMENTS")

    st.dataframe(
        visible_data[
            ["Mission Day", "Heart Rate", "SpO2", "Anomaly"]
        ],
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 3: SLEEP MONITORING
# =========================================================

elif page == "Sleep Monitoring":

    st.markdown("## ◉ SLEEP MONITORING")

    st.write(
        "Review sleep-duration patterns during the simulated mission."
    )

    average_sleep = visible_data["Sleep Hours"].mean()

    c1, c2 = st.columns(2)

    c1.metric(
        "Latest Sleep",
        f"{latest['Sleep Hours']:.1f} hours"
    )

    c2.metric(
        "Mission Average",
        f"{average_sleep:.1f} hours"
    )

    st.divider()

    st.plotly_chart(
        create_line_chart(
            visible_data,
            "Sleep Hours",
            "SLEEP DURATION TIMELINE",
            "Hours",
            "#9b8cff"
        ),
        use_container_width=True
    )

    st.markdown("### SLEEP RECORDS")

    st.dataframe(
        visible_data[
            ["Mission Day", "Sleep Hours", "Anomaly"]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Sleep readings are simulated. This prototype does not "
        "measure sleep stages or diagnose sleep disorders."
    )


# =========================================================
# PAGE 4: ACTIVITY MONITORING
# =========================================================

elif page == "Activity Monitoring":

    st.markdown("## ⌁ ACTIVITY MONITORING")

    average_activity = visible_data["Activity Minutes"].mean()

    c1, c2 = st.columns(2)

    c1.metric(
        "Latest Activity",
        f"{latest['Activity Minutes']:.0f} minutes"
    )

    c2.metric(
        "Mission Average",
        f"{average_activity:.1f} minutes"
    )

    st.divider()

    fig = px.bar(
        visible_data,
        x="Mission Day",
        y="Activity Minutes",
        title="DAILY ACTIVITY TIMELINE",
        template="plotly_dark",
        color="Activity Minutes",
        color_continuous_scale="Purples"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### ACTIVITY RECORDS")

    st.dataframe(
        visible_data[
            ["Mission Day", "Activity Minutes", "Anomaly"]
        ],
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 5: BEHAVIORAL HEALTH
# =========================================================

elif page == "Behavioral Health":

    st.markdown("## ✧ BEHAVIORAL HEALTH")

    st.write(
        "Explore the illustrative self-reported stress indicator "
        "across the mission timeline."
    )

    c1, c2 = st.columns(2)

    c1.metric(
        "Latest Stress Score",
        f"{latest['Stress Score']:.1f}/10"
    )

    c2.metric(
        "Mission Average",
        f"{visible_data['Stress Score'].mean():.1f}/10"
    )

    st.divider()

    st.plotly_chart(
        create_line_chart(
            visible_data,
            "Stress Score",
            "SELF-REPORTED STRESS TIMELINE",
            "Illustrative score (1–10)",
            "#ff9bba"
        ),
        use_container_width=True
    )

    st.info(
        "This is a simulated self-report indicator, not a "
        "clinical mental-health assessment."
    )

    st.markdown("### CREW WELLBEING RECORDS")

    st.dataframe(
        visible_data[
            ["Mission Day", "Stress Score", "Sleep Hours", "Anomaly"]
        ],
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAGE 6: AI ANOMALY DETECTION
# =========================================================

elif page == "AI Anomaly Detection":

    st.markdown("## ⚠ AI ANOMALY DETECTION CENTER")

    st.write(
        "Isolation Forest identifies records with unusual "
        "combinations of simulated health measurements."
    )

    c1, c2 = st.columns(2)

    c1.metric("Records Analyzed", len(visible_data))
    c2.metric("Flagged Records", anomaly_count)

    st.divider()

    anomalies = visible_data[
        visible_data["Anomaly"]
    ]

    if not anomalies.empty:

        st.warning(
            f"{len(anomalies)} unusual records identified for review."
        )

        st.dataframe(
            anomalies,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success(
            "No unusual records flagged in this mission period."
        )

    st.markdown("### MODEL INFORMATION")

    st.write("**Algorithm:** Isolation Forest")
    st.write("**Estimators:** 150")
    st.write("**Contamination setting:** 0.12")
    st.write("**Input indicators:** Heart Rate, Sleep, Activity, Stress, SpO2")

    st.caption(
        "Anomaly flags indicate statistical unusualness within "
        "this simulated dataset. They are not medical alerts "
        "or diagnoses."
    )


# =========================================================
# PAGE 7: ASTRONAUT DAILY CHECK-IN
# =========================================================

elif page == "Astronaut Daily Check-in":

    st.markdown("## 🚀 ASTRONAUT DAILY CHECK-IN")

    st.write(
        "Enter a self-reported health record for the selected crew member."
    )

    with st.form("health_checkin"):

        heart_rate = st.number_input(
            "Heart Rate (BPM)",
            min_value=30,
            max_value=220,
            value=72
        )

        spo2 = st.number_input(
            "SpO2 (%)",
            min_value=50.0,
            max_value=100.0,
            value=97.0
        )

        sleep = st.number_input(
            "Sleep Duration (Hours)",
            min_value=0.0,
            max_value=24.0,
            value=7.5
        )

        activity = st.number_input(
            "Activity (Minutes)",
            min_value=0,
            max_value=1440,
            value=60
        )

        stress = st.slider(
            "Self-reported Stress",
            min_value=1,
            max_value=10,
            value=3
        )

        symptoms = st.text_area(
            "Symptoms or Additional Notes",
            placeholder="Enter any observations..."
        )

        submitted = st.form_submit_button(
            "SUBMIT HEALTH CHECK-IN",
            use_container_width=True
        )

        if submitted:

            st.session_state.checkins.append({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Crew": astronaut,
                "Mission Day": mission_day,
                "Heart Rate": heart_rate,
                "SpO2": spo2,
                "Sleep Hours": sleep,
                "Activity Minutes": activity,
                "Stress Score": stress,
                "Notes": symptoms
            })

            st.success("Health check-in recorded successfully.")

    st.divider()

    st.markdown("### RECENT CHECK-IN RECORDS")

    if st.session_state.checkins:

        checkin_data = pd.DataFrame(
            st.session_state.checkins
        )

        st.dataframe(
            checkin_data,
            use_container_width=True,
            hide_index=True
        )

        csv_data = checkin_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            "DOWNLOAD CHECK-IN RECORDS",
            data=csv_data,
            file_name="astra_vitalis_checkins.csv",
            mime="text/csv"
        )

    else:
        st.info(
            "No check-ins recorded yet. Submit your first entry above."
        )


# ------------------------------------------------
# NASA RESEARCH ARCHIVE
# ------------------------------------------------

elif page == "NASA Research Archive":

    st.markdown("## NASA RESEARCH ARCHIVE")
    st.markdown("### OSD-575 | INSPIRATION4 BLOOD SERUM ANALYSIS")

    st.write(
        "Exploratory analysis of publicly available NASA "
        "Open Science Data Repository blood-serum data."
    )

    st.info(
        "This is a separate laboratory research dataset. "
        "It is not live wearable data and is not connected "
        "to the simulated Isolation Forest monitoring model."
    )

    @st.cache_data
    def load_nasa_cmp():
        return pd.read_csv("nasa_research/OSD575_CMP.csv")

    try:
        nasa = load_nasa_cmp().copy()

        # Extract participant and sample timepoint
        nasa["Participant"] = nasa["Sample Name"].str.extract(
            r"(C\d{3})"
        )

        nasa["Timepoint"] = nasa["Sample Name"].str.extract(
            r"(L-\d+|R\+\d+)"
        )

        time_order = [
            "L-92", "L-44", "L-3",
            "R+1", "R+45", "R+82", "R+194"
        ]

        nasa["Timepoint"] = pd.Categorical(
            nasa["Timepoint"],
            categories=time_order,
            ordered=True
        )

        nasa = nasa.sort_values(
            ["Participant", "Timepoint"]
        )

        # Measurement configuration
        measurements = {
            "Glucose": {
                "value": "glucose_value_milligram_per_deciliter",
                "min": "glucose_range_min_milligram_per_deciliter",
                "max": "glucose_range_max_milligram_per_deciliter",
                "unit": "mg/dL",
                "color": "#55d9e9"
            },
            "Albumin": {
                "value": "albumin_value_gram_per_deciliter",
                "min": "albumin_range_min_gram_per_deciliter",
                "max": "albumin_range_max_gram_per_deciliter",
                "unit": "g/dL",
                "color": "#bd91ff"
            },
            "Creatinine": {
                "value": "creatinine_value_milligram_per_deciliter",
                "min": "creatinine_range_min_milligram_per_deciliter",
                "max": "creatinine_range_max_milligram_per_deciliter",
                "unit": "mg/dL",
                "color": "#ff9bba"
            },
            "Sodium": {
                "value": "sodium_value_millimol_per_liter",
                "min": "sodium_range_min_millimol_per_liter",
                "max": "sodium_range_max_millimol_per_liter",
                "unit": "mmol/L",
                "color": "#a78bfa"
            }
        }

        # ------------------------------------------------
        # DATASET OVERVIEW
        # ------------------------------------------------

        st.divider()
        st.markdown("### DATASET OVERVIEW")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Samples", len(nasa))
        c2.metric(
            "Participants",
            nasa["Participant"].nunique()
        )
        c3.metric("Timepoints", nasa["Timepoint"].nunique())
        c4.metric("Parameters Analysed", len(measurements))

        st.write("**Source:** NASA Open Science Data Repository — OSD-575")
        st.write("**Mission:** SpaceX Inspiration4")
        st.write("**Data type:** Blood serum Comprehensive Metabolic Panel")

        st.markdown(
            "[Open original NASA OSD-575 dataset](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575)"
        )

        # ------------------------------------------------
        # COMPLETE REFERENCE RANGE AUDIT
        # ------------------------------------------------

        review_rows = []

        for name, cfg in measurements.items():

            for _, row in nasa.iterrows():

                value = pd.to_numeric(
                    row[cfg["value"]], errors="coerce"
                )

                lower = pd.to_numeric(
                    row[cfg["min"]], errors="coerce"
                )

                upper = pd.to_numeric(
                    row[cfg["max"]], errors="coerce"
                )

                if pd.isna(value):
                    status = "Missing measurement"

                elif pd.isna(lower) or pd.isna(upper):
                    status = "Reference range unavailable"

                elif value < lower:
                    status = "Below reference range"

                elif value > upper:
                    status = "Above reference range"

                else:
                    status = "Within reference range"

                review_rows.append({
                    "Participant": row["Participant"],
                    "Timepoint": str(row["Timepoint"]),
                    "Measurement": name,
                    "Value": value,
                    "Unit": cfg["unit"],
                    "Reference Min": lower,
                    "Reference Max": upper,
                    "Review": status
                })

        review = pd.DataFrame(review_rows)

        flagged = review[
            review["Review"].isin([
                "Below reference range",
                "Above reference range"
            ])
        ]

        # ------------------------------------------------
        # RESEARCH FINDINGS
        # ------------------------------------------------

        st.divider()
        st.markdown("### RESEARCH FINDINGS")

        f1, f2, f3, f4 = st.columns(4)

        f1.metric("Total Comparisons", len(review))
        f2.metric("Within Range", int(
            (review["Review"] == "Within reference range").sum()
        ))
        f3.metric("Below Range", int(
            (review["Review"] == "Below reference range").sum()
        ))
        f4.metric("Above Range", int(
            (review["Review"] == "Above reference range").sum()
        ))

        summary_rows = []

        for name in measurements:

            parameter_data = review[
                review["Measurement"] == name
            ]

            summary_rows.append({
                "Parameter": name,
                "Below Range": int(
                    (parameter_data["Review"] == "Below reference range").sum()
                ),
                "Within Range": int(
                    (parameter_data["Review"] == "Within reference range").sum()
                ),
                "Above Range": int(
                    (parameter_data["Review"] == "Above reference range").sum()
                ),
                "Missing": int(
                    (parameter_data["Review"] == "Missing measurement").sum()
                )
            })

        summary_df = pd.DataFrame(summary_rows)

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Comparisons use the reference limits supplied with "
            "each individual NASA dataset record."
        )

        # ------------------------------------------------
        # PARTICIPANT ANALYSIS
        # ------------------------------------------------

        st.divider()
        st.markdown("### PARTICIPANT ANALYSIS")

        participant = st.selectbox(
            "SELECT PARTICIPANT",
            sorted(nasa["Participant"].dropna().unique())
        )

        person = nasa[
            nasa["Participant"] == participant
        ].sort_values("Timepoint")

        st.caption(
            f"Displaying seven sample timepoints for participant {participant}."
        )

        # ------------------------------------------------
        # BLOOD CHEMISTRY TIMELINE
        # ------------------------------------------------

        st.markdown("### BLOOD CHEMISTRY TIMELINE")

        for name, cfg in measurements.items():

            fig = go.Figure()

            x_values = person["Timepoint"].astype(str)

            lower = pd.to_numeric(
                person[cfg["min"]], errors="coerce"
            )

            upper = pd.to_numeric(
                person[cfg["max"]], errors="coerce"
            )

            values = pd.to_numeric(
                person[cfg["value"]], errors="coerce"
            )

            # Reference minimum
            fig.add_trace(go.Scatter(
                x=x_values,
                y=lower,
                mode="lines",
                name="Reference minimum",
                line=dict(
                    color="rgba(85,217,233,0.55)",
                    width=1,
                    dash="dash"
                ),
                hovertemplate="Minimum: %{y}<extra></extra>"
            ))

            # Reference maximum and shaded band
            fig.add_trace(go.Scatter(
                x=x_values,
                y=upper,
                mode="lines",
                name="Reference maximum",
                line=dict(
                    color="rgba(85,217,233,0.55)",
                    width=1,
                    dash="dash"
                ),
                fill="tonexty",
                fillcolor="rgba(85,217,233,0.10)",
                hovertemplate="Maximum: %{y}<extra></extra>"
            ))

            # Identify out-of-range points
            marker_colors = []

            for value, low, high in zip(values, lower, upper):

                if pd.isna(value) or pd.isna(low) or pd.isna(high):
                    marker_colors.append("#a78bfa")

                elif value < low or value > high:
                    marker_colors.append("#ff657a")

                else:
                    marker_colors.append(cfg["color"])

            # Actual measurements
            fig.add_trace(go.Scatter(
                x=x_values,
                y=values,
                mode="lines+markers",
                name=name,
                connectgaps=False,
                line=dict(
                    color=cfg["color"],
                    width=3
                ),
                marker=dict(
                    size=10,
                    color=marker_colors,
                    line=dict(width=1, color="#ffffff")
                ),
                customdata=list(zip(lower, upper)),
                hovertemplate=(
                    "Timepoint: %{x}<br>"
                    "Measurement: %{y}<br>"
                    "Reference minimum: %{customdata[0]}<br>"
                    "Reference maximum: %{customdata[1]}"
                    "<extra></extra>"
                )
            ))

            fig.update_layout(
                title=f"{name} — {participant}",
                xaxis_title="Sample Timepoint",
                yaxis_title=cfg["unit"],
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(20,15,42,0.5)",
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=20, r=20, t=75, b=20)
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.caption(
            "The shaded band represents the recorded reference range. "
            "Pink markers identify measurements outside that range."
        )

        # ------------------------------------------------
        # REFERENCE RANGE REVIEW
        # ------------------------------------------------

        st.divider()
        st.markdown("### REFERENCE RANGE REVIEW")

        st.metric(
            "Out-of-range measurements across all participants",
            len(flagged)
        )

        st.dataframe(
            flagged,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Flags are based on dataset-provided reference limits. "
            "They are not medical diagnoses."
        )

        # ------------------------------------------------
        # DATA QUALITY
        # ------------------------------------------------

        st.divider()
        st.markdown("### DATA QUALITY & MISSING VALUES")

        original_columns = [
            col for col in nasa.columns
            if col not in ["Participant", "Timepoint"]
        ]

        missing = nasa[original_columns].isna().sum()
        missing = missing[missing > 0]

        if not missing.empty:

            missing_df = missing.reset_index()
            missing_df.columns = [
                "Column",
                "Missing Values"
            ]

            st.dataframe(
                missing_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.success("No missing values found in the dataset.")

        # ------------------------------------------------
        # RAW PARTICIPANT RECORDS
        # ------------------------------------------------

        st.divider()
        st.markdown("### RAW PARTICIPANT RECORDS")

        st.dataframe(
            person.drop(
                columns=["Participant", "Timepoint"]
            ),
            use_container_width=True,
            hide_index=True
        )

        # ------------------------------------------------
        # DOWNLOAD
        # ------------------------------------------------

        st.download_button(
            "DOWNLOAD NASA RESEARCH DATA",
            data=nasa.to_csv(index=False).encode("utf-8"),
            file_name="OSD575_CMP_research.csv",
            mime="text/csv"
        )

        st.download_button(
            "DOWNLOAD VALIDATION REPORT",
            data=review.to_csv(index=False).encode("utf-8"),
            file_name="OSD575_validation_report.csv",
            mime="text/csv"
        )

        # ------------------------------------------------
        # RESEARCH LIMITATIONS
        # ------------------------------------------------

        st.divider()
        st.markdown("### RESEARCH LIMITATIONS")

        st.write("""
        - Dataset contains four Inspiration4 participants.
        - Seven sample timepoints are available per participant.
        - Measurements represent blood-serum laboratory results,
          not continuous wearable readings.
        - Analysis is descriptive and exploratory.
        - Missing measurements and reference limits are preserved.
        - Findings cannot establish causation or clinical diagnosis.
        - The sample size is too small to generalize findings
          to the wider astronaut population.
        """)

        st.markdown(
            "**NASA Source:** "
            "[OSDR — OSD-575](https://osdr.nasa.gov/bio/repo/data/studies/OSD-575)"
        )

    except FileNotFoundError:
        st.error(
            "NASA dataset not found. Check that the file exists at "
            "nasa_research/OSD575_CMP.csv"
        )

    except Exception as e:
        st.error(f"Research archive error: {e}")



# -------------------- FOOTER -----------------------------

st.divider()

st.markdown("""
### ASTRA VITALIS | SOLVYRIS RESEARCH DIVISION

**EXPLORE. MONITOR. UNDERSTAND.**

A research prototype for astronaut health monitoring
during long-duration space missions.

*This prototype uses simulated data. Its anomaly flags are
not medical diagnoses, validated clinical alerts or substitutes
for professional medical assessment.*
""")

st.caption("ASTRA VITALIS — END OF SYSTEM INTERFACE")
