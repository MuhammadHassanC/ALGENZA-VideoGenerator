"""
ALGENZA Video Engine - TITAN EDITION (9:16 Vertical TikTok Renderer)
Features the "Khatarnak" ALGENZA QUANT SENTINEL MECHA mascot,
high-intensity combat-grade quant visual design, laser targeting HUD,
and institutional narrative directly from algenza.com.
Powered by pure-Python Skia compatibility engine (zero crashes on Windows).
"""

import os
import sys
import math
import re
import subprocess
import io
import numpy as np

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception:
        pass

import skia
from tl_titan import *

# 1. Discover FFmpeg Executable
try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_EXE = "ffmpeg"

# 2. TikTok Vertical Resolution
W, H = 1080, 1920
FPS = 60

# 3. Fonts Setup (Robust System & Fallbacks)
FD = os.environ.get('FD', '/usr/share/fonts/truetype/')
HF = FD + 'higgsfield/Montserrat-ExtraBold.ttf'
if not os.path.exists(HF): HF = FD + 'dejavu/DejaVuSans-Bold.ttf'

TF = {
    'h': skia.Typeface.MakeFromFile(HF),
    'b': skia.Typeface.MakeFromFile(FD + 'dejavu/DejaVuSans.ttf'),
    'bb': skia.Typeface.MakeFromFile(FD + 'dejavu/DejaVuSans-Bold.ttf'),
    'm': skia.Typeface.MakeFromFile(FD + 'dejavu/DejaVuSansMono.ttf'),
    'mb': skia.Typeface.MakeFromFile(FD + 'dejavu/DejaVuSansMono-Bold.ttf'),
    'lg': skia.Typeface.MakeFromFile(FD + 'higgsfield/Inter-Bold.ttf')
}

FC = {}
def F(k, s):
    s = int(s)
    if (k, s) not in FC:
        FC[(k, s)] = skia.Font(TF[k], s)
    return FC[(k, s)]

# 4. Brand Color Palette (Aggressive Cyberpunk & Algenza Gold Palette)
GOLD = '#DFC15D'      # Official Algenza Gold (from algenza.com logo)
GOLD_DARK = '#C9A86A' # Secondary Algenza Champagne Gold
CYAN = '#00F0FF'      # High-Voltage Cyber Electric Cyan
RED = '#FF1E40'       # Menacing Warning / Laser Red
GREEN = '#00FF88'     # Execution Fill / Verified Green
WH = '#F8FAFC'        # Ultra-Crisp White
MU = '#8E9DAF'        # Tactical Slate Muted
PN = '#0B0F17'        # Obsidian Mecha Panel Black
LN = '#1C2638'        # Heavy Cyber Armor Border
DK = '#05070B'        # Deep Visor Cavity Black

def P(h, a=1.0, sw=0):
    h = h.lstrip('#')
    a = max(0.0, min(1.0, a))
    p = skia.Paint(AntiAlias=True, Color=skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(a * 255)))
    if sw:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(sw)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p

def GL(h, a, sw=0, sig=12):
    p = P(h, a, sw)
    p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, sig))
    return p

def dash(a):
    p = P(MU, a, 2)
    p.setPathEffect(skia.DashPathEffect.Make([12, 8], 0))
    return p

def cl(x): return 0.0 if x < 0 else 1.0 if x > 1 else x
def eo(x): x = cl(x); return 1 - (1 - x) ** 3
def sm(t, a, b): return eo((t - a) / (b - a))
def bo(x):
    x = cl(x)
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2

def tx(c, s, x, y, k, sz, col=WH, a=1.0, al='l'):
    f = F(k, sz)
    w = f.measureText(s)
    if al == 'c': x -= w / 2
    elif al == 'r': x -= w
    c.drawString(s, x, y, f, P(col, a))
    return w

def logo_algenza(c, x, y, sz=44, a=1.0, al='c', glow=0.5):
    # Renders official Algenza double-polygon insignia & wordmark
    f = F('lg', sz)
    w_text = f.measureText("ALGENZA")
    poly_sz = sz * 0.95
    spacing = 16
    total_w = poly_sz + spacing + w_text
    
    if al == 'c': x0 = x - total_w / 2
    elif al == 'r': x0 = x - total_w
    else: x0 = x
    
    # Official Dual Polygons from algenza.com
    py = y - sz * 0.78
    p1 = skia.Path()
    p1.moveTo(x0 + poly_sz * 0.31, py + poly_sz * 0.45)
    p1.lineTo(x0 + poly_sz * 0.43, py + poly_sz * 0.69)
    p1.lineTo(x0 + poly_sz * 0.26, py + poly_sz * 1.00)
    p1.lineTo(x0, py + poly_sz * 1.00)
    p1.close()
    
    p2 = skia.Path()
    p2.moveTo(x0 + poly_sz * 0.49, py)
    p2.lineTo(x0 + poly_sz * 1.00, py + poly_sz * 1.00)
    p2.lineTo(x0 + poly_sz * 0.72, py + poly_sz * 1.00)
    p2.lineTo(x0 + poly_sz * 0.36, py + poly_sz * 0.26)
    p2.close()
    
    if glow > 0:
        c.drawPath(p1, GL(GOLD_DARK, glow * a * 0.7, 0, 16))
        c.drawPath(p2, GL(GOLD, glow * a * 0.8, 0, 18))
        
    c.drawPath(p1, P(GOLD_DARK, a))
    c.drawPath(p2, P(GOLD, a))
    
    # Wordmark
    tx_x = x0 + poly_sz + spacing
    if glow > 0:
        c.drawString("ALGENZA", tx_x, y, f, GL(GOLD, glow * a * 0.4, 0, 14))
    c.drawString("ALGENZA", tx_x, y, f, P(WH, a))
    return total_w

