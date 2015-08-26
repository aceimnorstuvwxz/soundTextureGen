#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
(C) 2015 Turnro.com

sound/music xxxx.mp3 ---> PCM --->FTT 
---->Requency Spectrum ----> xxxx.png as Texture for shader
'''


from pylab import*
from scipy.io import wavfile


sampFreq, snd = wavfile.read('440_sine.wav')
snd = snd / (2.**15)
s1 = snd[:,0] 
n = len(s1) 
p = fft(s1) # take the fourier transform 
nUniquePts = ceil((n+1)/2.0)
p = p[0:nUniquePts]
p = abs(p)
p = p / float(n) # scale by the number of points so that
                 # the magnitude does not depend on the length 
                 # of the signal or on its sampling frequency  
p = p**2  # square it to get the power 

# multiply by two (see technical document for details)
# odd nfft excludes Nyquist point
if n % 2 > 0: # we've got odd number of points fft
    p[1:len(p)] = p[1:len(p)] * 2
else:
    p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft

freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / n);
plot(freqArray/1000, 10*log10(p), color='k')
xlabel('Frequency (kHz)')
ylabel('Power (dB)')