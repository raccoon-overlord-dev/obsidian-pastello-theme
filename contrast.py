#!/usr/bin/env python3
"""WCAG contrast check for Pastello tokens in src/theme.css.

Body text, text-muted and the six hues must reach 4.5:1 against bg-primary
in both modes. Exits non-zero if any pair fails.
"""
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
MIN_RATIO = 4.5
CHECKED = ["text-normal", "text-muted", "lavender", "peach", "butter", "mint", "sky", "rose"]


def oklch_to_srgb(l, c, h):
    a, b = c * math.cos(math.radians(h)), c * math.sin(math.radians(h))
    l_ = (l + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (l - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (l - 0.0894841775 * a - 1.2914855480 * b) ** 3
    linear = (
        4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )
    # gamma-encode, clipping out-of-gamut channels like a browser would
    return [
        12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
        for x in (min(1.0, max(0.0, v)) for v in linear)
    ]


def parse_color(value):
    """sRGB channels in 0..1 from '#rrggbb' or 'oklch(L C H)'."""
    value = value.strip()
    if m := re.fullmatch(r"#([0-9a-fA-F]{6})", value):
        return [int(m[1][i:i + 2], 16) / 255 for i in (0, 2, 4)]
    if m := re.fullmatch(r"oklch\(\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\)", value):
        return oklch_to_srgb(*map(float, m.groups()))
    raise ValueError(f"unsupported color: {value}")


def luminance(rgb):
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def ratio(fg, bg):
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def tokens(css, mode):
    block = re.search(r"\.theme-" + mode + r"\s*\{([^}]*)\}", css)
    if not block:
        sys.exit(f"error: no .theme-{mode} block in src/theme.css")
    return dict(re.findall(r"--pastello-([a-z-]+):\s*([^;]+);", block[1]))


def main():
    css = (ROOT / "src" / "theme.css").read_text(encoding="utf-8")
    failed = False
    for mode in ("dark", "light"):
        t = tokens(css, mode)
        bg = parse_color(t["bg-primary"])
        print(f"{mode} (bg-primary {t['bg-primary']})")
        for name in CHECKED:
            r = ratio(parse_color(t[name]), bg)
            ok = r >= MIN_RATIO
            failed |= not ok
            print(f"  {name:<12} {t[name]:<24} {r:5.2f}:1  {'ok' if ok else 'FAIL'}")
    if failed:
        sys.exit(f"contrast check failed: some pairs are below {MIN_RATIO}:1")
    print("all pairs pass")


if __name__ == "__main__":
    assert round(ratio([0, 0, 0], [1, 1, 1]), 2) == 21.0  # sanity: black on white
    main()
