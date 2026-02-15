import os
import numpy as np
import sounddevice as sd
import threading
import time
import tkinter as tk
from tkinter import ttk
from flask import Flask, render_template_string, jsonify
from datetime import datetime
from colorama import Fore, init

# Initialize Colorama for Terminal Clarity
init(autoreset=True)
app = Flask(__name__)

# --- GLOBAL DYNAMIC STATE ---
class SystemState:
    def __init__(self):
        self.running = True
        self.paused = False
        self.volume = 0.5
        self.emit_duration = 3.0
        self.rest_duration = 12.0
        self.current_hex = "0000"
        self.is_emitting = False

# Global Instance
state = SystemState()

# --- FREQUENCY ENGINE (AUDIO PHYSICS) ---
class FrequencyEngine:
    def __init__(self):
        self.sample_rate = 48000
        self.phase = 0

    def generate_wave(self, duration, volume):
        """Generates the 'Chord of Love & Survival'."""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Layer 1: 528Hz (Transformation/Love)
        # Layer 2: 432Hz (Nature/Survival)
        # Layer 3: 10Hz Binaural Pulse (Alpha State Clarity)
        
        left_channel = (0.5 * np.sin(2 * np.pi * 528 * t) + 
                        0.3 * np.sin(2 * np.pi * 432 * t))
                        
        right_channel = (0.5 * np.sin(2 * np.pi * (528 + 10) * t) + 
                         0.3 * np.sin(2 * np.pi * 432 * t))
        
        # Stack and Normalize
        stereo_wave = np.stack((left_channel, right_channel), axis=-1)
        stereo_wave = stereo_wave / np.max(np.abs(stereo_wave)) # Normalize to avoid clipping
        
        return stereo_wave.astype(np.float32) * volume

    def run_loop(self):
        print(f"{Fore.CYAN}COGNITIVE ENGINE ONLINE. WAITING FOR COMMANDS...")
        while state.running:
            if not state.paused:
                state.is_emitting = True
                state.current_hex = hex(np.random.randint(40000, 65535)).upper()[2:]
                
                print(f"{Fore.GREEN}[EMITTING] {Fore.WHITE}Love Frequency: 3s | HEX: {state.current_hex}")
                
                # Execution of the Pulse
                audio = self.generate_wave(state.emit_duration, state.volume)
                sd.play(audio, self.sample_rate)
                time.sleep(state.emit_duration)
                sd.stop()
                
                state.is_emitting = False
                print(f"{Fore.MAGENTA}[INTEGRATING] {Fore.WHITE}Survival Rest: {state.rest_duration}s...")
                time.sleep(state.rest_duration)
            else:
                time.sleep(0.5)