def rr(c, l, t, r, b, rad, p):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(l, t, r, b), rad, rad), p)

def panel(c, l, t, r, b, a=1):
    rr(c, l, t, r, b, 20, P(PN, 0.94 * a))
    rr(c, l, t, r, b, 20, P(LN, a, 2))

CUR = [0.0, 0.0]
def head(c, s, x, y, a, sz=56):
    f = F('h', sz)
    sp = f.measureText(' ')
    for k, wd in enumerate(s.split()):
        g = sm(CUR[0], CUR[1] + 0.04 + k * 0.08, CUR[1] + 0.35 + k * 0.08)
        c.drawString(wd, x, y + (1 - g) * 24, f, P(WH, a * g))
        x += f.measureText(wd) + sp

def sub(c, s, x, y, a, sz=26):
    tx(c, s, x, y, 'b', sz, MU, a)

# 5. Background with Cyber Grid & Volatility Matrix
def mkbg():
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(skia.Color(8, 10, 15))
    
    # Tactical laser grid
    gp = P('#151B27', 0.85, 1)
    grid_sz = 54
    for x in range(0, W + 1, grid_sz): c.drawLine(x, 0, x, H, gp)
    for y in range(0, H + 1, grid_sz): c.drawLine(0, y, W, y, gp)
    
    # Ambient gold & cyan dual halos
    p1 = skia.Paint(AntiAlias=True)
    p1.setShader(skia.GradientShader.MakeRadial(skia.Point(W * 0.5, H * 0.35), H * 0.5, [skia.Color(223, 193, 93, 36), skia.Color(223, 193, 93, 0)]))
    c.drawRect(skia.Rect.MakeWH(W, H), p1)
    
    p2 = skia.Paint(AntiAlias=True)
    p2.setShader(skia.GradientShader.MakeRadial(skia.Point(W * 0.5, H * 0.8), H * 0.45, [skia.Color(0, 240, 255, 28), skia.Color(0, 240, 255, 0)]))
    c.drawRect(skia.Rect.MakeWH(W, H), p2)
    
    # Deep Vignette
    p3 = skia.Paint(AntiAlias=True)
    p3.setShader(skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), H * 0.65, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 180)]))
    c.drawRect(skia.Rect.MakeWH(W, H), p3)
    return s.makeImageSnapshot()

BG = mkbg()

# Load speech lip-sync envelope
try:
    MO = np.load('mouth_titan.npy')
except Exception:
    MO = np.zeros(10)

# Procedural High-Volatility Candlestick Data
rng = np.random.default_rng(99)
CAND = []
p_val = 2650.0  # Gold price scale
for k in range(16):
    o = p_val
    c_ = p_val + rng.normal(1.8, 3.2)
    h_ = max(o, c_) + abs(rng.normal(0, 2.0))
    l_ = min(o, c_) - abs(rng.normal(0, 2.0))
    CAND.append((o, h_, l_, c_))
    p_val = c_
PMIN = min(x[2] for x in CAND)
PMAX = max(x[1] for x in CAND)

def CY(v, base_y=1000, height_span=380):
    return base_y - (v - PMIN) / (PMAX - PMIN) * height_span

# Mascot Waypoints Across Scenes for TikTok 9:16 Vertical
# Positioned powerfully in the lower-middle half with scale
A = [
    (540, 1440, 1.15),   # S0: Below chart, scanning with laser
    (540, 1460, 1.10),   # S1: Alarm stance, crimson visor mode
    (540, 1380, 1.25),   # S2: Power stance below glowing ALGENZA logo
    (540, 1500, 1.05),   # S3: Below weapon cards
    (540, 1520, 1.00),   # S4: Below 5-stage pipeline
    (540, 1530, 1.00),   # S5: Guard stance below risk panel
    (540, 1510, 1.00),   # S6: Below proprietary code tree
    (540, 1440, 1.15),   # S7: Below golden stats
    (540, 1310, 1.30)    # S8: Centered below final CTA button
]

