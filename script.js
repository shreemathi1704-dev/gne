// DOM Element References
const ageInput = document.getElementById('age');
const ageGroupDisplay = document.getElementById('ageGroupDisplay');
const fileInput = document.getElementById('csvFile');
const fileNameText = document.getElementById('fileNameText');
const predictionForm = document.getElementById('predictionForm');
const reportSection = document.getElementById('reportSection');
const reportContent = document.getElementById('reportContent');
const downloadBtn = document.getElementById('downloadBtn');
const submitBtn = document.getElementById('submitBtn');

let lastReportData = null;

// ==========================================
// 1. Automatic Age Group Classification
// ==========================================
function updateAgeGroup(age) {
    let group = "Older adult";
    if (age <= 14) {
        group = "Child";
    } else if (age <= 24) {
        group = "Young";
    } else if (age <= 64) {
        group = "Adult";
    }
    
    ageGroupDisplay.textContent = group;
    
    // Add a soft visual pulse effect on update
    ageGroupDisplay.style.transform = "scale(1.03)";
    setTimeout(() => {
        ageGroupDisplay.style.transform = "scale(1)";
    }, 200);
}

ageInput.addEventListener('input', (e) => {
    const ageValue = parseInt(e.target.value) || 0;
    updateAgeGroup(ageValue);
});

// ==========================================
// 2. Drag & Drop and File Selection Handler
// ==========================================
fileInput.addEventListener('change', (e) => {
    handleFileSelection(e.target.files[0]);
});

function handleFileSelection(file) {
    if (file) {
        if (!file.name.endsWith('.csv')) {
            alert('Please upload a valid .csv genomic data file.');
            fileInput.value = '';
            fileNameText.innerHTML = `Drag & drop genomic CSV file here or <span class="browse">browse</span>`;
            return;
        }
        fileNameText.innerHTML = `Selected File: <strong style="color: var(--accent-glow);">${file.name}</strong> (${(file.size / 1024).toFixed(1)} KB)`;
    }
}

// ==========================================
// 3. Form Submission & Backend API Integration
// ==========================================
predictionForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const patientId = document.getElementById('patientId').value.trim();
    const age = ageInput.value;
    const sex = document.getElementById('sex').value;
    const selectedFile = fileInput.files[0];

    if (!selectedFile) {
        alert('Please attach a genomic CSV dataset before running analysis.');
        return;
    }

    // Prepare multipart form data
    const formData = new FormData();
    formData.append('patient_id', patientId);
    formData.append('age', age);
    formData.append('sex', sex);
    formData.append('file', selectedFile);

    // Update UI to loading state
    setLoadingState(true);

    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || 'Server responded with an error.');
        }

        const data = await response.json();
        lastReportData = data;
        
        // Render results into the dashboard
        renderReport(data);
        reportSection.style.display = 'block';
        
        // Smooth scroll to report output
        reportSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (err) {
        console.error('API Error:', err);
        alert(`Analysis failed: ${err.message}\nEnsure the FastAPI backend is running on http://127.0.0.1:8000`);
    } finally {
        setLoadingState(false);
    }
});

// Helper for loading button state
function setLoadingState(isLoading) {
    if (isLoading) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = `
            <span class="spinner" style="display:inline-block; animation: spin 1s linear infinite;">⏳</span> 
            Running QAOA & XGBoost Pipeline...
        `;
    } else {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Run AI Genomic Analysis';
    }
}

