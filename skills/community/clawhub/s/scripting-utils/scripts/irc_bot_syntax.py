#!/usr/bin/env python3
"""
IRC Bot command syntax for pbot (Perl), Limnoria (Python), and Eggdrop (Tcl).
Fetches syntax from documentation sources.
"""

import json
from dataclasses import dataclass
from typing import Optional

@dataclass
class BotCommand:
    bot: str
    command: str
    syntax: str
    example: str
    description: str
    permission: Optional[str] = None

class IRCBotSyntax:
    """
    IRC Bot command syntax reference.
    Sources:
    - pbot: https://github.com/pragma-/pbot
    - Limnoria: https://docs.limnoria.net/
    - Eggdrop: https://docs.eggheads.org/
    """
    
    PBOT_COMMANDS = {
        "keyword add": BotCommand(
            bot="pbot",
            command="keyword add",
            syntax="keyword add <keyword> <text>",
            example="keyword add hello Hello, World!",
            description="Add a keyword trigger",
            permission="admin"
        ),
        "fact add": BotCommand(
            bot="pbot",
            command="fact add",
            syntax="fact add <channel> <subject> <text>",
            example="fact add #channel python Python is a programming language",
            description="Add a factoid",
            permission=" whitelisted"
        ),
        "ban": BotCommand(
            bot="pbot",
            command="ban",
            syntax="ban <nick|mask> [duration] [reason]",
            example="ban spambot 1h Spamming",
            description="Ban a user",
            permission="op"
        ),
    }
    
    LIMNORIA_COMMANDS = {
        "config channel": BotCommand(
            bot="limnoria",
            command="config channel",
            syntax="config channel <#channel> <plugin>.<variable> <value>",
            example="config channel #bot supybot.plugins.Channel.enabled True",
            description="Configure channel-specific settings",
            permission="admin"
        ),
        "load": BotCommand(
            bot="limnoria",
            command="load",
            syntax="load <plugin>",
            example="load User",
            description="Load a plugin",
            permission="owner"
        ),
        "aka add": BotCommand(
            bot="limnoria",
            command="aka add",
            syntax="aka add <name> <command>",
            example="aka add hi say Hello $nick!",
            description="Create command alias",
            permission="admin"
        ),
    }
    
    EGGDROP_COMMANDS = {
        "bind": BotCommand(
            bot="eggdrop",
            command="bind",
            syntax="bind <type> <flags> <keyword> <proc>",
            example="bind pub - !hello pub_hello",
            description="Bind a command to a Tcl procedure",
            permission="n/a (script)"
        ),
        "putserv": BotCommand(
            bot="eggdrop",
            command="putserv",
            syntax="putserv <text>",
            example="putserv PRIVMSG #channel :Hello World",
            description="Send raw IRC command",
            permission="n/a (script)"
        ),
        "setudef": BotCommand(
            bot="eggdrop",
            command="setudef",
            syntax="setudef <type> <name>",
            example="setudef str bot_setting",
            description="Define user-defined variable",
            permission="n/a (script)"
        ),
    }
    
    ALL_COMMANDS = {
        "pbot": PBOT_COMMANDS,
        "limnoria": LIMNORIA_COMMANDS,
        "eggdrop": EGGDROP_COMMANDS,
    }
    
    def get_command(self, bot: str, command: str) -> Optional[BotCommand]:
        """Get command syntax for a specific bot."""
        bot = bot.lower()
        command = command.lower()
        
        bot_commands = self.ALL_COMMANDS.get(bot, {})
        return bot_commands.get(command)
    
    def list_commands(self, bot: Optional[str] = None) -> dict:
        """List available commands for a bot or all bots."""
        if bot:
            return {bot: list(self.ALL_COMMANDS.get(bot.lower(), {}).keys())}
        return {k: list(v.keys()) for k, v in self.ALL_COMMANDS.items()}
    
    def generate_script_template(self, bot: str, purpose: str) -> str:
        """Generate a script template for a bot."""
        templates = {
            "pbot": f"""# pbot applet - {purpose}
# Place in ~/.pbot/applets/

use strict;
use warnings;

sub {purpose.replace(' ', '_')} {{
    my ($self, $from, $to, $args) = @_;
    
    # Your code here
    return "Result: $args";
}}

1;
""",
            "limnoria": f"""# Limnoria plugin - {purpose}
# Place in plugins/{purpose.replace(' ', '')}/

from supybot import utils, plugins, ircutils, callbacks
from supybot.commands import *

class {purpose.replace(' ', '').title()}(callbacks.Plugin):
    \"\"\"{purpose}\"\"\"
    
    threaded = True
    
    def {purpose.replace(' ', '_')}(self, irc, msg, args):
        \"\"\"<args>\"\"\"
        irc.reply("Hello from {purpose}!")
    
Class = {purpose.replace(' ', '').title()}
""",
            "eggdrop": f"""# Eggdrop Tcl script - {purpose}
# Add to eggdrop.conf: source scripts/{purpose.replace(' ', '_')}.tcl

proc {purpose.replace(' ', '_')} {{nick uhost hand chan arg}} {{
    putserv "PRIVMSG $chan :Hello $nick, this is {purpose}!"
}}

bind pub - !{purpose.replace(' ', '_')} {purpose.replace(' ', '_')}
""",
        }
        return templates.get(bot.lower(), "# Unknown bot")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="IRC Bot command syntax reference")
    parser.add_argument("--bot", required=True, choices=["pbot", "limnoria", "eggdrop"])
    parser.add_argument("--command", help="Command to look up")
    parser.add_argument("--list", action="store_true", help="List all commands")
    parser.add_argument("--template", help="Generate script template for purpose")
    args = parser.parse_args()
    
    syntax = IRCBotSyntax()
    
    if args.list:
        commands = syntax.list_commands(args.bot)
        print(json.dumps(commands, indent=2))
    elif args.command:
        cmd = syntax.get_command(args.bot, args.command)
        if cmd:
            print(f"Bot: {cmd.bot}")
            print(f"Command: {cmd.command}")
            print(f"Syntax: {cmd.syntax}")
            print(f"Example: {cmd.example}")
            print(f"Description: {cmd.description}")
            if cmd.permission:
                print(f"Permission: {cmd.permission}")
        else:
            print(f"Command not found: {args.command}")
            print("Available commands:")
            cmds = syntax.list_commands(args.bot)
            print(json.dumps(cmds, indent=2))
    elif args.template:
        template = syntax.generate_script_template(args.bot, args.template)
        print(template)


if __name__ == "__main__":
    main()
