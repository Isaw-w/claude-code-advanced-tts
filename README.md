# Advanced TTS for AI Coding Assistants

Make AI coding assistants (Claude Code, Codex, etc.) speak responses aloud using macOS natural Siri voices.

https://github.com/user-attachments/assets/demo.mp4

## How it works

A shell script that takes text input, strips markdown formatting, and speaks it using macOS system TTS via AppleScript `say`.

The key insight: AppleScript `say` (without a `using` parameter) uses your **system Spoken Content voice**, which includes Apple's natural Siri voices — much more natural than the `say` CLI command or `AVSpeechSynthesizer`.

## Features

- Natural-sounding speech using Siri voices
- Automatic language detection (voice matches text language)
- Works with Claude Code, Codex, or any tool that can pipe text
- Strips markdown (code blocks, bold, headers, links) before speaking
- Kills previous speech when new response arrives (no overlap)
- Truncates long responses (2000 char limit)

## Requirements

- macOS (uses `osascript` and `say`)
- Siri voices downloaded (optional but recommended for natural TTS)

## Setup

### 1. Download Siri voices (recommended)

Go to **System Settings → Accessibility → Spoken Content → System Voice → Manage Voices** and download Siri voices for your languages. For example:

- English: Siri Voice 1 (Aaron) or Siri Voice 2
- Mandarin: Siri Voice 1 or Siri Voice 2 (Linfei)

Set your preferred voice as the system voice for each language.

### 2. Install the script

```bash
git clone https://github.com/Isaw-w/claude-code-advanced-tts.git
cp claude-code-advanced-tts/tts-speak.sh ~/.claude/tts-speak.sh
chmod +x ~/.claude/tts-speak.sh
```

### 3. Configure your AI tool

<details>
<summary><strong>Claude Code</strong></summary>

Edit `~/.claude/settings.json` and add the `Stop` hook:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.last_assistant_message // empty' | ~/.claude/tts-speak.sh &",
            "async": true
          }
        ]
      }
    ]
  }
}
```

If you already have other hooks, merge the `Stop` entry into your existing `hooks` object.

</details>

<details>
<summary><strong>Codex (OpenAI)</strong></summary>

Codex supports a `notify` hook that fires on `agent-turn-complete` with the assistant's response.

**1. Copy the notify script:**

```bash
cp claude-code-advanced-tts/codex-notify-tts.py ~/.claude/codex-notify-tts.py
```

**2. Add to your Codex `config.toml`:**

```toml
notify = ["python3", "~/.claude/codex-notify-tts.py"]
```

Or under a profile:

```toml
[profiles.tts]
notify = ["python3", "~/.claude/codex-notify-tts.py"]
```

Then run with `codex --profile tts`.

The notify script receives a JSON argument with `last-assistant-message` on each turn completion, extracts the text, and pipes it to `tts-speak.sh`.

</details>

<details>
<summary><strong>Any other tool</strong></summary>

The script reads from stdin or accepts text as an argument:

```bash
# Pipe text
echo "Hello world" | ~/.claude/tts-speak.sh

# Pass as argument
~/.claude/tts-speak.sh "Hello world"

# Pipe from any command
some-ai-tool --query "explain this code" | ~/.claude/tts-speak.sh
```

</details>

### 4. Stop speech anytime

```bash
killall say
```

## How voice selection works

macOS Spoken Content lets you configure a preferred voice per language. When AppleScript `say` runs without a `using` parameter, it uses the system voice matching the detected text language.

For example, if you set:
- System voice for English → Siri Aaron
- System voice for Mandarin → Siri Linfei

Then English responses use Aaron and Chinese responses use Linfei, automatically.

## Customization

### Change the character limit

Edit `tts-speak.sh` and change the `2000` in:
```bash
text=$(echo "$text" | cut -c1-2000)
```

### Use a specific voice

Add `using "VoiceName"` to the osascript command in the script:
```bash
osascript -e "say \"$text\" using \"Samantha\"" &
```

### Adjust speech rate

Add `speaking rate N` (words per minute, default ~175):
```bash
osascript -e "say \"$text\" speaking rate 200" &
```

## License

MIT
