# discharge Skill Examples

## I. Extract from Image

### Example 1: Complete Discharge Summary Image
```
User: /discharge @medical-reports/discharge-summary.jpg

After analyzing image, save:
{
  "id": "2024081500001",
  "basic_info": {
    "hospital": "XX Hospital",
    "department": "Gastroenterology",
    "admission_date": "2024-08-10",
    "discharge_date": "2024-08-15",
    "hospitalization_days": 5,
    "bed_number": "Bed 23"
  },
  "diagnosis": {
    "admission_diagnosis": {
      "main": "Acute cholecystitis",
      "secondary": ["Cholecystolithiasis"]
    },
    "discharge_diagnosis": {
      "main": "Acute cholecystitis",
      "secondary": ["Cholecystolithiasis", "Hypertension (Grade 2, Moderate Risk)"]
    }
  },
  "treatment_summary": {
    "main_treatments": [
      "NPO and gastrointestinal decompression",
      "Anti-infective therapy (Cefoperazone Sodium and Sulbactam Sodium)",
      "Antispasmodic and analgesic therapy"
    ],
    "medications": [
      {
        "drug_name": "Cefoperazone Sodium and Sulbactam Sodium",
        "dosage": "2g",
        "frequency": "Twice daily",
        "route": "IV infusion",
        "duration": "5 days",
        "start_date": "2024-08-10",
        "end_date": "2024-08-15",
        "drug_category": "Antibiotics",
        "indication": "Anti-infective"
      }
    ],
    "infusion_therapy": [
      {
        "solution_name": "0.9% Sodium Chloride Injection",
        "additives": ["Cefoperazone Sodium and Sulbactam Sodium 2g"],
        "dosage": "100ml",
        "frequency": "Twice daily",
        "route": "IV infusion",
        "duration": "5 days",
        "start_date": "2024-08-10",
        "end_date": "2024-08-15"
      }
    ],
    "treatment_effectiveness": {
      "overall_effect": "Excellent",
      "symptom_improvement": "Abdominal pain relieved, temperature normal",
      "adverse_reactions": [],
      "lab_improvements": "White blood cells returned to normal"
    },
    "surgeries": [
      {
        "surgery_name": "Laparoscopic cholecystectomy",
        "surgery_date": "2024-08-12",
        "anesthesia": "General anesthesia"
      }
    ]
  },
  "discharge_orders": {
    "medication_instructions": [
      {
        "drug_name": "Amoxicillin Capsules",
        "dosage": "0.5g",
        "frequency": "3 times daily",
        "duration": "7 days"
      }
    ],
    "dietary_guidance": "Low-fat diet, small frequent meals, avoid greasy foods"
  }
}
```

### Example 2: Manually Specify Dates
```
User: /discharge @medical-reports/discharge-summary.jpg 2024-08-10 2024-08-15

Use specified admission and discharge dates
```

## II. From Text Description

### Example 3: Simple Description
```
User: /discharge I was hospitalized for acute cholecystitis on August 10, discharged on August 15, had laparoscopic surgery, doctor advised low-fat diet, follow-up in 2 weeks

Save:
{
  "basic_info": {
    "admission_date": "2024-08-10",
    "discharge_date": "2024-08-15",
    "hospitalization_days": 5
  },
  "diagnosis": {
    "discharge_diagnosis": {
      "main": "Acute cholecystitis"
    }
  },
  "treatment_summary": {
    "surgeries": [
      {
        "surgery_name": "Laparoscopic surgery"
      }
    ]
  },
  "discharge_orders": {
    "dietary_guidance": "Low-fat diet",
    "follow_up_plan": [
      {
        "item": "Follow-up",
        "timing": "2 weeks"
      }
    ]
  }
}
```

### Example 4: Pneumonia Hospitalization
```
User: /discharge Hospitalized for pneumonia for 5 days in August 2024, continue antibiotics for 3 days after discharge, chest X-ray recheck in 1 week

Save:
{
  "basic_info": {
    "admission_date": "2024-08-XX",
    "discharge_date": "2024-08-XX",
    "hospitalization_days": 5
  },
  "diagnosis": {
    "discharge_diagnosis": {
      "main": "Pneumonia"
    }
  },
  "discharge_orders": {
    "medication_instructions": [
      {
        "drug_name": "Antibiotics",
        "duration": "3 days"
      }
    ],
    "follow_up_plan": [
      {
        "item": "Chest X-ray recheck",
        "timing": "1 week"
      }
    ]
  }
}
```

