from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,html
R=Path(__file__).parent;D=R/'dist'
C=json.loads((R/'config.json').read_text(encoding='utf-8'))
A=json.loads((R/'assets.json').read_text(encoding='utf-8'))
class Parser(HTMLParser):
 def __init__(self,s):super().__init__();self.nodes=[];self.feed(s)
 def handle_starttag(self,t,a):self.nodes.append((t,dict(a)))
errors=[];count=0;titles=set();descriptions=set()
for p in D.rglob('*.html'):
 source=p.read_text(encoding='utf-8');nodes=Parser(source).nodes;count+=1
 assert not any(x in source for x in ('href="/privacy/"','href="/terms/"')),f'{p}: removed link'
 if sum(t=='h1' for t,a in nodes)!=1:errors.append(f'{p}: H1 count')
 if p.name!='404.html':
  for key,val in [('name','description'),('property','og:title'),('property','og:description'),('name','twitter:title'),('name','twitter:description')]:
   assert any(t=='meta' and a.get(key)==val for t,a in nodes),f'{p}: {val}'
  assert any(t=='link' and a.get('rel')=='canonical' for t,a in nodes)==bool(C['origin'])
  assert any(t=='meta' and a.get('property')=='og:image' for t,a in nodes)==bool(C['origin'])
  title=html.unescape(re.search(r'<title>(.*?)</title>',source).group(1))
  description=next(a['content'] for t,a in nodes if t=='meta' and a.get('name')=='description')
  assert title not in titles and description not in descriptions,f'{p}: duplicate metadata'
  assert 15<=len(title)<=65,f'{p}: title length {len(title)}'
  assert 40<=len(description)<=165,f'{p}: description length {len(description)}'
  titles.add(title);descriptions.add(description)
 assert not any(t=='iframe' for t,a in nodes),f'{p}: map should load on demand'
 for t,a in nodes:
  if t=='img':assert 'alt' in a
  url=a.get('href',a.get('src',''));u=urlsplit(url)
  if u.scheme or u.netloc or not u.path:continue
  path=D/unquote(u.path.lstrip('/'))
  if u.path.endswith('/'):path=path/'index.html'
  if not path.exists():errors.append(f'{p}: missing {url}')
  if u.fragment and path.suffix=='.html' and path.exists():
   assert any(a.get('id')==u.fragment for t,a in Parser(path.read_text(encoding='utf-8')).nodes)
  for attribute in ('srcset','imagesrcset'):
   for candidate in a.get(attribute,'').split(','):
    if not candidate.strip():continue
    image_url,width=candidate.strip().split()
    assert (D/image_url.lstrip('/')).is_file(),f'{p}: missing {image_url}'
    assert re.fullmatch(r'\d+w',width),f'{p}: invalid responsive width'
  if t=='img' and a.get('src','').endswith('.webp'):
   assert int(a['width'])>0 and int(a['height'])>0
   if a.get('class')=='hero-image':
    assert a.get('fetchpriority')=='high' and a.get('loading')=='eager' and a.get('sizes')=='100vw'
   elif 'brand' not in a.get('class','') and 'logo' not in a.get('src',''):
    assert a.get('loading')=='lazy'
 for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>',source):json.loads(ld)
legal=(R/'brief.txt').read_text(encoding='utf-8').split('LEGAL TEXT STARTS:')[1].split('LEGAL TEXT ENDS.')[0].strip().split('\n\n')[1:]
raw=(D/'waiver/index.html').read_text(encoding='utf-8').split('<article class="legal">')[1].split('</article>')[0]
actual=[html.unescape(x) for x in re.findall('<p>(.*?)</p>',raw,re.S)]
assert actual==legal,'Waiver mismatch'
assert not (D/'privacy/index.html').exists() and not (D/'terms/index.html').exists()
assert (D/'sitemap.xml').exists()==bool(C['origin'])
if C['origin']:
 from xml.etree import ElementTree
 urls=[n.text for n in ElementTree.parse(D/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
 assert len(urls)==count-1
 assert all(u.startswith(C['origin']+'/') and not u.endswith(('/privacy/','/terms/')) for u in urls)
else: assert 'Sitemap:' not in (D/'robots.txt').read_text(encoding='utf-8')
try:
 from PIL import Image
except ImportError:
 print('Pillow unavailable: skipping encoded image dimension checks.')
else:
 for asset in A:
  for variant in asset['variants']:
   with Image.open(D/variant['src'].lstrip('/')) as im:
    assert im.size==(variant['width'],variant['height']),f'Incorrect image dimensions: {variant["src"]}'
 print(f'PASS: actual dimensions match all {sum(len(a["variants"]) for a in A)} responsive photo variants.')
assert not errors,'\n'.join(errors)
print(f'PASS: {count} HTML pages; internal links/assets/fragments; metadata; one H1; schema JSON; image alt attributes; exact waiver ({len(legal)} paragraphs).')
print(f'Total deployed asset size: {sum(p.stat().st_size for p in D.rglob("*") if p.is_file())/1024/1024:.2f} MB')
