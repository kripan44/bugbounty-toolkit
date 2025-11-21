# bugbounty-toolkit
Fast, minimal Python helpers for basic recon during bug bounty engagements.

Summary

    Small collection of scripts to enumerate URLs/subdomains, extract links/endpoints, check host status, and a large XSS payload list for testing.
    Intended for authorized security testing only. Do not use against systems you do not have permission to test.

Included files

    recon.py — Run subdomain enumeration (subfinder + Sublist3r), fetch pages from discovered subdomains and save found URLs to a project report file.
    automated_link_scanner.py — Fetches each URL from an input file and extracts full URLs and endpoint-like paths from the fetched HTML.
    status-checker.py — Simple script to check reachability (HTTP/HTTPS) for a list of hostnames.
    xss-payload-list.txt — A large list of XSS payloads for manual testing or to feed into fuzzers. Contains potentially dangerous JS payloads and obfuscated variants.

Requirements

    Python 3.8+
    Python packages:
        requests
        urllib3
        tqdm (used by recon.py)
    External tools (for recon.py):
        subfinder (recommended)
        Sublist3r Ensure these are installed and available in your PATH if you want recon.py to perform enumeration.

Quick installation

    Clone the repo (if not already): git clone https://github.com/kripan44/bugbounty-toolkit.git
    Create a virtual environment (recommended) and install Python deps: python3 -m venv .venv source .venv/bin/activate pip install -r requirements.txt (If a requirements.txt is not present, install manually: pip install requests urllib3 tqdm )

Usage

    recon.py

    Purpose: Enumerate subdomains (via subfinder and Sublist3r), fetch each subdomain, extract discovered full URLs and write a report.
    Notes: recon.py expects subfinder and Sublist3r to be installed. The script performs HTTP(s) requests with verify=False and a 5 second timeout.
    Usage: python3 recon.py <target-url> <project-name> Example: python3 recon.py https://example.com myproject Output:
        Writes a file named myproject.txt with the scan report (subdomain sections and discovered URLs).

    automated_link_scanner.py

    Purpose: Given a text file containing one or more base URLs (or any text with URLs), fetch each URL and extract:
        full URLs (http/https)
        endpoint/path-like strings (routes, asset paths, query strings)
    Usage: python3 automated_link_scanner.py urls.txt Example urls.txt: https://example.com https://sub.example.com
    Output: Printed to stdout — extracted URLs and endpoints grouped by base URL.

    status-checker.py

    Purpose: Read a list of domains/hosts from a file and check both http:// and https:// reachability.
    Usage: python3 status-checker.py domain_list.txt Example domain_list.txt: example.com sub.example.com
    Output: Prints reachable hosts and HTTP status codes to stdout.

    xss-payload-list.txt

    Purpose: Payload repository to use for manual testing or to feed into scanners / fuzzers.
    Usage examples:
        Use with a fuzzer or proxy tool to inject into parameters.
        Grep/select payloads you want to test: grep "alert(1)" xss-payload-list.txt
    Warning: Contains active JavaScript payloads. Use only in authorized environments. Do not run these payloads in production browsers or systems you do not control.

Behavior notes & caveats

    SSL verification is disabled in recon.py and automated_link_scanner.py (requests.get(..., verify=False)). This avoids failures on sites with self-signed certs but suppresses certificate checks — be aware.
    Many usage/help strings in the scripts show different filenames (leftover/typo). Use the actual script name when invoking (examples above).
    recon.py relies on external enumeration tools and will silently skip subdomains that do not respond within timeouts.
    status-checker.py does not catch all network exceptions; intermittent failures may raise exceptions in some environments — you can wrap requests.get calls with try/except for robustness.

Ethics, legality & safety

    Use these tools only on targets you have permission to test.
    The XSS payload file contains potentially dangerous payloads (exfiltration, JS execution). Do not use them irresponsibly.
    Respect rate limits, robots.txt, and applicable laws.

Suggested improvements

    Add a requirements.txt and a Makefile or install script.
    Add logging, configurable timeouts, and retry logic.
    Save outputs (automated_link_scanner.py) to files (CSV/JSON) in addition to stdout.
    Add argument parsing (argparse) for clearer CLI help and flags (timeout, verify-ssl, concurrency).
    Improve error handling in status-checker.py and use session pooling for requests.
    Optionally integrate with common tools (ffuf, wfuzz) for automatic fuzzing using the XSS payloads.

Contributing

    Open issues and pull requests are welcome. Keep changes focused and include tests where applicable.

Support / Contact

    Repo owner: kripan44 (use GitHub issues on the repository for questions or feature requests).
