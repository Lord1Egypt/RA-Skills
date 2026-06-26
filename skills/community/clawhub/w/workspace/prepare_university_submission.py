#!/usr/bin/env python3
"""
Prepare BSc project report for university submission
"""

import os
import sys
import shutil
from datetime import datetime
import subprocess

def check_document(file_path):
    """Check if document exists and is valid"""
    if not os.path.exists(file_path):
        print(f"❌ Document not found: {file_path}")
        return False
    
    file_size = os.path.getsize(file_path)
    print(f"✅ Document found: {file_path}")
    print(f"📄 File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    # Check if it's a valid .docx file
    if not file_path.lower().endswith('.docx'):
        print("⚠️  Warning: File doesn't have .docx extension")
    
    return True

def create_backup(file_path):
    """Create timestamped backup"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"BSc-project-report-BACKUP-{timestamp}.docx"
    backup_path = os.path.join(os.path.dirname(file_path), backup_name)
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup created: {backup_name}")
        return backup_path
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")
        return None

def check_conversion_tools():
    """Check available conversion tools"""
    tools = {
        'libreoffice': False,
        'soffice': False,
        'pandoc': False,
        'docx2pdf': False,
        'python_comtypes': False
    }
    
    # Check command line tools
    for tool in ['libreoffice', 'soffice', 'pandoc', 'docx2pdf']:
        try:
            subprocess.run(['which', tool], capture_output=True, check=False)
            tools[tool] = True
        except:
            pass
    
    # Check Python libraries
    try:
        import comtypes
        tools['python_comtypes'] = True
    except ImportError:
        pass
    
    print("\n🛠️  Available conversion tools:")
    for tool, available in tools.items():
        status = "✅" if available else "❌"
        print(f"  {status} {tool}")
    
    return tools

def create_submission_checklist():
    """Create submission checklist"""
    checklist = """# 📋 University Submission Checklist - BSc Project Report

## ✅ **Document Preparation**
- [ ] Report is complete (all 7 chapters)
- [ ] Formatting matches university template
- [ ] Page numbers are correct
- [ ] Table of Contents is updated
- [ ] References are properly formatted
- [ ] No spelling/grammar errors

## 📄 **File Preparation**
- [ ] Final .docx file ready
- [ ] PDF version created (if required)
- [ ] Backup copy saved
- [ ] File name follows university format

## 📧 **Submission Preparation**
- [ ] University email address verified
- [ ] Submission deadline confirmed
- [ ] Required attachments identified
- [ ] Cover letter/email drafted
- [ ] CC to advisor if required

## 🔒 **Final Checks**
- [ ] Document opens correctly
- [ ] All images/tables display properly
- [ ] File size is reasonable
- [ ] Metadata (author, title) is correct

## 🚀 **Submission Steps**
1. **Email Subject:** BSc Project Report - [Your Name] - [Student ID]
2. **Email Body:** Brief cover letter with project title, your details, advisor name
3. **Attachments:** Report (.docx/.pdf), any supplementary files
4. **Send to:** [University submission email]
5. **CC:** [Your advisor's email]
6. **Confirm receipt** with department office

## 📞 **Contact Information**
- Department Office: [Phone/Email]
- Advisor: [Name, Email]
- Submission Deadline: [Date]

**Good luck with your submission!** 🎓
"""
    
    checklist_path = "UNIVERSITY_SUBMISSION_CHECKLIST.md"
    with open(checklist_path, 'w', encoding='utf-8') as f:
        f.write(checklist)
    
    print(f"\n✅ Submission checklist created: {checklist_path}")
    return checklist_path

def create_email_template():
    """Create email template for submission"""
    email_template = """Subject: ارسال پروژه پایانی کارشناسی - [عنوان پروژه]

سلام بر استاد محترم/اداره آموزش،

با سلام و احترام،

بدین وسیله پروژه پایانی کارشناسی خود با عنوان:

«[عنوان کامل پروژه]»

را جهت بررسی و ارزیابی ارسال می‌کنم.

مشخصات دانشجو:
- نام و نام خانوادگی: [نام شما]
- شماره دانشجویی: [شماره دانشجویی]
- رشته: مهندسی کامپیوتر
- مقطع: کارشناسی
- استاد راهنما: [نام استاد راهنما]

مشخصات پروژه:
- عنوان: [عنوان پروژه]
- مدت زمان اجرا: [مدت زمان]
- تکنولوژی‌های استفاده شده: [فهرست تکنولوژی‌ها]
- فایل‌های پیوست:
  1. گزارش کامل پروژه (فایل Word)
  2. [سایر فایل‌های مورد نیاز]

لطفاً در صورت نیاز به اطلاعات بیشتر یا اصلاحات، مرا مطلع فرمایید.

با تشکر
[نام شما]
[شماره تماس]
[ایمیل]

---
English Version (if needed):

Subject: Submission of BSc Final Project - [Project Title]

Dear Professor/Academic Office,

I am writing to submit my Bachelor's final project titled:

"[Full Project Title]"

for review and evaluation.

Student Information:
- Full Name: [Your Name]
- Student ID: [Student ID]
- Major: Computer Engineering
- Degree: Bachelor's
- Advisor: [Advisor's Name]

Project Details:
- Title: [Project Title]
- Duration: [Duration]
- Technologies Used: [List of Technologies]
- Attached Files:
  1. Complete project report (Word document)
  2. [Other required files]

Please let me know if you need any further information or revisions.

Best regards,
[Your Name]
[Phone Number]
[Email]
"""
    
    email_path = "EMAIL_TEMPLATE_FOR_SUBMISSION.txt"
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(email_template)
    
    print(f"\n📧 Email template created: {email_path}")
    return email_path

def main():
    print("🎓 BSc Project Report - University Submission Preparation")
    print("=" * 60)
    
    # Document to process
    doc_file = "BSc-project-report-COMPLETE.docx"
    
    # Step 1: Check document
    print("\n1. 📄 Checking document...")
    if not check_document(doc_file):
        return
    
    # Step 2: Create backup
    print("\n2. 💾 Creating backup...")
    create_backup(doc_file)
    
    # Step 3: Check conversion tools
    print("\n3. 🛠️  Checking conversion tools...")
    tools = check_conversion_tools()
    
    # Step 4: Create submission checklist
    print("\n4. 📋 Creating submission checklist...")
    checklist = create_submission_checklist()
    
    # Step 5: Create email template
    print("\n5. 📧 Creating email template...")
    email_template = create_email_template()
    
    # Step 6: Summary
    print("\n" + "=" * 60)
    print("🎯 **PREPARATION COMPLETE**")
    print("=" * 60)
    
    print("\n📁 **Generated Files:**")
    print(f"  1. 📄 Backup document: BSc-project-report-BACKUP-*.docx")
    print(f"  2. 📋 Checklist: {checklist}")
    print(f"  3. 📧 Email template: {email_template}")
    
    print("\n🚀 **Next Steps:**")
    print("  1. Review the submission checklist")
    print("  2. Customize the email template with your details")
    print("  3. Convert to PDF if required (see tool availability above)")
    print("  4. Send to university email address")
    print("  5. Confirm receipt with department office")
    
    print("\n💡 **Tips:**")
    print("  • Send during business hours for faster response")
    print("  • Keep all correspondence for your records")
    print("  • Follow up if you don't receive confirmation within 48 hours")
    print("  • Save all files in multiple locations (cloud, external drive)")

if __name__ == "__main__":
    main()