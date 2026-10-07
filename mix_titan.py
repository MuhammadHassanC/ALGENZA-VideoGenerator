"""
ALGENZA Video Engine - TITAN Soundtrack & SFX Mixer
Heavy cyberpunk dark-quant electronic score, aggressive robotic sound design,
braams, laser sweeps, speech ducking, and mouth_titan.npy lip-sync envelope.
Outputs: mix_titan.wav and mouth_titan.npy
"""

import os
import sys
import numpy as np
import soundfile as sf
from tl_titan import *

SR = 48000
N = int((END + 0.8) * SR)
tt = np.arange(N) / SR
V = np.zeros(N)

# 1. Load and align voice lines
for i, s0 in enumerate(ST):
    wav_path = f"titan_v{i}.wav"
    if not os.path.exists(wav_path):
        continue
    s, r = sf.read(wav_path)
    if s.ndim > 1:
        s = s.mean(axis=1)
    if r != SR:
        n2 = int(len(s) * SR / r)
        s = np.interp(np.arange(n2) * r / SR, np.arange(len(s)), s)
    a = int(s0 * SR)
    if a < N:
        avail = min(len(s), N - a)
        V[a:a + avail] += s[:avail]

max_v = np.abs(V).max()
if max_v > 1e-9:
    V = (V / max_v) * 0.94

def midi_to_freq(m):
    return 440.0 * 2.0 ** ((m - 69.0) / 12.0)

def add_signal(target, sig, t0, gain=1.0):
    i = int(t0 * SR)
    if 0 <= i < N:
        j = min(N, i + len(sig))
        target[i:j] += gain * sig[:j - i]

# 2. Synthesize Aggressive Cyberpunk Quant Soundtrack
M = np.zeros(N)
bpm = 112.0
bt = 60.0 / bpm
bar = 4.0 * bt

# Dark minor power chord progression (D minor -> Bb maj -> G minor -> A dim/C)
CHORDS = [
    [50, 53, 57, 62],  # Dm9
    [46, 50, 53, 58],  # Bb maj7
    [43, 47, 50, 55],  # Gm7
    [45, 48, 52, 57]   # Am7
]

total_bars = int(END / bar) + 2

for b in range(total_bars):
    a = int(b * bar * SR)
    e = min(N, int((b + 1) * bar * SR))
    if a >= N:
        break
    
    u = tt[a:e] - b * bar
    env = np.clip(u / 0.25, 0, 1) * np.clip((bar - u) / 0.25, 0, 1)
    ch = CHORDS[b % len(CHORDS)]
    
    # 1. Dark aggressive saw pad
    for m in ch:
        f = midi_to_freq(m)
        for detune in (0.993, 1.000, 1.007):
            pad = np.sin(2 * np.pi * f * detune * tt[a:e])
            pad += 0.4 * np.sin(4 * np.pi * f * detune * tt[a:e])
            pad += 0.2 * np.sin(6 * np.pi * f * detune * tt[a:e])
            M[a:e] += 0.025 * env * pad
            
    # 2. Menacing Sub Bass with Distortion
    bass_freq = midi_to_freq(ch[0] - 24)
    bass = np.sin(2 * np.pi * bass_freq * tt[a:e])
    bass += 0.5 * np.sin(2 * np.pi * bass_freq * 2 * tt[a:e])
    bass = np.tanh(bass * 1.5)  # Analog saturation drive
    M[a:e] += 0.11 * env * bass
    
    # 3. Driving 16th Note Cyber Quant Arpeggiator
    for k in range(16):
        pl_len = int(0.22 * SR)
        u_pl = np.arange(pl_len) / SR
        note = ch[k % len(ch)] + 12 + (12 if k % 4 == 0 else 0)
        pluck = np.sin(2 * np.pi * midi_to_freq(note) * u_pl) * np.exp(-u_pl * 16.0)
        pluck += 0.3 * np.sin(4 * np.pi * midi_to_freq(note) * u_pl) * np.exp(-u_pl * 24.0)
        add_signal(M, pluck, b * bar + k * (bt / 4.0), gain=0.038)
        
    # 4. Cinematic Industrial Kick & Percussion Pulse
    for k in range(4):
        k_t = b * bar + k * bt
        # Heavy transient kick
        k_len = int(0.35 * SR)
        u_k = np.arange(k_len) / SR
        k_f = 130 * np.exp(-u_k * 30.0) + 38
        kick = np.sin(2 * np.pi * k_f * u_k) * np.exp(-u_k * 9.0)
        kick = np.tanh(kick * 1.8)
        add_signal(M, kick, k_t, gain=0.14)
        
        # Snare / cyber clap on beats 2 and 4
        if k in (1, 3):
            s_len = int(0.28 * SR)
            u_s = np.arange(s_len) / SR
            noise = np.random.normal(0, 1, s_len) * np.exp(-u_s * 18.0)
            snare_tone = np.sin(2 * np.pi * 210 * u_s) * np.exp(-u_s * 25.0)
            snare = 0.7 * noise + 0.3 * snare_tone
            add_signal(M, snare, k_t, gain=0.09)

