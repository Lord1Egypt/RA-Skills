---
name: early-gastric-cancer-endoscopic-treatment-indications
description: Determines whether a patient with early gastric cancer is eligible for endoscopic treatment (EMR or ESD) based on histology, invasion depth, ulceration status, and tumor size. Use this skill when evaluating a confirmed early gastric cancer case to decide between endoscopic resection and surgical intervention.
---

# Early Gastric Cancer Endoscopic Treatment Indications

## When to Use
Use this skill when:
- A patient has been diagnosed with early gastric cancer via endoscopy and biopsy.
- You need to determine if endoscopic submucosal dissection (ESD) or endoscopic mucosal resection (EMR) is appropriate.
- Clinical data includes histology type, invasion depth (T1a vs T1b), presence of ulceration, and tumor diameter.

## How to Execute

### Step 1: Assess Absolute Indications for Endoscopic Treatment
Confirm **all** of the following criteria are met:
- **Histology**: Differentiated adenocarcinoma (well or moderately differentiated).
- **Invasion depth**: Confined to the mucosa (T1a), confirmed by endoscopic ultrasound.
- **Ulceration**: Absent (no ulcer regardless of size).
- **Tumor size**: Maximum diameter < 2 cm.

→ If all criteria are satisfied, **recommend ESD** (preferred over EMR due to higher en bloc resection rate and lower recurrence).

### Step 2: Identify Contraindications Requiring Surgery
Endoscopic treatment is **contraindicated** if **any** of the following are present:
- Invasion into the submucosa (T1b).
- Presence of ulceration.
- Tumor diameter ≥ 2 cm.
- Undifferentiated histology (e.g., signet ring cell carcinoma, poorly differentiated adenocarcinoma).
- Inability to achieve complete endoscopic resection.
- Suspected or confirmed lymph node metastasis.

→ In these cases, **recommend standard radical gastrectomy with D2 lymphadenectomy**.

### Step 3: Document Rationale
Explain that submucosal invasion carries ~20% risk of lymph node metastasis, which endoscopic methods cannot address. Therefore, surgical resection is necessary when risk factors are present.

## Output Format
Return one of the following treatment recommendations:
- "推荐ESD"
- "可行EMR但ESD更优" (only if absolute indications are met but ESD unavailable)
- "禁忌内镜治疗，建议外科手术"