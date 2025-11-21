import requests
import sys

if len(sys.argv) != 2:
	print ("Invalid Format")
	print ("Supported format: python3 filename.py domain_list.txt")
	sys.exit()

filename = sys.argv[1]

# Open the file in read mode
with open(filename, "r") as f:
    domains = f.readlines()  # Reads all lines into a list

# Remove newline characters (\n) from each line
domains = [line.strip() for line in domains]

for domain in domains:
	for protocol in ["http://", "https://"]:
		response = requests.get(f"{protocol}{domain}")
		status = response.status_code
		try:
			print (f"{protocol}{domain} is reachable. Status code {status}")
		except requests.exceptions.RequestException:
			pass