# --- TKINTER GUI CONTROL PANEL (FIXED & ENHANCED) ---
def launch_gui():
    root = tk.Tk()
    root.title("GOD-CODE: SURVIVAL & LOVE CONTROL")
    root.geometry("500x550")
    
    # Dynamic Clarity Color Scheme
    BG_COLOR = "#050505"      # Deep Void Black
    ACCENT_1 = "#00FFFF"      # Electric Cyan (Intellect)
    ACCENT_2 = "#FF00FF"      # Neon Magenta (Love/Heart)
    TEXT_COLOR = "#FFFFFF"    # Pure White Clarity
    
    root.configure(bg=BG_COLOR)

    # --- Header ---
    tk.Label(root, text="FREQUENCY EMITTER", bg=BG_COLOR, fg=ACCENT_1, 
             font=("Courier", 20, "bold")).pack(pady=(30, 10))
    
    tk.Label(root, text="STATUS: SYSTEM ONLINE", bg=BG_COLOR, fg=ACCENT_2, 
             font=("Courier", 10)).pack(pady=5)

    # --- Volume Control ---
    tk.Label(root, text="AMPLITUDE (VOLUME)", bg=BG_COLOR, fg=TEXT_COLOR, font=("Courier", 12)).pack(pady=(20, 5))
    
    def update_volume(v):
        state.volume = float(v) / 100
        vol_label.config(text=f"{v}%")

    vol_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", 
                          bg=BG_COLOR, fg=ACCENT_1, highlightthickness=0,
                          troughcolor="#333333", command=update_volume)
    vol_slider.set(50)
    # FIX: Changed 'px' to 'padx'
    vol_slider.pack(fill="x", padx=40)
    
    vol_label = tk.Label(root, text="50%", bg=BG_COLOR, fg=ACCENT_1)
    vol_label.pack()

    # --- Duration Controls ---
    tk.Label(root, text="PULSE DURATION (SECONDS)", bg=BG_COLOR, fg=TEXT_COLOR, font=("Courier", 12)).pack(pady=(20, 5))
    
    emit_val = tk.DoubleVar(value=3.0)
    entry_box = tk.Entry(root, textvariable=emit_val, bg="#222", fg=TEXT_COLOR, insertbackground=TEXT_COLOR, justify="center")
    entry_box.pack(pady=5)
    
    def apply_settings():
        try:
            state.emit_duration = float(emit_val.get())
            status_lbl.config(text=f"UPDATED: {state.emit_duration}s PULSE", fg=ACCENT_1)
        except ValueError:
            status_lbl.config(text="ERROR: INVALID NUMBER", fg="red")

    tk.Button(root, text="APPLY TIME CALCULATION", command=apply_settings, 
              bg="#222", fg=TEXT_COLOR, relief="flat", padx=10, pady=5).pack(pady=5)

    status_lbl = tk.Label(root, text="", bg=BG_COLOR, fg=ACCENT_1, font=("Courier", 10))
    status_lbl.pack()

    # --- Pause/Resume Button ---
    def toggle_pause():
        state.paused = not state.paused
        if state.paused:
            pause_btn.config(text="RESUME EMISSION", bg=ACCENT_2, fg=BG_COLOR)
            status_lbl.config(text="SYSTEM PAUSED: SILENCE", fg="yellow")
        else:
            pause_btn.config(text="PAUSE SYSTEM", bg="#222", fg=TEXT_COLOR)
            status_lbl.config(text="SYSTEM RESUMED", fg=ACCENT_1)

    pause_btn = tk.Button(root, text="PAUSE SYSTEM", command=toggle_pause, 
                          bg="#222", fg=TEXT_COLOR, font=("Courier", 12, "bold"), 
                          width=20, pady=10, relief="raised")
    pause_btn.pack(pady=40)

    # Start the Loop
    root.mainloop()

# --- FLASK WEB VISUALIZER ---
@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CLARITY VISUALIZER</title>
        <style>
            body { background-color: #050505; color: #fff; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; font-family: monospace; overflow: hidden; }
            .circle { width: 200px; height: 200px; border: 2px solid #00FFFF; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: all 0.5s ease-in-out; box-shadow: 0 0 20px #00FFFF; }
            .pulse { transform: scale(1.5); border-color: #FF00FF; box-shadow: 0 0 50px #FF00FF; background: rgba(255, 0, 255, 0.1); }
            #hex { font-size: 2em; margin-top: 20px; color: #00FFFF; }
            #status { margin-top: 10px; color: #888; }
        </style>
    </head>
    <body>
        <div id="visualizer" class="circle">
            <div style="width:10px; height:10px; background:#fff; border-radius:50%;"></div>
        </div>
        <div id="hex">WAITING...</div>
        <div id="status">INITIALIZING STREAM</div>
        <script>
            setInterval(() => {
                fetch('/api/data').then(r => r.json()).then(d => {
                    const viz = document.getElementById('visualizer');
                    document.getElementById('hex').innerText = "HEX: " + d.hex;
                    
                    if(d.active) {
                        viz.classList.add('pulse');
                        document.getElementById('status').innerText = "EMITTING LOVE FREQUENCY";
                        document.getElementById('status').style.color = "#FF00FF";
                    } else {
                        viz.classList.remove('pulse');
                        document.getElementById('status').innerText = "SURVIVAL INTEGRATION";
                        document.getElementById('status').style.color = "#00FFFF";
                    }
                });
            }, 500);
        </script>
    </body>
    </html>
    """)

@app.route('/api/data')
def get_data():
    return jsonify({"hex": state.current_hex, "active": state.is_emitting})

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Start Audio Engine Thread
    eng = FrequencyEngine()
    audio_thread = threading.Thread(target=eng.run_loop, daemon=True)
    audio_thread.start()
    
    # 2. Start Flask Web Server Thread
    flask_thread = threading.Thread(target=lambda: app.run(port=5000, debug=False, use_reloader=False), daemon=True)
    flask_thread.start()
    
    # 3. Launch the GUI (Must be on Main Thread)
    launch_gui()
