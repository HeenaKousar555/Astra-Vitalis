
# ASTRA VITALIS 🚀
### Astronaut Health Intelligence System

**SOLVYRIS | Space Health Research Division**

ASTRA VITALIS is an astronaut health monitoring research prototype designed to explore physiological monitoring, behavioural wellbeing, and machine-learning-based anomaly detection during long-duration space missions.

The project combines an interactive Streamlit dashboard, NASA Inspiration4 blood chemistry data analysis, and controlled machine-learning experiments.

---

## 🌌 Project Features

### 1. Mission Overview
- Astronaut monitoring dashboard
- Mission-day tracking
- Crew profile selection
- Health indicator summaries

### 2. Cardiovascular Monitoring
- Heart rate monitoring
- Mission trend visualisation

### 3. Sleep Monitoring
- Sleep duration tracking
- Sleep trend analysis

### 4. Activity Monitoring
- Daily activity monitoring
- Activity trend visualisation

### 5. Behavioural Health
- Stress score monitoring
- Crew wellbeing records

### 6. AI Anomaly Detection
- Isolation Forest algorithm
- Statistical anomaly identification
- Monitoring indicators: heart rate, sleep, activity, stress and SpO2

### 7. Astronaut Daily Check-in
- Daily wellbeing entries
- SpO2 and personal observations
- CSV record export

### 8. NASA Research Archive
- NASA Inspiration4 blood serum dataset exploration
- Participant-wise blood chemistry visualisations
- Reference-range comparisons
- Missing-data investigation

---

## 🔬 Research Component

### NASA OSD-575 — Inspiration4

Dataset: SpaceX Inspiration4 Blood Serum Metabolic Panel and Immune/Cardiac Cytokine Arrays.

Source: https://osdr.nasa.gov/bio/repo/data/studies/OSD-575

Dataset overview:

| Description | Count |
|---|---:|
| Samples | 28 |
| Participants | 4 |
| Mission timepoints | 7 |
| Analysed parameters | 4 |

Parameters investigated:

- Glucose
- Albumin
- Creatinine
- Sodium

### Reference-Range Analysis

| Parameter | Below | Within | Above |
|---|---:|---:|---:|
| Glucose | 5 | 21 | 2 |
| Albumin | 0 | 28 | 0 |
| Creatinine | 0 | 27 | 1 |
| Sodium | 0 | 28 | 0 |
| **Total** | **5** | **104** | **3** |

A total of 112 parameter comparisons were performed.

These comparisons identify observations outside the reference intervals supplied with the dataset. They are not medical diagnoses.

---

## 🧠 Machine Learning Experiment

The project uses the Isolation Forest algorithm to investigate unusual patterns in simulated astronaut monitoring data.

**Model configuration:**
- Algorithm: Isolation Forest
- Estimators: 150
- Contamination: 0.12
- Random state: 42

**Input indicators:**
- Heart rate
- Sleep hours
- Activity minutes
- Stress score
- SpO2

The experiment introduces controlled unusual observations and evaluates model behaviour using precision, recall, F1-score and a confusion matrix.

The NASA blood chemistry dataset is analysed separately. It is not used to train or validate this Isolation Forest experiment.

---

## 📓 Research Notebook

`ASTRA_VITALIS_Research.ipynb`

The notebook documents:
- Dataset loading and exploration
- Missing-value analysis
- Blood chemistry visualisations
- Reference-range investigation
- Simulated monitoring data generation
- Isolation Forest experimentation
- Model evaluation
- Research findings and limitations

---

## 🛠️ Technology Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- Jupyter Notebook

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/HeenaKousar555/Astra-Vitalis.git
cd Astra-Vitalis
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the application

```bash
python -m streamlit run app.py
```

---

## 📁 Project Structure

```text
Astra-Vitalis/
│
├── app.py
├── ASTRA_VITALIS_Research.ipynb
├── README.md
├── .gitignore
├── requirements.txt
│
├── nasa_research/
│   ├── OSD575_CMP.csv
│   └── OSD575_validation_report.csv
│
└── research_outputs/
    ├── blood_chemistry_analysis.csv
    ├── anomaly_detection_results.csv
    └── feature_comparison.csv
```

---

## ⚠️ Research Limitations

- The NASA dataset contains 28 samples from four participants.
- The monitoring dashboard uses simulated physiological data.
- The Isolation Forest experiment uses simulated data.
- Reference-range deviations do not establish medical conditions.
- The model has not undergone clinical validation.
- The prototype is not intended for diagnosis or medical decision-making.

---

## 🔭 Future Scope

- Larger astronaut health datasets
- Personalised physiological baselines
- Multivariate time-series analysis
- Improved anomaly detection methods
- Integration with validated monitoring data sources
- Persistent crew monitoring records

---

## 👩‍🚀 Team

**SOLVYRIS**

Project: ASTRA VITALIS  
Research Area: Space Health Monitoring and Artificial Intelligence

**EXPLORE. MONITOR. UNDERSTAND.**
