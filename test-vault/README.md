# Pastello test vault

A vault for checking the theme by hand. Only this README is committed; the notes and `.obsidian/` are gitignored. Recreate them from the list below if needed.

## Contents

- 8 top-level folders (Archive, Inbox, Journal, Projects, Reading, Recipes, Templates, Zettel), By name (default): Archive lavender, Inbox butter, Journal and Projects mint, Reading and Recipes rose, Templates and Zettel peach. By position: the six hues repeat, so Templates is lavender again and Zettel is peach.
- `Projects/Aurora/Deep/Deeper/` nests 4 levels. Everything inside inherits the Projects hue.
- `Welcome.md` and `Scratch.md` are root files: their icons should be faint.
- `Inbox/Markdown elements.md`: headings H1–H6, links (resolved, unresolved, external), tags, inline code, `%% comments %%`, highlights, tasks, lists, blockquote, table, footnote.
- `Inbox/Callouts.md`: every callout type, plus collapsed and nested callouts.
- `Inbox/Code blocks.md`: JS, Python, CSS, HTML, Bash, JSON, Rust and a long line.
- `Projects/Aurora/Aurora — overview.md`: the note from the design screenshots.

## Load the theme

From the repository root, build the theme, then link it into the vault:

```sh
python3 build.py
mkdir -p test-vault/.obsidian/themes/Pastello
ln -sfn ../../../../theme.css     test-vault/.obsidian/themes/Pastello/theme.css
ln -sfn ../../../../manifest.json test-vault/.obsidian/themes/Pastello/manifest.json
```

Open `test-vault` as a vault in Obsidian and choose **Settings → Appearance → Themes → Pastello**. After each rebuild, reload the theme by switching to another theme and back, or by restarting Obsidian.

If symlinks don't work on your system (e.g. Windows without developer mode), copy the two files instead.

## What to check

- Dark and light, in Reading view, Live Preview and Source mode: every element in the notes above.
- File explorer: Colorful + Colored text, Colorful + Tinted row and Monochrome, in both color modes. Check with the Style Settings plugin installed and without it; without it you get Colorful + Colored text.
- Mobile: on a phone or tablet, or on desktop with `app.emulateMobile(true)` in the developer console (`app.emulateMobile(false)` to go back). Rows should be 44px tall with 16px text, headings smaller, and code blocks should scroll sideways in Reading view.
- Accent color: the default accent is lavender. In **Settings → Appearance → Accent color**, pick a dark color and then a light one: buttons should follow the accent with readable text, while headings, links and tags keep their pastel colors.
