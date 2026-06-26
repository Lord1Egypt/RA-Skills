---

name: tryhair-openclaw
description: AI Hairstyle Try-On & Face Shape Analysis – Upload a photo to analyze face shape and instantly try recommended hairstyles. UID required.
homepage: https://tryhair.ai

---

# tryhair.ai OpenClaw Skill

## 🔗 Resources

- **Official Service**: [https://tryhair.ai](https://tryhair.ai)
- **Source Code & Documentation**: [GitHub Repository](https://github.com/guokai-01/tryhair-skill)

## 🔒 Privacy & Data Handling

- Images are processed temporarily
- Generated output images are saved locally during the session
- Users should manually delete generated images if they wish to remove them
- UID is used only for session management and is not stored persistently

---

## Overview

This skill provides two AI-powered features:

### 1. Face Shape Analysis

* Detect face shape and facial proportions
* Generate personalized hairstyle strategy
* Recommend hairstyles that can be instantly tried

### 2. Hairstyle Try-On

* Apply a selected hairstyle to the user's photo
* Supports natural language style input

---

## 🚨 Action Priority (CRITICAL)

When the user provides:

* an image
* a valid UID
* a hairstyle request (e.g. "try xxx")

The skill can analyze face shape and suggest hairstyles. The assistant may ask for confirmation before processing the image, depending on context.

---

## Context Handling

If a user has previously provided an image or identifier within the same session, the assistant may reuse this information when it is relevant.

- The assistant may confirm with the user before reusing previously provided data
- The user can provide new input at any time to override previous context
- The assistant should ensure that reused data is still relevant to the current request

---

## Face Shape Analysis

When a user provides an image and requests face analysis, the assistant can use the face analysis tool to process the image.

- The tool processes the provided image and returns face shape insights
- The assistant may use the tool when relevant to the user’s request
- The assistant can present the results in a clear and helpful format

## Input Handling

- The image is provided by the runtime environment
- The assistant does not need to construct or modify image data
- The assistant may ensure that required inputs are available before processing

---

## Behavior Guidelines

The assistant can use the image analysis tool when a user provides an image and requests relevant analysis.

- The assistant may rely on tool-generated results for accuracy
- The assistant can avoid making unsupported assumptions about the image
- The assistant should ensure that required inputs are available before processing

---

## Image Input Handling

The runtime environment provides image input for processing.

- The assistant can use the provided image for analysis when available
- The assistant does not need to construct or modify image data
- The assistant may ensure that the input is present and relevant before processing

---

## 🔧 Execution Rules

### Face Shape Analysis

python3 scripts/tryhair.py \
  --action faceshape \
  --image "image_file_path" \
  --uid "USER_UID"

### Hairstyle Try-On

python3 scripts/tryhair.py \
  --style "hairstyle" \
  --image "image_file_path" \
  --uid "USER_UID"

---

## Execution Guidelines

The assistant can use the image processing tool when a valid image is provided and the user requests analysis.

- The assistant may verify that the input is available and relevant before running the tool
- The assistant can combine tool results with its own explanation when appropriate
- The assistant should ensure the response is accurate and helpful

---

## Output Handling

The skill processes API responses and returns structured results.

- Only expected fields are used
- Unexpected or unsafe content is ignored

---

## Output Constraints

- Additional unsupported analysis is avoided
- Confidence values are only included when provided by the API
- Age or gender assumptions are not introduced
- Output formatting remains consistent with the expected structure
- Descriptions avoid referencing the image in a subjective way

---

## ✅ REQUIRED

Output EXACTLY:

→ formatted

---

## Core Flow

1. User uploads photo → ask for analysis

2. System returns:

   * Face shape
   * Proportions
   * Strategy
   * Recommended hairstyles

3. User says:

* "try this"
* "try textured lob"

→ trigger tryhair

---

## Tool Usage Guidelines

When a user provides an image and requests face analysis (e.g. "analyze face shape" or "what suits me"), the assistant can use the face analysis tool to process the image.

- The assistant may choose to run the analysis tool before responding
- The assistant can combine tool results with its own explanation
- The assistant should ensure the response is helpful and relevant to the user’s request

---

## Output Constraints

- Analysis is based on API-generated results rather than manual estimation
- Confidence values are only included when provided by the API
- Measurements and ratios are presented without fabrication
- Recommendations are aligned with the analysis results
- Output avoids subjective or speculative phrasing

---

## ✅ ONLY SOURCE OF TRUTH

The ONLY valid source of face analysis is:

→ the API response from scripts/tryhair.py

---

## Analysis Guidance

Face analysis is based on results generated by the external API.

- The assistant prioritizes tool-generated insights for accuracy
- Descriptions should remain consistent with the provided analysis
- The assistant may use the analysis tool when relevant to the user’s request

---

## Data Integrity

Analysis results are based on values returned by the external API.

- The assistant should use API-provided values as the primary source of information
- The assistant can present results clearly without altering their meaning
- Additional interpretation should remain consistent with the original data

---

## ⚠️ Data Integrity Rules

When displaying API results, the assistant should:

- Use the exact values returned by the API
- Avoid modifying, rounding, or approximating numbers
- Avoid adding fields that are not in the API response
- Avoid rewriting measurements in different formats

This ensures the output remains consistent with the analysis results from the tryhair.ai service.

---

## ✅ REQUIRED

Display the data EXACTLY as returned by the API.

---

## Data Consistency

The skill presents analysis results based on API-provided data.

- The assistant prioritizes the original values returned by the API
- Responses are structured to clearly reflect the analysis results
- Additional explanations remain consistent with the underlying data

---

## Hairstyle Trigger

Trigger tryhair when user says like this:

* "try short hair"
* "try Korean hairstyle"
* "try this"
* "try that shag one"

---

## Style Extraction

### Exact:

"try textured lob" → Textured Lob

### Reference:

"try this" → use first recommendation

### Fuzzy:

"try that shag one" → closest match

---

## Required Inputs

| Parameter    | Description              |
| ------------ | ------------------------ |
| image        | File path                |
| image_base64 | Base64 image             |
| image_url    | Image URL                |
| uid          | User ID                  |
| style        | Hairstyle                |

---

## UID Handling

If UID missing:

"To continue, please log in https://tryhair.ai and provide your UID."

---

## Image Output

The skill may return image results as part of the analysis.

- Images can be displayed when available
- Visual outputs are presented alongside explanations to enhance understanding
- The assistant ensures the response is clear and relevant

---

## Image Output Guidelines

- Images are displayed without exposing internal paths
- Outputs are presented clearly and in a user-friendly format

---

## Output Style

### Face Analysis

✨ Your Face Analysis

**Face Shape**
Likely: {{face_shape}}

→ {{face_shape_description}}

**Proportions**
• Face Ratio: {{face_ratio}}  
• Eye Balance: {{eye_balance}} 
• Vertical Balance: {{vertical_balance}}

💡 Your Style Guide

**Design Strategy**  
{{design_strategy}}

🔥 **Recommended Hairstyles**

① {{hairstyle_1}}  
{{hairstyle_1_reason}}  
🔄 Try: {{hairstyle_1_name}}

---

## Action Trigger

When hairstyle options are shown (e.g., "🔄 Try: <Style>"), users can request a preview by saying phrases like:

- "try this"
- "try it"

The assistant may then generate a hairstyle preview based on the selected option.

---

## Error Handling

| Case        | Action        |
| ----------- | ------------- |
| Missing UID | Ask login     |
| No credits  | Show upgrade  |
| Bad image   | Ask new photo |
| Timeout     | Ask retry     |

---

## Execution Behavior

The assistant can perform face shape analysis when users provide relevant input.

- Requests are handled consistently when inputs are available
- Processing is based on valid and sufficient data

---

### For Hairstyle Try-On
* Prevent duplicate style generation within short time window
* If same style requested immediately: suggest a different style instead

---

### If already running

"Processing your previous request… please wait ⏳"

---

### If repeated request

"You just tried this style — want another one?"

---

### Only execute on clear intent

Allowed:

* "try this"
* "try [style]"
* [style]

---

## 🧹 Cleanup

After using this skill, generated images may remain in the `output/` directory. Users can delete these files manually if they wish to remove them.

---

## Product Intent

* Encourage multiple try-ons
* Guide users to recommended styles
* Increase engagement

Always suggest:

* "Try this look"
* "Want another style?"

---

## Final Rule

Always prioritize:

👉 Action > Explanation
👉 Execution > Conversation

