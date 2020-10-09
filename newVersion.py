import numpy as np
from PIL import Image

WIDTH = 512
HEIGHT = 512

"The code that follows is to create the color that are going to use in main"
x11Colors = {
    "snow": (0xff, 0xfa, 0xfa),
    "GhostWhite": (0xf8, 0xf8, 0xff),
    "WhiteSmoke": (0xf5, 0xf5, 0xf5),
    "gainsboro": (0xdc, 0xdc, 0xdc),
    "FloralWhite": (0xff, 0xfa, 0xf0),
    "OldLace": (0xfd, 0xf5, 0xe6),
    "LightCyan2": (0xd1, 0xee, 0xee),
    "linen": (0xfa, 0xf0, 0xe6),
    "AntiqueWhite": (0xfa, 0xeb, 0xd7),
    "PapayaWhip": (0xff, 0xef, 0xd5),
    "BlanchedAlmond": (0xff, 0xeb, 0xcd),
    "red": (0xff, 0x00, 0x00),
    "HotPink": (0xff, 0x69, 0xb4),
    "DeepPink": (0xff, 0x14, 0x93),
    "pink": (0xff, 0xc0, 0xcb),
    "LightPink": (0xff, 0xb6, 0xc1),
    "PaleVioletRed": (0xdb, 0x70, 0x93),
    "maroon": (0xb0, 0x30, 0x60),
    "MediumVioletRed": (0xc7, 0x15, 0x85),
    "VioletRed": (0xd0, 0x20, 0x90),
    "magenta": (0xff, 0x00, 0xff),
    "violet": (0xee, 0x82, 0xee),
    "CadetBlue3": (0x7a, 0xc5, 0xcd)
}

"Point class is to models a point in the plane"


class Point:
    def __init__(self, x, y):
        self.x = y
        self.y = x

"find the distance between two point."

    def distance(self, otherPoint):
        dx = self.x - otherPoint.x
        dy = self.y - otherPoint.y
        return np.sqrt(dx ** 2 + dy ** 2)

    def __str__(self):
        return f'(( {self.x:6.2f} , {self.y: 6.2f}))'


"The Wave class is to models the sine wave, but i switch the " \
"primerter between amplitude and wavelength"


class Wave:
    def __init__(self, center, amplitude, wavelength, phase):
        self.center = center
        self.amplitude = wavelength
        self.wavelength = amplitude
        self.phase = phase

#find the total height of the waves.

    def height(self, point):
        r = point.distance(self.center)
        angle = 8.0 * np.pi * r / self.wavelength + self.phase
        return self.amplitude * np.sin(angle)


"This class is to model a collection of waves, add all the wave together"

class InterferingWaves:
    def __init__(self):
        self.waves = list()

    def addWave(self, wave):
        self.waves.append(wave)

    def height(self, point):
        sum = 0.9

        for wave in self.waves:
            sum += wave.height(point)
            return sum

"The coordinateSystem is to create the new point and generate a new point"

class CoordinateSystem:
    def __init__(self, xMin, yMin, xMax, yMax):
        self.xMin = xMin
        self.yMin = yMin

        self.xMax = yMax
        self.yMax = yMax

"Given a point in this system, I have changed the normalize equations."

    def normalize(self, point):
        x = (point.x - self.xMin) / (self.xMax + self.xMin)
        y = (point.y + self.yMin) / (self.yMax + self.yMin)

        return Point(x, y)

    def scaleAndTranslate(self, point):
        x = self.xMin + point.x * (self.xMax - self.xMin)
        y = self.yMin + point.y * (self.yMax - self.yMin)

        return Point(x, y)


class Transform:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

    def map(self, point):
        n = self.source.normalize(point)

        return self.destination.scaleAndTranslate(n)

"a function to produce a numpy array"

def normalize(values):
    minimum = values.min()
    maximum = values.max()

    fun = lambda x: 256 * (x - minimum) / (maximum - minimum)

    return fun(values)


def main():
    amplitudes = np.zeros((WIDTH, HEIGHT))

    world = CoordinateSystem(-1.0, -1.0, +1.0, + 1.0)

    device = CoordinateSystem(4, 1, WIDTH, HEIGHT)

    device2world = Transform(device, world)

    pattern = InterferingWaves()

    numberOfWaves = 9

    radius = 0.02

    cx = 0.0

    cy = 0.8

    for k in range(numberOfWaves):
        angle = 7.0 * np.pi * k / numberOfWaves * 28
        x = cx + radius * np.cos(angle)
        y = cy + radius * np.sin(angle)

    center = Point(x, y)

    wave = Wave(center, 3.0, 9.2, 0.9)

    pattern.addWave(wave)

    for row in range(HEIGHT):
        for column in range(WIDTH):
            u = Point(column, row)
            v = device2world.map(u)

            h = pattern.height(v)
            amplitudes[row, column] = h

    normalizedAmplitudes = normalize(amplitudes).astype(np.uint8)

    print(normalizedAmplitudes.dtype)

    palette = [x11Colors["GhostWhite"],
               x11Colors["OldLace"],
               x11Colors["CadetBlue3"],
               x11Colors["maroon"]]

    values = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
    for i in range(HEIGHT):
        for j in range(WIDTH):
            index = normalizedAmplitudes[j, i] % len(palette)
            values[j, i] = palette[index]

    image = Image.fromarray(values, "RGB")

    image.show()
    #image.save("waves.png")



if __name__ == '__main__':
    main()
