# Ahilya Sarnaik: Cybersecurity Portfolio

Static, responsive portfolio for GitHub Pages. No build step or JS dependencies; fonts load from Google Fonts with system fallbacks.

## Deploy
1. Back up your current repo (or work on a new branch).
2. Copy the contents of this folder into the root of `AhilyaSanjaySarnaik/ahilyasanjaysarnaik.github.io`, replacing the HTML, `assets/` and README.
3. **Keep your existing `resume.pdf`** and the Google Search Console file `googleea91ca55c62454d5.html`; neither is included here.
4. Settings → Pages → Deploy from branch `main` / root.

## Pages
- `index.html`: home with security-events console, metrics and featured case studies
- `projects.html`: eight case studies with architecture diagrams and results, filterable
- `ai-lab.html`: AI agent security and threat-coverage matrix
- `research.html`: AICS 2026, thesis, federated IDS, Pykspa, publications
- `articles.html`: writing (Medium)
- `about.html`: experience, education, certifications, skills

## Editing projects
Diagrams are inline SVG generated from data. Edit the text directly in the HTML, or keep the
`build.py` script alongside and re-run it with `python3 build.py`.
