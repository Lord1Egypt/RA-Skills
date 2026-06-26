# SJTU slurm skill

This is the skill to interact with SJTU HPC platform on behalf of a user.

## Skill ability

- Manage your HPC account information like jAccount/Email binding, password update, prefer contact method setting, etc.
- Query job status, partition queue, platform information, storage usage, etc.
- Submit/manage job according to your instructions.
- Help you to migrate data between hot/cold storages.

In a sense, it can help to do all the things you can through SSH login to platform's entry node.

## Notes on using this skill

This skill will request API token and SSH key/certificate for you, and store them in workspace. **Make sure your claw is in safe environment. Never use this skill on a shared machine.**

To fullfill your instructions, claw agent may need to call lots of command, channel clients (like Feishu, weixin, QQ, etc.) cannot display the background command call process in real time. You may have to wait for a while to see the final reply, be patient if your LLM models service is not fast enough.

## Install skill

This skill has been published on [clawhub](https://clawhub.ai/taleintervenor/sjtu-slurm-skill) , so you can simplily ask your claw to install sjtu-slurm-skill skill itself.

Or if you prefer to maintain skills manually:

```
openclaw skills install sjtu-slurm-skill
openclaw skills update sjtu-slurm-skill
```

## Repository

This project is hosted on GitHub at https://github.com/SJTU-HPC/SJTU-SLURM-Skill. If you have any suggestions for improvement, feel free to open an issue or submit a pull request.