## III. Interactive Supplement

### Example 5: Incomplete Information
```
User: /discharge I just got discharged, had surgery

AI: Please tell me your discharge diagnosis (primary condition)?

User: Acute appendicitis

AI: What were your admission and discharge dates?

User: Admitted August 20, discharged August 23

Save: Complete discharge summary record
```

## IV. Output Confirmation Example

```
✅ Discharge summary saved

Hospitalization Information:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Hospital: XX Hospital
Department: Gastroenterology
Admission Date: 2024-08-10
Discharge Date: 2024-08-15
Length of Stay: 5 days

Primary Diagnosis:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Admission Diagnosis: Acute cholecystitis
Discharge Diagnosis: Acute cholecystitis

Main Treatment:
━━━━━━━━━━━━━━━━━━━━━━━━━━
- Laparoscopic cholecystectomy (2024-08-12)
- Anti-infective therapy
- Antispasmodic and analgesic therapy

Discharge Orders:
━━━━━━━━━━━━━━━━━━━━━━━━━━
Medication: Amoxicillin Capsules 0.5g 3 times daily × 7 days
Diet: Low-fat diet, small frequent meals
Follow-up: Outpatient follow-up 2 weeks post-op

Data saved to:
data/discharge-summary/2024-08/2024-08-15_acute-cholecystitis.json
```

## V. Complete Example with New Fields

### Example 6: Pneumonia Hospitalization (Including Infusion and Non-Drug Treatments)
```
User: /discharge My father was hospitalized for pneumonia, August 1 to August 7, used ceftriaxone antibiotics, also had nebulization and oxygen therapy

Save:
{
  "basic_info": {
    "admission_date": "2024-08-01",
    "discharge_date": "2024-08-07",
    "hospitalization_days": 6
  },
  "diagnosis": {
    "discharge_diagnosis": {
      "main": "Pneumonia"
    }
  },
  "treatment_summary": {
    "main_treatments": ["Anti-infective therapy", "Oxygen therapy", "Nebulization"],
    "medications": [
      {
        "drug_name": "Ceftriaxone for Injection",
        "dosage": "2g",
        "frequency": "Once daily",
        "route": "IV infusion",
        "duration": "6 days",
        "start_date": "2024-08-01",
        "end_date": "2024-08-07",
        "drug_category": "Antibiotics",
        "indication": "Anti-infective"
      },
      {
        "drug_name": "Ambroxol Hydrochloride Tablets",
        "dosage": "30mg",
        "frequency": "3 times daily",
        "route": "Oral",
        "duration": "7 days",
        "drug_category": "Expectorants",
        "indication": "Phlegm reduction"
      }
    ],
    "infusion_therapy": [
      {
        "solution_name": "0.9% Sodium Chloride Injection",
        "additives": ["Ceftriaxone 2g"],
        "dosage": "100ml",
        "frequency": "Once daily",
        "route": "IV infusion",
        "duration": "6 days",
        "start_date": "2024-08-01",
        "end_date": "2024-08-07"
      }
    ],
    "non_drug_treatments": [
      {
        "treatment_type": "Oxygen therapy",
        "treatment_name": "Low-flow oxygen",
        "parameters": "2L/min, twice daily, 30 minutes each",
        "duration": "5 days",
        "start_date": "2024-08-01",
        "end_date": "2024-08-06"
      },
      {
        "treatment_type": "Nebulization",
        "treatment_name": "Budesonide nebulization",
        "parameters": "2mg, twice daily",
        "duration": "5 days",
        "start_date": "2024-08-01",
        "end_date": "2024-08-06"
      }
    ],
    "treatment_effectiveness": {
      "overall_effect": "Excellent",
      "symptom_improvement": "Cough and sputum significantly reduced, temperature returned to normal, shortness of breath relieved",
      "adverse_reactions": ["Mild rash on day 2 of infusion, resolved after treatment"],
      "lab_improvements": "CRP decreased from 86mg/L to 8mg/L, white blood cell count normal"
    }
  }
}
```

## VI. Complete Oncology Treatment Examples

