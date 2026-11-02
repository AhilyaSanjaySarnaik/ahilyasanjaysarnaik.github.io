#!/usr/bin/env python3
"""Builds the static portfolio into /home/claude/site."""
import html, os

OUT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://ahilyasanjaysarnaik.github.io/"
EMAIL = "ahilyasarnaik12@gmail.com"
GH = "https://github.com/AhilyaSanjaySarnaik"
LI = "https://www.linkedin.com/in/ahilyacyber/"
MEDIUM = "https://medium.com/@ahilya_Cyber"
THM = "https://tryhackme.com/p/Clover.Code"
def repo(n): return f"{GH}/{n}"

e = html.escape

# ------------------------------------------------------------------ diagrams
def diagram(did, w, h, nodes, edges, title, groups=()):
    out = [f'<svg class="diagram" viewBox="0 0 {w} {h}" role="img" aria-labelledby="{did}-t" xmlns="http://www.w3.org/2000/svg">',
           f'<title id="{did}-t">{e(title)}</title><defs>']
    for k, col in (("n", "var(--faint)"), ("a", "var(--accent)"), ("d", "var(--deny)"), ("w", "var(--warn)")):
        out.append(f'<marker id="{did}-{k}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{col}"/></marker>')
    out.append('</defs>')
    for (x, y, gw, gh, lbl) in groups:
        out.append(f'<rect class="dg-group" x="{x}" y="{y}" width="{gw}" height="{gh}" rx="12"/>')
        if lbl: out.append(f'<text class="dg-glabel" x="{x+12}" y="{y+18}">{e(lbl)}</text>')
    mk = {"": "n", "accent": "a", "deny": "d", "warn": "w"}
    for ed in edges:
        kind = ed.get("kind", "")
        if "d" in ed:
            d = ed["d"]
        else:
            a, b = nodes[ed["from"]], nodes[ed["to"]]
            ax, ay, aw, ah = a[:4]; bx, by, bw, bh = b[:4]
            if bx >= ax + aw:
                x1, y1, x2, y2 = ax + aw, ay + ah / 2, bx, by + bh / 2
                m = ed.get("mid", (x1 + x2) / 2)
                d = f"M{x1} {y1}H{m}V{y2}H{x2-1}" if y1 != y2 else f"M{x1} {y1}H{x2-1}"
            elif bx + bw <= ax:
                x1, y1, x2, y2 = ax, ay + ah / 2, bx + bw, by + bh / 2
                m = (x1 + x2) / 2
                d = f"M{x1} {y1}H{m}V{y2}H{x2+1}"
            elif by > ay:
                x1, y1 = ed.get("x1", ax + aw / 2), ay + ah
                x2, y2 = ed.get("x2", bx + bw / 2), by
                m = (y1 + y2) / 2
                d = f"M{x1} {y1}V{m}H{x2}V{y2-1}" if x1 != x2 else f"M{x1} {y1}V{y2-1}"
            else:
                x1, y1 = ax + aw / 2, ay
                x2, y2 = bx + bw / 2, by + bh
                m = (y1 + y2) / 2
                d = f"M{x1} {y1}V{m}H{x2}V{y2+1}"
        cls = f"dg-edge {kind}".strip() + (" dg-flow" if ed.get("flow") else "")
        out.append(f'<path class="{cls}" d="{d}" marker-end="url(#{did}-{mk[kind]})"/>')
        if ed.get("label"):
            lx, ly = ed["lpos"]
            anchor = ed.get("anchor", "middle")
            out.append(f'<text class="dg-elabel" x="{lx}" y="{ly}" text-anchor="{anchor}">{e(ed["label"])}</text>')
    for key, n in nodes.items():
        x, y, nw, nh, label = n[:5]
        sub = n[5] if len(n) > 5 else ""
        kind = n[6] if len(n) > 6 else ""
        cx = x + nw / 2
        out.append(f'<g class="dg-node {kind}"><rect x="{x}" y="{y}" width="{nw}" height="{nh}" rx="9"/>')
        if sub:
            out.append(f'<text class="dg-label" x="{cx}" y="{y+nh/2-3}" text-anchor="middle">{e(label)}</text>')
            out.append(f'<text class="dg-sub" x="{cx}" y="{y+nh/2+13}" text-anchor="middle">{e(sub)}</text>')
        else:
            out.append(f'<text class="dg-label" x="{cx}" y="{y+nh/2+4.5}" text-anchor="middle">{e(label)}</text>')
        out.append('</g>')
    out.append('</svg>')
    return "".join(out)

def D_aws(did="aws"):
    n = {
        "atk": (10, 124, 124, 56, "Stratus Red Team", "attack simulation", "warn"),
        "log": (158, 124, 124, 56, "CloudTrail", "+ GuardDuty"),
        "eb":  (306, 124, 124, 56, "EventBridge", "event rules"),
        "fn":  (454, 124, 124, 56, "4 Lambda", "responders", "accent"),
        "ok":  (602, 124, 108, 56, "Remediated", "4.5 – 8.5 s", "accent"),
        "sns": (400, 232, 120, 44, "SNS alert", "", "info"),
        "ath": (540, 232, 170, 44, "Athena · CloudWatch", "", "info"),
    }
    ed = [
        {"from": "atk", "to": "log", "kind": "warn"},
        {"from": "log", "to": "eb"},
        {"from": "eb", "to": "fn", "flow": True, "kind": "accent"},
        {"from": "fn", "to": "ok", "kind": "accent"},
        {"from": "fn", "to": "sns", "x1": 500},
        {"from": "fn", "to": "ath", "x1": 540, "x2": 600},
    ]
    groups = [(140, 30, 580, 170, "AWS account · deployed with Terraform · 1 least-privilege IAM role per responder")]
    return diagram(did, 720, 290, n, ed, "AWS detection and response pipeline: attack events flow from CloudTrail and GuardDuty through EventBridge to four Lambda responders that remediate and alert", groups)

