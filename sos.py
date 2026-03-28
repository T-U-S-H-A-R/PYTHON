from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import socket
import subprocess

# ---------- AUTO PORT SELECT FUNCTION ----------
def get_free_port(start_port=8000, limit=20):
    port = start_port
    for _ in range(limit):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("0.0.0.0", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError("No free ports found!")

PORT = get_free_port(8000)

# ---------- IMAGE PATH (ANDROID SUPPORT) ----------
IMAGE_PATH = "a.jpg"
if not os.path.exists(IMAGE_PATH):
    IMAGE_PATH = "/storage/emulated/0/Download/a.jpg"

# ---------- SCRIPT MAPPING ----------
scripts = {
    "/shutdown": "shutdown.py",
    "/restart": "restart.py",
    "/battery": "battery.py",
    "/camera": "camera.py",
    "/time": "time.py",
    "/calendar": "calendar.py",
    "/weather": "weather.py",

    "/sin": "sin.py",
    "/cos": "cos.py",
    "/tan": "tan.py",
    "/cot": "cot.py",
    "/sec": "sec.py",
    "/cosec": "cosec.py",

    "/upward_parabola": "upward_parabola.py",
    "/downward_parabola": "downward_parabola.py",
    "/right_shift_parabola": "right_shift_parabola.py",
    "/left_shift_parabola": "left_shift_parabola.py",

    "/control": "control.py",
    "/german": "german.py",
    "/friday": "friday.py",
    "/japan": "japan.py",
    "/russia": "russia.py",
    "/china": "china.py",
    "/italian": "italian.py",
    "/french": "french.py",
    "/jarfrinova": "jarvis_friday_nova.py",

    # ---------- NEW BUTTON SCRIPTS ----------
    "/youtube": "youtube.py",
    "/google": "google.py",
    "/w3school": "w3school.py",
    "/chrome": "chrome.py",
    "/pandas": "pandas.py"
}

# ---------- HANDLER ----------
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):

        # Run scripts
        if self.path in scripts:
            subprocess.Popen(["python", scripts[self.path]])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Running {scripts[self.path]}".encode())
            return

        # Serve image
        if self.path == "/a.jpg" and os.path.exists(IMAGE_PATH):
            self.send_response(200)
            self.send_header("Content-type", "image/jpeg")
            self.end_headers()
            with open(IMAGE_PATH, "rb") as f:
                self.wfile.write(f.read())
            return

        # ---------- UI ----------
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JARVIS Mobile Panel</title>
<style>
body {
    background-image: url('/a.jpg');
    background-size: cover;
    margin: 0;
    text-align: center;
    color: white;
    font-family: Arial;
}
h1 {
    font-size: 5vw;
    text-shadow: 2px 2px 5px black;
}
.grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
    padding: 10px;
}
button {
    padding: 10px;
    font-size: 3vw;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}
button:hover {
    transform: scale(1.05);
}
</style>
</head>
<body>

<h1>JARVIS CONTROL</h1>

<div class="grid">
<button onclick="go('/shutdown')">Shutdown</button>
<button onclick="go('/restart')">Restart</button>
<button onclick="go('/battery')">Battery</button>
<button onclick="go('/camera')">Camera</button>
<button onclick="go('/time')">Time</button>
<button onclick="go('/calendar')">Calendar</button>
<button onclick="go('/weather')">Weather</button>

<button onclick="go('/sin')">Sin</button>
<button onclick="go('/cos')">Cos</button>
<button onclick="go('/tan')">Tan</button>
<button onclick="go('/cot')">Cot</button>
<button onclick="go('/sec')">Sec</button>
<button onclick="go('/cosec')">Cosec</button>

<button onclick="go('/upward_parabola')">Up</button>
<button onclick="go('/downward_parabola')">Down</button>
<button onclick="go('/right_shift_parabola')">Right</button>
<button onclick="go('/left_shift_parabola')">Left</button>

<button onclick="go('/control')">All</button>
<button onclick="go('/german')">German</button>
<button onclick="go('/friday')">Friday</button>
<button onclick="go('/japan')">Japan</button>
<button onclick="go('/russia')">Russia</button>
<button onclick="go('/china')">China</button>
<button onclick="go('/italian')">Italian</button>
<button onclick="go('/french')">French</button>
<button onclick="go('/jarfrinova')">JFN</button>

<!-- ---------- NEW BUTTONS ---------- -->
<button onclick="go('/youtube')">YouTube</button>
<button onclick="go('/google')">Google</button>
<button onclick="go('/w3school')">W3School</button>
<button onclick="go('/chrome')">Chrome</button>
<button onclick="go('/pandas')">Pandas</button>

</div>

<script>
function go(path){
    window.location.href = path;
}
</script>

</body>
</html>
""")

# ---------- RUN SERVER ----------
ip = "127.0.0.1"
print(f"\nServer running on: http://{ip}:{PORT}\n")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