### Example 7: Lung Cancer Chemotherapy + Immunotherapy
```
User: /discharge My father diagnosed with lung cancer, hospitalized for cycle 2 chemotherapy, TP regimen, also using PD-1 immunotherapy

Save:
{
  "basic_info": {
    "admission_date": "2024-08-01",
    "discharge_date": "2024-08-07",
    "hospitalization_days": 6,
    "department": "Medical Oncology"
  },
  "diagnosis": {
    "discharge_diagnosis": {
      "main": "Squamous cell carcinoma of right upper lung lobe (T2aN1M0, Stage IIIa)",
      "secondary": ["Hypertension", "Type 2 Diabetes"]
    }
  },
  "treatment_summary": {
    "main_treatments": ["Chemotherapy", "Immunotherapy", "Supportive care"],
    "chemotherapy": [
      {
        "regimen_name": "TP regimen",
        "cycle_number": 2,
        "total_planned_cycles": 6,
        "medications": ["Paclitaxel", "Cisplatin"],
        "dosage_details": "Paclitaxel 240mg d1 + Cisplatin 120mg d1-2",
        "route": "IV infusion",
        "cycle_start_date": "2024-08-02",
        "cycle_end_date": "2024-08-07",
        "next_cycle_date": "2024-08-23",
        "purpose": "Curative chemotherapy",
        "adverse_events": ["Nausea (CTCAE grade 2)", "Leukopenia (CTCAE grade 1)"],
        "toxicity_grade": "CTCAE grade 1-2"
      }
    ],
    "immunotherapy": [
      {
        "drug_name": "Pembrolizumab Injection",
        "drug_type": "PD-1 inhibitor",
        "dosage": "200mg",
        "frequency": "Every 3 weeks",
        "route": "IV infusion",
        "start_date": "2024-08-02",
        "end_date": "2024-08-02",
        "adverse_events": [],
        "notes": "Combined with chemotherapy, planned for 6 cycles total"
      }
    ],
    "medications": [
      {
        "drug_name": "Ondansetron",
        "dosage": "8mg",
        "frequency": "Twice daily",
        "route": "Oral",
        "duration": "5 days",
        "drug_category": "Anti-emetics",
        "indication": "Prevention of chemotherapy-related nausea and vomiting"
      }
    ],
    "treatment_effectiveness": {
      "overall_effect": "Effective",
      "symptom_improvement": "Cough symptoms improved compared to before, fatigue improved",
      "adverse_reactions": ["Mild nausea", "Mild leukopenia"],
      "lab_improvements": "Await repeat CT to assess tumor size changes"
    }
  },
  "discharge_orders": {
    "medication_instructions": [
      {
        "drug_name": "Recombinant Human Granulocyte Colony-Stimulating Factor",
        "dosage": "200μg",
        "frequency": "Once daily, subcutaneous injection",
        "duration": "3 days",
        "notes": "Use when WBC < 3.5×10^9/L"
      }
    ],
    "follow_up_plan": [
      {
        "item": "Cycle 3 chemotherapy",
        "timing": "2024-08-23",
        "location": "Medical Oncology Outpatient"
      },
      {
        "item": "CBC recheck",
        "timing": "Once weekly"
      },
      {
        "item": "Tumor assessment CT",
        "timing": "Before cycle 4 chemotherapy"
      }
    ],
    "warnings": ["Seek medical care if fever >38.5°C", "Watch for bleeding tendencies", "Avoid infection"]
  }
}
```