def D_guard(did="guard"):
    n = {
        "agent": (10, 126, 120, 56, "AI agent", "LLM client"),
        "c1": (196, 46, 250, 38, "1  API-key identity", "", "accent"),
        "c2": (196, 100, 250, 38, "2  Input sanitisation", "", "accent"),
        "c3": (196, 154, 250, 38, "3  ABAC per tool", "", "accent"),
        "c4": (196, 208, 250, 38, "4  Human approval (destructive)", "", "accent"),
        "mcp": (520, 70, 190, 56, "GitHub MCP server", "official"),
        "gh":  (520, 160, 190, 40, "GitHub API", ""),
        "log": (520, 230, 190, 44, "Security log", "every denial", "deny"),
    }
    ed = [
        {"d": "M130 154H160V65H195", "kind": "accent", "flow": True},
        {"d": "M321 84V99"}, {"d": "M321 138V153"}, {"d": "M321 192V207"},
        {"d": "M446 65H480V98H519", "kind": "accent", "label": "allow", "lpos": (484, 90), "anchor": "start"},
        {"from": "mcp", "to": "gh"},
        {"d": "M446 227H480V252H519", "kind": "deny", "label": "deny", "lpos": (484, 244), "anchor": "start"},
    ]
    groups = [(176, 16, 290, 244, "SupervisorGuard · every tool call")]
    return diagram(did, 720, 290, n, ed, "SupervisorGuard intercepts every agent tool call, applies four checks, then either forwards to the GitHub MCP server or logs a denial", groups)

def D_firewall(did="fw"):
    n = {
        "in": (10, 60, 100, 56, "Prompt or", "command"),
        "l1": (134, 60, 104, 56, "L1 Regex", "known patterns", "accent"),
        "l2": (254, 60, 104, 56, "L2 Gibberish", "heuristic", "accent"),
        "l3": (374, 60, 104, 56, "L3 DeBERTa", "classifier", "accent"),
        "l4": (494, 60, 104, 56, "L4 Similarity", "vector search", "accent"),
        "out": (622, 60, 88, 56, "Agent", "executes"),
        "blk": (134, 190, 464, 44, "Blocked  ·  audit-logged", "", "deny"),
    }
    ed = [
        {"from": "in", "to": "l1"}, {"from": "l1", "to": "l2", "kind": "accent"},
        {"from": "l2", "to": "l3", "kind": "accent"}, {"from": "l3", "to": "l4", "kind": "accent"},
        {"from": "l4", "to": "out", "kind": "accent", "label": "clean", "lpos": (610, 52)},
    ] + [{"d": f"M{x} 116V189", "kind": "deny"} for x in (186, 306, 426, 546)]
    return diagram(did, 720, 250, n, ed, "Four-layer agentic firewall: regex, gibberish heuristic, DeBERTa classifier and similarity search; any layer can block and log the input")

def D_med(did="med"):
    n = {
        "agent": (10, 112, 124, 56, "Clinical AI", "agent"),
        "gw":  (170, 112, 150, 56, "MedGuard gateway", "FastAPI", "accent"),
        "opa": (370, 20, 160, 52, "Open Policy Agent", "Rego · fail-closed", "info"),
        "tok": (370, 112, 160, 56, "Capability token", "1 use · 30 s", "accent"),
        "rec": (580, 112, 130, 56, "Patient records", "PHI scrubbed"),
        "aud": (370, 204, 160, 44, "JSON audit event", "every decision", "deny"),
    }
    ed = [
        {"from": "agent", "to": "gw"},
        {"from": "gw", "to": "opa", "kind": "", "label": "decide", "lpos": (340, 40), "anchor": "end"},
        {"from": "gw", "to": "tok", "kind": "accent", "flow": True},
        {"from": "tok", "to": "rec", "kind": "accent", "label": "1 user·tool·patient", "lpos": (555, 102)},
        {"from": "gw", "to": "aud", "kind": "deny", "label": "log", "lpos": (340, 240), "anchor": "end"},
    ]
    return diagram(did, 720, 270, n, ed, "MedGuard: the gateway asks OPA for a decision, issues a single-use capability token bound to user, tool and patient, scrubs PHI and logs every decision")

def D_honey(did="hp"):
    n = {
        "atk": (10, 110, 116, 60, "Attacker", "SSH · HTTP", "warn"),
        "obs": (150, 110, 128, 60, "Observe", "cmds · timing"),
        "sc":  (302, 110, 142, 60, "Threat score", "entropy+Bayes"),
        "fsm": (468, 110, 104, 60, "State", "engine", "accent"),
        "id":  (596, 110, 114, 60, "Shift identity", "banner · timing", "accent"),
        "b":   (150, 214, 422, 44, "Benchmarked vs Cowrie · Dionaea · Heralding · Elasticpot", "", "ghost"),
    }
    ed = [
        {"from": "atk", "to": "obs", "kind": "warn"}, {"from": "obs", "to": "sc"},
        {"from": "sc", "to": "fsm"}, {"from": "fsm", "to": "id", "kind": "accent", "flow": True},
        {"d": "M653 110V50H68V109", "kind": "accent", "label": "adapted responses as threat score rises", "lpos": (360, 42)},
    ]
    return diagram(did, 720, 270, n, ed, "Adaptive honeypot: attacker activity is scored with entropy and Bayesian updating, a state engine shifts the honeypot's SSH and HTTP identity in response")

def D_recon(did="rc"):
    n = {
        "d":  (10, 70, 100, 60, "Target", "domain"),
        "p":  (130, 70, 100, 60, "Passive", "DNS · CT logs"),
        "a":  (250, 70, 100, 60, "Assets", "inventory"),
        "g":  (370, 70, 100, 60, "Guardrail", "PII · injection", "accent"),
        "l":  (490, 70, 100, 60, "Local LLM", "Ollama · P1–P4", "info"),
        "r":  (610, 70, 100, 60, "Report", ".md / .docx"),
    }
    ed = [{"from": a, "to": b, "kind": k} for a, b, k in (("d","p",""),("p","a",""),("a","g","accent"),("g","l","accent"),("l","r",""))]
    return diagram(did, 720, 170, n, ed, "AI attack-surface platform: passive recon builds an asset inventory, a guardrail redacts PII and scores injection risk, a local LLM triages P1 to P4 and writes a report")