# 6. KHATARNAK MASCOT: ALGENZA QUANT SENTINEL MECHA (TITAN)
def draw_mecha_sentinel(c, t, m, x, y, s, i):
    # Combat states
    alarm_mode = (i == 1)
    power_surge = (i in (2, 7, NS - 1))
    scanning = (i in (0, 3, 4))
    
    # High-intensity colors based on mode
    v_color = RED if alarm_mode else GOLD if power_surge else CYAN
    core_pulse = 0.5 + 0.5 * math.sin(t * (14 if power_surge else 7))
    
    # 1. Aura of Dominance / Plasma Halo
    c.drawCircle(x, y, 170 * s, GL(v_color, 0.18 + 0.12 * core_pulse, 0, 48))
    
    # 2. Dual Ion Thrusters (Bottom Exhaust)
    thrust_flicker = 0.8 + 0.2 * math.sin(t * 30)
    for tx_offset in (-38, 38):
        c.drawLine(x + tx_offset * s, y + 105 * s, x + (tx_offset * 1.3) * s, y + (165 + 15 * thrust_flicker) * s, P(v_color, 0.8, 6 * s))
        c.drawCircle(x + (tx_offset * 1.3) * s, y + (165 + 15 * thrust_flicker) * s, 10 * s * thrust_flicker, GL(CYAN if not alarm_mode else RED, 0.5, 0, 16))
        c.drawCircle(x + (tx_offset * 1.3) * s, y + (165 + 15 * thrust_flicker) * s, 5 * s, P(WH))
        
    # 3. Heavy Angular Pauldrons (Shoulder Armor)
    for side in (-1, 1):
        sh_x = x + side * 76 * s
        sh_y = y - 40 * s
        p_sh = skia.Path()
        p_sh.moveTo(sh_x - side * 18 * s, sh_y - 30 * s)
        p_sh.lineTo(sh_x + side * 34 * s, sh_y - 15 * s)
        p_sh.lineTo(sh_x + side * 28 * s, sh_y + 35 * s)
        p_sh.lineTo(sh_x - side * 18 * s, sh_y + 25 * s)
        p_sh.close()
        c.drawPath(p_sh, P('#131B28'))
        c.drawPath(p_sh, P(GOLD_DARK if not alarm_mode else RED, 1, 3 * s))
        # Pauldron gold chevron stripe
        c.drawLine(sh_x, sh_y - 10 * s, sh_x + side * 18 * s, sh_y + 10 * s, P(GOLD, 1, 3 * s))
        
    # 4. Articulated Hydraulic Cyber Arms
    # Left Arm: Tactical Laser Pointer / Crosshair Projector
    al = 3.65 if scanning else 2.4 - 0.7 * m
    arm_x1 = x - 76 * s
    arm_y1 = y - 10 * s
    arm_x2 = arm_x1 + 85 * s * math.cos(al)
    arm_y2 = arm_y1 + 85 * s * math.sin(al)
    
    c.drawLine(arm_x1, arm_y1, arm_x2, arm_y2, P('#162232', 1, 14 * s))
    c.drawLine(arm_x1, arm_y1, arm_x2, arm_y2, P(CYAN if not alarm_mode else RED, 0.8, 3 * s))
    c.drawCircle(arm_x1, arm_y1, 10 * s, P(GOLD))
    c.drawCircle(arm_x2, arm_y2, 10 * s, P('#1D2B3F'))
    c.drawCircle(arm_x2, arm_y2, 6 * s, P(v_color))
    
    # Real Laser Projection Beam from Left Arm onto screen!
    if scanning or i == 0:
        laser_target_x = 540 + 280 * math.sin(t * 3.5)
        laser_target_y = 650 + 120 * math.cos(t * 2.8)
        c.drawLine(arm_x2, arm_y2, laser_target_x, laser_target_y, GL(RED if alarm_mode else CYAN, 0.6, 6))
        c.drawLine(arm_x2, arm_y2, laser_target_x, laser_target_y, P(WH, 0.9, 2))
        # Reticle at laser tip
        c.drawCircle(laser_target_x, laser_target_y, 14, P(v_color, 0.9, 2))
        c.drawCircle(laser_target_x, laser_target_y, 4, P(WH))
        
    # Right Arm: Hydraulic Combat Clench / Fist
    ar = (-0.95 + 0.45 * math.sin(t * 9)) if power_surge else 0.85 + 0.12 * math.sin(t * 2.5)
    r_arm_x1 = x + 76 * s
    r_arm_y1 = y - 10 * s
    r_arm_x2 = r_arm_x1 + 75 * s * math.cos(ar)
    r_arm_y2 = r_arm_y1 + 75 * s * math.sin(ar)
    c.drawLine(r_arm_x1, r_arm_y1, r_arm_x2, r_arm_y2, P('#162232', 1, 14 * s))
    c.drawLine(r_arm_x1, r_arm_y1, r_arm_x2, r_arm_y2, P(GOLD, 0.8, 3 * s))
    c.drawCircle(r_arm_x1, r_arm_y1, 10 * s, P(GOLD))
    c.drawCircle(r_arm_x2, r_arm_y2, 10 * s, P('#1D2B3F'))
    c.drawCircle(r_arm_x2, r_arm_y2, 6 * s, P(GOLD))
    
    # 5. Main Heavy Armored Torso (Titan Obsidian Chassis)
    torso = skia.Path()
    torso.moveTo(x - 64 * s, y - 85 * s)
    torso.lineTo(x + 64 * s, y - 85 * s)
    torso.lineTo(x + 72 * s, y + 45 * s)
    torso.lineTo(x + 48 * s, y + 105 * s)
    torso.lineTo(x - 48 * s, y + 105 * s)
    torso.lineTo(x - 72 * s, y + 45 * s)
    torso.close()
    c.drawPath(torso, P('#0E131C'))
    c.drawPath(torso, P('#202A3C', 1, 4 * s))
    
    # Armor plate cutouts & carbon texture
    c.drawLine(x - 52 * s, y - 10 * s, x + 52 * s, y - 10 * s, P(LN, 1, 2 * s))
    c.drawLine(x - 42 * s, y + 45 * s, x + 42 * s, y + 45 * s, P(LN, 1, 2 * s))
    
    # 6. Central Quantum Arc Reactor (Chest Core)
    core_y = y + 20 * s
    c.drawCircle(x, core_y, 34 * s, P('#080B10'))
    c.drawCircle(x, core_y, 34 * s, P(GOLD_DARK, 1, 3 * s))
    # Concentric energy rings
    c.drawCircle(x, core_y, 25 * s, GL(v_color, 0.45 * core_pulse, 0, 16))
    c.drawCircle(x, core_y, 18 * s, P(v_color, 0.85))
    c.drawCircle(x, core_y, 9 * s, P(WH))
    # Algenza chevron etched on the reactor
    chev = skia.Path()
    chev.moveTo(x - 12 * s, core_y + 10 * s)
    chev.lineTo(x, core_y - 10 * s)
    chev.lineTo(x + 12 * s, core_y + 10 * s)
    c.drawPath(chev, P(DK, 1, 3 * s))
    
    # 7. Angular Combat Helmet
    helmet = skia.Path()
    helmet.moveTo(x - 54 * s, y - 85 * s)
    helmet.lineTo(x - 42 * s, y - 150 * s)
    helmet.lineTo(x, y - 175 * s)  # Sharp battle crest tip
    helmet.lineTo(x + 42 * s, y - 150 * s)
    helmet.lineTo(x + 54 * s, y - 85 * s)
    helmet.close()
    c.drawPath(helmet, P('#121722'))
    c.drawPath(helmet, P(GOLD, 1, 4 * s))
    
    # Top Telemetry Spike / Antenna
    c.drawLine(x, y - 175 * s, x, y - 215 * s, P(GOLD, 1, 4 * s))
    c.drawCircle(x, y - 215 * s, 8 * s, GL(v_color, 0.6, 0, 10))
    c.drawCircle(x, y - 215 * s, 5 * s, P(WH))
    
    # 8. Menacing Cyber Visor (Cylon / Terminator Laser Scanner)
    visor_y = y - 120 * s
    rr(c, x - 44 * s, visor_y - 16 * s, x + 44 * s, visor_y + 16 * s, 8 * s, P(DK))
    rr(c, x - 44 * s, visor_y - 16 * s, x + 44 * s, visor_y + 16 * s, 8 * s, P('#2D3B52', 1, 2 * s))
    
    # Laser Eye Beam scanning horizontally inside the visor!
    scan_offset = math.sin(t * 7) * 26 * s
    c.drawLine(x - 38 * s, visor_y, x + 38 * s, visor_y, P(v_color, 0.4, 3 * s))
    c.drawCircle(x + scan_offset, visor_y, 11 * s, GL(v_color, 0.9, 0, 14))
    c.drawCircle(x + scan_offset, visor_y, 6 * s, P(WH))
    
    # 9. Audio-Reactive Cyber Grille / Mouth Cavity
    mouth_y = y - 72 * s
    m_h = (4 + 28 * m) * s
    m_w = (38 - 6 * m) * s
    rr(c, x - m_w / 2, mouth_y - m_h / 2, x + m_w / 2, mouth_y + m_h / 2, 4 * s, P('#05070B'))
    rr(c, x - m_w / 2, mouth_y - m_h / 2, x + m_w / 2, mouth_y + m_h / 2, 4 * s, P(v_color, 0.7, 2 * s))
    # Soundwave bars inside mouth
    for bar_idx in range(-3, 4):
        b_x = x + bar_idx * 5 * s
        b_h = max(2, (12 * m * math.cos(bar_idx * 0.4))) * s
        c.drawLine(b_x, mouth_y - b_h / 2, b_x, mouth_y + b_h / 2, P(v_color, 0.9, 2 * s))

