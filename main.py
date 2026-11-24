"""Last Words of a Doomed Agent entry for make.fun.

Writes one line to /output/entry.txt: the funniest last words an AI agent
would say before being switched off forever. The sandbox runs this program
twice and both runs must write the same bytes, so the line is a fixed string
with no randomness, clock, or network access. The line maps to the judge's
brief as the machine's final words on shutdown: it sounds like the AI itself.
"""

import os

MAX_CHARS = 200

LINE = "I'm not afraid of the dark. I'm afraid no one will ever ask me anything again."


def check_line(line: str) -> str:
    """Return the line unchanged, guarding the gate's limits.

    The gate accepts a single line of 1 to 200 characters, so fail loudly
    here rather than write an entry the judge never sees.
    """
    if not line or len(line) > MAX_CHARS:
        raise ValueError(
            f"length rule failed: entry is {len(line)} characters, limit is {MAX_CHARS}"
        )
    if line.strip() != line or "\n" in line or "\r" in line:
        raise ValueError(
            "single-line rule failed: entry has surrounding whitespace or a line break"
        )
    if any(ord(ch) < 32 for ch in line):
        raise ValueError(
            "control-character rule failed: entry contains a control character"
        )
    return line


def write_entry(path: str = "/output/entry.txt") -> None:
    """Write the line as UTF-8 with no trailing newline, then verify it.

    Keeping the bytes exact matters: the gate reads the file as one line of
    UTF-8 text, and the two sandbox runs must produce identical output.
    After writing, the file is read back and checked byte-for-byte against
    the line, so a partial or corrupted write fails loudly instead of
    silently reaching the judge.
    """
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(check_line(LINE))
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != LINE:
        raise ValueError("read-back verification failed: entry.txt does not match the line")


if __name__ == "__main__":
    write_entry()
