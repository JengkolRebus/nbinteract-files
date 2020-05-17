from skyfield.api import load
from skyfield.api import Topos
from skyfield import almanac
from datetime import datetime
from pytz import timezone

# global conj, sunset, m_alt, m_az, m_d 
conj = []
sunset = []
moon_alt = []
moon_az = []
sun_alt = []
sun_az = []


jkt = timezone('Asia/Jakarta')
ts = load.timescale()
e = load('de421.bsp')

moon = e['moon']
earth = e['earth']

obsUAD = Topos('7.83305556 S', '110.38305556 E')
loc = earth + obsUAD

t0 = ts.utc(2020)
t1 = ts.utc(2021)
f = almanac.oppositions_conjunctions(e, e['moon'])
t, y = almanac.find_discrete(t0, t1, f)

# print(t0.astimezone(jkt), t1.astimezone(jkt))

for ti, yi in zip(t, y):
    
    if(yi == 1):
        # t0 = ts.utc(ti.utc[0], ti.utc[1], ti.utc[2])
        # t1 = ts.utc(ti.utc[0], ti.utc[1], ti.utc[2]+1)
        # t_rs, y_rs = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(e, obsUAD))
        # print(t0.astimezone(jkt), t1.astimezone(jkt))

        # for t_sun, y_sun in zip(t_rs, y_rs):
        #     global sunset
        #     if (y_sun == False):
        #         sunset = t_sun

        
        conj.append(ti)
        # print(ti.astimezone(jkt))
        # print(ti.astimezone(jkt))
        # print('sunset: ', sunset.astimezone(jkt))
    else:
        pass

for i in conj:
    i_utc = i.utc
    t0 = ts.utc(i_utc[0], i_utc[1], i_utc[2], i_utc[3], i_utc[4], i_utc[5])
    t1 = ts.utc(i_utc[0], i_utc[1], i_utc[2]+1, i_utc[3], i_utc[4], i_utc[5])
    t_rs, y_rs = almanac.find_discrete(t0, t1, almanac.sunrise_sunset(e, obsUAD))
    for t_sun, y_sun in zip(t_rs, y_rs):
        if (y_sun == False):
            sunset.append(t_sun)
            # sunset = t_sun
        else:
            pass

for s in sunset:
    s_utc = s.utc
    astro_moon = loc.at(ts.utc(s_utc[0], s_utc[1], s_utc[2], s_utc[3], s_utc[4], s_utc[5])).observe(moon)
    astro_sun = loc.at(ts.utc(s_utc[0], s_utc[1], s_utc[2], s_utc[3], s_utc[4], s_utc[5])).observe(e['sun'])

    m_alt, m_az, m_d = astro_moon.apparent().altaz()
    s_alt, s_az, s_d = astro_sun.apparent().altaz()

    moon_alt.append(m_alt)
    moon_az.append(m_az)
    sun_alt.append(s_alt)
    sun_az.append(s_az)

f = open("Moon Conjunction.txt","w+")

# Print All Values
header_text = "Conjunction Time;Sunset Time;Sun Altitude;Sun Azimuth;Moon Altitude;Moon Azimuth \n"
print(header_text)
f.write(header_text)

for t_conj, t_sunset, s_alt, s_azm, m_alt, m_az in zip(conj, sunset, sun_alt, sun_az, moon_alt, moon_az):
    f.write(str(t_conj.astimezone(jkt)) + ";")
    f.write(str(t_sunset.astimezone(jkt)) + ";")
    f.write(str(s_alt) + ";")
    f.write(str(s_azm) + ";")
    f.write(str(m_alt) + ";")
    f.write(str(m_az) + "\n")
    print(t_conj.astimezone(jkt), end=";")
    print(t_sunset.astimezone(jkt), end=";")
    print(s_alt, end=";")
    print(s_azm, end=";")
    print(m_alt, end=";")
    print(m_az)

f.close()


# print(i.astimezone(jkt), end="\t")
# print(sunset.astimezone(jkt), end="\t")
# print(m_alt, end="\t")
# print(m_az)