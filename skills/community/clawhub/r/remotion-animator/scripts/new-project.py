#!/usr/bin/env python3
"""
new-project.py — Scaffold a new Remotion animation project.

Usage:
    python new-project.py my-video
    python new-project.py my-video --template intro
    python new-project.py my-video --template data-kinetic --width 1080 --height 1920

Templates: starter, intro, conversation, data-kinetic, explainer
"""

import argparse
import shutil
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOILERPLATE = os.path.join(SKILL_DIR, "assets", "boilerplate")
TEMPLATES = os.path.join(SKILL_DIR, "assets", "templates")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new Remotion project")
    parser.add_argument("name", help="Project folder name")
    parser.add_argument("--template", default="starter", choices=["starter", "intro", "conversation", "data-kinetic", "explainer"])
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    dest = os.path.join(os.getcwd(), args.name)
    if os.path.exists(dest):
        print(f"ERROR: {dest} already exists", file=sys.stderr)
        sys.exit(1)

    shutil.copytree(BOILERPLATE, dest, ignore=shutil.ignore_patterns("node_modules"))
    print(f"Created boilerplate at {dest}")

    if args.template != "starter":
        template_dir = os.path.join(TEMPLATES, args.template)
        if not os.path.exists(template_dir):
            print(f"ERROR: template '{args.template}' not found", file=sys.stderr)
            sys.exit(1)

        for item in os.listdir(template_dir):
            src = os.path.join(template_dir, item)
            dst = os.path.join(dest, "src", item)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
                print(f"  Overlay: {item}")

        mapping = {
            "intro": ("IntroVideo", "INTRO_DURATION"),
            "conversation": ("ConversationVideo", "CONVERSATION_DURATION"),
            "data-kinetic": ("DataKineticVideo", "DATA_DURATION"),
            "explainer": ("ExplainerVideo", "EXPLAINER_DURATION"),
        }
        comp, dur = mapping[args.template]
        import_map = {
            "intro": "./Intro",
            "conversation": "./Conversation",
            "data-kinetic": "./DataKinetic",
            "explainer": "./Explainer",
        }
        root_tsx = '''import "./index.css";
import { Composition } from "remotion";
import { %s, %s } from "%s";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={%s}
      durationInFrames={%s}
      fps={%d}
      width={%d}
      height={%d}
    />
  );
};
''' % (comp, dur, import_map[args.template], comp, dur, args.fps, args.width, args.height)
        with open(os.path.join(dest, "src", "Root.tsx"), "w") as f:
            f.write(root_tsx)

    elif args.template == "starter":
        root_path = os.path.join(dest, "src", "Root.tsx")
        with open(root_path) as f:
            content = f.read()
        content = content.replace('width={1920}', f'width={args.width}')
        content = content.replace('height={1080}', f'height={args.height}')
        with open(root_path, "w") as f:
            f.write(content)

    print(f"\nDone! cd {args.name} && npm install && npm run dev")


if __name__ == "__main__":
    main()
