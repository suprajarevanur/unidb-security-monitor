# UniDB Security Monitor

A SOC cybersecurity lab simulating real-world attack detection, intrusion monitoring, and secure database access built on a multi-VM network.

## Lab Architecture

- Kali Linux VM (192.168.64.2) - Attack simulation
- Ubuntu Server VM (192.168.64.3) - Target/defender

## Services on Ubuntu Server

| Service | Port | Description |
|---|---|---|
| MySQL | 3306 | Student university database |
| Flask Portal | 8080 | Student login web interface |
| Snort IDS | - | Network intrusion detection |
| Security Dashboard | 8888 | Real-time threat visualization |

## Project Files

| File | Description |
|---|---|
| flask_portal.py | Flask web app - student portal on port 8080 |
| dashboard.py | Security dashboard server on port 8888 |
| parser.py | Snort alert log parser |
| index.html | Dashboard frontend UI |
| dashboard.png | Live dashboard screenshot |

## Technologies Used

Python, Flask, MySQL, Snort 2.9, Kali Linux, Ubuntu Server 22.04, UTM (Apple Silicon)

## Author

Supraja Revanur - github.com/suprajarevanur

## Disclaimer

For educational purposes only. All attacks performed in an isolated virtual network.
