#!/usr/bin/env python
# coding: utf-8

# In[202]:


import pandas as pd
import numpy as np


# In[203]:


df = pd.read_csv('data-jumlah-lembaga-mahasiswa-baru-mahasiswa-terdaftar-lulusan-dan-tenaga-edukatif-perguruan-tinggi-negeri-dan-swasta-tahun-2011-sd-2013.csv')
df


# In[204]:


df['sum'] = df[['pt_negeri','pt_swasta']].sum(axis=1)
df


# In[205]:


columns = ['pt_negeri', 'pt_swasta']
df.drop(columns, inplace=True, axis=1)
df


# In[206]:


mhsbaru = df[df['indikator'].str.contains('Mahasiswa Baru')]
mhsbaru


# In[207]:


mhslulus = df[df['indikator'].str.contains('Lulusan')]
mhslulus


# In[208]:


df = pd.merge(mhsbaru, mhslulus, on='tahun', how='inner')
df


# In[209]:


df = df.rename(columns={'sum_x':'MahasiswaBaru','sum_y':'Lulusan'})
df


# In[210]:


columns = ['indikator_x', 'indikator_y']
df.drop(columns, inplace=True, axis=1)
df


# In[211]:


import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt


# In[229]:


def RangeSubjektif(_low, _high, _step):
    subjektif = np.arange(_low, _high, _step)
    return subjektif

def AlgortimaFuzzy1(_rule, _range_subjektif, _title):
    lo = fuzz.trimf(_range_subjektif, _rule[0])
    hi = fuzz.trimf(_range_subjektif, _rule[1])
    
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(_range_subjektif, lo, 'b', linewidth=1.5, label='Low')
    ax.plot(_range_subjektif, hi, 'g', linewidth=1.5, label='High')
    
    ax.set_title(_title)
    ax.legend()
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    plt.tight_layout()
    plt.show()
    
    return lo, hi

def AlgortimaFuzzy2(_rule, _range_subjektif, _title):
    lo = fuzz.trimf(_range_subjektif, _rule[0])
    hi = fuzz.trimf(_range_subjektif, _rule[1])
    
    fig, ax = plt.subplots(figsize=(10,4))
    ax.plot(_range_subjektif, lo, 'b', linewidth=1.5, label='Low')
    ax.plot(_range_subjektif, hi, 'g', linewidth=1.5, label='High')
    
    ax.set_title(_title)
    ax.legend()
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    plt.tight_layout()
    plt.show()
    
    return lo, hi


# In[214]:


def FungsiKeanggotaan(_range, _lo, _hi, _nilai):
    lo = fuzz.interp_membership(_range, _lo, _nilai)
    hi = fuzz.interp_membership(_range, _hi, _nilai)
    
    return lo,hi


# In[225]:


def Status(_keanggotaan):
    status =""
    if _keanggotaan[0] > _keanggotaan[1]:
        status = "low"
    elif _keanggotaan[0] < _keanggotaan[1]:
        status = "high"
        
    return status


# In[238]:


def RuleBased(_status_MahasiswaBaru, _statusLulusan):
    jumlah_MahasiswaBaru = _status_MahasiswaBaru
    jumlah_Lulusan = _statusLulusan
    
    persaingan_kerja =""
    
    if jumlah_MahasiswaBaru == 'low' and jumlah_Lulusan == 'low':
        persaingan_kerja = "lemah"
    elif jumlah_MahasiswaBaru == 'low' and jumlah_Lulusan == 'high':
        persaingan_kerja = "lemah"
    elif jumlah_MahasiswaBaru == 'high' and jumlah_Lulusan == 'low':
        persaingan_kerja = "kuat"
    elif jumlah_MahasiswaBaru == 'high' and jumlah_Lulusan == 'high':
        persaingan_kerja = "kuat"
    else :
        persaingan_kerja = "tidak diketahui"
        
    return persaingan_kerja


# In[230]:


xMahasiswaBaru = RangeSubjektif(260000,350000,1)
rMahasiswaBaru = np.array([
    [0, 260000, 280000],
    [265000, 350000, 350000]
])

xLulusan = RangeSubjektif(200000,240000,1)
rLulusan = np.array([
    [0, 200000, 225000],
    [220000, 240000, 240000]
])

lo_MahasiswaBaru, hi_MahasiswaBaru = AlgortimaFuzzy1(rMahasiswaBaru, xMahasiswaBaru, 'Mahasiswa Baru')
lo_Lulusan, hi_Lulusan = AlgortimaFuzzy2(rLulusan, xLulusan, 'Lulusan')

