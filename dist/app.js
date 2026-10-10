const toggle=document.querySelector('.menu-toggle');const nav=document.querySelector('#navigation');
function closeMenu(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Open menu');}
toggle?.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close menu':'Open menu');});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){closeMenu();toggle.focus();}});document.addEventListener('click',e=>{if(!e.target.closest('header'))closeMenu();});
const photos=[...document.querySelectorAll('[data-image]')],dialog=document.querySelector('#lightbox');let current=0,opener;
function showPhoto(i){current=(i+photos.length)%photos.length;const p=photos[current];document.querySelector('#photo-large').src=p.dataset.image;document.querySelector('#photo-large').alt=p.dataset.caption;document.querySelector('#photo-caption').textContent=p.dataset.caption;document.querySelector('#photo-count').textContent=`${current+1} / ${photos.length}`;}
photos.forEach((p,i)=>p.addEventListener('click',()=>{opener=p;showPhoto(i);dialog.showModal();document.body.style.overflow='hidden';}));
document.querySelector('[data-close]')?.addEventListener('click',()=>dialog.close());document.querySelector('[data-prev]')?.addEventListener('click',()=>showPhoto(current-1));document.querySelector('[data-next]')?.addEventListener('click',()=>showPhoto(current+1));
dialog?.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();showPhoto(current+1);}if(e.key==='ArrowLeft'){e.preventDefault();showPhoto(current-1);}});dialog?.addEventListener('close',()=>{document.body.style.overflow='';opener?.focus();});dialog?.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
const form=document.querySelector('#contact-form');if(form){const query=new URLSearchParams(location.search);if([...form.interest.options].some(o=>o.value===query.get('interest')))form.interest.value=query.get('interest');if(query.get('plan'))form.message.value=`Hi Tom, I’m interested in the ${query.get('plan')} membership. Please send me the payment and access details.`;
let config={email:'tom@statelinegym.com',contactEndpoint:null};fetch('/site-config.json').then(r=>r.json()).then(c=>{config=c;if(c.contactEndpoint){form.querySelector('.muted').textContent='Your message will be sent to State Line Gym.';form.querySelector('button').textContent='SEND MESSAGE ↗';}}).catch(()=>{});
form.addEventListener('submit',async e=>{e.preventDefault();const data=Object.fromEntries(new FormData(form));const status=document.querySelector('#form-status');if(config.contactEndpoint){const button=form.querySelector('button');button.disabled=true;try{const response=await fetch(config.contactEndpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});if(!response.ok)throw new Error();status.textContent='Your message has been sent.';form.reset();}catch{status.textContent='Your message could not be sent. Please call or email Tom directly.';}finally{button.disabled=false;}}else{const body=`Name: ${data.name}\nEmail: ${data.email}\nPhone: ${data.phone||'Not provided'}\nInterest: ${data.interest}\n\n${data.message}`;location.href=`mailto:${config.email}?subject=${encodeURIComponent('State Line Gym — '+data.interest)}&body=${encodeURIComponent(body)}`;status.textContent='Your email draft is ready in your email app. Please send it there. If no app opened, email Tom directly using the link above.';}});}

// Keep the initial page local and light; load the interactive map on request.
document.querySelectorAll('[data-load-map]').forEach(button => {
  button.addEventListener('click', () => {
    const panel = button.closest('[data-map-url]');
    const frame = document.createElement('iframe');
    frame.title = 'Google Map — State Line Gym location';
    frame.src = panel.dataset.mapUrl;
    frame.referrerPolicy = 'no-referrer-when-downgrade';
    frame.allowFullscreen = true;
    panel.replaceWith(frame);
    frame.focus();
  }, {once: true});
});