def D_soc(did="soc"):
    n = {
        "k": (10, 70, 150, 60, "Kali Linux", "~20 attack scenarios", "warn"),
        "w": (196, 70, 160, 60, "Windows endpoint", "Sysmon telemetry"),
        "s": (392, 70, 140, 60, "Splunk SIEM", "central logging", "accent"),
        "t": (568, 70, 142, 60, "SPL detections", "triage · investigate", "accent"),
    }
    ed = [{"from": "k", "to": "w", "kind": "warn"}, {"from": "w", "to": "s", "flow": True, "kind": "accent"}, {"from": "s", "to": "t", "kind": "accent"}]
    return diagram(did, 720, 170, n, ed, "SOC home lab: attacks from Kali against a Windows endpoint, Sysmon telemetry forwarded to Splunk, SPL searches for detection and triage")

# ------------------------------------------------------------------ charts
def bars(title, rows, note=""):
    o = [f'<div class="chart"><div class="chart-title">{e(title)}</div>']
    for r in rows:
        lbl, pct, val = r[0], r[1], r[2]
        cls = r[3] if len(r) > 3 else ""
        style = f' style="--lo:{r[4]}"' if len(r) > 4 else ""
        o.append(f'<div class="bar-row"><span class="bl">{e(lbl)}</span><div class="bar-track"><div class="bar-fill {cls}" data-w="{pct}%"{style}></div></div><span class="bv">{e(val)}</span></div>')
    if note: o.append(f'<div class="chart-note">{e(note)}</div>')
    o.append('</div>')
    return "".join(o)

def stats(items):
    return '<div class="stat-grid">' + "".join(f'<div><div class="v">{v}</div><div class="k">{e(k)}</div></div>' for v, k in items) + '</div>'

def tags(ts): return '<div class="tags">' + "".join(f'<span class="tag">{e(t)}</span>' for t in ts) + '</div>'

# ------------------------------------------------------------------ icons
I = {
 "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.4 8.3-8 9-4.6-.7-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>',
 "cloud": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 18a4.5 4.5 0 01-.6-9A6 6 0 0118 9.5 4.3 4.3 0 0117.5 18z"/></svg>',
 "key": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l3 3M15 8l2 2"/></svg>',
 "cpu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M10 10h4v4h-4zM9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>',
 "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>',
 "pen": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4L19 9l-4-4L4 16z"/><path d="M13 7l4 4"/></svg>',
}

# ------------------------------------------------------------------ layout
NAV = [("index.html", "Home"), ("projects.html", "Projects"), ("ai-lab.html", "AI Security"),
       ("research.html", "Research"), ("articles.html", "Writing"), ("about.html", "About")]

def page(fname, title, desc, body):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{l}</a>' for h, l in NAV)
    url = SITE + ("" if fname == "index.html" else fname)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0A0E16">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<link rel="canonical" href="{url}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230F1522'/%3E%3Ctext x='16' y='21' font-family='monospace' font-size='14' fill='%236EE7C8' text-anchor='middle'%3EAS%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="container nav-wrap">
<a class="brand" href="index.html"><span class="brand-mark">AS</span>Ahilya Sarnaik</a>
<button class="menu" type="button" aria-controls="primary-nav" aria-expanded="false">Menu</button>
<nav id="primary-nav" aria-label="Primary">{nav}<a class="nav-cv" href="resume.pdf" target="_blank" rel="noopener">Download CV</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="footer"><div class="container">
<span>© 2026 Ahilya Sarnaik · Dublin, Ireland</span>
<nav aria-label="Elsewhere"><a href="mailto:{EMAIL}">{EMAIL}</a><a href="{GH}" target="_blank" rel="noopener">GitHub</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a><a href="{MEDIUM}" target="_blank" rel="noopener">Medium</a></nav>
</div></footer>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""

CTA = f"""<section class="section"><div class="container"><div class="callout reveal">
<div><p class="kicker">Open to roles in Ireland</p><h2>Looking for a security engineer who builds the control and then tests it?</h2>
<p class="muted">Graduate and early-career roles in SOC, detection engineering, cloud security, IAM and AI security. Stamp 1G: no sponsorship needed.</p></div>
<div class="actions"><a class="btn primary" href="mailto:{EMAIL}">Email me</a><a class="btn secondary" href="{LI}" target="_blank" rel="noopener">LinkedIn</a></div>
</div></div></section>"""

