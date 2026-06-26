## Description: <br>
微信表情包制作工具。自动将六宫格、九宫格、十二宫格的原图裁剪并转换为符合微信表情包规范的格式（表情主图 240x240，聊天页图标 50x50）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanyang](https://clawhub.ai/user/guanyang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn prepared grid images into WeChat sticker pack assets, including resized PNG stickers, chat icons, and editable metadata templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runner creates a local Python virtual environment and installs third-party packages. <br>
Mitigation: Review and pin dependency versions before use in sensitive environments. <br>
Risk: Generated files in the selected output directory can be overwritten. <br>
Mitigation: Use a dedicated output directory and review existing contents before running the skill. <br>
Risk: Optional background removal depends on rembg model and package behavior. <br>
Mitigation: Keep background removal disabled unless that dependency behavior is acceptable for the input images and environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guanyang/wechat-sticker-maker) <br>
- [WeChat Sticker Open Platform](https://sticker.weixin.qq.com/) <br>
- [WeChat sticker making specifications](https://sticker.weixin.qq.com/cgi-bin/mmemoticon-bin/readtemplate?t=guide/index.html#/makingSpecifications#specifications_stickers) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Guidance] <br>
**Output Format:** [PNG image files and UTF-8 text templates, with command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates main sticker images at 240x240, icon images at 50x50, candidate cover and chat icon PNGs, plus meta.txt and info.txt templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
