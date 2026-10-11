from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd
from cancer_info import get_cancer_details

app = FastAPI(title="Q-Cancer AI API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def classify_age_group(age: int) -> str:
    if age <= 14:
        return "Child"
    elif age <= 24:
        return "Young"
    elif age <= 64:
        return "Adult"
    else:
        return "Older adult"

@app.get("/health")
def health_check():
    return {"status": "active", "message": "Q-Cancer Backend is running securely."}

@app.post("/predict")
async def predict_cancer(
    patient_id: str = Form(...),
    age: int = Form(...),
    sex: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Read uploaded genomic CSV
        contents = await file.read()
        from io import BytesIO
        df = pd.read_csv(BytesIO(contents))
        
        # Basic validation
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded genomic CSV file is empty.")

        # Determine age group
        age_group = classify_age_group(age)

        # Mock ML Model Inference (Replace this block with your XGBoost + QAOA pipeline)
        # --------------------------------------------------------------------------
        predicted_cancer = "Breast Cancer" if sex.lower() == "female" else "Colorectal Adenocarcinoma"
        confidence = 94.2
        risk_category = "Moderate / High"
        stage = "Stage II"
        tnm = "T2 N1 M0"
        spread = "Regional"
        # --------------------------------------------------------------------------

        # Fetch clinical reference data based on predicted cancer & age group
        clinical_info = get_cancer_details(predicted_cancer, age_group)

        return {
            "status": "success",
            "patient_info": {
                "patient_id": patient_id,
                "age": age,
                "age_group": age_group,
                "sex": sex
            },
            "prediction": {
                "cancer_type": predicted_cancer,
                "model": "XGBoost + QAOA Feature Selection",
                "confidence_score": confidence,
                "risk_category": risk_category,
                "stage": stage,
                "tnm": tnm,
                "spread_status": spread
            },
            "genomic_analysis": {
                "genes_analyzed": len(df.columns) * len(df),
                "genes_selected": 50,
                "important_genes": clinical_info["important_genes"]
            },
            "clinical_information": {
                "symptoms": clinical_info["symptoms"],
                "clinical_findings": clinical_info["clinical_findings"],
                "diagnostic_tests": clinical_info["diagnostic_tests"]
            },
            "treatment_options": [
                "Surgery (when appropriate)",
                "Radiation therapy",
                "Chemotherapy",
                "Targeted therapy",
                "Hormone therapy (if indicated)"
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))