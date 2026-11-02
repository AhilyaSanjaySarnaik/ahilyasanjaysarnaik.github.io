# Ahilya Sarnaik — Cybersecurity Engineer

**Live site: [ahilyasanjaysarnaik.github.io](https://ahilyasanjaysarnaik.github.io/)**

MSc Cybersecurity graduate (National College of Ireland, 2026) based in Dublin. I build security controls, then attack them to see whether they hold: automated cloud response on AWS, runtime guardrails for AI agents, access-control gateways and detection labs.

Open to graduate and early-career roles in SOC, detection engineering, cloud security, IAM and AI security in Ireland. Stamp 1G: no sponsorship required.

---

## Featured projects

| Project | What it does | Result | Code |
|---|---|---|---|
| **AWS Automated Threat Detection & Response** | 4 Python Lambda responders triggered by EventBridge over CloudTrail and GuardDuty findings. They reverse common AWS attack techniques automatically. Deployed with Terraform, with one least-privilege IAM role per responder. | Exposed SSH closed in **4.5–5.6 s**; S3 backdoor removed in **8.5 s**; CloudTrail restarted in **8.4 s** (Stratus Red Team) | [repo](https://github.com/AhilyaSanjaySarnaik/aws-detection-response) |
| **SupervisorGuard AI** | Runtime enforcement layer that intercepts every AI-agent tool call to the GitHub MCP server, with API-key identity, input sanitisation, per-tool ABAC and human approval for destructive actions. | Blocked **4 / 4** tested attacks (prompt injection, role spoofing, unauthenticated escalation, self-approval) | [repo](https://github.com/AhilyaSanjaySarnaik/supervisor-ai-chatbot) |
| **Agentic Firewall & MCP Tool Sanitizer** | Four-layer screen for AI coding agents (regex, gibberish heuristic, DeBERTa classifier, similarity search) plus a proxy that hides poisoned MCP tools. | **94.7%** recall at **3.2%** false positives | [repo](https://github.com/AhilyaSanjaySarnaik/Sanitization_tool) |
| **MedGuard** | Fail-closed access gateway for clinical AI using Open Policy Agent (Rego). It issues single-use, 30-second capability tokens bound to one user, tool and patient, and scrubs PHI from output. | **7** threats each mapped to a control and a test; **28** automated tests | [repo](https://github.com/AhilyaSanjaySarnaik/MedGuard-Agent) |
| **Adaptive Honeypot** *(MSc thesis)* | Honeypot that shifts its SSH/HTTP identity, status codes and response timing as an attacker's threat score rises, using entropy scoring, Bayesian updating and a finite-state engine. | Lowest resource use of 5 honeypots: **0.04% CPU**, **17 MiB**, 1.8–3.4× lighter than Cowrie, Dionaea, Heralding and Elasticpot over 91 attack runs | [repo](https://github.com/AhilyaSanjaySarnaik/adaptive_honeypot) |
| **AI Attack-Surface Intelligence Platform** | Passive recon (DNS, certificate transparency) with local-LLM (Ollama) triage from P1 to P4 and auto-generated reports. A guardrail layer redacts PII and scores injection risk. | Successful red-team payloads cut from **10/12 to 2/12** | [repo](https://github.com/AhilyaSanjaySarnaik/AI_Passive_Reccon_Plaform) |
| **SOC Home Lab** | Windows Sysmon telemetry forwarded to Splunk; attacks simulated from Kali Linux and investigated with SPL. | ~20 attack scenarios, 8+ custom detections mapped to MITRE ATT&CK | — |
| **Federated Intrusion Detection** | Adaptive gated aggregation for federated IDS across clients with highly skewed traffic. | F1 raised from **0.68 to 0.81** over FedAvg at ~5% false-alarm rate | — |

## Research

- **Adaptive retraining for malware detection under concept drift**: poster at AICS 2026
- **Intelligent violence detection**: first author, IJFMR Vol 7, Issue 3, 2025 ([DOI](https://doi.org/10.36948/ijfmr.2025.v07i03.44243))
- **Pykspa trojan behaviour analysis**: DGA, C2 traffic and persistence through network forensics (2026)
- **BERT phishing classifier**: 0.3% false positives, 0.9998 ROC-AUC on a held-out set

## Experience & education

- **Cyber Forensic Intern**, Excellent Cyber, Pune (Jan–Jul 2025): incident investigation from logs, disk images and endpoint telemetry; root-cause analysis; post-incident reporting with chain of custody
- **MSc Cybersecurity**, National College of Ireland (2025–2026), 2:1
- **BTech Computer Science (AI & ML)**, KIT's College of Engineering, Kolhapur (2021–2025), CGPA 8.7

## Skills

**Security operations:** Splunk SPL, Sysmon, MITRE ATT&CK, Sigma, Wireshark, digital forensics
**Cloud (AWS):** IAM, CloudTrail, GuardDuty, Lambda, EventBridge, S3, Athena, Terraform
**Identity & access:** least-privilege IAM, ABAC, Open Policy Agent (Rego)
**AI security:** prompt injection, MCP tool poisoning, guardrails, OWASP LLM Top 10, MITRE ATLAS
**Engineering:** Python, FastAPI, Docker, Linux, GitHub Actions, pytest

**Certifications:** ISO/IEC 27001 Information Security Associate (2026) · AWS Academy Cloud Foundations (2024) · CompTIA Security+ (exam Dec 2026) · TryHackMe top 3% globally

## Contact

[Email](mailto:ahilyasarnaik12@gmail.com) · [LinkedIn](https://www.linkedin.com/in/ahilyacyber/) · [GitHub](https://github.com/AhilyaSanjaySarnaik) · [Medium](https://medium.com/@ahilya_Cyber)

---

<sub>This repo is a static site served by GitHub Pages. To edit the pages, change the HTML directly or edit `build.py` and run `python3 build.py`.</sub>
