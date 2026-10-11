CANCER_DATABASE = {
    "Breast Cancer": {
        "symptoms": {
            "Child": ["Very rare", "Breast mass"],
            "Young": ["Breast lump/change", "Nipple/skin changes"],
            "Adult": ["Breast lump", "Nipple/skin changes"],
            "Older adult": ["Lump", "Nipple/skin changes"]
        },
        "clinical_findings": ["Palpable or imaging-detected breast abnormality", "Lymph-node abnormality"],
        "diagnostic_tests": ["Mammography", "Ultrasound", "MRI when indicated", "Biopsy", "ER/PR/HER2 testing"],
        "important_genes": ["BRCA1", "BRCA2", "TP53", "PIK3CA"]
    },
    "Lung Adenocarcinoma": {
        "symptoms": {
            "Child": ["Extremely rare", "Persistent cough/breathlessness"],
            "Young": ["Persistent cough", "Chest pain", "Breathlessness"],
            "Adult": ["Cough", "Breathlessness", "Weight loss"],
            "Older adult": ["Cough", "Breathlessness", "Weight loss"]
        },
        "clinical_findings": ["Lung lesion", "Abnormal respiratory findings"],
        "diagnostic_tests": ["Chest X-ray", "CT Scan", "Bronchoscopy/biopsy", "Molecular testing"],
        "important_genes": ["EGFR", "ALK", "ROS1", "TP53"]
    },
    "Acute Myeloid Leukemia (AML)": {
        "symptoms": {
            "Child": ["Fever", "Fatigue", "Bruising", "Infections"],
            "Young": ["Fatigue", "Fever", "Bleeding/bruising"],
            "Adult": ["Fatigue", "Infections", "Bleeding"],
            "Older adult": ["Fatigue", "Infections", "Bleeding"]
        },
        "clinical_findings": ["Abnormal CBC", "Pallor", "Low platelets"],
        "diagnostic_tests": ["Complete Blood Count (CBC)", "Blood smear", "Bone-marrow examination", "Cytogenetic/molecular tests"],
        "important_genes": ["FLT3", "NPM1", "DNMT3A", "IDH1"]
    },
    "Colorectal Adenocarcinoma": {
        "symptoms": {
            "Child": ["Rare", "Bowel changes"],
            "Young": ["Blood in stool", "Bowel changes"],
            "Adult": ["Blood in stool", "Constipation/diarrhea", "Abdominal pain"],
            "Older adult": ["Blood in stool", "Weight loss/anemia"]
        },
        "clinical_findings": ["Anemia", "Abdominal/rectal abnormality"],
        "diagnostic_tests": ["Stool testing", "Colonoscopy", "Biopsy", "CT Scan"],
        "important_genes": ["APC", "TP53", "KRAS", "BRAF"]
    }
    # (You can add the rest of the 33 cancers following this exact dictionary structure)
}

def get_cancer_details(cancer_name: str, age_group: str):
    # Default fallback if exact match isn't populated
    default_data = {
        "symptoms": ["Unexplained fatigue", "Weight loss", "Persistent localized pain"],
        "clinical_findings": ["Abnormal tissue mass", "Regional involvement"],
        "diagnostic_tests": ["Imaging (CT/MRI)", "Biopsy", "Pathology review"],
        "important_genes": ["TP53", "BRCA1", "EGFR", "KRAS"]
    }
    
    cancer = CANCER_DATABASE.get(cancer_name)
    if not cancer:
        return default_data
        
    symptoms = cancer["symptoms"].get(age_group, cancer["symptoms"].get("Adult", ["General symptoms"]))
    return {
        "symptoms": symptoms,
        "clinical_findings": cancer["clinical_findings"],
        "diagnostic_tests": cancer["diagnostic_tests"],
        "important_genes": cancer["important_genes"]
    }