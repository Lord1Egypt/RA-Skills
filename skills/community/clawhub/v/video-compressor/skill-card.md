## Description: <br>
Guide users to VideoAny Video Compressor tool to reduce video file size with quality/scale/format controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GaoQ1](https://clawhub.ai/user/GaoQ1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to guide video compression decisions and route authorized videos through VideoAny with quality, scale, and output format choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may upload confidential or sensitive videos to a third-party web service. <br>
Mitigation: Review VideoAny privacy and retention practices, and avoid uploading confidential videos unless authorized and approved. <br>
Risk: Legacy script names may mislead agents into expecting image, SVG, or dubbing behavior. <br>
Mitigation: Use scripts/guide_video_compressor.py as the primary entrypoint and treat legacy names as compatibility wrappers. <br>
Risk: Compression can reduce visual quality or affect playback compatibility. <br>
Mitigation: Test on a short clip and tune quality, scale, and format before a full export. <br>


## Reference(s): <br>
- [VideoAny Video Compressor](https://videoany.io/tools/video-compressor) <br>
- [ClawHub Video Compressor release page](https://clawhub.ai/GaoQ1/video-compressor) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Plain text guidance with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No local video processing; compression is performed on VideoAny web.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
