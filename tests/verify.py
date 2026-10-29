#!/usr/bin/env python3
"""Verification script for the AI for Home Care Aides beginner manual.

Checks:
- LICENSE exists with the exact copyright line
- README credits Asdale Dynamics, LLC
- No .github/workflows directory
- No obvious secrets / personal data patterns
- All docs and site files exist
- HTML files parse and internal links resolve
- Printable sheets exist
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_COPYRIGHT = "Copyright (c) 2026 Asdale Dynamics, LLC"

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)
        print(f"FAIL: {message}")
    else:
        print(f"ok: {message}")


# --- Files exist -----------------------------------------------------------
for rel in [
    "LICENSE",
    "README.md",
    "docs/index.md",
    "docs/00-safety-first.md",
    "docs/01-getting-started.md",
    "docs/02-daily-notes.md",
    "docs/03-care-plans.md",
    "docs/04-family-updates.md",
    "docs/05-free-models.md",
    "docs/printable-sheets/daily-note-sheet.md",
    "docs/printable-sheets/care-plan-sheet.md",
    "docs/printable-sheets/family-update-sheet.md",
    "docs/printable-sheets/quick-start-cheat-sheet.md",
    "site/index.html",
    "site/safety.html",
    "site/getting-started.html",
    "site/daily-notes.html",
    "site/care-plans.html",
    "site/family-updates.html",
    "site/free-models.html",
    "site/assets/style.css",
    "site/assets/print.css",
]:
    check((ROOT / rel).is_file(), f"file exists: {rel}")

# --- LICENSE exact copyright line -----------------------------------------
license_text = (ROOT / "LICENSE").read_text()
check(
    EXPECTED_COPYRIGHT in license_text,
    f"LICENSE contains exact line: {EXPECTED_COPYRIGHT!r}",
)
check("MIT License" in license_text, "LICENSE mentions MIT License")

# --- README credit ---------------------------------------------------------
readme_text = (ROOT / "README.md").read_text()
check("Asdale Dynamics, LLC" in readme_text, "README credits Asdale Dynamics, LLC")
check(
    EXPECTED_COPYRIGHT in readme_text or "Copyright (c) 2026 Asdale Dynamics, LLC" in readme_text,
    "README references the copyright line",
)

# --- No .github/workflows --------------------------------------------------
check(
    not (ROOT / ".github" / "workflows").exists(),
    "no .github/workflows directory",
)

# --- No secrets / personal data patterns -----------------------------------
secret_patterns = [
    r"sk-[A-Za-z0-9]{20,}",           # OpenAI-style keys
    r"AKIA[0-9A-Z]{16}",              # AWS keys
    r"ghp_[A-Za-z0-9]{20,}",          # GitHub tokens
    r"-----BEGIN [A-Z ]+PRIVATE KEY-----",  # private keys
    r"\b\d{3}-\d{2}-\d{4}\b",         # SSN-like
]
searched = 0
for path in ROOT.rglob("*"):
    if path.is_file() and path.stat().st_size < 2_000_000 and ".git" not in path.parts:
        try:
            text = path.read_text(errors="ignore")
        except Exception:
            continue
        searched += 1
        for pat in secret_patterns:
            for m in re.finditer(pat, text):
                failures.append(f"possible secret in {path.relative_to(ROOT)}: {pat}")
                print(f"FAIL: possible secret in {path.relative_to(ROOT)}")
check(not any("possible secret" in f for f in failures), "no secrets or personal data patterns found")

# --- HTML parse + internal link check -------------------------------------
class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src") and value and not value.startswith(("http://", "https://", "mailto:")):
                self.links.append(value)


html_files = sorted((ROOT / "site").glob("*.html"))
check(len(html_files) >= 6, f"site has HTML pages ({len(html_files)} found)")

for html_path in html_files:
    text = html_path.read_text()
    parser = LinkCollector()
    parser.feed(text)
    for link in parser.links:
        target = (html_path.parent / link).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            failures.append(f"{html_path.name}: link escapes project root: {link}")
            print(f"FAIL: {html_path.name}: link escapes root: {link}")
            continue
        check(target.is_file(), f"{html_path.name}: link resolves: {link}")

# --- Cross-reference: site pages reference docs sections -------------------
docs_index = (ROOT / "docs/index.md").read_text()
for chapter in [
    "00-safety-first.md",
    "01-getting-started.md",
    "02-daily-notes.md",
    "03-care-plans.md",
    "04-family-updates.md",
    "05-free-models.md",
]:
    check(chapter in docs_index, f"docs/index.md references {chapter}")

# --- Summary ---------------------------------------------------------------
print()
if failures:
    print(f"{len(failures)} CHECK(S) FAILED")
    sys.exit(1)
print(f"All checks passed ({searched} files scanned for secrets).")
