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
}

def get_cancer_details(cancer_name: str, age_group: str):
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