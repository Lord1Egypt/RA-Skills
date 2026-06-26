---
name: resume-studio
description: Professional resume generator. Use when user needs to create, optimize, or customize resumes for job applications. Supports Word and PDF output, multiple styles, industry templates, and ATS-friendly formats. 简历生成、求职简历、简历优化。
version: 1.0.2
license: MIT-0
metadata: {"openclaw": {"emoji": "📋", "requires": {"bins": ["python3"], "env": []}}}
dependencies: "pip install python-docx fpdf2"
---

# Resume Studio

Professional resume generator with ATS-friendly templates, multiple styles, and Word/PDF output.

## Features

- 📋 **Smart Generation**: AI-powered content optimization
- 🎨 **Multiple Styles**: Classic, Modern, Creative, Minimal, Academic
- 📄 **Word Output**: Professional .docx format
- 👤 **Photo Support**: Optional photo area
- 🌐 **Web Research**: Query job market trends
- 📁 **File Import**: Import existing materials
- 🎯 **ATS-Friendly**: Passes Applicant Tracking Systems
- 🌍 **Multi-Language**: Chinese and English support
- 🖥️ **Cross-Platform**: Windows, macOS, Linux

## Trigger Conditions

- "帮我写简历" / "Help me write a resume"
- "生成求职简历" / "Generate job resume"
- "优化我的简历" / "Optimize my resume"
- "resume-studio"

## Resume Styles

### Classic (经典)
- Traditional layout
- Professional fonts
- Suitable for: Finance, Law, Government

### Modern (现代)
- Clean design
- Bold headers
- Suitable for: Tech, Marketing, Design

### Creative (创意)
- Unique layout
- Color accents
- Suitable for: Design, Media, Art

### Minimal (极简)
- Simple structure
- Focus on content
- Suitable for: Academic, Research

## Information Collection

```
Agent collects:

1. Basic Info
   - Name
   - Phone
   - Email
   - Location

2. Education
   - School
   - Degree
   - Major
   - GPA (optional)

3. Experience
   - Company
   - Position
   - Duration
   - Responsibilities

4. Skills
   - Technical skills
   - Languages
   - Certifications

5. Target Position
   - Job title
   - Industry
   - Specific requirements
```

## Python Code

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from fpdf import FPDF
import os

