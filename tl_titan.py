"""
ALGENZA Video Engine - TITAN EDITION (High-Intensity TikTok 9:16)
Hard-hitting institutional script tailored directly to algenza.com
"""

import json
import os

# 9 Aggressive, high-conversion narration lines for TikTok / Reels
LINES = [
    "Ninety-five percent of manual traders lose everything to emotional hesitation and predatory algorithms.",
    "Slippage, missed Gold spikes, and brutal prop firm drawdown rules wipe out accounts in seconds.",
    "Enter ALGENZA. Institutional algorithmic warfare engineered for pure execution dominance.",
    "Custom MT5 Expert Advisors, asynchronous Python bridges, and sub-millisecond FIX Protocol integrations.",
    "Our five-stage architecture: raw tick filtering, deterministic signals, and direct broker routing.",
    "A hard risk engine with strict daily loss ceilings protecting your capital before human panic begins.",
    "Zero black boxes. Zero repainting. Clean, modular MQL5 and Python source code you own forever.",
    "Over two hundred custom algorithmic systems engineered by lead architect Muhammad Hassan.",
    "Stop trading like an amateur. Deploy your algorithmic edge today at algenza.com."
]

NS = len(LINES)

# Calibrated speech defaults
DEFAULT_DURATIONS = [5.2, 5.4, 5.0, 5.6, 5.2, 5.5, 5.1, 4.9, 4.4]

TTS_FILE = "tts_titan.json"
if os.path.exists(TTS_FILE):
    try:
        with open(TTS_FILE, "r") as f:
            T = json.load(f)
            D = T.get("d", DEFAULT_DURATIONS)
            if len(D) != NS:
                D = DEFAULT_DURATIONS
    except Exception:
        D = DEFAULT_DURATIONS
else:
    D = DEFAULT_DURATIONS

GAP = 0.45
ST = []
_t = 1.2  # Quick start for high-retention TikTok

for x in D:
    ST.append(_t)
    _t += x + GAP

END = _t + 2.0
SS = [0.0] + [s - 0.28 for s in ST[1:]]
SE = SS[1:] + [END]

CHAR_T = 1.0
BTN_T = SS[-1] + 0.65

def cand_t(k):
    return 0.4 + k * 0.08

def card_t(k):
    return SS[3] + 0.25 + k * 0.40

def node_t(k):
    return SS[4] + 0.25 + k * (SE[4] - SS[4] - 0.4) / 5.0

def alert_t(k):
    return SS[5] + 0.9 + k * 0.95

def check_t(k):
    return SS[6] + 0.8 + k * 0.50

def events():
    """Returns high-intensity sound events (timestamp, type, param)"""
    E = []
    # Scene transitions: aggressive cyber whoosh & heavy impact
    for i in range(1, NS):
        E.append((SS[i], "whoosh", 0))
        E.append((SS[i] + 0.05, "braam", 55))
    
    # Scene 0: Warning tick surge & glitch
    for k in range(16):
        E.append((cand_t(k), "tick", 2800 + k * 45))
    E.append((0.8, "lock", 1200))
    
    # Scene 1: Alarm ding & heavy stress sub drop
    E.append((SS[1] + 1.0, "alarm", 880))
    E.append((SS[1] + 2.4, "boom", 45))
    
    # Scene 2: ALGENZA Brand Impact - Massive cinematic sub boom
    E.append((SS[2] + 0.15, "heavy_boom", 38))
    E.append((SS[2] + 0.80, "charge", 1400))
    
    # Scene 3: Weapon Cards lock-in clicks
    for k in range(3):
        E.append((card_t(k), "lock", 750 + k * 120))
    
    # Scene 4: 5-Stage Laser Pipeline nodes
    for k in range(5):
        E.append((node_t(k), "laser", 900 + k * 150))
    
    # Scene 5: Risk Engine shield activation & alert
    E.append((alert_t(0), "shield", 600))
    E.append((alert_t(1), "ding", 1050))
    
    # Scene 6: Code tree laser checks
    for k in range(3):
        E.append((check_t(k), "lock", 800 + k * 100))
    
    # Scene 7: Golden counter power surge
    E.append((SS[7] + 0.4, "charge", 1200))
    E.append((SS[7] + 1.6, "ding", 1320))
    
    # Scene 8: Final CTA strike
    E.append((BTN_T, "heavy_boom", 40))
    E.append((BTN_T + 0.3, "whoosh", 0))
    
    return E