# 3. Procedural "Khatarnak" Sound Effects Engine
for t0, typ, p in events():
    if typ == "whoosh":
        dur = 0.55
        n_w = int(dur * SR)
        u = np.arange(n_w) / SR
        wn = np.random.normal(0, 1, n_w)
        fc = 300 + 4200 * (u / dur) ** 2
        sig = np.sin(2 * np.pi * fc * u) * wn * np.sin(np.pi * u / dur) ** 2
        add_signal(M, sig, t0 - 0.25, gain=0.15)
        
    elif typ == "braam":
        # Massive Hans Zimmer style institutional reese braam
        dur = 1.6
        n_b = int(dur * SR)
        u = np.arange(n_b) / SR
        f0 = p if p > 0 else 50
        braam = np.sin(2 * np.pi * f0 * u) + 0.6 * np.sin(4 * np.pi * f0 * u) + 0.3 * np.sin(6 * np.pi * f0 * u)
        braam += 0.4 * np.random.normal(0, 1, n_b) * np.exp(-u * 6.0)
        braam = np.tanh(braam * 3.0) * np.exp(-u * 2.2)
        add_signal(M, braam, t0, gain=0.22)
        
    elif typ == "heavy_boom":
        dur = 2.4
        n_b = int(dur * SR)
        u = np.arange(n_b) / SR
        f_boom = 90 * np.exp(-u * 6.0) + 32
        sub_boom = np.sin(2 * np.pi * f_boom * u) * np.exp(-u * 1.8)
        sub_boom += 0.3 * np.random.normal(0, 1, n_b) * np.exp(-u * 12.0)
        sub_boom = np.tanh(sub_boom * 2.5)
        add_signal(M, sub_boom, t0, gain=0.32)
        
    elif typ == "laser":
        dur = 0.22
        n_l = int(dur * SR)
        u = np.arange(n_l) / SR
        f_laser = p * np.exp(-u * 18.0)
        sig = np.sin(2 * np.pi * f_laser * u) * np.exp(-u * 12.0)
        add_signal(M, sig, t0, gain=0.10)
        
    elif typ == "lock":
        # Mechanical weapon/target lock click
        dur = 0.12
        n_c = int(dur * SR)
        u = np.arange(n_c) / SR
        click = np.sin(2 * np.pi * p * u) * np.exp(-u * 50.0)
        click += 0.5 * np.random.normal(0, 1, n_c) * np.exp(-u * 80.0)
        add_signal(M, click, t0, gain=0.12)
        
    elif typ == "alarm":
        # Emergency risk alarm ding
        dur = 0.45
        n_a = int(dur * SR)
        u = np.arange(n_a) / SR
        sig = (np.sin(2 * np.pi * p * u) + 0.5 * np.sin(2 * np.pi * (p * 1.414) * u)) * np.exp(-u * 7.0)
        add_signal(M, sig, t0, gain=0.16)
        
    elif typ == "shield":
        # Futuristic forcefield energize
        dur = 0.8
        n_s = int(dur * SR)
        u = np.arange(n_s) / SR
        f_sweep = 200 + 1200 * (u / dur)
        shield = np.sin(2 * np.pi * f_sweep * u) * (1 - u / dur) * (0.8 + 0.2 * np.sin(2 * np.pi * 35 * u))
        add_signal(M, shield, t0, gain=0.15)
        
    elif typ == "charge":
        dur = 0.9
        n_c = int(dur * SR)
        u = np.arange(n_c) / SR
        f_ch = 300 + 1800 * (u / dur) ** 2
        charge = np.sin(2 * np.pi * f_ch * u) * (u / dur) * np.exp(-((u - dur)**2) / 0.1)
        add_signal(M, charge, t0, gain=0.12)
        
    elif typ == "tick":
        dur = 0.04
        n_k = int(dur * SR)
        u = np.arange(n_k) / SR
        tick = np.sin(2 * np.pi * p * u) * np.exp(-u * 140.0)
        add_signal(M, tick, t0, gain=0.08)

# 4. Speech Sidechain Ducking
w_env = np.abs(V)
# 80ms smoothing window
ws = int(0.08 * SR)
if ws > 1:
    kernel = np.ones(ws) / ws
    w_env = np.convolve(w_env, kernel, mode="same")
duck = np.clip(1.0 - 0.55 * np.clip(w_env / 0.18, 0, 1), 0.35, 1.0)
M_ducked = M * duck

# Master Mix: Voice + Music/SFX
MIX = V + M_ducked

# 5. Master Peak & Loudness Polish
peak = np.abs(MIX).max()
if peak > 0.95:
    MIX = (MIX / peak) * 0.95

# Stereo mastering with wide spatial presence
left = MIX + 0.15 * np.roll(M_ducked, 140)
right = MIX - 0.15 * np.roll(M_ducked, 140)
stereo = np.column_stack([left, right])
stereo = np.clip(stereo, -0.98, 0.98)

out_wav = "mix_titan.wav"
sf.write(out_wav, stereo, SR, subtype="PCM_16")
print(f"SUCCESS! Rendered master soundtrack: {out_wav} ({len(stereo)/SR:.2f}s, 48kHz Stereo)")

# 6. Extract Speech Envelope for Character Mouth Lip-Sync
FPS = 60
n_frames = int(END * FPS) + 120
mouth = np.zeros(n_frames, dtype=np.float32)

chunk_len = int(SR / FPS)
for fi in range(n_frames):
    t_start = int(fi * SR / FPS)
    t_end = min(N, t_start + chunk_len)
    if t_start < N:
        chunk = np.abs(V[t_start:t_end])
        val = float(chunk.max()) if len(chunk) > 0 else 0.0
        mouth[fi] = np.clip(val * 1.8, 0.0, 1.0)

# Smooth mouth movement
sm_mouth = np.convolve(mouth, np.ones(5) / 5.0, mode="same")
np.save("mouth_titan.npy", sm_mouth)
print(f"SUCCESS! Generated mouth lip-sync envelope: mouth_titan.npy ({len(sm_mouth)} frames)")
