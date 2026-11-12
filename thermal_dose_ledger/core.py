import math
from .common import number
def run(data):
 samples=data['samples'];reference=number(data['reference_kelvin'],100,3000);activation=number(data['activation_over_R_kelvin'],0,1e6);gap=number(data.get('maximum_gap_s',60),1e-9,1e6)
 if not isinstance(samples,list)or not 1<=len(samples)<=10000:raise ValueError('samples')
 rows=[];last=None;total=0.;missing=[]
 for s in samples:
  t=number(s['time_s'],0,1e12);temp=number(s['kelvin'],100,3000);exponent=activation*(1/reference-1/temp)
  if abs(exponent)>100:raise ValueError('exponent_regime')
  rate=math.exp(exponent)
  if last:
   dt=t-last[0]
   if dt<=0:raise ValueError('time_order')
   if dt>gap:missing.append({'start_s':last[0],'end_s':t});dose=None
   else:dose=dt*(last[1]+rate)/2;total+=dose
   rows.append({'start_s':last[0],'end_s':t,'equivalent_seconds':dose})
  last=t,rate
 return {'known_equivalent_seconds':total,'intervals':rows,'unknown_intervals':missing,'complete':not missing,'physical_process_validated':False}
