## Description: <br>
Voice Listener starts a Baidu Speech Recognition listener that uses wake and stop words to transcribe speech into the currently focused application. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanqing203](https://clawhub.ai/user/fanqing203) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to run hands-free dictation through Baidu Speech Recognition and paste recognized speech into chat, document, or editor fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Microphone audio is sent to Baidu while the listener is running, including audio used to detect activation. <br>
Mitigation: Run the listener only when dictation is intended, stop it with Ctrl+C when finished, and confirm that users accept Baidu audio processing. <br>
Risk: Recognized speech can be pasted into whichever application currently has focus. <br>
Mitigation: Focus only the intended input field before speaking and avoid terminals, administrator consoles, password fields, and other sensitive contexts. <br>
Risk: Baidu API credentials are stored in a local configuration file. <br>
Mitigation: Protect the Baidu configuration file, avoid committing real keys, and rotate credentials if the file is exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fanqing203/voice-listener) <br>
- [Publisher Profile](https://clawhub.ai/user/fanqing203) <br>
- [Baidu AI Open Platform](https://ai.baidu.com/) <br>
- [Baidu Speech Recognition Documentation](https://ai.baidu.com/ai-doc/SPEECH/Vk38lxily) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Recognized text pasted into the focused application, with console status messages and JSON-based Baidu API configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires microphone access and Baidu API credentials; recognized speech can also be copied to the clipboard if automatic input fails.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