# ------------------------------------------------------------------ projects data
PROJECTS = [
 dict(id="aws-detection-response", cat="cloud detection", label="Cloud · Detection & response", date="Jun 2026",
  title="AWS automated threat detection & response",
  problem="Cloud attacks such as opening SSH to the internet, backdooring an S3 bucket or switching off CloudTrail do their damage in minutes. I wanted the response to happen in seconds, without a human in the loop.",
  points=["<strong>4 Python responders</strong> on Lambda, triggered by EventBridge rules over CloudTrail and GuardDuty findings, each remediating one attack technique.",
          "Deployed with <strong>Terraform</strong>, one least-privilege IAM role per responder, plus dry-run mode for safe testing.",
          "Validated against real attack techniques using <strong>Stratus Red Team</strong> in a sandbox account.",
          "SNS alerting, CloudWatch metrics and Athena queries over CloudTrail for investigation; pytest with mocked AWS in a <strong>GitHub Actions</strong> CI pipeline."],
  stack=["Python","Lambda","EventBridge","CloudTrail","GuardDuty","Terraform","Athena","GitHub Actions"],
  diagram=D_aws, link=repo("aws-detection-response"),
  results=lambda: bars("Time to remediate (sandbox, Stratus Red Team)", [
      ("SSH exposed to internet", 56, "4.5–5.6 s", "range", "80%"),
      ("CloudTrail logging stopped", 84, "8.4 s"),
      ("S3 bucket policy backdoor", 85, "8.5 s")], "Scale: 0–10 seconds. Measured end-to-end from attack to reversal.")),
 dict(id="supervisorguard", cat="ai", label="AI security · Authorization", date="2026",
  title="SupervisorGuard AI: runtime enforcement for MCP agents",
  problem="AI agents connected to real tools can be talked into doing things their user never approved. Model output can't be the security boundary, so the boundary has to sit between the agent and the tool.",
  points=["Security layer that <strong>intercepts every agent tool call</strong> to the official GitHub MCP server before it executes, tested against live GitHub API calls.",
          "Enforces <strong>API-key identity</strong>, input sanitisation, <strong>attribute-based access control</strong> per tool, and human approval for destructive actions such as merges.",
          "Every denial is written to a security log, so blocked attempts can be investigated afterwards."],
  stack=["Python","FastAPI","MCP","ABAC","GitHub API"],
  diagram=D_guard, link=repo("supervisor-ai-chatbot"),
  results=lambda: stats([("4 / 4","tested attacks blocked"),("0","unlogged denials"),("4","enforcement checks")]) +
     '<ul style="margin-top:16px"><li>Prompt injection</li><li>Role spoofing</li><li>Unauthenticated escalation</li><li>Self-approval of a merge</li></ul>'),
 dict(id="agentic-firewall", cat="ai", label="AI security · Prompt injection", date="2026",
  title="Agentic firewall & MCP tool sanitizer",
  problem="AI coding agents read untrusted text all day. Single-layer filters are either too strict or easy to bypass, and a poisoned MCP tool can leak secrets without any obviously bad prompt.",
  points=["<strong>Four-layer screen</strong> for prompts and commands: regex rules, a gibberish heuristic, a fine-tuned <strong>DeBERTa</strong> classifier, and similarity matching against known attacks.",
          "<strong>Sanitizing proxy</strong> hides poisoned MCP tools, including tool pairs that only leak secrets when used together.",
          "Every block is audit-logged with the layer that caught it."],
  stack=["Python","DeBERTa","Vector search","MCP"],
  diagram=D_firewall, link=repo("Sanitization_tool"),
  results=lambda: stats([("94.7%","recall on attack prompts"),("3.2%","false-positive rate"),("4","detection layers")])),
 dict(id="medguard", cat="ai iam", label="IAM · Healthcare AI", date="Jan 2026",
  title="MedGuard: access governance gateway for clinical AI",
  problem="An AI assistant in a hospital should only ever see the records of patients its user is assigned to, and patient data must never leak in its answers.",
  points=["<strong>Fail-closed</strong> gateway with policies in <strong>Open Policy Agent (Rego)</strong>: no decision means no access.",
          "Issues <strong>single-use, 30-second capability tokens</strong> bound to one user, one tool and one patient.",
          "<strong>PHI scrubbing</strong> on output and a JSON audit event for every allow and deny decision.",
          "Threat model mapping <strong>7 threats</strong> to a control and a test each, backed by <strong>28 automated tests</strong>."],
  stack=["FastAPI","OPA / Rego","HMAC-SHA256","Docker Compose","pytest"],
  diagram=D_med, link=repo("MedGuard-Agent"),
  results=lambda: stats([("7","threats → control → test"),("28","automated tests"),("30 s","token lifetime, single use")])),
 dict(id="adaptive-honeypot", cat="research detection", label="Research · MSc thesis", date="Sep 2026",
  title="Adaptive honeypot architecture",
  problem="Static honeypots are easy for attackers to fingerprint. Can a honeypot change how it looks as an attacker becomes more hostile, and stay lightweight while doing it?",
  points=["Python honeypot that changes its <strong>SSH and HTTP identity</strong>, status codes and response timing as the attacker's threat score rises.",
          "Threat scoring with <strong>entropy</strong> and <strong>Bayesian updating</strong>, driving a finite-state engine.",
          "Benchmarked against <strong>Cowrie, Dionaea, Heralding and Elasticpot</strong> across <strong>91 attack runs</strong> in an isolated lab, using packet captures, container metrics and logs."],
  stack=["Python","Docker Compose","Ubuntu Server","Kali Linux","TShark","UFW"],
  diagram=D_honey, link=repo("adaptive_honeypot"),
  results=lambda: stats([("0.04%","CPU, lowest of all 5"),("17 MiB","memory footprint"),("1.8–3.4×","lighter than baselines")])),
 dict(id="attack-surface", cat="ai detection", label="Recon · AI guardrails", date="2026",
  title="AI attack-surface intelligence platform",
  problem="Recon produces long lists of assets that someone has to triage. A local LLM can help, but the LLM itself becomes an injection target.",
  points=["<strong>Passive recon</strong> from DNS and certificate-transparency logs builds an asset inventory.",
          "A <strong>local LLM</strong> (Ollama) triages each asset from P1 to P4 and writes a report in Markdown or Word.",
          "Guardrail layer <strong>redacts PII</strong> and scores injection risk before anything reaches the model."],
  stack=["Python","Ollama","DNS","Certificate transparency"],
  diagram=D_recon, link=repo("AI_Passive_Reccon_Plaform"),
  results=lambda: bars("Red-team payloads that succeeded", [
      ("Without guardrail", 83, "10 / 12", "deny"),
      ("With guardrail", 17, "2 / 12")])),
 dict(id="soc-lab", cat="detection", label="SOC · SIEM", date="Jan 2025",
  title="SOC home lab: SIEM monitoring & threat detection",
  problem="Detection rules are only useful if you've seen what the attack looks like in your own logs. I built a lab to generate that evidence and practise investigating it.",
  points=["Virtualised environment forwarding <strong>Windows Sysmon</strong> telemetry to <strong>Splunk</strong> for central logging and endpoint monitoring.",
          "Simulated around <strong>20 attack scenarios</strong> from Kali Linux to test detection visibility.",
          "Wrote <strong>SPL searches</strong> to correlate attack indicators, triage alerts and investigate endpoint activity, mapped to MITRE ATT&amp;CK."],
  stack=["Splunk","Sysmon","Windows","Kali Linux","MITRE ATT&CK"],
  diagram=D_soc, link=None,
  results=lambda: stats([("~20","attack scenarios"),("8+","custom detections"),("ATT&amp;CK","mapped techniques")])),
 dict(id="federated-ids", cat="research", label="Research · ML security", date="2026",
  title="Federated intrusion detection on skewed traffic",
  problem="In federated learning each organisation's network traffic looks different. Standard averaging (FedAvg) breaks down when that data is highly skewed.",
  points=["Designed <strong>adaptive gated aggregation</strong> for federated intrusion detection across non-IID clients.",
          "Raised <strong>F1 from 0.68 to 0.81</strong> over FedAvg on highly skewed traffic at about a <strong>5% false-alarm rate</strong>."],
  stack=["Federated learning","Python","IDS","Evaluation"],
  diagram=None, link=None,
  results=lambda: bars("F1 score on highly skewed traffic", [
      ("FedAvg baseline", 68, "0.68", "muted"),
      ("Adaptive gated aggregation", 81, "0.81")], "≈5% false-alarm rate. Scale 0–1.")),
]
P = {p["id"]: p for p in PROJECTS}

