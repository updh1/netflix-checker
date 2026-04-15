# Netflix Account Checker

A multithreaded Netflix account checker that validates credentials and retrieves subscription details using proxies.

## Features

- Multi-threaded (100 threads by default)
- Proxy support (HTTP/HTTPS, with/without auth)
- Rate limiting (max 30 concurrent connections)
- Automatic retry on bans/timeouts
- Detects:
  - Active subscriptions (with plan details)
  - Free trials
  - Expired accounts
  - Invalid credentials
  - IP/Proxy bans

## Requirements

```bash
pip install requests user_agent colorama
Usage
bash
python Netflix.py
You will be prompted for:
```
```bash
Combo file – path to file with email:password pairs (one per line)

Proxies file – path to file with proxies (one per line)
```

Supported proxy formats
```bash
ip:port
user:pass@ip:port
http://user:pass@ip:port
```
Output Files
```bash
Netflix-Hits.txt	Working accounts with plan details (plan, quality, screens, payment method, country)
nf-free.txt	Free trial accounts
```
# Capture 
```bash
john@gmail.com:password123 | Plan = Premium | Stream Quality = 4K+HDR | Screens = 4 | Payment = Credit Card | Country = US
```

Disclaimer
This tool is for educational purposes only.

Use only on accounts you own or have permission to test

The author is not responsible for any misuse

Netflix may block IPs that send excessive requests

License
Educational use only.

# Author
@updh1
