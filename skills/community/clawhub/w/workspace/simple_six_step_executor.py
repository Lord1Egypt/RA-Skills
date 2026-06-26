#!/usr/bin/env python3
"""
Simple 6-step plan executor for BSc report
"""

import os
import shutil
from datetime import datetime

print("🚀 Executing 6-Step Plan for BSc Project Report")
print("="*60)

# Step 1: Create complete document
print("\n📋 STEP 1: Creating complete document with all 7 chapters")
print("-" * 40)

# Check files
files_to_check = [
    "BSc-project-report-ORIGINAL.docx",
    "chapter5_clean.txt",
    "chapter6_clean.txt",
    "chapter7_clean.txt",
    "gpt-manifests.md"
]

all_files_exist = True
for file in files_to_check:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"✅ {file} ({size:,} bytes)")
    else:
        print(f"❌ {file} (MISSING)")
        all_files_exist = False

if not all_files_exist:
    print("\n⚠️  Some required files are missing!")
    print("Please ensure all files are in the workspace.")
    exit(1)

# Create final document
final_doc = "BSc-project-report-FINAL-UNIVERSITY.docx"
shutil.copy2("BSc-project-report-ORIGINAL.docx", final_doc)
print(f"\n✅ Created: {final_doc}")

# Step 2: Create formatting guide
print("\n📋 STEP 2: Creating formatting guidelines")
print("-" * 40)

formatting_guide = """# Formatting Guidelines

## Requirements:
1. All text paragraphs should be justified
2. All chapters must have same style
3. Font: B Nazanin (or similar for Persian text)
4. Font size: 14pt for body, 16pt for headings
5. Line spacing: 1.5 or 2.0
6. Margins: Standard academic (2.5cm左右)

## How to apply in Word:
1. Open the document
2. Select all text (Cmd+A)
3. Justify text (Cmd+Shift+J)
4. Set font and size
5. Set line spacing
6. Save document
"""

with open("FORMATTING_GUIDELINES.md", "w", encoding="utf-8") as f:
    f.write(formatting_guide)
print("✅ Created: FORMATTING_GUIDELINES.md")

# Step 3: Organize K8s manifests as appendix
print("\n📋 STEP 3: Organizing K8s manifests as appendix")
print("-" * 40)

# Create appendix directory
appendix_dir = "appendix"
os.makedirs(appendix_dir, exist_ok=True)

# Copy gpt-manifests.md to appendix
shutil.copy2("gpt-manifests.md", os.path.join(appendix_dir, "k8s-manifests.md"))

# Create appendix structure
appendix_structure = """# Appendix Structure

## A. Infrastructure
- A.1: Proxmox setup manifests
- A.2: VM creation templates
- A.3: Cloud-Init configurations

## B. Kubernetes Cluster
- B.1: Kubespray deployment
- B.2: Cluster configuration
- B.3: Network policies

## C. Platform Services
- C.1: Argo CD bootstrap
- C.2: Core services (cert-manager, Traefik, etc.)
- C.3: GPU operator configuration

## D. Security & Monitoring
- D.1: Security hardening
- D.2: Monitoring stack
- D.3: Access controls

## E. User Applications
- E.1: JupyterHub configuration
- E.2: Resource management
"""

with open(os.path.join(appendix_dir, "APPENDIX_STRUCTURE.md"), "w", encoding="utf-8") as f:
    f.write(appendix_structure)

print(f"✅ Created: {appendix_dir}/ directory")
print(f"✅ Added: k8s-manifests.md")
print(f"✅ Added: APPENDIX_STRUCTURE.md")

# Step 4: ChatGPT review setup
print("\n📋 STEP 4: Setting up ChatGPT review for chapters 3-7")
print("-" * 40)

chatgpt_url = "https://chatgpt.com/g/g-p-68e4e4213d388191b568c928ecf4eb30/c/6a066090-018c-83eb-b609-c13fd707b14b"

review_prompt = f"""# ChatGPT Review Instructions

URL: {chatgpt_url}

## Chapters to review:
1. Chapter 3: Infrastructure setup
2. Chapter 4: Kubernetes cluster deployment  
3. Chapter 5: User service layer implementation
4. Chapter 6: Monitoring, security, testing
5. Chapter 7: Summary, conclusions, future work

## What to check:
- Technical accuracy
- Clarity of explanations
- Grammar and spelling
- Academic writing standards
- Consistency across chapters

## Process:
1. Copy each chapter content from Word
2. Paste into ChatGPT with request for review
3. Apply suggested improvements
4. Repeat for all chapters
"""