def case(p):
    link = (f'<a class="text-link external" href="{p["link"]}" target="_blank" rel="noopener">View code on GitHub</a>' if p["link"] else '')
    vis = ""
    if p["diagram"]:
        vis += f'<div class="panel"><div class="panel-label"><span>Architecture</span></div><div class="diagram-wrap">{p["diagram"](p["id"]+"-d")}</div></div>'
    vis += f'<div class="panel"><div class="panel-label"><span>Results</span></div>{p["results"]()}</div>'
    pts = "".join(f"<li>{x}</li>" for x in p["points"])
    return f"""<article class="case" id="{p['id']}" data-cat="{p['cat']}">
<div class="case-head">
<div class="case-meta"><span class="cat">{e(p['label'])}</span><span>{e(p['date'])}</span></div>
<h2>{e(p['title'])}</h2>
<p class="problem">{e(p['problem'])}</p>
<ul>{pts}</ul>
{tags(p['stack'])}
{link}
</div>
<div class="case-visual">{vis}</div>
</article>"""

# ------------------------------------------------------------------ pages
def index():
    logs = [
        ("fix", "REMEDIATE", "aws-responder", "Security group opened SSH to 0.0.0.0/0. Rule revoked in 4.5 s."),
        ("deny", "DENY", "supervisorguard", "merge_pull_request: agent attempted self-approval. Human approval required."),
        ("deny", "BLOCK", "agentic-firewall", "Prompt injection caught at layer 3 (DeBERTa). Event logged."),
        ("deny", "DENY", "medguard", "Patient not assigned to caller. Policy fail-closed, no token issued."),
        ("warn", "ADAPT", "adaptive-honeypot", "Threat score rising. SSH banner and response timing rotated."),
        ("fix", "REMEDIATE", "aws-responder", "CloudTrail logging stopped. Trail restarted in 8.4 s."),
    ]
    rows = "".join(f'<div class="log {c}"><span class="verdict">{v}</span><span class="src">{s}</span><span class="msg">{e(m)}</span></div>' for c, v, s, m in logs)
    feat = []
    for pid, blurb, res in [
        ("aws-detection-response", "Event-driven pipeline that detects and reverses AWS attacks in seconds, validated with Stratus Red Team.", [("4.5 s","fastest remediation"),("4","Lambda responders")]),
        ("supervisorguard", "Runtime guardrail that intercepts every AI-agent tool call to the GitHub MCP server before it runs.", [("4 / 4","tested attacks blocked"),("ABAC","per-tool policy")]),
        ("adaptive-honeypot", "MSc thesis: a honeypot that changes its identity as attackers get more hostile, benchmarked against four established honeypots.", [("91","attack runs"),("0.04%","CPU usage")]),
    ]:
        p = P[pid]
        r = "".join(f'<div class="result"><div class="v">{v}</div><div class="k">{e(k)}</div></div>' for v, k in res)
        feat.append(f"""<a class="feature-card reveal" href="projects.html#{pid}">
<div class="fc-text"><div class="fc-meta">{e(p['label'])} · {e(p['date'])}</div><h3>{e(p['title'])}</h3><p>{e(blurb)}</p>
<div class="result-row">{r}</div>{tags(p['stack'][:5])}<span class="text-link">Read case study →</span></div>
<div class="fc-visual"><div class="diagram-wrap" style="width:100%">{p['diagram'](pid+'-h')}</div></div></a>""")
    more = []
    for pid, blurb in [("agentic-firewall","Four-layer prompt-injection screen for AI coding agents: 94.7% recall at 3.2% false positives."),
                       ("medguard","Fail-closed OPA gateway that limits clinical AI agents to assigned patients, with 30-second capability tokens."),
                       ("attack-surface","Passive recon with local-LLM triage and a guardrail that cut successful injections from 10/12 to 2/12."),
                       ("soc-lab","Sysmon telemetry into Splunk, ~20 simulated attacks, and custom SPL detections mapped to ATT&CK.")]:
        p = P[pid]
        more.append(f'<article class="card reveal"><div class="fc-meta">{e(p["label"])}</div><h3>{e(p["title"])}</h3><p>{e(blurb)}</p>{tags(p["stack"][:4])}<a class="text-link" href="projects.html#{pid}">Case study →</a></article>')
    focus = [("cloud","Cloud detection & response","AWS CloudTrail, GuardDuty, EventBridge and Lambda: detect, contain and reverse in seconds."),
             ("shield","SOC & investigation","Splunk, Sysmon, MITRE ATT&CK and seven months of forensic casework."),
             ("key","Identity & access","Least-privilege IAM, ABAC and policy-as-code with Open Policy Agent."),
             ("cpu","AI agent security","Prompt injection, MCP tool poisoning and runtime authorization for agents.")]
    fc = "".join(f'<article class="card reveal"><div class="icon">{I[i]}</div><h3>{t}</h3><p>{d}</p></article>' for i, t, d in focus)
    body = f"""
<section class="hero"><div class="container">
<div class="hero-grid">
<div>
<p class="eyebrow">Cybersecurity engineer · Dublin</p>
<h1>I build security controls, then try to break them.</h1>
<p class="lead">I'm Ahilya Sarnaik, an MSc Cybersecurity graduate (NCI, 2026). I build automated cloud response on AWS, runtime guardrails for AI agents, and detection labs, and I measure every one of them against real attacks.</p>
<div class="actions"><a class="btn primary" href="projects.html">View case studies</a><a class="btn secondary" href="resume.pdf" target="_blank" rel="noopener">Download CV</a></div>
<div class="status"><span class="dot"></span>Open to roles in Ireland · Stamp 1G, no sponsorship needed</div>
</div>
<div class="console" aria-label="Sample security events produced by my projects">
<div class="console-bar"><div class="lights"><i></i><i></i><i></i></div><span>security-events.log</span><span>live</span></div>
<div class="console-body">{rows}</div>
<div class="console-foot"><span>Events from projects on this site</span><span class="cursor"></span></div>
</div>
</div>
<div class="metrics">
<div class="metric"><div class="num">4.5<small>s</small></div><div class="lbl">fastest automated AWS remediation</div></div>
<div class="metric"><div class="num">94.7<small>%</small></div><div class="lbl">prompt-injection recall, 3.2% FP</div></div>
<div class="metric"><div class="num">91</div><div class="lbl">attack runs in honeypot thesis</div></div>
<div class="metric"><div class="num">7<small>mo</small></div><div class="lbl">digital forensics internship</div></div>
<div class="metric"><div class="num">Top 3<small>%</small></div><div class="lbl">globally on TryHackMe</div></div>
</div>
</div></section>

<section class="section"><div class="container">
<div class="section-heading"><div><p class="kicker">Featured work</p><h2>Built, attacked, measured.</h2><p class="muted">Every project ships with a threat model, an architecture and a number I can defend in an interview.</p></div><a class="text-link" href="projects.html">All projects →</a></div>
{''.join(feat)}
<div class="grid four" style="margin-top:20px">{''.join(more)}</div>
</div></section>

<section class="section alt"><div class="container">
<div class="section-heading"><div><p class="kicker">Focus areas</p><h2>Where I work.</h2></div></div>
<div class="grid four">{fc}</div>
</div></section>

<section class="section"><div class="container"><div class="split">
<div class="reveal"><p class="kicker">Background</p><h2>Investigator first, engineer second.</h2>
<p class="lead">My seven-month forensics internship at Excellent Cyber taught me to reconstruct incidents from logs, disk images and endpoint telemetry, and to write it up so a client could act on it. My projects now automate that kind of investigation in AWS and in AI agent pipelines.</p>
<div class="actions"><a class="btn secondary" href="about.html">Experience & skills</a><a class="btn secondary" href="research.html">Research</a></div></div>
<div class="panel reveal"><div class="panel-label"><span>At a glance</span></div><ul class="list-plain">
<li><span>MSc Cybersecurity, National College of Ireland</span><span>2:1 · 2026</span></li>
<li><span>BTech Computer Science (AI &amp; ML)</span><span>8.7 CGPA</span></li>
<li><span>Cyber Forensic Intern, Excellent Cyber</span><span>Jan–Jul 2025</span></li>
<li><span>Poster, AICS 2026</span><span>concept drift</span></li>
<li><span>ISO/IEC 27001 Information Security Associate</span><span>Feb 2026</span></li>
<li><span>CompTIA Security+</span><span><span class="badge">Dec 2026</span></span></li>
</ul></div>
</div></div></section>
{CTA}"""
    return page("index.html", "Ahilya Sarnaik · Cybersecurity Engineer, Dublin",
                "Dublin-based cybersecurity engineer: AWS detection and response, SOC, IAM and AI agent security. Open to roles in Ireland, no sponsorship needed.", body)

