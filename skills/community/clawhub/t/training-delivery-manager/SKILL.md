---
name: training-delivery-manager
description: A comprehensive skill for managing corporate training delivery, including contract generation, travel booking, materials preparation, venue setup, and post-training communications. Use this skill to automate the end-to-end workflow for training projects.
---

# Corporate Training Delivery Manager Skill

This skill automates the standard workflow for corporate training delivery. It provides templates and checklists for the entire process, from contract signing to post-training promotion.

## Main Workflow

At the beginning of the task, ask the user which of the following workflows they need assistance with. This will determine which set of instructions and resources to use.

1.  **商务合同 (Contract Management)**
2.  **预定机票与酒店 (Travel Booking)**
3.  **打印培训课件与各种物料 (Materials Preparation)**
4.  **布置场地 (Venue Setup)**
5.  **培训内部通讯稿与推文 (Post-Training Communications)**

Based on the user's choice, follow the corresponding instructions below.

### 1. 商务合同 (Contract Management)

This workflow generates a formal training cooperation agreement.

1.  **Gather Information**: Ask the user for the following details:
    *   甲方 (Client Name)
    *   培训课程 (Training Course)
    *   授课时间 (Training Dates)
    *   授课地点 (Training Location)
    *   培训费用 (Training Fee)

2.  **Generate Contract**: 
    *   Locate the contract template at `/home/ubuntu/skills/training-delivery-manager/templates/contract_template.docx`.
    *   Create a copy of the template for the new contract.
    *   Programmatically fill in the placeholders in the copied document with the information gathered in the previous step.
    *   Save the finalized contract as `[客户名称]_培训合作协议.docx`.
    *   Deliver the generated Word document to the user.

### 2. 预定机票与酒店 (Travel Booking)

This workflow provides a checklist for booking travel for the trainer.

1.  **Consult the Guide**: Read the travel booking standards and procedures from `/home/ubuntu/skills/training-delivery-manager/references/travel_booking_guide.md`.
2.  **Generate Checklist**: Based on the guide, generate a clear and actionable to-do list for the user. The list should remind the user of the key standards (Economy Class, 4-star hotel) and the booking process.

### 3. 打印培训课件与各种物料 (Materials Preparation)

This workflow provides a comprehensive checklist for all training materials.

1.  **Consult the Checklist**: Read the detailed materials checklist from `/home/ubuntu/skills/training-delivery-manager/references/materials_checklist.md`.
2.  **Present To-Do List**: Present the checklist to the user as a to-do list to ensure all items are prepared.

### 4. 布置场地 (Venue Setup)

This workflow provides a guide for setting up the training venue.

1.  **Consult the Guide**: Read the venue setup instructions from `/home/ubuntu/skills/training-delivery-manager/references/venue_setup_guide.md`.
2.  **Present Checklist**: Present the guide's content to the user as a step-by-step checklist for arranging the venue.

### 5. 培训内部通讯稿与推文 (Post-Training Communications)

This workflow helps create a promotional article and a design brief for a poster.

1.  **Consult the Guide**: First, read the content creation guidelines at `/home/ubuntu/skills/training-delivery-manager/references/communications_guide.md`.

2.  **For the Promotional Article (推文)**:
    *   Ask the user for key details about the training (e.g., theme, highlights, participants, key takeaways).
    *   Use the template at `/home/ubuntu/skills/training-delivery-manager/templates/promotional_article_template.md`.
    *   Fill in the template with the provided details to create a draft of the article.
    *   Deliver the final article as a Markdown file.

3.  **For the Poster (海报)**:
    *   Review the reference image at `/home/ubuntu/skills/training-delivery-manager/templates/poster_reference.jpg` to understand the desired style.
    *   Based on the guidelines in the communications guide and the reference image, generate a design brief. The brief should include:
        *   **Objective**: To create a visually engaging poster summarizing the training event.
        *   **Key Elements**: Main title, client logo, key training highlights, and a selection of high-quality photos.
        *   **Style**: Professional, energetic, and aligned with the client's branding (using red as a primary color, similar to the example).
    *   Deliver this design brief to the user.

## Bundled Resources

- **`templates/`**: Contains ready-to-use templates for contracts and promotional articles, as well as a reference image for poster design.
- **`references/`**: Contains detailed guides and checklists for each step of the workflow. Read these files as needed to perform the tasks.
