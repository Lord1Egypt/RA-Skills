# Vibbit Skills

![Vibbit](assets/vibbit-logo.png)

[中文说明](README.zh-CN.md)

Create images and videos with Vibbit through conversation in your Agent. Start with a product link, an idea, a script, or reference content.

## What you can do

- **Ecommerce marketing:** Extract information from a product link, save it to your product library, and use product details and reference images to create ecommerce hero images, marketing visuals, and advertising videos.
- **Talking-head videos:** Use a script or library audio to drive an avatar, reuse a suitable existing performance, or add library B-roll when requested. Avatar-only videos keep the speaker on screen.
- **Video creation:** Turn ideas, scripts, and references into plans, storyboards, generated content, and revisions.
- **Person replacement:** Use your model photos to replace facial features and hairstyles in reference videos while retaining the selected outfit, scene, and presentation.
- **Comics:** Adapt novels, stories, or scripts into comic pages with consistent characters, settings, and props, then continue chapters or revise individual pages.
- **Creative reuse:** Save scripts, talent, and scenes in private persistent storage, extract new script templates from videos, and reuse selected entries for new-product video variants.
- **Multilingual content:** Translate videos while preserving original voices, or use your selected voice for everyone or individual speakers, with subtitles and speech corrections as needed.
- **Audio and subtitles:** Transcribe recordings, export subtitle files, check voiceovers against scripts, and locate keyword passages.
- **Semantic mixcuts:** Analyze reference edits and save reusable rules. The Agent matches library footage and arranges original sound, avatars, and narration, with cloud editing by default.
- **Material reuse:** Find library images, audio and video by name, tags or content; retrieve original files and matching clips for scripts, editing, references and continued production.
- **Video storage:** Save local or linked videos in your Vibbit material library, choose a name and an existing group, and optionally enable analysis.
- **Video links:** Use platform videos for translation, transcription and reference-based creation; additional platforms can use the optional yt-dlp downloader when the Agent environment supports it.

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