def projects():
    cats = [("all","All"),("cloud","Cloud"),("ai","AI security"),("detection","Detection & SOC"),("iam","Identity & access"),("research","Research")]
    f = "".join(f'<button class="filter" type="button" data-cat="{c}" aria-pressed="{str(c=="all").lower()}">{l}</button>' for c, l in cats)
    body = f"""
<section class="page-hero"><div class="container">
<p class="eyebrow">Case studies</p><h1>Projects</h1>
<p class="lead">For each one: the problem, the architecture, what I built and how it held up when attacked. Code is linked wherever it's public.</p>
<div class="filters" role="group" aria-label="Filter projects">{f}</div>
</div></section>
<section class="section tight"><div class="container">{''.join(case(p) for p in PROJECTS)}</div></section>
{CTA}"""
    return page("projects.html", "Projects · Ahilya Sarnaik",
                "Security case studies: AWS automated response, MCP agent guardrails, prompt-injection firewall, OPA access gateway, adaptive honeypot, SOC lab.", body)

def ai_lab():
    rows = [("Direct prompt injection", 1,1,0,1), ("Indirect injection / poisoned tools", 0,1,0,1),
            ("Role spoofing & unauthenticated escalation", 1,0,1,0), ("Excessive agency / destructive actions", 1,0,1,0),
            ("Sensitive data leakage (secrets, PII, PHI)", 0,1,1,1), ("Unaudited decisions", 1,1,1,0)]
    tr = "".join("<tr><td>"+t+"</td>"+"".join('<td><span class="chk">✓</span></td>' if v else '<td><span class="dash">—</span></td>' for v in vals)+"</tr>" for t,*vals in rows)
    cards = "".join(f'<article class="card reveal"><div class="fc-meta">{e(P[i]["label"])}</div><h3>{e(P[i]["title"])}</h3><p>{e(P[i]["problem"])}</p><a class="text-link" href="projects.html#{i}">Case study →</a></article>'
                    for i in ("supervisorguard","agentic-firewall","medguard","attack-surface"))
    body = f"""
<section class="page-hero"><div class="container">
<p class="eyebrow">AI agent security</p><h1>Securing what AI agents are allowed to do.</h1>
<p class="lead">An agent with tools has the permissions of every tool it can call. I build the controls that sit outside the model: identity, authorization, input screening, data scrubbing and audit. Then I red-team them.</p>
</div></section>
<section class="section tight"><div class="container">
<div class="section-heading"><div><p class="kicker">Coverage</p><h2>Which threat each project defends against</h2><p class="muted">Threat categories follow the OWASP Top 10 for LLM Applications and MITRE ATLAS.</p></div></div>
<div class="table-wrap reveal"><table class="matrix"><thead><tr><th>Threat</th><th>SupervisorGuard</th><th>Agentic firewall</th><th>MedGuard</th><th>Recon guardrail</th></tr></thead><tbody>{tr}</tbody></table></div>
</div></section>
<section class="section"><div class="container"><div class="grid">{cards}</div></div></section>
<section class="section alt"><div class="container">
<div class="section-heading"><div><p class="kicker">Principles</p><h2>How I approach it</h2></div></div>
<div class="grid three">
<article class="card reveal"><div class="icon">{I['key']}</div><h3>Enforce outside the model</h3><p>Permissions are checked by code the model can't talk its way past: identity, ABAC and policy-as-code.</p></article>
<article class="card reveal"><div class="icon">{I['shield']}</div><h3>Everything untrusted is input</h3><p>Retrieved text, tool descriptions and tool results are screened like user input, because attackers put payloads there.</p></article>
<article class="card reveal"><div class="icon">{I['search']}</div><h3>Evidence over claims</h3><p>Repeatable attack test cases, published recall and false-positive rates, and stated limitations.</p></article>
</div></div></section>
{CTA}"""
    return page("ai-lab.html", "AI Agent Security · Ahilya Sarnaik",
                "AI agent security projects: MCP runtime authorization, prompt-injection firewall, clinical AI access gateway and LLM guardrails.", body)

