#!/usr/bin/env python3
"""
build.py — Stefan Mladenovski Portfolio Builder
Run this once after placing your source HTML files in the same directory.

Usage:
  1. Place all your original HTML files in this directory
  2. Rename them to match the SOURCE_FILES mapping below
  3. Run: python3 build.py
  4. Output files (with nav bar injected) go into ./output/
  5. Copy everything in ./output/ to your GitHub Pages repo

Source file names (what you name your originals):
  billtrust.html          → billtrust-sre.html
  nextsense.html          → nextsense-k8s-platform.html
  telekom.html            → telekom-mk.html
  bookshop_local.html     → local-k8s-observability.html
  reflective.html         → reflective-app.html
  bookshop_eks.html       → eks-bookshop.html
  wordpress.html          → wordpress-aws.html
"""

import os
import shutil

SOURCE_FILES = {
    'billtrust.html':       'billtrust-sre.html',
    'nextsense.html':       'nextsense-k8s-platform.html',
    'telekom.html':         'telekom-mk.html',
    'bookshop_local.html':  'local-k8s-observability.html',
    'reflective.html':      'reflective-app.html',
    'bookshop_eks.html':    'eks-bookshop.html',
    'wordpress.html':       'wordpress-aws.html',
}

NAV_CSS = """
  .portfolio-nav {
    position: sticky; top: 0; z-index: 100;
    background: rgba(247,245,240,0.92);
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    border-bottom: 1px solid var(--border);
    padding: 0.6rem 2rem;
    display: flex; align-items: center; justify-content: space-between; gap: 1rem;
  }
  .portfolio-nav a {
    font-family: var(--mono); font-size: 11px; color: var(--accent);
    text-decoration: none; letter-spacing: 0.06em;
  }
  .portfolio-nav a:hover { text-decoration: underline; }
  .portfolio-nav-label {
    font-family: var(--mono); font-size: 10px; color: var(--text-faint);
    letter-spacing: 0.08em; text-transform: uppercase;
  }"""

NAV_HTML = '<nav class="portfolio-nav"><a href="index.html">\u2190 Portfolio</a><span class="portfolio-nav-label">Stefan Mladenovski</span></nav>'

FOOTER_LINK = '\n      <a class="footer-link" href="index.html">\u2190 Portfolio</a>'


def inject_nav(html):
    # Inject CSS before the last </style> tag
    idx = html.rfind('</style>')
    if idx != -1:
        html = html[:idx] + NAV_CSS + '\n' + html[idx:]
    # Inject nav HTML right after <body>
    html = html.replace('<body>', '<body>\n' + NAV_HTML, 1)
    # Add ← Portfolio to footer links if present
    if 'footer-links' in html and 'index.html' not in html.split('footer-links')[1][:500]:
        html = html.replace('<div class="footer-links">', '<div class="footer-links">' + FOOTER_LINK, 1)
    return html


def main():
    out_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(out_dir, exist_ok=True)

    # Copy index.html if it exists
    index_src = os.path.join(os.path.dirname(__file__), 'index.html')
    if os.path.exists(index_src):
        shutil.copy(index_src, os.path.join(out_dir, 'index.html'))
        print('OK  index.html')
    else:
        print('MISSING  index.html  — place the index.html file here')

    # Process each project page
    ok = 0
    missing = []
    for src_name, out_name in SOURCE_FILES.items():
        src_path = os.path.join(os.path.dirname(__file__), src_name)
        out_path = os.path.join(out_dir, out_name)

        if os.path.exists(src_path):
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
            injected = inject_nav(content)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(injected)
            print(f'OK  {src_name}  →  {out_name}')
            ok += 1
        else:
            print(f'MISSING  {src_name}  (will be  {out_name})')
            missing.append(src_name)

    print(f'\n{ok}/{len(SOURCE_FILES)} pages built.')
    if missing:
        print(f'\nMissing source files: {missing}')
        print('Rename your original HTML files to match the names above and re-run.')
    else:
        print('\nAll done! Upload everything in ./output/ to your GitHub Pages repo.')
        print('Your portfolio will be live at: https://stefanmladenovskii.github.io')


if __name__ == '__main__':
    main()
