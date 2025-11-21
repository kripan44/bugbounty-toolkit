import sys
import os
import re
import requests
import urllib3
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ---------------------------------------------------------
# URL Pattern
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
# Validate Input
# ---------------------------------------------------------
if len(sys.argv) != 3:
    print("Usage: python3 enum-tool.py <url> <project-name>")
    sys.exit()

input_url = sys.argv[1]
project_name = sys.argv[2]

if len(url_pattern.findall(input_url)) == 0:
    print("Invalid URL")
    sys.exit()

domain = (
    input_url.replace("https://", "")
             .replace("http://", "")
             .replace("www.", "")
             .split("/")[0]
)

print(f"\n[+] Project: {project_name}")
print(f"[+] Target Domain: {domain}\n")

# ---------------------------------------------------------
# Subdomain Enumeration
# ---------------------------------------------------------
print("[*] Running Subfinder...")
subfinder_out = os.popen(f"subfinder -d {domain} -all -silent").read()

print("[*] Running Sublist3r...")
sublist3r_out = os.popen(f"sublist3r -d {domain} -silent").read()

subdomains = set()

for line in subfinder_out.splitlines():
    if domain in line.strip():
        subdomains.add(line.strip())

for line in sublist3r_out.splitlines():
    if domain in line.strip():
        subdomains.add(line.strip())

subdomains = sorted(subdomains)

print(f"\n[+] Unique subdomains found: {len(subdomains)}\n")

# ---------------------------------------------------------
# Fetch Function (Multithreaded)
# ---------------------------------------------------------
def fetch_subdomain(sub):
    urls = set()
    targets = [f"https://{sub}", f"http://{sub}"]

    for t in targets:
        try:
            r = requests.get(t, timeout=5, verify=False)
            html = r.text
            matches = url_pattern.findall(html)

            for m in matches:
                urls.add(m.replace(" ", "").replace("\n", ""))

            if urls:
                break

        except:
            continue

    return sub, sorted(urls)

# ---------------------------------------------------------
# Multithreaded Scanning
# ---------------------------------------------------------
print("[*] Multithreaded scanning started...\n")

full_results = {}
futures = []

with ThreadPoolExecutor(max_workers=20) as executor:
    for sub in subdomains:
        futures.append(executor.submit(fetch_subdomain, sub))

    for f in tqdm(as_completed(futures), total=len(futures),
                  desc="Progress", unit="subdomain"):
        sub, urls = f.result()
        full_results[sub] = urls

# ---------------------------------------------------------
# CREATE ONLY project_name.txt
# ---------------------------------------------------------
output_file = f"{project_name}.txt"

with open(output_file, "w") as f:
    f.write(f"Project Report: {project_name}\n")
    f.write("=====================================\n\n")

    for sub in sorted(full_results.keys()):
        f.write(f"{sub}\n")
        f.write("-------------------------------------\n")

        urls = full_results[sub]

        if not urls:
            f.write("    (No URLs found)\n\n")
            continue

        for url in urls:
            f.write(f"    {url}\n")

        f.write("\n")

print("\n[+] Scan completed.")
print(f"[+] Output saved to: {output_file}")