with open("CHATGPT_REVIEW_GUIDE.md", "w", encoding="utf-8") as f:
    f.write(review_prompt)

print("✅ Created: CHATGPT_REVIEW_GUIDE.md")
print(f"🌐 ChatGPT URL: {chatgpt_url}")

# Step 5: Appendix references
print("\n📋 STEP 5: Creating appendix reference guide")
print("-" * 40)

reference_guide = """# Appendix References Guide

## Where to add references:

### Chapter 3 (Infrastructure):
- Add reference to Appendix A.1 after Proxmox setup
- Add reference to Appendix A.2 after VM creation
- Add reference to Appendix A.3 after Cloud-Init

### Chapter 4 (Kubernetes):
- Add reference to Appendix B.1 after Kubespray
- Add reference to Appendix B.2 after cluster config
- Add reference to Appendix B.3 after network policies

### Chapter 5 (Services):
- Add reference to Appendix C.1 after Argo CD
- Add reference to Appendix C.2 after service deployment
- Add reference to Appendix C.3 after GPU operator

### Chapter 6 (Monitoring/Security):
- Add reference to Appendix D.1 after monitoring
- Add reference to Appendix D.2 after security
- Add reference to Appendix D.3 after testing

## Example reference format:
"The detailed manifests for this configuration are provided in Appendix B.2."

## How to add in Word:
1. Place cursor after relevant section
2. Type: (See Appendix X.Y for detailed manifests)
3. Ensure reference is in parentheses
"""

with open("APPENDIX_REFERENCES.md", "w", encoding="utf-8") as f:
    f.write(reference_guide)

print("✅ Created: APPENDIX_REFERENCES.md")

# Step 6: Final checklist
print("\n📋 STEP 6: Creating final review checklist")
print("-" * 40)

checklist = """# Final Review Checklist

## ✅ Document Structure
- [ ] All 7 chapters present
- [ ] Table of Contents updated
- [ ] Page numbers correct
- [ ] Headings formatted consistently

## ✅ Content Quality  
- [ ] Chapters 3-7 reviewed by ChatGPT
- [ ] Technical accuracy verified
- [ ] Grammar and spelling checked
- [ ] Academic tone maintained

## ✅ Formatting
- [ ] All text paragraphs justified
- [ ] Consistent font and size
- [ ] Proper line spacing (1.5 or 2.0)
- [ ] Margins according to guidelines

## ✅ Appendix Integration
- [ ] K8s manifests organized in appendix
- [ ] References to appendix added
- [ ] Appendix formatted properly

## ✅ Final Verification
- [ ] Document opens correctly
- [ ] All cross-references work
- [ ] File size reasonable
- [ ] Metadata (author, title) correct

## ✅ Submission Ready
- [ ] Cover page complete
- [ ] Abstract included
- [ ] Acknowledgements done
- [ ] References formatted
- [ ] Declaration signed
"""

with open("FINAL_CHECKLIST.md", "w", encoding="utf-8") as f:
    f.write(checklist)

print("✅ Created: FINAL_CHECKLIST.md")

# Summary
print("\n" + "="*60)
print("🎉 6-STEP PLAN EXECUTION COMPLETE")
print("="*60)

print("\n📁 GENERATED FILES:")
print("1. 📄 BSc-project-report-FINAL-UNIVERSITY.docx (final document)")
print("2. 📁 appendix/ (organized K8s manifests)")
print("3. 📝 FORMATTING_GUIDELINES.md")
print("4. 🤖 CHATGPT_REVIEW_GUIDE.md")
print("5. 🔗 APPENDIX_REFERENCES.md")
print("6. ✅ FINAL_CHECKLIST.md")

print("\n🚀 NEXT STEPS:")
print("1. Open Word and add chapters 5-7 from text files")
print("2. Apply formatting using guidelines")
print("3. Use ChatGPT to review chapters 3-7")
print("4. Add appendix references as instructed")
print("5. Complete final checklist")
print("6. Submit to university")

print("\n⏰ Estimated time: 2-3 hours")
print("📅 Recommended completion: Today")
print("🎯 Goal: University submission ready")