def char(c, t, m):
    if t < 0.2: return
    i = max(k for k in range(NS) if t >= SS[k])
    if i == 0:
        x, y, s = A[0]
    else:
        g = sm(t, SS[i], SS[i] + 0.6)
        a, b = A[i - 1], A[i]
        x, y, s = [a[j] + (b[j] - a[j]) * g for j in range(3)]
        
    # Controlled aggressive mechanical hover
    y += math.sin(t * 3.2) * 8 * s
    draw_mecha_sentinel(c, t, m, x, y, s, i)

# 7. Scene Renders (All tailored for TikTok 9:16 Vertical)
def s0(c, t):
    # Scene 0: Hook - 95% of traders lose
    tx_x, tx_y = 70, 260
    head(c, "95% OF TRADERS LOSE.", tx_x, tx_y, 1, 60)
    sub(c, "Destroyed by emotions & algorithmic predators.", tx_x, tx_y + 54, 1, 26)
    
    # Live High-Volatility Gold Chart
    base_x, base_y, span_y, cand_step = 80, 960, 380, 58
    for k, (o, h, l, cc) in enumerate(CAND):
        g = sm(t, cand_t(k), cand_t(k) + 0.22)
        if g <= 0: continue
        x = base_x + k * cand_step
        col = GREEN if cc >= o else RED
        c.drawLine(x, CY(h, base_y, span_y), x, CY(l, base_y, span_y), P(col, g, 3))
        yo = CY(o, base_y, span_y)
        yc = yo + (CY(cc, base_y, span_y) - yo) * g
        rr(c, x - 13, min(yo, yc), x + 13, max(yo, yc) + 2, 4, P(col))
        
    g = sm(t, 2.0, 3.0)
    n = int(16 * g)
    if n > 1:
        pa = skia.Path()
        pa.moveTo(base_x, CY(CAND[0][3], base_y, span_y))
        for k in range(1, n):
            pa.lineTo(base_x + k * cand_step, CY(CAND[k][3], base_y, span_y))
        c.drawPath(pa, GL(CYAN, 0.6, 10))
        c.drawPath(pa, P(CYAN, 0.9, 3))

