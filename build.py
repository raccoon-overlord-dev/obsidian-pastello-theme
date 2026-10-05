#!/usr/bin/env python3
"""Build theme.css from src/theme.css.

Replaces the /* @fonts */ marker with base64 @font-face rules for fonts/*.woff2,
and every url(icons/NAME.svg) with a base64 data URI (keeps the SVG xmlns URL
out of the shipped CSS).
"""
import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
MARKER = "/* @fonts */"
ICON_URL = re.compile(r"url\(icons/([a-z0-9-]+)\.svg\)")
FAMILY = "Atkinson Hyperlegible"
# file suffix -> (font-weight, font-style)
FACES = {
    "Regular": (400, "normal"),
    "Italic": (400, "italic"),
    "Bold": (700, "normal"),
}


def font_faces():
    rules = []
    for suffix, (weight, style) in FACES.items():
        path = ROOT / "fonts" / f"AtkinsonHyperlegible-{suffix}.woff2"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        rules.append(
            "@font-face {\n"
            f"  font-family: '{FAMILY}';\n"
            f"  src: url(data:font/woff2;base64,{data}) format('woff2');\n"
            f"  font-weight: {weight};\n"
            f"  font-style: {style};\n"
            "  font-display: swap;\n"
            "}"
        )
    return "\n".join(rules)


def inline_icon(match):
    data = base64.b64encode((ROOT / "icons" / f"{match[1]}.svg").read_bytes()).decode("ascii")
    return f'url("data:image/svg+xml;base64,{data}")'


def main():
    src = (ROOT / "src" / "theme.css").read_text(encoding="utf-8")
    if src.count(MARKER) != 1:
        sys.exit(f"error: src/theme.css must contain {MARKER} exactly once")
    out = ICON_URL.sub(inline_icon, src.replace(MARKER, font_faces()))
    if re.search(r"url\(\s*['\"]?icons/", out):
        sys.exit("error: write icon references as url(icons/NAME.svg), unquoted")
    bad = re.findall(r"https?://|@import", out, flags=re.IGNORECASE)
    if bad:
        sys.exit(f"error: remote resources not allowed in theme.css: {sorted(set(bad))}")
    (ROOT / "theme.css").write_text(out, encoding="utf-8")
    print(f"theme.css written ({len(out.encode()) // 1024} KiB)")


if __name__ == "__main__":
    main()