def research():
    hp = P["adaptive-honeypot"]; fd = P["federated-ids"]
    body = f"""
<section class="page-hero"><div class="container">
<p class="eyebrow">Research</p><h1>Where defences drift, adapt or fail.</h1>
<p class="lead">My research asks practical questions about detection systems: what happens when the data changes, when attackers fingerprint the defence, or when training data isn't evenly spread.</p>
</div></section>
<section class="section tight"><div class="container">
<div class="panel reveal" style="padding:36px">
<div class="case-meta" style="margin-bottom:14px"><span class="cat">Poster · AICS 2026</span><span>Malware detection</span></div>
<h2 style="font-size:clamp(1.5rem,2.6vw,2rem)">Adaptive retraining for malware detection under concept drift</h2>
<p class="lead" style="margin-top:14px">Does ADWIN-triggered retraining beat a fixed schedule for detecting malicious Chrome extensions as the ecosystem changes?</p>
<div class="grid three" style="margin-top:28px">
<div><p class="kicker" style="margin-bottom:8px">Finding</p><p class="muted">Adaptive timing did not consistently beat evenly spaced retraining at the same frequency.</p></div>
<div><p class="kicker" style="margin-bottom:8px">Trade-off</p><p class="muted">During a major ecosystem shift it caught more malware, but at the cost of substantially more analyst alerts.</p></div>
<div><p class="kicker" style="margin-bottom:8px">Takeaway</p><p class="muted">Retraining frequency, training data and alert cost matter as much as how clever the schedule is.</p></div>
</div></div>
</div></section>
<section class="section tight"><div class="container"><div class="grid">
<article class="card reveal"><div class="fc-meta">MSc thesis · Sep 2026</div><h3>{e(hp['title'])}</h3><p>{e(hp['problem'])}</p>{hp['results']()}<a class="text-link" href="projects.html#adaptive-honeypot">Case study →</a></article>
<article class="card reveal"><div class="fc-meta">ML security · 2026</div><h3>{e(fd['title'])}</h3><p>{e(fd['problem'])}</p>{fd['results']()}<a class="text-link" href="projects.html#federated-ids">Details →</a></article>
<article class="card reveal"><div class="fc-meta">Threat intelligence · 2026</div><h3>Pykspa trojan behaviour analysis</h3><p>Network-forensics analysis of the Pykspa trojan, documenting its domain generation algorithm, command-and-control traffic and persistence.</p>{tags(['Network forensics','DGA','C2','Wireshark'])}</article>
<article class="card reveal"><div class="fc-meta">NLP security</div><h3>BERT phishing classifier</h3><p>Transformer-based phishing detection evaluated on a held-out set.</p>{stats([('0.3%','false positives'),('0.9998','ROC-AUC'),('BERT','model')])}</article>
</div></div></section>
<section class="section tight"><div class="container"><div class="section-heading"><div><p class="kicker">Publications</p><h2>Published work</h2></div></div>
<div class="panel reveal"><ul class="list-plain">
<li><span><strong>Intelligent violence detection</strong>, first author. International Journal for Multidisciplinary Research (IJFMR), Vol 7, Issue 3. <a class="text-link external" href="https://doi.org/10.36948/ijfmr.2025.v07i03.44243" target="_blank" rel="noopener">DOI</a></span><span>2025</span></li>
<li><span><strong>Adaptive retraining for malware detection under concept drift</strong>, poster presentation, AICS</span><span>2026</span></li>
</ul></div></div></section>
{CTA}"""
    return page("research.html", "Research · Ahilya Sarnaik",
                "Security research: concept drift in malware detection (AICS 2026), adaptive honeypots, federated intrusion detection, Pykspa trojan analysis.", body)

def articles():
    topics = [("cpu","AI agent security","Prompt injection, tool authorization and MCP trust boundaries, written from building and attacking SupervisorGuard and the agentic firewall."),
              ("search","Reconnaissance","Passive recon techniques and how to triage what you find without drowning in assets."),
              ("shield","ISO 27001 & vendor risk","Applying ISO/IEC 27001 Annex A controls to real vendor and cloud configurations.")]
    c = "".join(f'<article class="card reveal"><div class="icon">{I[i]}</div><h3>{t}</h3><p>{d}</p><a class="text-link external" href="{MEDIUM}" target="_blank" rel="noopener">Read on Medium</a></article>' for i,t,d in topics)
    body = f"""
<section class="page-hero"><div class="container">
<p class="eyebrow">Writing</p><h1>Technical write-ups</h1>
<p class="lead">I publish what I learn from building and breaking things: what worked, what didn't, and the numbers. My writing lives on Medium.</p>
<div class="actions"><a class="btn primary" href="{MEDIUM}" target="_blank" rel="noopener">All articles on Medium ↗</a></div>
</div></section>
<section class="section tight"><div class="container"><div class="grid three">{c}</div></div></section>
<section class="section tight"><div class="container"><div class="panel reveal"><div class="panel-label"><span>Also</span></div><ul class="list-plain">
<li><span>Hands-on labs on <a class="text-link external" href="{THM}" target="_blank" rel="noopener">TryHackMe</a>: 40+ rooms across SOC, web, Windows and AI</span><span>Top 3% global</span></li>
<li><span>Source code and READMEs on <a class="text-link external" href="{GH}" target="_blank" rel="noopener">GitHub</a></span><span>public repos</span></li>
</ul></div></div></section>
{CTA}"""
    return page("articles.html", "Writing · Ahilya Sarnaik", "Technical security writing on AI agent security, reconnaissance and ISO 27001 vendor risk.", body)

