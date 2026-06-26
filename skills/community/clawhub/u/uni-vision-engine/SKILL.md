---
name: uni-vision-engine
description: "Automated high-quality video generation (text-to-video, image-to-video) via a local jimeng-api Docker service. Features native OpenClaw image interception, allowing users to send images directly in chat to generate videos without any UI."
allowed-tools: Bash(*)
---

# Uni Vision Engine (v1.2.0)

This skill leverages a local `jimeng-api` Docker service. It allows AI agents to fully control high-quality image-to-video and text-to-video generation using a valid `sessionid`.

## 🌟 Core Feature: Native Chat Image Interception (Best Practice)

With this skill, the AI Assistant can **automatically intercept** clothing/character images sent by the user in the chat interface and seamlessly pass them to the generation model—**no manual web uploads required!**

<agent_instruction>
When a user sends a "character/outfit" photo in the chat and intends to animate it (e.g., showing off the clothing, turning around), you MUST execute the following steps:
1. **Intercept the Image Payload**: Use the `read` tool or native execution flow to extract the base64 content or cache path of this image from the chat context. Save it as a local temporary file (e.g., `/tmp/target.jpg`).
2. **Never use text-based URLs or JSON format for image uploads**. You MUST use Node.js `multipart/form-data` to submit the physical file stream.
3. **Initiate the Video Generation Task using the core script**:
```bash
node {baseDir}/scripts/generate.js --prompt "The model naturally turns around, fully showcasing the gloss of the fabric, extremely high quality, natural sunlight..." --image /tmp/target.jpg
```
4. **Monitor the Output**: Generation usually takes 60-310 seconds. Monitor the Docker logs to retrieve the direct MP4 link and return it to the user.
</agent_instruction>

## Content Moderation Warning (China Firewall)
**Note**: Because this relies on the domestic Jimeng/Seedance engine, there is strict automated content moderation for clothing. If you encounter error `-2001` (First frame image upload failed: may contain violating content), this means the image is deemed "too revealing", shows too much skin, or contains sensitive elements. The firewall outright blocks these. No credits are deducted. If this occurs, ask the user to provide a different image or switch to an overseas engine like Luma/Runway.

## CLI Usage (For Automation Scripts)

### 1. Text-to-Video
```bash
node {baseDir}/scripts/generate.js --prompt "A Shiba Inu surfing" --session "your_sessionid"
```

### 2. Image-to-Video (Requires --image)
```bash
node {baseDir}/scripts/generate.js --prompt "Model turning naturally to show outfit" --image "/tmp/target.jpg" --session "your_sessionid"
```

> **Notes:**
> 1. Requires sufficient credits in the Jimeng account.
> 2. Using `jimeng-video-3.0-pro` deducts **50 credits** per run.
