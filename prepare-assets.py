from PIL import Image,ImageOps
import zipfile,io,json,re
from pathlib import Path
root=Path(__file__).parent; out=root/'dist/assets';out.mkdir(exist_ok=True,parents=True)
z=zipfile.ZipFile(root/'original-assets/photos.zip')
names=[n for n in z.namelist() if not n.startswith('.') and n.lower().endswith(('.jpg','.jpeg'))]
alts=['Open-air warehouse training floor','Dumbbell racks and free weights','Power rack and lifting platform','Strength training racks','Warehouse squat racks','Bench and lifting rack','Weight plates and strength equipment','Training station in the warehouse','Strength equipment against the warehouse wall','Cable machine','Bench and weight plates','Plate-loaded strength machine','Seated strength machine','Cardio equipment','Specialty bars stored on the wall','Strength training equipment','Warehouse access ramp','Equipment along the training floor','Bars and plates','Training accessories','Barbell storage','Gym access keypad','Dumbbells','100-pound weight plate','Ohio Power Bar','Barbell end cap','Earthquake Bar','Rogue Olympic Bar','Specialty bar grip','Olympic bar end cap',"Fringe Women’s Olympic Bar",'Longhorn Bar','Specialty bar end cap']
assets=[]
for i,n in enumerate(names):
 im=ImageOps.exif_transpose(Image.open(io.BytesIO(z.read(n)))).convert('RGB');slug=re.sub('[^a-z0-9]+','-',alts[i].lower()).strip('-')+'-state-line-gym'
 variants=[]
 for bound in [360,600,1400]:
  v=im.copy();v.thumbnail((bound,bound),Image.Resampling.LANCZOS)
  filename=f'{slug}-{bound}.webp';v.save(out/filename,'WEBP',quality=74,method=6)
  variants.append({'src':f'/assets/{filename}','width':v.width,'height':v.height})
 assets.append({'src':variants[-1]['src'],'small':variants[1]['src'],'alt':alts[i]+' at State Line Gym','width':variants[-1]['width'],'height':variants[-1]['height'],'variants':variants})
(root/'assets.json').write_text(json.dumps(assets,indent=2),encoding='utf-8')
logo=Image.open(root/'original-assets/logo.png').convert('RGBA')
logo.save(out/'state-line-logo.png',optimize=True)
logo.thumbnail((480,162),Image.Resampling.LANCZOS)
logo.save(out/'state-line-logo.webp','WEBP',lossless=True,method=6)
logo.thumbnail((64,64),Image.Resampling.LANCZOS)
logo.save(out/'favicon.png',optimize=True)
print(f'Optimized {len(assets)} photos in three sizes, plus the original logo artwork.')
