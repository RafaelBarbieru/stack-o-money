import sys, io, base64, json
from PIL import Image
src = sys.argv[1]
# Real Europa-series dimensions (mm)
dims = {5:(120,62),10:(127,67),20:(133,72),50:(140,77),100:(147,77)}
files = {5:'eur_5.jpg',10:'eur_10.jpg',20:'eur_20.jpg',50:'eur_50.jpg',100:'eur_100.jpg'}
out = {}
for d,f in files.items():
    im = Image.open(f"{src}/{f}")
    if im.mode == 'RGBA':
        bg = Image.new('RGB', im.size, (245,243,236)); bg.paste(im, mask=im.split()[3]); im = bg
    im = im.convert('RGB')
    w = 1024; h = round(w*dims[d][1]/dims[d][0])   # force exact real aspect ratio
    im = im.resize((w,h), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf,'JPEG',quality=86,optimize=True)
    out[d] = 'data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
    print(d, (w,h), len(buf.getvalue())//1024, 'KB')
with open(f"{src}/textures.js",'w') as fh:
    fh.write('// Generated from eur_*.png/jpg: resized to the exact real banknote aspect ratio, embedded so index.html works from file://\n')
    fh.write('window.BANKNOTE_TEXTURES = '+json.dumps({str(k):v for k,v in out.items()})+';\n')
