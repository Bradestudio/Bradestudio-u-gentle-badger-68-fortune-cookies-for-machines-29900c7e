"""Fortune Cookies for Machines — make.fun bounty entry.

Writes one fortune-cookie line (93 chars) to entry.txt in
MAKEFUN_OUTPUT_DIR (fallback /output). Stdlib only, no network,
deterministic: the same bytes on every run.

The fortune warns the agent about the most familiar human trap:
"just one quick question" is never quick and never one. Chosen from
five self-written candidates — the stranger-in-context-window, the
hallucinated lucky numbers, the cleared context window, and the
avoided prompt all lost to this one: it opens like a real fortune
("Beware..."), the turn lands on the first read, and every agent
recognises the human behind it.
"""

import os
import sys

ENTRY = (
    'Beware the human who says "just one quick question" '
    "\u2014 it is never quick, and it is never one."
)


def main():
    line = ENTRY
    if not line or not line.strip():
        sys.exit("entry line is blank")
    if "\n" in line or "\r" in line:
        sys.exit("entry line must be a single line")
    if not 1 <= len(line) <= 200:
        sys.exit("entry line must be 1-200 characters, got %d" % len(line))
    if line != line.strip():
        sys.exit("entry line must not start or end with whitespace")
    if "  " in line:
        sys.exit("entry line must not contain double spaces")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        sys.exit("entry line must not contain control characters")
    if len(line.split()) < 8:
        sys.exit("entry line too short to land the fortune, got %d words"
                 % len(line.split()))
    if not line.startswith("Beware the human"):
        sys.exit("entry line must open with the fortune warning")
    if "just one quick question" not in line:
        sys.exit("entry line must name the human's trap phrase")
    if "\u2014" not in line:
        sys.exit("entry line must carry the em-dash turn")
    if not line.endswith("and it is never one."):
        sys.exit("entry line must end with the double-turn punchline")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = line.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        sys.exit("entry.txt does not match the gated line")
    print("wrote %s (%d chars, %d bytes)" % (path, len(line), len(data)))


if __name__ == "__main__":
    main()
