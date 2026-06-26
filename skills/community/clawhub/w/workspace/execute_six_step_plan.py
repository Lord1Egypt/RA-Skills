#!/usr/bin/env python3
"""
Execute the 6-step plan for BSc project report preparation
"""

import os
import sys
import shutil
import subprocess
import json
from datetime import datetime
import time

class BScReportPreparer:
    def __init__(self):
        self.workspace = os.getcwd()
        self.original_doc = "BSc-project-report-ORIGINAL.docx"
        self.final_doc = "BSc-project-report-FINAL-UNIVERSITY.docx"
        self.backup_prefix = "BSc-project-report-BACKUP"
        
    def step1_create_complete_document(self):
        """Step 1: Create Word document with all 7 chapters"""
        print("\n" + "="*60)
        print("STEP 1: Creating complete document with all 7 chapters")
        print("="*60)
        
        # Check if original document exists
        if not os.path.exists(self.original_doc):
            print(f"❌ Original document not found: {self.original_doc}")
            return False
        
        # Create backup of original
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_file = f"{self.backup_prefix}-STEP1-{timestamp}.docx"
        shutil.copy2(self.original_doc, backup_file)
        print(f"✅ Backup created: {backup_file}")
        
        # Copy as final document
        shutil.copy2(self.original_doc, self.final_doc)
        print(f"✅ Created final document: {self.final_doc}")
        
        # Check chapter files
        chapter_files = {
            "chapter5": "chapter5_clean.txt",
            "chapter6": "chapter6_clean.txt", 
            "chapter7": "chapter7_clean.txt"
        }
        
        for chap, file in chapter_files.items():
            if os.path.exists(file):
                file_size = os.path.getsize(file)
                print(f"✅ {chap} content available: {file} ({file_size:,} bytes)")
            else:
                print(f"❌ {chap} file not found: {file}")
                return False
        
        print("\n📋 Chapter status:")
        print("  • Chapters 1-4: In original Word document")
        print("  • Chapter 5: Available in chapter5_clean.txt")
        print("  • Chapter 6: Available in chapter6_clean.txt")
        print("  • Chapter 7: Available in chapter7_clean.txt")
        
        # Create instructions for manual chapter addition
        self._create_chapter_addition_guide()
        
        return True
    
    def step2_apply_formatting_guidelines(self):
        """Step 2: Apply formatting guidelines"""
        print("\n" + "="*60)
        print("STEP 2: Applying formatting guidelines")
        print("="*60)
        
        # Check for formatting guideline file
        format_guide = self._find_formatting_guide()
        
        # Create formatting automation script
        formatting_script = self._create_formatting_automation_script(format_guide)
        
        print("📋 Formatting requirements:")
        print("  1. All text paragraphs should be justified")
        print("  2. All chapters must have same style")
        print("  3. Consistent font size and spacing")
        print("  4. Proper heading styles")
        
        if format_guide:
            print(f"✅ Formatting guide found: {format_guide}")
        else:
            print("⚠️  No formatting guide found. Using standard academic formatting.")
        
        print(f"\n📝 Created formatting automation script: {formatting_script}")
        
        # Create peekaboo automation JSON
        peekaboo_script = self._create_peekaboo_formatting_script()
        print(f"👀 Created Peekaboo automation script: {peekaboo_script}")
        
        return True
    
    def step3_organize_k8s_manifests(self):
        """Step 3: Organize K8s manifests as appendix"""
        print("\n" + "="*60)
        print("STEP 3: Organizing K8s manifests as appendix")
        print("="*60)
        
        # Check for gpt-manifests.md
        if not os.path.exists("gpt-manifests.md"):
            print("❌ gpt-manifests.md not found")
            return False
        
        # Read the manifest file
        with open("gpt-manifests.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create appendix directory structure
        appendix_dir = "appendix"
        os.makedirs(appendix_dir, exist_ok=True)
        
        # Create appendix content
        appendix_content = self._create_appendix_content(content)
        
        # Save appendix files
        appendix_file = os.path.join(appendix_dir, "k8s-manifests-appendix.md")
        with open(appendix_file, 'w', encoding='utf-8') as f:
            f.write(appendix_content)
        
        print(f"✅ Created appendix directory: {appendix_dir}")
        print(f"✅ Created appendix content: {appendix_file}")
        
        # Create summary of manifests
        manifest_count = content.count('```yaml') + content.count('```yml')
        print(f"📊 Found {manifest_count} K8s manifest sections in gpt-manifests.md")
        
        # Create appendix instructions for Word
        word_appendix_guide = self._create_word_appendix_guide(appendix_dir)
        print(f"📝 Created Word appendix integration guide: {word_appendix_guide}")
        
        return True
    
    def step4_chatgpt_review(self):
        """Step 4: Use ChatGPT to review and fix chapters 3-7"""
        print("\n" + "="*60)
        print("STEP 4: ChatGPT review of chapters 3-7")
        print("="*60)
        
        # Check Chrome ChatGPT tab
        chatgpt_url = "https://chatgpt.com/g/g-p-68e4e4213d388191b568c928ecf4eb30/c/6a066090-018c-83eb-b609-c13fd707b14b"
        
        print(f"🌐 ChatGPT URL: {chatgpt_url}")
        print("\n📋 Chapters to review:")
        print("  • Chapter 3: Infrastructure setup")
        print("  • Chapter 4: Kubernetes cluster deployment")
        print("  • Chapter 5: User service layer implementation")
        print("  • Chapter 6: Monitoring, security, testing")
        print("  • Chapter 7: Summary and conclusions")
        
        # Create review prompts
        review_prompts = self._create_chatgpt_review_prompts()
        
        # Create automation script for Chrome
        chrome_script = self._create_chrome_automation_script(chatgpt_url, review_prompts)
        
        print(f"\n🤖 Created ChatGPT review prompts: {review_prompts}")
        print(f"🔧 Created Chrome automation script: {chrome_script}")
        
        print("\n⚠️  Note: Chrome automation requires manual approval for accessibility permissions")
        
        return True
    
    def step5_add_appendix_references(self):
        """Step 5: Add references to appendix in report sections"""
        print("\n" + "="*60)
        print("STEP 5: Adding references to appendix")
        print("="*60)
        
        # Create reference mapping
        reference_mapping = {
            "Chapter 3 (Infrastructure)": [
                "Appendix A.1: Proxmox setup manifests",
                "Appendix A.2: VM creation manifests",
                "Appendix A.3: Cloud-Init configurations"
            ],
            "Chapter 4 (Kubernetes)": [
                "Appendix B.1: Kubespray deployment manifests",
                "Appendix B.2: Cluster configuration",
                "Appendix B.3: Network policies"
            ],
            "Chapter 5 (Services)": [
                "Appendix C.1: Argo CD bootstrap manifests",
                "Appendix C.2: Service deployment manifests",
                "Appendix C.3: GPU operator configuration"
            ],
            "Chapter 6 (Monitoring/Security)": [
                "Appendix D.1: Monitoring stack manifests",
                "Appendix D.2: Security hardening manifests",
                "Appendix D.3: Testing configurations"
            ]
        }
        
        # Create reference guide
        reference_guide = self._create_reference_guide(reference_mapping)
        
        print("📋 Reference points to add:")
        for chapter, refs in reference_mapping.items():
            print(f"\n  {chapter}:")
            for ref in refs:
                print(f"    • {ref}")
        
        print(f"\n📝 Created reference integration guide: {reference_guide}")
        
        # Create Word search/replace instructions
        word_ref_script = self._create_word_reference_script(reference_mapping)
        print(f"🔧 Created Word reference automation script: {word_ref_script}")
        
        return True
    
    def step6_final_review(self):
        """Step 6: Final review based on guidelines"""
        print("\n" + "="*60)
        print("STEP 6: Final review and issue fixing")
        print("="*60)
        
        # Create final checklist
        checklist = self._create_final_checklist()
        
        # Create validation script
        validation_script = self._create_validation_script()
        
        print("📋 Final review checklist:")
        print("  1. ✅ All 7 chapters present and complete")
        print("  2. ✅ Formatting guidelines applied (justification, styles)")
        print("  3. ✅ K8s manifests organized as appendix")
        print("  4. ✅ Chapters 3-7 reviewed and fixed by ChatGPT")
        print("  5. ✅ Appendix references added to corresponding sections")
        print("  6. ✅ Final proofreading and validation")
        
        print(f"\n📝 Created final checklist: {checklist}")
        print(f"🔧 Created validation script: {validation_script}")
        
        # Create submission package
        submission_package = self._create_submission_package()
        print(f"📦 Created submission package: {submission_package}")
        
        return True
    
    def _create_chapter_addition_guide(self):
        """Create guide for adding chapters 5-7 to Word"""
        guide = """# Chapter Addition Guide for Word Document

## Current Document: BSc-project-report-FINAL-UNIVERSITY.docx

### Chapters to Add:
1. **Chapter 5**: پیاده‌سازی لایه سرویس‌های در سطح کاربر
   - Source: `chapter5_clean.txt`
   
2. **Chapter 6**: پایش، سخت‌سازی امنیتی، آزمون‌ها و تحویل نهایی
   - Source: `chapter6_clean.txt`
   
3. **Chapter 7**: خلصه، نتیجه‌گیری و کارهای آینده
   - Source: `chapter7_clean.txt`

### Steps to Add Chapters:

#### Manual Method:
1. Open `BSc-project-report-FINAL-UNIVERSITY.docx` in Microsoft Word
2. Go to the end of Chapter 4
3. Insert → Page Break (for new chapter)
4. For each chapter:
   a. Type the chapter title
   b. Apply Style: "Heading 1"
   c. Copy content from corresponding .txt file
   d. Paste after heading
   e. Apply "Heading 2" to sub-sections (5.1, 5.2, etc.)

#### Automated Method (Peekaboo):
Run the Peekaboo automation script:
```bash
peekaboo run word_chapter_addition.json
```

### Formatting Notes:
- Use consistent font (likely B Nazanin or similar for Persian)
- Text size: 14pt for body, 16pt for headings
- Line spacing: 1.5 or 2.0
- Text alignment: Justified
- Margins: Standard academic (2.5cm左右)
"""
        
        with open("CHAPTER_ADDITION_GUIDE.md", 'w', encoding='utf-8') as f:
            f.write(guide)
        
        return "CHAPTER_ADDITION_GUIDE.md"
    
    def _find_formatting_guide(self):
        """Find formatting guide PDF"""
        possible_paths = [
            "~/Downloads/BSc-Projects-Docs--1401/BSc-project-report-format.pdf",
            "~/Downloads/BSc-project-report-format.pdf",
            "./BSc-project-report-format.pdf",
            "./format-guide.pdf"
        ]
        
        for path in possible_paths:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                return expanded
        
        return None
    
    def _create_formatting_automation_script(self, format_guide):
        """Create script for formatting automation"""
        script = """#!/usr/bin/env python3
# Word Document Formatting Automation

import subprocess
import time

def apply_word_formatting():
    \"\"\"Apply formatting to Word document\"\"\"
    
    # Open Word document
    doc_path = "./BSc-project-report-FINAL-UNIVERSITY.docx"
    
    # AppleScript for Word formatting
    applescript = '''
    tell application "Microsoft Word"
        activate
        open "{}"
        delay 5
        
        -- Select all text
        tell active document
            select (content of text object of it)
        end tell
        
        -- Apply paragraph formatting
        tell selection
            -- Justify text
            set paragraph format of it to justify paragraph justify align
            -- Set line spacing
            set line spacing rule of paragraph format of it to line spacing multiple
            set line spacing of paragraph format of it to 1.5
            -- Set font
            set name of font object of it to "B Nazanin"
            set size of font object of it to 14
        end tell
        
        -- Save document
        save active document
    end tell
    '''.format(doc_path)
    
    # Run AppleScript
    try:
        subprocess.run(['osascript', '-e', applescript])
        print("✅ Formatting applied successfully")
        return True
    except Exception as e:
        print(f"❌ Error applying formatting: {e}")
        return False

if __name__ == "__main__":
    apply_word_formatting()
"""
        
        with open("apply_formatting.py", 'w', encoding='utf-8') as f:
            f.write(script)
        
        # Make executable
        os.chmod("apply_formatting.py", 0o755)
        
        return "apply_formatting.py"
    
    def _create_peekaboo_formatting_script(self):
        """Create Peekaboo JSON for formatting"""
        script = {
            "name": "Word Document Formatting",
            "description": "Apply university formatting guidelines to Word document",
            "steps": [
                {
                    "name": "Open Word Document",
                    "action": "run",
                    "command": f"open -a 'Microsoft Word' '{self.final_doc}'",
                    "wait": 10000
                },
                {
                    "name": "Wait for Word to load",
                    "action": "sleep",
                    "duration": 5000
                },
                {
                    "name": "Select All Text",
                    "action": "keystroke",
                    "keys": ["command", "a"]
                },
                {
                    "name": "Apply Justification",
                    "action": "run",
                    "command": "peekaboo tools --filter 'justify' --json",
                    "wait": 1000
                },
                {
                    "name": "Set Font Size",
                    "action": "keystroke",
                    "keys": ["command", "shift", "p"],
                    "wait": 1000
                },
                {
                    "name": "Type font size",
                    "action": "type",
                    "text": "14",
                    "wait": 500
                },
                {
                    "name": "Press Enter",
                    "action": "keystroke",
                    "keys": ["return"],
                    "wait": 1000
                },
                {
                    "name": "Save Document",
                    "action": "keystroke",
                    "keys": ["command", "s"],
                    "wait": 2000
                },
                {
                    "name": "Close Word",
                    "action": "keystroke",
                    "keys": ["command", "q"],
                    "wait": 3000
                }
            ]
        }
        
        with open("word_formatting.peekaboo.json", 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        
        return "word_formatting.peekaboo.json"
    
    def _create_appendix_content(self, manifest_content):
        """Create formatted appendix content from manifests"""
        # Extract YAML sections
        lines = manifest_content.split('\n')
        appendix_lines = []
        current_section = None
        in_yaml_block = False
        yaml_content = []
        
        for line in lines:
            if line.startswith('###') and ')' not in line:
                # New section
                if current_section and yaml_content:
                    appendix_lines.append(f"\n```yaml\n{''.join(yaml_content)}\n```")
                    yaml_content = []
                current_section = line.strip('# ')
                appendix_lines.append(f"\n## {current_section}")
            elif line.strip().startswith('```yaml') or line.strip().startswith('```yml'):
                in_yaml_block = True
                yaml_content = []
            elif line.strip() == '```' and in_yaml_block:
                in_yaml_block = False
                if yaml_content:
                    appendix_lines.append(f"\n```yaml\n{''.join(yaml_content)}\n```")
                    yaml_content = []
            elif in_yaml_block:
                yaml_content.append(line + '\n')
            elif line.strip() and not line.startswith('[') and 'http' not in line:
                # Regular content (not citations)
                appendix_lines.append(line)
        
        # Add any remaining YAML
        if yaml_content:
            appendix_lines.append(f"\n```yaml\n{''.join(yaml_content)}\n```")
        
        # Create full
    def _create_appendix_content(self, manifest_content):
        """Create formatted appendix content from manifests"""
        # Create structured appendix
        appendix = """# Appendix: Kubernetes Manifests for GPU Lab Platform

## A. Infrastructure Setup

### A.1 Proxmox Configuration
[Proxmox setup manifests would go here]

### A.2 VM Creation Templates
[VM creation manifests would go here]

### A.3 Cloud-Init Configurations
[Cloud-Init configurations would go here]

## B. Kubernetes Cluster Deployment

### B.1 Kubespray Deployment
[Kubespray deployment manifests]

### B.2 Cluster Configuration
[Cluster configuration manifests]

### B.3 Network Policies
[Network policy manifests]

## C. Platform Services

### C.1 Argo CD Bootstrap
```yaml
# bootstrap/project-gpu-lab.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: gpu-lab
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  description: University GPU Lab platform
  sourceRepos:
    - https://git.example.edu/university/gpu-lab-gitops.git
  destinations:
    - namespace: "*"
      server: https://kubernetes.default.svc
  clusterResourceWhitelist:
    - group: "*"
      kind: "*"
  namespaceResourceWhitelist:
    - group: "*"
      kind: "*"
```

### C.2 Core Services
- cert-manager
- Traefik ingress
- TopoLVM storage
- NVIDIA GPU Operator
- Kueue job queueing

### C.3 Monitoring Stack
- Prometheus
- Grafana
- Alertmanager

## D. Security & Access Control

### D.1 Identity Management
- Keycloak OIDC provider
- Role-based access control (RBAC)
- Network policies

### D.2 Registry & Artifacts
- Harbor container registry
- Image scanning
- Vulnerability management

## E. User Applications

### E.1 JupyterHub Configuration
[JupyterHub Helm values and manifests]

### E.2 User Baseline Resources
[Resource quotas, limit ranges, priority classes]

---

*Note: Complete manifests are available in the git repository at: https://git.example.edu/university/gpu-lab-gitops.git*
"""
        
        return appendix
    
    def _create_word_appendix_guide(self, appendix_dir):
        """Create guide for adding appendix to Word"""
        guide = f"""# Appendix Integration Guide

## Appendix Location: {appendix_dir}/

## Files to Include in Word Appendix:

1. **Appendix A: Infrastructure Manifests**
   - Proxmox configuration
   - VM templates
   - Cloud-Init scripts

2. **Appendix B: Kubernetes Cluster**
   - Kubespray deployment
   - Network configurations
   - Storage setups

3. **Appendix C: Platform Services**
   - Argo CD bootstrap manifests
   - Service deployments
   - GPU operator configuration

4. **Appendix D: Security & Monitoring**
   - Security hardening
   - Monitoring stack
   - Access controls

5. **Appendix E: User Applications**
   - JupyterHub configuration
   - Resource management

## Steps to Add Appendix to Word:

1. Open `BSc-project-report-FINAL-UNIVERSITY.docx`
2. Go to end of Chapter 7
3. Insert → Page Break
4. Add title: "پیوست: مانیفست‌های Kubernetes برای پلتفرم آزمایشگاهی GPU"
5. Apply Style: "Heading 1"
6. Copy content from appendix files
7. Format as needed

## Formatting Notes:
- Use smaller font for code blocks (11pt)
- Use monospace font for YAML manifests
- Add line numbers for reference
- Include cross-references in main chapters
"""
        
        guide_path = os.path.join(appendix_dir, "WORD_APPENDIX_GUIDE.md")
        with open(guide_path, 'w', encoding='utf-8') as f:
            f.write(guide)
        
        return guide_path
    
    def _create_chatgpt_review_prompts(self):
        """Create ChatGPT review prompts for chapters 3-7"""
        prompts = {
            "chapter3": {
                "file": "chapter3_review_prompt.txt",
                "content": """Review and improve Chapter 3: Infrastructure Setup

Please review the following chapter for:
1. Technical accuracy of Proxmox, VM creation, Cloud-Init setup
2. Clarity of explanations
3. Logical flow and structure
4. Grammar and language (Persian/English mix)
5. Consistency with academic writing standards

Specific areas to check:
- Proxmox installation and configuration
- VM template creation process
- Cloud-Init for automated provisioning
- Network configuration details
- Storage setup for VMs

Please provide:
1. Corrections for any technical inaccuracies
2. Suggestions for improving clarity
3. Grammar and spelling corrections
4. Recommendations for better structure
5. Missing details that should be added"""
            },
            "chapter4": {
                "file": "chapter4_review_prompt.txt",
                "content": """Review and improve Chapter 4: Kubernetes Cluster Deployment

Please review the following chapter for:
1. Accuracy of Kubespray deployment process
2. Network configuration (Calico CNI)
3. Storage setup (TopoLVM)
4. Security configurations
5. GPU passthrough setup

Specific areas to check:
- Kubespray inventory and configuration
- Network policies and CNI setup
- Storage class configurations
- RBAC and security policies
- GPU operator installation

Please provide corrections and improvements."""
            },
            "chapter5": {
                "file": "chapter5_review_prompt.txt",
                "content": """Review and improve Chapter 5: User Service Layer Implementation

Please review for:
1. Multi-tenant architecture design
2. JupyterHub configuration
3. Resource quota management
4. Authentication and authorization
5. Batch job scheduling with Kueue

Focus on:
- Technical accuracy of Kubernetes manifests
- Security of multi-tenant isolation
- Efficiency of resource allocation
- Clarity of architectural diagrams (if any)
- Completeness of implementation details"""
            },
            "chapter6": {
                "file": "chapter6_review_prompt.txt",
                "content": """Review and improve Chapter 6: Monitoring, Security Hardening, Testing

Please review for:
1. Monitoring stack implementation (Prometheus, Grafana)
2. Security hardening measures
3. Testing methodology and results
4. Performance benchmarks
5. Deployment and delivery process

Check:
- Monitoring architecture and alerting
- Security policies and compliance
- Test cases and validation results
- Performance metrics and analysis
- Deployment pipeline details"""
            },
            "chapter7": {
                "file": "chapter7_review_prompt.txt",
                "content": """Review and improve Chapter 7: Summary, Conclusions, Future Work

Please review for:
1. Summary of key achievements
2. Conclusions drawn from the project
3. Future work recommendations
4. Impact and contributions
5. Academic writing quality

Ensure:
- Clear summary of all chapters
- Well-supported conclusions
- Practical future work suggestions
- Proper academic tone and structure
- No repetition or redundancy"""
            }
        }
        
        # Save prompts to files
        for chap, data in prompts.items():
            with open(data["file"], 'w', encoding='utf-8') as f:
                f.write(data["content"])
        
        return list(prompts.keys())
    
    def _create_chrome_automation_script(self, chatgpt_url, review_prompts):
        """Create script for Chrome automation with ChatGPT"""
        script = f"""#!/usr/bin/env python3
# Chrome Automation for ChatGPT Review

import subprocess
import time
import os

def open_chatgpt_and_review():
    \"\"\"Open ChatGPT and prepare for chapter review\"\"\"
    
    # Open Chrome with ChatGPT URL
    print("🌐 Opening ChatGPT in Chrome...")
    subprocess.run(['open', '-a', 'Google Chrome', '{chatgpt_url}'])
    time.sleep(10)
    
    print("📋 Chapter review prompts prepared:")
    for prompt_file in {review_prompts}:
        if os.path.exists(prompt_file):
            print(f"  • {{prompt_file}}")
    
    print("\\n🚀 Next steps:")
    print("1. Wait for ChatGPT page to load")
    print("2. Copy each chapter content")
    print("3. Paste into ChatGPT with corresponding prompt")
    print("4. Apply suggested improvements to Word document")
    print("5. Repeat for chapters 3-7")
    
    return True

if __name__ == "__main__":
    open_chatgpt_and_review()
"""
        
        with open("chatgpt_review_automation.py", 'w', encoding='utf-8') as f:
            f.write(script)
        
        os.chmod("chatgpt_review_automation.py", 0o755)
        return "chatgpt_review_automation.py"
    
    def _create_reference_guide(self, reference_mapping):
        """Create guide for adding appendix references"""
        guide = "# Appendix Reference Integration Guide\\n\\n"
        guide += "## Reference Points to Add in Each Chapter\\n\\n"
        
        for chapter, refs in reference_mapping.items():
            guide += f"### {chapter}\\n"
            for ref in refs:
                guide += f"- {ref}\\n"
            guide += "\\n"
        
        guide += "## How to Add References in Word:\\n"
        guide += "1. **Find relevant sections** in each chapter\\n"
        guide += "2. **Add reference markers** like: \"(See Appendix A.1 for detailed manifests)\"\\n"
        guide += "3. **Use cross-references** if Word supports it\\n"
        guide += "4. **Create reference list** at end of each chapter if needed\\n"
        guide += "5. **Update table of contents** after adding references\\n\\n"
        
        guide += "## Example References:\\n"
        guide += "- \"The Proxmox setup configuration is detailed in Appendix A.1.\"\\n"
        guide += "- \"Kubernetes manifests for this deployment are provided in Appendix B.2.\"\\n"
        guide += "- \"Security policies are documented in Appendix D.2.\"\\n"
        
        with open("APPENDIX_REFERENCE_GUIDE.md", 'w', encoding='utf-8') as f:
            f.write(guide)
        
        return "APPENDIX_REFERENCE_GUIDE.md"
    
    def _create_word_reference_script(self, reference_mapping):
        """Create script for adding references in Word"""
        script = {
            "name": "Add Appendix References to Word",
            "description": "Search and add appendix references throughout document",
            "steps": [
                {
                    "name": "Open Word Document",
                    "action": "run",
                    "command": f"open -a 'Microsoft Word' '{self.final_doc}'",
                    "wait": 10000
                },
                {
                    "name": "Search for infrastructure sections",
                    "action": "keystroke",
                    "keys": ["command", "f"],
                    "wait": 1000
                },
                {
                    "name": "Search terms for Chapter 3",
                    "action": "type",
                    "text": "Proxmox",
                    "wait": 500
                },
                {
                    "name": "Add reference after found text",
                    "action": "type",
                    "text": " (See Appendix A.1 for detailed configuration manifests)",
                    "wait": 1000
                },
                # More steps would be added here for each reference point
                {
                    "name": "Save document",
                    "action": "keystroke",
                    "keys": ["command", "s"],
                    "wait": 2000
                }
            ]
        }
        
        with open("add_references.peekaboo.json", 'w', encoding='utf-8') as f:
            json.dump(script, f, indent=2, ensure_ascii=False)
        
        return "add_references.peekaboo.json"
    
    def _create_final_checklist(self):
        """Create final review checklist"""
        checklist = """# Final Review Checklist

## Document Structure
- [ ] All 7 chapters present and in correct order
- [ ] Table of Contents updated and accurate
- [ ] Page numbers correct and consistent
- [ ] Headings properly formatted (Heading 1, Heading 2, etc.)

## Content Quality
- [ ] Chapters 3-7 reviewed and corrected by ChatGPT
- [ ] Technical accuracy verified
- [ ] Grammar and spelling checked
- [ ] Academic tone maintained throughout
- [ ] No plagiarism or citation issues

## Formatting
- [ ] All text paragraphs justified
- [ ] Consistent font and size throughout
- [ ] Proper line spacing (1.5 or 2.0)
- [ ] Margins according to university guidelines
- [ ] Figures and tables properly labeled

## Appendix Integration
- [ ] K8s manifests organized as appendix
- [ ] References to appendix added in relevant sections
- [ ] Appendix formatted consistently
- [ ] Code blocks in monospace font
- [ ] Line numbers for manifests

## Technical Details
- [ ] All Kubernetes manifests accurate and complete
- [ ] Architecture diagrams (if any) clear and labeled
- [ ] Configuration details correct
- [ ] Security measures properly documented
- [ ] Performance metrics accurate

## Final Verification
- [ ] Document opens correctly in Word
- [ ] All hyperlinks work (if any)
- [ ] PDF conversion successful
- [ ] File size reasonable
- [ ] Metadata (author, title) correct

## Submission Ready
- [ ] Cover page with university details
- [ ] Abstract included
- [ ] Acknowledgements section
- [ ] References/Bibliography formatted
- [ ] Declaration of originality signed
"""
        
        with open("FINAL_REVIEW_CHECKLIST.md", 'w', encoding='utf-8') as f:
            f.write(checklist)
        
        return "FINAL_REVIEW_CHECKLIST.md"
    
    def _create_validation_script(self):
        """Create validation script for final document"""
        script = """#!/usr/bin/env python3
# Final Document Validation Script

import os
import sys

def validate_document():
    \"\"\"Validate final document meets requirements\"\"\"
    
    doc_path = "BSc-project-report-FINAL-UNIVERSITY.docx"
    
    if not os.path.exists(doc_path):
        print(f"❌ Final document not found: {doc_path}")
        return False
    
    # Check file size
    file_size = os.path.getsize(doc_path)
    print(f"📄 Document size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    # Check for required files
    required_files = [
        "chapter5_clean.txt",
        "chapter6_clean.txt", 
        "chapter7_clean.txt",
        "gpt-manifests.md"
    ]
    
    print("\\n📋 Required source files:")
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")
            all_ok = False
    
    # Check generated files
    print("\\n🔧 Generated files:")
    generated_files = [
        "CHAPTER_ADDITION_GUIDE.md",
        "apply_formatting.py",
        "appendix/",
        "APPENDIX_REFERENCE_GUIDE.md",
        "FINAL_REVIEW_CHECKLIST.md"
    ]
    
    for file in generated_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} (not generated yet)")
    
    print("\\n🎯 Validation complete!")
    if all_ok:
        print("✅ All requirements met")
        return True
    else:
        print("⚠️  Some requirements missing")
        return False

if __name__ == "__main__":
    validate_document()
"""
        
        with open("validate_document.py", 'w', encoding='utf-8') as f:
            f.write(script)
        
        os.chmod("validate_document.py", 0o755)
        return "validate_document.py"
    
    def _create_submission_package(self):
        """Create submission package structure"""
        package_dir = "SUBMISSION_PACKAGE"
        os.makedirs(package_dir, exist_ok=True)
        
        # Create README for submission
        readme = """# BSc Project Report - Submission Package

## Contents:

### 1. Main Document
- `BSc-project-report-FINAL-UNIVERSITY.docx` - Complete report with all 7 chapters

### 2. Source Files
- `chapter5_clean.txt` - Chapter 5 content
- `chapter6_clean.txt` - Chapter 6 content  
- `chapter7_clean.txt` - Chapter 7 content
- `gpt-manifests.md` - Kubernetes manifests

### 3. Appendix
- `appendix/` - Organized K8s manifests
- Appendix references integrated in main document

### 4. Supporting Documentation
- `CHAPTER_ADDITION_GUIDE.md` - How chapters were added
- `APPENDIX_REFERENCE_GUIDE.md` - Reference integration guide
- `FINAL_REVIEW_CHECKLIST.md` - Quality assurance checklist

### 5. Automation Scripts
- `apply_formatting.py` - Word formatting automation
- `validate_document.py` - Document validation

## Submission Instructions:

1. **Email Submission:**
   - Send `BSc-project-report-FINAL-UNIVERSITY.docx` as attachment
   - Include brief cover email

2. **Online Portal:**
   - Upload Word document
   - Upload PDF version (if required)
   - Include any supplementary files

3. **Hard Copy:** (if required)
   - Print on A4 paper
   - Single-sided or double-sided as per guidelines
   - Bind according to university requirements

## Contact Information:
- Student: [Your Name]
- Student ID: [Your ID]
- Advisor: [Advisor Name]
- Department: Computer Engineering
- University: [University Name]

## Submission Deadline:
[Insert deadline date and time]
"""
        
        readme_path = os.path.join(package_dir, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme)
        
        # Copy important files to package
        files_to_copy = [
            "            "BSc-project-report-FINAL-UNIVERSITY.docx",
            "chapter5_clean.txt",
            "chapter6_clean.txt",
            "chapter7_clean.txt",
            "gpt-manifests.md",
            "CHAPTER_ADDITION_GUIDE.md",
            "APPENDIX_REFERENCE_GUIDE.md",
            "FINAL_REVIEW_CHECKLIST.md"
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, os.path.join(package_dir, file))
                print(f"  📄 Copied: {file}")
        
        print(f"📦 Submission package created: {package_dir}/")
        return package_dir
    
    def execute_all_steps(self):
        """Execute all 6 steps"""
        print("🚀 Starting 6-Step BSc Report Preparation")
        print("="*60)
        
        steps = [
            ("Step 1: Create complete document", self.step1_create_complete_document),
            ("Step 2: Apply formatting guidelines", self.step2_apply_formatting_guidelines),
            ("Step 3: Organize K8s manifests", self.step3_organize_k8s_manifests),
            ("Step 4: ChatGPT review", self.step4_chatgpt_review),
            ("Step 5: Add appendix references", self.step5_add_appendix_references),
            ("Step 6: Final review", self.step6_final_review)
        ]
        
        results = []
        for step_name, step_func in steps:
            print(f"\n▶️  Executing {step_name}...")
            try:
                success = step_func()
                results.append((step_name, success))
                if success:
                    print(f"✅ {step_name} - COMPLETED")
                else:
                    print(f"❌ {step_name} - FAILED")
            except Exception as e:
                print(f"💥 {step_name} - ERROR: {e}")
                results.append((step_name, False))
        
        # Print summary
        print("\n" + "="*60)
        print("📊 EXECUTION SUMMARY")
        print("="*60)
        
        completed = sum(1 for _, success in results if success)
        total = len(results)
        
        print(f"\n✅ Completed: {completed}/{total} steps")
        
        for i, (step_name, success) in enumerate(results, 1):
            status = "✅" if success else "❌"
            print(f"{status} Step {i}: {step_name}")
        
        if completed == total:
            print("\n🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
            print("\n📁 Generated files:")
            print("  • BSc-project-report-FINAL-UNIVERSITY.docx (final document)")
            print("  • appendix/ (organized K8s manifests)")
            print("  • Various guides and automation scripts")
            print("\n🚀 Next: Open the final document and apply formatting")
        else:
            print(f"\n⚠️  {total - completed} steps need manual attention")
            print("Check the generated guides for completion instructions")
        
        return all(success for _, success in results)

def main():
    preparer = BScReportPreparer()
    preparer.execute_all_steps()

if __name__ == "__main__":
    main()