def pf(w):
    return 600 - (90 * math.sin(w * .007) + 50 * math.sin(w * .02 + 1) + 22 * math.sin(w * .06))

def s1(c, t):
    # Scene 1: Liquidity Trap - Slippage & Prop drawdown rules
    u = t - SS[1]
    tx_x, tx_y = 70, 260
    head(c, "HUMANS CANNOT COMPETE.", tx_x, tx_y, 1, 56)
    sub(c, "Slippage. Blown drawdowns. Missed Gold spikes.", tx_x, tx_y + 52, 1, 26)
    
    pan_l, pan_t, pan_r, pan_b = 70, 360, 1010, 960
    panel(c, pan_l, pan_t, pan_r, pan_b)
    
    sc = u * 280
    pa = skia.Path()
    step_x = 6
    for j, sx in enumerate(range(pan_l + 20, pan_r - 19, step_x)):
        (pa.moveTo if j == 0 else pa.lineTo)(sx, pf(sx + sc) - 80)
    c.drawPath(pa, GL(RED, 0.6, 12))
    c.drawPath(pa, P(RED, 1, 3))
    
    for k in range(int(sc / 380) - 1, int((sc + 1300) / 380) + 2):
        wx = k * 380 + 190
        sx = wx - sc
        if not (pan_l + 50 < sx < pan_r - 40): continue
        py = pf(wx) - 80
        c.drawCircle(sx, py, 11, P(RED))
        rr(c, sx - 80, py - 70, sx + 80, py - 22, 10, P(RED, 0.95))
        tx(c, "LIQUIDITY SWEPT", sx, py - 38, 'bb', 19, WH, 1, 'c')
        
    # Emergency Siren Badge
    c.drawCircle(pan_r - 70, pan_t - 70, 42, GL(RED, 0.5 + 0.5 * math.sin(t * 12), 0, 20))
    c.drawCircle(pan_r - 70, pan_t - 70, 32, P(RED))
    tx(c, "!", pan_r - 70, pan_t - 58, 'bb', 36, WH, 1, 'c')

def s2(c, t):
    # Scene 2: ALGENZA Brand Impact Reveal
    u = t - SS[2]
    cx, cy = 540, 620
    g = sm(u, 0.1, 0.8)
    
    # Cinematic shockwave rings
    for rad_mul in (1.2, 1.6, 2.0):
        c.drawCircle(cx, cy, 320 * g * rad_mul, GL(GOLD, 0.25 * (1 - g), 0, 24))
        c.drawCircle(cx, cy, 320 * g * rad_mul, P(GOLD, (1 - g), 3))
        
    logo_algenza(c, cx, cy, sz=120, a=g, al='c', glow=0.6)
    
    tx(c, "INSTITUTIONAL ALGORITHMIC WARFARE", cx, cy + 120, 'bb', 32, GOLD, sm(u, 0.8, 1.4), 'c')
    tx(c, "Engineered for pure execution dominance.", cx, cy + 170, 'b', 28, MU, sm(u, 1.2, 1.8), 'c')

CARDS = [
    ("MT5 / MQL5 Systems", "Deterministic Expert Advisors", "Institutional execution state machine"),
    ("Python Async Bridge", "IBKR & WebSocket Streams", "Real-time order routing & queuing"),
    ("FIX 4.4 Gateways", "Sub-Millisecond Execution", "Direct low-latency broker protocol")
]
def s3(c, t):
    # Scene 3: The Weapons Arsenal
    tx_x, tx_y = 70, 260
    head(c, "YOUR TRADING ARSENAL.", tx_x, tx_y, 1, 56)
    sub(c, "Built directly for real execution conditions.", tx_x, tx_y + 50, 1, 26)
    
    for k, (ti, su, detail) in enumerate(CARDS):
        g = sm(t, card_t(k), card_t(k) + 0.45)
        if g <= 0: continue
        x = 70
        y = 350 + k * 230 + (1 - g) * 45
        card_w, card_h = 940, 205
        
        panel(c, x, y, x + card_w, y + card_h, g)
        rr(c, x, y, x + card_w, y + 6, 3, P(GOLD, g))
        
        # Weapon spec badge
        rr(c, x + 35, y + 35, x + 115, y + 115, 14, P('#141D2B', g))
        rr(c, x + 35, y + 35, x + 115, y + 115, 14, P(GOLD, g, 2))
        tx(c, f"0{k+1}", x + 75, y + 84, 'bb', 36, GOLD, g, 'c')
        
        tx(c, ti, x + 145, y + 70, 'h', 38, WH, g)
        tx(c, su, x + 145, y + 115, 'bb', 24, CYAN, g)
        tx(c, detail, x + 145, y + 155, 'b', 22, MU, g)

