#!/usr/bin/env python3
"""Codex TTS notification handler.

Speaks the assistant's response aloud when a turn completes.
Place this script anywhere and point your Codex config.toml at it:

    notify = ["python3", "/path/to/codex-notify-tts.py"]
"""

import json
import os
import subprocess
import sys


def main() -> int:
    notification = json.loads(sys.argv[1])

    if notification.get("type") != "agent-turn-complete":
        return 0

    text = notification.get("last-assistant-message", "")
    if not text.strip():
        return 0

    script = os.path.expanduser("~/.claude/tts-speak.sh")
    subprocess.Popen(
        ["bash", script],
        stdin=subprocess.PIPE,
    ).communicate(input=text.encode())

    return 0


if __name__ == "__main__":
    sys.exit(main())
