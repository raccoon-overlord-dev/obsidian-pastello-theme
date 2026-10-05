#!/usr/bin/env python3
"""Build theme.css from src/theme.css.

Replaces the /* @fonts */ marker with base64 @font-face rules for the
Atkinson Hyperlegible faces in fonts/ and the Lucide icon subset in icons/.
"""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
MARKER = "/* @fonts */"
# (family, file, font-weight, font-style)
FACES = [
    ("Atkinson Hyperlegible", "fonts/AtkinsonHyperlegible-Regular.woff2", 400, "normal"),
    ("Atkinson Hyperlegible", "fonts/AtkinsonHyperlegible-Italic.woff2", 400, "italic"),
    ("Atkinson Hyperlegible", "fonts/AtkinsonHyperlegible-Bold.woff2", 700, "normal"),
    ("Pastello Icons", "icons/lucide-icons.woff2", 400, "normal"),
]


def font_faces():
    rules = []
    for family, file, weight, style in FACES:
        data = base64.b64encode((ROOT / file).read_bytes()).decode("ascii")
        rules.append(
            "@font-face {\n"
            f"  font-family: '{family}';\n"
            f"  src: url('data:font/woff2;base64,{data}') format('woff2');\n"
            f"  font-weight: {weight};\n"
            f"  font-style: {style};\n"
            "  font-display: swap;\n"
            "}"
        )
    return "\n".join(rules)


def main():
    src = (ROOT / "src" / "theme.css").read_text(encoding="utf-8")
    if src.count(MARKER) != 1:
        sys.exit(f"error: src/theme.css must contain {MARKER} exactly once")
    out = src.replace(MARKER, font_faces())
    bad = re.findall(r"https?://|@import", out, flags=re.IGNORECASE)
    if bad:
        sys.exit(f"error: remote resources not allowed in theme.css: {sorted(set(bad))}")
    (ROOT / "theme.css").write_text(out, encoding="utf-8")
    print(f"theme.css written ({len(out.encode())} bytes)")


if __name__ == "__main__":
    main()
