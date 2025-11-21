import re
import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------------------
# FULL URL Pattern
# ---------------------------------------------------------
url_pattern = re.compile(
    r"""
    https?://
    (?:www\.)?
    [\w.-]+(?:\s*\.\s*[\w.-]+)+
    (?:/[^\s"'<>]*)?
    """,
    re.IGNORECASE | re.VERBOSE
)

# ---------------------------------------------------------
# ENDPOINT / PATH Pattern
# (matches API routes, endpoints, JS/CSS files, parameters, etc.)
# ---------------------------------------------------------
endpoint_pattern = re.compile(
    r"""
    (?:
        /[A-Za-z0-9_\-./]+       # /api/v1/user /assets/js/app.js
        (?:\?[^\s"'<>]*)?        # optional query params
    )
    """,
    re.VERBOSE
)

# ---------------------------------------------------------
# Validate Input
# ---------------------------------------------------------
if len(sys.argv) != 2:
    print("Usage: python3 extractor.py <file-with-urls>")
    sys.exit()

url_file = sys.argv[1]

try:
    with open(url_file, "r") as f:
        file_content = f.read()
except FileNotFoundError:
    print("File not found.")
    sys.exit()

# Extract base URLs from the input file
input_urls = sorted(set(url_pattern.findall(file_content)))

if not input_urls:
    print("No valid URLs found in file.")
    sys.exit()

print(f"[+] Loaded {len(input_urls)} URLs from {url_file}")
print("[*] Starting extraction...\n")

# ---------------------------------------------------------
# PROCESS EACH URL
# ---------------------------------------------------------
results = {}

for base_url in input_urls:
    print(f"[+] Fetching: {base_url}")
    found_urls = set()
    found_endpoints = set()

    try:
        r = requests.get(base_url, timeout=5, verify=False)
        html = r.text

        # Extract full URLs
        for m in url_pattern.findall(html):
            found_urls.add(m.strip())

        # Extract endpoints / routes
        for ep in endpoint_pattern.findall(html):
            clean = ep.strip()
            found_endpoints.add(clean)

    except Exception as e:
        print(f"    [-] Error: {e}")
        results[base_url] = {"urls": [], "endpoints": []}
        continue

    results[base_url] = {
        "urls": sorted(found_urls),
        "endpoints": sorted(found_endpoints)
    }

# ---------------------------------------------------------
# OUTPUT RESULTS
# ---------------------------------------------------------
print("\n==============================================")
print("                FINAL RESULTS")
print("==============================================\n")

for base, data in results.items():

    print(base)
    print("----------------------------------------------")

    urls = data["urls"]
    endpoints = data["endpoints"]

    # URLs
    if urls:
        print("  URLs:")
        for u in urls:
            print(f"    {u}")
    else:
        print("  URLs: (none)")

    print()

    # Endpoints
    if endpoints:
        print("  Endpoints:")
        for ep in endpoints:
            print(f"    {ep}")
    else:
        print("  Endpoints: (none)")

    print("\n")

print("Done.\n")