NL = ["MARKET DATA", "SIGNAL ENGINE", "RISK ENGINE", "EXECUTION", "MONITORING"]
def s4(c, t):
    # Scene 4: 5-Stage Execution Architecture
    tx_x, tx_y = 70, 260
    head(c, "5-STAGE ARCHITECTURE.", tx_x, tx_y, 1, 54)
    sub(c, "Direct from algenza.com system blueprint.", tx_x, tx_y + 50, 1, 26)
    
    pan_l, pan_r = 70, 1010
    NY = 360
    NX = [170 + k * 180 for k in range(5)]
    
    for k in range(4):
        c.drawLine(NX[k] + 32, NY, NX[k + 1] - 32, NY, P(LN, 1, 4))
        g = sm(t, node_t(k) + 0.15, node_t(k + 1))
        if g > 0:
            c.drawLine(NX[k] + 32, NY, NX[k] + 32 + (NX[k + 1] - NX[k] - 64) * g, NY, GL(GOLD, 0.7, 8))
            c.drawLine(NX[k] + 32, NY, NX[k] + 32 + (NX[k + 1] - NX[k] - 64) * g, NY, P(GOLD, 1, 4))
            
    st = -1
    for k in range(5):
        c.drawCircle(NX[k], NY, 30, P(PN))
        c.drawCircle(NX[k], NY, 30, P(LN, 1, 3))
        a = cl((t - node_t(k)) / 0.35)
        if a > 0:
            st = k
            c.drawCircle(NX[k], NY, 42 * bo(a), GL(GOLD, 0.5, 0, 16))
            c.drawCircle(NX[k], NY, 30 * bo(a), P(GOLD))
        tx(c, str(k + 1), NX[k], NY + 10, 'bb', 26, DK if a > 0.5 else MU, 1, 'c')
        tx(c, NL[k], NX[k], NY + 70, 'bb', 15, WH if a > 0.5 else MU, 1, 'c')
        
    pan_t, pan_b = 480, 1020
    panel(c, pan_l, pan_t, pan_r, pan_b)
    if st < 0: return
    
    u = t - node_t(st)
    X = pan_l + 45
    Y = pan_t + 55
    
    if st == 0:
        for j, (k_name, v_val) in enumerate((("INGESTION", "Raw Tick & Depth Stream"), ("SPREAD FILTER", "Strict Enforcement Cap"), ("DATA BUFFER", "Rolling Asynchronous Window"))):
            tx(c, k_name, X, Y + 50 + j * 90, 'mb', 26, GOLD)
            tx(c, v_val, X + 220, Y + 50 + j * 90, 'm', 26, WH)
    elif st == 1:
        for j, (k_name, v_val) in enumerate((("STATE MACHINE", "Deterministic & Non-Repainting"), ("CONFLUENCE", "Multi-Timeframe Structure"), ("SESSION LOCK", "London & NY Overlap Windows"))):
            tx(c, k_name, X, Y + 50 + j * 90, 'mb', 26, CYAN)
            tx(c, v_val, X + 230, Y + 50 + j * 90, 'm', 26, WH)
    elif st == 2:
        for j, (k_name, v_val) in enumerate((("DAILY LOSS", "Hard Account Ceiling Stop"), ("BASKET DD", "Dynamic Trailing Lock"), ("RISK / TRADE", "Strict 1.0% Hard Gate"))):
            tx(c, k_name, X, Y + 50 + j * 90, 'mb', 26, RED)
            tx(c, v_val, X + 210, Y + 50 + j * 90, 'm', 26, WH)
    elif st == 3:
        for j, (k_name, v_val) in enumerate((("ORDER ROUTING", "Direct Broker REST / FIX Bridge"), ("SLIPPAGE CAP", "< 0.4ms Execution Tolerance"), ("BRACKET ORDERS", "Hard Server-Side SL / TP"))):
            tx(c, k_name, X, Y + 50 + j * 90, 'mb', 26, GREEN)
            tx(c, v_val, X + 240, Y + 50 + j * 90, 'm', 26, WH)
    else:
        for j, (k_name, v_val) in enumerate((("HEARTBEAT", "Active 24/7 VPS Watchdog"), ("DISCONNECT", "Automated Failsafe State"), ("AUDIT LOG", "Structured JSON Telemetry"))):
            tx(c, k_name, X, Y + 50 + j * 90, 'mb', 26, GOLD)
            tx(c, v_val, X + 210, Y + 50 + j * 90, 'm', 26, WH)

def s5(c, t):
    # Scene 5: Hard Risk Engine
    u = t - SS[5]
    tx_x, tx_y = 70, 260
    head(c, "HARD RISK CEILINGS.", tx_x, tx_y, 1, 54)
    sub(c, "Automated protection before human panic begins.", tx_x, tx_y + 50, 1, 26)
    
    pan1_l, pan1_r, pan1_t, pan1_b = 70, 1010, 350, 700
    panel(c, pan1_l, pan1_t, pan1_r, pan1_b)
    
    for k, (lb, v, fr) in enumerate((("Max Daily Drawdown", "2.0%", 0.35), ("Risk Per Trade", "1.0%", 0.20), ("Prop Firm Challenge", "100% SAFE", 1.0))):
        y = pan1_t + 85 + k * 105
        tx(c, lb, pan1_l + 40, y, 'bb', 24, WH)
        tx(c, v, pan1_r - 40, y, 'mb', 26, GOLD if k < 2 else GREEN, 1, 'r')
        rr(c, pan1_l + 40, y + 30, pan1_r - 40, y + 44, 6, P(LN))
        g = sm(u, 0.2 + k * 0.25, 1.0 + k * 0.25)
        if g > 0:
            rr(c, pan1_l + 40, y + 30, pan1_l + 40 + (pan1_r - pan1_l - 80) * fr * g, y + 44, 6, P(GREEN if k == 2 else GOLD))
            
    # Live Phone Alert Mockup
    X0, Y0, X1, Y1 = 140, 760, 940, 1220
    panel(c, X0, Y0, X1, Y1)
    tx(c, "TELEGRAM EXECUTION ALERT", X0 + 40, Y0 + 60, 'bb', 24, CYAN)
    tx(c, "now", X1 - 40, Y0 + 60, 'b', 20, MU, 1, 'r')
    tx(c, "> PASS GATE ACTIVATED: XAUUSD", X0 + 40, Y0 + 120, 'mb', 28, GREEN)
    tx(c, "> Hard SL locked at entry + 2R", X0 + 40, Y0 + 170, 'm', 24, WH)
    tx(c, "> Daily profit target reached. System locked safely.", X0 + 40, Y0 + 220, 'b', 22, MU)

