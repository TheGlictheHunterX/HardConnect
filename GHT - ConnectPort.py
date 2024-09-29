import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import subprocess
import os

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    sock.close()
    return port if result == 0 else None

def check_open_ports(host, start_port, end_port):
    open_ports = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}
        for future in futures:
            port = future.result()
            if port:
                open_ports.append(port)
                print(f"Port {port} is open")
    return open_ports

def attempt_session_on_ports(host, open_ports):
    for port in open_ports:
        command = ""
        if port == 22:
            command = f"ssh user@{host} -p {port}"  # Replace 'user' with the actual username
        elif port == 23:
            command = f"telnet {host} {port}"
        elif port == 80:
            command = f"curl http://{host}:{port}"  # Simple HTTP request
        elif port == 443:
            command = f"curl https://{host}:{port}"  # Simple HTTPS request

        if command:
            print(f"Attempting to open session on port {port}...")
            subprocess.call(command, shell=True)

def main():
    host = input("Enter the host (e.g., example.com or 192.168.1.1): ").strip()
    start_port = 1
    end_port = 1024
    print("Checking for open ports...")
    open_ports = check_open_ports(host, start_port, end_port)
    if open_ports:
        print("Attempting to open sessions on open ports...")
        attempt_session_on_ports(host, open_ports)
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()
