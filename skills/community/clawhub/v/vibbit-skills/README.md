# Vibbit Skills

[中文说明](README.zh-CN.md)

Create images and videos with Vibbit through conversation in your Agent. Start with a product link, an idea, a script, or reference content.

## What you can do

- **Ecommerce marketing:** Extract information from a product link, save it to your product library, and use product details and reference images to create ecommerce hero images, marketing visuals, and advertising videos.
- **Talking-head videos:** Combine a script or existing audio with a digital avatar to create a talking-head video.
- **Video creation:** Turn ideas, scripts, and references into plans, storyboards, generated content, and revisions.
- **Comics:** Adapt novels, stories, or scripts into comic pages with consistent characters, settings, and props, then continue chapters or revise individual pages.
- **Creative reuse:** Save scripts, talent, and scenes in private persistent storage, extract new script templates from videos, and reuse selected entries for new-product video variants.
- **Multilingual content:** Translate videos and create voiceovers and subtitles in your target language.
- **Audio and subtitles:** Transcribe recordings, export subtitle files, check voiceovers against scripts, and locate keyword passages.

## Install

```bash
npx skills add vibbit-ai/skills
```

Follow the installation prompts to select your Agent.

If the command cannot complete installation, use a skill marketplace supported by your Agent:

- [SkillHub](https://skillhub.cn/skills/vibbit-skills)
- [ClawHub](https://clawhub.ai/zgissing/skills/vibbit-skills)

Install in the environment where your Agent actually runs, using the installation method supported by that platform.

After installation, ask your Agent to guide you through connecting your Vibbit account. Once the connection is verified, you can start creating.

## Start creating

- “Here is a product link. Make an ad for US customers.”
- “Use the product details and reference images to create an ecommerce hero image.”
- “Adapt this reference video into an ad for my product, then make an English version.”
- “Turn this story into a comic, keeping the characters and settings consistent.”
- “Save this video as a reusable script template for future products.”
- “Use my saved scripts and talent to make three videos for this new product.”

## Update

To update an installation made with the command above, run:

```bash
npx --yes skills@latest update vibbit-skills -y
```

## Links

- [Vibbit](https://vibbit.ai/)
- [API documentation](https://vibbit.apifox.cn/)