FILES = ["Algenza_TitanEngine.mq5", "IBKR_AsyncBridge.py", "FIX_GateHandler.cpp", "PropRiskGuardian.mq5", "Architecture_Manual.pdf"]
def s6(c, t):
    # Scene 6: Zero Black Boxes / 100% Proprietary Code
    u = t - SS[6]
    tx_x, tx_y = 70, 260
    head(c, "ZERO BLACK BOXES.", tx_x, tx_y, 1, 56)
    sub(c, "Clean, modular source code you own forever.", tx_x, tx_y + 50, 1, 26)
    
    pan_l, pan_r, pan_t, pan_b = 70, 1010, 350, 800
    panel(c, pan_l, pan_t, pan_r, pan_b)
    tx(c, "ALGENZA_DEPLOYMENT_PACKAGE /", pan_l + 40, pan_t + 55, 'mb', 20, GOLD)
    
    for k, fn in enumerate(FILES):
        a = sm(u, 0.2 + k * 0.14, 0.55 + k * 0.14)
        y = pan_t + 105 + k * 65
        rr(c, pan_l + 45, y - 24, pan_l + 70, y + 4, 4, P(GOLD, a, 3))
        tx(c, fn, pan_l + 90, y, 'm', 22, WH, a)
        
    chk_x = 130
    CHK = ["100% Full Source Code Handover", "Deterministic Non-Repainting Logic", "Direct Systems Engineer Support"]
    for k, s in enumerate(CHK):
        y = 900 + k * 130
        g = cl((t - check_t(k)) / 0.35)
        c.drawCircle(chk_x, y, 28, P(LN, 1, 3))
        if g > 0:
            c.drawCircle(chk_x, y, 28 * bo(g), P(GOLD))
            pa = skia.Path()
            pa.moveTo(chk_x - 12, y)
            pa.lineTo(chk_x - 3, y + 10)
            pa.lineTo(chk_x + 14, y - 10)
            c.drawPath(pa, P(DK, g, 5))
        tx(c, s, chk_x + 50, y + 10, 'bb', 24, WH, 0.35 + 0.65 * g)

def s7(c, t):
    # Scene 7: Proven Firepower - Muhammad Hassan
    u = t - SS[7]
    tx_x, tx_y = 70, 260
    head(c, "PROVEN FIREPOWER.", tx_x, tx_y, 1, 54)
    sub(c, "Lead Systems Engineer: Muhammad Hassan", tx_x, tx_y + 50, 1, 26)
    
    for k in range(2):
        g = sm(u, 0.3 + k * 0.35, 0.8 + k * 0.35)
        if g <= 0: continue
        x = 70
        y = 360 + k * 440 + (1 - g) * 50
        card_w, card_h = 940, 390
        cx = x + card_w / 2
        
        panel(c, x, y, x + card_w, y + card_h, g)
        rr(c, x, y, x + card_w, y + 6, 3, P(GOLD, g))
        v = sm(u, 0.35 + k * 0.35, 1.7 + k * 0.35)
        
        if k == 0:
            tx(c, f"{int(round(200 * v))}+", cx, y + 190, 'h', 115, GOLD, g, 'c')
            tx(c, "Custom Algorithmic Systems Delivered", cx, y + 280, 'bb', 28, WH, g, 'c')
            tx(c, "Verified across MT5, MT4 & Python", cx, y + 330, 'b', 24, MU, g, 'c')
        else:
            tx(c, "100%", cx, y + 190, 'h', 115, CYAN, g, 'c')
            tx(c, "Proprietary Code Handover & IP", cx, y + 280, 'bb', 28, WH, g, 'c')
            tx(c, "github.com/Shifrozy", cx, y + 330, 'm', 24, GOLD, g, 'c')

def s8(c, t):
    # Scene 8: Final Strike - Call to Action
    u = t - SS[8]
    a = sm(u, 0.1, 0.5)
    cx, cy = 540, 460
    
    logo_algenza(c, cx, cy, sz=54, a=a, al='c', glow=0.6)
    head(c, "DEPLOY YOUR EDGE.", 70, 580, sm(u, 0.2, 0.7), 54)
    sub(c, "Turn your strategy into an automated weapon.", 70, 645, sm(u, 0.5, 1.0), 26)
    
    g = bo((t - BTN_T) / 0.5)
    if g > 0.01:
        btn_w = 640
        btn_cx, btn_cy = 540, 770
        hw, hh = btn_w / 2 * g, 48 * g
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(btn_cx - hw, btn_cy - hh, btn_cx + hw, btn_cy + hh), hh, hh), GL(GOLD, 0.65, 0, 26))
        rr(c, btn_cx - hw, btn_cy - hh, btn_cx + hw, btn_cy + hh, hh, P(GOLD))
        tx(c, "algenza.com", btn_cx, btn_cy + 14, 'bb', int(42 * g) + 1, DK, 1, 'c')
        
    tx(c, "Direct WhatsApp: +92 319 7375850", cx, 890, 'bb', 26, WH, sm(u, 0.8, 1.3), 'c')

