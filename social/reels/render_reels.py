#!/usr/bin/env python3
import json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "social" / "reels" / "output"
OUT.mkdir(parents=True, exist_ok=True)

W,H,DUR = 1080,1920,12
CHARCOAL = "0x252827"
GOLD = "0xB69A63"
CREAM = "0xF5F2EB"
RUST = "0xA06F47"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

FOX = ROOT / "logo-d.png"
FC = ROOT / "media" / "logos" / "fine-country-visible-v4.png"

campaign = [
  dict(n=1, slug="project-story", source="hero-hq.mp4",
       kicker="FOX DIGITAL LAND PRESENTS", title="Netherhouse Mews",
       subtitle="Four distinctive homes. One extraordinary valley setting.",
       detail="Turnditch · Amber Valley · DE56 2EA",
       cta="Explore the full development story"),
  dict(n=2, slug="redevelopment", source="site-film.mp4",
       kicker="THE OPPORTUNITY", title="A former dairy farm",
       subtitle="Reimagined for contemporary rural living",
       detail="Four detached family homes · 0.64 ha / 1.57 acres",
       cta="Historic farmyard. Modern architecture."),
  dict(n=3, slug="masterplan", source="masterplan-3d.jpg",
       kicker="THE MASTERPLAN", title="Four homes. One setting.",
       subtitle="A design-led courtyard above the Ecclesbourne Valley",
       detail="Interactive masterplan · 4 houses · 4 garages",
       cta="Netherhouse Mews · Turnditch"),
  dict(n=4, slug="hillside-overview", source="card-hillside.mp4",
       kicker="TYPE 01 · PLOTS 1 & 2", title="The Hillside",
       subtitle="5 bedrooms + office + cinema",
       detail="243.5 m² / 2,621 sq ft · double garage",
       cta="Split-level living shaped by the hillside"),
  dict(n=5, slug="plot-1", source="hillside-rear.webp",
       kicker="PLOT 01", title="The Hillside",
       subtitle="Signature split-level family home",
       detail="5 bedrooms · 3 ensuites · cinema · office",
       cta="Cantilevered balconies · glazed gable"),
  dict(n=6, slug="plot-2", source="hillside-front.webp",
       kicker="PLOT 02", title="The Hillside",
       subtitle="Mirrored counterpart to Plot 01",
       detail="243.5 m² / 2,621 sq ft · double garage",
       cta="48 m² kitchen / dining hall"),
  dict(n=7, slug="plot-3-meadow", source="card-meadow.mp4",
       kicker="TYPE 02 · PLOT 3", title="The Meadow",
       subtitle="5 bedrooms + office",
       detail="205.1 m² / 2,208 sq ft · double garage",
       cta="55 m² open-plan kitchen / dining"),
  dict(n=8, slug="plot-4-ridge", source="card-ridge.mp4",
       kicker="TYPE 03 · PLOT 4", title="The Ridge",
       subtitle="5 bedrooms + office + cinema",
       detail="231.3 m² · double garage",
       cta="Contemporary rural architecture"),
  dict(n=9, slug="planning", source="masterplan.webp",
       kicker="FULL PLANNING PERMISSION", title="AVA/2025/0519",
       subtitle="Consent granted · 2 March 2026",
       detail="Amber Valley Borough Council",
       cta="Oven-ready development opportunity"),
  dict(n=10, slug="biodiversity", source="aerial-south-west.webp",
       kicker="LANDSCAPE & BIODIVERSITY", title="38.2% BNG secured",
       subtitle="On-site biodiversity net gain",
       detail="Enhanced landscaping · sustainable drainage",
       cta="Designed to sit naturally in its setting"),
  dict(n=11, slug="location", source="aerial-south-east.webp",
       kicker="THE LOCATION", title="Turnditch, Derbyshire",
       subtitle="Village-edge setting above the Ecclesbourne Valley",
       detail="Belper 10 min · Duffield 10 min · Derby 25 min",
       cta="Hillcliff Lane · DE56 2EA"),
  dict(n=12, slug="agent-contact", source="lifestyle.mp4",
       kicker="SALES & ENQUIRIES", title="Fine & Country",
       subtitle="Anthony Taylor · 07726 314580",
       detail="anthony.taylor@fineandcountry.com",
       cta="Netherhouse Mews · viewing & offers"),
]

def esc(s):
    return str(s).replace("\\","\\\\").replace(":","\\:").replace("'","\\'").replace("%","\\%")

def draw(text, y, size, font=BOLD, color=CREAM, x="70"):
    return f"drawtext=fontfile={font}:text='{esc(text)}':fontcolor={color}:fontsize={size}:x={x}:y={y}:line_spacing=12"

def render(item):
    src = ROOT / item["source"]
    out = OUT / f'{item["n"]:02d}-{item["slug"]}.mp4'
    is_image = src.suffix.lower() in {".webp",".png",".jpg",".jpeg"}

    if is_image:
        input_args = ["-loop","1","-i",str(src)]
    else:
        input_args = ["-stream_loop","-1","-i",str(src)]
    input_args += ["-i",str(FOX),"-i",str(FC)]

    if is_image:
        base = (
          f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
          f"crop=1080:1920,zoompan=z='min(zoom+0.0007,1.10)':d={DUR*30}:s=1080x1920:fps=30,"
          f"eq=brightness=-0.04:saturation=0.92[base]"
        )
    else:
        base = (
          "[0:v]split=2[bg][fg];"
          "[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "gblur=sigma=30,eq=brightness=-0.16:saturation=0.82[bg2];"
          "[fg]scale=1080:1080:force_original_aspect_ratio=decrease[fg2];"
          "[bg2][fg2]overlay=(W-w)/2:(H-h)/2[base]"
        )

    text_layer = (
      "[base]"
      "drawbox=x=0:y=0:w=1080:h=355:color=0x252827@0.86:t=fill,"
      "drawbox=x=0:y=1440:w=1080:h=480:color=0x252827@0.92:t=fill,"
      "drawbox=x=70:y=338:w=940:h=2:color=0xB69A63@0.85:t=fill,"
      + draw(item["kicker"],92,29,color=GOLD)
      + "," + draw(item["title"],145,64)
      + "," + draw(item["subtitle"],245,30,font=FONT)
      + "," + draw(item["detail"],1515,30,font=FONT)
      + "," + draw(item["cta"],1600,27,font=BOLD,color=GOLD)
      + "[txt]"
    )

    filters = [
      base,
      text_layer,
      "[1:v]scale=92:-1[fox]",
      "[2:v]scale=260:-1[fc]",
      "[txt][fox]overlay=920:35[foxed]",
      "[foxed][fc]overlay=770:1740:format=auto[final]"
    ]

    cmd = [
      "ffmpeg","-y",*input_args,
      "-filter_complex",";".join(filters),
      "-map","[final]","-t",str(DUR),"-r","30","-an",
      "-c:v","libx264","-preset","veryfast","-crf","21",
      "-pix_fmt","yuv420p","-movflags","+faststart",str(out)
    ]
    print("Rendering", out.name)
    subprocess.run(cmd, check=True)

for item in campaign:
    render(item)

(OUT / "campaign.json").write_text(json.dumps(campaign, indent=2), encoding="utf-8")
print("Rendered", len(campaign), "reels to", OUT)