// ==========================================
// 4. Report Rendering Engine
// ==========================================
function renderReport(data) {
    const p = data.patient_info;
    const pred = data.prediction;
    const gen = data.genomic_analysis;
    const cin = data.clinical_information;
    const treatments = data.treatment_options;

    reportContent.innerHTML = `
        <div class="report-section-box">
            <h3>Patient & Classification Profile</h3>
            <p><strong>Patient ID:</strong> ${p.patient_id} &nbsp;|&nbsp; <strong>Age:</strong> ${p.age} (${p.age_group}) &nbsp;|&nbsp; <strong>Sex:</strong> ${p.sex}</p>
        </div>

        <div class="report-section-box" style="border-left-color: var(--primary-glow);">
            <h3>AI Cancer Classification & Risk</h3>
            <p style="font-size: 1.1rem; margin-bottom: 6px;"><strong>Predicted Cancer:</strong> <span style="color: var(--accent-glow);">${pred.cancer_type}</span></p>
            <p><strong>Model Used:</strong> ${pred.model}</p>
            <p><strong>Prediction Confidence:</strong> <span class="badge" style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4);">${pred.confidence_score}%</span></p>
            <p style="margin-top: 6px;"><strong>Risk Category:</strong> ${pred.risk_category} &nbsp;|&nbsp; <strong>Estimated Stage:</strong> ${pred.stage} (${pred.tnm})</p>
        </div>

        <div class="report-section-box">
            <h3>Genomic Markers (QAOA Feature Selection)</h3>
            <p><strong>Important Genes Identified:</strong> ${gen.important_genes.join(', ')}</p>
            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Analyzed ${gen.genes_analyzed.toLocaleString()} data points down to ${gen.genes_selected} core predictive features.</p>
        </div>

        <div class="report-section-box">
            <h3>Clinical Symptoms & Findings (${p.age_group})</h3>
            <p><strong>Common Symptoms:</strong> ${cin.symptoms.join(', ')}</p>
            <p style="margin-top: 4px;"><strong>Possible Clinical Findings:</strong> ${cin.clinical_findings.join(', ')}</p>
        </div>

        <div class="report-section-box">
            <h3>Common Diagnostic Evaluation</h3>
            <ul style="margin-top: 4px;">
                ${cin.diagnostic_tests.map(test => `<li>\${test}</li>`).join('')}
            </ul>
        </div>

        <div class="report-section-box">
            <h3>Treatment Management Options</h3>
            <ul style="margin-top: 4px;">
                ${treatments.map(opt => `<li>\${opt}</li>`).join('')}
            </ul>
        </div>
    `;
}

// ==========================================
// 5. Export Report Functionality
// ==========================================
downloadBtn.addEventListener('click', () => {
    if (!lastReportData) return;

    // Format clean text report output
    const p = lastReportData.patient_info;
    const pred = lastReportData.prediction;
    const cin = lastReportData.clinical_information;

    const reportText = `
====================================================
        Q-CANCER AI GENOMIC ANALYSIS REPORT
====================================================
Patient ID       : ${p.patient_id}
Age / Group      : ${p.age} Years (${p.age_group})
Sex              : ${p.sex}
Analysis Date    : ${new Date().toLocaleDateString()}
----------------------------------------------------
PREDICTION RESULTS
----------------------------------------------------
Predicted Cancer : ${pred.cancer_type}
Model            : ${pred.model}
Confidence Score : ${pred.confidence_score}%
Risk Category    : ${pred.risk_category}
Stage / TNM      : ${pred.stage} (${pred.tnm})
----------------------------------------------------
IMPORTANT GENES
----------------------------------------------------
${lastReportData.genomic_analysis.important_genes.join(', ')}
----------------------------------------------------
SYMPTOMS & FINDINGS (${p.age_group})
----------------------------------------------------
Symptoms         : ${cin.symptoms.join(', ')}
Clinical Findings: ${cin.clinical_findings.join(', ')}
----------------------------------------------------
RECOMMENDED DIAGNOSTIC EVALUATION
----------------------------------------------------
${cin.diagnostic_tests.map(t => `- \${t}`).join('\n')}
----------------------------------------------------
IMPORTANT DISCLAIMER
----------------------------------------------------
This is an AI-based genomic analysis and classification 
report. It is NOT a medical diagnosis. Confirmation 
requires formal clinical evaluation and pathology.
====================================================
    `.trim();

    // Trigger text file download
    const blob = new Blob([reportText], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${p.patient_id}_Q_Cancer_Report.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});