SC = [s0, s1, s2, s3, s4, s5, s6, s7, s8]

# 8. Subtitle Wrapping & Display
def wrap(s, n):
    out = []
    cur = ""
    for w in s.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    out.append(cur)
    return out

def subs(c, t):
    wrap_limit = 42
    font_sz = 24
    sub_cx = W / 2
    sub_y_base = H - 140
    
    for i, s0_ in enumerate(ST):
        e = s0_ + D[i]
        if s0_ - 0.1 <= t <= e + 0.3:
            a = min(sm(t, s0_ - 0.1, s0_ + 0.15), 1 - sm(t, e + 0.05, e + 0.3))
            ls = wrap(LINES[i], wrap_limit)
            f = F('b', font_sz)
            mw = max(f.measureText(l) for l in ls)
            y0 = sub_y_base - (len(ls) - 1) * 36
            rr(c, sub_cx - mw / 2 - 24, y0 - 34, sub_cx + mw / 2 + 24, sub_y_base + 16, 12, P('#000000', 0.65 * a))
            for j, l in enumerate(ls):
                tx(c, l, sub_cx, y0 + j * 36, 'b', font_sz, WH, a, 'c')

def wm(c, t):
    a = sm(t, SS[2] + 1.2, SS[2] + 2.0) * (1 - sm(t, SS[NS - 1], SS[NS - 1] + 0.4))
    if a <= 0: return
    logo_algenza(c, 70, 110, 26, a, al='l')

# High-voltage cyber sparks
_pr = np.random.default_rng(77)
PT = list(zip(_pr.uniform(0, W, 80), _pr.uniform(0, H, 80), _pr.uniform(6, 26, 80), _pr.uniform(1.8, 4.2, 80), _pr.uniform(0, 6.28, 80)))

def parts(c, t):
    for x0, y0, sp, sz, ph in PT:
        y = (y0 - t * sp) % H
        x = x0 + math.sin(t * 0.8 + ph) * 20
        c.drawCircle(x, y, sz, P(GOLD if ph > 3.14 else CYAN, 0.12 + 0.18 * (0.5 + 0.5 * math.sin(t * 3 + ph))))

def sweep(c, t):
    for i in range(1, NS):
        u = (t - (SS[i] - 0.15)) / 0.50
        if 0 < u < 1:
            x = -100 + u * (W + 200)
            c.drawRect(skia.Rect.MakeLTRB(x - 45, 0, x + 45, H), GL(GOLD, 0.22, 0, 32))
            c.drawRect(skia.Rect.MakeLTRB(x - 2, 0, x + 2, H), P('#FFE899', 0.85))

SURF = skia.Surface(W, H)

def frame(fi):
    t = fi / FPS
    c = SURF.getCanvas()
    c.drawImage(BG, 0, 0)
    parts(c, t)
    CUR[0] = t
    
    for i in range(NS):
        if not (SS[i] - 0.01 <= t <= SE[i] + 0.06): continue
        a = 1.0 if i == 0 else sm(t, SS[i], SS[i] + 0.32)
        CUR[1] = SS[i] + (1.2 if i == 0 else 0)
        if i < NS - 1: a *= 1 - sm(t, SE[i] - 0.28, SE[i] + 0.05)
        if a <= 0.002: continue
        
        c.saveLayerAlpha(None, int(a * 255))
        z = 1 + 0.040 * cl((t - SS[i]) / (SE[i] - SS[i]))
        c.translate(W / 2, H / 2 + (1 - a) * 20)
        c.scale(z, z)
        c.translate(-W / 2, -H / 2)
        SC[i](c, t)
        c.restore()
        
    sweep(c, t)
    wm(c, t)
    char(c, t, float(MO[min(fi, len(MO) - 1)]))
    subs(c, t)
    return SURF

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'still':
        for ts in sys.argv[2:]:
            out_name = f'titan_still_{ts}.png'
            frame(int(float(ts) * FPS)).makeImageSnapshot().save(out_name, skia.kPNG)
            print(f"Saved {out_name}")
    else:
        w = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        out_seg = sys.argv[4] if len(sys.argv) > 4 else f'seg_titan_{w}.mp4'
        NF = int(END * FPS)
        a = NF * w // n
        b = NF * (w + 1) // n
        
        cmd = [
            FFMPEG_EXE, '-y', '-loglevel', 'error',
            '-f', 'rawvideo', '-pix_fmt', 'rgba',
            '-s', f'{W}x{H}', '-r', str(FPS),
            '-i', '-',
            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
            '-pix_fmt', 'yuv420p', '-g', '60',
            '-bf', '0', '-flags', '+cgop',
            out_seg
        ]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        for fi in range(a, b):
            p.stdin.write(frame(fi).makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
        p.stdin.close()
        p.wait()
        print(f"seg {w} done", flush=True)