def about():
    skills = [("Security operations","Splunk SPL, Sysmon, MITRE ATT&CK, Sigma, Wireshark, log analysis, digital forensics, alert triage"),
              ("Cloud security (AWS)","IAM, STS, VPC, EC2, S3, CloudTrail, GuardDuty, Lambda, EventBridge, SNS, Athena, Terraform"),
              ("Identity & access","Least-privilege IAM, ABAC, Open Policy Agent (Rego), capability tokens"),
              ("AI security","Prompt injection, MCP tool poisoning, guardrails, PII redaction, OWASP LLM Top 10, MITRE ATLAS"),
              ("Engineering","Python, Bash, PowerShell, FastAPI, Docker, Linux, GitHub Actions, pytest, Git"),
              ("Governance & testing","ISO/IEC 27001, NIST CSF, threat modelling, OWASP Top 10, Nmap, Burp Suite, Metasploit")]
    sk = "".join(f'<article class="card reveal"><h3>{e(t)}</h3><p>{e(d)}</p></article>' for t,d in skills)
    body = f"""
<section class="page-hero"><div class="container">
<p class="eyebrow">About</p><h1>Ahilya Sarnaik</h1>
<p class="lead">Cybersecurity engineer based in Dublin. I studied AI and machine learning, then cybersecurity, and I work where the two meet: detecting and responding to attacks in the cloud, and controlling what AI agents can do.</p>
<div class="status"><span class="dot"></span>Stamp 1G · eligible to work full-time in Ireland, no sponsorship required</div>
</div></section>
<section class="section tight"><div class="container"><div class="split">
<div><p class="kicker">Experience</p><div class="timeline">
<div class="tl-item reveal"><div class="tl-when">2025 – present</div><div><h3>Independent AI &amp; cloud security research</h3><div class="org">Remote</div><ul>
<li>Red-team LLM applications and AI agents for prompt injection, role spoofing and tool poisoning, documenting each attack, control and residual risk.</li>
<li>Map AWS configurations and IAM policies to ISO/IEC 27001 Annex A controls with written remediation plans.</li>
<li>Publish technical write-ups on Medium.</li></ul></div></div>
<div class="tl-item reveal"><div class="tl-when">Jan – Jul 2025</div><div><h3>Cyber Forensic Intern</h3><div class="org">Excellent Cyber · Pune, India</div><ul>
<li>Investigated security incidents using system logs, disk images and endpoint telemetry, and performed root-cause analysis.</li>
<li>Explained forensic findings to clients in clear, non-technical terms.</li>
<li>Wrote post-incident reports with recommendations, maintaining chain of custody for all evidence.</li></ul></div></div>
</div>
<p class="kicker" style="margin-top:48px">Education</p><div class="timeline">
<div class="tl-item reveal"><div class="tl-when">Sep 2025 – Oct 2026</div><div><h3>MSc Cybersecurity · 2:1</h3><div class="org">National College of Ireland, Dublin</div><ul><li>Cloud security, SOC operations, malware analysis, AI/ML in cybersecurity. Thesis: adaptive honeypot architecture.</li></ul></div></div>
<div class="tl-item reveal"><div class="tl-when">2021 – 2025</div><div><h3>BTech Computer Science (AI &amp; ML) · CGPA 8.7</h3><div class="org">KIT's College of Engineering (Autonomous), Kolhapur</div></div></div>
</div></div>
<div class="panel reveal"><div class="panel-label"><span>Certifications &amp; achievements</span></div><ul class="list-plain">
<li><span>CompTIA Security+</span><span><span class="badge">exam Dec 2026</span></span></li>
<li><span>ISO/IEC 27001 Information Security Associate · SkillFront</span><span>Feb 2026</span></li>
<li><span>AWS Academy Graduate: Cloud Foundations; ML Foundations</span><span>Jan 2024</span></li>
<li><span>Cyber Security Management Job Simulation · ANZ (Forage)</span><span>Apr 2024</span></li>
<li><span>TryHackMe, 40+ rooms</span><span><span class="badge ok">Top 3%</span></span></li>
</ul><hr style="margin:18px 0"><div class="panel-label"><span>Community</span></div><ul class="list-plain">
<li><span>Volunteer, women-in-cybersecurity events</span><span>Dublin</span></li>
<li><span>Volunteer, Society of Women Engineers student events</span><span>Kolhapur</span></li>
</ul></div>
</div></div></section>
<section class="section alt"><div class="container"><div class="section-heading"><div><p class="kicker">Skills</p><h2>Technical toolkit</h2></div></div><div class="grid three">{sk}</div></div></section>
{CTA}"""
    return page("about.html", "About · Ahilya Sarnaik", "Experience, education, skills and certifications of Dublin-based cybersecurity engineer Ahilya Sarnaik.", body)

README = f"""# Ahilya Sarnaik: Cybersecurity Portfolio

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
"""

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in [("index.html", index), ("projects.html", projects), ("ai-lab.html", ai_lab),
                     ("research.html", research), ("articles.html", articles), ("about.html", about)]:
        with open(os.path.join(OUT, name), "w") as f: f.write(fn())
    with open(os.path.join(OUT, "README.md"), "w") as f: f.write(README)
    print("built")
