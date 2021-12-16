from datetime import datetime, timedelta
import requests, pandas as pd, subprocess
from pathlib import Path

outdir = Path('images')

outdir.mkdir(exist_ok=True)

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'})

url = "https://iswa.gsfc.nasa.gov/IswaSystemWebApp/iSWACygnetStreamer"
date_fmt = "%Y-%m-%d %H:%M:%S"

en_dt = datetime.now()
st_dt = en_dt - timedelta(days=2)
dr = pd.date_range(st_dt, en_dt, periods=150)

for n, ts in enumerate(dr.to_list()):
  with s.get(url, params={"timestamp": ts.strftime(date_fmt), 'window': "-1", "cygnetId": "239"}) as resp:
    fn = str(n) + ".jpeg"
    (outdir / fn).open('wb').write(resp.content)
    print(f"Got: {fn}")


subprocess.run("""ffmpeg -framerate 8 -i images/%d.jpeg out.mp4""".split())

# ffmpeg -framerate 8 -i images/%d.jpeg out.mp4
