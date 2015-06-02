import numpy as np
import matplotlib as m

m.use('TkAgg')
m.interactive(True)

import matplotlib.pyplot as plt
from matplotlib import cm
import lensdemo_funcs as ldf

from matplotlib.widgets import Slider

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.45)
# Package some image display preferences in a dictionary object, for use below:
myargs = {'interpolation': 'nearest', 'origin': 'lower', 'cmap': cm.spectral}
#myargs = {'interpolation': 'nearest', 'origin': 'lower', 'cmap': cm.gray}

# Make some x and y coordinate images:
nx = 501
ny = 501
xhilo = [-2.5, 2.5]
yhilo = [-2.5, 2.5]
x = (xhilo[1] - xhilo[0]) * np.outer(np.ones(ny), np.arange(nx)) / float(nx-1) + xhilo[0]
y = (yhilo[1] - yhilo[0]) * np.outer(np.arange(ny), np.ones(nx)) / float(ny-1) + yhilo[0]

# Set some Gaussian blob image parameters and pack them into an array:
g_amp = 1.0   # peak brightness value
g_sig = 0.05  # Gaussian "sigma" (i.e., size)
g_xcen = 0.0  # x position of center
g_ycen = 0.0  # y position of center
g_axrat = 1.0 # minor-to-major axis ratio
g_pa = 0.0    # major-axis position angle (degrees) c.c.w. from x axis
gpar = np.asarray([g_amp, g_sig, g_xcen, g_ycen, g_axrat, g_pa])

# Set some SIE lens-model parameters and pack them into an array:
l_amp = 1.5   # Einstein radius
l_xcen = 0.0  # x position of center
l_ycen = 0.0  # y position of center
l_axrat = 1.0 # minor-to-major axis ratio
l_pa = 0.0    # major-axis position angle (degrees) c.c.w. from x axis
lpar = np.asarray([l_amp, l_xcen, l_ycen, l_axrat, l_pa])

#g_image = ldf.gauss_2d(x, y, gpar)
(xg, yg) = ldf.sie_grad(x, y, lpar)
g_lensimage = ldf.gauss_2d(x-xg, y-yg, gpar)

f = plt.imshow(g_lensimage, **myargs)

ax = plt.axes([0.25,0.1,0.65,0.03])
slaxrat = Slider(ax, 'Lens Axis Ratio', 0.0, 5.0, valinit=l_axrat)

ax = plt.axes([0.25,0.15,0.65,0.03])
sgaxrat = Slider(ax, 'Gaussian Axis Ratio', 0.0, 5.0, valinit=g_axrat)

ax = plt.axes([0.25,0.20,0.65,0.03])
sgpa = Slider(ax, 'Gaussian Major-Axis Angle', 0.0, 360.0, valinit=g_pa)

ax = plt.axes([0.25,0.25,0.65,0.03])
sgxcen = Slider(ax, 'Gaussian X-center', -1.5, 1.5, valinit=g_xcen)

ax = plt.axes([0.25,0.30,0.65,0.03])
sgycen = Slider(ax, 'Gaussian Y-center', -1.5, 1.5, valinit=g_ycen)

def update(val):
    g_axrat = sgaxrat.val
    g_xcen = sgxcen.val
    g_ycen = sgycen.val
    g_pa = sgpa.val 
    l_axrat = slaxrat.val

    gpar = np.asarray([g_amp, g_sig, g_xcen, g_ycen, g_axrat, g_pa])
    lpar = np.asarray([l_amp, l_xcen, l_ycen, l_axrat, l_pa])
    
    #g_image = ldf.gauss_2d(x, y, gpar)
    (xg, yg) = ldf.sie_grad(x, y, lpar)
    g_lensimage = ldf.gauss_2d(x-xg, y-yg, gpar)
    f.set_data(g_lensimage)
    fig.canvas.draw_idle()

slaxrat.on_changed(update)
sgaxrat.on_changed(update)
sgycen.on_changed(update)
sgxcen.on_changed(update)
sgpa.on_changed(update)

plt.show()
