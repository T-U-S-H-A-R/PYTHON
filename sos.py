from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket
import subprocess
from urllib.parse import parse_qs
# ---------- CONFIGURATION ----------
PIN = "8081"  # Aapka Security PIN
PORT = 8000   # Aapka Port (Auto-select function use kar sakte hain)
IMAGE_PATH = "a.jpg"
# ---------- SCRIPT MAPPING ----------
scripts = 
{
    "/shutdown": "shutdown.py",
    "/camera": "camera.py",
    "/pandas": "pandas.py",
    "/youtube": "youtube.py",
    # ... baki saare scripts yahan daal dein
}

class SecureHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # URL se parameters nikalne ke liye (e.g. ?pin=8081)
        query_params = parse_qs(self.path.split('?')[-1]) if '?' in self.path else {}
        user_pin = query_params.get('pin', [None])[0]

        # 1. Serve Image (Bina PIN ke background load ho sake)
        if self.path == "/a.jpg":
            if os.path.exists(IMAGE_PATH):
                self.send_response(200)
                self.send_header("Content-type", "image/jpeg")
                self.end_headers()
                with open(IMAGE_PATH, "rb") as f:
                    self.wfile.write(f.read())
            return

        # 2. Check Security PIN
        if user_pin != PIN:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"""
            <html>
            <body style="background-color:#1a1a1a; color:white; text-align:center; font-family:Arial; padding-top:100px;">
                <h1>ACCESS DENIED</h1>
                <p>Please enter Security PIN to access JARVIS:</p>
                <form method="GET">
                    <input type="password" name="pin" style="padding:10px; border-radius:5px; border:none;">
                    <button type="submit" style="padding:10px; background:cyan; border:none; border-radius:5px;">LOGIN</button>
                </form>
            </body>
            </html>
            """)
            return

        # 3. Run Scripts (Agar PIN sahi hai)
        clean_path = self.path.split('?')[0]
        if clean_path in scripts:
            subprocess.Popen(["python", scripts[clean_path]])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Executed {scripts[clean_path]} successfully!".encode())
            return

        # 4. Serve Secure UI
        self.send_response(200)
        self.end_headers()
        ui_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>JARVIS Secure Panel</title>
            <style>
                body {{ background-image: url('/a.jpg'); background-size: cover; color: white; text-align: center; }}
                .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding: 20px; }}
                button {{ padding: 15px; background: rgba(0,255,255,0.2); color: white; border: 1px solid cyan; border-radius: 8px; }}
            </style>
        </head>
        <body>
            <h1>JARVIS SECURE HUB</h1>
            <div class="grid">
                <button onclick="go('/shutdown')">Shutdown</button>
                <button onclick="go('/camera')">Camera</button>
                <button onclick="go('/pandas')">Pandas</button>
                <button onclick="go('/youtube')">YouTube</button>
            </div>
            <script>
                function go(path){{
                    // PIN ko har request ke saath bhejte rehna zaroori hai
                    window.location.href = path + "?pin={PIN}";
                }}
            </script>
        </body>
        </html>
        """
        self.wfile.write(ui_html.encode())

# RUN SERVER
print(f"Secure Server started on Port {PORT}...")
HTTPServer(("0.0.0.0", PORT), SecureHandler).serve_forever()