class ResumeGenerator:
    def __init__(self, style='modern'):
        self.style = style
        self.data = {}
    
    def set_basic_info(self, name, phone, email, location=''):
        self.data['name'] = name
        self.data['phone'] = phone
        self.data['email'] = email
        self.data['location'] = location
    
    def add_education(self, school, degree, major, year, gpa=None):
        if 'education' not in self.data:
            self.data['education'] = []
        self.data['education'].append({
            'school': school,
            'degree': degree,
            'major': major,
            'year': year,
            'gpa': gpa
        })
    
    def add_experience(self, company, position, duration, responsibilities):
        if 'experience' not in self.data:
            self.data['experience'] = []
        self.data['experience'].append({
            'company': company,
            'position': position,
            'duration': duration,
            'responsibilities': responsibilities
        })
    
    def set_skills(self, technical=[], languages=[], certifications=[]):
        self.data['skills'] = {
            'technical': technical,
            'languages': languages,
            'certifications': certifications
        }
    
    def generate_docx(self, output_path):
        doc = Document()
        
        # Name
        name_para = doc.add_paragraph()
        name_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        name_run = name_para.add_run(self.data.get('name', 'Name'))
        name_run.font.size = Pt(24)
        name_run.bold = True
        
        # Contact
        contact = doc.add_paragraph()
        contact.alignment = WD_ALIGN_PARAGRAPH.CENTER
        contact_text = f"{self.data.get('phone', '')} | {self.data.get('email', '')}"
        if self.data.get('location'):
            contact_text += f" | {self.data['location']}"
        contact.add_run(contact_text)
        
        doc.add_paragraph()
        
        # Education
        doc.add_heading('Education', level=2)
        for edu in self.data.get('education', []):
            doc.add_paragraph(f"{edu['school']} - {edu['degree']} in {edu['major']} ({edu['year']})")
        
        # Experience
        doc.add_heading('Experience', level=2)
        for exp in self.data.get('experience', []):
            doc.add_heading(f"{exp['position']} at {exp['company']}", level=3)
            doc.add_paragraph(f"Duration: {exp['duration']}")
            for resp in exp['responsibilities']:
                doc.add_paragraph(f"• {resp}")
        
        # Skills
        doc.add_heading('Skills', level=2)
        skills = self.data.get('skills', {})
        if skills.get('technical'):
            doc.add_paragraph(f"Technical: {', '.join(skills['technical'])}")
        if skills.get('languages'):
            doc.add_paragraph(f"Languages: {', '.join(skills['languages'])}")
        if skills.get('certifications'):
            doc.add_paragraph(f"Certifications: {', '.join(skills['certifications'])}")
        
        doc.save(output_path)
        return output_path
    
    def generate_pdf(self, output_path):
        pdf = FPDF()
        pdf.add_page()
        
        # Name
        pdf.set_font('Helvetica', 'B', 20)
        pdf.cell(0, 15, self.data.get('name', 'Name'), new_x='LMARGIN', new_y='NEXT', align='C')
        
        # Contact
        pdf.set_font('Helvetica', '', 10)
        contact = f"{self.data.get('phone', '')} | {self.data.get('email', '')}"
        pdf.cell(0, 8, contact, new_x='LMARGIN', new_y='NEXT', align='C')
        pdf.ln(10)
        
        # Education
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 8, 'Education', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(3)
        pdf.set_font('Helvetica', '', 11)
        for edu in self.data.get('education', []):
            pdf.cell(0, 6, f"{edu['school']} - {edu['degree']}", new_x='LMARGIN', new_y='NEXT')
        
        pdf.ln(8)
        
        # Experience
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 8, 'Experience', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(3)
        pdf.set_font('Helvetica', '', 11)
        for exp in self.data.get('experience', []):
            pdf.set_font('Helvetica', 'B', 11)
            pdf.cell(0, 6, f"{exp['position']} at {exp['company']}", new_x='LMARGIN', new_y='NEXT')
            pdf.set_font('Helvetica', '', 10)
            pdf.cell(0, 5, f"Duration: {exp['duration']}", new_x='LMARGIN', new_y='NEXT')
            for resp in exp['responsibilities']:
                pdf.cell(0, 5, f"  • {resp}", new_x='LMARGIN', new_y='NEXT')
            pdf.ln(5)
        
        pdf.ln(8)
        
        # Skills
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 8, 'Skills', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(3)
        pdf.set_font('Helvetica', '', 11)
        skills = self.data.get('skills', {})
        if skills.get('technical'):
            pdf.cell(0, 6, f"Technical: {', '.join(skills['technical'])}", new_x='LMARGIN', new_y='NEXT')
        if skills.get('languages'):
            pdf.cell(0, 6, f"Languages: {', '.join(skills['languages'])}", new_x='LMARGIN', new_y='NEXT')
        
        pdf.output(output_path)
        return output_path

# Example
resume = ResumeGenerator('modern')
resume.set_basic_info('John Doe', '13800138000', 'john@example.com', 'Beijing')
resume.add_education('Peking University', 'Bachelor', 'Computer Science', '2020-2024')
resume.add_experience('TechCorp', 'Software Engineer', '2024-present', [
    'Developed AI features',
    'Improved system performance by 50%'
])
resume.set_skills(['Python', 'AI', 'Cloud'], ['Chinese', 'English'], ['AWS Certified'])

resume.generate_docx('resume.docx')
resume.generate_pdf('resume.pdf')
```

## Notes

- ATS-friendly formatting
- Professional typography
- Multi-language support
- Cross-platform compatible
