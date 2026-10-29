# STATUS

## What was built

A beginner manual on AI for home care aides, covering daily notes, care plans,
and family updates using free AI models. Education only — never medical advice;
never paste client details. Plain English, step by step, with printable sheets.
Credits Asdale Dynamics, LLC throughout.

## Contents

- `LICENSE` — MIT License, copyright line exactly:
  `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` — purpose, audience, golden rules, credits Asdale Dynamics, LLC
- `docs/` — full manual in Markdown:
  - `index.md` — manual home with chapter and printable-sheet index
  - `00-safety-first.md` — golden rules, what client details means, de-identifying
  - `01-getting-started.md` — pick a free tool, account safety, first prompt
  - `02-daily-notes.md` — step-by-step daily visit notes with example
  - `03-care-plans.md` — summaries and checklists, never clinical decisions
  - `04-family-updates.md` — warm short messages for families with example
  - `05-free-models.md` — free web chatbots, local AI (Ollama, LM Studio, Jan), free tiers
  - `printable-sheets/` — four one-page worksheets (daily note, care plan, family update, quick-start cheat sheet)
- `site/` — static HTML website mirroring the manual (open `site/index.html` in any browser, no build step):
  - `index.html`, `safety.html`, `getting-started.html`, `daily-notes.html`, `care-plans.html`, `family-updates.html`, `free-models.html`
  - `printable-sheets/` — four rendered, printable HTML worksheets linked from the site index
  - `assets/style.css` — screen styles; `assets/print.css` — print styles
- `tests/verify.py` — verification script

## How to run it

- Read the manual: open `docs/index.md` in any Markdown reader, or open
  `site/index.html` in any web browser. No server, no install, no build step.
- Print sheets: open any sheet under `site/printable-sheets/` and use File >
  Print. Print styles are in `site/assets/print.css`.
- Run verification: `python3 tests/verify.py` (Python 3, standard library only)

## Verification results

`python3 tests/verify.py` — ALL CHECKS PASSED (28 files scanned for secrets).

Verified:
- All expected files exist (docs chapters, printable sheets, site pages, CSS, tests)
- `LICENSE` contains the exact line `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` credits Asdale Dynamics, LLC and references the copyright line
- No `.github/workflows` directory present
- No secret or personal-data patterns (API keys, SSN-like strings, private keys) in any file
- All HTML files parse and all internal links resolve to existing files
- Every page links to `print.css` for clean printing
- `docs/index.md` references all six chapters

No secrets, API keys, or personal data were added. Nothing was pushed, no remote
repository was created, nothing was published.

## Known gaps

- Examples use made-up placeholders ([Client], [Date], etc.); real usage requires the aide to substitute their own de-identified facts and follow agency policy.
- Local AI tools (Ollama, LM Studio, Jan) are named as options but not installed or tested in this repo — installation is a manual step for the user.
- The Markdown sheets under `docs/printable-sheets/` are the canonical text source; the rendered HTML versions live under `site/printable-sheets/` and must be kept in sync if the text changes.
- No automated spell-check or accessibility testing included.
