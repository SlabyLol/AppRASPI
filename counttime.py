import tkinter as tk
from datetime import datetime, timedelta

# ---------------------------
# Hilfsfunktionen
# ---------------------------
def parse_clock_time(timestr):
    parts = timestr.strip().split(":")
    if len(parts) == 2:
        h, m = parts
        s = "0"
    elif len(parts) == 3:
        h, m, s = parts
    else:
        raise ValueError("Format HH:MM oder HH:MM:SS")
    h, m, s = int(h), int(m), int(s)
    if not (0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60):
        raise ValueError("Ungültige Uhrzeit")
    return h, m, s

def seconds_until_target(h, m, s):
    now = datetime.now()
    target = now.replace(hour=h, minute=m, second=s, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return int((target - now).total_seconds())

def format_hms(seconds):
    if seconds < 0: seconds = 0
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

# ---------------------------
# Hauptfenster
# ---------------------------
root = tk.Tk()
root.title("Countdown")
root.configure(bg="black")
root.geometry("520x330")

# Anzeige groß
label = tk.Label(root, text="--:--:--", font=("Digital-7", 95, "bold"), bg="black", fg="lime")
label.pack(pady=(15, 5))

# Eingabe
tk.Label(root, text="Uhrzeit eingeben (HH:MM oder HH:MM:SS):",
         font=("Arial", 12), bg="black", fg="white").pack()
entry = tk.Entry(root, font=("Arial", 20), justify="center")
entry.pack(pady=5)
entry.insert(0, "00:00:00")

status = tk.Label(root, text="", font=("Arial", 10), bg="black", fg="red")
status.pack()

# Buttons
frame = tk.Frame(root, bg="black")
frame.pack(pady=10)
start_button = tk.Button(frame, text="Start", font=("Arial", 16), width=10)
stop_button = tk.Button(frame, text="Stop", font=("Arial", 16), width=10, state="disabled")
start_button.grid(row=0, column=0, padx=8)
stop_button.grid(row=0, column=1, padx=8)

after_id = None
running = False

# ---------------------------
# MINI-DISPLAY UNTEN RECHTS
# ---------------------------
mini = tk.Toplevel()
mini.title("Mini")
mini.geometry("200x80+1500+900")  # Position rechts unten (bei Full-HD Monitor)
mini.overrideredirect(True)       # Keine Fensterrahmen
mini.configure(bg="black")

mini_label = tk.Label(mini, text="--:--:--", font=("Digital-7", 40, "bold"),
                      bg="black", fg="lime")
mini_label.pack()

# Always on top
mini.attributes("-topmost", True)

# ---------------------------
# Blinken
# ---------------------------
def blink_zero():
    current = label.cget("fg")
    new = "black" if current == "red" else "red"
    label.config(fg=new)
    mini_label.config(fg=new)
    root.after(500, blink_zero)

# ---------------------------
# Countdown Tick
# ---------------------------
def countdown_tick(remaining):
    global after_id, running

    if remaining >= 0 and running:

        formatted = format_hms(remaining)

        # Anzeige aktualisieren
        label.config(text=formatted)
        mini_label.config(text=formatted)

        if remaining == 0:
            label.config(fg="red")
            mini_label.config(fg="red")
            blink_zero()
            running = False
            start_button.config(state="normal")
            stop_button.config(state="disabled")
            return
        else:
            label.config(fg="lime")
            mini_label.config(fg="lime")

        after_id = root.after(1000, countdown_tick, remaining - 1)
    else:
        running = False
        start_button.config(state="normal")
        stop_button.config(state="disabled")

# ---------------------------
# Start
# ---------------------------
def start_countdown():
    global running, after_id
    if running:
        return

    try:
        h, m, s = parse_clock_time(entry.get())
        secs = seconds_until_target(h, m, s)
    except Exception as e:
        status.config(text=f"Fehler: {e}")
        return

    status.config(text="")
    running = True
    start_button.config(state="disabled")
    stop_button.config(state="disabled")

    formatted = format_hms(secs)
    label.config(text=formatted, fg="lime")
    mini_label.config(text=formatted, fg="lime")

    after_id = root.after(1000, countdown_tick, secs - 1)

start_button.config(command=start_countdown)

# ---------------------------
# Stop
# ---------------------------
def stop_countdown():
    global running, after_id
    if after_id is not None:
        root.after_cancel(after_id)
    running = False
    label.config(text="--:--:--", fg="lime")
    mini_label.config(text="--:--:--", fg="lime")
    start_button.config(state="normal")
    stop_button.config(state="disabled")
    status.config(text="Countdown gestoppt")

stop_button.config(command=stop_countdown)

entry.bind("<Return>", lambda e: start_countdown())

root.mainloop()
