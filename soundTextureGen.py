#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
(C) 2015 Turnro.com

sound/music xxxx.mp3 ---> PCM --->FTT 
---->Requency Spectrum ----> xxxx.png as Texture for shader
'''

import sys
from pylab import*
from scipy.io import wavfile
from PIL import Image, ImageDraw

TEXTURE_WIDTH = 256 #1024->281min 256->18min max,因为有PNG压缩，所以对图像的大小影响小，但对显存影响还是明显的。
FPS = 60
FFT_SCOPE = 1024 #fft 窗大小
FFT_UNIFORM = 200 #峰值在150左右,200保证安全


'''
shadertoy
https://www.shadertoy.com/view/MslGWN
我们仅需要这4个采样点的power数据，也刚好使得一个帧能够用纹理的一个Pixel表示。
'''
FFT_SAMPLE_R = 0.01
FFT_SAMPLE_G = 0.07
FFT_SAMPLE_B = 0.15
FFT_SAMPLE_A = 0.30
def genfft(s1):
    global fft_max
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

    ret = [abs(10*log10(x)) for x in p]
    return ret
'''
# for v in p:
#     print 10*log10(v)

freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / n);
img = Image.new("RGBA", (TEXTURE_WIDTH,TEXTURE_WIDTH), color=(256,0,0,256))
draw = ImageDraw.Draw(img)


plot(freqArray/1000, 10*log10(p), color='k')
xlabel('Frequency (kHz)')
ylabel('Power (dB)')
'''

def gen(fn):
    sampFreq, snd = wavfile.read(fn)
    #sampFreq采样率为1分钟的采样次数
    snd = snd / (2.**15)
    sound_length = len(snd)*1.0/sampFreq
    print "sound length = ",sound_length/60.0
    s1 = snd[:,0]
    #s1是左信道的全部数据 
    print "s1 size =",len(s1)
    
    img = Image.new("RGBA", (TEXTURE_WIDTH,TEXTURE_WIDTH), color=(0,0,0,256))
    draw = ImageDraw.Draw(img)
    
    FFT_STEP = sampFreq*1.0/FPS
    gfmax = 0.0
    for i in xrange(int(sound_length*FPS)):
        start_index = FFT_STEP*i
        end_index = start_index + FFT_SCOPE
        if  end_index >= len(s1):
            end_index = len(s1)-1
            
        if (start_index > 0.5*FFT_STEP):
            start_index -= 0.5*FFT_STEP
            end_index -= 0.5*FFT_STEP

        fft_data = s1[start_index:end_index]
        fft_ret = genfft(fft_data)
#         print len(fft_ret)
        fft_ret_len = len(fft_ret)
        rgba = [fft_ret[int(FFT_SAMPLE_R*fft_ret_len)],
                fft_ret[int(FFT_SAMPLE_G*fft_ret_len)],
                fft_ret[int(FFT_SAMPLE_B*fft_ret_len)],
                fft_ret[int(FFT_SAMPLE_A*fft_ret_len)]]
        for x in rgba:
            if x > gfmax:
                gfmax = x
        rgba = [1.0-x/FFT_UNIFORM for x in rgba]
        ###make uniform
        draw.point((i%TEXTURE_WIDTH, i/TEXTURE_WIDTH), fill=(int(256*rgba[0]),
                                      int(256*rgba[1]),
                                      int(256*rgba[2]),
                                      int(256*rgba[3])))
    img.save(fn+".png", 'PNG')
    print "max=",gfmax

if __name__ == "__main__":
    if len(sys.argv) == 2:
        fn = sys.argv[1]
        gen(fn)
    else:
        print "mp3 file path as parameter..."
    
    print 'DONE'