### Example 8: Breast Cancer Postoperative Adjuvant Radiotherapy
```
User: /discharge Breast cancer postoperative radiotherapy, completed 25 sessions, just finished

Save:
{
  "basic_info": {
    "admission_date": "2024-07-10",
    "discharge_date": "2024-08-10",
    "hospitalization_days": 31,
    "department": "Radiation Oncology"
  },
  "diagnosis": {
    "discharge_diagnosis": {
      "main": "Postoperative left breast invasive ductal carcinoma (pT2N0M0, Stage IIa)",
      "secondary": []
    }
  },
  "treatment_summary": {
    "main_treatments": "Postoperative adjuvant radiotherapy",
    "surgeries": [
      {
        "surgery_name": "Left breast modified radical mastectomy",
        "surgery_date": "2024-06-15"
      }
    ],
    "radiotherapy": [
      {
        "target_site": "Left chest wall and supraclavicular region",
        "radiation_type": "Photon radiotherapy",
        "technique": "IMRT (Intensity-Modulated Radiation Therapy)",
        "total_dose": "50Gy",
        "dose_per_fraction": "2Gy/fraction",
        "fractions": 25,
        "frequency": "Once daily, 5 times per week",
        "start_date": "2024-07-10",
        "end_date": "2024-08-10",
        "purpose": "Adjuvant radiotherapy",
        "toxicity": "Mild radiation dermatitis (CTCAE grade 1), mild fatigue",
        "notes": "Radiotherapy completed smoothly, planned dose completed"
      }
    ],
    "treatment_effectiveness": {
      "overall_effect": "Excellent",
      "symptom_improvement": "Radiotherapy completed, good local control",
      "adverse_reactions": ["Mild skin redness", "Mild fatigue"],
      "lab_improvements": "Normal CBC, normal liver and kidney function"
    }
  },
  "discharge_orders": {
    "medication_instructions": [],
    "wound_care": "Keep radiotherapy area skin clean and dry, avoid friction and direct sunlight, use physician-recommended skin care products",
    "follow_up_plan": [
      {
        "item": "Post-radiotherapy follow-up",
        "timing": "1 month after radiotherapy",
        "location": "Radiation Oncology Outpatient"
      },
      {
        "item": "Regular follow-up",
        "timing": "Every 3 months for 2 years"
      }
    ]
  }
}
```

### Example 9: Colorectal Cancer Targeted Therapy
```
User: /discharge Colorectal cancer with liver metastasis, using bevacizumab targeted therapy, 4th time

Save:
{
  "basic_info": {
    "admission_date": "2024-08-05",
    "discharge_date": "2024-08-06",
    "hospitalization_days": 1,
    "department": "Medical Oncology"
  },
  "diagnosis": {
    "discharge_diagnosis": {
      "main": "Sigmoid colon adenocarcinoma (pT4aN1bM1a, Stage IV) with liver metastasis",
      "secondary": ["Hypertension"]
    }
  },
  "treatment_summary": {
    "main_treatments": ["Targeted therapy", "Maintenance chemotherapy"],
    "chemotherapy": [
      {
        "regimen_name": "Capecitabine monotherapy maintenance",
        "cycle_number": 4,
        "total_planned_cycles": 12,
        "medications": ["Capecitabine Tablets"],
        "dosage_details": "Capecitabine 1.5g twice daily orally d1-14",
        "route": "Oral",
        "cycle_start_date": "2024-08-05",
        "cycle_end_date": "2024-08-18",
        "purpose": "Palliative chemotherapy",
        "adverse_events": ["Hand-foot syndrome (CTCAE grade 1)"]
      }
    ],
    "targeted_therapy": [
      {
        "drug_name": "Bevacizumab Injection",
        "target": "VEGF",
        "dosage": "400mg",
        "frequency": "Every 3 weeks",
        "route": "IV infusion",
        "start_date": "2024-08-05",
        "end_date": "2024-08-05",
        "adverse_events": [],
        "notes": "Combined with chemotherapy, 4th dose administered"
      }
    ],
    "treatment_effectiveness": {
      "overall_effect": "Effective",
      "symptom_improvement": "Abdominal distension relieved, appetite improved",
      "adverse_reactions": ["Mild hand-foot syndrome"],
      "lab_improvements": "CEA decreased from 45ng/mL to 18ng/mL"
    }
  },
  "discharge_orders": {
    "medication_instructions": [
      {
        "drug_name": "Capecitabine Tablets",
        "dosage": "1.5g",
        "frequency": "Twice daily, taken after breakfast and dinner",
        "duration": "14 days",
        "notes": "Rest 7 days before starting next cycle"
      }
    ],
    "dietary_guidance": "Light diet, avoid spicy and irritating foods",
    "follow_up_plan": [
      {
        "item": "Next cycle treatment",
        "timing": "2024-08-26"
      },
      {
        "item": "Imaging assessment",
        "timing": "After 2 cycles"
      }
    ],
    "warnings": ["Care for hand and foot skin", "Seek medical care if diarrhea worsens"]
  }
}
```
